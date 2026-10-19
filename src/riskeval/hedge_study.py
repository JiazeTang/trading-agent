"""对冲测试：半导体均值回归多头，要不要用生物科技或消费电子来对冲 / 分散。

    python -m riskeval.hedge_study --out reports/hedge_study

设定（看结果之前写死）：
- 多头：16 只半导体股里"板块普跌 + 200 日线上方 + 跌破布林下轨"的每段信号第一天，次日收盘买入，持有 42 个交易日（约 2 个月）。
  这就是 mr_screen 里持有 2 个月的规则。
- 每个候选 H 都做三种组合，逐日计算：
  * 不对冲：只持有半导体多头；
  * 做空对冲：多头 1 份，做空 β 份 H。β 用入场前 120 个交易日的日收益回归，限制在 0–3；
  * 搭配做多：半导体和 H 各一半。
- 评价看：2 个月收益的均值、胜率、标准差、平均 / 最差持有期最大浮亏。对冲有没有用，看它降了多少风险、花了多少收益。
- 另外给出每个候选和半导体篮子（NVDA / TSM / MU 等权）的相关性、半导体大跌日的相关性，以及它现在的均值回归状态。
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from riskeval import signals
from riskeval.mr_screen import SELLOFF_SHARE, TARGETS

CANDIDATES = {
    "生物科技": ["XBI", "IBB", "AMGN", "GILD", "VRTX", "REGN", "ALNY", "ARGX", "INSM", "BIIB"],
    "消费电子": ["AAPL", "SONY", "DELL", "HPQ", "LOGI", "GRMN"],
    "参照(常用对冲工具)": ["SMH", "QQQ", "SPY"],
}
CURRENT_LONGS = ["NVDA", "TSM", "MU"]
HOLD = 42
BETA_WINDOW = 120


def entries(semis: pd.DataFrame) -> list[tuple[pd.Timestamp, str]]:
    """持有 2 个月规则的入场：板块普跌 + 200 日线上方 + 跌破下轨，每段信号只取第一天。"""
    z = signals.zscore(semis)
    below = z <= -2
    breadth = below.sum(axis=1) / z.notna().sum(axis=1).replace(0, np.nan)
    selloff = breadth >= SELLOFF_SHARE
    rule = below.apply(lambda c: c & selloff) & (semis > signals.sma(semis, 200))
    rule = rule.fillna(False).astype(bool)
    first = rule & ~rule.shift(1, fill_value=False)
    first = first[first.index >= "2016-01-01"]
    return [(d, t) for d, t in first.stack()[lambda s: s].index]


def _path_stats(daily: np.ndarray) -> tuple[float, float]:
    equity = np.cumprod(1 + daily)
    return equity[-1] - 1, min(equity.min() - 1, 0.0)


def trades(closes: pd.DataFrame, longs: list[tuple[pd.Timestamp, str]], hedge: str) -> pd.DataFrame:
    """每笔多头入场在三种组合下的 2 个月收益和最大浮亏。"""
    rets = closes.pct_change(fill_method=None)
    index = closes.index
    rows = []
    for day, ticker in longs:
        t = index.get_loc(day)
        if t + 1 + HOLD >= len(index):
            continue
        hold = slice(t + 2, t + 2 + HOLD)
        long_r = rets[ticker].iloc[hold].to_numpy()
        hedge_r = rets[hedge].iloc[hold].to_numpy()
        past = rets[[ticker, hedge]].iloc[max(0, t - BETA_WINDOW + 1):t + 1].dropna()
        if np.isnan(long_r).any() or np.isnan(hedge_r).any() or len(past) < BETA_WINDOW // 2:
            continue
        beta = float(np.clip(past.cov().iloc[0, 1] / past[hedge].var(), 0, 3))
        row = {"date": day, "ticker": ticker, "beta": beta}
        for name, daily in {"不对冲": long_r, "做空对冲": long_r - beta * hedge_r, "搭配做多": 0.5 * (long_r + hedge_r)}.items():
            row[f"{name}·收益"], row[f"{name}·最大浮亏"] = _path_stats(daily)
        rows.append(row)
    return pd.DataFrame(rows)


def summarize_hedges(closes: pd.DataFrame, longs, group_of: dict[str, str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    summary, detail = [], []
    for hedge, group in group_of.items():
        t = trades(closes, longs, hedge)
        if t.empty:
            continue
        for combo in ["不对冲", "做空对冲", "搭配做多"]:
            ret, mae = t[f"{combo}·收益"], t[f"{combo}·最大浮亏"]
            summary.append({
                "候选": hedge, "板块": group, "组合": combo, "笔数": len(t), "平均β": t["beta"].mean(),
                "胜率": (ret > 0).mean(), "平均收益": ret.mean(), "中位收益": ret.median(), "收益标准差": ret.std(),
                "最差收益": ret.min(), "平均最大浮亏": mae.mean(), "最差最大浮亏": mae.min(),
            })
        detail.append(t.assign(候选=hedge))
    return pd.DataFrame(summary), pd.concat(detail, ignore_index=True) if detail else pd.DataFrame()


def correlations(closes: pd.DataFrame, group_of: dict[str, str], end) -> pd.DataFrame:
    """和半导体篮子（NVDA / TSM / MU 等权）的日收益相关性和 β。"""
    rets = closes.pct_change(fill_method=None)
    basket = rets[CURRENT_LONGS].mean(axis=1)
    last_year = rets.index > end - pd.Timedelta(days=365)
    down = basket <= -0.02
    rows = []
    for hedge, group in group_of.items():
        h = rets[hedge]
        rows.append({
            "候选": hedge, "板块": group,
            "相关性(2016起)": basket[rets.index >= "2016-01-01"].corr(h),
            "相关性(近一年)": basket[last_year].corr(h[last_year]),
            "β(近一年)": basket[last_year].cov(h[last_year]) / h[last_year].var(),
            "半导体大跌日(≤-2%)它的平均涨跌": h[down & last_year].mean(),
            "半导体大跌日它也跌的比例": (h[down & last_year] < 0).mean(),
        })
    return pd.DataFrame(rows)


def current_state(closes: pd.DataFrame, group_of: dict[str, str]) -> pd.DataFrame:
    day = closes.index[-1]
    c = closes[list(group_of)]
    z = signals.zscore(c).loc[day]
    return pd.DataFrame({
        "板块": pd.Series(group_of),
        "布林z值": z.round(2),
        "均值回归状态": np.select([z <= -2, z <= -1.5, z >= 2], ["跌破下轨(超卖)", "接近下轨", "突破上轨(超买)"], "中性"),
        "200日线上方": (c > signals.sma(c, 200)).loc[day],
        "近20日涨跌": (c / c.shift(20) - 1).loc[day],
        "距52周高点": (c / c.rolling(252, min_periods=60).max() - 1).loc[day],
    }).rename_axis(f"候选({day.date()})").reset_index()


def run(closes: pd.DataFrame) -> dict[str, pd.DataFrame]:
    semis = [t for ts in TARGETS.values() for t in ts if t in closes.columns]
    group_of = {t: g for g, ts in CANDIDATES.items() for t in ts if t in closes.columns}
    longs = entries(closes[semis])
    summary, detail = summarize_hedges(closes, longs, group_of)
    end = closes.index[-1]
    return {
        "summary": summary,
        "trades": detail,
        "correlations": correlations(closes, group_of, end),
        "current": current_state(closes, group_of),
    }


PERCENT = ["胜率", "平均收益", "中位收益", "收益标准差", "最差收益", "平均最大浮亏", "最差最大浮亏", "近20日涨跌", "距52周高点",
           "半导体大跌日(≤-2%)它的平均涨跌", "半导体大跌日它也跌的比例"]


def write_report(results: dict[str, pd.DataFrame], out: Path, data_end) -> None:
    out.mkdir(parents=True, exist_ok=True)
    for name, table in results.items():
        table.to_csv(out / f"{name}.csv", index=False)

    def fmt(table):
        table = table.copy()
        for column in table.columns:
            if column in PERCENT:
                table[column] = table[column].map(lambda x: "" if pd.isna(x) else f"{x:.1%}")
            elif table[column].dtype.kind == "f":
                table[column] = table[column].map(lambda x: "" if pd.isna(x) else f"{x:.2f}")
        header = "| " + " | ".join(map(str, table.columns)) + " |"
        body = ["| " + " | ".join(map(str, row)) + " |" for row in table.itertuples(index=False)]
        return "\n".join([header, "|" + "---|" * len(table.columns), *body]) if len(table) else "（无）"

    s = results["summary"]
    base = s[s["组合"] == "不对冲"].iloc[:1][["组合", "笔数", "胜率", "平均收益", "中位收益", "收益标准差", "最差收益", "平均最大浮亏", "最差最大浮亏"]]
    cols = ["候选", "板块", "平均β", "胜率", "平均收益", "中位收益", "收益标准差", "最差收益", "平均最大浮亏", "最差最大浮亏"]
    sections = [
        f"# 对冲测试：半导体均值回归多头（持有 2 个月）\n\n数据截至 {data_end:%Y-%m-%d}。由 `python -m riskeval.hedge_study` 生成，设定见该模块说明。"
        "历史入场从 2016 年开始；样本是少数几次板块普跌里的多笔入场，彼此高度相关。",
        "## 不对冲的基准\n\n" + fmt(base),
        "## 做空对冲（多头 1 份，做空 β 份候选）\n\n" + fmt(s[s["组合"] == "做空对冲"][cols]),
        "## 搭配做多（半导体和候选各一半）\n\n" + fmt(s[s["组合"] == "搭配做多"][cols]),
        "## 和半导体篮子（NVDA / TSM / MU）的相关性\n\n" + fmt(results["correlations"]),
        "## 候选现在的均值回归状态\n\n" + fmt(results["current"]),
    ]
    (out / "README.md").write_text("\n\n".join(sections) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> None:
    from riskeval import daily_data

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--start", default="2015-01-01")
    parser.add_argument("--out", default="reports/hedge_study")
    args = parser.parse_args(argv)

    tickers = sorted({t for ts in TARGETS.values() for t in ts} | {t for ts in CANDIDATES.values() for t in ts})
    closes = daily_data.download_closes(tickers, args.start, chunk=50)
    missing = [t for t in tickers if t not in closes.columns]
    if missing:
        print("以下代码没有下载到数据，本次跳过：", missing)
    results = run(closes)
    write_report(results, Path(args.out), closes.index[-1])
    print(f"已写入 {args.out}/README.md")


if __name__ == "__main__":
    main()
