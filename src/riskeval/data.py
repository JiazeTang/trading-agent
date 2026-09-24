"""30 分钟 K 线：从 Alpaca 下载，只保留常规交易时段，缓存到本地，检查数据质量。

价格用 adjustment=all（拆股 + 分红复权）。每次分红都会改写全部历史价格，
所以缓存不做增量追加；要更新就整份重新下载（baseline 的 --refresh）。
"""

from __future__ import annotations

import math
import os
from pathlib import Path

import pandas as pd
import requests

from riskeval.sessions import NY_TZ, nyse_schedule, session_dates

BARS_URL = "https://data.alpaca.markets/v2/stocks/{symbol}/bars"
BAR_MINUTES = 30
PRICE_COLUMNS = ["open", "high", "low", "close"]


def default_end() -> pd.Timestamp:
    """今天美东零点，只取到昨天为止的完整交易日。

    免费账户不能查询最近 15 分钟的 SIP 数据，所以刚过零点时再往前留一点余量。
    """
    now = pd.Timestamp.now(tz=NY_TZ)
    return min(now.normalize(), now - pd.Timedelta(minutes=16))


def fetch_alpaca_bars(symbol: str, start, end, *, http=None) -> pd.DataFrame:
    """下载 [start, end) 的 30 分钟 K 线（含盘前盘后），索引是 K 线开始时间（UTC）。"""
    key = os.environ.get("APCA_API_KEY_ID")
    secret = os.environ.get("APCA_API_SECRET_KEY")
    if not key or not secret:
        raise RuntimeError("缺少 Alpaca 密钥：请设置环境变量 APCA_API_KEY_ID 和 APCA_API_SECRET_KEY")

    http = http or requests.Session()
    headers = {"APCA-API-KEY-ID": key, "APCA-API-SECRET-KEY": secret}
    params = {
        "timeframe": f"{BAR_MINUTES}Min",
        "start": _rfc3339(start),
        "end": _rfc3339(end),
        "adjustment": "all",
        "feed": "sip",
        "limit": 10000,
    }
    rows = []
    while True:
        resp = http.get(BARS_URL.format(symbol=symbol), params=params, headers=headers, timeout=30)
        resp.raise_for_status()
        page = resp.json()
        rows.extend(page.get("bars") or [])
        if not page.get("next_page_token"):
            break
        params["page_token"] = page["next_page_token"]

    bars = pd.DataFrame(rows, columns=["t", "o", "h", "l", "c", "v"])
    bars = bars.rename(columns={"o": "open", "h": "high", "l": "low", "c": "close", "v": "volume"})
    bars.index = pd.DatetimeIndex(pd.to_datetime(bars.pop("t"), utc=True), name="timestamp")
    return bars.sort_index()


def keep_regular_hours(bars: pd.DataFrame, schedule: pd.DataFrame) -> pd.DataFrame:
    """只保留开始时间落在常规交易时段 [开盘, 收盘) 内的 K 线，提前收盘日按日历处理。"""
    day = session_dates(bars.index)
    opens = schedule["open"].reindex(day).array
    closes = schedule["close"].reindex(day).array
    return bars[(bars.index >= opens) & (bars.index < closes)]


def load_bars(symbol: str, start, end, *, cache_dir="data", refresh: bool = False) -> pd.DataFrame:
    """读取缓存的常规时段 30 分钟 K 线；没有缓存或 refresh=True 时从 Alpaca 重新下载。"""
    path = Path(cache_dir) / f"{symbol}_{BAR_MINUTES}min_from_{pd.Timestamp(start):%Y%m%d}.parquet"
    if path.exists() and not refresh:
        return pd.read_parquet(path)

    raw = fetch_alpaca_bars(symbol, start, end)
    raw = raw[~raw.index.duplicated(keep="last")]
    bars = keep_regular_hours(raw, nyse_schedule(start, end))
    if bars.empty:
        raise RuntimeError(f"{symbol} 在 {start} ~ {end} 没有常规时段的 K 线")
    if (bars[PRICE_COLUMNS] <= 0).any().any():
        raise ValueError(f"{symbol} 数据里有非正价格，请检查数据源")

    path.parent.mkdir(parents=True, exist_ok=True)
    bars.to_parquet(path)
    return bars


def check_quality(bars: pd.DataFrame, schedule: pd.DataFrame) -> pd.DataFrame:
    """逐交易日核对 K 线根数（正常 13 根，提前收盘日 7 根），返回根数不对的交易日。"""
    bar_length = pd.Timedelta(minutes=BAR_MINUTES)
    expected = ((schedule["close"] - schedule["open"]) / bar_length).map(math.ceil)
    actual = bars.groupby(session_dates(bars.index)).size().reindex(schedule.index, fill_value=0)
    table = pd.DataFrame({"expected": expected.astype(int), "actual": actual.astype(int)})
    return table[table["actual"] != table["expected"]]


def _rfc3339(value) -> str:
    ts = pd.Timestamp(value)
    ts = ts.tz_localize("UTC") if ts.tz is None else ts.tz_convert("UTC")
    return ts.strftime("%Y-%m-%dT%H:%M:%SZ")
