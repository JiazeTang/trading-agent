"""策略体检：概率夏普比、紧缩夏普比、最短业绩长度，以及蒙特卡洛风险分布和停用标准。

    python -m riskeval.strategy_health --out reports/strategy_health

以下设定在看结果之前写死：

- 对象：M1 规则 A（半导体部分 4000 单独运行）；M2 核心 60% SMH + 规则 A（当前方案）。
  2016 年起，扣单边 0.05% 成本。对照：SMH、QQQ 一直持有。
- 概率夏普比 PSR（Bailey & López de Prado 2012）：用日收益的 Sharpe、偏度、峰度，
  算"真实 Sharpe 高于基准"的概率。基准取 0 和年化 0.5。全期和 2023 年以后分别算。
- 最短业绩长度 MinTRL：在 95% 置信度下，至少要多少年的数据才能确认 Sharpe 高于基准。
- 紧缩夏普比 DSR：把基准换成"N 个独立试验里光靠运气能得到的最大 Sharpe 的期望值"，
  N 取 10 / 50 / 100。本项目到 2026-10 实际试过的规则变体大约有几十个。
- 蒙特卡洛：对日收益做平稳块重抽样（平均块长 20 个交易日，保留波动聚集），生成 10,000 条 1 年路径，
  统计 1 年收益、最大回撤、最长水下天数的分布。另对规则 A 的逐笔交易重抽样（每年笔数按历史平均），
  统计一年里最长连亏笔数和平均每笔收益。
- 停用标准：实盘或模拟盘出现以下任一情况，就暂停新开仓并复盘：
  滚动 1 年最大回撤比模拟的 95% 分位更深；连亏笔数超过模拟的 99% 分位；滚动 1 年收益低于模拟的 5% 分位。
"""

from __future__ import annotations

import argparse
import json
from math import e, sqrt
from pathlib import Path
from statistics import NormalDist

import numpy as np
import pandas as pd

from riskeval.mr_screen import TARGETS

TRADING_DAYS = 252
START = pd.Timestamp("2016-01-01")
SPLIT = pd.Timestamp("2023-01-01")
COST = 0.0005
EULER = 0.5772156649
TRIALS = [10, 50, 100]
PATHS, BLOCK, HORIZON = 10_000, 20, TRADING_DAYS
N = NormalDist()


# ---------- 夏普比的统计 ----------

def moments(returns: pd.Series) -> tuple[float, float, float, int]:
    """日 Sharpe、偏度、峰度（正态分布为 3）和样本数。"""
    r = returns.dropna().to_numpy()
    mean, sd = r.mean(), r.std(ddof=1)
    centred = r - mean
    skew = (centred ** 3).mean() / sd ** 3
    kurt = (centred ** 4).mean() / sd ** 4
    return mean / sd, skew, kurt, len(r)


def _sr_variance(sr: float, skew: float, kurt: float) -> float:
    return 1 - skew * sr + (kurt - 1) / 4 * sr ** 2


def psr(returns: pd.Series, benchmark_annual: float = 0.0) -> float:
    """真实年化 Sharpe 高于 benchmark_annual 的概率。"""
    sr, skew, kurt, n = moments(returns)
    star = benchmark_annual / sqrt(TRADING_DAYS)
    return N.cdf((sr - star) * sqrt(n - 1) / sqrt(_sr_variance(sr, skew, kurt)))


def min_track_record_years(returns: pd.Series, benchmark_annual: float = 0.0, confidence: float = 0.95) -> float:
    sr, skew, kurt, _ = moments(returns)
    star = benchmark_annual / sqrt(TRADING_DAYS)
    if sr <= star:
        return float("inf")
    periods = 1 + _sr_variance(sr, skew, kurt) * (N.inv_cdf(confidence) / (sr - star)) ** 2
    return periods / TRADING_DAYS


