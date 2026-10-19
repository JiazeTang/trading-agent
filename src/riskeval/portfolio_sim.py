"""组合模拟：出场方式（满 42 天 / 回到中轨）× 买入方式（一次买满 / 分两批）× 入场规则（A / B）。

    python -m riskeval.portfolio_sim --out reports/portfolio_sim

设定（看结果之前写死）：
- 半导体部分 4000，分 3 个仓位；有空位时从当天信号里按 z 值从低到高买入，次日收盘成交。
  规则 A：单只跌破下轨且在 200 日线上方；规则 B：另外要求 16 只里至少一半同时跌破下轨。
- 买入方式：一次买满；或先买一半，之后某天收盘从下轨下方收回下轨上方再买另一半，
  补仓前如果收盘跌破 200 日线就取消补仓。
- 出场：-20% 止损（按平均成本、收盘价判断）；满 42 个交易日卖出，或收盘回到 20 日均线（z ≥ 0）就卖出。
  卖出后资金回到这个仓位，可以接下一个信号（多次买入）。
- 第一部分：从 PERIOD_START 起，加上 REGN、VRTX 各 1200 持有和 1600 现金，看本金 8000 的结果。
- 第二部分：只看半导体部分，从 2016 年起连续模拟，统计所有和第一部分一样长的时间段的收益分布，
  避免只凭一段行情下结论。
"""

from __future__ import annotations

import argparse
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

from riskeval import signals
from riskeval.mr_screen import SELLOFF_SHARE, TARGETS

PERIOD_START = pd.Timestamp("2026-06-01")
HISTORY_START = pd.Timestamp("2016-01-01")
CAPITAL, SEMI_CAPITAL, SLOTS = 8000.0, 4000.0, 3
HOLDS = {"REGN": 1200.0, "VRTX": 1200.0}
MAX_HOLD, STOP = 42, -0.20


def simulate_semis(closes: pd.DataFrame, semis: list[str], start, require_selloff: bool,
                   exit_mode: str, split_entry: bool) -> tuple[pd.Series, pd.DataFrame]:
    """半导体部分的逐日模拟，返回每日金额和交易记录。"""
    px = closes[semis]
    z = signals.zscore(px)
    sma200 = signals.sma(px, 200)
    below = z <= -2
    rule = below & (px > sma200)
    if require_selloff:
        breadth = below.sum(axis=1) / z.notna().sum(axis=1).replace(0, np.nan)
        rule = rule.apply(lambda c: c & (breadth >= SELLOFF_SHARE))
    rule = rule.fillna(False)

    days = px.index[px.index >= start]
    slots = [{"cash": SEMI_CAPITAL / SLOTS, "ticker": None} for _ in range(SLOTS)]
    pending, log, equity = [], [], {}
    prev_day = px.index[px.index.get_loc(days[0]) - 1]

    for day in days:
        price, zt, zp = px.loc[day], z.loc[day], z.loc[prev_day]
        for s in slots:
            if s["ticker"] is None:
                continue
            t = s["ticker"]
            s["held"] += 1
            cost = s["spent"] / s["shares"]
            change = price[t] / cost - 1
            reason = ("止损" if change <= STOP else
                      "回到中轨" if exit_mode == "回到中轨" and zt[t] >= 0 else
                      "到期" if s["held"] >= MAX_HOLD else None)
            if reason:
                s["cash"] += s["shares"] * price[t]
                log.append({"股票": t, "买入日": s["date"].date(), "卖出日": day.date(), "持有天数": s["held"],
                            "收益": change, "补仓": s["added"], "原因": reason})
                s["ticker"] = None
            elif s["reserve"] > 0:
                if zp[t] <= -2 < zt[t]:
                    s["shares"] += s["reserve"] / price[t]
                    s["spent"] += s["reserve"]
                    s["cash"] -= s["reserve"]
                    s["reserve"], s["added"] = 0.0, True
                elif price[t] < sma200.at[day, t]:
                    s["reserve"] = 0.0
        holding = {s["ticker"] for s in slots if s["ticker"]}
        for t in pending:
            free = next((s for s in slots if s["ticker"] is None), None)
            if free is None or t in holding or np.isnan(price[t]):
                continue
            first = free["cash"] / 2 if split_entry else free["cash"]
            free.update(ticker=t, shares=first / price[t], spent=first, cash=free["cash"] - first,
                        reserve=free["cash"] - first if split_entry else 0.0, date=day, held=0, added=False)
            holding.add(t)
        today = rule.loc[day]
        pending = list(zt[today[today].index].sort_values().index)
        equity[day] = sum(s["cash"] + (s["shares"] * price[s["ticker"]] if s["ticker"] else 0.0) for s in slots)
        prev_day = day

    for s in slots:
        if s["ticker"]:
            log.append({"股票": s["ticker"], "买入日": s["date"].date(), "卖出日": "持有中", "持有天数": s["held"],
                        "收益": price[s["ticker"]] / (s["spent"] / s["shares"]) - 1, "补仓": s["added"], "原因": "未卖出"})
    return pd.Series(equity), pd.DataFrame(log)


VARIANTS = [
    {"规则": rule, "出场": exit_mode, "买入": entry}
    for rule, exit_mode, entry in product(["B 板块普跌", "A 单只信号"], ["满42天", "回到中轨"], ["一次买满", "分两批"])
]


