import numpy as np
import pandas as pd
import pytest

from riskeval.baseline import build_baseline
from riskeval.metrics import cvar95, risk_metrics, var95
from synthetic import make_bars


def test_risk_metrics_on_known_path():
    index = pd.DatetimeIndex(["2024-01-02 14:30Z", "2024-01-02 15:00Z", "2024-01-03 14:30Z", "2024-01-03 15:00Z"])
    returns = pd.Series([0.10, -0.20, 0.05, 0.10], index=index)

    m = risk_metrics(returns)

    assert m["total_return"] == pytest.approx(1.1 * 0.8 * 1.05 * 1.1 - 1)
    assert m["max_drawdown"] == pytest.approx(-0.20)
    assert m["max_dd_days"] == 2
    assert m["worst_day"] == pytest.approx(1.1 * 0.8 - 1)
    assert m["worst_bar"] == pytest.approx(-0.20)


def test_drawdown_counts_loss_from_the_starting_point():
    index = pd.DatetimeIndex(["2024-01-02 14:30Z", "2024-01-02 15:00Z"])
    m = risk_metrics(pd.Series([-0.10, 0.05], index=index))
    assert m["max_drawdown"] == pytest.approx(-0.10)
    assert m["max_dd_days"] == 1


def test_no_drawdown_when_price_only_rises():
    index = pd.DatetimeIndex(["2024-01-02 14:30Z", "2024-01-02 15:00Z"])
    m = risk_metrics(pd.Series([0.01, 0.02], index=index))
    assert m["max_drawdown"] == 0
    assert m["max_dd_days"] == 0


def test_var_and_cvar_use_the_worst_five_percent():
    daily = pd.Series(np.arange(-10, 10) / 100)
    assert var95(daily) == pytest.approx(-0.0905)
    assert cvar95(daily) == pytest.approx(-0.10)


def test_baseline_quarter_return_matches_regime_return():
    bars = make_bars("2022-01-01", "2022-12-31", {"2022Q1": 0.10, "2022Q2": -0.12, "2022Q3": 0.02, "2022Q4": 0.03})

    per_quarter, summary = build_baseline(bars)

    assert per_quarter["total_return"].to_numpy() == pytest.approx([0.10, -0.12, 0.02, 0.03])
    assert summary["quarters"].to_dict() == {
        ("up", "dev"): 1,
        ("sideways", "dev"): 1,
        ("sideways", "holdout"): 1,
        ("down", "dev"): 1,
    }
    assert summary.loc[("down", "dev"), "median_mdd"] == pytest.approx(-0.12)
