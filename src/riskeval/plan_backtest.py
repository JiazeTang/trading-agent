"""整个账户 8000 按现行方案（2026-10-19 确定）从 2016 年起原样回测，回答"整体年化多少"。

    python -m riskeval.plan_backtest --out reports/plan_backtest

这里不挑规则、不调参数，只把现行方案整体跑一遍，以下照搬方案：
- SMH 2400、REGN 1200、VRTX 1200：2016 年第一个交易日收盘买入，一直持有，不再平衡。
- 加码仓 1600：规则 A，2 个仓位，等额；回到 20 日均线卖出，-20% 止损，不设最长持有。
  直接调用模拟盘账本 A 的代码（paper_trading.run_ledger），和每天的模拟盘是同一套规则。
- 现金 1600：不计利息（偏保守；按 2016–2026 的短期国债利率，每年少算约 2%×1600 ≈ 30）。
- 成本：每次买卖扣 0.05%。复权收盘价，含分红再投资。
- 对照：同样的 8000，不要加码仓（那 1600 也买 SMH）；8000 全买 SMH；8000 全买 QQQ。
- 统计：年化收益、年化波动、Sharpe、最大回撤、最差一天，每个自然年的收益，2016–2022 与 2023 年后，
  以及各部分对总盈利的贡献。

局限：16 只半导体按今天的市值挑选；REGN、VRTX 也是今天选的。2016–2026 是半导体大牛市。数字偏乐观。
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from riskeval.mr_screen import TARGETS
from riskeval.paper_trading import run_ledger

START = pd.Timestamp("2016-01-01")
SPLIT = pd.Timestamp("2023-01-01")
COST = 0.0005
TOTAL = 8000.0
PLAN = {"SMH": 2400.0, "REGN": 1200.0, "VRTX": 1200.0}
OVERLAY, CASH = 1600.0, 1600.0
PARTS = {"SMH 核心仓": "SMH", "加码仓（规则 A）": "overlay", "REGN": "REGN", "VRTX": "VRTX", "现金": "cash"}


def hold(price: pd.Series, amount: float, index: pd.DatetimeIndex) -> pd.Series:
    """收盘买入后一直持有的市值（扣一次买入成本）。"""
    p = price.reindex(index).ffill()
    return amount * (1 - COST) * p / p.iloc[0]


def plan_parts(closes: pd.DataFrame) -> pd.DataFrame:
    """现行方案每一部分的每日市值。"""
    semis = [t for ts in TARGETS.values() for t in ts if t in closes.columns]
    overlay = run_ledger(closes[semis], "equal", start=START)["equity"]
    index = overlay.index
    parts = {"SMH 核心仓": hold(closes["SMH"], PLAN["SMH"], index), "加码仓（规则 A）": overlay,
             "REGN": hold(closes["REGN"], PLAN["REGN"], index), "VRTX": hold(closes["VRTX"], PLAN["VRTX"], index),
             "现金": pd.Series(CASH, index=index)}
    return pd.DataFrame(parts)


def stats(equity: pd.Series) -> dict:
    daily = equity.pct_change().dropna()
    years = len(daily) / 252
    vol = daily.std() * np.sqrt(252)
    out = {"期末金额": equity.iloc[-1], "年化收益": (equity.iloc[-1] / equity.iloc[0]) ** (1 / years) - 1,
           "年化波动": vol, "Sharpe": daily.mean() * 252 / vol, "最大回撤": (equity / equity.cummax() - 1).min(),
           "最差一天": daily.min()}
    for label, part in {"2016-22": equity[equity.index < SPLIT], "2023后": equity[equity.index >= SPLIT]}.items():
        n = len(part) - 1
        out[f"年化·{label}"] = (part.iloc[-1] / part.iloc[0]) ** (252 / n) - 1 if n > 0 else np.nan
        out[f"最大回撤·{label}"] = (part / part.cummax() - 1).min() if n > 0 else np.nan
    return out


def calendar_returns(curves: dict[str, pd.Series]) -> pd.DataFrame:
    rows = []
    for name, eq in curves.items():
        yearly = eq.groupby(eq.index.year).last()
        start = pd.Series([eq.iloc[0]], index=[yearly.index[0] - 1])
        rets = pd.concat([start, yearly]).pct_change().dropna()
        rows.append({"组合": name} | {str(y) + ("(至今)" if y == eq.index[-1].year else ""): r for y, r in rets.items()})
    return pd.DataFrame(rows)


def run(closes: pd.DataFrame) -> dict:
    closes = closes.dropna(how="all")
    parts = plan_parts(closes)
    index = parts.index
    curves = {
        "现行方案（SMH 2400 + 加码仓 1600 + REGN/VRTX 各 1200 + 现金 1600）": parts.sum(axis=1),
        "不要加码仓（SMH 4000 + REGN/VRTX 各 1200 + 现金 1600）":
            hold(closes["SMH"], 4000.0, index) + parts["REGN"] + parts["VRTX"] + CASH,
        "8000 全买 SMH": hold(closes["SMH"], TOTAL, index),
        "8000 全买 QQQ": hold(closes["QQQ"], TOTAL, index),
    }
    summary = pd.DataFrame([{"组合": name} | stats(eq) for name, eq in curves.items()])
    start_value = parts.iloc[0]
    gain = parts.iloc[-1] - start_value
    contribution = pd.DataFrame({
        "部分": list(PARTS), "投入": [start_value[p] if p != "加码仓（规则 A）" else OVERLAY for p in PARTS],
        "现在": [parts[p].iloc[-1] for p in PARTS],
        "这部分自己的年化": [stats(parts[p])["年化收益"] if p != "现金" else 0.0 for p in PARTS],
        "占总盈利": [gain[p] / gain.sum() for p in PARTS],
    })
    return {"summary": summary, "calendar": calendar_returns(curves), "contribution": contribution,
            "data_end": index[-1], "start": index[0]}


PERCENT = {"年化收益", "年化波动", "最大回撤", "最差一天", "年化·2016-22", "年化·2023后", "最大回撤·2016-22",
           "最大回撤·2023后", "这部分自己的年化", "占总盈利"}
MONEY = {"期末金额", "投入", "现在"}


def _render(table: pd.DataFrame) -> str:
    table = table.copy()
    for column in table.columns:
        if table[column].dtype.kind != "f":
            continue
        fmt = ((lambda x: f"{x:,.0f}") if column in MONEY else (lambda x: f"{x:.2f}") if column == "Sharpe" else
               (lambda x: f"{x:.1%}"))
        table[column] = table[column].map(lambda x, f=fmt: "" if pd.isna(x) else f(x))
    header = "| " + " | ".join(map(str, table.columns)) + " |"
    body = ["| " + " | ".join(map(str, row)) + " |" for row in table.itertuples(index=False)]
    return "\n".join([header, "|" + "---|" * len(table.columns), *body])


def write_report(results: dict, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    for name in ["summary", "calendar", "contribution"]:
        results[name].to_csv(out / f"{name}.csv", index=False)
    risk = ["组合", "期末金额", "年化收益", "年化波动", "Sharpe", "最大回撤", "最差一天"]
    split = ["组合", "年化·2016-22", "最大回撤·2016-22", "年化·2023后", "最大回撤·2023后"]
    sections = [
        f"# 整个账户回测（{results['start']:%Y-%m-%d} 到 {results['data_end']:%Y-%m-%d}，本金 8000）\n\n"
        "由 `python -m riskeval.plan_backtest` 生成，设定见该模块说明。现金不计利息，已扣成本。"
        "16 只半导体和 REGN、VRTX 都是按今天挑的，2016–2026 又是半导体大牛市，数字偏乐观。规则输出加历史回测，不是投资建议。",
        "## 总体\n\n" + _render(results["summary"][risk]),
        "## 分段\n\n" + _render(results["summary"][split]),
        "## 每年的收益\n\n" + _render(results["calendar"]),
        "## 现行方案里各部分的贡献\n\n" + _render(results["contribution"]),
    ]
    (out / "README.md").write_text("\n\n".join(sections) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> None:
    from riskeval import daily_data

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--start", default="2015-01-01")
    parser.add_argument("--out", default="reports/plan_backtest")
    args = parser.parse_args(argv)

    semis = [t for ts in TARGETS.values() for t in ts]
    closes = daily_data.download_closes(semis + ["SMH", "QQQ", "REGN", "VRTX"], args.start, chunk=50)
    results = run(closes)
    write_report(results, Path(args.out))
    print(f"已写入 {args.out}/README.md")


if __name__ == "__main__":
    main()
