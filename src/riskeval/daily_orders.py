"""每日操作单：核心仓 SMH + 规则 A 超跌加码（回到中轨卖出，-20% 止损）。

    python -m riskeval.daily_orders --out reports/daily_orders

读取 portfolio/holdings.csv（实际持仓）和 portfolio/account.json（加码仓现金、仓位数、核心仓目标），
用最新收盘价给出下一个交易日收盘前要做的事：
- 加码仓：收盘回到 20 日均线（z ≥ 0）或较买入价跌 20% → 卖出；
- 空出的加码仓位：在 16 只半导体里按 z 值从低到高挑"跌破下轨且在 200 日线上方"的买入；
- 核心仓、分散仓：只显示市值，不操作；核心仓没买够时提示还差多少。
规则和 structure_study 里"核心60% SMH + A加码(2仓)"一致。
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from riskeval import signals
from riskeval.mr_screen import TARGETS

STOP = -0.20
NEAR = -1.5
HOLDINGS_COLUMNS = ["ticker", "role", "shares", "entry_price", "entry_date"]


def load_portfolio(folder: Path) -> tuple[pd.DataFrame, dict]:
    holdings = pd.read_csv(folder / "holdings.csv", comment="#", skipinitialspace=True)
    holdings = holdings.reindex(columns=HOLDINGS_COLUMNS).dropna(subset=["ticker"])
    holdings["ticker"] = holdings["ticker"].str.strip().str.upper()
    holdings["role"] = holdings["role"].str.strip().str.lower()
    holdings["shares"] = pd.to_numeric(holdings["shares"], errors="coerce").fillna(0.0)
    holdings["entry_price"] = pd.to_numeric(holdings["entry_price"], errors="coerce")
    account = json.loads((folder / "account.json").read_text(encoding="utf-8"))
    return holdings, account


def trigger_price(history: pd.Series, z_target: float = -2.0, window: int = 20) -> float:
    """下一个交易日收盘价低于这个价格时，z 值会 ≤ z_target（布林带随新收盘价一起变化）。"""
    recent = history.dropna().iloc[-(window - 1):].to_numpy()
    if len(recent) < window - 1:
        return np.nan

    def z_of(price: float) -> float:
        values = np.append(recent, price)
        return (price - values.mean()) / values.std(ddof=1)

    low, high = recent[-1] * 0.3, recent[-1] * 1.5
    if z_of(high) < z_target:
        return high
    for _ in range(60):
        mid_price = (low + high) / 2
        low, high = (mid_price, high) if z_of(mid_price) < z_target else (low, mid_price)
    return (low + high) / 2


def trigger_table(closes: pd.DataFrame, tickers: list[str], group_of: dict[str, str]) -> pd.DataFrame:
    """每只股票下一个交易日的买入触发价、不追高线（中轨）和 200 日线。"""
    day = closes.index[-1]
    z = signals.zscore(closes[tickers]).loc[day]
    mid = signals.sma(closes[tickers], 20).loc[day]
    sma200 = signals.sma(closes[tickers], 200).loc[day]
    rows = []
    for t in tickers:
        last, trig = closes.at[day, t], trigger_price(closes[t])
        if z[t] <= -2 and last > sma200[t]:
            state = "已触发：可按收盘价买入（低于中轨即可）"
        elif trig <= sma200[t]:
            state = "触发价低于 200 日线：跌到那里也不买"
        else:
            state = "未触发：收盘 ≤ 触发价才买"
        rows.append({"股票": t, "子行业": group_of.get(t, "ETF"), "最新收盘": last, "布林z值": round(z[t], 2),
                     "明日触发价": trig, "距触发价": trig / last - 1, "中轨(不追高线)": mid[t],
                     "200日线": sma200[t], "状态": state})
    return pd.DataFrame(rows).sort_values("距触发价", ascending=False)


def complete_closes(closes: pd.DataFrame, required: list[str], min_share: float = 0.9) -> pd.DataFrame:
    """去掉末尾数据不完整的行（数据源有时会先给出一行空价格）。"""
    present = [t for t in required if t in closes.columns]
    ok = closes[present].notna().mean(axis=1) >= min_share
    if "SMH" in closes.columns:
        ok &= closes["SMH"].notna()
    last_good = ok[ok].index.max()
    return closes.loc[:last_good]


def last_closed_session(now: pd.Timestamp | None = None) -> pd.Timestamp:
    """最近一个已经收盘的 NYSE 交易日（无时区日期）。"""
    from riskeval.sessions import nyse_schedule

    now = now or pd.Timestamp.now(tz="UTC")
    schedule = nyse_schedule(now - pd.Timedelta(days=10), now)
    closed = schedule[schedule["close"] <= now]
    return closed.index[-1]


def make_orders(closes: pd.DataFrame, holdings: pd.DataFrame, account: dict) -> dict[str, pd.DataFrame]:
    semis = [t for ts in TARGETS.values() for t in ts if t in closes.columns]
    group_of = {t: g for g, ts in TARGETS.items() for t in ts}
    day = closes.index[-1]
    z = signals.zscore(closes)
    mid = signals.sma(closes, 20)
    std = closes.rolling(20, min_periods=20).std()
    sma200 = signals.sma(closes, 200)
    price = closes.loc[day]

    overlay = holdings[holdings["role"] == "overlay"]
    sells, keep = [], []
    for _, h in overlay.iterrows():
        t = h["ticker"]
        change = price[t] / h["entry_price"] - 1 if h["entry_price"] else np.nan
        reason = ("止损：较买入价跌超 20%" if change <= STOP else
                  "回到中轨：收盘 ≥ 20 日均线" if z.at[day, t] >= 0 else None)
        row = {"股票": t, "持股数": h["shares"], "买入价": h["entry_price"], "最新收盘": price[t], "浮动盈亏": change,
               "布林z值": round(z.at[day, t], 2), "明日卖出线": closes[t].dropna().iloc[-19:].mean(), "止损价": h["entry_price"] * (1 + STOP)}
        (sells if reason else keep).append(row | ({"操作": "尽快卖出（按规则今天收盘就该卖）", "原因": reason} if reason
                                                else {"操作": "继续持有；收盘前价格 ≥ 明日卖出线或 ≤ 止损价就卖"}))

    held_value = sum(r["持股数"] * r["最新收盘"] for r in keep + sells)
    overlay_equity = float(account["overlay_cash"]) + held_value
    sale_cash = sum(r["持股数"] * r["最新收盘"] for r in sells)
    free_slots = int(account["overlay_slots"]) - len(keep)
    budget = overlay_equity / int(account["overlay_slots"])
    cash_after_sales = float(account["overlay_cash"]) + sale_cash

    held = set(holdings["ticker"])
    zt = z.loc[day, semis]
    eligible = (zt <= -2) & (price[semis] > sma200.loc[day, semis])
    candidates = zt[eligible & ~zt.index.isin(held)].sort_values()
    buys = []
    for rank, (t, zv) in enumerate(candidates.items(), start=1):
        amount = min(budget, cash_after_sales) if rank <= free_slots else np.nan
        if rank <= free_slots:
            cash_after_sales -= amount
        buys.append({"排序": rank, "股票": t, "子行业": group_of[t], "布林z值": round(zv, 2),
                     "下轨": mid.at[day, t] - 2 * std.at[day, t], "中轨": mid.at[day, t],
                     "相对200日线": price[t] / sma200.at[day, t] - 1,
                     "操作": "买入" if rank <= free_slots else "候补",
                     "建议金额": amount})

    near = zt[(zt > -2) & (zt <= NEAR) & (price[semis] > sma200.loc[day, semis]) & ~zt.index.isin(held)].sort_values()
    watch = [{"股票": t, "子行业": group_of[t], "布林z值": round(v, 2), "下轨": mid.at[day, t] - 2 * std.at[day, t]}
             for t, v in near.items()]

    others = []
    for _, h in holdings[holdings["role"] != "overlay"].iterrows():
        t = h["ticker"]
        others.append({"股票": t, "类别": {"core": "核心仓", "hold": "分散仓"}.get(h["role"], h["role"]),
                       "持股数": h["shares"], "市值": h["shares"] * price[t],
                       "浮动盈亏": price[t] / h["entry_price"] - 1 if h["entry_price"] else np.nan})
    core_value = sum(r["市值"] for r in others if r["类别"] == "核心仓")
    core_gap = max(float(account.get("core_target", 0)) - core_value, 0.0)

    below = (z.loc[day, semis] <= -2).mean()
    market = pd.DataFrame([{
        "日期": day.date(), "16只里跌破下轨的比例": below,
        "SMH布林z值": round(z.at[day, "SMH"], 2), "SMH相对200日线": price["SMH"] / sma200.at[day, "SMH"] - 1,
        "加码仓净值": overlay_equity, "空仓位": max(free_slots, 0), "核心仓还差": core_gap,
    }])
    triggers = trigger_table(closes, semis + ["SMH"], group_of)
    return {"market": market, "triggers": triggers, "sells": pd.DataFrame(sells), "keep": pd.DataFrame(keep),
            "buys": pd.DataFrame(buys), "watch": pd.DataFrame(watch), "others": pd.DataFrame(others)}


PERCENT = {"浮动盈亏", "相对200日线", "16只里跌破下轨的比例", "SMH相对200日线", "距触发价"}
MONEY = {"买入价", "最新收盘", "明日卖出线", "止损价", "下轨", "中轨", "建议金额", "市值", "加码仓净值", "核心仓还差",
         "明日触发价", "中轨(不追高线)", "200日线"}


def _render(table: pd.DataFrame) -> str:
    if table.empty:
        return "（无）"
    table = table.copy()
    for column in table.columns:
        if column in PERCENT:
            table[column] = table[column].map(lambda x: "" if pd.isna(x) else f"{x:.1%}")
        elif column in MONEY:
            table[column] = table[column].map(lambda x: "" if pd.isna(x) else f"{x:,.2f}")
    header = "| " + " | ".join(map(str, table.columns)) + " |"
    body = ["| " + " | ".join(map(str, row)) + " |" for row in table.itertuples(index=False)]
    return "\n".join([header, "|" + "---|" * len(table.columns), *body])


def summary_lines(orders: dict[str, pd.DataFrame]) -> list[str]:
    lines = []
    for _, r in orders["sells"].iterrows():
        lines.append(f"卖出 {r['股票']}（{r['原因']}，浮动盈亏 {r['浮动盈亏']:.1%}）")
    buys = orders["buys"]
    for _, r in buys[buys["操作"] == "买入"].iterrows() if not buys.empty else []:
        lines.append(f"买入 {r['股票']} 约 {r['建议金额']:,.0f}（z = {r['布林z值']}）")
    gap = orders["market"].iloc[0]["核心仓还差"]
    if gap >= 1:
        lines.append(f"核心仓 SMH 还差约 {gap:,.0f} 没买")
    return lines


def write_report(orders: dict[str, pd.DataFrame], out: Path, warning: str | None = None) -> list[str]:
    out.mkdir(parents=True, exist_ok=True)
    day = orders["market"].iloc[0]["日期"]
    todo = ([warning] if warning else []) + summary_lines(orders)
    sections = [
        f"# 每日操作单（按 {day} 收盘价计算）\n\n由 `python -m riskeval.daily_orders` 自动生成。"
        "建议在下一个交易日收盘前约 10 分钟、价格和下面差不多时执行，用限价单。"
        "成交后请更新 `portfolio/holdings.csv`（买入价填实际成交价）和 `portfolio/account.json` 里的 `overlay_cash`。"
        "这是规则的机械输出，不是投资建议。",
        "## 要做的事\n\n" + ("\n".join(f"- {line}" for line in todo) if todo else "- 今天没有需要操作的。"),
        "## 板块状态\n\n" + _render(orders["market"]),
        "## 加码仓：要卖出的\n\n" + _render(orders["sells"]),
        "## 加码仓：继续持有（明日卖出线和止损价）\n\n回测是在收盘价回到 20 日均线的当天收盘卖出。"
        "下一个交易日收盘前约 10 分钟，如果价格 ≥ 明日卖出线（前 19 个交易日的收盘均值），"
        "收盘价大概率会回到中轨，就在收盘前卖出；价格 ≤ 止损价也卖出。\n\n" + _render(orders["keep"]),
        "## 新信号（跌破下轨且在 200 日线上方，按 z 值排序）\n\n" + _render(orders["buys"]),
        "## 接近下轨，明天可能触发\n\n" + _render(orders["watch"]),
        "## 下一个交易日的买入触发价\n\n收盘价 ≤ 明日触发价就会出现买入信号（还要在 200 日线上方）；"
        "已经触发的，收盘价只要还低于中轨就可以买，高于中轨就不追。按距离从近到远排序。\n\n" + _render(orders["triggers"]),
        "## 核心仓和分散仓\n\n" + _render(orders["others"]),
    ]
    (out / "README.md").write_text("\n\n".join(sections) + "\n", encoding="utf-8")
    (out / "todo.txt").write_text("\n".join(todo) + ("\n" if todo else ""), encoding="utf-8")
    (out / "date.txt").write_text(f"{day}{'-stale' if warning else ''}\n", encoding="utf-8")
    return todo


def main(argv: list[str] | None = None) -> None:
    from riskeval import daily_data

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--portfolio", default="portfolio")
    parser.add_argument("--out", default="reports/daily_orders")
    args = parser.parse_args(argv)

    holdings, account = load_portfolio(Path(args.portfolio))
    tickers = sorted({t for ts in TARGETS.values() for t in ts} | {"SMH"} | set(holdings["ticker"]))
    start = (pd.Timestamp.today() - pd.Timedelta(days=500)).strftime("%Y-%m-%d")
    raw = daily_data.download_closes(tickers, start, chunk=50)
    closes = complete_closes(raw, tickers)
    expected = last_closed_session()
    warning = None
    if closes.index[-1] < expected:
        warning = (f"数据警告：最新完整数据只到 {closes.index[-1]:%Y-%m-%d}，"
                   f"应有 {expected:%Y-%m-%d} 的收盘价。操作单可能过期，请稍后在 Actions 里手动重跑 daily-orders。")
    todo = write_report(make_orders(closes, holdings, account), Path(args.out), warning)
    print("\n".join(todo) if todo else "今天没有需要操作的。")


if __name__ == "__main__":
    main()
