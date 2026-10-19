"""止损 / 止盈怎么设，以及"上半年牛市之后的震荡市里严格执行规则"会是什么结果。

    python -m riskeval.exit_study --out reports/exit_study

第一部分：出场规则网格（看结果之前写死，只测这些组合）
- 入场：收盘跌破 20 日布林下轨且在 200 日线上方，次日收盘买入；每只股票的交易不重叠。
- 止损：不设 / -10% / -15% / -20%；止盈：不设 / +10% / +15% / +20% / 收盘回到 20 日均线（布林中轨）。
- 都按收盘价判断、按收盘价成交；最长持有 42 个交易日。
- 在两个股票池上测：之前的 16 只半导体、S&P 500。并按 2023 年前后分开，看结论稳不稳。

第二部分：组合模拟（从 PERIOD_START 到最新收盘）
- 本金 8000：半导体 4000 分成 3 个仓位，每个约 1333；REGN、VRTX 各 1200 在第一天买入一直持有；现金 1600。
- 半导体仓位有空位时，从当天有信号的股票里选 z 值最低的买入；
  规则 A 只要求单只股票跌破下轨且在 200 日线上方，规则 B 还要求板块普跌（16 只里至少一半同时跌破下轨）。
- 出场：-20% 止损，或持有满 42 个交易日；到最新收盘还没卖的按最新收盘价估值。
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from riskeval import signals
from riskeval.mr_screen import SELLOFF_SHARE, TARGETS

MAX_HOLD = 42
STOPS = {"不设": None, "-10%": -0.10, "-15%": -0.15, "-20%": -0.20}
TAKES = {"不设": None, "+10%": 0.10, "+15%": 0.15, "+20%": 0.20, "回到中轨": "mean"}
SPLIT = pd.Timestamp("2023-01-01")
PERIOD_START = pd.Timestamp("2026-06-01")
CAPITAL = 8000.0
SEMI_SLOTS, SEMI_CAPITAL = 3, 4000.0
HOLDS = {"REGN": 1200.0, "VRTX": 1200.0}


def exit_day(path: np.ndarray, z_path: np.ndarray, entry: float, stop, take) -> int:
    """从买入后第一天起，返回第几天卖出（1 起算）。path、z_path 是买入后每天的收盘价和 z 值。"""
    for day, (price, z) in enumerate(zip(path, z_path), start=1):
        change = price / entry - 1
        if stop is not None and change <= stop:
            return day
        if take == "mean" and z >= 0:
            return day
        if isinstance(take, float) and change >= take:
            return day
    return len(path)


def trades_for(close: pd.Series, z: pd.Series, signal: pd.Series, stop, take, start="2016-01-01") -> list[dict]:
    close, z = close.dropna(), z.reindex(close.dropna().index)
    flags = signal.reindex(close.index, fill_value=False).to_numpy()
    values, zs, dates = close.to_numpy(), z.to_numpy(), close.index
    t, out = dates.searchsorted(pd.Timestamp(start)), []
    while t < len(dates) - MAX_HOLD - 1:
        if flags[t]:
            entry = values[t + 1]
            path, z_path = values[t + 2:t + 2 + MAX_HOLD], zs[t + 2:t + 2 + MAX_HOLD]
            days = exit_day(path, z_path, entry, stop, take)
            out.append({"date": dates[t], "ret": path[days - 1] / entry - 1, "days": days,
                        "mae": min(path[:days].min() / entry - 1, 0.0)})
            t += 1 + days
        else:
            t += 1
    return out


def exit_grid(closes: pd.DataFrame) -> pd.DataFrame:
    z = signals.zscore(closes)
    rule = ((z <= -2) & (closes > signals.sma(closes, 200))).fillna(False)
    rows = []
    for stop_name, stop in STOPS.items():
        for take_name, take in TAKES.items():
            trades = pd.DataFrame([tr for t in closes.columns for tr in trades_for(closes[t], z[t], rule[t], stop, take)])
            before, after = trades[trades["date"] < SPLIT], trades[trades["date"] >= SPLIT]
            rows.append({
                "止损": stop_name, "止盈": take_name, "交易笔数": len(trades),
                "胜率": (trades["ret"] > 0).mean(), "平均收益": trades["ret"].mean(), "中位收益": trades["ret"].median(),
                "最差一笔": trades["ret"].min(), "平均持有天数": trades["days"].mean(),
                "平均每天收益": trades["ret"].sum() / trades["days"].sum(),
                "2023前平均收益": before["ret"].mean(), "2023后平均收益": after["ret"].mean(),
                "2023后胜率": (after["ret"] > 0).mean(),
            })
    return pd.DataFrame(rows)


def simulate_portfolio(closes: pd.DataFrame, semis: list[str], require_selloff: bool) -> tuple[pd.Series, pd.DataFrame]:
    """逐日模拟 8000 的组合，返回每日净值和交易记录。"""
    z = signals.zscore(closes[semis])
    below = z <= -2
    rule = below & (closes[semis] > signals.sma(closes[semis], 200))
    if require_selloff:
        breadth = below.sum(axis=1) / z.notna().sum(axis=1).replace(0, np.nan)
        rule = rule.apply(lambda c: c & (breadth >= SELLOFF_SHARE))
    rule = rule.fillna(False)

    days = closes.index[closes.index >= PERIOD_START]
    first = days[0]
    holds = {t: amount / closes.at[first, t] for t, amount in HOLDS.items()}
    cash = CAPITAL - SEMI_CAPITAL - sum(HOLDS.values())
    slots = [{"cash": SEMI_CAPITAL / SEMI_SLOTS, "ticker": None} for _ in range(SEMI_SLOTS)]
    pending: list[str] = []
    log, equity = [], {}

    for i, day in enumerate(days):
        price = closes.loc[day]
        # 1) 先处理到期和止损（按今天收盘）
        for slot in slots:
            if slot["ticker"] is None:
                continue
            slot["held"] += 1
            change = price[slot["ticker"]] / slot["entry"] - 1
            if change <= -0.20 or slot["held"] >= MAX_HOLD:
                slot["cash"] = slot["shares"] * price[slot["ticker"]]
                log.append({"股票": slot["ticker"], "买入日": slot["date"].date(), "卖出日": day.date(),
                            "持有天数": slot["held"], "收益": change, "原因": "止损" if change <= -0.20 else "到期"})
                slot["ticker"] = None
        # 2) 昨天的信号今天收盘买入
        holding = {s["ticker"] for s in slots if s["ticker"]}
        for ticker in pending:
            free = next((s for s in slots if s["ticker"] is None), None)
            if free is None or ticker in holding or np.isnan(price[ticker]):
                continue
            free.update(ticker=ticker, entry=price[ticker], shares=free["cash"] / price[ticker], date=day, held=0)
            holding.add(ticker)
        # 3) 今天收盘出现的信号，按 z 从低到高排队，明天买
        today = rule.loc[day]
        pending = list(z.loc[day][today[today].index].sort_values().index)

        value = cash + sum(n * price[t] for t, n in holds.items())
        value += sum(s["shares"] * price[s["ticker"]] if s["ticker"] else s["cash"] for s in slots)
        equity[day] = value

    for slot in slots:
        if slot["ticker"]:
            log.append({"股票": slot["ticker"], "买入日": slot["date"].date(), "卖出日": "持有中",
                        "持有天数": slot["held"], "收益": price[slot["ticker"]] / slot["entry"] - 1, "原因": "未到期(按最新收盘估值)"})
    return pd.Series(equity), pd.DataFrame(log)


def path_stats(equity: pd.Series, label: str) -> dict:
    daily = equity.pct_change().dropna()
    return {
        "组合": label, "期末金额": equity.iloc[-1], "收益率": equity.iloc[-1] / equity.iloc[0] - 1,
        "年化波动": daily.std() * np.sqrt(252),
        "最大回撤": (equity / equity.cummax() - 1).min(),
        "最差一天": daily.min(),
    }


def benchmark(closes: pd.DataFrame, weights: dict[str, float]) -> pd.Series:
    days = closes.index[closes.index >= PERIOD_START]
    shares = {t: w / closes.at[days[0], t] for t, w in weights.items()}
    return pd.Series({d: sum(n * closes.at[d, t] for t, n in shares.items()) for d in days})


def run(closes: pd.DataFrame, sp500: pd.DataFrame | None) -> dict[str, pd.DataFrame]:
    semis = [t for ts in TARGETS.values() for t in ts if t in closes.columns]
    results = {"grid_semis": exit_grid(closes[semis])}
    if sp500 is not None:
        results["grid_sp500"] = exit_grid(sp500)

    eq_a, log_a = simulate_portfolio(closes, semis, require_selloff=False)
    eq_b, log_b = simulate_portfolio(closes, semis, require_selloff=True)
    rest = CAPITAL - SEMI_CAPITAL
    paths = [
        path_stats(eq_a, "规则A：单只信号就买（含 REGN/VRTX 和现金）"),
        path_stats(eq_b, "规则B：板块普跌时才买（含 REGN/VRTX 和现金）"),
        path_stats(benchmark(closes, {"SMH": SEMI_CAPITAL, **HOLDS}) + (rest - sum(HOLDS.values())),
                   "对照：同样结构，但半导体部分一直拿 SMH"),
        path_stats(benchmark(closes, {"NVDA": CAPITAL / 3, "TSM": CAPITAL / 3, "MU": CAPITAL / 3}), "对照：8000 全部买入持有 NVDA/TSM/MU"),
        path_stats(benchmark(closes, {"SMH": CAPITAL}), "对照：8000 全部买入持有 SMH"),
    ]
    monthly = pd.DataFrame({"规则A": eq_a, "规则B": eq_b}).resample("ME").last()
    monthly.index = monthly.index.to_period("M").astype(str)
    results.update({
        "portfolio": pd.DataFrame(paths),
        "trades_a": log_a, "trades_b": log_b,
        "monthly": monthly.rename_axis("月末").reset_index(),
    })
    return results


PERCENT = ["胜率", "平均收益", "中位收益", "最差一笔", "平均每天收益", "2023前平均收益", "2023后平均收益", "2023后胜率",
           "收益率", "年化波动", "最大回撤", "最差一天", "收益"]


def _render(table: pd.DataFrame) -> str:
    if table.empty:
        return "（无）"
    table = table.copy()
    for column in table.columns:
        if column in PERCENT:
            digits = 2 if column == "平均每天收益" else 1
            table[column] = table[column].map(lambda x, d=digits: "" if pd.isna(x) else f"{x:.{d}%}")
        elif table[column].dtype.kind == "f":
            table[column] = table[column].map(lambda x: "" if pd.isna(x) else f"{x:,.1f}")
    header = "| " + " | ".join(map(str, table.columns)) + " |"
    body = ["| " + " | ".join(map(str, row)) + " |" for row in table.itertuples(index=False)]
    return "\n".join([header, "|" + "---|" * len(table.columns), *body])


def write_report(results: dict[str, pd.DataFrame], out: Path, data_end) -> None:
    out.mkdir(parents=True, exist_ok=True)
    for name, table in results.items():
        table.to_csv(out / f"{name}.csv", index=False)
    sections = [
        f"# 止损止盈与震荡市模拟（数据截至 {data_end:%Y-%m-%d}）\n\n由 `python -m riskeval.exit_study` 生成，设定见该模块说明。",
        "## 出场规则网格：16 只半导体\n\n" + _render(results["grid_semis"]),
    ]
    if "grid_sp500" in results:
        sections.append("## 出场规则网格：S&P 500\n\n" + _render(results["grid_sp500"]))
    sections += [
        f"## 组合模拟：{PERIOD_START:%Y-%m-%d} 起，本金 8000\n\n" + _render(results["portfolio"]),
        "## 每月末金额\n\n" + _render(results["monthly"]),
        "## 规则 A 的交易\n\n" + _render(results["trades_a"]),
        "## 规则 B 的交易\n\n" + _render(results["trades_b"]),
    ]
    (out / "README.md").write_text("\n\n".join(sections) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> None:
    from riskeval import daily_data

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--start", default="2015-01-01")
    parser.add_argument("--out", default="reports/exit_study")
    parser.add_argument("--skip-sp500", action="store_true")
    args = parser.parse_args(argv)

    semis = [t for ts in TARGETS.values() for t in ts]
    closes = daily_data.download_closes(semis + list(HOLDS) + ["SMH"], args.start, chunk=50)
    sp500 = None if args.skip_sp500 else daily_data.download_closes(daily_data.sp500_tickers(), args.start)
    results = run(closes, sp500)
    write_report(results, Path(args.out), closes.index[-1])
    print(f"已写入 {args.out}/README.md")


if __name__ == "__main__":
    main()
