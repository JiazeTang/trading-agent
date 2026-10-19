"""日线信号：Kova Score 的公开近似、趋势模板、均值回归、板块市况。

输入都是"日期 × 股票"的复权收盘价宽表（或单列 Series）。

Kova Score 的真实算法是付费会员专属、没有公开。作者公开说过它衡量"个股相对全市场的强弱"，
用法是只看 90 分以上、价格 > 10 > 20 > 50 日 EMA、距 52 周高点 10% 以内的股票。
这里用最常见的相对强度排名做法近似它：

    强度 = 0.4×近 63 日涨幅 + 0.2×近 126 日 + 0.2×近 189 日 + 0.2×近 252 日
    分数 = 当天在全市场股票池里的百分位，映射到 1–99

它只是近似，结论只对这个近似成立；要拿真实 Kova Score 校准后才能推到 Kova 本身。
"""

from __future__ import annotations

import numpy as np
import pandas as pd

RS_WEIGHTS = {63: 0.4, 126: 0.2, 189: 0.2, 252: 0.2}
MIN_RANKED = 100  # 当天至少有这么多只股票有完整数据才打分


def _change(closes, days: int):
    return closes / closes.shift(days) - 1


def rs_rating(closes: pd.DataFrame) -> pd.DataFrame:
    """相对强度分数（1–99），按天在所有列之间排名。"""
    strength = sum(weight * _change(closes, days) for days, weight in RS_WEIGHTS.items())
    pct = strength.rank(axis=1, pct=True)
    rating = (pct * 99).clip(lower=1)
    enough = strength.notna().sum(axis=1) >= MIN_RANKED
    return rating.where(enough, axis=0)


def ema(closes, span: int):
    return closes.ewm(span=span, adjust=False).mean()


def trend_aligned(closes):
    """价格 > 10 日 EMA > 20 日 EMA > 50 日 EMA。"""
    e10, e20, e50 = ema(closes, 10), ema(closes, 20), ema(closes, 50)
    return (closes > e10) & (e10 > e20) & (e20 > e50)


def near_52w_high(closes, within: float = 0.10):
    """收盘价距过去 252 个交易日最高收盘价不超过 within。"""
    high = closes.rolling(252, min_periods=252).max()
    return closes >= (1 - within) * high


def zscore(closes, window: int = 20):
    """收盘价相对 window 日均线的标准差倍数；≤ -2 即跌破布林带下轨。"""
    mean = closes.rolling(window, min_periods=window).mean()
    std = closes.rolling(window, min_periods=window).std()
    return (closes - mean) / std


def sma(closes, window: int):
    return closes.rolling(window, min_periods=window).mean()


def sector_regime(index: pd.Series, window: int = 20, efficiency: float = 0.3) -> pd.Series:
    """入场当天就能知道的板块市况（只用过去 window 天的数据）。

    效率比 = |window 日净涨跌| / 每日涨跌绝对值之和。效率比 ≥ efficiency 算趋势，
    再按净涨跌分上行/下行；否则算震荡。
    """
    net = index - index.shift(window)
    path = index.diff().abs().rolling(window, min_periods=window).sum()
    ratio = net.abs() / path
    labels = np.select(
        [ratio >= efficiency, ratio.notna()],
        [np.where(net > 0, "上行趋势", "下行趋势"), "震荡"],
        default="",
    )
    return pd.Series(labels, index=index.index).replace("", np.nan)
