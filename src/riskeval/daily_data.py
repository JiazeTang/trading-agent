"""日线数据：全市场股票池（S&P 1500）和复权收盘价。

需要能访问 Wikipedia 和 Yahoo Finance，所以在 GitHub Actions 里运行（见 .github/workflows/kova-study.yml）。
原始价格只留在运行环境里，不提交到仓库。

股票池用的是今天的 S&P 1500 成分股，有幸存者偏差：已经退市或被踢出指数的弱势股不在里面，
会让"相对强度"的排名略偏乐观。对同一时期内的信号比较影响有限，但要记住它。
"""

from __future__ import annotations

import time
from io import StringIO

import pandas as pd
import requests

WIKI_PAGES = {
    "S&P 500": "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
    "S&P 400": "https://en.wikipedia.org/wiki/List_of_S%26P_400_companies",
    "S&P 600": "https://en.wikipedia.org/wiki/List_of_S%26P_600_companies",
}
USER_AGENT = "Mozilla/5.0 (riskeval research script; low request volume)"


def sp1500_tickers() -> list[str]:
    """S&P 500 / 400 / 600 当前成分股，代码转成 Yahoo 格式（BRK.B → BRK-B）。"""
    tickers: set[str] = set()
    for name, url in WIKI_PAGES.items():
        html = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=30).text
        for table in pd.read_html(StringIO(html)):
            column = next((c for c in table.columns if str(c).lower() in ("symbol", "ticker symbol", "ticker")), None)
            if column is not None:
                tickers.update(str(t).strip().replace(".", "-") for t in table[column].dropna())
                break
        else:
            raise RuntimeError(f"{name} 页面里没找到代码列")
    return sorted(tickers)


def download_closes(tickers: list[str], start: str, chunk: int = 200, pause: float = 2.0) -> pd.DataFrame:
    """分批下载复权收盘价（日期 × 代码），批次之间暂停，避免触发限流。

    并发下载偶尔会有个别代码失败（如 yfinance 本地缓存被锁），最后对缺失的代码单线程重试。
    """
    frames = [_download(tickers[i:i + chunk], start, threads=True, pause=pause) for i in range(0, len(tickers), chunk)]
    closes = pd.concat(frames, axis=1)
    closes = closes.loc[:, ~closes.columns.duplicated()].dropna(axis=1, how="all")
    for _ in range(2):
        missing = [t for t in tickers if t not in closes.columns]
        if not missing:
            break
        retry = _download(missing, start, threads=False, pause=pause).dropna(axis=1, how="all")
        closes = pd.concat([closes, retry], axis=1)
    return closes.sort_index()


def _download(batch: list[str], start: str, threads: bool, pause: float) -> pd.DataFrame:
    import yfinance as yf

    data = yf.download(batch, start=start, auto_adjust=True, progress=False, threads=threads)
    closes = data["Close"] if isinstance(data.columns, pd.MultiIndex) else data[["Close"]].set_axis(batch, axis=1)
    closes.index = pd.DatetimeIndex(closes.index).tz_localize(None).normalize()
    time.sleep(pause)
    return closes


def market_caps(tickers: list[str], pause: float = 0.5) -> pd.Series:
    """当前市值；取不到的记为 NaN。"""
    import yfinance as yf

    caps = {}
    for ticker in tickers:
        try:
            caps[ticker] = float(yf.Ticker(ticker).fast_info["market_cap"])
        except Exception:  # noqa: BLE001 - 单只取不到不影响整体
            caps[ticker] = float("nan")
        time.sleep(pause)
    return pd.Series(caps)
