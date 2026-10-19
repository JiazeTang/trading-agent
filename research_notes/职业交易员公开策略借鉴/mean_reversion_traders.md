# Professional short-term mean-reversion and swing traders: public rules and independent evidence (职业交易员短线均值回归策略：公开规则与独立证据)

Research date: 2026-10-19. Scope: Connors/Alvarez, Raschke, Larry Williams, brief notes on other systematic practitioners, practitioner refinements relevant to the project's rule (close < 20-day lower Bollinger band, z ≤ -2, stock > 200-day MA), and evidence of decay in 2020–2026.

**Method note (read first):** The network policy blocked direct page fetches for nearly every source (substack, alvarezquanttrading.com, quantifiedstrategies.com, statoasis.com, bettersystemtrader.com, marginofpain.com all returned DNS or proxy 403 errors). Every finding below therefore comes from **search-engine excerpts** of the cited pages, not from reading the full pages. Numbers are quoted as the excerpts gave them. Before relying on a number, open the source page. Labels used throughout:
- **[STATED RULE]**: the author's published rule
- **[SELF-REPORTED]**: the author's or vendor's own performance claim
- **[INDEPENDENT]**: a third-party replication or test
- **[VENDOR]**: the source sells strategies, courses or software, so treat it as marketing-adjacent
- **[UNOFFICIAL COPY]**: an excerpt from a pirated or unofficial copy of a book

---

## 1. Larry Connors and Cesar Alvarez: RSI(2), ConnorsRSI, "Short Term Trading Strategies That Work", scaling in, stops, published win rates, and post-publication decay

### Takeaway
Connors-style rules (buy above the 200-day MA when the 2-period RSI is deeply oversold, exit on strength such as a close above the 5-day MA) had a real historical edge in US index ETFs and liquid stocks. Independent post-publication tests show the edge **shrank, by about a third to four-fifths depending on the measure, but did not vanish**. After the book, RSI(2) on SPY no longer beat buy-and-hold on a risk-adjusted basis. Win rates near 75–80% hold up better than returns do, and that matches the project's finding that a high win rate alone says little.

