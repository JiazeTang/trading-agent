"""半导体股：Kova Score 近似信号 vs 均值回归，持有 1 / 2 / 3 个月的胜负统计。

    python -m riskeval.kova_study --out reports/kova_study

以下设定在看结果之前写死：
- 股票：四个子行业各取当前市值前 4（候选名单见 SUBGROUPS），基准 SMH。
- 每个交易日都可以是入场日：信号在第 t 天收盘算出，第 t+1 天收盘买入，持有 21 / 42 / 63 个交易日。
- 策略（全部见 STRATEGIES）：
  * 随便哪天买入 —— 基准，用来判断信号有没有带来额外的东西
  * Kova 近似 ≥ 90；Kova 完整用法（≥ 90 + EMA 多头排列 + 距 52 周高点 10% 以内）；Kova 近似 < 50 作对照
  * 均值回归：收盘跌破 20 日布林带下轨（z ≤ -2）；以及只在 200 日均线上方时才做
- 市况：入场当天用 SMH 过去 20 天的效率比判断（≥ 0.3 为趋势，否则震荡），只用当时已知的数据。
- 时间：重点看最近一年的入场日，2016 年以来的结果作对照。
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from riskeval import forward, signals

SUBGROUPS = {
    "计算与设计": ["NVDA", "AVGO", "AMD", "QCOM", "ARM", "MRVL", "ADI", "TXN", "MCHP", "NXPI"],
    "存储": ["MU", "SNDK", "WDC", "STX"],
    "光通信与互连": ["COHR", "LITE", "CIEN", "FN", "CRDO", "ALAB", "AAOI"],
    "制造与设备": ["TSM", "ASML", "AMAT", "LRCX", "KLAC", "INTC", "TER", "GFS", "ENTG"],
}
TOP_N = 4
BENCHMARKS = ["SMH", "SPY"]

STRATEGIES = {
    "随便哪天买入(基准)": lambda s: s["has_price"],
    "Kova近似≥90": lambda s: s["rs"] >= 90,
    "Kova完整用法": lambda s: (s["rs"] >= 90) & s["trend"] & s["near_high"],
    "Kova近似<50(对照)": lambda s: s["rs"] < 50,
    "均值回归:跌破布林下轨": lambda s: s["z"] <= -2,
    "均值回归+200日线上方": lambda s: (s["z"] <= -2) & (s["close"] > s["sma200"]),
}

PERCENT = ["胜率", "平均赚", "平均赔", "平均收益", "中位收益", "平均超额(对SMH)", "跑赢SMH比例",
           "持有期年化波动", "平均最大浮亏", "最差最大浮亏", "SMH涨跌", "收益至今", "最大浮亏至今", "1个月收益"]


def pick_targets(caps: pd.Series) -> dict[str, list[str]]:
    """每个子行业取市值前 TOP_N；取不到市值的排在后面，保持候选名单顺序。"""
    picked = {}
    for group, candidates in SUBGROUPS.items():
        order = caps.reindex(candidates).sort_values(ascending=False, na_position="last")
        picked[group] = list(order.index[:TOP_N])
    return picked


def build_signals(universe: pd.DataFrame, targets: list[str]) -> dict[str, pd.DataFrame]:
    rs = signals.rs_rating(universe)
    close = universe[targets]
    return {
        "close": close,
        "has_price": close.notna(),
        "rs": rs[targets],
        "trend": signals.trend_aligned(close),
        "near_high": signals.near_52w_high(close),
        "z": signals.zscore(close),
        "sma200": signals.sma(close, 200),
    }


def long_signals(sig: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """每个 (日期, 股票) 一行，每个策略一列布尔值。"""
    columns = {name: rule(sig).fillna(False).astype(bool).stack() for name, rule in STRATEGIES.items()}
    table = pd.DataFrame(columns)
    table.index.names = ["date", "ticker"]
    return table.reset_index()


def run(universe: pd.DataFrame, targets_by_group: dict[str, list[str]], recent_days: int = 365) -> dict[str, pd.DataFrame]:
    targets = [t for group in targets_by_group.values() for t in group if t in universe.columns]
    group_of = {t: g for g, ts in targets_by_group.items() for t in ts}
    sig = build_signals(universe, targets)
    smh = universe["SMH"].dropna()

    rows = forward.panel(sig["close"], smh).merge(long_signals(sig), on=["date", "ticker"])
    rows["group"] = rows["ticker"].map(group_of)
    rows["regime"] = rows["date"].map(signals.sector_regime(smh))
    rows["pos"] = smh.index.get_indexer(rows["date"])
    end = smh.index[-1]
    recent = rows["date"] > end - pd.Timedelta(days=recent_days)
    periods = {"近一年": rows[recent], "2016年以来": rows[rows["date"] >= "2016-01-01"]}

    summary, by_regime, by_group = [], [], []
    for period, subset in periods.items():
        for name in STRATEGIES:
            chosen = subset[subset[name]]
            for horizon, part in chosen.groupby("horizon", sort=False):
                key = {"时期": period, "策略": name, "持有": horizon}
                summary.append(key | {"信号段数": _episodes(part)} | forward.summarize(part))
                for regime, piece in part.groupby("regime"):
                    by_regime.append(key | {"入场时SMH市况": regime} | forward.summarize(piece))
                if period == "近一年":
                    for group, piece in part.groupby("group"):
                        by_group.append(key | {"子行业": group} | forward.summarize(piece))

    last_year = rows[recent & (rows["horizon"] == "1个月")]
    by_month = []
    for name in STRATEGIES:
        chosen = last_year[last_year[name]]
        for month, part in chosen.groupby(chosen["date"].dt.to_period("M")):
            by_month.append({"策略": name, "入场月份": str(month)} | forward.summarize(part))

    per_stock = (rows[recent].melt(id_vars=["ticker", "group", "horizon", "ret"], value_vars=list(STRATEGIES),
                                   var_name="策略", value_name="on")
                 .query("on").dropna(subset=["ret"])
                 .groupby(["策略", "horizon", "group", "ticker"])["ret"].agg(["count", "mean"])
                 .rename(columns={"count": "入场次数", "mean": "平均收益"}).reset_index())

    return {
        "summary": pd.DataFrame(summary),
        "by_regime": pd.DataFrame(by_regime),
        "by_group": pd.DataFrame(by_group),
        "by_month": pd.DataFrame(by_month),
        "per_stock": per_stock,
        "smh_months": _smh_months(smh, end, recent_days),
        "mr_recent": _recent_mean_reversion(sig, rows, end),
        "latest": _latest(sig, group_of),
        "targets": pd.DataFrame([{"子行业": g, "股票": ", ".join(ts)} for g, ts in targets_by_group.items()]),
    }


def _episodes(part: pd.DataFrame) -> int:
    """信号段数：同一只股票连续的信号交易日算一段。"""
    return sum(1 + int((np.diff(np.sort(g["pos"].unique())) > 1).sum()) for _, g in part.groupby("ticker"))


def _smh_months(smh: pd.Series, end, recent_days: int) -> pd.DataFrame:
    monthly = smh.resample("ME").last()
    table = pd.DataFrame({"SMH涨跌": monthly.pct_change()})
    regime = signals.sector_regime(smh)
    counts = regime.groupby(regime.index.to_period("M")).value_counts().unstack(fill_value=0)
    table.index = table.index.to_period("M")
    table = table.join(counts)
    return table[table.index >= (end - pd.Timedelta(days=recent_days)).to_period("M")].rename_axis("月份").reset_index()


def _recent_mean_reversion(sig, rows, end, days: int = 92) -> pd.DataFrame:
    """最近约三个月里每一次"跌破布林下轨"的入场：1 个月结果（若已完整）和持有至今。"""
    close = sig["close"]
    hits = rows[(rows["horizon"] == "1个月") & rows["均值回归:跌破布林下轨"] & (rows["date"] > end - pd.Timedelta(days=days))]
    out = []
    for _, r in hits.iterrows():
        path = close[r["ticker"]].loc[r["date"]:].dropna()
        if len(path) < 2:
            continue
        entry = path.iloc[1]
        out.append({
            "股票": r["ticker"], "子行业": r["group"], "信号日": r["date"].date(),
            "入场时SMH市况": r["regime"], "1个月收益": r["ret"],
            "收益至今": path.iloc[-1] / entry - 1,
            "最大浮亏至今": min(path.iloc[1:].min() / entry - 1, 0.0),
            "200日线上方": bool(sig["close"].at[r["date"], r["ticker"]] > sig["sma200"].at[r["date"], r["ticker"]]),
        })
    return pd.DataFrame(out)


def _latest(sig, group_of) -> pd.DataFrame:
    """最新一天每只股票的指标，用来和真实 Kova Score 对照校准。"""
    day = sig["close"].index[-1]
    return pd.DataFrame({
        "子行业": pd.Series(group_of),
        "Kova近似": sig["rs"].loc[day].round(0),
        "EMA多头排列": sig["trend"].loc[day],
        "距52周高点10%内": sig["near_high"].loc[day],
        "布林z值": sig["z"].loc[day].round(2),
    }).rename_axis(f"股票({day.date()})").reset_index()


def write_report(results: dict[str, pd.DataFrame], out: Path, data_end) -> None:
    out.mkdir(parents=True, exist_ok=True)
    for name, table in results.items():
        table.to_csv(out / f"{name}.csv", index=False)

    s = results["summary"]
    headline = ["时期", "策略", "持有", "信号段数", "入场次数", "赚钱次数", "赔钱次数", "胜率", "平均赚", "平均赔",
                "平均收益", "平均超额(对SMH)", "持有期年化波动", "平均最大浮亏"]
    regime_cols = ["策略", "持有", "入场时SMH市况", "入场次数", "胜率", "平均收益", "平均超额(对SMH)", "平均最大浮亏"]
    month_cols = ["策略", "入场月份", "入场次数", "胜率", "平均收益", "平均超额(对SMH)"]
    group_cols = ["策略", "持有", "子行业", "入场次数", "胜率", "平均收益", "平均超额(对SMH)", "平均最大浮亏"]
    stock_cols = ["策略", "持有", "股票数", "收益为正的股票数", "收益为负的股票数"]
    regime = results["by_regime"]
    sections = [
        f"# 半导体：Kova 近似信号 vs 均值回归\n\n数据截至 {data_end:%Y-%m-%d}。由 `python -m riskeval.kova_study` 生成，设定见该模块说明。"
        "\"Kova 近似\"是按公开描述复现的相对强度分数，不是 KovaView 的真实分数。"
        "每天都可以入场，持有期互相重叠，入场次数远多于独立样本数，\"信号段数\"更接近独立样本数。",
        "## 股票池\n\n" + _md(results["targets"]),
        "## 最近一年 SMH 每月涨跌和市况天数\n\n" + _md(results["smh_months"]),
        "## 总表\n\n" + _md(s[headline]),
        "## 按股票：按每只股票的平均收益算，赚钱 / 赔钱的股票数（最近一年）\n\n" + _md(s[s["时期"] == "近一年"][stock_cols]),
        "## 按入场时的 SMH 市况（最近一年）\n\n" + _md(regime[regime["时期"] == "近一年"][regime_cols]),
        "## 按入场时的 SMH 市况（2016 年以来）\n\n" + _md(regime[regime["时期"] == "2016年以来"][regime_cols]),
        "## 按子行业（最近一年）\n\n" + _md(results["by_group"][group_cols]),
        "## 按入场月份，持有 1 个月（最近一年）\n\n" + _md(results["by_month"][month_cols]),
        "## 最近约三个月的均值回归入场\n\n" + _md(results["mr_recent"]),
        "## 最新指标（用来和真实 Kova Score 对照）\n\n" + _md(results["latest"]),
    ]
    (out / "README.md").write_text("\n\n".join(sections) + "\n", encoding="utf-8")


def _md(table: pd.DataFrame) -> str:
    if table.empty:
        return "（无）"
    table = table.copy()
    for column in table.columns:
        if column in PERCENT:
            table[column] = table[column].map(lambda x: "" if pd.isna(x) else f"{x:.1%}")
        elif table[column].dtype.kind == "f":
            table[column] = table[column].map(lambda x: "" if pd.isna(x) else f"{x:g}")
    header = "| " + " | ".join(map(str, table.columns)) + " |"
    rule = "|" + "---|" * len(table.columns)
    body = ["| " + " | ".join(map(str, row)) + " |" for row in table.itertuples(index=False)]
    return "\n".join([header, rule, *body])


def main(argv: list[str] | None = None) -> None:
    from riskeval import daily_data

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--start", default="2015-01-01")
    parser.add_argument("--out", default="reports/kova_study")
    parser.add_argument("--cache", help="本地缓存 parquet 路径（可选）")
    args = parser.parse_args(argv)

    candidates = sorted({t for ts in SUBGROUPS.values() for t in ts})
    if args.cache and Path(args.cache).exists():
        universe = pd.read_parquet(args.cache)
    else:
        tickers = sorted(set(daily_data.sp1500_tickers()) | set(candidates) | set(BENCHMARKS))
        universe = daily_data.download_closes(tickers, args.start)
        if args.cache:
            Path(args.cache).parent.mkdir(parents=True, exist_ok=True)
            universe.to_parquet(args.cache)
    print(f"股票池 {universe.shape[1]} 只，{universe.index[0]:%Y-%m-%d} ~ {universe.index[-1]:%Y-%m-%d}")

    targets = pick_targets(daily_data.market_caps(candidates))
    print("入选：", targets)
    results = run(universe, targets)
    write_report(results, Path(args.out), universe.index[-1])
    print(f"已写入 {args.out}/README.md")


if __name__ == "__main__":
    main()
