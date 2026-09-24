"""交易日历：美东时区、NYSE 交易日及每天的开收盘时间（含提前收盘日）。"""

from __future__ import annotations

import exchange_calendars as xcals
import pandas as pd

NY_TZ = "America/New_York"


def nyse_schedule(start, end) -> pd.DataFrame:
    """[start, end] 内每个交易日的开盘、收盘时间（UTC）。索引是交易日日期（无时区）。"""
    calendar = xcals.get_calendar("XNYS", start="2000-01-01")
    return calendar.schedule.loc[_as_date(start):_as_date(end), ["open", "close"]]


def session_dates(index: pd.DatetimeIndex) -> pd.DatetimeIndex:
    """把 UTC 时间戳映射到所属交易日（美东日期，无时区）。"""
    return index.tz_convert(NY_TZ).tz_localize(None).normalize()


def _as_date(value) -> pd.Timestamp:
    ts = pd.Timestamp(value)
    if ts.tz is not None:
        ts = ts.tz_convert(NY_TZ).tz_localize(None)
    return ts.normalize()
