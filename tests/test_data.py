import pandas as pd
import pytest

from riskeval.data import check_quality, fetch_alpaca_bars, keep_regular_hours
from riskeval.sessions import nyse_schedule
from synthetic import bar_times


def test_keep_regular_hours_handles_extended_hours_and_early_close():
    stamps = pd.DatetimeIndex([
        "2024-11-29 13:00Z",  # 08:00 美东，盘前
        "2024-11-29 14:30Z",  # 09:30 开盘第一根
        "2024-11-29 17:30Z",  # 12:30，提前收盘日的最后一根
        "2024-11-29 18:00Z",  # 13:00，提前收盘日已收盘
        "2024-11-30 15:00Z",  # 周六
        "2024-12-02 20:30Z",  # 15:30，正常日最后一根
        "2024-12-02 21:00Z",  # 16:00，盘后
    ])
    bars = pd.DataFrame({"close": range(len(stamps))}, index=stamps)

    kept = keep_regular_hours(bars, nyse_schedule("2024-11-29", "2024-12-02"))

    assert list(kept.index) == [stamps[1], stamps[2], stamps[5]]


def test_check_quality_reports_missing_bars_and_days():
    index = bar_times("2024-11-26", "2024-12-03")
    missing_bar = pd.Timestamp("2024-11-26 15:00Z")
    missing_day = index[(index >= "2024-12-02") & (index < "2024-12-03")]
    bars = pd.DataFrame({"close": 1.0}, index=index.drop([missing_bar, *missing_day]))

    issues = check_quality(bars, nyse_schedule("2024-11-26", "2024-12-03"))

    assert issues.to_dict("index") == {
        pd.Timestamp("2024-11-26"): {"expected": 13, "actual": 12},
        pd.Timestamp("2024-12-02"): {"expected": 13, "actual": 0},
    }


def test_check_quality_expects_seven_bars_on_early_close():
    index = bar_times("2024-11-29", "2024-11-29")
    assert len(index) == 7
    bars = pd.DataFrame({"close": 1.0}, index=index)
    assert check_quality(bars, nyse_schedule("2024-11-29", "2024-11-29")).empty


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        pass

    def json(self):
        return self.payload


class FakeHttp:
    def __init__(self, pages):
        self.pages = list(pages)
        self.calls = []

    def get(self, url, params, headers, timeout):
        self.calls.append({"url": url, "params": dict(params), "headers": headers})
        return FakeResponse(self.pages.pop(0))


def _bar(t, price):
    return {"t": t, "o": price, "h": price, "l": price, "c": price, "v": 10, "n": 1, "vw": price}


def test_fetch_alpaca_bars_follows_pagination(monkeypatch):
    monkeypatch.setenv("APCA_API_KEY_ID", "key")
    monkeypatch.setenv("APCA_API_SECRET_KEY", "secret")
    http = FakeHttp([
        {"bars": [_bar("2024-01-02T14:30:00Z", 400.0)], "next_page_token": "abc"},
        {"bars": [_bar("2024-01-02T15:00:00Z", 401.0)], "next_page_token": None},
    ])

    bars = fetch_alpaca_bars("QQQ", "2024-01-02", "2024-01-03", http=http)

    assert list(bars.columns) == ["open", "high", "low", "close", "volume"]
    assert list(bars["close"]) == [400.0, 401.0]
    assert str(bars.index.tz) == "UTC"
    first, second = http.calls
    assert first["url"].endswith("/v2/stocks/QQQ/bars")
    assert first["params"]["timeframe"] == "30Min"
    assert first["params"]["adjustment"] == "all"
    assert first["params"]["start"] == "2024-01-02T00:00:00Z"
    assert "page_token" not in first["params"]
    assert second["params"]["page_token"] == "abc"
    assert first["headers"] == {"APCA-API-KEY-ID": "key", "APCA-API-SECRET-KEY": "secret"}


def test_fetch_alpaca_bars_requires_keys(monkeypatch):
    monkeypatch.delenv("APCA_API_KEY_ID", raising=False)
    monkeypatch.delenv("APCA_API_SECRET_KEY", raising=False)
    with pytest.raises(RuntimeError, match="APCA_API_KEY_ID"):
        fetch_alpaca_bars("QQQ", "2024-01-02", "2024-01-03", http=FakeHttp([]))
