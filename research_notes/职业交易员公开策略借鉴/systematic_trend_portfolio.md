# Systematic trend followers and rules-based stock momentum managers: rules, evidence, and lessons for a small single-sector portfolio

Labels used throughout:
- **[RULE]** = a rule as published or described.
- **[SELF]** = performance the author reported for their own method, in-sample or marketing.
- **[INDEP]** = a third-party replication or out-of-sample check.
- **[ACAD]** = academic or peer-reviewed work.
- **[UNVERIFIED]** = from a secondary blog or vendor page whose method I could not check.

Research constraint: WebFetch and direct downloads were blocked in this session (DNS failures and proxy 403 on allocatesmartly.com, quantconnect.com, concretumgroup.com, typepad.com and others). Every finding below therefore comes from search-engine summaries of the cited pages, not from reading full texts. Treat exact numbers as needing a check against the primary document before you rely on them.

## 1. Turtle Traders (Dennis / Faith / original rules): rules and what testing shows

### Takeaway
The Turtle system is an ATR ("N") risk-budgeting framework built on Donchian breakouts. The part most worth borrowing for a small stock portfolio is its correlated-group unit caps and ATR sizing, not the breakout trigger itself. The published Turtle-era results are futures backtests ending in 2006. I found no rigorous, independent, survivorship-free test of the full Turtle rules on US single stocks in recent decades. The closest independent stock evidence is the Wilcox/Crittenden and Zarattini/Pagani/Wilcox all-time-high plus ATR-trailing-stop studies in section 6.

