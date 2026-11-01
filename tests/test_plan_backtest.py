import numpy as np
import pandas as pd
import pytest

from riskeval.mr_screen import TARGETS
from riskeval.plan_backtest import CASH, OVERLAY, PLAN, hold, run, write_report


def _closes(seed=0):
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range("2015-01-02", "2018-12-31")
    names = [t for ts in TARGETS.values() for t in ts] + ["SMH", "QQQ", "REGN", "VRTX"]
    data = 100 * np.exp(np.cumsum(rng.normal(0.0004, 0.02, (len(dates), len(names))), axis=0))
    return pd.DataFrame(data, index=dates, columns=names)


def test_hold_tracks_price_after_one_buy_cost():
    index = pd.bdate_range("2016-01-04", periods=3)
    value = hold(pd.Series([10.0, 11.0, 12.0], index=index), 1000.0, index)
    assert value.iloc[-1] == pytest.approx(1000 * (1 - 0.0005) * 1.2)


def test_plan_starts_at_8000_and_parts_add_up(tmp_path):
    res = run(_closes())
    plan = res["summary"].iloc[0]
    contrib = res["contribution"]
    assert contrib["投入"].sum() == pytest.approx(sum(PLAN.values()) * (1 - 0.0005) + OVERLAY + CASH, rel=1e-3)
    assert contrib["现在"].sum() == pytest.approx(plan["期末金额"])
    assert contrib["占总盈利"].sum() == pytest.approx(1.0)
    assert set(res["calendar"].columns[:1]) == {"组合"}
    write_report(res, tmp_path)
    assert "每年的收益" in (tmp_path / "README.md").read_text(encoding="utf-8")
