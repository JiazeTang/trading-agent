"""测试用的合成 K 线：时间戳来自真实 NYSE 日历，价格按指定的季度收益平滑变化。"""

from __future__ import annotations

import pandas as pd

from riskeval.sessions import nyse_schedule, session_dates


def bar_times(start, end) -> pd.DatetimeIndex:
    """[start, end] 内所有常规时段 30 分钟 K 线的开始时间（UTC）。"""
    schedule = nyse_schedule(start, end)
    stamps = [pd.date_range(o, c, freq="30min", inclusive="left") for o, c in zip(schedule["open"], schedule["close"])]
    return pd.DatetimeIndex(pd.concat([s.to_series() for s in stamps]).index, name="timestamp")


def make_bars(start, end, quarter_returns: dict[str, float], first_open: float = 100.0) -> pd.DataFrame:
    """每个季度内每根 K 线按相同比例涨跌，使季度收益恰好等于 quarter_returns 里的值。"""
    index = bar_times(start, end)
    quarter = session_dates(index).to_period("Q")
    counts = pd.Series(quarter).value_counts()
    growth = [(1 + quarter_returns[str(q)]) ** (1 / counts[q]) for q in quarter]
    close = first_open * pd.Series(growth, index=index).cumprod()
    open_ = close.shift(1).fillna(first_open)
    return pd.DataFrame({
        "open": open_,
        "high": pd.concat([open_, close], axis=1).max(axis=1),
        "low": pd.concat([open_, close], axis=1).min(axis=1),
        "close": close,
        "volume": 1000.0,
    })
