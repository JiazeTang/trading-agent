import numpy as np
import pandas as pd
import pytest

from riskeval.swing_study import (CAPITAL, COST, ENTRIES, EXITS, STOPS, account_stats, entry_flags, event_table,
                                  exit_reason, indicators, new_position, run, simulate, step, stock_trades)


def _walk(prices, z=0.0, ma=0.0, exit_rule="mean", stop=None, sigma=0.03):
    """按顺序喂收盘价，返回（第几天卖出, 原因）；z、ma 可以是常数或序列。"""
    pos = new_position(100.0, sigma, None)
    zs = z if np.ndim(z) else [z] * len(prices)
    for day, (price, zz) in enumerate(zip(prices, zs), start=1):
        step(pos, price)
        reason = exit_reason(pos, price, zz, ma, exit_rule, stop)
        if reason:
            return day, reason
    return None, None


def test_fixed_and_sigma_stops():
    assert _walk([95, 89], z=-1, stop=("fixed", 0.10)) == (2, "止损")
    # 3σ = 9%：跌到 91 还没到，跌到 90.9 就到了
    assert _walk([91.5, 90.9], z=-1, stop=("sigma", 3.0)) == (2, "止损")


def test_trailing_stop_follows_the_high():
    # 先涨到 120，再回落到 120 × (1 - 9%) = 109.2 以下才止损，虽然仍高于买入价
    assert _walk([110, 120, 112, 109], z=-1, stop=("trail", 3.0)) == (4, "止损")


def test_time_and_trend_stops():
    assert _walk([99] * 12, z=-1, stop=("time", 10)) == (10, "止损")
    assert _walk([101] * 12, z=-1, stop=("time", 10), exit_rule="hold20") == (None, None)
    assert _walk([98], z=-1, ma=99.0, stop=("trend", None)) == (1, "止损")


def test_exits():
    assert _walk([101, 102], z=[-0.5, 0.1]) == (2, "出场")
    assert _walk([101, 102, 103], z=[0.5, 1.9, 2.1], exit_rule="upper") == (3, "出场")
    # 中轨后跟踪：先回到中轨（第 2 天），之后第一次跌回中轨下方（第 4 天）才卖
    assert _walk([101, 103, 104, 102], z=[-0.5, 0.2, 0.8, -0.1], exit_rule="trail_mean") == (4, "出场")
    assert _walk([101] * 25, z=-1, exit_rule="hold20") == (20, "出场")
    assert _walk([101] * 50, z=-1, exit_rule="upper") == (42, "到期")


def _market(seed=0):
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range("2015-01-02", "2018-12-31")
    cols = {}
    for k in range(4):
        r = rng.normal(0.0006, 0.02, len(dates))
        cols[f"S{k}"] = 100 * np.exp(np.cumsum(r))
    cols["SMH"] = 100 * np.exp(np.cumsum(rng.normal(0.0005, 0.015, len(dates))))
    return pd.DataFrame(cols, index=dates)


def test_trades_do_not_overlap_and_pay_costs():
    px = _market()
    ind = indicators(px)
    flags = entry_flags(px, ind, sector=True)
    e1 = flags[ENTRIES[0]]["S0"].to_numpy()
    trades = stock_trades(px["S0"].to_numpy(), ind["z"]["S0"].to_numpy(), ind["ma"]["S0"].to_numpy(),
                          ind["sigma"]["S0"].to_numpy(), e1, px.index, "hold20", None)
    assert trades and all(t["days"] == 20 or t["reason"] == "到期" for t in trades)
    starts = [px.index.get_loc(t["date"]) for t in trades]
    assert all(b - a >= 21 for a, b in zip(starts, starts[1:]))
    first = trades[0]
    i = px.index.get_loc(first["date"]) + 1
    gross = px["S0"].iloc[i + 20] / px["S0"].iloc[i] - 1
    assert first["ret"] == pytest.approx((1 + gross) * (1 - COST) ** 2 - 1)


def test_simulate_keeps_cash_when_no_signal_and_respects_slots():
    px = _market()
    ind = indicators(px)
    e1 = entry_flags(px, ind, sector=True)[ENTRIES[0]][["S0", "S1", "S2", "S3"]]
    stocks = px[["S0", "S1", "S2", "S3"]]
    eq, expo, log = simulate(stocks, ind, e1, "mean", ("fixed", 0.20))
    assert eq.iloc[0] == pytest.approx(CAPITAL)
    assert (expo <= 1 + 1e-9).all() and (expo >= 0).all()
    assert len(log) > 0
    none = simulate(stocks, ind, e1 & False, "mean", None)[0]
    assert (none == CAPITAL).all()
    stats = account_stats(eq, expo, len(log))
    assert stats["最大回撤"] <= 0 and 0 < stats["持仓时间占比"] < 1


def test_event_table_measures_forward_returns_from_next_close():
    dates = pd.bdate_range("2015-01-02", "2017-12-29")
    px = pd.DataFrame({"A": np.linspace(100, 200, len(dates))}, index=dates)
    flag = pd.DataFrame({"A": False}, index=dates)
    t = dates.get_loc(pd.Timestamp("2016-06-01"))
    flag.iloc[t, 0] = True
    table = event_table(px, {ENTRIES[0]: flag})
    expected = px["A"].iloc[t + 2] / px["A"].iloc[t + 1] - 1
    assert table.loc[0, "段数"] == 1 and table.loc[0, "1天平均"] == pytest.approx(expected)
    assert table.loc[0, "最高点在第几天(中位)"] == 42


def test_run_produces_every_table():
    px = _market(1)
    res = run(px.rename(columns={"S0": "NVDA", "S1": "AMD", "S2": "MU", "S3": "TSM"}), None)
    assert len(res["grid"]) == len(EXITS) * len(STOPS)
    assert len(res["account"]) == len(EXITS) * (len(STOPS) + 1) + 1
    assert set(res["verdicts"]["能降波动"]) <= {"是", "否", "降了波动但 Sharpe 损失超过一成"}
    assert len(res["replacement"]) >= 1


def test_improvement_luck_check():
    from riskeval.swing_study import improvement_dsr

    dates = pd.bdate_range("2016-01-04", periods=2500)
    rng = np.random.default_rng(3)
    base = pd.Series(1000 * np.cumprod(1 + rng.normal(0.0004, 0.01, len(dates))), index=dates)
    noise = pd.Series(1000 * np.cumprod(1 + rng.normal(0.0004, 0.01, len(dates))), index=dates)
    better = base * np.cumprod(np.full(len(dates), 1.0008))
    assert improvement_dsr(better, base, 31) > 0.95
    assert improvement_dsr(noise, base, 31) < 0.95
