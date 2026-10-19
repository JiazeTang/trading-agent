import numpy as np
import pandas as pd
import pytest

from riskeval import forward, signals
from riskeval.kova_study import pick_targets


def test_rs_rating_ranks_stronger_stocks_higher():
    dates = pd.bdate_range("2020-01-01", periods=300)
    growth = np.linspace(-0.001, 0.002, 120)  # 第 i 只股票每天涨 growth[i]
    closes = pd.DataFrame(np.exp(np.outer(np.arange(300), growth)), index=dates)

    rating = signals.rs_rating(closes).iloc[-1]

    assert rating.is_monotonic_increasing
    assert rating.iloc[-1] == pytest.approx(99)
    assert signals.rs_rating(closes).iloc[200].isna().all()  # 不足 252 天不打分


def test_rs_rating_requires_enough_stocks():
    dates = pd.bdate_range("2020-01-01", periods=300)
    closes = pd.DataFrame(np.ones((300, 10)), index=dates)
    assert signals.rs_rating(closes).isna().all().all()


def test_sector_regime_uses_efficiency_ratio():
    up = pd.Series(np.arange(1.0, 41.0))
    choppy = pd.Series([10.0, 11.0] * 20)
    assert signals.sector_regime(up).iloc[-1] == "上行趋势"
    assert signals.sector_regime(up[::-1].reset_index(drop=True)).iloc[-1] == "下行趋势"
    assert signals.sector_regime(choppy).iloc[-1] == "震荡"
    assert pd.isna(signals.sector_regime(up).iloc[5])


def test_forward_stats_enters_next_day_and_tracks_path():
    close = pd.Series([100.0, 110.0, 99.0, 121.0, 132.0], index=pd.bdate_range("2024-01-01", periods=5))

    stats = forward.forward_stats(close, h=2)

    first = stats.iloc[0]  # 信号在第 0 天，第 1 天以 110 买入，第 3 天以 121 卖出
    assert first["ret"] == pytest.approx(121 / 110 - 1)
    assert first["mae"] == pytest.approx(99 / 110 - 1)
    assert first["ret_to_date"] == pytest.approx(132 / 110 - 1)
    assert np.isnan(stats["ret"].iloc[3])  # 持有期不完整


def test_summarize_counts_wins_losses_and_stocks():
    rows = pd.DataFrame({
        "ticker": ["A", "A", "B", "B"],
        "ret": [0.10, -0.05, -0.02, np.nan],
        "excess": [0.05, -0.01, -0.03, np.nan],
        "vol": 0.3, "mae": [-0.02, -0.08, -0.04, np.nan],
    })

    s = forward.summarize(rows)

    assert (s["入场次数"], s["赚钱次数"], s["赔钱次数"]) == (3, 1, 2)
    assert s["平均赚"] == pytest.approx(0.10)
    assert s["平均赔"] == pytest.approx(-0.035)
    assert (s["收益为正的股票数"], s["收益为负的股票数"]) == (1, 1)
    assert s["最差最大浮亏"] == pytest.approx(-0.08)


def test_pick_targets_takes_largest_per_group_and_skips_missing_caps():
    caps = pd.Series({"MU": 3.0, "SNDK": 1.0, "WDC": np.nan, "STX": 2.0})
    assert pick_targets(caps)["存储"] == ["MU", "STX", "SNDK", "WDC"]