def expected_max_sharpe(trials: int, sr_variance: float) -> float:
    """N 个独立试验、真实 Sharpe 都为 0 时，样本 Sharpe 最大值的期望（日频单位）。"""
    return sqrt(sr_variance) * ((1 - EULER) * N.inv_cdf(1 - 1 / trials) + EULER * N.inv_cdf(1 - 1 / (trials * e)))


def dsr(returns: pd.Series, trials: int) -> tuple[float, float]:
    """紧缩夏普比，以及对应的"运气门槛"（年化 Sharpe）。"""
    sr, skew, kurt, n = moments(returns)
    star = expected_max_sharpe(trials, _sr_variance(sr, skew, kurt) / (n - 1))
    probability = N.cdf((sr - star) * sqrt(n - 1) / sqrt(_sr_variance(sr, skew, kurt)))
    return probability, star * sqrt(TRADING_DAYS)


def sharpe_table(series: dict[str, pd.Series]) -> pd.DataFrame:
    rows = []
    for name, r in series.items():
        for period, part in {"2016年起": r, "2023年起": r[r.index >= SPLIT]}.items():
            sr, skew, kurt, n = moments(part)
            row = {"对象": name, "区间": period, "年数": n / TRADING_DAYS, "年化Sharpe": sr * sqrt(TRADING_DAYS),
                   "偏度": skew, "峰度": kurt, "PSR(>0)": psr(part, 0.0), "PSR(>0.5)": psr(part, 0.5),
                   "最短年数(>0)": min_track_record_years(part, 0.0), "最短年数(>0.5)": min_track_record_years(part, 0.5)}
            for trials in TRIALS:
                probability, hurdle = dsr(part, trials)
                row[f"DSR(N={trials})"] = probability
                row[f"运气门槛(N={trials})"] = hurdle
            rows.append(row)
    return pd.DataFrame(rows)


# ---------- 蒙特卡洛 ----------

def stationary_bootstrap(returns: np.ndarray, paths: int = PATHS, horizon: int = HORIZON,
                         block: int = BLOCK, seed: int = 0) -> np.ndarray:
    """平稳块重抽样：每一步以 1/block 的概率跳到随机位置，否则接着取下一天。"""
    rng = np.random.default_rng(seed)
    n = len(returns)
    jumps = rng.random((paths, horizon)) < 1 / block
    starts = rng.integers(0, n, (paths, horizon))
    idx = np.empty((paths, horizon), dtype=int)
    idx[:, 0] = starts[:, 0]
    for t in range(1, horizon):
        idx[:, t] = np.where(jumps[:, t], starts[:, t], (idx[:, t - 1] + 1) % n)
    return returns[idx]


def path_risk(sampled: np.ndarray) -> dict[str, np.ndarray]:
    wealth = np.cumprod(1 + sampled, axis=1)
    peak = np.maximum.accumulate(np.maximum(wealth, 1.0), axis=1)
    drawdown = wealth / peak - 1
    underwater = drawdown < 0
    longest = np.zeros(len(sampled), dtype=int)
    current = np.zeros(len(sampled), dtype=int)
    for t in range(sampled.shape[1]):
        current = np.where(underwater[:, t], current + 1, 0)
        longest = np.maximum(longest, current)
    return {"一年收益": wealth[:, -1] - 1, "最大回撤": drawdown.min(axis=1), "最长水下天数": longest}


def longest_losing_streak(outcomes: np.ndarray) -> np.ndarray:
    """每一行里连续亏损（≤0）的最长笔数。"""
    longest = np.zeros(len(outcomes), dtype=int)
    current = np.zeros(len(outcomes), dtype=int)
    for t in range(outcomes.shape[1]):
        current = np.where(outcomes[:, t] <= 0, current + 1, 0)
        longest = np.maximum(longest, current)
    return longest


def trade_bootstrap(trade_returns: np.ndarray, per_year: int, paths: int = PATHS, seed: int = 1) -> dict[str, np.ndarray]:
    rng = np.random.default_rng(seed)
    sampled = trade_returns[rng.integers(0, len(trade_returns), (paths, per_year))]
    return {"最长连亏笔数": longest_losing_streak(sampled), "平均每笔收益": sampled.mean(axis=1)}


