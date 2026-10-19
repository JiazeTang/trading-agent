"""结构改进回测：波动率定仓 + 半导体组风险上限，以及"核心仓 + 超跌加码"。

    python -m riskeval.structure_study --out reports/structure_study

只看半导体部分（4000，即 8000 计划里的一半）。以下设定在看结果之前写死：

- 信号：规则 A（单只跌破 20 日布林下轨且在 200 日线上方）或规则 B（另外要求 16 只里至少一半同时跌破下轨），
  次日收盘买入；按 z 值从低到高排队。出场：-20% 止损；规则 B 持有满 42 天，规则 A 回到 20 日均线就卖。
- 等额：每个仓位 = 加码资金当前净值 ÷ 仓位数。
- 波动率定仓：在等额基础上乘以 min(1, 30% ÷ 该股入场前 20 日年化波动)，波动越大买得越少。
- 组风险上限：单只股票仓位合计不超过半导体部分净值的 64%。
  依据：8000 账户的半导体单股组合在 25% 压力跳空下最多亏总资金的 8%，即 8000 × 8% ÷ 25% = 2560 = 4000 的 64%。
- 核心仓：60% 买入 SMH 一直持有，剩下 40% 分 2 个仓位做超跌加码。SMH 是分散的 ETF，不计入单股组上限。
- 评价：2016 年起的年化收益、波动、最大回撤、最差一天、最差 5% 日均值（CVaR），
  收益 ÷ 波动，所有长度与 2026-06-01 至今相同的时间段的收益分布，2016–2022 和 2023 年后分段，
  以及 2026-06-01 起重新开始的结果。
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from riskeval import signals
from riskeval.mr_screen import SELLOFF_SHARE, TARGETS

CAPITAL = 4000.0
HISTORY_START = pd.Timestamp("2016-01-01")
PERIOD_START = pd.Timestamp("2026-06-01")
SPLIT = pd.Timestamp("2023-01-01")
STOP, MAX_HOLD = -0.20, 42
TARGET_VOL, VOL_FLOOR = 0.30, 0.10
GROUP_CAP = 0.64
CORE = "SMH"

VARIANTS = {
    "现行B：板块普跌+满42天，等额3仓": dict(rule="B", slots=3, sizing="equal", cap=False, core=0.0),
    "现行A：单只信号+回到中轨，等额3仓": dict(rule="A", slots=3, sizing="equal", cap=False, core=0.0),
    "B + 波动率定仓 + 组上限": dict(rule="B", slots=3, sizing="vol", cap=True, core=0.0),
    "A + 波动率定仓 + 组上限": dict(rule="A", slots=3, sizing="vol", cap=True, core=0.0),
    "核心60% SMH + B加码(2仓)": dict(rule="B", slots=2, sizing="equal", cap=False, core=0.6),
    "核心60% SMH + A加码(2仓)": dict(rule="A", slots=2, sizing="equal", cap=False, core=0.6),
    "核心60% SMH + A加码(波动率定仓+组上限)": dict(rule="A", slots=2, sizing="vol", cap=True, core=0.6),
}


def build_rules(px: pd.DataFrame) -> dict[str, pd.DataFrame]:
    z = signals.zscore(px)
    below = z <= -2
    rule_a = (below & (px > signals.sma(px, 200))).fillna(False)
    breadth = below.sum(axis=1) / z.notna().sum(axis=1).replace(0, np.nan)
    rule_b = rule_a.apply(lambda c: c & (breadth >= SELLOFF_SHARE)).fillna(False)
    return {"A": rule_a, "B": rule_b, "z": z}


def simulate(px: pd.DataFrame, core_px: pd.Series, rules: dict, start, rule: str, slots: int,
             sizing: str, cap: bool, core: float) -> tuple[pd.Series, pd.Series, pd.DataFrame]:
    """返回（每日净值, 每日单股仓位占净值比例, 交易记录）。"""
    z, signal = rules["z"], rules[rule]
    vol = px.pct_change(fill_method=None).rolling(20).std() * np.sqrt(252)
    exit_mean = rule == "A"
    days = px.index[px.index >= start]
    core_shares = core * CAPITAL / core_px[days[0]]
    cash, open_, pending = CAPITAL * (1 - core), {}, []
    equity, exposure, log = {}, {}, []

    for day in days:
        price = px.loc[day]
        for t in list(open_):
            pos = open_[t]
            pos["held"] += 1
            change = price[t] / pos["entry"] - 1
            reason = ("止损" if change <= STOP else
                      "回到中轨" if exit_mean and z.at[day, t] >= 0 else
                      "到期" if not exit_mean and pos["held"] >= MAX_HOLD else None)
            if reason:
                cash += pos["shares"] * price[t]
                log.append({"股票": t, "买入日": pos["date"].date(), "卖出日": day.date(), "收益": change,
                            "仓位": pos["size"], "原因": reason})
                del open_[t]
        stocks = sum(p["shares"] * price[t] for t, p in open_.items())
        total = core_shares * core_px[day] + cash + stocks
        overlay = cash + stocks
        for t in pending:
            if len(open_) >= slots or t in open_ or np.isnan(price[t]):
                continue
            size = overlay / slots
            if sizing == "vol":
                size *= min(1.0, TARGET_VOL / max(vol.at[day, t], VOL_FLOOR))
            if cap:
                size = min(size, GROUP_CAP * total - stocks)
            size = min(size, cash)
            if size < 1:
                continue
            open_[t] = {"entry": price[t], "shares": size / price[t], "date": day, "held": 0, "size": size}
            cash -= size
            stocks += size
        today = signal.loc[day]
        pending = list(z.loc[day][today[today].index].sort_values().index)
        total = core_shares * core_px[day] + cash + stocks
        equity[day], exposure[day] = total, stocks / total
    return pd.Series(equity), pd.Series(exposure), pd.DataFrame(log)


def stats(equity: pd.Series, window: int) -> dict:
    daily = equity.pct_change().dropna()
    years = len(daily) / 252
    cagr = (equity.iloc[-1] / equity.iloc[0]) ** (1 / years) - 1
    vol = daily.std() * np.sqrt(252)
    roll = (equity / equity.shift(window) - 1).dropna()
    worst5 = daily[daily <= daily.quantile(0.05)].mean()
    out = {"年化收益": cagr, "年化波动": vol, "收益/波动": cagr / vol if vol else np.nan,
           "最大回撤": (equity / equity.cummax() - 1).min(), "最差一天": daily.min(), "最差5%日均值": worst5,
           "同长度时段中位收益": roll.median(), "同长度时段最差10%": roll.quantile(0.1), "同长度时段亏钱比例": (roll < 0).mean()}
    for label, part in {"2016-22": equity[equity.index < SPLIT], "2023后": equity[equity.index >= SPLIT]}.items():
        d = part.pct_change().dropna()
        out[f"{label}年化"] = (part.iloc[-1] / part.iloc[0]) ** (252 / len(d)) - 1
        out[f"{label}最大回撤"] = (part / part.cummax() - 1).min()
    return out


def run(closes: pd.DataFrame) -> dict[str, pd.DataFrame]:
    semis = [t for ts in TARGETS.values() for t in ts if t in closes.columns]
    px, core_px = closes[semis], closes[CORE]
    rules = build_rules(px)
    window = int((px.index >= PERIOD_START).sum())
    rows, logs = [], {}
    for name, v in VARIANTS.items():
        eq, expo, log = simulate(px, core_px, rules, HISTORY_START, **v)
        recent, _, recent_log = simulate(px, core_px, rules, PERIOD_START, **v)
        rows.append({"方案": name} | stats(eq, window) | {
            "平均单股仓位占比": expo.mean(), "每年交易笔数": len(log) / (len(eq) / 252),
            "6月1日起收益": recent.iloc[-1] / CAPITAL - 1, "6月1日起最大回撤": (recent / recent.cummax() - 1).min(),
        })
        logs[name] = recent_log
    hold_days = px.index[px.index >= HISTORY_START]
    smh = CAPITAL * core_px[hold_days] / core_px[hold_days[0]]
    ew = CAPITAL * (1 + px.loc[hold_days].pct_change(fill_method=None).mean(axis=1).fillna(0)).cumprod()
    for name, eq in {"对照：100% SMH 持有": smh, "对照：16只等权持有(幸存者偏差)": ew}.items():
        recent = eq[eq.index >= PERIOD_START]
        rows.append({"方案": name} | stats(eq, window) | {
            "平均单股仓位占比": np.nan, "每年交易笔数": 0.0,
            "6月1日起收益": recent.iloc[-1] / recent.iloc[0] - 1, "6月1日起最大回撤": (recent / recent.cummax() - 1).min(),
        })
    return {"summary": pd.DataFrame(rows), "logs": logs, "window": window}


NOT_PERCENT = {"收益/波动", "每年交易笔数"}


def _render(table: pd.DataFrame) -> str:
    table = table.copy()
    for column in table.columns:
        if table[column].dtype.kind == "f":
            fmt = ((lambda x: f"{x:,.0f}") if column == "仓位" else
                   (lambda x: f"{x:.2f}") if column in NOT_PERCENT else (lambda x: f"{x:.1%}"))
            table[column] = table[column].map(lambda x, f=fmt: "" if pd.isna(x) else f(x))
    header = "| " + " | ".join(map(str, table.columns)) + " |"
    body = ["| " + " | ".join(map(str, row)) + " |" for row in table.itertuples(index=False)]
    return "\n".join([header, "|" + "---|" * len(table.columns), *body]) if len(table) else "（无）"


def write_report(results: dict, out: Path, data_end) -> None:
    out.mkdir(parents=True, exist_ok=True)
    s = results["summary"]
    s.to_csv(out / "summary.csv", index=False)
    risk = ["方案", "年化收益", "年化波动", "收益/波动", "最大回撤", "最差一天", "最差5%日均值", "平均单股仓位占比", "每年交易笔数"]
    windows = ["方案", "同长度时段中位收益", "同长度时段最差10%", "同长度时段亏钱比例", "6月1日起收益", "6月1日起最大回撤"]
    split = ["方案", "2016-22年化", "2016-22最大回撤", "2023后年化", "2023后最大回撤"]
    sections = [
        f"# 结构改进回测（数据截至 {data_end:%Y-%m-%d}）\n\n由 `python -m riskeval.structure_study` 生成，设定见该模块说明。"
        "只看半导体部分 4000；16 只股票按今天的市值挑选，有幸存者偏差，看各方案之间的相对差别。",
        "## 2016 年以来的风险与收益\n\n" + _render(s[risk]),
        f"## 所有长度为 {results['window']} 个交易日的时间段，以及 2026-06-01 起\n\n" + _render(s[windows]),
        "## 分段：2016–2022 与 2023 年以后\n\n" + _render(s[split]),
    ]
    for name, log in results["logs"].items():
        log.to_csv(out / f"trades_{name.split('：')[0]}.csv", index=False)
        sections.append(f"## 2026-06-01 起的交易：{name}\n\n" + (_render(log) if len(log) else "（无交易）"))
    (out / "README.md").write_text("\n\n".join(sections) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> None:
    from riskeval import daily_data

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--start", default="2015-01-01")
    parser.add_argument("--out", default="reports/structure_study")
    args = parser.parse_args(argv)

    semis = [t for ts in TARGETS.values() for t in ts]
    closes = daily_data.download_closes(semis + [CORE], args.start, chunk=50)
    results = run(closes)
    write_report(results, Path(args.out), closes.index[-1])
    print(f"已写入 {args.out}/README.md")


if __name__ == "__main__":
    main()
