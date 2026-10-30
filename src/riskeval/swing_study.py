"""波段交易研究：在规则 A（跌破布林下轨的超跌）基础上，比较入场时机、出场时机、止损形式和要承担的波动。

    python -m riskeval.swing_study --out reports/swing_study

以下设定在看结果之前写死。

数据：16 只半导体（主样本，按今天的市值挑选，有幸存者偏差）和 S&P 500 现有成分股（稳健性检查，只做前两部分）。
2016 年起；按收盘价判断、按收盘价成交；第二、三部分每次买卖各扣 0.05% 成本。
σ 指信号当天往前 20 个交易日日收益的标准差（例如 3%），入场时定下，持有期间不变。

第一部分　入场时机（事件研究，不扣成本）
- E1 现行：收盘 z ≤ -2（跌破 20 日布林下轨）且在 200 日线上方。
- E2 确认后再买：前 5 个交易日内出现过 E1，今天收盘收回下轨（z > -2）、比昨天收涨，且仍在 200 日线上方。
- E3 更深超跌：z ≤ -2.5 且在 200 日线上方。
- E4 板块普跌：E1，且当天至少一半股票同时跌破下轨（规则 B；只在半导体上算）。
- 对照：收盘在 200 日线上方的任意一天（每 5 个交易日取一次），看"什么都不挑"能赚多少。
- 信号每段只取第一天（前 5 个交易日没有同类信号），下一个交易日收盘买入。统计买入后第 1、3、5、10、20、42
  个交易日的累计收益（平均、上涨比例），42 天内的平均最大浮盈和最大浮亏，收盘最高点和最低点出现在第几天（中位数），
  以及 20 天收益按 2023 年前后分开的平均值。

第二部分　出场和止损（逐笔；入场固定为 E1，下一个交易日收盘买入；同一只股票的交易不重叠）
- 出场：X1 回到中轨：收盘 z ≥ 0 就卖（现行）。X2 到上轨：收盘 z ≥ +2 才卖。
  X3 中轨后跟踪：先等收盘回到中轨，之后第一次收盘跌回中轨下方才卖。X4 固定持有 20 个交易日。
  都最长持有 42 个交易日。
- 止损（每种出场各配一遍；同一天先判断止损）：S0 不止损；S1 固定 -10%；S2 固定 -20%（现行）；
  S3 波动止损：比买入价跌超过 3σ；S4 移动止损：比持有以来的最高收盘（含买入价）低超过 3σ；
  S5 时间止损：持有满 10 个交易日仍低于买入价；S6 趋势止损：收盘跌破 200 日线。
- 统计：笔数、胜率、平均收益、中位收益、收益标准差、最差 5% 的平均、最差一笔、平均持有天数、
  平均每天收益（总收益 ÷ 总持有天数）、平均最大浮亏、止损触发比例，以及 2023 年前后的平均收益。

第三部分　账户层面（只在半导体上做，对应实际的加码仓：1600，分 2 个仓位）
- 第二部分的 28 个组合各模拟一遍：有空位时从前一天有 E1 信号的股票里选 z 值最低的，按当天收盘买入；
  每个仓位 = 加码仓当前净值 ÷ 2；空仓的钱不计利息。
- 另加"波动率定仓"：每种出场配 S0，仓位再乘 min(1, 30% ÷ 入场前 20 日年化波动)（年化波动最低按 10% 算）。
- 对照：1600 全部买入 SMH 一直持有。
- 统计：年化收益、年化波动、持仓日的年化波动（只算有持仓的日子）、Sharpe（年化平均日收益 ÷ 年化波动）、
  最大回撤、最差一天、持仓时间占比、每年交易笔数；对 16 只等权日收益做回归得到的 beta 和年化超额收益（alpha）；
  以及 2016–2022 和 2023 年后各自的 Sharpe、年化波动、最大回撤、超额收益。
- 为什么要看超额收益：市场整体上涨时，持仓时间越长，Sharpe 自然越高，哪怕择时毫无本事
  （用随机游走的合成数据试跑时就出现过）。超额收益扣掉了"跟着市场涨"的部分，才是入场和出场本身的贡献。

判断标准（看结果之前写死）：
- 某种止损或定仓"能降波动"：账户年化波动在两段都比同一出场的 S0 低，全期最大回撤更浅，而且 Sharpe 不低于 S0 的 90%。
- 换掉现行（E1 + X1 + S2）的条件：账户的超额收益和 Sharpe 在 2016–2022 和 2023 年后两段都高于现行，
  全期最大回撤不比现行深，S&P 500 上同一组合的平均每天收益不低于现行，
  而且改进不是运气：把备选方案的日收益缩放到和现行同样的波动后减去现行的日收益，
  这条差值序列的紧缩夏普比 DSR（按 31 个备选方案计）≥ 95%。只满足一部分就不换。
  （用随机游走的合成数据试跑时，没有这最后一条，31 个备选里总有一两个"两段都更好"。）
- 这次共 4 种入场、28 + 4 个账户组合，计入项目累计试过的版本数（DSR 用）。
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from riskeval import signals
from riskeval.mr_screen import SELLOFF_SHARE, TARGETS
from riskeval.strategy_health import dsr

START = pd.Timestamp("2016-01-01")
SPLIT = pd.Timestamp("2023-01-01")
COST = 0.0005
MAX_HOLD = 42
HORIZONS = [1, 3, 5, 10, 20, 42]
EPISODE_GAP = 5
CONTROL_EVERY = 5
CAPITAL, SLOTS = 1600.0, 2
TARGET_VOL, VOL_FLOOR = 0.30, 0.10
CORE = "SMH"

ENTRIES = ["E1 现行：跌破下轨", "E2 确认后再买", "E3 更深超跌 z≤-2.5", "E4 板块普跌", "对照：200日线上方任意一天"]
EXITS = {"X1 回到中轨": "mean", "X2 到上轨": "upper", "X3 中轨后跟踪": "trail_mean", "X4 持有20天": "hold20"}
STOPS = {
    "S0 不止损": None,
    "S1 固定-10%": ("fixed", 0.10),
    "S2 固定-20%": ("fixed", 0.20),
    "S3 波动3σ": ("sigma", 3.0),
    "S4 移动3σ": ("trail", 3.0),
    "S5 时间10天": ("time", 10),
    "S6 跌破200日线": ("trend", None),
}
CURRENT = ("X1 回到中轨", "S2 固定-20%")


# ---------- 信号 ----------

def indicators(px: pd.DataFrame) -> dict[str, pd.DataFrame]:
    z = signals.zscore(px)
    ma = signals.sma(px, 200)
    sigma = px.pct_change(fill_method=None).rolling(20).std()
    return {"z": z, "ma": ma, "sigma": sigma}


def entry_flags(px: pd.DataFrame, ind: dict, sector: bool) -> dict[str, pd.DataFrame]:
    z, above = ind["z"], px > ind["ma"]
    e1 = ((z <= -2) & above).fillna(False)
    recent = e1.astype(float).shift(1).rolling(EPISODE_GAP, min_periods=1).max().fillna(0) > 0
    e2 = (recent & (z > -2) & (px > px.shift(1)) & above).fillna(False)
    e3 = ((z <= -2.5) & above).fillna(False)
    flags = {ENTRIES[0]: e1, ENTRIES[1]: e2, ENTRIES[2]: e3}
    if sector:
        breadth = (z <= -2).sum(axis=1) / z.notna().sum(axis=1).replace(0, np.nan)
        flags[ENTRIES[3]] = e1.apply(lambda c: c & (breadth >= SELLOFF_SHARE)).fillna(False)
    control = above.fillna(False)
    every = pd.Series(np.arange(len(px)) % CONTROL_EVERY == 0, index=px.index)
    flags[ENTRIES[4]] = control.apply(lambda c: c & every)
    return flags


def first_of_episode(flags: pd.DataFrame) -> pd.DataFrame:
    """前 EPISODE_GAP 个交易日没有同类信号的信号日。"""
    earlier = flags.astype(float).shift(1).rolling(EPISODE_GAP, min_periods=1).max().fillna(0) > 0
    return flags & ~earlier


# ---------- 第一部分：事件研究 ----------

def forward_paths(px: pd.DataFrame, flags: pd.DataFrame, start=START) -> tuple[np.ndarray, np.ndarray]:
    """每个信号：下一个交易日收盘买入后，第 1..MAX_HOLD 天的累计收益（行 = 信号）和信号日期。"""
    paths, dates = [], []
    for t in px.columns:
        values = px[t].to_numpy()
        idx = np.flatnonzero(flags[t].to_numpy() & (px.index >= start))
        idx = idx[idx + 1 + MAX_HOLD < len(values)]
        if not len(idx):
            continue
        entry = values[idx + 1]
        path = np.stack([values[idx + 1 + k] for k in range(1, MAX_HOLD + 1)], axis=1) / entry[:, None] - 1
        keep = np.isfinite(entry) & np.isfinite(path).all(axis=1)
        paths.append(path[keep])
        dates.append(px.index[idx[keep]])
    if not paths:
        return np.empty((0, MAX_HOLD)), np.array([], dtype="datetime64[ns]")
    return np.vstack(paths), np.concatenate([np.asarray(d) for d in dates])


def event_table(px: pd.DataFrame, flags: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for name, flag in flags.items():
        use = flag if name == ENTRIES[4] else first_of_episode(flag)
        paths, dates = forward_paths(px, use)
        if not len(paths):
            continue
        row = {"入场": name, "段数": float(len(paths))}
        for h in HORIZONS:
            row[f"{h}天平均"] = paths[:, h - 1].mean()
        for h in HORIZONS:
            row[f"{h}天上涨比例"] = (paths[:, h - 1] > 0).mean()
        early = dates < np.datetime64(SPLIT)
        row |= {
            "42天内平均最大浮盈": np.maximum(paths.max(axis=1), 0).mean(),
            "42天内平均最大浮亏": np.minimum(paths.min(axis=1), 0).mean(),
            "最高点在第几天(中位)": float(np.median(paths.argmax(axis=1) + 1)),
            "最低点在第几天(中位)": float(np.median(paths.argmin(axis=1) + 1)),
            "20天平均·2016-22": paths[early, 19].mean() if early.any() else np.nan,
            "20天平均·2023后": paths[~early, 19].mean() if (~early).any() else np.nan,
        }
        rows.append(row)
    return pd.DataFrame(rows)


# ---------- 第二部分：出场和止损 ----------

def exit_reason(pos: dict, price: float, z: float, ma: float, exit_rule: str, stop) -> str | None:
    """pos 里的 held（已持有天数）和 peak（含今天的最高收盘）由调用方先更新。返回卖出原因或 None。"""
    change = price / pos["entry"] - 1
    if stop is not None:
        kind, k = stop
        if ((kind == "fixed" and change <= -k) or
                (kind == "sigma" and change <= -k * pos["sigma"]) or
                (kind == "trail" and price <= pos["peak"] * (1 - k * pos["sigma"])) or
                (kind == "time" and pos["held"] >= k and change < 0) or
                (kind == "trend" and price < ma)):
            return "止损"
    if exit_rule == "mean" and z >= 0:
        return "出场"
    if exit_rule == "upper" and z >= 2:
        return "出场"
    if exit_rule == "trail_mean":
        if pos["armed"] and z < 0:
            return "出场"
        if z >= 0:
            pos["armed"] = True
    if exit_rule == "hold20" and pos["held"] >= 20:
        return "出场"
    if pos["held"] >= MAX_HOLD:
        return "到期"
    return None


def new_position(entry: float, sigma: float, day) -> dict:
    return {"entry": entry, "sigma": sigma, "held": 0, "peak": entry, "armed": False, "date": day, "mae": 0.0}


def step(pos: dict, price: float) -> None:
    pos["held"] += 1
    pos["peak"] = max(pos["peak"], price)
    pos["mae"] = min(pos["mae"], price / pos["entry"] - 1)


def net(gross: float) -> float:
    return (1 + gross) * (1 - COST) ** 2 - 1


def stock_trades(close: np.ndarray, z: np.ndarray, ma: np.ndarray, sigma: np.ndarray, flags: np.ndarray,
                 dates: pd.DatetimeIndex, exit_rule: str, stop, start=START) -> list[dict]:
    out, n = [], len(close)
    signal_days = np.flatnonzero(flags & (dates >= start))
    t = signal_days[0] if len(signal_days) else n
    while t < n - 1:
        i = t + 1
        if not (np.isfinite(close[i]) and np.isfinite(sigma[t])):
            t = _next(signal_days, t + 1, n)
            continue
        pos, reason = new_position(close[i], sigma[t], dates[t]), None
        for j in range(i + 1, min(n, i + MAX_HOLD + 1)):
            if not np.isfinite(close[j]):
                continue
            step(pos, close[j])
            reason = exit_reason(pos, close[j], z[j], ma[j], exit_rule, stop)
            if reason:
                break
        if reason is None:
            break  # 数据结束时还没卖出，不计入
        out.append({"date": dates[t], "ret": net(close[j] / pos["entry"] - 1), "days": pos["held"],
                    "mae": pos["mae"], "reason": reason})
        t = _next(signal_days, j, n)
    return out


def _next(signal_days: np.ndarray, frm: int, n: int) -> int:
    k = signal_days.searchsorted(frm)
    return signal_days[k] if k < len(signal_days) else n


def all_trades(px: pd.DataFrame, ind: dict, flag: pd.DataFrame, exit_rule: str, stop) -> pd.DataFrame:
    rows = []
    for t in px.columns:
        rows += stock_trades(px[t].to_numpy(), ind["z"][t].to_numpy(), ind["ma"][t].to_numpy(),
                             ind["sigma"][t].to_numpy(), flag[t].to_numpy(), px.index, exit_rule, stop)
    return pd.DataFrame(rows, columns=["date", "ret", "days", "mae", "reason"])


def trade_stats(tr: pd.DataFrame) -> dict:
    if not len(tr):
        return {"笔数": 0.0}
    r = tr["ret"]
    early = tr["date"] < SPLIT
    return {
        "笔数": float(len(tr)), "胜率": (r > 0).mean(), "平均收益": r.mean(), "中位收益": r.median(),
        "收益标准差": r.std(), "最差5%平均": r[r <= r.quantile(0.05)].mean(), "最差一笔": r.min(),
        "平均持有天数": tr["days"].mean(), "平均每天收益": r.sum() / tr["days"].sum(),
        "平均最大浮亏": tr["mae"].mean(), "止损比例": (tr["reason"] == "止损").mean(),
        "平均收益·2016-22": r[early].mean() if early.any() else np.nan,
        "平均收益·2023后": r[~early].mean() if (~early).any() else np.nan,
    }


def trade_grid(px: pd.DataFrame, ind: dict, e1: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for exit_name, exit_rule in EXITS.items():
        for stop_name, stop in STOPS.items():
            rows.append({"出场": exit_name, "止损": stop_name} | trade_stats(all_trades(px, ind, e1, exit_rule, stop)))
    return pd.DataFrame(rows)


# ---------- 第三部分：账户 ----------

def simulate(px: pd.DataFrame, ind: dict, e1: pd.DataFrame, exit_rule: str, stop, sizing: str = "equal",
             start=START, capital: float = CAPITAL, slots: int = SLOTS) -> tuple[pd.Series, pd.Series, pd.DataFrame]:
    """返回（每日净值, 每日持仓占净值比例, 交易记录）。前一天收盘出信号，当天收盘买入。"""
    close, z, ma, sigma = (a[px.columns].to_numpy() for a in (px, ind["z"], ind["ma"], ind["sigma"]))
    flags = e1[px.columns].to_numpy()
    tickers, dates = list(px.columns), px.index
    first = dates.searchsorted(start)
    cash, open_, pending = capital, {}, []
    equity, exposure, log = np.full(len(dates), np.nan), np.full(len(dates), np.nan), []
    last = close[first].copy()

    for d in range(first, len(dates)):
        price = np.where(np.isfinite(close[d]), close[d], last)
        last = price
        sold = set()
        for k in list(open_):
            pos = open_[k]
            if not np.isfinite(close[d, k]):
                continue
            step(pos, price[k])
            reason = exit_reason(pos, price[k], z[d, k], ma[d, k], exit_rule, stop)
            if reason:
                cash += pos["shares"] * price[k] * (1 - COST)
                log.append({"股票": tickers[k], "买入日": pos["date"].date(), "卖出日": dates[d].date(),
                            "收益": net(price[k] / pos["entry"] - 1), "持有天数": pos["held"], "原因": reason})
                del open_[k]
                sold.add(k)
        stocks = sum(p["shares"] * price[k] for k, p in open_.items())
        for k, sig in pending:
            if len(open_) >= slots or k in open_ or k in sold or not np.isfinite(close[d, k]):
                continue
            size = (cash + stocks) / slots
            if sizing == "vol":
                size *= min(1.0, TARGET_VOL / max(sig * np.sqrt(252), VOL_FLOOR))
            size = min(size, cash)
            if size < 1:
                continue
            pos = new_position(price[k], sig, dates[d])
            pos["shares"] = size * (1 - COST) / price[k]
            open_[k] = pos
            cash -= size
            stocks += pos["shares"] * price[k]
        today = np.flatnonzero(flags[d] & np.isfinite(sigma[d]))
        pending = [(k, sigma[d, k]) for k in today[np.argsort(z[d, today])]]
        equity[d] = cash + stocks
        exposure[d] = stocks / equity[d]
    index = dates[first:]
    return pd.Series(equity[first:], index=index), pd.Series(exposure[first:], index=index), pd.DataFrame(log)


def _alpha_beta(daily: pd.Series, bench: pd.Series) -> tuple[float, float]:
    both = pd.concat([daily.rename("y"), bench.rename("x")], axis=1, sort=True).dropna()
    if len(both) < 20 or both.iloc[:, 1].var() == 0:
        return np.nan, np.nan
    beta = both.iloc[:, 0].cov(both.iloc[:, 1]) / both.iloc[:, 1].var()
    return (both.iloc[:, 0].mean() - beta * both.iloc[:, 1].mean()) * 252, beta


def account_stats(equity: pd.Series, exposure: pd.Series | None = None, trades: int | None = None,
                  bench: pd.Series | None = None) -> dict:
    daily = equity.pct_change().dropna()
    years = len(daily) / 252
    vol = daily.std() * np.sqrt(252)
    out = {"年化收益": (equity.iloc[-1] / equity.iloc[0]) ** (1 / years) - 1, "年化波动": vol}
    if exposure is not None:
        held = exposure.shift(1).reindex(daily.index) > 0
        out["持仓日年化波动"] = daily[held].std() * np.sqrt(252) if held.sum() > 1 else np.nan
    out |= {"Sharpe": daily.mean() * 252 / vol if vol else np.nan,
            "最大回撤": (equity / equity.cummax() - 1).min(), "最差一天": daily.min()}
    if exposure is not None:
        out["持仓时间占比"] = (exposure > 0).mean()
        out["每年交易笔数"] = trades / years
    if bench is not None:
        out["超额收益"], out["beta"] = _alpha_beta(daily, bench)
    for label, part in {"2016-22": equity[equity.index < SPLIT], "2023后": equity[equity.index >= SPLIT]}.items():
        d = part.pct_change().dropna()
        sd = d.std() * np.sqrt(252) if len(d) > 1 else np.nan
        out[f"Sharpe·{label}"] = d.mean() * 252 / sd if sd else np.nan
        out[f"年化波动·{label}"] = sd
        out[f"最大回撤·{label}"] = (part / part.cummax() - 1).min()
        if bench is not None:
            out[f"超额收益·{label}"] = _alpha_beta(d, bench)[0]
    return out


def account_grid(px: pd.DataFrame, ind: dict, e1: pd.DataFrame,
                 core: pd.Series | None) -> tuple[pd.DataFrame, dict[tuple[str, str], pd.Series]]:
    bench = px.pct_change(fill_method=None).mean(axis=1)
    rows, curves = [], {}
    for exit_name, exit_rule in EXITS.items():
        for stop_name, stop in [*STOPS.items(), ("S0 + 波动率定仓", None)]:
            sizing = "vol" if stop_name.endswith("定仓") else "equal"
            eq, expo, log = simulate(px, ind, e1, exit_rule, stop, sizing=sizing)
            rows.append({"出场": exit_name, "止损": stop_name} | account_stats(eq, expo, len(log), bench))
            curves[(exit_name, stop_name)] = eq
    if core is not None:
        hold = core[core.index >= START].dropna()
        rows.append({"出场": "对照：1600 全买 SMH", "止损": "—"} | account_stats(CAPITAL * hold / hold.iloc[0], bench=bench))
    return pd.DataFrame(rows), curves


def improvement_dsr(alt: pd.Series, cur: pd.Series, trials: int) -> float:
    """备选缩放到和现行同样的波动后，减去现行的日收益；这条差值序列的 DSR。"""
    a, c = alt.pct_change().dropna(), cur.pct_change().dropna()
    diff = a * (c.std() / a.std()) - c
    return dsr(diff, trials)[0] if diff.std() > 0 else np.nan


# ---------- 判断 ----------

def verdicts(account: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for exit_name in EXITS:
        part = account[account["出场"] == exit_name].set_index("止损")
        base = part.loc["S0 不止损"]
        for stop_name, r in part.iterrows():
            if stop_name == "S0 不止损":
                continue
            lower = (r["年化波动·2016-22"] < base["年化波动·2016-22"] and r["年化波动·2023后"] < base["年化波动·2023后"]
                     and r["最大回撤"] > base["最大回撤"])
            keeps = r["Sharpe"] >= 0.9 * base["Sharpe"]
            rows.append({"出场": exit_name, "止损或定仓": stop_name,
                         "波动变化": r["年化波动"] - base["年化波动"], "最大回撤变化": r["最大回撤"] - base["最大回撤"],
                         "Sharpe变化": r["Sharpe"] - base["Sharpe"],
                         "能降波动": "是" if lower and keeps else ("降了波动但 Sharpe 损失超过一成" if lower else "否")})
    return pd.DataFrame(rows)


def replacement(account: pd.DataFrame, curves: dict, grid_sp500: pd.DataFrame | None) -> pd.DataFrame:
    """列出在半导体两段都更好、回撤不更深的备选，再看 S&P 500 和"改进是不是运气"。"""
    acc = account.set_index(["出场", "止损"])
    cur = acc.loc[CURRENT]
    sp = grid_sp500.set_index(["出场", "止损"]) if grid_sp500 is not None else None
    trials = len(curves) - 1
    rows = []
    for key, r in acc.iterrows():
        if key not in curves or key == CURRENT:
            continue
        both = all(r[f"{m}·{h}"] > cur[f"{m}·{h}"] for m in ["Sharpe", "超额收益"] for h in ["2016-22", "2023后"])
        if not (both and r["最大回撤"] >= cur["最大回撤"]):
            continue
        sp_ok = (sp.loc[key, "平均每天收益"] >= sp.loc[CURRENT, "平均每天收益"]) if sp is not None and key in sp.index else None
        luck = improvement_dsr(curves[key], curves[CURRENT], trials)
        ok = bool(sp_ok) and luck >= 0.95
        rows.append({"出场": key[0], "止损": key[1], "两段Sharpe和超额都更高": "是", "回撤不更深": "是",
                     "S&P 500 每天收益不更低": {True: "是", False: "否", None: "无对应组合"}[sp_ok],
                     "改进不是运气的把握(DSR)": luck, "结论": "满足全部条件，可以考虑替换" if ok else "不满足全部条件"})
    if not rows:
        rows.append({"出场": "—", "止损": "—", "两段Sharpe和超额都更高": "—", "回撤不更深": "—",
                     "S&P 500 每天收益不更低": "—", "改进不是运气的把握(DSR)": np.nan,
                     "结论": "没有组合在两段 Sharpe 和超额收益都更高且回撤不更深，维持现行"})
    return pd.DataFrame(rows)


# ---------- 汇总 ----------

def run(closes: pd.DataFrame, sp500: pd.DataFrame | None) -> dict[str, pd.DataFrame]:
    closes = closes.dropna(how="all")
    semis = [t for ts in TARGETS.values() for t in ts if t in closes.columns]
    px = closes[semis]
    ind = indicators(px)
    flags = entry_flags(px, ind, sector=True)
    e1 = flags[ENTRIES[0]]
    results = {"events": event_table(px, flags), "grid": trade_grid(px, ind, e1)}
    results["account"], curves = account_grid(px, ind, e1, closes[CORE] if CORE in closes.columns else None)
    if sp500 is not None:
        sp = sp500.dropna(how="all")
        sp_ind = indicators(sp)
        sp_flags = entry_flags(sp, sp_ind, sector=False)
        results["events_sp500"] = event_table(sp, sp_flags)
        results["grid_sp500"] = trade_grid(sp, sp_ind, sp_flags[ENTRIES[0]])
    results["verdicts"] = verdicts(results["account"])
    results["replacement"] = replacement(results["account"], curves, results.get("grid_sp500"))
    return results


NOT_PERCENT = {"平均持有天数", "最高点在第几天(中位)", "最低点在第几天(中位)", "每年交易笔数",
               "Sharpe", "Sharpe·2016-22", "Sharpe·2023后", "Sharpe变化", "beta"}
FINE_PERCENT = {"平均每天收益"} | {f"{h}天平均" for h in HORIZONS}


def _render(table: pd.DataFrame) -> str:
    table = table.copy()
    for column in table.columns:
        if table[column].dtype.kind == "f":
            fmt = ((lambda x: f"{x:.0f}") if column in {"段数", "笔数"} else
                   (lambda x: f"{x:.2f}") if column in NOT_PERCENT else
                   (lambda x: f"{x:.2%}") if column in FINE_PERCENT else (lambda x: f"{x:.1%}"))
            table[column] = table[column].map(lambda x, f=fmt: "" if pd.isna(x) else f(x))
    header = "| " + " | ".join(map(str, table.columns)) + " |"
    body = ["| " + " | ".join(map(str, row)) + " |" for row in table.itertuples(index=False)]
    return "\n".join([header, "|" + "---|" * len(table.columns), *body]) if len(table) else "（无）"


def _event_sections(events: pd.DataFrame, title: str) -> list[str]:
    avg = ["入场", "段数"] + [f"{h}天平均" for h in HORIZONS]
    up = ["入场"] + [f"{h}天上涨比例" for h in HORIZONS]
    shape = ["入场", "42天内平均最大浮盈", "42天内平均最大浮亏", "最高点在第几天(中位)", "最低点在第几天(中位)",
             "20天平均·2016-22", "20天平均·2023后"]
    return [f"## 一、入场时机：{title}\n\n买入后第 N 个交易日的平均累计收益（不扣成本）\n\n" + _render(events[avg]),
            "上涨比例\n\n" + _render(events[up]),
            "42 天内的波动形状\n\n" + _render(events[shape])]


def write_report(results: dict, out: Path, data_end) -> None:
    out.mkdir(parents=True, exist_ok=True)
    for name, table in results.items():
        table.to_csv(out / f"{name}.csv", index=False)
    grid_cols = ["出场", "止损", "笔数", "胜率", "平均收益", "中位收益", "收益标准差", "最差5%平均", "最差一笔",
                 "平均持有天数", "平均每天收益", "平均最大浮亏", "止损比例", "平均收益·2016-22", "平均收益·2023后"]
    acc_cols = ["出场", "止损", "年化收益", "年化波动", "持仓日年化波动", "Sharpe", "最大回撤", "最差一天",
                "持仓时间占比", "每年交易笔数", "超额收益", "beta"]
    split_cols = ["出场", "止损"] + [f"{m}·{h}" for h in ["2016-22", "2023后"]
                                   for m in ["Sharpe", "超额收益", "年化波动", "最大回撤"]]
    sections = [
        f"# 波段交易研究（数据截至 {data_end:%Y-%m-%d}）\n\n由 `python -m riskeval.swing_study` 生成，设定和判断标准见该模块说明。"
        "规则输出加历史回测，不是投资建议。16 只半导体按今天的市值挑选，有幸存者偏差，主要看各方案之间的相对差别，"
        "并用 S&P 500 核对方向。",
        *_event_sections(results["events"], "16 只半导体"),
    ]
    if "events_sp500" in results:
        sections += _event_sections(results["events_sp500"], "S&P 500")
    sections.append("## 二、出场和止损：逐笔（16 只半导体，已扣成本）\n\n" + _render(results["grid"][grid_cols]))
    if "grid_sp500" in results:
        sections.append("## 二、出场和止损：逐笔（S&P 500，已扣成本）\n\n" + _render(results["grid_sp500"][grid_cols]))
    sections += [
        "## 三、账户层面：加码仓 1600、2 个仓位（16 只半导体，已扣成本）\n\n"
        "超额收益和 beta：对 16 只等权的日收益做回归。beta 是跟着板块涨跌的程度，超额收益是扣掉这部分之后剩下的年化收益。\n\n"
        + _render(results["account"][acc_cols]),
        "分段：2016–2022 与 2023 年以后\n\n" + _render(results["account"][split_cols]),
        "## 四、按事先写定的标准判断\n\n止损或定仓能不能降波动（和同一出场的 S0 不止损比）\n\n" + _render(results["verdicts"]),
        "要不要换掉现行（E1 + 回到中轨 + 固定 -20%）\n\n" + _render(results["replacement"]),
    ]
    (out / "README.md").write_text("\n\n".join(sections) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> None:
    from riskeval import daily_data

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--start", default="2015-01-01")
    parser.add_argument("--out", default="reports/swing_study")
    parser.add_argument("--skip-sp500", action="store_true")
    args = parser.parse_args(argv)

    semis = [t for ts in TARGETS.values() for t in ts]
    closes = daily_data.download_closes(semis + [CORE], args.start, chunk=50)
    sp500 = None if args.skip_sp500 else daily_data.download_closes(daily_data.sp500_tickers(), args.start)
    results = run(closes, sp500)
    write_report(results, Path(args.out), closes.index[-1])
    print(f"已写入 {args.out}/README.md")


if __name__ == "__main__":
    main()
