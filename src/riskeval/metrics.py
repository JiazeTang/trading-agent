"""风险指标。输入是持有期内逐根 30 分钟 K 线的收益（每天第一根包含隔夜跳空）。

亏损类指标一律用负数表示，例如最大回撤 -0.25 表示从高点回落 25%。
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from riskeval.regimes import REGIMES, SPLITS
from riskeval.sessions import session_dates

BARS_PER_DAY = 13
TRADING_DAYS = 252
BARS_PER_YEAR = BARS_PER_DAY * TRADING_DAYS


def bar_returns(bars: pd.DataFrame) -> pd.Series:
    """买入持有的逐 K 线收益：每根收盘相对上一根收盘，第一根用自己的开盘价作基准。"""
    returns = bars["close"].pct_change()
    returns.iloc[0] = bars["close"].iloc[0] / bars["open"].iloc[0] - 1
    return returns


def daily_returns(returns: pd.Series) -> pd.Series:
    """把 30 分钟收益复利合成为日收益，索引是交易日。"""
    return (1 + returns).groupby(session_dates(returns.index)).prod() - 1


def risk_metrics(returns: pd.Series) -> dict[str, float]:
    """一段持有期的风险指标。"""
    equity = (1 + returns).cumprod()
    # 起点净值 1 也算一个高点，这样第一根就下跌也会计入回撤
    drawdown = equity / equity.cummax().clip(lower=1.0) - 1
    daily = daily_returns(returns)
    return {
        "total_return": equity.iloc[-1] - 1,
        "ann_vol": returns.std() * np.sqrt(BARS_PER_YEAR),
        "downside_vol": np.sqrt((returns.clip(upper=0) ** 2).mean() * BARS_PER_YEAR),
        "max_drawdown": drawdown.min(),
        "max_dd_days": underwater_days(drawdown),
        "var95_daily": var95(daily),
        "cvar95_daily": cvar95(daily),
        "worst_day": daily.min(),
        "worst_bar": returns.min(),
    }


def underwater_days(drawdown: pd.Series) -> int:
    """最长一次处于回撤中（净值低于前高）跨越的交易日数。"""
    underwater = drawdown < 0
    if not underwater.any():
        return 0
    run_id = (~underwater).cumsum()[underwater]
    days = pd.Series(session_dates(drawdown.index)[underwater.to_numpy()], index=run_id.index)
    return int(days.groupby(run_id).nunique().max())


def var95(daily: pd.Series) -> float:
    """95% 历史 VaR：5% 的交易日跌得比这个还多。"""
    return daily.quantile(0.05)


def cvar95(daily: pd.Series) -> float:
    """95% CVaR：最差那 5% 交易日的平均收益。"""
    return daily[daily <= var95(daily)].mean()


def quarter_metrics(returns: pd.Series, quarters: pd.DataFrame) -> pd.DataFrame:
    """每个季度一行：市况标签、数据集，加上该季度的风险指标。"""
    quarter = session_dates(returns.index).to_period("Q")
    groups = list(returns.groupby(quarter))
    table = pd.DataFrame(
        [risk_metrics(r) for _, r in groups],
        index=pd.PeriodIndex([q for q, _ in groups], freq="Q", name="quarter"),
    )
    return quarters[["regime", "split"]].join(table)


def regime_summary(per_quarter: pd.DataFrame, returns: pd.Series) -> pd.DataFrame:
    """按 (市况, 数据集) 汇总。

    季度指标取中位数和最差值；日度 VaR / CVaR 把同类季度的所有交易日合在一起算，
    单个季度只有约 63 个交易日，单独算 5% 分位太不稳。
    """
    evaluated = per_quarter[per_quarter["split"] != "excluded"]
    by_quarter = evaluated.groupby(["regime", "split"])
    summary = pd.DataFrame({
        "quarters": by_quarter.size(),
        "median_return": by_quarter["total_return"].median(),
        "median_vol": by_quarter["ann_vol"].median(),
        "median_mdd": by_quarter["max_drawdown"].median(),
        "worst_mdd": by_quarter["max_drawdown"].min(),
    })

    daily = daily_returns(returns)
    labels = evaluated[["regime", "split"]].reindex(daily.index.to_period("Q"))
    by_day = daily.groupby([labels["regime"].to_numpy(), labels["split"].to_numpy()])
    summary["var95_daily"] = by_day.apply(var95)
    summary["cvar95_daily"] = by_day.apply(cvar95)
    summary["worst_day"] = by_day.min()

    order = pd.MultiIndex.from_product([REGIMES, SPLITS], names=["regime", "split"])
    summary = summary.reindex(order).dropna(subset=["quarters"])
    summary["quarters"] = summary["quarters"].astype(int)
    return summary
