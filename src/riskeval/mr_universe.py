"""把均值回归规则扩大到 S&P 500：哪些股票历史胜率高、现在有没有信号、历史胜率能不能预测未来。

    python -m riskeval.mr_universe --out reports/mr_universe

规则（看结果之前写死）：
- 信号：收盘跌破 20 日布林下轨（z ≤ -2）且在 200 日均线上方；次日收盘买入，持有 42 个交易日（约 2 个月）。
- 每只股票按时间顺序模拟不重叠的交易：持仓期间出现的新信号忽略，卖出后才接受下一个信号。
- 个股排名用胜率的 Wilson 95% 下界，同时要求至少 10 笔交易，避免少数几次碰巧全赢的股票排到前面。
- 样本外检验：用 2016–2022 年的交易排名，看 2023 年以后排名前 50 的股票是否真的比其余股票好。
  如果不好，说明"历史胜率高"主要是运气，不能拿来选股。
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from riskeval import signals
from riskeval.mr_screen import TARGETS

HOLD = 42
MIN_TRADES = 10
SPLIT = "2023-01-01"
TOP = 50


def wilson_lower(wins: float, n: float, z: float = 1.96) -> float:
    if n == 0:
        return np.nan
    p = wins / n
    centre = p + z * z / (2 * n)
    margin = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (centre - margin) / (1 + z * z / n)


def simulate(close: pd.Series, signal: pd.Series, start: str = "2016-01-01") -> pd.DataFrame:
    """单只股票不重叠的交易：信号日 t，t+1 收盘买入，t+1+HOLD 收盘卖出。"""
    close = close.dropna()
    signal = signal.reindex(close.index, fill_value=False)
    values, dates = close.to_numpy(), close.index
    first = dates.searchsorted(pd.Timestamp(start))
    rows, t = [], first
    flags = signal.to_numpy()
    while t < len(dates) - HOLD - 1:
        if flags[t]:
            entry, exit_ = values[t + 1], values[t + 1 + HOLD]
            path = values[t + 2:t + 2 + HOLD]
            rows.append({"date": dates[t], "ret": exit_ / entry - 1, "mae": min(path.min() / entry - 1, 0.0)})
            t += HOLD + 1
        else:
            t += 1
    return pd.DataFrame(rows, columns=["date", "ret", "mae"])


def baseline_win(close: pd.Series, start: str = "2016-01-01") -> float:
    """任意一天买入持有 2 个月的胜率，用来判断信号有没有带来额外的东西。"""
    close = close.dropna()
    ret = close.shift(-(HOLD + 1)) / close.shift(-1) - 1
    ret = ret[ret.index >= start].dropna()
    return (ret > 0).mean() if len(ret) else np.nan


def stock_table(trades: pd.DataFrame, baselines: pd.Series) -> pd.DataFrame:
    g = trades.groupby("ticker")
    table = pd.DataFrame({
        "交易笔数": g.size(),
        "赚钱笔数": g["ret"].apply(lambda r: int((r > 0).sum())),
        "平均收益": g["ret"].mean(),
        "中位收益": g["ret"].median(),
        "平均最大浮亏": g["mae"].mean(),
        "最差最大浮亏": g["mae"].min(),
    })
    table["胜率"] = table["赚钱笔数"] / table["交易笔数"]
    table["胜率下界(95%)"] = [wilson_lower(w, n) for w, n in zip(table["赚钱笔数"], table["交易笔数"])]
    table["随便买的胜率"] = baselines.reindex(table.index)
    table["胜率提升"] = table["胜率"] - table["随便买的胜率"]
    return table


def out_of_sample(trades: pd.DataFrame) -> pd.DataFrame:
    """用 SPLIT 之前的交易排名，看之后的表现。"""
    before, after = trades[trades["date"] < SPLIT], trades[trades["date"] >= SPLIT]
    g = before.groupby("ticker")["ret"]
    rank = pd.DataFrame({"n": g.size(), "wins": g.apply(lambda r: (r > 0).sum())})
    rank = rank[rank["n"] >= MIN_TRADES // 2]
    rank["lb"] = [wilson_lower(w, n) for w, n in zip(rank["wins"], rank["n"])]
    top = set(rank.sort_values("lb", ascending=False).index[:TOP])
    rows = []
    for label, chosen in {f"样本前排名前{TOP}": after["ticker"].isin(top),
                          "其余股票": after["ticker"].isin(set(rank.index) - top)}.items():
        part = after[chosen]
        rows.append({"分组": label, "股票数": part["ticker"].nunique(), "交易笔数": len(part),
                     "之后的胜率": (part["ret"] > 0).mean(), "之后的平均收益": part["ret"].mean(),
                     "之后的平均最大浮亏": part["mae"].mean()})
    per_stock_after = after.groupby("ticker")["ret"].apply(lambda r: (r > 0).mean())
    before_rate = (rank["wins"] / rank["n"]).reindex(per_stock_after.index).dropna()
    corr = before_rate.rank().corr(per_stock_after.reindex(before_rate.index).rank())  # 秩相关，不依赖 scipy
    rows.append({"分组": "个股前后胜率的秩相关", "股票数": len(before_rate), "交易笔数": np.nan,
                 "之后的胜率": corr, "之后的平均收益": np.nan, "之后的平均最大浮亏": np.nan})
    return pd.DataFrame(rows)


def run(closes: pd.DataFrame, groups: dict[str, str]) -> dict[str, pd.DataFrame]:
    z = signals.zscore(closes)
    above = closes > signals.sma(closes, 200)
    rule = ((z <= -2) & above).fillna(False)

    trades = pd.concat([simulate(closes[t], rule[t]).assign(ticker=t) for t in closes.columns], ignore_index=True)
    baselines = pd.Series({t: baseline_win(closes[t]) for t in closes.columns})
    table = stock_table(trades, baselines)
    table["分组"] = pd.Series(groups).reindex(table.index).fillna("S&P 500")

    day = closes.index[-1]
    state = pd.DataFrame({
        "布林z值": z.loc[day].round(2),
        "200日线上方": above.loc[day],
        "收回下轨(确认)": (z.loc[day] > -2) & (z.shift(1).loc[day] <= -2),
    })
    state["现在"] = np.select(
        [state["布林z值"] <= -2, state["收回下轨(确认)"], state["布林z值"] <= -1.5],
        ["跌破下轨", "今天收回下轨", "接近下轨"], "未触发")
    ranked = table[table["交易笔数"] >= MIN_TRADES].join(state).sort_values("胜率下界(95%)", ascending=False)
    eligible = ranked["200日线上方"] & ranked["现在"].isin(["跌破下轨", "今天收回下轨"])

    overall = trades.assign(win=trades["ret"] > 0)
    return {
        "now": ranked[eligible].reset_index(names="股票"),
        "watch": ranked[ranked["200日线上方"] & (ranked["现在"] == "接近下轨")].head(30).reset_index(names="股票"),
        "top": ranked.head(40).reset_index(names="股票"),
        "oos": out_of_sample(trades),
        "overall": pd.DataFrame([{
            "股票数": closes.shape[1], "交易笔数": len(trades), "胜率": overall["win"].mean(),
            "平均收益": trades["ret"].mean(), "中位收益": trades["ret"].median(),
            "平均最大浮亏": trades["mae"].mean(), "随便买的胜率(各股平均)": baselines.mean(),
            "今天跌破下轨的比例": (z.loc[day] <= -2).mean(),
        }]),
        "all_stocks": table.reset_index(names="股票"),
    }


PERCENT = ["平均收益", "中位收益", "平均最大浮亏", "最差最大浮亏", "胜率", "胜率下界(95%)", "随便买的胜率", "胜率提升",
           "之后的胜率", "之后的平均收益", "之后的平均最大浮亏", "随便买的胜率(各股平均)", "今天跌破下轨的比例"]


def _render(table: pd.DataFrame) -> str:
    if table.empty:
        return "（无）"
    table = table.copy()
    for column in table.columns:
        if column in PERCENT:
            table[column] = table[column].map(lambda x: "" if pd.isna(x) else f"{x:.1%}")
        elif table[column].dtype.kind == "f":
            table[column] = table[column].map(lambda x: "" if pd.isna(x) else f"{x:g}")
    header = "| " + " | ".join(map(str, table.columns)) + " |"
    body = ["| " + " | ".join(map(str, row)) + " |" for row in table.itertuples(index=False)]
    return "\n".join([header, "|" + "---|" * len(table.columns), *body])


def write_report(results: dict[str, pd.DataFrame], out: Path, data_end) -> None:
    out.mkdir(parents=True, exist_ok=True)
    for name, table in results.items():
        table.to_csv(out / f"{name}.csv", index=False)
    cols = ["股票", "分组", "现在", "布林z值", "交易笔数", "胜率", "胜率下界(95%)", "随便买的胜率", "胜率提升",
            "平均收益", "中位收益", "平均最大浮亏", "最差最大浮亏"]
    sections = [
        f"# 均值回归：扩大到 S&P 500（数据截至 {data_end:%Y-%m-%d}）\n\n由 `python -m riskeval.mr_universe` 生成，规则见该模块说明。"
        "股票池是今天的 S&P 500 成分股（有幸存者偏差）加上之前的 16 只半导体股。",
        "## 整体\n\n" + _render(results["overall"]),
        "## 样本外检验：历史胜率能不能用来选股\n\n用 2023 年以前的交易排名，看 2023 年以后的表现。"
        "最后一行是个股前后胜率的秩相关，接近 0 说明历史胜率基本不能预测未来。\n\n" + _render(results["oos"]),
        f"## 现在有信号的股票（在 200 日线上方，今天跌破下轨或刚收回下轨；至少 {MIN_TRADES} 笔历史交易）\n\n" + _render(results["now"][cols]),
        "## 接近下轨、可以观察的股票（前 30）\n\n" + _render(results["watch"][cols]),
        "## 历史胜率下界最高的 40 只（不管现在有没有信号）\n\n" + _render(results["top"][cols]),
    ]
    (out / "README.md").write_text("\n\n".join(sections) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> None:
    from riskeval import daily_data

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--start", default="2015-01-01")
    parser.add_argument("--out", default="reports/mr_universe")
    args = parser.parse_args(argv)

    groups = {t: g for g, ts in TARGETS.items() for t in ts}
    sp500 = daily_data.sp500_tickers()
    tickers = sorted(set(sp500) | set(groups))
    closes = daily_data.download_closes(tickers, args.start)
    results = run(closes, groups)
    write_report(results, Path(args.out), closes.index[-1])
    print(f"已写入 {args.out}/README.md")


if __name__ == "__main__":
    main()
