"""逐日入场的持有期统计：每个交易日都假设按信号买入，持有固定交易日数后卖出。

信号用第 t 天收盘价算出，第 t+1 天收盘买入（不偷看当天收盘），第 t+1+h 天收盘卖出。
持有期不完整（离现在不足 h 天）的入场日记为 NaN，另给出"持有至最新收盘"的浮动盈亏。
"""

from __future__ import annotations

import numpy as np
import pandas as pd

HORIZONS = {"1个月": 21, "2个月": 42, "3个月": 63}
TRADING_DAYS = 252


def _future_window(series: pd.Series, h: int, how: str) -> pd.Series:
    """第 t+2 … t+1+h 天的滚动统计，对齐到第 t 天。"""
    rolled = getattr(series[::-1].rolling(h, min_periods=h), how)()[::-1]
    return rolled.shift(-2)


def forward_stats(close: pd.Series, h: int) -> pd.DataFrame:
    """单只股票每个入场日的：持有收益、持有期年化波动、持有期最大浮亏、持有至最新的收益。"""
    entry = close.shift(-1)
    exit_ = close.shift(-(h + 1))
    daily = close.pct_change(fill_method=None)
    lowest = _future_window(close, h, "min")
    return pd.DataFrame({
        "ret": exit_ / entry - 1,
        "vol": _future_window(daily, h, "std") * np.sqrt(TRADING_DAYS),
        "mae": (lowest / entry - 1).clip(upper=0),
        "ret_to_date": close.dropna().iloc[-1] / entry - 1,
    })


def panel(closes: pd.DataFrame, benchmark: pd.Series, horizons: dict[str, int] = HORIZONS) -> pd.DataFrame:
    """所有股票、所有入场日、所有持有期的长表，含相对基准（如 SMH）的超额收益。"""
    frames = []
    for label, h in horizons.items():
        bench = forward_stats(benchmark, h)
        for ticker in closes.columns:
            stats = forward_stats(closes[ticker], h)
            stats["excess"] = stats["ret"] - bench["ret"]
            stats["ticker"] = ticker
            stats["horizon"] = label
            frames.append(stats.rename_axis("date").reset_index())
    return pd.concat(frames, ignore_index=True)


def summarize(rows: pd.DataFrame) -> dict[str, float]:
    """一组入场日的胜负统计。只统计持有期完整的入场日。"""
    done = rows.dropna(subset=["ret"])
    ret = done["ret"]
    wins, losses = ret[ret > 0], ret[ret <= 0]
    per_stock = done.groupby("ticker")["ret"].mean()
    return {
        "入场次数": len(done),
        "股票数": done["ticker"].nunique(),
        "赚钱次数": len(wins),
        "赔钱次数": len(losses),
        "胜率": len(wins) / len(done) if len(done) else np.nan,
        "平均赚": wins.mean(),
        "平均赔": losses.mean(),
        "平均收益": ret.mean(),
        "中位收益": ret.median(),
        "平均超额(对SMH)": done["excess"].mean(),
        "跑赢SMH比例": (done["excess"] > 0).mean() if len(done) else np.nan,
        "持有期年化波动": done["vol"].mean(),
        "平均最大浮亏": done["mae"].mean(),
        "最差最大浮亏": done["mae"].min(),
        "收益为正的股票数": int((per_stock > 0).sum()),
        "收益为负的股票数": int((per_stock <= 0).sum()),
    }

