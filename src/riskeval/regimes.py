"""按季度划分市况，并事先固定开发集 / 留出集。

下面的规则在看到任何策略结果之前定下，之后不再修改：

- 季度收益 > +8% 记为 up（上涨），< -8% 记为 down（下跌），其余记为 sideways（震荡）。
- 只有交易日齐全的季度参与评估；不完整的季度（比如还没结束的当前季度）记为 excluded。
- 每类市况内部按时间先后交替分配：第 1、3、5… 个季度进 dev（开发集），
  第 2、4、6… 个进 holdout（留出集）。新季度只会追加在后面，已有季度的分配不会变。

标签用的是整个季度的涨跌，要等季度结束才知道。所以它只能用来给结果分组，
绝不能作为策略的输入。
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from riskeval.sessions import session_dates

THRESHOLD = 0.08
REGIMES = ["up", "sideways", "down"]
SPLITS = ["dev", "holdout"]


def label_quarters(bars: pd.DataFrame, calendar_sessions: pd.DatetimeIndex,
                   threshold: float = THRESHOLD) -> pd.DataFrame:
    """每个季度一行：起止交易日、交易日数、是否完整、季度收益、市况标签、所属数据集。

    calendar_sessions 是交易所日历里的全部交易日，要覆盖数据涉及的每个完整季度，
    用来判断季度内的交易日是否齐全。
    """
    days = pd.Series(session_dates(bars.index), index=bars.index)
    quarter = days.dt.to_period("Q")

    closes = bars["close"].groupby(quarter).last()
    base = closes.shift(1)
    base.iloc[0] = bars["open"].iloc[0]
    returns = closes / base - 1

    seen = days.groupby(quarter).nunique()
    expected = calendar_sessions.to_series().groupby(calendar_sessions.to_period("Q")).size()

    table = pd.DataFrame({
        "start": days.groupby(quarter).min(),
        "end": days.groupby(quarter).max(),
        "sessions": seen,
        "complete": seen == expected.reindex(seen.index),
        "return": returns,
    })
    table["regime"] = np.select([returns > threshold, returns < -threshold], ["up", "down"], "sideways")

    table["split"] = "excluded"
    complete = table[table["complete"]]
    order = complete.groupby("regime").cumcount()
    table.loc[complete.index, "split"] = np.where(order % 2 == 0, "dev", "holdout")
    table.index.name = "quarter"
    return table
