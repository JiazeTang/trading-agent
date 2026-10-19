import numpy as np
import pandas as pd

from riskeval.portfolio_sim import SEMI_CAPITAL, simulate_semis


def _closes():
    dates = pd.bdate_range("2015-01-02", "2016-12-30")
    up = np.linspace(100, 200, len(dates))
    dip = up.copy()
    i = dates.get_loc(pd.Timestamp("2016-06-01"))
    dip[i:i + 3] *= [0.93, 0.92, 0.94]  # 急跌后反弹，制造一次跌破下轨
    return pd.DataFrame({"A": dip, "B": up}, index=dates)


def test_mean_exit_sells_early_and_recycles_cash():
    closes = _closes()
    equity, log = simulate_semis(closes, ["A", "B"], pd.Timestamp("2016-01-04"), require_selloff=False,
                                 exit_mode="回到中轨", split_entry=False)
    trade = log.iloc[0]
    assert trade["股票"] == "A" and trade["原因"] == "回到中轨" and trade["持有天数"] < 42
    assert trade["收益"] > 0
    assert equity.iloc[-1] > SEMI_CAPITAL


def test_split_entry_adds_on_confirmation():
    closes = _closes()
    _, log = simulate_semis(closes, ["A", "B"], pd.Timestamp("2016-01-04"), require_selloff=False,
                            exit_mode="满42天", split_entry=True)
    assert bool(log.iloc[0]["补仓"])
