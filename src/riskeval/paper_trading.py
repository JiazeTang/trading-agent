"""模拟盘（影子账本）：加码仓的现行规则和"按波动定仓位"候选，从 2026-10-30 收盘起每天按收盘价记账。

    python -m riskeval.paper_trading --out reports/paper_trading

以下在 2026-10-30 开盘前写死，之后不改。要改规则就另开一个新账本，旧账本照常记下去。

- 资金：只管加码仓 1600，2 个仓位。SMH 核心仓、REGN、VRTX、现金都不在这里。
- 信号：16 只半导体里，收盘跌破 20 日布林下轨（z ≤ -2）且在 200 日线上方的，按 z 值从低到高排，下一个交易日收盘买入。
- 出场：收盘回到 20 日均线（z ≥ 0）当天收盘卖出；收盘较买入价跌 20% 当天收盘止损。不设最长持有天数（和实盘规则一致）。
- 账本 A（现行）：每个仓位 = 加码仓当前净值 ÷ 2。
- 账本 B（候选）：A 的金额再乘以 min(1, 30% ÷ 入场前 20 日年化波动)，年化波动最低按 10% 算；没用到的钱留作现金。
- 两本账用同一份数据、同一套信号，只差仓位大小。按收盘价成交，可以买碎股，每次买卖扣 0.05%。
  每笔买入另记"整股能买几股"和取整后没花出去的钱，用来判断不能买碎股时能不能照做。
- 每天的结果由 GitHub Actions 提交到 reports/paper_trading，git 历史就是当时的记录，事后不能改。
- 同一套代码从 2016 年起跑一遍作为回测参照，看模拟盘是否落在回测给出的范围里。

评估（写死）：
- 2027-04-30 之前，或账本 A 完成的交易不到 8 笔之前，不做任何决定，也不因为盈亏改规则。
- 到期后，实盘加码仓改用 B 的条件，三条都要满足：
  1. 有持仓的日子里，B 的年化波动不超过 A 的 85%（回测参照见报告）；
  2. B 的最大回撤不比 A 深（B 只是把仓位缩小，如果更深，说明代码或数据有问题，先查原因）；
  3. 实际下单做得到：券商能买碎股；或者只能买整股时，B 的买入取整后没花出去的钱，平均不超过计划金额的一半。
- 两本账的收益差在半年里没有统计意义（最短业绩长度要好几年），不作为依据。
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np
import pandas as pd

from riskeval.mr_screen import TARGETS
from riskeval.swing_study import COST, ENTRIES, entry_flags, exit_reason, indicators, net, new_position, step

START = pd.Timestamp("2026-10-30")
EVALUATE_AFTER = pd.Timestamp("2027-04-30")
MIN_TRADES = 8
VOL_RATIO_MAX = 0.85
CAPITAL, SLOTS = 1600.0, 2
STOP = ("fixed", 0.20)
TARGET_VOL, VOL_FLOOR = 0.30, 0.10
BACKTEST_START = pd.Timestamp("2016-01-01")
LEDGERS = {"A 现行：等额": "equal", "B 候选：按波动定仓位": "vol"}


def size_factor(sigma_daily: float, sizing: str) -> float:
    if sizing == "equal":
        return 1.0
    return min(1.0, TARGET_VOL / max(sigma_daily * np.sqrt(252), VOL_FLOOR))


def run_ledger(px: pd.DataFrame, sizing: str, start=START, capital: float = CAPITAL, slots: int = SLOTS) -> dict:
    """按收盘价逐日记账。返回每日净值和持仓比例、已完成的交易、仍在持有的仓位。"""
    ind = indicators(px)
    signal = entry_flags(px, ind, sector=False)[ENTRIES[0]]
    close, z, ma, sigma, flags = (a.to_numpy() for a in (px, ind["z"], ind["ma"], ind["sigma"], signal))
    tickers, dates = list(px.columns), px.index
    first = dates.searchsorted(start)
    cash, open_, pending, trades = capital, {}, [], []
    equity, exposure = {}, {}
    last = close[first].copy() if first < len(dates) else None

    for d in range(first, len(dates)):
        price = np.where(np.isfinite(close[d]), close[d], last)
        last = price
        sold = set()
        for k in list(open_):
            pos = open_[k]
            if not np.isfinite(close[d, k]):
                continue
            step(pos, price[k])
            reason = exit_reason(pos, price[k], z[d, k], ma[d, k], "mean", STOP)
            if reason:
                cash += pos["shares"] * price[k] * (1 - COST)
                trades.append({"股票": tickers[k], "买入日": pos["date"].date(), "买入价": pos["entry"], "金额": pos["amount"],
                               "卖出日": dates[d].date(), "卖出价": price[k], "持有天数": pos["held"],
                               "收益": net(price[k] / pos["entry"] - 1), "原因": "回到中轨" if reason == "出场" else reason})
                del open_[k]
                sold.add(k)
        stocks = sum(p["shares"] * price[k] for k, p in open_.items())
        for k, sig in pending:
            if len(open_) >= slots or k in open_ or k in sold or not np.isfinite(close[d, k]):
                continue
            planned = (cash + stocks) / slots
            amount = min(planned * size_factor(sig, sizing), cash)
            if amount < 1:
                continue
            pos = new_position(price[k], sig, dates[d])
            pos |= {"max_hold": None, "amount": amount, "shares": amount * (1 - COST) / price[k],
                    "whole": math.floor(amount / price[k])}
            open_[k] = pos
            cash -= amount
            stocks += pos["shares"] * price[k]
        today = np.flatnonzero(flags[d] & np.isfinite(sigma[d]))
        pending = [(k, sigma[d, k]) for k in today[np.argsort(z[d, today])]]
        equity[dates[d]] = cash + stocks
        exposure[dates[d]] = stocks / (cash + stocks)

    holding = [{"股票": tickers[k], "买入日": p["date"].date(), "买入价": p["entry"], "金额": p["amount"],
                "股数": p["shares"], "整股能买": p["whole"], "最新收盘": last[k], "浮动盈亏": last[k] / p["entry"] - 1,
                "明日卖出线": px[tickers[k]].dropna().iloc[-19:].mean(), "止损价": p["entry"] * (1 - STOP[1])}
               for k, p in open_.items()]
    return {"equity": pd.Series(equity, dtype=float), "exposure": pd.Series(exposure, dtype=float),
            "trades": pd.DataFrame(trades), "holding": pd.DataFrame(holding)}


def ledger_stats(result: dict) -> dict:
    eq, expo = result["equity"], result["exposure"]
    out = {"净值": eq.iloc[-1] if len(eq) else CAPITAL, "收益": (eq.iloc[-1] / CAPITAL - 1) if len(eq) else 0.0,
           "完成交易": float(len(result["trades"])), "持仓数": float(len(result["holding"]))}
    daily = eq.pct_change().dropna()
    held = (expo.shift(1).reindex(daily.index) > 0)
    out["有持仓的天数"] = float(held.sum())
    out["持仓日年化波动"] = daily[held].std() * np.sqrt(252) if held.sum() > 1 else np.nan
    out["最大回撤"] = (eq / eq.cummax() - 1).min() if len(eq) else 0.0
    return out


def backtest_stats(result: dict) -> dict:
    eq, expo = result["equity"], result["exposure"]
    daily = eq.pct_change().dropna()
    years = len(daily) / 252
    vol = daily.std() * np.sqrt(252)
    held = expo.shift(1).reindex(daily.index) > 0
    return {"年化收益": (eq.iloc[-1] / eq.iloc[0]) ** (1 / years) - 1, "年化波动": vol,
            "持仓日年化波动": daily[held].std() * np.sqrt(252), "Sharpe": daily.mean() * 252 / vol,
            "最大回撤": (eq / eq.cummax() - 1).min(), "每年交易笔数": len(result["trades"]) / years}


def unspent_share(trades: pd.DataFrame, holding: pd.DataFrame) -> float:
    """只能买整股时，取整后没花出去的钱占计划金额的平均比例。"""
    rows = []
    for table in (trades, holding):
        if len(table):
            for _, r in table.iterrows():
                whole = math.floor(r["金额"] / r["买入价"])
                rows.append(1 - whole * r["买入价"] / r["金额"])
    return float(np.mean(rows)) if rows else np.nan


def evaluate(paper: dict, today) -> pd.DataFrame:
    a, b = (ledger_stats(paper[name]) for name in LEDGERS)
    ratio = b["持仓日年化波动"] / a["持仓日年化波动"] if a["持仓日年化波动"] else np.nan
    names = list(LEDGERS)
    whole = unspent_share(paper[names[1]]["trades"], paper[names[1]]["holding"])
    ready = today >= EVALUATE_AFTER and a["完成交易"] >= MIN_TRADES
    rows = [
        {"条目": "评估时间", "要求": f"{EVALUATE_AFTER:%Y-%m-%d} 之后，且 A 完成至少 {MIN_TRADES} 笔",
         "现在": f"{today:%Y-%m-%d}，A 已完成 {a['完成交易']:.0f} 笔", "是否满足": "是" if ready else "还没到"},
        {"条目": "1. 持仓日波动 B ÷ A", "要求": f"≤ {VOL_RATIO_MAX:.0%}",
         "现在": "数据不够" if np.isnan(ratio) else f"{ratio:.0%}", "是否满足": "—" if np.isnan(ratio) else ("是" if ratio <= VOL_RATIO_MAX else "否")},
        {"条目": "2. 最大回撤 B 不比 A 深", "要求": "B ≥ A", "现在": f"A {a['最大回撤']:.1%}，B {b['最大回撤']:.1%}",
         "是否满足": "是" if b["最大回撤"] >= a["最大回撤"] - 1e-12 else "否"},
        {"条目": "3. 只能买整股时没花出去的钱（B）", "要求": "能买碎股，或平均 ≤ 50%",
         "现在": "还没有买入" if np.isnan(whole) else f"平均 {whole:.0%}", "是否满足": "看你的券商"},
    ]
    if not ready:
        rows.append({"条目": "结论", "要求": "", "现在": "评估期未到，照常执行现行规则，不因盈亏做决定", "是否满足": ""})
    return pd.DataFrame(rows)


# ---------- 报告 ----------

PERCENT = {"收益", "浮动盈亏", "持仓日年化波动", "最大回撤", "年化收益", "年化波动"}
MONEY = {"净值", "买入价", "卖出价", "金额", "最新收盘", "明日卖出线", "止损价"}


def _render(table: pd.DataFrame) -> str:
    if table is None or table.empty:
        return "（无）"
    table = table.copy()
    for column in table.columns:
        if table[column].dtype.kind not in "fi":
            continue
        fmt = ((lambda x: f"{x:.1%}") if column in PERCENT else (lambda x: f"{x:,.2f}") if column in MONEY else
               (lambda x: f"{x:.3f}") if column == "股数" else (lambda x: f"{x:.2f}") if column == "Sharpe" else
               (lambda x: f"{x:.1f}") if column == "每年交易笔数" else (lambda x: f"{x:.0f}"))
        table[column] = table[column].map(lambda x, f=fmt: "" if pd.isna(x) else f(x))
    header = "| " + " | ".join(map(str, table.columns)) + " |"
    body = ["| " + " | ".join(map(str, row)) + " |" for row in table.itertuples(index=False)]
    return "\n".join([header, "|" + "---|" * len(table.columns), *body])


def run(closes: pd.DataFrame, today=None) -> dict:
    semis = [t for ts in TARGETS.values() for t in ts if t in closes.columns]
    px = closes[semis].dropna(how="all")
    today = today if today is not None else px.index[-1]
    paper = {name: run_ledger(px, sizing, start=START) for name, sizing in LEDGERS.items()}
    backtest = {name: run_ledger(px, sizing, start=BACKTEST_START) for name, sizing in LEDGERS.items()}
    return {"paper": paper, "backtest": backtest, "today": today, "data_end": px.index[-1]}


def write_report(results: dict, out: Path, warning: str | None = None) -> None:
    out.mkdir(parents=True, exist_ok=True)
    paper, backtest = results["paper"], results["backtest"]
    status = pd.DataFrame([{"账本": name} | ledger_stats(r) for name, r in paper.items()])
    reference = pd.DataFrame([{"账本": name} | backtest_stats(r) for name, r in backtest.items()])
    ratio = reference.loc[1, "持仓日年化波动"] / reference.loc[0, "持仓日年化波动"]
    equity = pd.DataFrame({name: r["equity"] for name, r in paper.items()})
    equity.index.name = "date"
    equity.to_csv(out / "equity.csv")
    for i, (name, r) in enumerate(paper.items()):
        r["trades"].to_csv(out / f"trades_{'AB'[i]}.csv", index=False)
    started = len(equity) > 0
    sections = [
        f"# 模拟盘（数据截至 {results['data_end']:%Y-%m-%d}）\n\n"
        f"由 `python -m riskeval.paper_trading` 生成，规则和评估标准在 2026-10-30 写死，见该模块说明。"
        "只管加码仓 1600、2 个仓位；两本账信号相同，只差仓位大小。按收盘价记账，扣 0.05% 成本。"
        "规则输出加历史回测，不是投资建议。",
    ]
    if warning:
        sections.append(f"> {warning}")
    if not started:
        sections.append(f"还没开始：第一天是 {START:%Y-%m-%d} 收盘（当天只记 1600 现金，信号在下一个交易日收盘买入）。")
    sections += [
        "## 现在的状态\n\n" + _render(status),
        "## 评估进度\n\n" + _render(evaluate(paper, results["today"])),
    ]
    for name, r in paper.items():
        sections.append(f"## {name}：持仓\n\n明日卖出线 = 前 19 日收盘均值，收盘前价格 ≥ 这条线就卖；"
                        "整股能买 = 买入金额能买几股整股。\n\n" + _render(r["holding"]))
        sections.append(f"## {name}：已完成的交易\n\n" + _render(r["trades"]))
    sections.append(f"## 回测参照：同一套代码从 {BACKTEST_START:%Y-%m-%d} 跑到现在\n\n"
                    f"有持仓的日子里，B 的波动是 A 的 {ratio:.0%}。模拟盘的数字应该大致落在这个范围；"
                    "差得很远时先查代码和数据。16 只半导体有幸存者偏差。\n\n" + _render(reference))
    (out / "README.md").write_text("\n\n".join(sections) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> None:
    from riskeval import daily_data
    from riskeval.daily_orders import complete_closes, last_closed_session

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--start", default="2015-01-01")
    parser.add_argument("--out", default="reports/paper_trading")
    args = parser.parse_args(argv)

    semis = [t for ts in TARGETS.values() for t in ts]
    raw = daily_data.download_closes(semis + ["SMH"], args.start, chunk=50)
    closes = complete_closes(raw, semis)
    expected = last_closed_session()
    warning = None
    if closes.index[-1] < expected:
        warning = f"数据警告：最新完整数据只到 {closes.index[-1]:%Y-%m-%d}，应有 {expected:%Y-%m-%d}。今天的账可能没记上，下次运行会补上。"
    write_report(run(closes), Path(args.out), warning)
    print(f"已写入 {args.out}/README.md")


if __name__ == "__main__":
    main()
