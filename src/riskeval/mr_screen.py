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
        "跌破下轨+200日线上方": below & above200,
        "板块普跌时跌破下轨": _on_days(below, selloff),
        "板块普跌+200日线上方": _on_days(below, selloff) & above200,
        "板块普跌+200日线下方": _on_days(below, selloff) & ~above200 & sma200.notna(),
        "收回下轨(确认)": confirm,
        "板块普跌后收回下轨": _on_days(confirm, recent_selloff),
    }
    rows = forward.panel(closes, smh)
    rows = rows[rows["date"] >= "2016-01-01"]
    rules = {name: m.fillna(False).astype(bool) for name, m in rules.items()}
    starts = {f"{name}·段首": m & ~m.shift(1, fill_value=False) for name, m in rules.items()}
    flags = pd.DataFrame({name: m.stack() for name, m in (rules | starts).items()})
    flags.index.names = ["date", "ticker"]
    rows = rows.merge(flags.reset_index(), on=["date", "ticker"])

    analogs = []
    for name in [*rules, *starts]:
        for horizon, part in rows[rows[name]].groupby("horizon", sort=False):
            analogs.append({"规则": name, "持有": horizon} | forward.summarize(part))

    per_stock = pd.DataFrame([
        {"规则": name, "持有": horizon, "股票": ticker, "子行业": group_of[ticker]} | _stock_stats(part, name)
        for name in PER_STOCK_RULES
        for (horizon, ticker), part in rows[rows[name]].groupby(["horizon", "ticker"], sort=False)
    ])

    day = closes.index[-1]
    last = closes.loc[day]
    snapshot = pd.DataFrame({
        "子行业": pd.Series(group_of),
        "状态": _state(z.loc[day], z.shift(1).loc[day]),
        "布林z值": z.loc[day].round(2),
        "200日线上方": above200.loc[day],
        "跌破下轨": below.loc[day],
        "连续天数": _streak(below).loc[day],
        "相对200日线": last / sma200.loc[day] - 1,
        "相对50日线": last / signals.sma(closes, 50).loc[day] - 1,
        "距52周高点": last / closes.rolling(252, min_periods=60).max().loc[day] - 1,
        "近20日涨跌": last / closes.shift(20).loc[day] - 1,
        "近20日年化波动": closes.pct_change(fill_method=None).rolling(20).std().loc[day] * np.sqrt(252),
    }).rename_axis("股票").reset_index()
    ranking = _two_month_ranking(snapshot, per_stock)

    return {
        "snapshot": snapshot,
        "ranking": ranking,
        "analogs": pd.DataFrame(analogs),
        "per_stock": pd.DataFrame(per_stock),
        "episodes": _selloff_episodes(selloff, breadth, smh),
        "breadth_now": pd.DataFrame([{
            "日期": day.date(), "跌破下轨的股票占比": breadth.loc[day],
            "SMH近20日涨跌": smh.loc[day] / smh.shift(20).loc[day] - 1,
            "SMH相对200日线": smh.loc[day] / signals.sma(smh, 200).loc[day] - 1,
        }]),
    }


PER_STOCK_RULES = ["单只跌破下轨(全部)", "跌破下轨+200日线上方", "收回下轨(确认)"]


def _stock_stats(part: pd.DataFrame, rule: str) -> dict[str, float]:
    """单只股票在某条规则下的统计。"段首"只取每段信号的第一天入场，基本不重叠，更接近独立样本。"""
    done = part.dropna(subset=["ret"])
    first = done[done[f"{rule}·段首"]]
    return {
        "信号天数": len(done),
        "信号段数": len(first),
        "按天胜率": (done["ret"] > 0).mean() if len(done) else np.nan,
        "段首胜率": (first["ret"] > 0).mean() if len(first) else np.nan,
        "段首平均收益": first["ret"].mean(),
        "段首中位收益": first["ret"].median(),
        "段首平均最大浮亏": first["mae"].mean(),
        "段首最差浮亏": first["mae"].min(),
    }


def _state(z_now: pd.Series, z_prev: pd.Series) -> pd.Series:
    """当前所处阶段：跌破下轨中 / 今天收回下轨 / 接近下轨 / 未触发。"""
    state = pd.Series("未触发", index=z_now.index)
    state[(z_now > -2) & (z_now <= -1.5)] = "接近下轨"
    state[(z_now > -2) & (z_prev <= -2)] = "今天收回下轨(确认)"
    state[z_now <= -2] = "跌破下轨中"
    return state


def _two_month_ranking(snapshot: pd.DataFrame, per_stock: pd.DataFrame) -> pd.DataFrame:
    """持有 2 个月视角的逐只排名：现状 + 历史上"跌破下轨且在 200 日线上方"和"收回下轨"之后的表现。"""
    two = per_stock[per_stock["持有"] == "2个月"].set_index(["规则", "股票"])
    dip = two.loc["跌破下轨+200日线上方"][["信号段数", "段首胜率", "段首平均收益", "段首中位收益", "段首平均最大浮亏", "段首最差浮亏"]]
    conf = two.loc["收回下轨(确认)"][["信号段数", "段首胜率", "段首平均收益"]].add_prefix("确认后·")
    table = snapshot[["股票", "子行业", "状态", "布林z值", "200日线上方", "近20日年化波动"]].set_index("股票")
    table = table.join(dip).join(conf).reset_index()
    return table.sort_values(["段首胜率", "段首平均收益"], ascending=False)


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
               "近20日涨跌", "近20日年化波动", "按天胜率", "段首胜率", "段首平均收益", "段首中位收益", "段首平均最大浮亏",
               "段首最差浮亏", "确认后·段首胜率", "确认后·段首平均收益",
               "跌破下轨占比", "SMH此前20日涨跌", "SMH之后1个月", "SMH之后3个月", "SMH1个月内最大浮亏", "SMH3个月内最大浮亏"]
    fmt = lambda t: _md(_percent(t, percent))  # noqa: E731
    a = results["analogs"]
    cols = ["规则", "持有", "入场次数", "股票数", "胜率", "平均赚", "平均赔", "平均收益", "中位收益",
            "平均超额(对SMH)", "持有期年化波动", "平均最大浮亏", "最差最大浮亏"]
    sections = [
        f"# 均值回归选股（数据截至 {data_end:%Y-%m-%d}）\n\n由 `python -m riskeval.mr_screen` 生成，规则见该模块说明。"
        "历史统计从 2016 年开始，入场日互相重叠，独立样本远少于入场次数。",
        "## 现在的板块状态\n\n" + fmt(results["breadth_now"]),
        "## 持有 2 个月：逐只排名\n\n按\"跌破下轨且在 200 日线上方\"每段信号第一天入场、持有 2 个月的历史胜率排序；"
        "\"确认后\"是收回下轨那天入场。段数少于 8 的结论不可靠。\n\n" + fmt(results["ranking"]),
        "## 每只股票的现状\n\n" + fmt(results["snapshot"]),
        "## 历史类比：不同规则之后持有 1 / 2 / 3 个月（带\"·段首\"的只取每段信号第一天入场）\n\n" + _md(a[cols]),
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
