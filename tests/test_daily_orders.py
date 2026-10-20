import json

import numpy as np
import pandas as pd
import pytest

from riskeval.daily_orders import load_portfolio, make_orders, summary_lines
from riskeval.mr_screen import TARGETS


def _closes(dip=None, pop=None):
    dates = pd.bdate_range("2025-01-01", periods=300)
    tickers = [t for ts in TARGETS.values() for t in ts] + ["SMH"]
    closes = pd.DataFrame({t: np.linspace(100, 150, 300) for t in tickers}, index=dates)
    if dip:
        closes.iloc[-1, closes.columns.get_loc(dip)] *= 0.93
    if pop:
        closes.iloc[-1, closes.columns.get_loc(pop)] *= 1.05
    return closes


def _holdings(rows):
    return pd.DataFrame(rows, columns=["ticker", "role", "shares", "entry_price", "entry_date"])


def test_buys_lowest_z_into_free_slot():
    orders = make_orders(_closes(dip="AMD"), _holdings([]), {"overlay_cash": 1600, "overlay_slots": 2, "core_target": 2400})
    buys = orders["buys"]
    assert list(buys["股票"]) == ["AMD"]
    assert buys.iloc[0]["建议金额"] == pytest.approx(800)
    assert any("核心仓 SMH 还差约 2,400" in line for line in summary_lines(orders))


def test_sells_overlay_back_at_mean_and_on_stop():
    holdings = _holdings([["MU", "overlay", 5, 140.0, "2025-12-01"], ["NVDA", "overlay", 5, 300.0, "2025-12-01"],
                          ["SMH", "core", 10, 120.0, "2025-12-01"]])
    orders = make_orders(_closes(pop="MU"), holdings, {"overlay_cash": 0, "overlay_slots": 2, "core_target": 1000})
    sells = orders["sells"].set_index("股票")
    assert sells.loc["MU", "原因"].startswith("回到中轨")
    assert sells.loc["NVDA", "原因"].startswith("止损")
    assert orders["market"].iloc[0]["核心仓还差"] == 0


def test_load_portfolio_skips_comments(tmp_path):
    (tmp_path / "holdings.csv").write_text("# note\nticker,role,shares,entry_price,entry_date\nsmh, Core ,2,100,2026-10-20\n")
    (tmp_path / "account.json").write_text(json.dumps({"overlay_cash": 1600, "overlay_slots": 2}))
    holdings, account = load_portfolio(tmp_path)
    assert holdings.iloc[0]["ticker"] == "SMH" and holdings.iloc[0]["role"] == "core"
    assert account["overlay_slots"] == 2


def test_trigger_price_puts_next_close_on_the_lower_band():
    from riskeval import signals
    from riskeval.daily_orders import trigger_price

    rng = np.random.default_rng(1)
    history = pd.Series(100 + rng.normal(0, 2, 60).cumsum())
    price = trigger_price(history)
    extended = pd.concat([history, pd.Series([price])], ignore_index=True)
    assert signals.zscore(extended).iloc[-1] == pytest.approx(-2.0, abs=1e-6)
    assert price < history.iloc[-1]


def test_complete_closes_drops_trailing_empty_row():
    from riskeval.daily_orders import complete_closes

    closes = _closes()
    closes.loc[closes.index[-1] + pd.offsets.BDay(1)] = np.nan
    cleaned = complete_closes(closes, list(closes.columns))
    assert cleaned.index[-1] == closes.index[-2]


def test_keep_rows_show_next_day_sell_line():
    holdings = _holdings([["MU", "overlay", 5, 150.0, "2025-12-01"]])
    closes = _closes(dip="MU")
    orders = make_orders(closes, holdings, {"overlay_cash": 0, "overlay_slots": 2})
    row = orders["keep"].iloc[0]
    assert row["明日卖出线"] == pytest.approx(closes["MU"].iloc[-19:].mean())


def test_last_closed_session_skips_weekend():
    from riskeval.daily_orders import last_closed_session

    saturday = pd.Timestamp("2026-10-17 12:00", tz="UTC")
    assert last_closed_session(saturday) == pd.Timestamp("2026-10-16")
