import numpy as np
import pandas as pd
import pytest

from riskeval.style_compare import _from_state, hourly_orb, metrics, vol_breakout


def test_vol_breakout_fills_at_trigger_and_sells_at_close():
    idx = pd.bdate_range("2024-01-01", periods=2)
    o = pd.DataFrame({"X": [100.0, 100.0]}, index=idx)
    h = pd.DataFrame({"X": [104.0, 106.0]}, index=idx)
    l = pd.DataFrame({"X": [100.0, 99.0]}, index=idx)
    c = pd.DataFrame({"X": [101.0, 105.0]}, index=idx)
    gross, turns, hit = vol_breakout(o, h, l, c)
    assert gross["X"].iloc[1] == pytest.approx(105 / 102 - 1)  # 触发价 = 100 + 0.5 × 4
    assert turns["X"].iloc[1] == 2 and not hit["X"].iloc[0]


def test_state_trades_next_close():
    idx = pd.bdate_range("2024-01-01", periods=5)
    c = pd.DataFrame({"X": [100.0, 101.0, 103.0, 106.0, 110.0]}, index=idx)
    state = pd.DataFrame({"X": [1, 1, 1, 1, 1]}, index=idx)
    gross, turns, held = _from_state(c, state)
    assert gross["X"].iloc[1] == 0  # 第 0 天收盘决定，第 1 天收盘买入
    assert gross["X"].iloc[2] == pytest.approx(103 / 101 - 1)
    assert turns["X"].iloc[1] == 1


def test_hourly_orb_enters_on_break_and_stops_below_range():
    idx = pd.DatetimeIndex(["2024-01-02 09:30", "2024-01-02 10:30", "2024-01-02 11:30", "2024-01-02 15:30"],
                           tz="America/New_York")
    h = pd.DataFrame({"X": [101.0, 103, 103, 103]}, index=idx)
    l = pd.DataFrame({"X": [99.0, 100, 98, 97]}, index=idx)
    c = pd.DataFrame({"X": [100.0, 102, 98.5, 97.5]}, index=idx)
    gross, turns, _ = hourly_orb(c, h, l, c)
    assert gross["X"].iloc[0] == pytest.approx(98.5 / 102 - 1)
    assert turns["X"].iloc[0] == 2


def test_metrics_reports_periods_and_years():
    idx = pd.bdate_range("2016-01-01", "2026-10-16")
    daily = pd.Series(0.0004, index=idx)
    m = metrics(daily, pd.Series(True, index=idx), pd.Series(0.0, index=idx))
    assert m["年化收益"] == pytest.approx((1.0004) ** 252 - 1, rel=0.01)
    assert m["最大回撤"] == 0
