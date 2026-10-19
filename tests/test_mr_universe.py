import numpy as np
import pandas as pd
import pytest

from riskeval.mr_universe import HOLD, simulate, wilson_lower


def test_wilson_lower_penalises_small_samples():
    assert wilson_lower(3, 3) < wilson_lower(30, 30) < 1
    assert wilson_lower(30, 30) > wilson_lower(27, 30)
    assert wilson_lower(5, 10) == pytest.approx(0.2366, abs=1e-3)


def test_simulate_skips_signals_while_holding():
    dates = pd.bdate_range("2016-01-01", periods=200)
    close = pd.Series(np.linspace(100, 199, 200), index=dates)
    signal = pd.Series(False, index=dates)
    signal.iloc[[0, 5, 60]] = True  # 第 5 天的信号落在第一笔持仓期内，应被忽略

    trades = simulate(close, signal)

    assert list(trades["date"]) == [dates[0], dates[60]]
    assert trades["ret"].iloc[0] == pytest.approx(close.iloc[1 + HOLD] / close.iloc[1] - 1)
    assert (trades["mae"] == 0).all()
