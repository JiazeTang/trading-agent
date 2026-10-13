# Mean-Reversion / Short-Term Reversal: Return-Risk Profile, and Combining Mean Reversion with Trend/Momentum

> **How these notes were verified (read first).** In this session, WebFetch and direct PDF downloads were blocked (DNS failures and proxy policy), so I could not open full papers. Every number below comes from abstracts, publisher or RePEc pages, author PDFs, or reputable secondary summaries (CXO Advisory, Quantpedia, Alpha Architect, AQR-related commentary). Each one appeared in search-result extracts of those pages. Labels used throughout:
> - **[abstract]**: the paper's own abstract or publisher page.
> - **[paper text via snippet]**: an extract from the paper's PDF that appeared in search results.
> - **[secondary]**: a third party's summary. Check it against the paper before relying on it.
> - **[unverified]**: could not be confirmed.
>
> Unless stated otherwise, results are **gross of transaction costs**.

## Q1. Short-term reversal as liquidity provision (Lehmann 1990; Lo & MacKinlay 1990; Nagel 2012): returns, VIX dependence, tail-risk implications

### Takeaway
Cross-sectional short-term reversal (buy recent losers, sell recent winners over 1 day to 1 week) is best read as being paid for supplying liquidity.
- **Raw returns have decayed a lot.** Daily contrarian returns fell from 1.38%/day in 1995 to 0.13%/day in 2007 (gross, mostly small caps).
- **Returns depend strongly on the state of the market.** Expected returns and conditional Sharpe ratios jump when the VIX is high (Nagel 2012).
- **The strategy carries short-volatility exposure.** Reversal portfolios have large negative betas to volatility shocks. They can also suffer sudden losses at the onset of deleveraging (the August 2007 "quant meltdown").
- **So it is not a crisis hedge.** It is a short-volatility-like premium that pays most after stress begins, but takes mark-to-market hits as stress starts.

