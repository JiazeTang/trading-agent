import pandas as pd
import pytest

from riskeval.regimes import label_quarters
from riskeval.sessions import nyse_schedule
from synthetic import make_bars

QUARTER_RETURNS = {
    "2022Q1": 0.10,   # up
    "2022Q2": -0.12,  # down
    "2022Q3": 0.02,   # sideways
    "2022Q4": 0.09,   # up
    "2023Q1": -0.01,  # sideways
    "2023Q2": -0.09,  # down
    "2023Q3": 0.20,   # 数据只到 8 月中，季度不完整
}


@pytest.fixture
def quarters():
    bars = make_bars("2022-01-01", "2023-08-15", QUARTER_RETURNS)
    calendar = nyse_schedule("2022-01-01", "2023-09-30").index
    return label_quarters(bars, calendar)


def test_quarter_returns_match_price_path(quarters):
    expected = pd.Series(QUARTER_RETURNS).drop("2023Q3")
    actual = quarters["return"].drop(pd.Period("2023Q3"))
    assert actual.to_numpy() == pytest.approx(expected.to_numpy())


def test_regime_labels_and_split_are_fixed_by_rule(quarters):
    table = quarters[["regime", "split"]]
    table.index = table.index.astype(str)
    assert table.to_dict("index") == {
        "2022Q1": {"regime": "up", "split": "dev"},
        "2022Q2": {"regime": "down", "split": "dev"},
        "2022Q3": {"regime": "sideways", "split": "dev"},
        "2022Q4": {"regime": "up", "split": "holdout"},
        "2023Q1": {"regime": "sideways", "split": "holdout"},
        "2023Q2": {"regime": "down", "split": "holdout"},
        "2023Q3": {"regime": "up", "split": "excluded"},
    }


def test_incomplete_quarter_is_flagged(quarters):
    assert quarters["complete"].drop(pd.Period("2023Q3")).all()
    assert not quarters.loc[pd.Period("2023Q3"), "complete"]