def summarize(dist: dict[str, np.ndarray], name: str) -> list[dict]:
    rows = []
    for metric, values in dist.items():
        q = np.quantile(values, [0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99])
        rows.append({"对象": name, "指标": metric, "1%": q[0], "5%": q[1], "25%": q[2], "中位": q[3],
                     "75%": q[4], "95%": q[5], "99%": q[6], "小于0的概率": float((values < 0).mean())})
    return rows


def historical_worst(returns: pd.Series) -> dict[str, float]:
    """历史上任意滚动 1 年里的最差收益和最深回撤，用来和模拟分布对照。"""
    wealth = (1 + returns).cumprod()
    yearly = wealth / wealth.shift(HORIZON) - 1
    worst_dd = 0.0
    values = wealth.to_numpy()
    for i in range(HORIZON, len(values), 5):
        window = values[i - HORIZON:i + 1] / values[i - HORIZON]
        worst_dd = min(worst_dd, (window / np.maximum.accumulate(np.maximum(window, 1.0)) - 1).min())
    return {"历史最差滚动1年收益": float(yearly.min()), "历史最深滚动1年回撤": worst_dd}


# ---------- 主流程 ----------

def build_series(closes: pd.DataFrame) -> tuple[dict[str, pd.Series], dict[str, pd.DataFrame]]:
    from riskeval.structure_study import CAPITAL, VARIANTS, build_rules, simulate
    from riskeval.style_compare import net_daily_returns

    semis = [t for ts in TARGETS.values() for t in ts if t in closes.columns]
    rules = build_rules(closes[semis])
    series, logs = {}, {}
    for label, key in {"M1 规则A": "现行A：单只信号+回到中轨，等额3仓",
                       "M2 核心60%SMH+规则A（当前方案）": "核心60% SMH + A加码(2仓)"}.items():
        equity, _, log = simulate(closes[semis], closes["SMH"], rules, START, **VARIANTS[key])
        series[label] = net_daily_returns(equity, log, COST, CAPITAL)
        logs[label] = log
    for etf in ["SMH", "QQQ"]:
        r = closes[etf].pct_change(fill_method=None)
        series[f"对照：{etf} 一直持有"] = r[r.index >= START].dropna()
    return series, logs


def run(closes: pd.DataFrame) -> dict:
    series, logs = build_series(closes)
    sharpe = sharpe_table(series)
    risk_rows, worst_rows, kill = [], [], []
    for name, r in series.items():
        dist = path_risk(stationary_bootstrap(r.to_numpy()))
        risk_rows += summarize(dist, name)
        worst_rows.append({"对象": name} | historical_worst(r))
        entry = {"对象": name,
                 "停用线：滚动1年回撤深于": float(np.quantile(dist["最大回撤"], 0.05)),
                 "停用线：滚动1年收益低于": float(np.quantile(dist["一年收益"], 0.05)),
                 "停用线：连亏笔数超过": np.nan}
        if name in logs:
            log = logs[name]
            years = len(r) / TRADING_DAYS
            per_year = max(int(round(len(log) / years)), 1)
            trades = trade_bootstrap(log["收益"].to_numpy(dtype=float), per_year)
            risk_rows += summarize(trades, name + f"（逐笔，每年{per_year}笔）")
            entry["停用线：连亏笔数超过"] = int(np.quantile(trades["最长连亏笔数"], 0.99))
            entry["历史最长连亏笔数"] = int(longest_losing_streak(log["收益"].to_numpy(dtype=float)[None, :])[0])
        kill.append(entry)
    return {"sharpe": sharpe, "risk": pd.DataFrame(risk_rows), "worst": pd.DataFrame(worst_rows),
            "kill": pd.DataFrame(kill)}


PLAIN = {"年数", "年化Sharpe", "偏度", "峰度", "最短年数(>0)", "最短年数(>0.5)", "历史最长连亏笔数",
         "停用线：连亏笔数超过"} | {f"运气门槛(N={t})" for t in TRIALS}