### Cited Findings
**Lehmann (1990)**
- Lehmann (1990), "Fads, Martingales, and Market Efficiency", *Quarterly Journal of Economics* 105(1):1–28, US stocks, weekly horizon. It finds "systematic tendencies for current 'winners' and 'losers' in one week to experience sizeable return reversals over the subsequent week". The profits "persist after corrections for the mismeasurement of security returns because of thin trading and bid-ask spreads" and under plausible transaction costs [abstract] — [NBER w2533](https://www.nber.org/papers/w2533); [RePEc/QJE](https://ideas.repec.org/a/oup/qjecon/v105y1990i1p1-28..html).
- Lehmann's Table II, as summarized by Alpha Architect [secondary, not checked against the table]:
  - prior-week winners averaged about −0.35% to −0.55% the next week;
  - prior-week losers averaged about +0.86% to +1.24% the next week.
  - Source: [Alpha Architect summary](https://alphaarchitect.com/2015/01/14/quantitative-momentum-research-short-term-return-reversal/).

**Lo & MacKinlay (1990)**
- Lo & MacKinlay (1990), "When are contrarian profits due to stock market overreaction?", *Review of Financial Studies*. Contrarian profits can arise without overreaction: if some stocks' returns systematically lead others', a contrarian portfolio earns positive expected returns. They find large-stock returns lead small-stock returns and "present evidence against overreaction as the only source of contrarian profits" [abstract] — [MIT abstract page](https://web.mit.edu/~alo/www/Papers/lo-mackinlay-90b.html); [NBER w2977](https://www.nber.org/system/files/working_papers/w2977/w2977.pdf).
- A widely repeated characterization is that "less than 50%" of contrarian profits come from overreaction. I saw this only in a secondary paper during search, not in the retrieved abstract text [unverified]. Jegadeesh & Titman (1995) later disputed the decomposition and attributed most profits to overreaction to firm-specific news [secondary, unverified].

**Khandani & Lo (2007/2011): decay of daily contrarian returns**
- Setup: they simulate the Lehmann / Lo-MacKinlay contrarian strategy, rebalanced daily (long prior-day losers, short prior-day winners). Universe: all CRSP stocks plus 10 size deciles. Sample: 3 Jan 1995 – 31 Aug 2007. Gross: no costs, price impact or short-sale constraints.
- Average daily return [paper text via snippet]:
  - **1.38%/day in 1995** (≈345%/yr on a 250-day year);
  - **0.44%/day in 2000**;
  - **0.13%/day in 2007 YTD** (to 31 Aug).
  - Source: [Khandani & Lo, MIT PDF](https://web.mit.edu/Alo/www/Papers/august07.pdf); [SSRN 1015987](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1015987).
- Size dependence in 1995: **3.57%/day in the smallest decile vs 0.04%/day in the largest**. Most of the "edge" sat in illiquid small caps [paper text via snippet] — [MIT PDF](https://web.mit.edu/Alo/www/Papers/august07.pdf).
- To restore historical return levels, they re-simulated at roughly **8:1 leverage (2006 levels)**. The strategy dropped and then recovered sharply in the week of 6 Aug 2007, after several weeks of weak performance. Their "unwind hypothesis": forced liquidation of one or more large quant market-neutral books. The later version (2008–2011), using transactions data, finds the unwinding began in July 2007 and lasted to year-end. It also finds a temporary withdrawal of market-making capital from 8 Aug [abstract] — [NBER w14465](https://www.nber.org/system/files/working_papers/w14465/w14465.pdf).
- A blog excerpt cites a loss of about 12 daily standard deviations for the unleveraged model portfolio, but the text was truncated [unverified] — [Harvard blog](https://archive.blogs.harvard.edu/cqtwo/2007/10/25/what-happened-to-the-quants-in-august-2007/).

**Nagel (2012), "Evaporating Liquidity"**
- Published in *RFS* 25(7):2005–2039. Abstract [abstract] — [EconPapers](https://econpapers.repec.org/RePEc:oup:rfinst:v:25:y:2012:i:7:p:2005-2039); [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1988706):
  - Short-term reversal returns proxy for the returns to liquidity provision.
  - "The expected return from liquidity provision is strongly time-varying and highly predictable with the VIX index."
  - "Expected returns and conditional Sharpe ratios increase enormously along with the VIX during times of financial market turmoil, such as the financial crisis 2007-09."
  - Reversal strategies on industry portfolios, which earn little unconditionally, also earn high returns and Sharpe ratios when the VIX is high.
  - Nagel attributes evaporating liquidity mainly to liquidity suppliers withdrawing, which raises the return they require.
- Construction [paper text via snippet]: each day, the average of five reversal strategies. Each weights stocks in proportion to the negative of market-adjusted returns on day t−1, …, t−5, scaled to $1 long and $1 short.
- Path over time [paper text via snippet]: returns "declined steadily to less than 0.2% per day" before the crisis, then "virtually exploded during the financial crisis", exceeding levels seen in the 1998 LTCM crisis — [NBER w17653](https://www.nber.org/system/files/working_papers/w17653/w17653.pdf).
- Nagel's equal-weighted reversal portfolio puts heavy weight on small stocks — [Drechsler, Moreira & Savov, "Liquidity and Volatility"](https://rodneywhitecenter.wharton.upenn.edu/wp-content/uploads/2022/03/Paper5_Drechsler.pdf).
- Replication on large stocks: a **1-point rise in the VIX predicts about 5.37 bp higher reversal return over the next 5 days** [secondary; conference slides] — [Moreira, Duke slides](https://conferences.fuqua.duke.edu/past/documents/2018/Alan-Moreira.pdf).
- Collin-Dufresne & Daniel ("Liquidity and Return Reversals", preliminary draft, Dec 2014) [paper text via snippet; marked "do not quote"] — [Kent Daniel PDF](https://www.kentdaniel.net/papers/unpublished/str2.pdf):
  - they also find a strong relation between strategy returns and the VIX;
  - but most idiosyncratic price shocks are permanent, and the temporary part decays with a **half-life of about 2.5 days**;
  - the *speed* of mean reversion is not tied to VIX-type illiquidity measures.

**Short-volatility nature**
- Drechsler, Moreira & Savov ("Liquidity and Volatility", working paper; publication status not verified) [abstract-level] — [Wharton WP](https://rodneywhitecenter.wharton.upenn.edu/wp-content/uploads/2020/12/18-20.Drechsler2.pdf); [Stern PDF](https://pages.stern.nyu.edu/~asavov/alexisavov/Alexi_Savov_files/DMS_Liquidity_and_Volatility.pdf):
  - short-term reversal portfolios, which mimic liquidity providers, have **large negative betas to aggregate volatility shocks**;
  - those betas explain reversals' average returns using the **same price of volatility risk as in index options**.
- Interpretation: the reversal premium is economically a short-volatility premium.

**Costs and capacity**
- de Groot, Huij & Zhou (2012), "Another look at trading costs and short-term reversal profits", *JBF* 36(2):371–382 [abstract] — [RePEc](https://ideas.repec.org/a/eee/jbfina/v36y2012i2p371-382.html):
  - most cost drag comes from trading small caps;
  - restricting to large caps and using turnover-reducing construction leaves about **30–50 bp per week net of costs**.
  - Sample, per CXO [secondary]: 1990–2009, 1,500 largest US stocks — [CXO](https://www.cxoadvisory.com/?p=6251).

### Inferences
- **The liquidity-provision payoff has two phases.**
  - At the onset of a liquidity shock (Aug 2007; volatility spikes), providers lose because positions keep moving against them, and leveraged providers are forced out.
  - Once the VIX is high and capital has withdrawn, forward-looking expected returns are at their highest.
  - So the strategy is "short vol" in its exposure to volatility shocks (DMS), yet "long expected return" in high-VIX states (Nagel). Both hold at once.
  - For a single-instrument QQQ strategy, this means the best opportunities and the worst mark-to-market losses cluster in the same high-volatility regimes.
- **Cross-sectional evidence doesn't transfer directly to QQQ.** These results come from portfolios of many stocks, hedged against the market. A long-only QQQ dip-buying strategy carries the market factor on top of the liquidity premium. Its tail risk should be worse than the market-neutral reversal portfolios studied here.
- **Expect much less than headline returns.** Daily-horizon raw reversal returns decayed sharply as markets became more liquid and competitive (1995→2007). Profits concentrate in small, illiquid names, which QQQ is not.

### Gaps
- No exact Sharpe ratios, skewness, or full-sample means for Lehmann (1990), Lo-MacKinlay (1990) or Nagel (2012); the full texts could not be opened.
- No figure for the share of weeks with positive profits in Lehmann (1990).
- Nagel's exact sample period and VIX regression coefficients not obtained. (The figure appears to run through 2010; unverified.)
- Ni, Pearson, Poteshman & White (dealer gamma and autocorrelation, RFS) not located in search.

## Q2. Index-level short-horizon mean reversion (S&P 500 / SPY / QQQ): has the sign of daily or intraday autocorrelation changed?

### Takeaway
At the **daily, multi-day** horizon, autocorrelation of US and global index returns has switched **from positive (pre-1990s) to negative (2000s onward)**.
- Baltussen, van Bekkum & Da (2019 JFE) link the switch to the growth of index products (futures, ETFs, index funds).
- Trading against this serial dependence earned an annual Sharpe of about 0.63–0.67 after March 1999, gross.

At the **intraday** horizon the evidence points the other way for the *market*:
- the last 30 minutes show momentum (Gao et al. 2018; Baltussen et al. 2021), linked to gamma hedging;
- half-hour stock returns show reversal at short lags but continuation at daily-multiple lags (Heston, Korajczyk & Sadka 2010).

For 30-minute bars on QQQ, the evidence favors multi-day reversal over bar-to-bar intraday reversal.

### Cited Findings
**Daily horizon: the sign switch**
- Baltussen, van Bekkum & Da, "Indexing and stock market serial dependence around the world", *JFE* 132(1):26–48 (2019; online 2018) [abstract] — [accepted manuscript](https://personal.eur.nl/vanbekkum/2018%20JFE%20BaltussenVanBekkumDa.pdf); [EUR Pure](https://pure.eur.nl/en/publications/indexing-and-stock-market-serial-dependence-around-the-world/):
  - 20 major indexes in 15 countries;
  - serial dependence was "positive until the 1990s" and "switches to negative since the 2000s" in most markets, statistically and economically significant;
  - the decline is linked to the popularity of index futures, ETFs and index funds, supported by tests using Nikkei 225 weights and S&P 500 membership;
  - the mechanism is partly arbitrage between index products and their constituents: index products impound non-fundamental shocks into the underlying stocks, and these then revert.
- Same paper: "a strategy that trades against MAC(5) using all indexes in our sample [or the S&P 500 index alone] would result in an annual Sharpe ratio of **0.63 (0.67)** after March 2, 1999". MAC(5) is a multi-lag autocorrelation measure over 5 lags [paper text via snippet] — [accepted manuscript](https://personal.eur.nl/vanbekkum/2018%20JFE%20BaltussenVanBekkumDa.pdf).
  - Cost treatment not confirmed; presumably gross.
- Conflict: a third-party "PapersWithBacktest" replication lists **Sharpe −0.21 over 1990–2026**. The methodology is unknown, and the sample includes pre-1999, when the paper itself shows positive dependence [secondary, unverified]. This could signal post-publication decay or a methodology mismatch — [PapersWithBacktest](https://paperswithbacktest.com/strategies/indexing-and-stock-market-serial-dependence-around-the-world).
- Older positive autocorrelation was partly an artifact of stale prices in the cash index. Richardson & Whitelaw: Russell 2000 daily *index* autocorrelation **22%** vs **6%** for its futures contract [secondary aggregator] — [Sewell stylized-facts page](https://finance.martinsewell.com/stylized-facts/dependence).
- Practitioner tracking: the rolling 252-day lag-1 autocorrelation of S&P 500 daily returns fell below **−0.40** after the March 2020 crash, then quickly reverted toward neutral [blog, unverified] — [Price Action Lab, "Mean-Reversion Is Waning" (2021)](https://www.priceactionlab.com/Blog/2021/09/mean-reversion-waning/).
- Martin (2021), "On the autocorrelation of the stock market", *J. Financial Econometrics* 19(1):39–52 [abstract-level] — [LSE](https://researchonline.lse.ac.uk/id/eprint/106215):
  - uses an option-implied measure at a 6-month horizon (not daily);
  - S&P 500 autocorrelation was near zero before the subprime crisis and about **−20% to −30%** afterwards.

**Intraday horizon: momentum and reversal**
- Gao, Han, Li & Zhou (2018), "Market intraday momentum", *JFE* [abstract] — [WUSTL](https://profiles.wustl.edu/en/publications/market-intraday-momentum/):
  - SPY high-frequency data, 1993–2013;
  - the first half-hour return (measured from the previous close) predicts the **last half-hour** return;
  - stronger on volatile days, high-volume days, recession days and macro-news days.
- Working-paper numbers (1999–2012), via CXO [secondary]: R² ≈ 2%; 3.5% with the 12th half-hour added; 4.8% when first-half-hour volatility is high. Timing strategy: **6.3% vs −0.5%/yr, gross**. CXO notes these tests ignore frictions — [CXO](https://cxoadvisory.com/calendar-effects/first-and-last-half-hours-of-trading-linked).
- Baltussen, Da, Lammers & Martens (2021), "Hedging demand and market intraday momentum", *JFE* 142:377–403 [abstract] — [EUR Pure](https://pure.eur.nl/en/publications/hedging-demand-and-market-intraday-momentum/); [author PDF](https://www3.nd.edu/~zda/intramom.pdf):
  - 60+ futures on equities, bonds, commodities and FX, 1974–2020;
  - the rest-of-day return positively predicts the last-30-minute return "everywhere";
  - driven by hedging of short-gamma positions (option market makers, leveraged ETFs);
  - the effect **reverts over the next days**.
- Barbon & Buraschi ("Gamma Fragility", WP) [abstract-level] — [author page](https://abarbon.com/papers/gamma-fragility):
  - intraday **momentum** follows from *negative* dealer gamma imbalance interacting with illiquidity;
  - intraday **reversal** follows from *positive* gamma imbalance.
- Zarattini, Aziz & Barbon (2024), "Beat the Market: An Effective Intraday Momentum Strategy for S&P500 ETF (SPY)", SFI RP 24-97 (WP) [abstract] — [SFI](https://www.sfi.ch/de/publications/n-24-97-beat-the-market-an-effective-intraday-momentum-strategy-for-s-p500-etf-spy); [CXO](https://www.cxoadvisory.com/?p=45565):
  - an intraday trend-following rule on SPY with trailing stops;
  - 2007–early 2024: **total 1,985%, 19.6%/yr, Sharpe 1.33, net of costs**;
  - working paper, not peer-reviewed; the parameters may be fitted in-sample.
- Heston, Korajczyk & Sadka (2010), "Intraday patterns in the cross-section of stock returns", *JF* 65(4):1369–1407 [abstract] — [Kellogg](https://www.kellogg.northwestern.edu/academics-research/research/detail/2010/intraday-patterns-in-the-cross-section-of-stock-returns); [arXiv](https://arxiv.org/pdf/1005.3535):
  - NYSE stocks, Jan 2001 – Dec 2005, 13 half-hour intervals per day;
  - **short-lag half-hour returns reverse** (bid-ask bounce, liquidity imbalances lasting under an hour);
  - returns at lags that are multiples of one day (13, 26, 39… half-hours) **continue**, for up to 40 trading days;
  - strongest in the first and last half-hours.
- The "Term Structure of Intraday Return Autocorrelations" working paper [abstract-level] — [CESA WP 14](https://www.fernuni-hagen.de/igas/docs/cesa_wp_14.pdf):
  - US stocks, 2017–2021;
  - negative autocorrelation is most pronounced at horizons of **30 minutes and longer**, but only in mid and large caps;
  - linked to inventory control and option market makers' gamma.
- Safari & Schmidhuber (2025), "Trends and Reversion in Financial Markets on Time Scales from Minutes to Decades", *Physica A* 675 [abstract] — [arXiv v2](https://arxiv.org/html/2501.16772v2); [RePEc](https://ideas.repec.org/a/eee/phsmap/v675y2025ics0378437125004480.html):
  - data: futures tick data, daily futures, centuries of monthly and yearly data;
  - **trending regime from a few hours to a few years; reversion at shorter and longer scales**;
  - the short-scale reversion regime, beyond what tick size explains, ends at about **30 minutes** [abstract-level, per search extract];
  - **in the trending regime, weak trends persist while strong trends revert**.

### Inferences
- **Daily/multi-day dip-buying has support; bar-to-bar intraday reversal is weak.** For QQQ on 30-minute bars, the most robust published mean-reversion edge is at **daily, multi-day** horizons (since about 2000; linked to ETF and index arbitrage). At 30 minutes, QQQ sits at the boundary where microstructure reversion fades (Safari-Schmidhuber) and intraday trend effects start (Gao et al.; Baltussen et al. 2021), especially late in the session and on volatile, short-gamma days.
- **Sensible design.** Use *multi-day* oversold signals (e.g., 1–5 day declines) on 30-minute bars for execution timing. Avoid fading moves inside the session's last hour.
- **QQQ-specific exposure.** QQQ has large single-name and leveraged-ETF (TQQQ/SQQQ) rebalancing flows. These are the short-gamma flows that Baltussen et al. (2021) link to end-of-day momentum, so they apply directly to QQQ. This is inference: no QQQ-specific paper was found.

### Gaps
- No published study of 30-minute return autocorrelation for QQQ/NDX specifically. A search found only constituent-level and generic intraday studies. The user's own data must be tested.
- No verified post-2019 out-of-sample update of the Baltussen et al. index-reversal Sharpe ratio; the third-party replication conflicts.
- Published-version R² and net returns for Gao et al. (2018) were not obtained, and post-2013 decay was not checked.

## Q3. Negative skew / "picking up nickels in front of a steamroller": high win rate, rare large losses

### Takeaway
Lempérière et al. (2017) document an approximately **linear relation between a strategy's Sharpe ratio and its negative skewness** across risk premia (equity, Fama-French, FX carry, short vol, bonds, credit). Trend following is the clear exception: positive skew *and* positive returns. Short-term reversal is not tested directly in that paper. However, it is economically short-volatility (DMS), it suffered the August 2007 unwind, and it is the mirror image of trend. So it should be expected to sit on the negative-skew side.

Practitioner tests of long-only index dip-buying show the typical profile: a **high win rate (65–72%) with a modest profit factor**, meaning small average wins against occasional large losses.

### Cited Findings
**Lempérière et al. (2017)**
- Lempérière, Deremble, Nguyen, Seager, Potters & Bouchaud (2017), "Risk premia: asymmetric tail risks and excess returns", *Quantitative Finance* 17(1):1–14 [abstract] — [arXiv 1409.7720](https://arxiv.org/abs/1409.7720); [RePEc](https://ideas.repec.org/a/taf/quantf/v17y2017i1p1-14.html); [T&F](https://www.tandfonline.com/doi/full/10.1080/14697688.2016.1183035):
  - risk premia are "strongly correlated with tail-risk skewness but very little with volatility";
  - using a new skewness measure, there is "an approximately linear relation" between Sharpe ratio and negative skewness;
  - trend following is the exception, with positive skewness and positive excess returns; Fama-French value (HML) and low-volatility show this less strongly;
  - some strategies may therefore be "pure alpha"/anomalies rather than risk premia.
- Their skewness measure ζ\* and Sharpe ratios, from the paper text via snippet — [ResearchGate/arXiv](https://www.researchgate.net/publication/314531713_Risk_Premia_Asymmetric_Tail_Risks_and_Excess_Returns):

| Series | ζ\* (skewness) | Sharpe ratio |
|---|---|---|
| SMB | ≈ −1.39 | 0.14 |
| UMD (cross-sectional momentum) | ≈ −1.38 | 0.67 |
| HML | ≈ +0.43 | 0.64 |
| US market factor, daily | ≈ −1.47 | 0.57 |
| US market factor, monthly | ≈ −0.32 | — |

- Exact Sharpe/skew for their trend-following series not obtained.

**Momentum and trend for comparison**
- Daniel & Moskowitz (2016), "Momentum crashes", *JFE* 122(2):221–247 [abstract] — [NBER w20439](https://www.nber.org/papers/w20439):
  - cross-sectional momentum suffers "infrequent but strong and persistent strings of negative returns";
  - crashes occur in "panic" states: after market declines, when volatility is high, and at the same time as market rebounds;
  - a dynamic strategy forecasting momentum's mean and variance roughly doubles alpha and Sharpe.
  - Note: cross-sectional momentum is also negatively skewed (UMD ζ\* ≈ −1.38 above). Only *time-series* trend following has positive skew.
- Moskowitz, Ooi & Pedersen (2012), "Time series momentum", *JFE*, 1985–2009, futures across asset classes [abstract]: TSMOM "performs best during extreme markets" — [SSRN 2089463](https://papers.ssrn.com/abstract=2089463).
  - NBIM characterizes the payoff as straddle-like on equities [secondary] — [NBIM note](https://www.nbim.no/globalassets/documents/news/2014/discussionnote_time_series_momentum_latest.pdf).

**Short-vol and put-selling analogues**
- Reversal portfolios have large negative betas to aggregate volatility shocks, priced like index-option volatility risk — [Drechsler, Moreira & Savov WP](https://rodneywhitecenter.wharton.upenn.edu/wp-content/uploads/2020/12/18-20.Drechsler2.pdf).
- Put-based (negatively skewed) vs call-based (positively skewed) strategies: a significantly negative skewness premium in daily returns, about **5 percentage points per year** [abstract-level] — [Wallmeier (2025), *J. Futures Markets*](https://onlinelibrary.wiley.com/doi/full/10.1002/fut.22615).

**Win rate vs payoff in practitioner backtests (vendor, single-path, low evidentiary weight)**
- Source: [BacktRex S&P 500](https://backtrex.com/en/backtests/connors-rsi-2-sp-500); [BacktRex DAX](https://backtrex.com/en/backtests/connors-rsi-2-dax).
- Rules: Connors RSI(2) < 5 with close > 200-day SMA, exit on close > 5-day SMA; 0.02% commission per side.

| Market and period | Trades | Win rate | Profit factor | Max DD (strategy vs B&H) | CAGR (strategy vs B&H) |
|---|---|---|---|---|---|
| S&P 500 CFD, Oct 2016 – Oct 2026 | 73 | 71.2% | 1.43 | −21.5% vs −35% | ~1.7% vs 13.5% |
| DAX, same rules | — | 66.7% | — | 12.9% | ~1.4% vs 9.0% |
| EUR/USD, same rules | — | 54.7% | 0.78 | — | — |

  - DAX: the author notes the win rate beat break-even by only about 6 points.
  - EUR/USD: the edge did not carry over to FX.

### Inferences
- **What to expect from a QQQ mean-reversion strategy:** a win rate well above 50%, average win smaller than average loss, negative skew in trade P&L, and loss clusters in volatility shocks and at the onset of trending sell-offs.
- **The structural complement is time-series trend:** positive skew, best in extreme markets. Cross-sectional momentum is *not* that complement, because it also crashes in panic rebounds.
- **Judge it on skew-aware metrics, not Sharpe alone.** Following Lempérière et al., a mean-reversion Sharpe should be "discounted" for its negative skew. Report skewness, worst-trade and worst-week loss, tail ratios and max drawdown next to Sharpe in the regime split.

### Gaps
- No primary study found that directly reports skewness, win rate and payoff ratio for *index-level* short-term mean-reversion strategies.
- Lempérière et al. do not appear to include a short-term reversal strategy; any placement of reversal on their Sharpe-skew line is inference.
- Trend-following ζ\* and Sharpe from Lempérière et al. not retrieved.

## Q4. Trend filters on mean reversion (e.g., long only above the 200-day MA): drawdown reduction and cost

### Takeaway
I found **no peer-reviewed study that directly tests a long-term trend filter on a short-term index mean-reversion strategy**. The indirect evidence points to a clear trade-off.
- **What the filter removes:** the highest-volatility, post-decline states. That is where:
  - short-term reversal profits are *largest* (Nagel 2012; Nguyen 2020: reversal profits higher after down markets);
  - index autocorrelation is most negative (Bogousslavsky-LeBaron-Pontiff; Gu & Finnerty).
- **What it protects against:** the bear-market regimes where catching falling knives produces the steamroller losses.
- **What MA timing buys in general:** its benefit comes mainly from avoiding a few bear markets, and it has weakened over time (Zakamulin).
- **Practitioner evidence:** the filter cuts drawdowns but leaves the strategy in the market rarely, at a large cost in CAGR.

### Cited Findings
**Reversal profits are highest after down markets**
- Nguyen (2020), "Alternative reversal variable", *Finance Research Letters* 33 [abstract] — [RePEc](https://ideas.repec.org/a/eee/finlet/v33y2020ics1544612319300856.html):
  - reversal profits are significantly higher in down markets than in up markets, largely because momentum is weak in down markets;
  - a reported ratio (up-market profit ≈ one third of down-market profit) is **unverified**.
- Short-term reversal performs better after DOWN market states or when the market is volatile [abstract-level snippet, truncated] — [SMU, "Earnings momentum meets short-term return reversal"](https://ink.library.smu.edu.sg/cgi/viewcontent.cgi?article=7866&context=lkcsb_research).
- Emerging markets and US: reversal returns are conditional on market-related volatility [abstract-level] — [Hanken study, J. Multinational Fin. Mgmt.](https://research.hanken.fi/en/publications/reversal-returns-and-expected-returns-from-liquidity-provision-ev/).

**Index autocorrelation is most negative in high volatility and on down days**
- Bogousslavsky, LeBaron & Pontiff, "A Century of Market Reversals: Resurrecting Volatility" (WP; SSRN Sept 2025, rev. Nov 2025; ABFER 2023/24 version) [abstract] — [SSRN 5410662](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5410662); [ABFER PDF](https://abfer.org/media/abfer-events-2024/annual-conference/papers-investment/AC24P3015-A-Century-of-Market-Reversals--Resurrecting-Volatility.pdf):
  - volatility plays a strong role in market return autocorrelation;
  - **daily market autocorrelations are lower (more reversal) on negative-return days**, consistent with collateral concerns;
  - anticipated volume, not volume shocks, drives reversals.
- Gu & Finnerty, Dow over 103 years [secondary, as cited in the same paper]: positive autocorrelation is more frequent in low-volatility periods, negative autocorrelation in high-volatility periods — [ABFER PDF](https://abfer.org/media/abfer-events-2024/annual-conference/papers-investment/AC24P3015-A-Century-of-Market-Reversals--Resurrecting-Volatility.pdf).

**Moving-average timing: where the benefit comes from**
- Zakamulin, "A Comprehensive Look at the Empirical Performance of Moving Average Trading Strategies" (SSRN 2677212), about 155 years of US data [secondary summaries] — [SSRN](https://papers.ssrn.com/abstract=2677212); [Alpha Architect](https://alphaarchitect.com/2016/04/the-moving-average-research-king-valeriy-zakamulin/); [CXO](https://www.cxoadvisory.com/?p=27792):
  - all MA timing rules generate many false signals in both bull and bear trends, but tend to beat the market in bear states;
  - the outperformance comes mostly from the bear markets of the 1870s, 1900s, 1930s, 1970s and 2000s;
  - the rules capture the biggest down months but exclude the biggest up months;
  - no statistically significant outperformance in the second half of the sample;
  - long underperformance spells (e.g., early 1930s – late 1960s; late 1970s – early 2000s for one rule).
- Studies claiming strong MA results can suffer look-ahead bias; without it, MA timing is "only marginally better" than buy-and-hold [secondary] — [Alpha Architect](https://alphaarchitect.com/2016/04/the-moving-average-research-king-valeriy-zakamulin/).

**Practitioner backtest of the filter**
- Practitioner RSI(2) + 200-day SMA filter on the S&P 500 CFD, Oct 2016 – Oct 2026 (vendor) — [BacktRex](https://backtrex.com/en/backtests/connors-rsi-2-sp-500):
  - max drawdown −21.5% vs −35% for buy-and-hold;
  - CAGR about 1.7% vs 13.5%;
  - 73 trades in 10 years, so very low time-in-market.
  - The headline: lower drawdown, but most of the return given up.

**The rebound exclusion**
- Momentum crashes occur during market rebounds after declines in high volatility — [Daniel & Moskowitz (2016)](https://www.nber.org/papers/w20439).
- These are exactly the post-decline rebound states that a "price > 200-day MA" filter excludes for a long-only mean-reversion trader.

### Inferences
- **The filter is a tail-risk-for-return trade.** It removes exposure to the regimes with the highest *conditional* mean-reversion expected returns (high VIX, post-decline). Those are also the regimes of highest *conditional* variance and steamroller risk (2008, 2020, 2022-style).
  - Expected effect: lower max drawdown and lower left-tail, but lower total return, fewer trades and possibly long idle periods.
  - Sharpe may rise or fall depending on the sample; it is not a free lunch.
- **On QQQ in particular**, the price-vs-200-day-MA filter would have kept the strategy largely out during 2000–2002, 2008, and much of 2022. In a regime split by quarter, most "down" quarters will show near-zero exposure. Report *exposure-adjusted* returns (return per day in market) alongside raw returns.
- **Softer filters are worth testing,** given the evidence that reversal pays most in high volatility:
  - scale position size down (not to zero) below the 200-day MA;
  - require a volatility-normalized oversold threshold;
  - add a hard stop or time stop.
- **Make the regime result trustworthy:**
  - Zakamulin finds MA-timing benefits concentrated in a handful of bear markets, so a 200-day filter's backtest benefit on QQQ will hinge on very few episodes (2000–02, 2008, 2022). Statistical confidence will be low.
  - Use walk-forward and block-bootstrap evaluation, and do not tune the MA length.

### Gaps
- No peer-reviewed paper quantifying "short-term index mean reversion with vs without a 200-day MA filter" (drawdown, Sharpe, skew) was found.
- No QQQ-specific evidence.
- No 200-day-specific drawdown or whipsaw statistics from Zakamulin; the full text was inaccessible.

## Q5. Combining momentum/trend with mean reversion: diversification evidence, and combining vs regime switching

### Takeaway
The evidence consistently shows that **combining** momentum (trend) with mean reversion improves risk-adjusted returns. The main reason is the reliably **negative correlation** between momentum and (long-horizon) reversal or value.
- Balvers & Wu (2006): combination strategies across 18 national equity markets beat pure momentum and pure mean reversion.
- Asness, Moskowitz & Pedersen (2013): value-momentum correlation about −0.5 everywhere.
- Serban (2010): a combination yields higher Sharpe ratios than traditional FX strategies.

Regime *switching* can look excellent in-sample (Dobrynskaya: dynamic momentum-contrarian switch). But it depends on in-sample thresholds, and AQR's work finds timing factors is "deceptively difficult". The weight of evidence favors **static diversification across styles, with at most modest tilts**, over hard regime detection.

### Cited Findings
**Balvers & Wu (2006)**
- Balvers & Wu (2006), "Momentum and mean reversion across national equity markets", *J. Empirical Finance* 13(1):24–48:
  - combined momentum-contrarian strategies select among **18 developed equity markets** at monthly frequency;
  - they earn about **1.1%–1.7% per month excess return** and generally outperform pure momentum and pure mean-reversion strategies [abstract/introduction via ScienceDirect] — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0927539805000708);
  - the pure mean-reversion strategy earns about **13.4% annualized excess return** [paper excerpt via ResearchGate] — [ResearchGate](https://www.researchgate.net/publication/222405923_Momentum_and_mean_reversion_across_national_equity_markets);
  - the result survives factor-risk and transaction-cost adjustments [secondary].
- The often-quoted **16.7%/yr** for the combination comes from the 2002 HKIMR working paper and an Academia.edu summary. It is not confirmed in the published paper [secondary/unverified] — [HKIMR WP](https://www.aof.org.hk/uploads/publication/298/ub_full_0_2_37_wp200211_text.pdf); [Academia.edu](https://www.academia.edu/19150469/Momentum_and_mean_reversion_across_national_equity_markets).
- Model [secondary]: prices are a common trend plus a country-specific component, with momentum under 1 year and mean reversion over 3–5 years — [Quantpedia](https://quantpedia.com/strategies/mean-reversion-effect-in-country-equity-indexes).
- Sample period: 1969–1999 per the working paper [unverified for the published version].

**Serban (2010)**
- Serban (2010), "Combining mean reversion and momentum trading strategies in foreign exchange markets", *JBF* 34(11):2720–2727 [abstract] — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0378426610001883); [RePEc](https://ideas.repec.org/a/eee/jbfina/v34y2010i11p2720-2727.html):
  - applies the Balvers-Wu-type equity combination model to deviations from uncovered interest parity (UIP);
  - finds a similar pattern to stock returns, and the combination "produces higher Sharpe ratios than traditional FX strategies".
  - Exact Sharpe ratios, sample and currencies not obtained.
- Independent replication (QuantConnect; EURUSD, GBPUSD, USDCAD, USDJPY; monthly rebalancing; 3-month momentum factor plus a deviation-from-mean factor) [secondary] — [QuantConnect](https://www.quantconnect.com/research/15255/combining-mean-reversion-and-momentum-in-forex-market/):
  - model coefficients close to the paper's;
  - **returns and Sharpe "not as good as what the paper claimed"**: about 11%/yr, Sharpe ≈ 0.8, max drawdown ≈ 11%.

**Value and momentum everywhere (long-horizon reversal as the "mean reversion" leg)**
- Asness, Moskowitz & Pedersen (2013), "Value and Momentum Everywhere", *JF* — [paper PDF](https://pages.stern.nyu.edu/~lpederse/papers/ValMomEverywhere.pdf); [Swedroe/ETF.com summary](https://www.etf.com/sections/index-investor-corner/swedroe-close-look-value-momentum):
  - value and momentum are negatively correlated within and across asset classes [abstract];
  - average within-asset-class correlation about **−0.49**, about **−0.60** for individual stocks [secondary];
  - a 50/50 combination has a much higher Sharpe than either alone and less than half the volatility of either in every region [secondary].

**Regime switching vs combining**
- Dobrynskaya (2017), "Dynamic Momentum and Contrarian Trading" (HSE WP 61/FE/2017; SSRN 3041227) [abstract + secondary] — [RePEc](https://ideas.repec.org/p/hig/wpaper/61-fe-2017.html); [CXO](https://www.cxoadvisory.com/technical-trading/momentum-contrarian-equities-switching-strategy/); [CAIA](https://caia.org/node/5387):
  - the strategy holds momentum in calm times, switches to contrarian for 3 months after a market crash, then reverts;
  - contrarian positions are held in about 15% of months, 1927–2015;
  - it turns major momentum crashes into gains, with average return about 1.5× standard momentum and positive skew;
  - CXO: 17.4% vs 10.0%/yr, but the **switch threshold is set in-sample**.
- Asness (2016), "The Siren Song of Factor Timing" [secondary] — [ai-CIO](https://www.ai-cio.com/news/dont-try-to-time-factors-says-cliff-asness/); [Quantpedia](https://vvv.quantpedia.com/?p=674):
  - value-spread-based factor timing "look[s] very weak historically";
  - timing should be done "in very small doses, if at all", with possible use only at extremes.
  - Follow-up: Asness, Chandra, Ilmanen & Israel (2017), "Contrarian Factor Timing is Deceptively Difficult".
- Daniel & Moskowitz (2016): forecasting momentum's mean and variance (a *continuous* risk-management rule, not a binary regime switch) roughly doubles Sharpe — [NBER w20439](https://www.nber.org/papers/w20439).

**Practitioner combination backtests (vendor or blog, in-sample, low evidentiary weight)**
- Price Action Lab [blog]: trend on 23 futures, 2000–2024 (Sharpe 0.82), plus mean reversion. The legs were uncorrelated on average; mean reversion provided returns in crisis periods when trend stalled; the trend leg was flat mid-2015 to mid-2019 — [Price Action Lab 2024](https://www.priceactionlab.com/Blog/2024/05/trend-following-mean-reversion/).
- Algomatic Trading [blog]: drawdown correlation of **−0.13** between trend and mean-reversion systems; combined max drawdown 12.9%, MAR 0.81, but max drawdown duration still 840 days — [Algomatic](https://www.algomatictrading.com/post/why-two-strategies-are-better-than-one-trend-following-mean-reversion).
- A retail Substack RealTest study (trend on SPY plus mean reversion on S&P 500 stocks) [blog; exact post among these two not pinned down] — [setup4alpha](https://setup4alpha.substack.com/p/trend-mean-reversion-portfolio) / [intuitivequants](https://intuitivequants.substack.com/p/trend-and-mean-reversion):
  - a 50/50 mix had lower drawdown than either leg and higher MAR;
  - the 252-day rolling correlation averaged **0.32**, ranging **−0.07 to 0.67**, so diversification was unstable.

**Why the two styles complement each other**
- Time-series momentum (trend) does best in extreme markets — [MOP 2012](https://papers.ssrn.com/abstract=2089463).
- Short-term reversal's expected returns are highest when the VIX is high — [Nagel 2012](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1988706).
- Cross-sectional momentum crashes in post-decline rebounds — [Daniel & Moskowitz 2016](https://www.nber.org/papers/w20439).

### Inferences
- **Combining beats switching on robustness.** Combining is robust because it does not require identifying the regime in real time. The benefit comes from the opposite skew and payoff shapes: trend is long-convexity, mean reversion is short-convexity. Regime switching adds a model-selection layer whose in-sample advantage (Dobrynskaya) tends to shrink out-of-sample (Asness et al.).
- **What this means for the user's QQQ project:**
  - run breakout/trend and dip-buying sleeves *together* with fixed or volatility-targeted weights;
  - do not toggle between them on a detected "range-bound vs trending" label;
  - if any conditioning is used, prefer continuous scaling (e.g., by realized volatility or by distance from a long MA) over binary switches.
- **Correlation is not a constant.** The practitioner correlation range (−0.07 to 0.67) shows the diversification benefit is state-dependent and can vanish. Measure the realized correlation between the user's breakout and mean-reversion sleeves *by regime* (up/sideways/down quarters), not just full-sample.

### Gaps
- Exact Sharpe ratios, drawdowns and inter-strategy correlations from Balvers & Wu (2006) and Serban (2010) not retrieved; full texts were inaccessible.
- No peer-reviewed study found that directly compares "static combination" vs "regime-detected switching" for trend + short-term mean reversion on a single equity index.
- AMP's value-momentum result concerns *long-horizon* value/reversal (3–5 years). How well it transfers to *short-horizon* (days) reversal vs trend is inference.

## Q6. Regime dependence: when does mean reversion make or lose money?

### Takeaway
**Mean reversion makes money:**
- in high-volatility, post-decline states (high VIX, after down markets, on negative-return days);
- when liquidity providers have withdrawn;
- when dealers are long gamma (intraday);
- in range-bound regimes, where weak moves fade.

**It loses money:**
- at the onset of liquidity and deleveraging shocks (August 2007);
- during strong persistent trends and short-gamma intraday dynamics, when moves extend rather than revert;
- when volatility shocks hit (negative volatility beta).

Its raw edge has also **decayed** as markets became more liquid (1995–2007). At the index level it **reappeared with negative sign** after about 1999 as indexing grew.

### Cited Findings
**Where mean reversion makes money**
- High VIX: expected returns and conditional Sharpe from reversal "increase enormously" during turmoil (2007–09) — [Nagel 2012](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1988706). Large-stock replication: +5.37 bp over the next 5 days per VIX point — [Moreira slides](https://conferences.fuqua.duke.edu/past/documents/2018/Alan-Moreira.pdf).
- Down markets: reversal profits are significantly higher after down markets than up markets (cross-section, monthly reversal) — [Nguyen 2020, FRL](https://ideas.repec.org/a/eee/finlet/v33y2020ics1544612319300856.html).
- High volatility and negative days: market autocorrelation is lower (more reversal) when volatility is high and on negative-return days — [Bogousslavsky, LeBaron & Pontiff](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5410662). Over 103 years of the Dow, positive autocorrelation is more frequent in low volatility and negative in high volatility (Gu & Finnerty, as cited) — [ABFER PDF](https://abfer.org/media/abfer-events-2024/annual-conference/papers-investment/AC24P3015-A-Century-of-Market-Reversals--Resurrecting-Volatility.pdf).
- Dealer gamma, intraday: positive gamma imbalance goes with intraday reversal, negative with intraday momentum, amplified by illiquidity — [Barbon & Buraschi, "Gamma Fragility"](https://abarbon.com/papers/gamma-fragility). Short-gamma hedging drives end-of-day market momentum in 60+ futures, 1974–2020 — [Baltussen et al. 2021](https://pure.eur.nl/en/publications/hedging-demand-and-market-intraday-momentum/).
- Intraday momentum regime: first-half-hour → last-half-hour momentum is stronger on volatile, high-volume, recession and macro-news days — [Gao et al. 2018](https://profiles.wustl.edu/en/publications/market-intraday-momentum/).
  - Note the tension with the daily evidence: high-volatility days favor *intraday continuation into the close* and *multi-day reversal afterwards*. Baltussen et al. (2021) find the intraday momentum reverts over subsequent days.

**Where it loses money**
- Deleveraging shocks: the daily contrarian strategy suffered sharp losses in the week of 6 Aug 2007 (during a forced unwind) before rebounding — [Khandani & Lo](https://web.mit.edu/Alo/www/Papers/august07.pdf).
- Volatility shocks: reversal portfolios carry large negative volatility betas — [Drechsler, Moreira & Savov](https://rodneywhitecenter.wharton.upenn.edu/wp-content/uploads/2020/12/18-20.Drechsler2.pdf).

**Trending vs range-bound by time scale**
- Markets trend from a few hours to a few years and revert at shorter and longer scales. Within the trending regime, *weak* trends persist and *strong* trends revert. Within the reversion regime, weak trends revert and *statistically significant* trends persist — [Safari & Schmidhuber 2025](https://arxiv.org/html/2501.16772v2).
- Momentum horizon under 1 year; mean reversion over 3–5 years at the national-index level — [Balvers & Wu 2006 via Quantpedia](https://quantpedia.com/strategies/mean-reversion-effect-in-country-equity-indexes).

**Decay and secular change**
- Daily contrarian returns fell from 1.38%/day (1995) to 0.13%/day (2007 YTD) — [Khandani & Lo](https://web.mit.edu/Alo/www/Papers/august07.pdf).
- Nagel's reversal returns were under 0.2%/day before the 2007 crisis — [NBER w17653](https://www.nber.org/system/files/working_papers/w17653/w17653.pdf).
- Large-cap, cost-aware reversal still earned 30–50 bp/week net (1990–2009) — [de Groot, Huij & Zhou 2012](https://ideas.repec.org/a/eee/jbfina/v36y2012i2p371-382.html).
- Index serial dependence turned negative after about 1999 with indexing — [Baltussen, van Bekkum & Da](https://personal.eur.nl/vanbekkum/2018%20JFE%20BaltussenVanBekkumDa.pdf).
- Time-series momentum's later weakness is partly attributed to lower trend persistence and higher cross-asset correlations [secondary] — [NBIM note](https://www.nbim.no/globalassets/documents/news/2014/discussionnote_time_series_momentum_latest.pdf).

### Inferences
**Mapping to the user's regime split**

| Quarter type | Mean reversion | Breakout / trend | Notes |
|---|---|---|---|
| Sideways / range-bound | Best | Struggles | Consistent with the user's recent breakout weakness |
| Up, low-volatility | Modestly positive | Positive | Few deep dips; time-in-market low |
| Down, high-volatility | Highest *conditional* expected return but largest left-tail losses | Positive (TSMOM) | A 200-day MA filter removes most exposure here |

- **The combination fits this pattern.** Breakout/trend and mean reversion are complementary by regime, which supports running both rather than switching.
- **Use volatility, not trend direction alone, as a conditioning variable.** Volatility, dealer gamma and liquidity are the variables the literature ties most directly to mean-reversion profitability.
- **Watch the 30-minute bar horizon.** Fading intraday moves late in the session on high-volatility days runs against documented intraday momentum. Multi-day dip entries are better supported.

### Gaps
- No direct published evidence on QQQ mean-reversion performance split by up, sideways and down quarters.
- No published study quantifying trend vs range-bound regime returns for single-index short-term mean reversion with transaction costs.
- No verified evidence on post-2020 decay of index-level daily reversal (one practitioner blog reports a sharp swing in 2020; one replication reports a negative Sharpe for the Baltussen et al. strategy over 1990–2026, both unverified).
