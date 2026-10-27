"""交易风格对比：日内突破、波段动量、趋势持有、均值回归、等牛市，放在同一套口径下回测。

    python -m riskeval.style_compare --out reports/style_compare

这是历史回测，不是实时模拟盘。以下设定在看结果之前写死：

标的：QQQ、SMH（ETF，没有幸存者偏差），以及 16 只半导体等权（按今天的市值挑选，有幸存者偏差）。
多只股票时每只固定分 1/N 的资金，各自独立交易。

成本（单边，含佣金和滑点）：理想 0；一般 0.05%；不理想 0.15%。

日内（不过夜，每天收盘前全部卖出）
- D1 开盘买、收盘卖：作为日内的基准。
- D2 波动率突破（Larry Williams）：价格涨到"开盘价 + 0.5 × 前一天振幅"时买入，按这个价格成交，收盘卖出。
- D3 小时线开盘区间突破（ORB）：某根小时线收盘站上第一小时的最高价时买入，收盘跌破第一小时最低价就卖，
  否则收盘卖出。数据只有最近约 2 年。

波段 / 动量（持有几天到几个月）
- S1 唐奇安突破：收盘创 50 日新高，并且价格 > 50 日线 > 200 日线时买入；收盘跌破 20 日线卖出。
- S2 新高 + 宽跟踪止损：收盘创 252 日新高时买入；收盘跌破"买入后最高收盘价 − 10 × ATR(20)"时卖出。
- S3 动量轮动：每月最后一个交易日，从 16 只里选过去 126 日涨幅最高的 3 只等权持有一个月；
  SMH 在 200 日线下方时空仓。

均值回归（现行方案）
- M1 规则 A：跌破 20 日布林下轨且在 200 日线上方时买入，回到 20 日均线卖出，-20% 止损，3 个仓位。
- M2 核心 60% SMH + 规则 A 加码（当前方案）。

等牛市 / 长期持有
- L1 一直持有。
- L2 200 日线择时：收盘在 200 日线上方就持有，下方就空仓。

除日内外，信号都按收盘价算，下一个交易日收盘成交。
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from riskeval import signals
from riskeval.mr_screen import TARGETS

START = pd.Timestamp("2016-01-01")
COSTS = {"理想": 0.0, "一般": 0.0005, "不理想": 0.0015}
PERIODS = {
    "2022熊市": ("2022-01-01", "2022-12-31"),
    "2026年4-5月牛市": ("2026-04-01", "2026-05-31"),
    "2026年6月起震荡": ("2026-06-01", None),
}


# ---------- 每种风格：返回（毛收益, 当天单边交易次数, 是否持仓），都是"日期 × 代码"的表 ----------

def open_to_close(o, c):
    gross = c / o - 1
    traded = gross.notna()
    return gross.fillna(0), 2.0 * traded, traded


def vol_breakout(o, h, l, c, k=0.5):
    trigger = o + k * (h.shift(1) - l.shift(1))
    hit = (h >= trigger) & trigger.notna()
    gross = (c / trigger - 1).where(hit, 0.0)
    return gross.fillna(0), 2.0 * hit, hit


def _from_state(c: pd.DataFrame, state: pd.DataFrame):
    """收盘时决定的持仓状态，下一个交易日收盘成交。"""
    state = state.astype(float).fillna(0)
    held = state.shift(2).fillna(0)
    gross = held * c.pct_change(fill_method=None).fillna(0)
    turns = state.diff().fillna(state).abs().shift(1).fillna(0)
    return gross, turns, held > 0


def _state_machine(c: pd.Series, enter: pd.Series, should_exit) -> pd.Series:
    state, inside, peak = np.zeros(len(c)), False, np.nan
    values, enters = c.to_numpy(), enter.fillna(False).to_numpy()
    for i in range(len(c)):
        if inside:
            peak = max(peak, values[i])
            if should_exit(i, peak):
                inside = False
        elif enters[i]:
            inside, peak = True, values[i]
        state[i] = inside
    return pd.Series(state, index=c.index)


def donchian(c):
    sma20, sma50, sma200 = signals.sma(c, 20), signals.sma(c, 50), signals.sma(c, 200)
    high50 = c.shift(1).rolling(50, min_periods=50).max()
    state = pd.DataFrame({
        t: _state_machine(c[t], (c[t] >= high50[t]) & (c[t] > sma50[t]) & (sma50[t] > sma200[t]),
                          lambda i, peak, t=t: c[t].iat[i] < sma20[t].iat[i])
        for t in c.columns})
    return _from_state(c, state)


def new_high_trail(h, l, c, atr_mult=10.0):
    prev = c.shift(1)
    tr = pd.concat([h - l, (h - prev).abs(), (l - prev).abs()]).groupby(level=0).max()
    atr = tr.rolling(20, min_periods=20).mean()
    high252 = c.shift(1).rolling(252, min_periods=252).max()
    state = pd.DataFrame({
        t: _state_machine(c[t], c[t] >= high252[t],
                          lambda i, peak, t=t: c[t].iat[i] < peak - atr_mult * atr[t].iat[i])
        for t in c.columns})
    return _from_state(c, state)


def trend_filter(c):
    return _from_state(c, c > signals.sma(c, 200))


def buy_and_hold(c):
    return _from_state(c, c.notna())


def momentum_rotation(c, gate: pd.Series, top: int = 3, lookback: int = 126):
    month_end = c.index.to_series().groupby(c.index.to_period("M")).max()
    weights = pd.DataFrame(np.nan, index=c.index, columns=c.columns)
    sma_gate = signals.sma(gate, 200)
    momentum = c / c.shift(lookback) - 1
    for day in month_end:
        row = pd.Series(0.0, index=c.columns)
        if gate.get(day, np.nan) > sma_gate.get(day, np.nan):
            best = momentum.loc[day].dropna().nlargest(top).index
            row[best] = 1.0 / top
        weights.loc[day] = row
    weights = weights.ffill().fillna(0)
    held = weights.shift(2).fillna(0)
    gross = (held * c.pct_change(fill_method=None).fillna(0)).sum(axis=1)
    turns = weights.diff().abs().sum(axis=1).shift(1).fillna(0)
    return gross, turns, held.sum(axis=1) > 0


def hourly_orb(o, h, l, c):
    """小时线开盘区间突破，返回每天每只的（毛收益, 单边次数, 是否交易）。"""
    days = c.index.tz_convert("America/New_York").normalize().tz_localize(None) if c.index.tz else c.index.normalize()
    out_g, out_t = {}, {}
    for t in c.columns:
        frame = pd.DataFrame({"h": h[t], "l": l[t], "c": c[t], "day": days}).dropna()
        gross, turns = {}, {}
        for day, bars in frame.groupby("day"):
            if len(bars) < 3:
                continue
            top, bottom = bars["h"].iat[0], bars["l"].iat[0]
            entry = exit_ = None
            for close in bars["c"].iloc[1:]:
                if entry is None and close > top:
                    entry = close
                elif entry is not None and close < bottom:
                    exit_ = close
                    break
            if entry is None:
                gross[day], turns[day] = 0.0, 0.0
            else:
                gross[day] = (exit_ if exit_ is not None else bars["c"].iat[-1]) / entry - 1
                turns[day] = 2.0
        out_g[t], out_t[t] = pd.Series(gross), pd.Series(turns)
    gross, turns = pd.DataFrame(out_g).fillna(0), pd.DataFrame(out_t).fillna(0)
    return gross, turns, turns > 0


# ---------- 汇总 ----------

def net_returns(gross, turns, cost: float) -> pd.Series:
    net = gross - turns * cost
    return net.mean(axis=1) if isinstance(net, pd.DataFrame) else net


def metrics(daily: pd.Series, exposure, turns, start=START) -> dict:
    daily = daily[daily.index >= start]
    equity = (1 + daily).cumprod()
    years = len(daily) / 252
    cagr = equity.iloc[-1] ** (1 / years) - 1
    vol = daily.std() * np.sqrt(252)
    yearly = (1 + daily).groupby(daily.index.year).prod() - 1
    full_years = yearly[[y for y in yearly.index if (daily.index.year == y).sum() > 200]]
    exp = (exposure.mean(axis=1) if isinstance(exposure, pd.DataFrame) else exposure.astype(float))
    trn = (turns.mean(axis=1) if isinstance(turns, pd.DataFrame) else turns)
    out = {"年化收益": cagr, "年化波动": vol, "收益/波动": cagr / vol if vol else np.nan,
           "最大回撤": (equity / equity.cummax() - 1).min(),
           "最好一年": full_years.max(), "中位一年": full_years.median(), "最差一年": full_years.min(),
           "持仓时间": exp[exp.index >= start].mean(), "每年单边交易次数": trn[trn.index >= start].sum() / years}
    for name, (a, b) in PERIODS.items():
        part = daily.loc[a:b] if b else daily.loc[a:]
        out[name] = (1 + part).prod() - 1 if len(part) else np.nan
    return out


def run_daily(ohlc: dict[str, pd.DataFrame], semis: list[str]) -> pd.DataFrame:
    o, h, l, c = (ohlc[k] for k in ["open", "high", "low", "close"])
    universes = {"QQQ": ["QQQ"], "SMH": ["SMH"], "16只半导体": semis}
    styles = {
        "D1 日内：开盘买收盘卖": lambda u: open_to_close(o[u], c[u]),
        "D2 日内：波动率突破": lambda u: vol_breakout(o[u], h[u], l[u], c[u]),
        "S1 波段：唐奇安50日突破": lambda u: donchian(c[u]),
        "S2 动量：新高+10ATR跟踪止损": lambda u: new_high_trail(h[u], l[u], c[u]),
        "L1 长期：一直持有": lambda u: buy_and_hold(c[u]),
        "L2 长期：200日线择时": lambda u: trend_filter(c[u]),
    }
    rows = []
    for style, fn in styles.items():
        for uname, u in universes.items():
            gross, turns, held = fn(u)
            for cost_name, cost in COSTS.items():
                rows.append({"风格": style, "标的": uname, "成本": cost_name}
                            | metrics(net_returns(gross, turns, cost), held, turns))
    gross, turns, held = momentum_rotation(c[semis], c["SMH"])
    for cost_name, cost in COSTS.items():
        rows.append({"风格": "S3 动量轮动：月度前3名", "标的": "16只半导体", "成本": cost_name}
                    | metrics(gross - turns * cost, held, turns))
    rows += mean_reversion_rows(c, semis)
    return pd.DataFrame(rows)


def net_daily_returns(equity: pd.Series, log: pd.DataFrame, cost: float, capital: float) -> pd.Series:
    """structure_study.simulate 的净值扣掉单边成本（买入金额和卖出金额各收一次）后的日收益。"""
    charges = pd.Series(0.0, index=equity.index)
    for _, trade in log.iterrows():
        for day, amount in [(trade["买入日"], trade["仓位"]), (trade["卖出日"], trade["仓位"] * (1 + trade["收益"]))]:
            stamp = pd.Timestamp(day)
            if stamp in charges.index:
                charges[stamp] += amount * cost
    adjusted = equity - charges.cumsum()
    return adjusted.pct_change().fillna(adjusted.iloc[0] / capital - 1)


def mean_reversion_rows(c: pd.DataFrame, semis: list[str]) -> list[dict]:
    from riskeval.structure_study import CAPITAL, VARIANTS, build_rules, simulate

    rows = []
    rules = build_rules(c[semis])
    for label, key in {"M1 均值回归：规则A": "现行A：单只信号+回到中轨，等额3仓",
                       "M2 均值回归：核心60%SMH+规则A（当前方案）": "核心60% SMH + A加码(2仓)"}.items():
        equity, exposure, log = simulate(c[semis], c["SMH"], rules, START, **VARIANTS[key])
        for cost_name, cost in COSTS.items():
            daily = net_daily_returns(equity, log, cost, CAPITAL)
            turns = pd.Series(0.0, index=equity.index)
            for column in ["买入日", "卖出日"]:
                for day in log[column]:
                    if pd.Timestamp(day) in turns.index:
                        turns[pd.Timestamp(day)] += 1
            rows.append({"风格": label, "标的": "16只半导体(+SMH)", "成本": cost_name}
                        | metrics(daily, exposure > 0, turns))
    return rows


def run_hourly(hourly: dict[str, pd.DataFrame], daily_close: pd.DataFrame, daily_open: pd.DataFrame,
               names: list[str]) -> pd.DataFrame:
    gross, turns, traded = hourly_orb(*(hourly[k][names] for k in ["open", "high", "low", "close"]))
    start = gross.index.min()
    rows = []
    for cost_name, cost in COSTS.items():
        rows.append({"风格": "D3 日内：小时线开盘区间突破", "标的": "、".join(names), "成本": cost_name}
                    | metrics(net_returns(gross, turns, cost), traded, turns, start=start))
        g, t, held = open_to_close(daily_open[names], daily_close[names])
        rows.append({"风格": "D1 日内：开盘买收盘卖（同期对照）", "标的": "、".join(names), "成本": cost_name}
                    | metrics(net_returns(g, t, cost), held, t, start=start))
    g, t, held = buy_and_hold(daily_close[names])
    rows.append({"风格": "L1 一直持有（同期对照）", "标的": "、".join(names), "成本": "一般"}
                | metrics(net_returns(g, t, COSTS["一般"]), held, t, start=start))
    return pd.DataFrame(rows)


NOT_PERCENT = {"收益/波动", "每年单边交易次数"}


def _render(table: pd.DataFrame) -> str:
    if table.empty:
        return "（无）"
    table = table.copy()
    for column in table.columns:
        if table[column].dtype.kind == "f":
            fmt = (lambda x: f"{x:.2f}" if column == "收益/波动" else f"{x:.0f}") if column in NOT_PERCENT else (lambda x: f"{x:.1%}")
            table[column] = table[column].map(lambda x, f=fmt: "" if pd.isna(x) else f(x))
    header = "| " + " | ".join(map(str, table.columns)) + " |"
    body = ["| " + " | ".join(map(str, row)) + " |" for row in table.itertuples(index=False)]
    return "\n".join([header, "|" + "---|" * len(table.columns), *body])


def write_report(daily: pd.DataFrame, hourly: pd.DataFrame | None, out: Path, data_end) -> None:
    out.mkdir(parents=True, exist_ok=True)
    daily.to_csv(out / "daily_styles.csv", index=False)
    main = ["风格", "标的", "年化收益", "年化波动", "收益/波动", "最大回撤", "最好一年", "中位一年", "最差一年",
            "持仓时间", "每年单边交易次数"]
    periods = ["风格", "标的", *PERIODS]
    normal = daily[daily["成本"] == "一般"]
    intraday = daily[daily["风格"].str.startswith("D")][["风格", "标的", "成本", "年化收益", "最大回撤", "最好一年", "最差一年"]]
    sections = [
        f"# 交易风格对比（数据截至 {data_end:%Y-%m-%d}，2016 年起）\n\n由 `python -m riskeval.style_compare` 生成，设定见该模块说明。"
        "这是历史回测，不是实时模拟盘。\"16只半导体\"有幸存者偏差，ETF（QQQ、SMH）的结果更可信。",
        "## 主表（一般成本：单边 0.05%）\n\n" + _render(normal[main]),
        "## 不同市况下的收益（一般成本）\n\n" + _render(normal[periods]),
        "## 日内风格对成本有多敏感（理想 / 一般 / 不理想）\n\n" + _render(intraday),
    ]
    if hourly is not None and len(hourly):
        hourly.to_csv(out / "hourly_orb.csv", index=False)
        sections.append("## 小时线开盘区间突破（只有最近约 2 年数据）\n\n"
                        + _render(hourly[["风格", "标的", "成本", "年化收益", "年化波动", "最大回撤", "持仓时间", "每年单边交易次数"]]))
    (out / "README.md").write_text("\n\n".join(sections) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> None:
    from riskeval import daily_data

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", default="reports/style_compare")
    args = parser.parse_args(argv)

    semis = [t for ts in TARGETS.values() for t in ts]
    ohlc = daily_data.download_ohlc(semis + ["QQQ", "SMH"], start="2015-01-01")
    semis = [t for t in semis if t in ohlc["close"].columns]
    daily = run_daily(ohlc, semis)

    hourly_names = ["QQQ", "SMH", "NVDA", "AMD", "MU", "TSM"]
    try:
        hourly = daily_data.download_ohlc(hourly_names, period="730d", interval="1h")
        names = [t for t in hourly_names if t in hourly["close"].columns]
        hourly_table = run_hourly(hourly, ohlc["close"], ohlc["open"], names)
    except Exception as error:  # noqa: BLE001 - 小时线取不到时只跳过这一部分
        print("小时线数据下载失败，跳过：", error)
        hourly_table = None
    write_report(daily, hourly_table, Path(args.out), ohlc["close"].index[-1])
    print(f"已写入 {args.out}/README.md")


if __name__ == "__main__":
    main()
