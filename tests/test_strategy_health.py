import numpy as np
import pandas as pd
import pytest

from riskeval.strategy_health import (dsr, expected_max_sharpe, longest_losing_streak, min_track_record_years,
                                      path_risk, psr, stationary_bootstrap)


def _normal_returns(annual_sharpe, years=10, seed=0):
    rng = np.random.default_rng(seed)
    daily_vol = 0.01
    r = rng.normal(annual_sharpe / np.sqrt(252) * daily_vol, daily_vol, 252 * years)
    return pd.Series(r)


def test_psr_is_high_for_a_strong_strategy_and_near_half_for_noise():
    assert psr(_normal_returns(2.0)) > 0.99
    assert 0.05 < psr(_normal_returns(0.0, seed=3)) < 0.95


def test_min_track_record_matches_normal_rule_of_thumb():
    # 正态、年化 Sharpe 1：大约需要 (1.645 / 1)^2 ≈ 2.7 年
    years = min_track_record_years(_normal_returns(1.0, years=30))
    assert 1.5 < years < 5
    assert min_track_record_years(_normal_returns(-1.0)) == float("inf")


def test_luck_hurdle_grows_with_number_of_trials():
    assert expected_max_sharpe(100, 1e-4) > expected_max_sharpe(10, 1e-4) > 0
    p10, hurdle10 = dsr(_normal_returns(1.0), 10)
    p100, hurdle100 = dsr(_normal_returns(1.0), 100)
    assert hurdle100 > hurdle10 and p100 < p10


def test_bootstrap_shapes_and_drawdown_sign():
    sampled = stationary_bootstrap(_normal_returns(0.5).to_numpy(), paths=200, horizon=50)
    assert sampled.shape == (200, 50)
    risk = path_risk(sampled)
    assert (risk["最大回撤"] <= 0).all() and (risk["最长水下天数"] <= 50).all()


def test_longest_losing_streak():
    outcomes = np.array([[0.1, -0.1, -0.2, 0.0, 0.3, -0.1]])
    assert longest_losing_streak(outcomes)[0] == 3