def _kwargs(v: dict) -> dict:
    return {"require_selloff": v["规则"].startswith("B"), "exit_mode": v["出场"], "split_entry": v["买入"] == "分两批"}


def period_results(closes: pd.DataFrame, semis: list[str]) -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
    days = closes.index[closes.index >= PERIOD_START]
    holds = sum(amount / closes.at[days[0], t] * closes.loc[days, t] for t, amount in HOLDS.items())
    cash = CAPITAL - SEMI_CAPITAL - sum(HOLDS.values())
    rows, logs = [], {}
    for v in VARIANTS:
        sleeve, log = simulate_semis(closes, semis, PERIOD_START, **_kwargs(v))
        total = sleeve + holds.reindex(sleeve.index) + cash
        daily = total.pct_change().dropna()
        done = log[log["卖出日"] != "持有中"]
        rows.append(v | {
            "期末金额": total.iloc[-1], "收益率": total.iloc[-1] / CAPITAL - 1,
            "半导体部分收益": sleeve.iloc[-1] / SEMI_CAPITAL - 1,
            "年化波动": daily.std() * np.sqrt(252), "最大回撤": (total / total.cummax() - 1).min(),
            "交易笔数": len(log), "已卖出笔数": len(done), "已卖出胜率": (done["收益"] > 0).mean() if len(done) else np.nan,
        })
        logs[f"{v['规则'][0]}·{v['出场']}·{v['买入']}"] = log
    return pd.DataFrame(rows), logs


def history_distribution(closes: pd.DataFrame, semis: list[str], window: int) -> pd.DataFrame:
    """2016 年起连续模拟半导体部分，所有长度为 window 个交易日的时间段的收益分布。"""
    rows = []
    for v in VARIANTS:
        sleeve, log = simulate_semis(closes, semis, HISTORY_START, **_kwargs(v))
        roll = (sleeve / sleeve.shift(window) - 1).dropna()
        daily = sleeve.pct_change().dropna()
        years = len(sleeve) / 252
        rows.append(v | {
            "时间段数": len(roll), "中位收益": roll.median(), "平均收益": roll.mean(),
            "最差10%分位": roll.quantile(0.1), "最好10%分位": roll.quantile(0.9), "亏钱的比例": (roll < 0).mean(),
            "2016起年化收益": (sleeve.iloc[-1] / SEMI_CAPITAL) ** (1 / years) - 1,
            "年化波动": daily.std() * np.sqrt(252), "最大回撤": (sleeve / sleeve.cummax() - 1).min(),
            "每年交易笔数": len(log) / years, "空仓时间比例": _idle_share(sleeve),
        })
    return pd.DataFrame(rows)


def _idle_share(sleeve: pd.Series) -> float:
    """半导体部分完全没有持仓（净值不动）的交易日比例。"""
    return float((sleeve.diff().abs() < 1e-9).mean())


PERCENT = ["收益率", "半导体部分收益", "年化波动", "最大回撤", "已卖出胜率", "中位收益", "平均收益", "最差10%分位",
           "最好10%分位", "亏钱的比例", "2016起年化收益", "空仓时间比例", "收益"]


def _render(table: pd.DataFrame) -> str:
    if table.empty:
        return "（无）"
    table = table.copy()
    for column in table.columns:
        if column in PERCENT:
            table[column] = table[column].map(lambda x: "" if pd.isna(x) else f"{x:.1%}")
        elif table[column].dtype.kind == "f":
            table[column] = table[column].map(lambda x: "" if pd.isna(x) else f"{x:,.1f}")
    header = "| " + " | ".join(map(str, table.columns)) + " |"
    body = ["| " + " | ".join(map(str, row)) + " |" for row in table.itertuples(index=False)]
    return "\n".join([header, "|" + "---|" * len(table.columns), *body])


def main(argv: list[str] | None = None) -> None:
    from riskeval import daily_data

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--start", default="2015-01-01")
    parser.add_argument("--out", default="reports/portfolio_sim")
    args = parser.parse_args(argv)

    semis = [t for ts in TARGETS.values() for t in ts]
    closes = daily_data.download_closes(semis + list(HOLDS) + ["SMH"], args.start, chunk=50)
    semis = [t for t in semis if t in closes.columns]
    period, logs = period_results(closes, semis)
    window = int((closes.index >= PERIOD_START).sum())
    history = history_distribution(closes, semis, window)

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    period.to_csv(out / "period.csv", index=False)
    history.to_csv(out / "history.csv", index=False)
    sections = [
        f"# 组合模拟：出场方式 × 买入方式（数据截至 {closes.index[-1]:%Y-%m-%d}）\n\n由 `python -m riskeval.portfolio_sim` 生成，设定见该模块说明。",
        f"## {PERIOD_START:%Y-%m-%d} 起，本金 8000（含 REGN/VRTX 各 1200 和现金 1600）\n\n" + _render(period),
        f"## 2016 年起所有长度为 {window} 个交易日的时间段（只看半导体部分 4000）\n\n" + _render(history),
    ]
    for name, log in logs.items():
        log.to_csv(out / f"trades_{name}.csv", index=False)
        sections.append(f"## 交易记录：{name}\n\n" + _render(log))
    (out / "README.md").write_text("\n\n".join(sections) + "\n", encoding="utf-8")
    print(f"已写入 {out}/README.md")


if __name__ == "__main__":
    main()