### Cited Findings
- [RULE] Sizing: unit = 1% of account equity / (N × dollar value per point). N is the 20-day ATR (Wilder smoothing), so 1N of adverse move costs about 1% of equity in any instrument — [theturtletrader.com](https://www.theturtletrader.com/turtle-trading-rules/); [easytradeweb.com](https://www.easytradeweb.com/en/turtle-trading-strategy-rules/)
- [RULE] Stops: 2N from entry. Pyramiding: add a unit every ½N of favorable move, up to 4 units per market — [theturtletrader.com](https://www.theturtletrader.com/turtle-trading-rules/); [takeprofitapp.com](https://takeprofitapp.com/en/learn/turtle-trading-system)
  - Sources disagree on stop handling after adds. One says the stops on earlier units rise by ½N; another says all stops move to 2N below the latest entry — [myplaniq.com](https://www.myplaniq.com/LTISystem/jsp/strategy/View.action?ID=330&action=view) vs [takeprofitapp.com](https://takeprofitapp.com/en/learn/turtle-trading-system)
- [RULE] Unit caps:
  - 4 units in a single market
  - 6 units in closely correlated markets (example: heating oil and crude)
  - 10 units in loosely correlated markets
  - 12 units in one direction overall

  Some sources read the 6-unit cap as "closely correlated markets *in one direction*" — [theturtletrader.com](https://www.theturtletrader.com/turtle-trading-rules/); [MQL5 article](https://www.mql5.com/en/articles/23448)
- [RULE] System 1 enters on a 20-day breakout and System 2 on a 55-day breakout (Donchian channels) — [TradingView open-source implementation](https://il.tradingview.com/script/Zwdj5FDq-Turtle-Trading-System-Not-Financial-Advise); [IG](https://www.ig.com/sg/trading-strategies/turtle-trading--what-is-it-and-what-are-the-rules--180904)
- [RULE] IG notes that the system is built to exploit trending markets and can have sustained drawdowns in range-bound markets — [IG](https://www.ig.com/sg/trading-strategies/turtle-trading--what-is-it-and-what-are-the-rules--180904)
- [SELF/IN-SAMPLE] *Way of the Turtle* (Curtis Faith) futures backtests over 1996–2006, risking 0.5% of equity per trade, as tabulated by QuantifiedStrategies:
  - "Donchian Trend": about 29.4% CAGR, 36.7% max drawdown
  - Donchian Trend with time exit: about 57.2% CAGR, 43.6% max drawdown
  - ATR-channel and Bollinger variants: about 49.5% and 51.8% CAGR

  The trend filter is a 25-day average above a 350-day average, with entry on a 20-day breakout. Sources disagree on whether the averages are EMA or SMA — [QuantifiedStrategies](https://www.quantifiedstrategies.com/trend-following-trading-strategy/); [Rayner Teo hosted PDF](https://tradingwithrayner.com/wp-content/uploads/2014/11/turtle-strategy-revised.pdf)
  - Caveats: these are futures, not stocks, and the window ends in 2006. I found no post-2006 out-of-sample test with the same rules.
- [INDEP, weak] QuantifiedStrategies says trend following "still works". However, its test is a simple monthly momentum rule on continuous futures from 2007 onward, not the full Turtle system, and its claim that returns are lower than in the 1980s is asserted rather than measured — [QuantifiedStrategies substack](https://quantifiedstrategies.substack.com/p/turtle-trading-strategies-rules-statistics)
- [UNVERIFIED, anecdotal] A forum user testing Turtle-style rules on FX reported that only about 3–4 of every 10 trades win, and that results are poor in whipsaw markets — [EliteTrader](https://www.elitetrader.com/et/threads/turtle-trading-thoughts.229820/post-3343821)
- [INDEP] Jerry Parker, an original Turtle, now runs Chesapeake Capital:
  - The program trades 100+ markets with small positions in each; elsewhere he says it went from about 25 markets to over 300 — [The Hedge Fund Journal](https://thehedgefundjournal.com/trend-following-diversifies-and-mitigates-risk/); [tradelikeanengineer (Swanscott interview summary)](https://tradelikeanengineer.com/blogs/trading-podcasts/andrew-swanscott-interview-with-jerry-parker)
  - He has traded single stocks since the 1990s but not stock indices — [The Hedge Fund Journal](https://thehedgefundjournal.com/chesapeake-capitals-jerry-parker/)
  - In other words, the surviving Turtle evolved toward *many* markets, not toward concentration.

### Inferences
- The Turtle edge depended on breadth: dozens of uncorrelated futures, each risked at about 1% per N. The unit caps exist because correlated markets break out together. On a 3-stock semiconductor book every breakout is effectively the same signal, so the 4/6/10/12 structure collapses to "one market".
- Illustrative arithmetic for an 8,000 account (assumed numbers, not data):
  - At 1% risk per N, 1N costs $80.
  - For a $180 stock with an assumed ATR of $4.50 (2.5%), one unit is 80/4.5 ≈ 17 shares ≈ $3,060, or about 38% of the account. A 2N stop costs about $160, or 2%.
  - Two units in one name, or one unit in each of NVDA, TSM and MU, would already exceed 100% of capital. So for a small cash account the binding constraint is capital, not the Turtle risk caps.
- The most transferable Turtle idea is to treat NVDA, TSM and MU as one "closely correlated group" with one group risk cap. For example, cap *total* group risk at roughly the risk you would accept in a single market, instead of risking 1% in each name.

### Gaps
- I could not open the original Turtle rules PDF or *Way of the Turtle* (fetches blocked). That means I could not confirm:
  - the drawdown rule, often described as cutting the notional account size after each 10% drawdown (not confirmed here, so it is omitted as a fact)
  - the exact System 1 "skip after winner" filter
  - the exit channels (10- and 20-day)
- I found no peer-reviewed or survivorship-free test of 20/55-day Donchian breakout plus 2N stops on US single stocks after 2006.

## 2. Andreas Clenow, *Stocks on the Move*: rules, results, replications

### Takeaway
Clenow's rules are:
- rank S&P 500 stocks by annualized 90-day exponential-regression slope × R²
- buy only when the index is above its 200-day average
- skip stocks below their 100-day average or with a recent gap of more than 15%
- size by 0.1% equity risk per 20-day ATR
- trade weekly

Third-party replications vary widely, from roughly double the S&P 500 return over 1999–2014 to *trailing* the S&P 500 in a shorter Python test. I could not verify the book's own figures. The method is designed for a diversified basket of about 20–30 stocks across sectors, so it does not map directly onto a concentrated semiconductor portfolio.

### Cited Findings
- [RULE] Momentum score: annualized exponential regression slope over the past 90 days × R² (coefficient of determination) — [search summary of thechartist.com.au, teddykoker.com and others](https://teddykoker.com/2019/05/momentum-strategy-from-stocks-on-the-move-in-python/)
- [RULE] Position size: 0.1% of portfolio equity divided by the 20-day ATR. One QuantConnect user cites ATR100 instead, which appears to be that user's variant, not the book's rule — [teddykoker.com](https://teddykoker.com/2019/05/momentum-strategy-from-stocks-on-the-move-in-python/); [QuantConnect thread 3136](https://www.quantconnect.com/forum/discussion/3136/Andreas+F+Clenow+Momentum)
- [RULE] Filters:
  - Trade on Wednesdays (weekly).
  - Open new positions only if SPY is above its 200-day SMA.
  - The stock must be above its 100-day SMA.
  - Exclude stocks with a gap above 15%.
  - Exit when a stock drops out of the top ranks or falls below its 100-day average.

  — [QuantConnect thread 3136](https://www.quantconnect.com/forum/discussion/3136/andreas-f-clenow-momentum/p1); [QuantConnect thread 16578](https://www.quantconnect.com/forum/discussion/16578/quot-stocks-on-the-move-quot-momentum-strategy-by-cabedovestment/)
- [INDEP, attribution uncertain] One comparison table covering 1999–2014 shows about 12.3% a year and −24% max drawdown for the Clenow-style strategy, versus about 5.2% a year and −55% for the S&P 500. The table is internally inconsistent: it shows both −24.0% and −23.5% for the strategy. The source sits among the search results for [The Chartist](https://www.thechartist.com.au/momentum-investing/), but I could not confirm which page it came from.
- [INDEP] A Python/Backtrader re-implementation reported about 8.99% annual return and 11.71% max drawdown, against roughly 12% CAGR and 13.5% drawdown for the S&P 500 over the same (short, recent) window. In other words, it *lagged* the index with similar drawdown — [Teddy Koker 2019](https://teddykoker.com/2019/05/momentum-strategy-from-stocks-on-the-move-in-python/)
- [INDEP] Other replications exist but I could not read their statistics:
  - a test on the Nifty 500 — [utkaldesai blog](https://utkaldesai.wordpress.com/2020/05/14/backtesting-andreas-clenows-stocks-on-the-move-on-nifty-500/)
  - a "How (Not) to Invest" critique — [chrischow](https://chrischow.github.io/dataandstuff/2018-11-10-how-not-to-invest-clenow-momentum/)
  - a live portfolio tracker — [TuringTrader](https://www.turingtrader.com/portfolios/clenow-stocks-on-the-move/)
- [INDEP, not faithful] A QuantConnect backtest reports 14.92% CAGR, 17.9% max drawdown and Sharpe 1.085 from about 2008. It used a fixed ETF list (QuantConnect cached backtest: QQQ, FDN, XLP, TLH, TLT) rather than the S&P 500 universe, so it is not a replication — [QuantConnect backtest](https://www.quantconnect.com/terminal/cache/embedded_backtest_305e8728b6090b0e5ceb1a1f742b8534.html)

### Inferences
- Clenow's 0.1%-per-ATR sizing implies weight ≈ 0.1% / (ATR as a % of price).
  - For a semiconductor stock with ATR around 3–4% of price, that is about a 2.5–3.3% weight per name, so you need 30 or more names to be fully invested.
  - The design assumes broad cross-sector breadth. Applied to 3–5 correlated semiconductor names it would leave most capital in cash, or require scaling the risk factor up 10×, which removes the diversification logic.
- The portable pieces for this project are:
  - the index regime filter (no *new* buys when SPY or QQQ is below its 200-day average)
  - the "below 100-day average → exit" rule
  - the gap filter, which avoids names whose trend came from one earnings or news jump; this is relevant to MU and NVDA earnings gaps
  - the regression-slope × R² score, which rewards *smooth* trends and is a cleaner tie-breaker among correlated semiconductor names than raw return
- The project found that the Kova-like RS plus trend-template filter "added little" in the past year. That is consistent with these replications: cross-sectional ranking adds the most when the universe is broad and dispersion is high. Within one sector, dispersion is low and ranks change mostly on noise.

### Gaps
- I could not confirm the book's own reported CAGR and drawdown, its exact rebalancing cadence for position sizes (often described as twice monthly), or the top-20% rank cutoff (fetches blocked).
- I found no independent post-2015 (post-publication) out-of-sample study with a survivorship-free S&P 500 membership history.

## 3. Antonacci Dual Momentum (GEM) and Faber rotation: performance after publication

### Takeaway
GEM's in-sample record (1974–2013) was very strong. After publication (book 2014), several independent replications find it *lagged* buy-and-hold S&P 500 on return while keeping a smaller maximum drawdown, and most of that drawdown edge came from 2008. Results are highly sensitive to the lookback length. Faber's 10-month moving-average timing beat the market in 2008–09 and then underperformed stocks in 6 of the next 8 years. One independent replication of his sector-rotation paper could not reproduce outperformance.

### Cited Findings
- [SELF/IN-SAMPLE] GEM (gross, monthly rebalancing) returned 17.43% a year over 1974–2013, versus 9.55% for buy-and-hold ACWI, with lower volatility — [CXO Advisory](https://cxoadvisory.com/momentum-investing/a-few-notes-on-dual-momentum-investing)
- [RULE] GEM uses relative momentum (US vs. international equities over a 12-month lookback) plus absolute momentum (the winner must beat T-bills, otherwise hold bonds), with monthly rebalancing — [CXO Advisory](https://cxoadvisory.com/momentum-investing/a-few-notes-on-dual-momentum-investing); [Antonacci on Medium](https://medium.com/@garyantonacci_30463/extended-backtest-of-global-equities-momentum-dual-momentum-eb12902612e0)
- [INDEP] Quant for Free compared 2008–2026 results:

  | Strategy | CAGR | Max drawdown |
  |---|---|---|
  | GEM | 9.1% | −20% |
  | SPY buy-and-hold | 11.6% | −42% |

  It says GEM lagged even a plain 60/40 out of sample, and that "its drawdown edge was mostly a 2008 story" — [Quant for Free](https://quant4free.com/analysis/dual-momentum/)
- [INDEP] Marius Petit (SSRN, 2026), replicating 1971–2026: GEM has underperformed a passive index by about 4.8 percentage points a year since 2010, and its deepest drawdown in 55 years came in 2021–2023 while it held the defensive asset — [SSRN 7427878](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7427878)
- [INDEP] ReSolve found that over 2009–2018, GEM with a 10-month lookback returned 146% in total, versus 43% with a 9-month lookback. That is extreme parameter fragility — [ReSolve, "A Craftsman's Perspective"](https://investresolve.com/inc/uploads/pdf/global-equity-momentum-a-craftsmans-perspective.pdf)
- [SELF] Antonacci attributes the lag to occasional whipsaws and late entries or exits at turning points. In a 2018 case study, the 12-month lookback stayed invested through the late-2018 drawdown — [Optimal Momentum](https://www.optimalmomentum.com/whither-fragility-dual-momentum-gem/)
- [RULE + SELF/IN-SAMPLE] Faber's 2007 tactical asset allocation model: hold each of 5 asset classes (US stocks, foreign stocks, bonds, REITs, commodities) only when it is above its 10-month SMA, otherwise cash, equal weight, monthly. It was tested on US equities from 1900 — [Quantpedia](https://quantpedia.com/strategies/asset-class-trend-following); [CXO](https://www.cxoadvisory.com/technical-trading/long-term-outperformance-from-trends-defined-by-moving-averages)
- [SELF, out-of-sample 2018 update in JPM] Faber's 10-year follow-up: the timing system "outperformed by a significant amount during the 2008–2009 bear market, [then] went on to underperform stocks six of the next eight years." Swedroe reports a Sharpe "improvement from 0.45 to 0.80", but it is unclear whether that compares buy-and-hold vs. timing or in- vs. out-of-sample — [ETF.com / Swedroe](https://www.etf.com/sections/index-investor-corner/swedroe-why-financial-trends-persist); [paper PDF](https://allocatortraining.com/wp-content/uploads/2023/06/A-Quantitative-Approach-to-Tactical-Asset-Allocation.pdf)
- [SELF/IN-SAMPLE] Faber's sector/industry relative-strength paper, using data from the 1920s, found that simple momentum beat buy-and-hold about 70% of the time — [StockCharts ChartSchool](https://chartschool.stockcharts.com/table-of-contents/trading-strategies-and-models/trading-strategies/fabers-sector-rotation-trading-strategy)
- [INDEP, anecdotal] A Portfolio123 user replicating Faber's relative-strength strategies was "unable to show ANY outperformance over the S&P 500… at best match", even before 2010 — [Portfolio123 community](https://community.portfolio123.com/t/replicating-meb-fabers-relative-strength-strategies-for-investing/61878)
- [INDEP] Allocate Smartly notes that "it's very hard to predict what specific set of parameters is going to outperform out of sample" — [Allocate Smartly, Trinity Lite](https://allocatesmartly.com/meb-fabers-trinity-portfolio-lite/)

### Inferences
- The pattern after publication is consistent:
  - absolute-momentum or MA regime filters reliably cut deep drawdowns in long bear markets (2000–02, 2008)
  - they cost return in V-shaped or choppy markets (2010s, 2018, 2020, 2022–23)
  - over 2010–2026 they mostly lagged buy-and-hold equities

  This matches the project's own result: a lower-volatility, lower-drawdown rule did not beat buy-and-hold over 2016–2026.
- Lookback fragility (10 vs. 9 months: 146% vs. 43%) means any single-parameter regime filter in this project should be tested across a band of lookbacks (e.g., 150–250 days), and possibly averaged across them, rather than fixed at 200.

### Gaps
- I could not read Allocate Smartly's GEM page (blocked), which would give a standardized post-2014 record including trading-day sensitivity.
- I found no independent out-of-sample test of Faber's *sector* rotation published after 2013 with disclosed methods.

## 4. Parker, Basso, Seykota, Tharp: position sizing, risk per trade, portfolio heat

### Takeaway
The public, testable rules are:
- size each position by volatility (ATR) so that each one carries a small, fixed fraction of equity at risk, about 0.5–1% (Basso: half of 1% per futures position)
- budget risk by asset class or correlated group rather than by position count (Parker: 25% of risk budget to each of 4 asset classes)
- measure each trade in R-multiples of its initial risk (Tharp)

I found no primary-source figures for Seykota's risk per trade, or for any professional's "portfolio heat" cap.

### Cited Findings
- [SELF, primary transcript] Tom Basso says he got down to half of 1% of total equity in any one futures position — [ReSolve podcast transcript (PDF)](https://investresolve.com/inc/uploads/pdf/tom-basso-podcast-transcript.pdf)
- [UNVERIFIED secondary] Other descriptions of Basso's method, all from secondary sources:
  - Position size = equity × allocated volatility % ÷ dollar ATR (example 0.75%).
  - Compute both a risk-based size and a volatility-based size and take the smaller.
  - Cut risk per trade by 50% at a 5% equity drawdown and by 75% at a 10% drawdown.
  - Cap total open "heat" at 6–12%.

  — [tradingmomentum substack](https://tradingmomentum.substack.com/p/the-art-and-science-of-position-sizing); [tradermarkus review](https://tradermarkus.com/tom-basso-successful-traders-size-their-positions-review/); [paperswithbacktest](https://paperswithbacktest.com/strategies/tom-basso)

  The heat cap and drawdown-scaling numbers are not traced to a Basso primary source.
- [SELF] Jerry Parker:
  - allocates 25% of his risk budget to each of currencies, commodities, stocks and interest rates
  - "there is a lot of overlap in correlations, so there are probably only about 50 unique drivers of returns" across 300+ markets
  - aims to hold winners for 6–12 months and accepts 30%+ drawdowns on a single trade
  - runs the Blueprint Chesapeake Multi-Asset Trend ETF (TFPN)

  — [tradelikeanengineer (interview summary)](https://tradelikeanengineer.com/blogs/trading-podcasts/andrew-swanscott-interview-with-jerry-parker); [Blueprint](https://blueprintip.com/headlines/plan-the-trade-and-trade-the-plan-with-jerry-parker/); [Better System Trader panel](https://robuxio.com/education/interviews/bst-trading-panel-10-jerry-parker)
- [RULE] Van Tharp:
  - Each trade's P&L is expressed as an R-multiple of its initial risk; expectancy is the mean R.
  - System Quality Number: SQN = √n × mean(R) / stdev(R), with n often capped at 100 when comparing systems.
  - R-multiples require a defined initial stop.
  - Rough secondary grading bands: below 2 is below average, 2–2.5 average, 2.5–3 good, 3–5 excellent.

  — [TradesViz glossary](https://www.tradesviz.com/glossary/system-quality-number/); [LuxAlgo](https://www.luxalgo.com/library/concept/sqn/); [NexusFi](https://nexusfi.com/a/risk-management/system-quality-number-sqn)
- [INDEP/ACAD-adjacent] Zarattini/Pagani/Wilcox report trade quality in R units: average profit per trade fell from 0.39R before 2005 to 0.31R over 2005–2024. This is a concrete published expectancy benchmark for a stock trend system — [search summary of SSRN 5084316](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5084316)

### Inferences
- With 8,000 and 0.5–1% risk per position ($40–80), ATR stops on volatile semiconductor names imply positions of roughly $1,000–3,000. A fully invested 3-name book is therefore already near or above the risk an individual Turtle or Basso position would carry, and all three positions move together.
- Correlated-group budgeting à la Parker translates to a sector-level cap. For example, cap combined semiconductor open risk at about 1.5–2% of equity, however many names are held, and hold the rest of the exposure in QQQ or a non-semiconductor sleeve.
- The R-multiple log is directly testable in the project's backtests:
  - record initial stop distance for every trade
  - report mean R, R distribution, and SQN for mean-reversion entries vs. trend entries

  For comparison, the Zarattini et al. benchmark is about 0.3R per trade with very right-skewed outcomes.

### Gaps
- I found no primary-source quote of Ed Seykota's risk per trade or sizing formula in this session.
- I found no primary source for Parker's per-trade risk percentage, or for any practitioner's portfolio-heat cap.
- Basso's drawdown-scaling rule is from a secondary site only.

## 5. Correlation and concentration: how professionals cap correlated exposure, and implications for NVDA + TSM + MU

### Takeaway
Professionals cap exposure at the level of the *correlated group*, not the individual instrument:
- Turtles: 6 units for closely correlated markets vs. 4 for a single market
- Parker: risk budget per asset class, and about 50 independent drivers among 300+ markets
- Clenow: about 20–30 cross-sector names at 0.1% risk each

Holding NVDA, TSM and MU together is effectively a single, leveraged bet on the semiconductor factor, so it should be sized as one position. I found no reliable published correlation matrix for these names; the project should compute it.

### Cited Findings
- [RULE] Turtle caps of 4 units per market, 6 per closely correlated group, 10 per loosely correlated group and 12 per direction put a correlated group at only 1.5× a single market's maximum risk — [theturtletrader.com](https://www.theturtletrader.com/turtle-trading-rules/)
- [SELF] Parker: many small positions across 100–300+ markets; "about 50 unique drivers" because of correlation overlap — [The Hedge Fund Journal](https://thehedgefundjournal.com/trend-following-diversifies-and-mitigates-risk/); [tradelikeanengineer](https://tradelikeanengineer.com/blogs/trading-podcasts/andrew-swanscott-interview-with-jerry-parker)
- [DATA, secondary] Sector ETF concentration and volatility:
  - SMH holds about 30% combined in NVDA and TSMC, and a Motley Fool piece calls any single name above 20% a red flag — [Webull/Motley Fool](https://www.webull.com/news/15249996840969216)
  - SOXX's top 10 holdings were about 61.65% of the fund in one snapshot — [Equibles](https://equibles.com/etfs/soxx)
  - SOXX returned −45% in 2022 and +68% in 2023 — [wealthvieu](https://wealthvieu.com/investing/index-funds-etfs/semiconductor-etfs/)
- [UNVERIFIED, likely unreliable] A social-media post cited a 3-month NVDA–SOX correlation of 0.03, with TSM and MU "just below 0.90". It is an undated snapshot from one post, not reproducible, and should not be used — [search result, Webull news](https://www.webull.com/news/15257546374734848)
- [ACAD] Daniel & Moskowitz find that winner and loser betas diverge sharply after market declines: loser-decile beta above 3, winner beta below 0.5. Momentum portfolios built in one regime therefore carry hidden factor bets that unwind together — [Daniel & Moskowitz, Momentum Crashes](https://www.kentdaniel.net/papers/published/mom12.pdf)

### Inferences
- Practical translation for this portfolio:
  1. Define a "semiconductor group" (NVDA, TSM, MU, AMD, AVGO, SOXX/SMH) with one group risk budget, Turtle-style. Size each name so that the *sum* of their ATR-stop risks stays within that budget.
  2. When several names signal at once, take the best-ranked one or two (e.g., by Clenow slope × R²), not all of them, because extra names add correlated risk but little independent expectancy.
  3. Treat QQQ as partially overlapping. Semiconductors are a large share of Nasdaq-100 weight, so QQQ plus semiconductors is not full diversification either; quantify this with rolling 60/120-day correlations in the project's data.
- Diversification the professionals rely on (many uncorrelated markets) is largely unavailable to a single-sector, 8,000 portfolio. The realistic substitutes are cash, T-bills, or a bond ETF as the "absolute momentum" alternative, plus a broader index sleeve.

### Gaps
- I found no reliable, dated correlation matrix for NVDA, TSM, MU, AMD and SOXX. It should be computed from the project's own price data, e.g., rolling 60- and 252-day daily-return correlations.
- I found no practitioner document giving an explicit "sector cap %" for single-stock trend portfolios.

## 6. Regime filters (index above 200-day, breadth) and evidence on single-stock trend following

### Takeaway
The academic evidence on *market-state* conditioning comes from Daniel & Moskowitz, who use a volatility/forecast-based dynamic weighting rather than a 200-day moving average. They show momentum crashes cluster after market declines in high-volatility "panic" rebounds, and that dynamic scaling roughly doubles momentum's Sharpe. Support for a simple "index above 200-day" filter is mostly practitioner or self-reported: it cuts drawdowns but, after publication, typically costs return (see GEM and Faber).

The strongest independent evidence that trend following works on single US stocks comes from two studies with survivorship-free data:
- Wilcox & Crittenden (2005)
- Zarattini, Pagani & Wilcox (2025)

Their system buys all-time highs and exits on a wide ATR trailing stop. It works because fewer than 7% of trades deliver most of the profit, so cutting trades or capping winners destroys it.

### Cited Findings
- [ACAD] Daniel & Moskowitz:
  - Momentum crashes occur in "panic" states — after market declines, when volatility is high — and coincide with market rebounds.
  - A dynamic strategy based on forecasts of momentum's mean and variance "approximately doubles the alpha and Sharpe ratio" of static momentum, across periods, international markets and asset classes.

  — [SSRN 2486272](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2486272); [PDF](https://www.kentdaniel.net/papers/published/mom12.pdf)
- [UNVERIFIED practitioner] Claims that momentum traded only in index uptrends achieves similar returns with lower drawdowns (citing StockCharts / Robust Trader) — [Cracking Markets](https://www.crackingmarkets.com/us-stock-momentum-trading-system-for-retail-traders-deep-research/)
- [SELF, out-of-sample] Faber's 10-month SMA filter: large outperformance in 2008–09, then lagged stocks in 6 of 8 subsequent years — [ETF.com / Swedroe](https://www.etf.com/sections/index-investor-corner/swedroe-why-financial-trends-persist)
- [INDEP, 2005] Wilcox & Crittenden, "Does Trend Following Work on Stocks?":
  - Rules: buy at all-time highs, exit on an ATR-based trailing stop.
  - Data: 24,000+ NYSE/AMEX/NASDAQ securities including delisted ones, 1983–2004, 18,000+ trades.
  - Costs: 0.5% round-turn, with minimum-price and liquidity filters.
  - Results: positive expectancy and strong right skew.
  - A reviewer reported $1,000 growing to about $30,000 over the period.
  - Stops of 8–12 ATR tested in 0.5 steps showed no material difference.

  — [paper PDF (Penn mirror)](https://www.cis.upenn.edu/~mkearns/finread/trend.pdf); [oxfordstrat mirror](https://oxfordstrat.com/coasdfASD32/uploads/2016/03/Does-Trend-Following-Work-on-Stocks.pdf); [Daily Speculations review](https://dailyspeculations.com/vic/trend.html); [marketnull deep-dive](https://marketnull.substack.com/p/does-trend-following-still-work-on)
- [INDEP/working paper, 2025] Zarattini, Pagani & Wilcox, "Does Trend-Following Still Work on Stocks?":
  - Data: survivorship-free US stocks, 1950 to November 2024.
  - Entry: close at or above the highest adjusted close in the stock's history, then buy at the next open. Exit: ATR trailing stop that is never lowered. Positions are volatility-sized.
  - Profit concentration: fewer than 7% of trades generate the majority of profits, and this held out-of-sample over 2005–2024.
  - Long-only portfolio, 1991–2024: 15.19% CAGR and 6.18% annual alpha, *gross of fees*.
  - Trade quality declined modestly: average trade 0.39R before 2005 vs. 0.31R after.
  - Transaction costs are the main obstacle; a "turnover control" algorithm is said to keep it viable after costs.
  - One summary mentions a 42-day ATR in the stop formula (unverified).

  — [SSRN 5084316](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5084316); [Concretum summary](https://concretumgroup.substack.com/p/does-trend-following-still-work-on); [Harbourfront Quant](https://harbourfrontquant.substack.com/p/does-trend-following-still-work-on); [Quantpedia](https://quantpedia.com/strategies/trend-following-effect-in-stocks)
- [ACAD] Time-series momentum:
  - Moskowitz, Ooi & Pedersen (2012): an asset's own past 12-month return predicts its return over about the next year, after which it partially reverses. The effect was positive for all 58 futures and forward contracts tested; the sample excludes single stocks — [TSMOM paper](https://w4.stern.nyu.edu/facdir/lpederse/papers/TimeSeriesMomentum.pdf)
  - Lim, Wang & Yao (2018, *Journal of Banking & Finance*): strong time-series momentum in *individual* US stocks over 1927–2017. It holds across subperiods and firm sizes, varies with market state, and dual-momentum variants earn more — [Univ. of Melbourne listing](https://findanexpert.unimelb.edu.au/scholarlywork/1355921-time-series-momentum-in-nearly-100-years-of-stock-returns)
  - The earlier working-paper version (1927–2014) reports: value-weighted TSMOM about 0.55% a month gross vs. 1.30% for cross-sectional; three-factor alpha about 0.70% a month; dual momentum about 1.88% a month; TSMOM avoided January losses and momentum crashes — [CXO Advisory](https://www.cxoadvisory.com/momentum-investing/time-series-and-dual-momentum-for-individual-stocks/); [Manchester listing](https://research.manchester.ac.uk/en/publications/the-enduring-effect-of-time-series-momentum-on-stock-returns-over/)

### Inferences
- For a small semiconductor portfolio, the published evidence favors **trend-holding** rules over **buy-the-dip** rules for capturing the right tail:
  - all-time-high or 52-week-high entries
  - very wide ATR trailing stops (8–12 ATR in the 2005 study)
  - volatility sizing

  The project's mean-reversion rule (buy below the lower Bollinger band while above the 200-day) reduced drawdown but missed upside. That fits the finding that most profits come from fewer than 7% of trades, i.e., from staying in big winners.
- Regime filters: use the index-above-200-day rule as a *new-entry gate* (Clenow style), not as a forced liquidation trigger, and test it across lookbacks. Daniel & Moskowitz suggest the larger risk is the *post-crash rebound* period. A volatility-scaled exposure, cutting size when realized volatility is high, is a better-supported alternative to a binary MA switch.
- Caveat on decay and survivorship:
  - The single-stock trend results come from broad universes of thousands of names, which is a different setting from a 3-name portfolio.
  - Picking semiconductor names *today*, after their 2016–2026 run, introduces hindsight and survivorship bias into any backtest of this project.
  - Average R per trade fell after publication (0.39R to 0.31R), and GEM and Faber lagged after publication. Expect lower forward edge than in-sample backtests show.

### Gaps
- I found no academic test of a simple "S&P 500 above 200-day SMA" gate applied to stock-momentum portfolios. Evidence for it is practitioner-only.
- I found no independent evidence on breadth-based regime filters (e.g., % of stocks above their 200-day) with disclosed methods in this session.
- I could not access the Zarattini et al. PDF to confirm the exact stop formula, the per-trade risk constant, net-of-cost CAGR, or max drawdown.