def _render(table: pd.DataFrame, plain: set[str] | None = None) -> str:
    plain = PLAIN | (plain or set())
    table = table.copy()
    for column in table.columns:
        if table[column].dtype.kind in "fi":
            if column in plain:
                table[column] = table[column].map(lambda x: "" if pd.isna(x) else ("∞" if np.isinf(x) else f"{round(x, 2) + 0.0:.2f}".rstrip("0").rstrip(".")))
            else:
                table[column] = table[column].map(lambda x: "" if pd.isna(x) else f"{x:.1%}")
    header = "| " + " | ".join(map(str, table.columns)) + " |"
    body = ["| " + " | ".join(map(str, row)) + " |" for row in table.itertuples(index=False)]
    return "\n".join([header, "|" + "---|" * len(table.columns), *body])


def write_report(results: dict, out: Path, data_end) -> None:
    out.mkdir(parents=True, exist_ok=True)
    for name in ["sharpe", "risk", "worst", "kill"]:
        results[name].to_csv(out / f"{name}.csv", index=False)
    (out / "summary.json").write_text(json.dumps(
        {k: v.replace({np.inf: None}).to_dict("records") for k, v in results.items()}, ensure_ascii=False, default=float, indent=1),
        encoding="utf-8")
    s = results["sharpe"]
    psr_cols = ["对象", "区间", "年数", "年化Sharpe", "偏度", "峰度", "PSR(>0)", "PSR(>0.5)", "最短年数(>0)", "最短年数(>0.5)"]
    dsr_cols = ["对象", "区间"] + [c for t in TRIALS for c in (f"运气门槛(N={t})", f"DSR(N={t})")]
    risk = results["risk"]
    count_metrics = risk["指标"].isin(["最长水下天数", "最长连亏笔数"])
    sections = [
        f"# 策略体检（数据截至 {data_end:%Y-%m-%d}）\n\n由 `python -m riskeval.strategy_health` 生成，设定见该模块说明。"
        "规则输出加历史回测，不是投资建议。16 只半导体按今天的市值挑选，有幸存者偏差，M1、M2 的结果偏乐观。",
        "## 概率夏普比（PSR）和最短业绩长度\n\nPSR(>0)：真实 Sharpe 大于 0 的概率；PSR(>0.5)：大于年化 0.5 的概率。"
        "最短年数：在 95% 置信度下，至少要多少年的数据才能确认。\n\n" + _render(s[psr_cols]),
        "## 紧缩夏普比（DSR）：扣掉\"试了很多次\"的运气\n\n运气门槛：试 N 个毫无优势的版本，光靠运气能得到的最高年化 Sharpe 的期望。"
        "DSR：真实 Sharpe 高于这个门槛的概率。\n\n" + _render(s[dsr_cols]),
        "## 蒙特卡洛：未来一年的风险分布（10,000 条路径）\n\n收益和回撤是百分比；水下天数和连亏笔数是数量。\n\n"
        + _render(risk[~count_metrics]) + "\n\n" + _render(risk[count_metrics], {"1%", "5%", "25%", "中位", "75%", "95%", "99%"}),
        "## 历史上最差的滚动一年（和模拟分布对照）\n\n" + _render(results["worst"]),
        "## 事先定死的停用标准\n\n实盘或模拟盘出现任意一条，就暂停新开仓并复盘：\n\n" + _render(results["kill"]),
    ]
    (out / "README.md").write_text("\n\n".join(sections) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> None:
    from riskeval import daily_data

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", default="reports/strategy_health")
    args = parser.parse_args(argv)

    semis = [t for ts in TARGETS.values() for t in ts]
    closes = daily_data.download_closes(semis + ["SMH", "QQQ"], "2015-01-01", chunk=50)
    write_report(run(closes), Path(args.out), closes.index[-1])
    print(f"已写入 {args.out}/README.md")


if __name__ == "__main__":
    main()