### Cited Findings
**Rules [STATED RULE]**
- Standard RSI(2) rule: go long when RSI(2) drops below 10 (below 5 for stricter entries) while price is above the 200-day SMA, and exit when price closes above the 5-day SMA. The rule comes from Connors & Alvarez, *Short Term Trading Strategies That Work* (2008), tested on US index and ETF data. — [LuxAlgo RSI-2 concept page](https://www.luxalgo.com/library/concept/rsi-2/); [StockCharts ChartSchool RSI(2)](https://chartschool.stockcharts.com/table-of-contents/trading-strategies-and-models/trading-strategies/rsi-2)
- Book rule "Rule 5 – Stops Hurt": "the tighter your stops, the less money you will make. The wider your stops, the better." A stop-test table in the book shows the **no-stop row with the highest average return and win rate (about 0.58% per trade, about 69.81% winners)**. Stop rows were lower, but the excerpt is truncated and its column labels are unclear. The book's S&P 500 analysis covers 1995-01-01 to 2007-12-31. — [UNOFFICIAL COPY] [pdfcoffee excerpt of the book](https://pdfcoffee.com/short-term-trading-strategies-that-work-by-larry-connors-and-cesar-alvarez-pdf-free.html)
- **R3 strategy** (Connors & Alvarez, *High Probability ETF Trading*, 2009): above the 200-day SMA, and RSI(2) has declined for three consecutive days with the first drop starting from above 60. The book reportedly studied ">1,000 signals", with performance described as consistent across ETFs and large caps. No win rate appeared in the excerpt. — [TradingView community script citing the book](https://it.tradingview.com/script/QJSXeJnv); [WH SelfInvest R3 description](https://www.whselfinvest.com/en-lu/trading-platform/free-trading-strategies/tradingsystem/81-r3-larry-connors)
- **TPS (scaling in, "Time-Price-Scale")**: trade only when the S&P 500 ETF is above its 200-day MA. Open **10%** of the full position when RSI(2) < 25 for two days in a row, then add **20%, 30% and 40%** on each further lower close. Exit on the close when RSI(2) > 70. — [TuringTrader Connors TPS](https://www.turingtrader.com/portfolios/connors-tps/); [QuantifiedStrategies TPS](https://www.quantifiedstrategies.com/tps-trading-strategy/) [VENDOR]. No verified TPS win rate was found. One forum guess of "70% range" is unsourced — [Wealth-Lab forum](https://wl6.wealth-lab.com/Forum/Posts/Connors-TPS-Strategy-40197)
- **ConnorsRSI (CRSI(3,2,100))** = the average of RSI(3) of price, RSI(2) of the up/down streak length, and the 100-day percent rank of the 1-day return. An unchanged close resets the streak to 0. — [TA-Lib CRSI](https://ta-lib.org/functions/crsi.html). Connors' stock rules used liquidity filters of **price > $5 and average daily volume > 500,000 shares**. — [Concretum Research on X](https://x.com/ConcretumR/status/1879572346362593308)
- TradingMarkets (Connors' firm) ETF variant: ConnorsRSI < 10 entry, exit when CRSI > 60. The setup "occurred 873 times since 2006", but no win rate appeared in the excerpt. — [VENDOR] [TradingMarkets](https://tradingmarkets.com/etfs/how-to-trade-etfs-with-connorsrsi-1583071)

**Published or self-reported statistics**
- Connors' own CRSI study of US stocks, 1990–2014: when CRSI < 10, the average next-week return was about **+1.25%**; when CRSI > 90, about **-0.50%**. — [SELF-REPORTED, as quoted by Concretum](https://x.com/ConcretumR/status/1879572346362593308)
- QuantifiedStrategies RSI(2) on SPY: **76% win rate**. — [VENDOR] [QuantifiedStrategies RSI-2](https://www.quantifiedstrategies.com/rsi-2-strategy/)
- QuantifiedStrategies RSI variant on QQQ with an extra filter: **CAGR 12.75% vs 6.4% buy-and-hold, 196 trades, 75% winners, max drawdown 19.5%**. The excerpt did not give the sample period or say whether the rule was optimised in-sample. — [VENDOR] [QuantifiedStrategies Substack, QQQ RSI](https://quantifiedstrategies.substack.com/p/rsi-mean-reversion-trading-strategy)

**Independent replications and decay [INDEPENDENT]**
- **SPY 1993–2026, split at the book's publication**: Sharpe **0.97 before the book, 0.68 after**, against **0.87 for buy-and-hold** after publication. Before publication there were 116 trades with **81% winners**. The edge per trade is "about a third smaller but still positive". SPY was "the best of the six [indices] by a distance", so SPY's results may flatter the rule. — [EmpiricaLab Substack](https://empiricalab.substack.com/p/connors-rsi2-spy)
- **SPY, 26 years, classic RSI(2) with a 200-day filter**: **181 trades (about 7 a year), 82% win rate**. Drawdown was lower than buy-and-hold, but total return was lower too. — [GuruFinanceInsights Substack](https://gurufinanceinsights.substack.com/p/i-backtested-the-classic-rsi2-mean)
- **StatOasis, SPY/QQQ/IWM/DIA through June 2026**: RSI(2) on SPY gave a **59.1% win rate at a fixed 5-bar hold and 65.1% at a 10-bar hold**. StatOasis **could not reproduce** a widely quoted ~90% win rate for RSI(5) on SPY. Only **53.8% of ConnorsRSI parameter variants were profitable**. The best robust variants (Connors RSI and Z-score RSI) came from **QQQ**, not SPY. — [StatOasis Better-RSI Showdown](https://statoasis.com/overfit/research/better-rsi-backtest)
- **Noise floor**: optimising 384 RSI mean-reversion variants over 3 years of shuffled, drift-free SPY produced a **median best Sharpe of 1.17 from pure noise**. — [StatOasis robustness study](https://statoasis.com/overfit/research/why-most-traders-fail-the-missing-piece-called-robustness-testing)
- **Concretum Research, out-of-sample CRSI on US stocks 1990–2025 (Norgate data, same liquidity filters)**: the next-week return when CRSI < 5 fell from **about +1.5% in 1990–2000 to about +0.3% in 2015–2025**. The return when CRSI > 95 moved from about -0.7% to about -0.5%. Concretum's verdict: the edge is "smaller but not gone". — [Concretum Research on X](https://x.com/ConcretumR/status/1879572346362593308?lang=en)
- Alvarez's own ConnorsRSI(3,2,100) analysis found **near-zero average P/L in 2014 and 2015** for a 5-day hold. — [Alvarez Quant Trading, ConnorsRSI Analysis](https://alvarezquanttrading.com/blog/connorsrsi-analysis/)
- Pre-sample test: a trade2win user found that for **1965–1995** the RSI(2) rule had a **66% win rate but lost money overall**. The edge was not present in earlier decades. — [trade2win thread](https://www.trade2win.com/threads/backtest-results-for-connors-rsi2-strategy.242688/)
- RSI(2) pullback across **about 150 S&P 500 names as a basket**: profit factor **1.57**, but **per-ticker results varied widely**. The poster framed it as a basket strategy, not a single-stock one. — [Elite Trader thread](https://www.elitetrader.com/et/threads/backtested-a-mean-reversion-rsi-2-pullback-strategy-on-150-s-p500-names.390710/)
- General decay: a study of published systematic strategies found post-publication Sharpe decay has "increased substantially over time, especially since 2000". — [arXiv 2105.01380, Why and how systematic strategies decay](https://arxiv.org/pdf/2105.01380)

**Alvarez on stops and exits (practitioner, partly [SELF-REPORTED])**
- Alvarez found that **making stops wider improved results, and removing them improved results further**, because big mean-reversion losses tend to come from **overnight gaps that a stop cannot prevent**. In 2016 he wrote that adding any kind of stop "seems to make the numbers worse" for mean reversion. — [Better System Trader ep. 003](https://bettersystemtrader.com/003-cesar-alvarez/); [Alvarez, Adding Stops and Scaling Out to a Mean Reversion Strategy](https://alvarezquanttrading.com/blog/adding-stops-and-scaling-out-to-a-mean-reversion-strategy/)
- **N-day (time) exits**: in a Russell 1000 test, 2006–2016, the average trade was a loser after 8 days, yet **forcing an exit at 8 days made both returns and drawdowns worse**. Results were sensitive to small changes in the hold period. — [Alvarez, N-Day exits with Mean Reversion](https://alvarezquanttrading.com/blog/n-day-exits-with-mean-reversion/)
- In later podcasts Alvarez describes using an **n-bar exit (for example 7 days)** regardless of the RSI or MA condition. He prefers time exits and profit targets over trailing stops for mean reversion, and he discusses regime filters. This partly conflicts with the 2016 blog result above. — [Better System Trader ep. 130](https://bettersystemtrader.com/130-building-mean-reversion-strategies-with-cesar-alvarez-part-2/); [Better System Trader ep. 133](https://bettersystemtrader.com/133-building-mean-reversion-strategies-with-cesar-alvarez-part-3/)

### Inferences
- The project's 61% win rate against a 60% random-entry baseline matches StatOasis's 59–65% RSI(2) win rates for fixed holds on SPY. A win rate measured against zero is mostly the market's upward drift. The useful benchmark is **conditional forward return minus unconditional forward return**, which is how Concretum frames its CRSI test. The project should adopt this framing.
- Connors' entries are **faster and more extreme** than a 20-day z ≤ -2: a 2–3 day oscillator, often requiring several consecutive down days. His exits are also **faster**: a close above the 5-day MA or RSI(2) > 70, typically 3–7 days. The project's "exit at the 20-day mean" (about 78% winners, about 3% average gain) is close to this. Its 42-day hold is really a different strategy, closer to "buy the dip in an uptrend and ride the trend".
- Connors' "no stop" argument rests on index ETFs and baskets of liquid stocks, where single-name gap risk is diversified. For a concentrated semiconductor book, catastrophic single-name gaps such as earnings or export-control news are the main residual risk. The project's finding that -15% to -20% stops cost little is consistent with "wide stops OK, tight stops hurt".
- The Elite Trader result (per-ticker dispersion within a profitable basket) and the project's own finding (per-stock win rates do not persist) point the same way. **Treat the edge as a property of the basket or index, not of individual tickers.**

### Gaps
- Could not read the exact tables in *Short Term Trading Strategies That Work* (2008), *High Probability ETF Trading* (2009) or *An Introduction to ConnorsRSI* (2012/2014). The win rates by RSI threshold (<2, <5, <10), the cumulative-RSI rule and the consecutive-down-days statistics are unverified here. From background knowledge (unverified): the cumulative RSI rule sums RSI(2) over 2 days with the sum below 35, and the book reports that buying after multiple down days or below a lower MA beat buying after up days or breakouts. Confirm against the book.
- No independent test was found specifically for **QQQ or individual semiconductor stocks over 2020–2026** under Connors' rules.
- No verified win rate for TPS (scale-in). There is no independent evidence that scaling in improves risk-adjusted return compared with a single entry. It increases exposure on the losing trades by construction.

---

## 2. Linda Bradford Raschke: Holy Grail, 80-20s, Turtle Soup, *Street Smarts*, and her trend vs. range filters

### Takeaway
Raschke's setups are **discretionary pattern trades**, mostly on futures, with mechanical triggers: a pullback to the 20-period MA in a strong ADX trend, and fading false 20-day breakouts. No published, audited win rates or independent large-sample backtests were found for Holy Grail, 80-20s or Turtle Soup. Her main transferable idea is a **regime switch**: trade pullbacks only when ADX shows a strong trend, and fade breakouts at range extremes.

### Cited Findings
- **Holy Grail (long)** [STATED RULE, via secondary descriptions]: 14-period ADX starts **above 30 and rising**. Price retraces to the 20-period moving average, and a buy stop goes at the high of the bar that touches the average. One source says 20 **SMA**, while community scripts say 20 **EMA** (a conflict). The setup comes from *Street Smarts* (Connors & Raschke). — [Trading Setups Review, Holy Grail](https://tradingsetupsreview.com/the-holy-grail-trading-setup); [TradingView Holy Grail script](https://my.tradingview.com/script/hawl3ybg-Holy-Grail-Setup-with-Confidence-Opacity)
- **Turtle Soup (long)** [STATED RULE]: the market makes a **new 20-day low** (the Turtles' sell trigger). The **previous 20-day low must be at least 4 sessions old**, and a buy stop goes just above that earlier low (a failed-breakdown fade). **Turtle Soup Plus One** is the same setup triggered one day later. — [ProEA Turtle Soup](https://proea.app/en/blog/turtle-soup); [MQL5 article 2717](https://www.mql5.com/en/articles/2717); [Aron Groups](https://arongroups.co/forex-articles/turtle-soup-trading-strategy/)
- **80-20s** [STATED RULE, partially described]: a daily bar with an extreme open-to-close position in its range (80%+), followed by a test-and-reverse entry. It is grouped with Turtle Soup and Momentum Pinball as "test" setups. An MQL5 coder implemented the rules but notes the implementation omits "some of the important details of the authors' trading". — [MQL5 article 2785, 80-20 trading strategy](https://www.mql5.com/en/articles/2785)
- The *Street Smarts* publication year is cited as both 1995 and 1996. — [RoboForex summary](https://roboforex.com/blog/education/trading-strategies-that-were-a-revolution-three-strategies-of-linda-raschke/); [pdfcoffee listing (1995)](https://pdfcoffee.com/street-smarts-laurence-a-connors-and-linda-bradford-raschke-1995-file-goc-5-pdf-free.html)
- Raschke profile titled "Turtle Soup, the First Market Wizard, and One Losing Year". This is a career claim and not independently audited in the excerpt. — [Complete Trader's Edge](https://completetradersedge.com/linda-raschke-turtle-soup-pattern-trader/)
- **No backtest statistics** (win rate, expectancy, drawdown) for Holy Grail, 80-20s or Turtle Soup turned up. TradingView and MQL5 items are indicator or EA implementations, not performance studies. — [search result set above; e.g., MQL5 2717](https://www.mql5.com/en/articles/2717)

### Inferences
- The Holy Grail is the "trend-pullback" cousin of the project's rule, with a stronger trend requirement (ADX > 30 rising, not just above the 200-day MA) and a **shallower pullback** (a touch of the 20 MA, not -2σ). Blending idea: require a trend-strength filter, and enter on a **reversal trigger** (a buy stop above the prior bar's high) rather than buying the close of the down day. This waits for the first sign of a turn and avoids catching a falling knife. It is untested; validate it in the project's own backtest.
- Turtle Soup is effectively "buy the new 20-day low, but only after it fails". On a 20-day z ≤ -2 signal, a Turtle-Soup-style confirmation would be: wait for price to reclaim the prior 20-day low or the prior day's high.

### Gaps
- No independent quantitative evidence on any Raschke setup in US equities or ETFs in 2020–2026.
- Raschke's own statements on ADX or range filters beyond the Holy Grail's ADX > 30 were not retrievable (her site and Schwager interview text could not be fetched).

---

## 3. Larry Williams: %R, short-term patterns, volatility breakouts, and the Robbins World Cup record with its caveats

### Takeaway
Williams' 1987 World Cup result (a $10,000 account to about $1.14M, +11,376%) is a real-money contest result listed as verified by the contest organiser's affiliate. It was achieved with extreme leverage in futures, and the account **gave back roughly half from a mid-year peak above $2M**. It shows tolerance for enormous volatility, not a replicable risk profile for an 8,000-dollar stock account. His pattern claims, such as the Oops pattern with "almost 90% winners", are self-reported book results. Independent tests are sparse and mixed.

### Cited Findings
- **1987 Robbins World Cup Championship of Futures Trading**: $10,000 grew to **$1,137,600 (+11,376%)** over the 12-month contest. — [Wikipedia, Larry R. Williams](https://en.wikipedia.org/wiki/Larry_R._Williams); [World Cup Trading Championships, Larry Williams](https://worldcupchampionships.com/team/larry-williams); trading-tournaments.com lists the result as "Verified" — [trading-tournaments.com profile](https://trading-tournaments.com/traders/larry-williams)
- Sources disagree on the dollar figures: a net gain of $1,137,607 versus a year-end account of $1,147,607. Reported returns range from about 10,900% to 11,376%. — [Trading Tournaments career article](https://trading-tournaments.com/articles/larry-williams-trading-career); [TradingGreats](https://www.tradinggreats.com/traders/larry-williams)
- **Intra-year drawdown**: the account peaked **above $2.1M mid-year**, then "a couple of final trades didn't work out" and it closed at about $1.1M, roughly a 45–50% give-back from the peak. He traded mainly Treasury bonds and S&P 500 futures. — [Complete Trader's Edge](https://completetradersedge.com/larry-williams-11376-percent-trading-record); [Unger Academy](https://ungeracademy.com/blog/larry-williams-10000-to-1-million-trading) [VENDOR]; see also the critical take "the problem with a record year" — [Margin of Pain](https://marginofpain.com/larry-williams-problem-with-record-year/)
- His daughter Michelle Williams (the actress) won the same contest in **1997 with about 1,000%** (one source says 1,001%). — [Trading Tournaments](https://trading-tournaments.com/articles/larry-williams-trading-career); [TradingGreats](https://www.tradinggreats.com/traders/larry-williams)
- Caveat: an "audited" claim appears on promotional sites, but I could not confirm an independent audit beyond the contest's own records. Results for later years (for example 1988) were not found. — [search summary of CMT Association / trader profiles](https://cmtassociation.org/presenter/larry-williams/)
- **Volatility breakout** [STATED RULE, secondary]: buy or sell stops are placed at today's open ± a percentage of the prior day's range. An MQL5 author's 2025 gold backtest of this idea (+60%) is a single-market, single-year coder test, not Williams' result. — [MQL5 article 20745](https://www.mql5.com/en/articles/20745)
- **Oops pattern**: price gaps open below the prior day's low, then the entry is a buy stop at the prior low (gap-and-reverse). Williams' book claimed **"almost 90% winning trades" on bonds and S&P** [SELF-REPORTED]. An independent DAX futures test found gap signals were "more often than not … false signals". — [Unger Academy, We Tested Larry Williams' Oops Pattern](https://ungeracademy.com/blog/we-tested-larry-williams-oops-pattern-the-results-might-surprise-you) [VENDOR but independent of Williams]
- Williams %R defaults to a 14-period lookback. The book's specific %R entry rules were not retrievable. — [EBC Financial, Larry Williams strategy 2026](https://www.ebc.com/forex/larry-williams-strategy-wr-cot-signals-2026)

### Inferences
- The Williams lesson for this project is about **variance, not edge**. Contest-winning returns come from extreme leverage with roughly 50% drawdowns, which is incompatible with an 8,000-dollar account that must survive.
- The Oops and volatility-breakout ideas share the Raschke idea of **entering on a reversal trigger after weakness**, not buying the close of the down day. Whether that improves a Bollinger-band entry is an empirical question for the project's backtester.

### Gaps
- I could not access official Robbins contest documentation or audit details (methodology, number of entrants, survivorship).
- No independent large-sample test of Williams' patterns on US large-cap stocks or ETFs was found.

---

## 4. Other systematic practitioners with public rules (brief)

### Takeaway
Little citable rule-level material was retrievable. What exists suggests Bollinger-band mean reversion on index futures and ETFs is a common practitioner building block, usually combined with trend filters and session or day filters, but no audited performance was found.

### Cited Findings
- **Kevin Davey** (attributed): a Bollinger Bands mean-reversion script that buys on a close below the lower band and exits on a close above the upper band. The attribution to Davey is unconfirmed. — [TradingView script "Bollinger Bands Mean Reversion by Kevin Davey"](https://www.tradingview.com/script/umOCSa0t/). A community adaptation of his "Entry Strategy #3" to DAX 15-minute bars added a long-only rule, an MA entry filter and an exclude-Fridays rule, with testing still pending. — [ProRealCode forum](https://www.prorealcode.com/topic/nasdaq-mean-reversion/)
- **Andrea Unger / Unger Academy**: mean-reversion entries at support or resistance (for example the prior session's high or low), with a return-to-mean exit. US stock index futures (mini S&P, Nasdaq) are described as markets where mean reversion has "historically worked well". — [VENDOR] [Unger Academy blog](https://ungeracademy.com/blog/the-simplest-trading-strategy-trend-following-mean-reverting-or-breakout)
- **Michael Stokes (MarketSci), second-hand**: short-term mean reversion in the S&P is a "recent phenomenon [that] may actually now be inoperative". His adaptive model switched from trend-following to mean reversion around 2000–2003. — [RRSP Strategy blog summary](https://rrspstrategy.wordpress.com/2013/05/21/is-there-a-mean-reversion-anomaly/)
- **IBS (Internal Bar Strength)**, a close-location-in-range reversal signal: academic evidence shows daily mean reversion in equity-index ETFs. — [Pagonidis, The IBS Effect (NAAIM)](https://www.naaim.org/wp-content/uploads/2014/04/00V_Alexander_Pagonidis_The-IBS-Effect-Mean-Reversion-in-Equity-ETFs-1.pdf). Executing at the next open instead of the signal close cut the S&P average gain per trade from **0.41% to 0.31%**. — [The Robust Trader, IBS](https://therobusttrader.com/internal-bar-strength-ibs/). IBS reportedly works best in volatile or bear markets. — [VENDOR] [QuantifiedStrategies IBS](https://www.quantifiedstrategies.com/ibs-internal-bar-strength-indicator-strategies/). WealthLab claims ">300% on QQQ in the past decade". — [VENDOR] [WealthLab IBS blog](https://www.wealth-lab.com/blog/build-a-profitable-mean-reversion-strategy-using-the-ibs-indicator)
- **Howard Bandy** (*Mean Reversion Trading Systems*) and **Tom Basso**: no retrievable rule-level content.

### Inferences
- Davey's (attributed) band rule exits at the **upper** band, a longer hold than the project's mid-band exit. That is consistent with the project's finding that longer holds raise the average gain.

### Gaps
- No rules or statistics retrieved for Bandy or Basso. Their book content would need direct access.

---

## 5. Practitioner refinements relevant to the current rule: which have independent evidence?

### Takeaway
Ranked by strength of independent evidence:
1. **Basket or ETF trading instead of single-name selection**: supported by the pattern of results.
2. **Wide or no price stops, rather than tight stops**: practitioner tests consistently support this, with a gap-risk caveat.
3. **Short, fast-exit rules**: these raise win rate but not necessarily total return.
4. **RSI(2) or consecutive-down-day entries versus Bollinger z**: no head-to-head independent evidence found.
5. **Scaling in, earnings avoidance, index regime filter**: plausible but largely untested in public sources.

### Cited Findings
- **Basket vs. single stock**: an RSI(2) pullback on about 150 S&P 500 names was profitable as a basket (PF 1.57), with wide per-ticker dispersion. — [Elite Trader](https://www.elitetrader.com/et/threads/backtested-a-mean-reversion-rsi-2-pullback-strategy-on-150-s-p500-names.390710/). The best robust RSI variants came from QQQ, the index ETF. — [StatOasis](https://statoasis.com/overfit/research/better-rsi-backtest)
- **Stops**: tighter stops mean lower profit and no stop was best in Connors' table [UNOFFICIAL COPY] — [pdfcoffee](https://pdfcoffee.com/short-term-trading-strategies-that-work-by-larry-connors-and-cesar-alvarez-pdf-free.html). Alvarez found wider stops better and no stops better still, because gaps defeat stops. — [Better System Trader ep. 003](https://bettersystemtrader.com/003-cesar-alvarez/); [Alvarez blog](https://alvarezquanttrading.com/blog/adding-stops-and-scaling-out-to-a-mean-reversion-strategy/)
- **Time stop**: mixed. Alvarez's 2006–2016 Russell 1000 test showed an 8-day forced exit worsened returns and drawdown, and results were sensitive to the hold length. — [Alvarez N-day exits](https://alvarezquanttrading.com/blog/n-day-exits-with-mean-reversion/). Later, he advocates a roughly 7-bar exit. — [Better System Trader ep. 130](https://bettersystemtrader.com/130-building-mean-reversion-strategies-with-cesar-alvarez-part-2/)
- **Exit speed versus hold length**: RSI(2) on SPY had a 59.1% win rate at a 5-bar hold and 65.1% at a 10-bar hold. — [StatOasis](https://statoasis.com/overfit/research/better-rsi-backtest). Classic RSI(2) with an exit on a close above the 5-day MA reached about 82% winners on SPY, but lagged buy-and-hold in total return. — [GuruFinanceInsights](https://gurufinanceinsights.substack.com/p/i-backtested-the-classic-rsi2-mean)
- **Scaling in (TPS)**: rule documented, with no independent risk-adjusted evidence found. — [TuringTrader TPS](https://www.turingtrader.com/portfolios/connors-tps/)
- **Liquidity filter**: Connors used price > $5 and ADV > 500k shares, and Concretum reused these filters in its out-of-sample test. — [Concretum on X](https://x.com/ConcretumR/status/1879572346362593308). Mechanism evidence: a working paper attributes daily reversal to liquidity frictions and finds it **stronger in high-priced, liquid stocks** like S&P 500 names. — [Graziani, Time Series Reversal: A Payment Cycle Friction](https://afajof.org/management/viewp.php?n=133448)
- **Earnings avoidance**: no study measuring the effect on pullback strategies was found. Only opinion pieces exist, for example "a perfect setup into a known event is a lottery ticket". — [Audacity Capital guide](https://audacity.capital/trading-guides/mean-reversion/)
- **Execution timing**: signals computed on the close but executed at the next open lose part of the edge (IBS S&P average gain fell from 0.41% to 0.31%). — [The Robust Trader](https://therobusttrader.com/internal-bar-strength-ibs/)
- **Costs and overfitting**: a strategy with a pre-cost Sharpe of 1.5 may fall to about 0.8 after realistic friction (practitioner estimate). — [Quantvero](https://www.quantvero.com/algo-trading/mean-reversion-trading-strategy/). Optimising over noise yields a median best Sharpe of 1.17. — [StatOasis](https://statoasis.com/overfit/research/why-most-traders-fail-the-missing-piece-called-robustness-testing)

### Inferences
Suggested blend candidates for the project, each to be tested against the random-entry baseline, not against zero:
- (a) Replace or AND the z ≤ -2 entry with a short-horizon oversold measure: RSI(2) < 10, CRSI < 10, or 3+ consecutive down closes.
- (b) Add an **index regime filter** (QQQ or SOXX above its 200-day MA) alongside the stock's own 200-day filter.
- (c) Use a reversal-trigger entry: a buy stop above the prior high (Raschke/Williams) versus buying the signal close.
- (d) Trade QQQ, SOXX or SMH or an equal-weight basket of semiconductor names, not single-name picks, given the evidence that per-ticker edges do not persist.
- (e) Keep a wide catastrophe stop (-15% to -20%) plus an earnings-date blackout as gap-risk control rather than edge enhancement.
- (f) Compare exit families: close above the 5-day MA, RSI(2) > 70, return to the 20-day mean, and N-day.

Expect the win rate to rise and the average gain per trade to fall with faster exits. The decision metric should be expectancy times trade frequency, after costs, versus buy-and-hold.

### Gaps
- No public head-to-head test of Bollinger z-score versus RSI(2) versus consecutive down days on the same universe and period was found.
- No independent evidence on earnings blackouts or on scaling in for single stocks.
- Index-regime-filter evidence specific to semiconductors or QQQ in 2020–2026 was not found.

---

## 6. Do these short-term edges still exist on US index ETFs and large caps in 2020–2026?

### Takeaway
The best available independent evidence says the edge is **weaker but still positive**:
- RSI(2) on SPY after 2008 has a lower Sharpe than buy-and-hold (0.68 vs 0.87), with a still-positive per-trade edge.
- CRSI's next-week oversold excess return on US stocks fell from about 1.5% in the 1990s to about 0.3% in 2015–2025.
- QQQ appears to be the most robust index ETF for RSI-type variants through mid-2026.

Year-to-year results are lumpy: contrarian S&P rules made large gains in 2022 and lost in 2020–2021.

### Cited Findings
- SPY RSI(2) post-publication Sharpe 0.68 vs buy-and-hold 0.87; per-trade edge about a third smaller but positive (data to 2026). — [EmpiricaLab](https://empiricalab.substack.com/p/connors-rsi2-spy)
- CRSI < 5 next-week return was **about +1.5% (1990–2000) and about +0.3% (2015–2025)**; "smaller but not gone". — [Concretum Research](https://x.com/ConcretumR/status/1879572346362593308?lang=en)
- SPY/QQQ/IWM/DIA data through June 2026: only 53.8% of CRSI variants were profitable, and the best robust variants were on QQQ. — [StatOasis](https://statoasis.com/overfit/research/better-rsi-backtest)
- A contrarian S&P 500 rule backtest had **large gains in 2001 and 2022, and losses in 2020 and 2021**. This is an informal backtest. — [Raven Quant](https://ravenquant.com/sp-500-contrarian-strategy/)
- Earlier decay warnings: ConnorsRSI showed near-zero average P/L in 2014–2015 [INDEPENDENT/practitioner] — [Alvarez](https://alvarezquanttrading.com/blog/connorsrsi-analysis/). The edge appeared only around 2000–2003 and may become inoperative (Stokes, second-hand) — [RRSP Strategy](https://rrspstrategy.wordpress.com/2013/05/21/is-there-a-mean-reversion-anomaly/). RSI(2) lost money over 1965–1995. — [trade2win](https://www.trade2win.com/threads/backtest-results-for-connors-rsi2-strategy.242688/)
- Decay of published strategies has accelerated since 2000. — [arXiv 2105.01380](https://arxiv.org/pdf/2105.01380)

### Inferences
- Short-term reversal looks **regime-dependent**. It appeared around 2000, was strong through about 2014, has been weaker since, and pays most in high-volatility selloffs such as 2008, 2020 and 2022. The project's 2016–2026 window falls largely in the "weakened" era, which explains why its win rate barely beats random entry.
- For a retail trader, the realistic aim is a **modest, regime-dependent excess return over buy-and-hold with lower time in market**, not a standalone high-Sharpe engine. Blending the mean-reversion entry with a core long position in QQQ or semiconductors, adding on oversold signals rather than going from flat to all-in, is consistent with this evidence but untested here.

### Gaps
- No independent 2020–2026 test isolated **semiconductor stocks** (NVDA, AMD, AVGO, etc.) or **SOXX/SMH** under Connors-style rules.
- I could not read the full EmpiricaLab and Concretum write-ups, so post-2020 sub-period numbers, transaction-cost assumptions and post-publication win rates are not confirmed.
- No peer-reviewed paper specifically measuring daily reversal decay in US index ETFs after 2020 was found.
