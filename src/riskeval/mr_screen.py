"""均值回归选股：这 16 只半导体股现在有没有满足条件的，历史上类似情形之后怎么走。

    python -m riskeval.mr_screen --out reports/mr_screen

规则沿用 kova_study，看结果之前写死：
- 跌破布林下轨：收盘价低于 20 日均线 2 个标准差（z ≤ -2）。
- 板块普跌：当天 16 只里至少一半同时跌破下轨。眼下就是这种情形。
- 确认：前一天还在下轨下方，当天收回下轨上方。这是常见的改良做法，属于探索性对比。
- 入场和持有方式与 kova_study 相同：信号日第二天收盘买入，持有 21 / 42 / 63 个交易日。
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from riskeval import forward, signals
from riskeval.kova_study import _md

TARGETS = {
    "计算与设计": ["NVDA", "AVGO", "AMD", "TXN"],
    "存储": ["MU", "SNDK", "STX", "WDC"],
    "光通信与互连": ["LITE", "ALAB", "CIEN", "COHR"],
    "制造与设备": ["TSM", "ASML", "INTC", "LRCX"],
}
SELLOFF_SHARE = 0.5
EPISODE_GAP = 10  # 相隔超过这么多交易日的普跌才算新的一次


def compute(closes: pd.DataFrame, smh: pd.Series) -> dict[str, pd.DataFrame]:
    group_of = {t: g for g, ts in TARGETS.items() for t in ts}
    z = signals.zscore(closes)
    sma200 = signals.sma(closes, 200)
    below = z <= -2
    breadth = below.sum(axis=1) / z.notna().sum(axis=1).replace(0, np.nan)
    selloff = breadth >= SELLOFF_SHARE
    recent_selloff = selloff.rolling(5, min_periods=1).max().astype(bool)
    confirm = (z > -2) & (z.shift(1) <= -2)
    above200 = closes > sma200

    rules = {
        "单只跌破下轨(全部)": below,
        "板块普跌时跌破下轨": _on_days(below, selloff),
        "板块普跌+200日线上方": _on_days(below, selloff) & above200,
        "板块普跌+200日线下方": _on_days(below, selloff) & ~above200 & sma200.notna(),
        "收回下轨(确认)": confirm,
        "板块普跌后收回下轨": _on_days(confirm, recent_selloff),
    }
    rows = forward.panel(closes, smh)
    rows = rows[rows["date"] >= "2016-01-01"]
    flags = pd.DataFrame({name: m.fillna(False).astype(bool).stack() for name, m in rules.items()})
    flags.index.names = ["date", "ticker"]
    rows = rows.merge(flags.reset_index(), on=["date", "ticker"])

    analogs = []
    for name in rules:
        for horizon, part in rows[rows[name]].groupby("horizon", sort=False):
            analogs.append({"规则": name, "持有": horizon} | forward.summarize(part))

    per_stock = []
    one_month = rows[(rows["horizon"] == "1个月") & rows["单只跌破下轨(全部)"]]
    for ticker, part in one_month.groupby("ticker"):
        s = forward.summarize(part)
        per_stock.append({"股票": ticker, "子行业": group_of[ticker], "历史信号天数": s["入场次数"],
                          "1个月胜率": s["胜率"], "1个月平均收益": s["平均收益"],
                          "1个月平均最大浮亏": s["平均最大浮亏"], "1个月最差浮亏": s["最差最大浮亏"]})

    day = closes.index[-1]
    last = closes.loc[day]
    snapshot = pd.DataFrame({
        "子行业": pd.Series(group_of),
        "布林z值": z.loc[day].round(2),
        "跌破下轨": below.loc[day],
        "连续天数": _streak(below).loc[day],
        "相对200日线": last / sma200.loc[day] - 1,
        "相对50日线": last / signals.sma(closes, 50).loc[day] - 1,
        "距52周高点": last / closes.rolling(252, min_periods=60).max().loc[day] - 1,
        "近20日涨跌": last / closes.shift(20).loc[day] - 1,
        "近20日年化波动": closes.pct_change(fill_method=None).rolling(20).std().loc[day] * np.sqrt(252),
    }).rename_axis("股票").reset_index()
    snapshot = snapshot.merge(pd.DataFrame(per_stock)[["股票", "历史信号天数", "1个月胜率", "1个月平均收益", "1个月平均最大浮亏"]],
                              on="股票", how="left")

    return {
        "snapshot": snapshot,
        "analogs": pd.DataFrame(analogs),
        "per_stock": pd.DataFrame(per_stock),
        "episodes": _selloff_episodes(selloff, breadth, smh),
        "breadth_now": pd.DataFrame([{
            "日期": day.date(), "跌破下轨的股票占比": breadth.loc[day],
            "SMH近20日涨跌": smh.loc[day] / smh.shift(20).loc[day] - 1,
            "SMH相对200日线": smh.loc[day] / signals.sma(smh, 200).loc[day] - 1,
        }]),
    }


def _on_days(flags: pd.DataFrame, days: pd.Series) -> pd.DataFrame:
    """只保留 days 为 True 的日子里的信号。"""
    return flags.apply(lambda column: column & days)


def _streak(flags: pd.DataFrame) -> pd.DataFrame:
    """每只股票截至当天连续为 True 的天数。"""
    out = flags.astype(int).copy()
    for column in flags:
        f = flags[column].fillna(False).astype(bool)
        group = (~f).cumsum()
        out[column] = f.groupby(group).cumsum()
    return out


def _selloff_episodes(selloff: pd.Series, breadth: pd.Series, smh: pd.Series) -> pd.DataFrame:
    """2016 年以来每一次板块普跌的第一天，以及 SMH 之后 1 / 3 个月的表现。"""
    days = selloff[selloff].index
    days = days[days >= "2016-01-01"]
    pos = smh.index.get_indexer(days)
    starts = [d for i, d in enumerate(days) if i == 0 or pos[i] - pos[i - 1] > EPISODE_GAP]
    one, three = forward.forward_stats(smh, 21), forward.forward_stats(smh, 63)
    return pd.DataFrame([{
        "普跌开始": d.date(), "跌破下轨占比": breadth.loc[d],
        "SMH此前20日涨跌": smh.loc[d] / smh.shift(20).loc[d] - 1,
        "SMH之后1个月": one.at[d, "ret"], "SMH之后3个月": three.at[d, "ret"],
        "SMH1个月内最大浮亏": one.at[d, "mae"], "SMH3个月内最大浮亏": three.at[d, "mae"],
    } for d in starts])


def write_report(results: dict[str, pd.DataFrame], out: Path, data_end) -> None:
    out.mkdir(parents=True, exist_ok=True)
    for name, table in results.items():
        table.to_csv(out / f"{name}.csv", index=False)
    percent = ["跌破下轨的股票占比", "SMH近20日涨跌", "SMH相对200日线", "相对200日线", "相对50日线", "距52周高点",
               "近20日涨跌", "近20日年化波动", "1个月胜率", "1个月平均收益", "1个月平均最大浮亏", "1个月最差浮亏",
               "跌破下轨占比", "SMH此前20日涨跌", "SMH之后1个月", "SMH之后3个月", "SMH1个月内最大浮亏", "SMH3个月内最大浮亏"]
    fmt = lambda t: _md(_percent(t, percent))  # noqa: E731
    a = results["analogs"]
    cols = ["规则", "持有", "入场次数", "股票数", "胜率", "平均赚", "平均赔", "平均收益", "中位收益",
            "平均超额(对SMH)", "持有期年化波动", "平均最大浮亏", "最差最大浮亏"]
    sections = [
        f"# 均值回归选股（数据截至 {data_end:%Y-%m-%d}）\n\n由 `python -m riskeval.mr_screen` 生成，规则见该模块说明。"
        "历史统计从 2016 年开始，入场日互相重叠，独立样本远少于入场次数。",
        "## 现在的板块状态\n\n" + fmt(results["breadth_now"]),
        "## 每只股票的现状（含它自己历史上跌破下轨后 1 个月的表现）\n\n" + fmt(results["snapshot"]),
        "## 历史类比：不同规则之后持有 1 / 2 / 3 个月\n\n" + _md(a[cols]),
        "## 2016 年以来每次板块普跌之后 SMH 的走势\n\n" + fmt(results["episodes"]),
    ]
    (out / "README.md").write_text("\n\n".join(sections) + "\n", encoding="utf-8")


def _percent(table: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    table = table.copy()
    for column in table.columns.intersection(columns):
        table[column] = table[column].map(lambda x: "" if pd.isna(x) else f"{x:.1%}")
    return table


def main(argv: list[str] | None = None) -> None:
    from riskeval import daily_data

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--start", default="2015-01-01")
    parser.add_argument("--out", default="reports/mr_screen")
    args = parser.parse_args(argv)

    tickers = [t for ts in TARGETS.values() for t in ts]
    data = daily_data.download_closes(tickers + ["SMH"], args.start, chunk=50)
    results = compute(data[tickers], data["SMH"].dropna())
    write_report(results, Path(args.out), data.index[-1])
    print(f"已写入 {args.out}/README.md")


if __name__ == "__main__":
    main()
