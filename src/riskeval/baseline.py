"""里程碑 1：QQQ 买入持有在上涨 / 震荡 / 下跌三类市况下的风险基线。

    python -m riskeval.baseline              # 有缓存用缓存，没有就从 Alpaca 下载
    python -m riskeval.baseline --refresh    # 重新下载（更新数据，或改了 --start 之后）

结果打印在终端，完整表格写到 reports/。
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from riskeval.data import check_quality, default_end, load_bars
from riskeval.metrics import bar_returns, quarter_metrics, regime_summary
from riskeval.regimes import label_quarters
from riskeval.sessions import nyse_schedule, session_dates

PERCENT_COLUMNS = [
    "return", "total_return", "median_return", "ann_vol", "median_vol", "downside_vol",
    "max_drawdown", "median_mdd", "worst_mdd", "var95_daily", "cvar95_daily", "worst_day", "worst_bar",
]


def build_baseline(bars: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """返回 (季度明细, 市况汇总)。"""
    days = session_dates(bars.index)
    first_quarter, last_quarter = days[0].to_period("Q"), days[-1].to_period("Q")
    calendar = nyse_schedule(first_quarter.start_time, last_quarter.end_time).index

    quarters = label_quarters(bars, calendar)
    returns = bar_returns(bars)
    per_quarter = quarter_metrics(returns, quarters)
    return per_quarter, regime_summary(per_quarter, returns)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="QQQ 买入持有的分市况风险基线")
    parser.add_argument("--symbol", default="QQQ")
    parser.add_argument("--start", default="2016-01-01", help="Alpaca 的 SIP 历史数据从 2016 年开始")
    parser.add_argument("--refresh", action="store_true", help="忽略缓存，重新下载")
    parser.add_argument("--out", default="reports", help="CSV 输出目录")
    args = parser.parse_args(argv)

    bars = load_bars(args.symbol, args.start, default_end(), refresh=args.refresh)
    first, last = session_dates(bars.index[[0, -1]])
    print(f"{args.symbol}：{len(bars)} 根常规时段 30 分钟 K 线，{first:%Y-%m-%d} ~ {last:%Y-%m-%d}")

    issues = check_quality(bars, nyse_schedule(first, last))
    print(f"数据质量：{len(issues)} 个交易日的 K 线根数和日历不符")
    if not issues.empty:
        print(issues.head(20).to_string())

    per_quarter, summary = build_baseline(bars)

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    per_quarter.to_csv(out / f"{args.symbol}_quarters.csv")
    summary.to_csv(out / f"{args.symbol}_regimes.csv")

    columns = ["regime", "split", "total_return", "max_drawdown", "ann_vol", "worst_day"]
    print("\n季度明细（split=excluded 表示季度不完整，不参与评估）")
    print(_as_percent(per_quarter[columns]).to_string())
    print("\n按市况汇总（买入持有）")
    print(_as_percent(summary).to_string())
    print(f"\n完整表格已写入 {out}/")


def _as_percent(table: pd.DataFrame) -> pd.DataFrame:
    table = table.copy()
    for column in table.columns.intersection(PERCENT_COLUMNS):
        table[column] = table[column].map(lambda x: f"{x:.1%}")
    return table


if __name__ == "__main__":
    main()
