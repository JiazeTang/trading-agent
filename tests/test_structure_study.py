import numpy as np
import pandas as pd
import pytest

from riskeval.structure_study import CAPITAL, GROUP_CAP, build_rules, simulate


def _data():
    dates = pd.bdate_range("2015-01-02", "2016-12-30")
    trend = np.linspace(100, 200, len(dates))
    a = trend.copy()
    i = dates.get_loc(pd.Timestamp("2016-06-01"))
    a[i:i + 3] *= [0.93, 0.92, 0.94]
    px = pd.DataFrame({"A": a, "B": trend * 1.01}, index=dates)
    return px, pd.Series(trend, index=dates)


def test_core_only_tracks_core_and_overlay_trades():
    px, core = _data()
    rules = build_rules(px)
    eq, expo, log = simulate(px, core, rules, pd.Timestamp("2016-01-04"), rule="A", slots=2,
                             sizing="equal", cap=False, core=0.6)
    assert len(log) == 1 and log.iloc[0]["股票"] == "A"
    assert log.iloc[0]["仓位"] == pytest.approx(CAPITAL * 0.4 / 2, rel=0.05)
    assert eq.iloc[-1] > CAPITAL


def test_group_cap_limits_single_stock_exposure():
    px, core = _data()
    rules = build_rules(px)
    _, expo, _ = simulate(px, core, rules, pd.Timestamp("2016-01-04"), rule="A", slots=1,
                          sizing="equal", cap=True, core=0.0)
    assert expo.max() <= GROUP_CAP + 0.05
