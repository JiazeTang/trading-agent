import numpy as np
import pytest

from riskeval.exit_study import exit_day


def test_exit_day_stop_take_and_mean():
    path = np.array([95.0, 88.0, 120.0])
    z = np.array([-1.0, -0.5, 0.5])
    assert exit_day(path, z, 100.0, -0.10, None) == 2
    assert exit_day(path, z, 100.0, None, 0.15) == 3
    assert exit_day(path, z, 100.0, None, "mean") == 3
    assert exit_day(path, z, 100.0, None, None) == 3
    assert exit_day(path, z, 100.0, -0.20, 0.10) == 3
