import numpy as np
import pandas as pd
import pytest

from riskeval import paper_trading
from riskeval.paper_trading import CAPITAL, evaluate, ledger_stats, run, run_ledger, size_factor, write_report


def _market(seed=0, end="2018-12-31"):
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range("2015-01-02", end)
    names = ["NVDA", "AMD", "MU", "TSM", "SMH"]
    data = {t: 100 * np.exp(np.cumsum(rng.normal(0.0005, 0.025, len(dates)))) for t in names}
    return pd.DataFrame(data, index=dates)


def test_size_factor():
    assert size_factor(0.03, "equal") == 1.0
    assert size_factor(0.01, "vol") == 1.0                      # 年化约 16%，低于 30%，不缩
    assert size_factor(0.04, "vol") == pytest.approx(0.30 / (0.04 * np.sqrt(252)))


def test_both_ledgers_trade_the_same_signals_with_smaller_b():
    px = _market()[["NVDA", "AMD", "MU", "TSM"]]
    a = run_ledger(px, "equal", start=pd.Timestamp("2016-01-04"))
    b = run_ledger(px, "vol", start=pd.Timestamp("2016-01-04"))
    assert len(a["trades"]) > 3
    key = ["股票", "买入日", "卖出日"]
    assert a["trades"][key].equals(b["trades"][key])
    assert (b["trades"]["金额"].to_numpy() <= a["trades"]["金额"].to_numpy() + 1e-9).all()
    assert a["equity"].iloc[0] == pytest.approx(CAPITAL)
    assert set(a["trades"]["原因"]) <= {"回到中轨", "止损"}       # 不设最长持有


def test_ledger_before_start_is_empty_and_report_says_so(tmp_path):
    px = _market(end="2016-06-30")
    res = run(px, today=pd.Timestamp("2016-06-30"))
    assert all(len(r["equity"]) == 0 for r in res["paper"].values())
    write_report(res, tmp_path)
    text = (tmp_path / "README.md").read_text(encoding="utf-8")
    assert "还没开始" in text and "回测参照" in text


def test_evaluation_waits_for_time_and_trades(monkeypatch):
    px = _market()
    monkeypatch.setattr(paper_trading, "START", pd.Timestamp("2016-01-04"))
    res = run(px)
    early = evaluate(res["paper"], pd.Timestamp("2017-01-02"))
    assert early.iloc[0]["是否满足"] == "还没到"
    stats = ledger_stats(res["paper"]["A 现行：等额"])
    assert stats["最大回撤"] <= 0 and stats["完成交易"] >= 0
