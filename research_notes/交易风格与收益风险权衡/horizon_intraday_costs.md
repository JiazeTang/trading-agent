# Trading horizon vs returns, risk and costs: overnight vs intraday, intraday predictability, turnover/cost penalty, day-trader record (focus: SPY/QQQ, 30-min bars)

> Verification note (read first): in this session the page-fetch tool failed for every host (DNS errors) and direct downloads were blocked by the proxy. So **every number below comes from search-engine extracts of abstracts, author pages, or secondary summaries, not from reading the paper PDFs.** Each item is tagged:
> - **[abstract]**: the paper's own abstract or author listing.
> - **[secondary]**: a third-party summary (CXO Advisory, Alpha Architect, news, blogs, GitHub).
> - **[unverified]**: only one weak source, or the sources conflict.
>
> Sample period, instrument and gross/net status are given wherever the sources stated them.

## Q1. Overnight vs intraday returns: where SPY/QQQ returns are earned, and what being flat every night costs

### Takeaway
From 1993 to 2025, roughly 90% of SPY's price gain (and about 93% of QQQ's since 1999) came close-to-open. The open-to-close (intraday) leg returned close to zero over the full sample, and was negative for QQQ in 1999–2006. A strategy that goes flat at every close therefore gives up almost all of the passive equity drift, and any edge has to come from intraday timing. In exchange it avoids gap risk.

There are two caveats:
- The overnight edge is too small and too noisy to harvest as a standalone trade after costs.
- The 2–3 a.m. part of the overnight drift in E-mini futures has disappeared since 2021.

### Cited Findings
**Cliff, Cooper & Gulen (2008), "Return differences between trading and non-trading hours: Like night and day"**
- Working paper dated July 2007; the published author order is Cliff, Cooper, Gulen. The paper splits returns into four windows: Night (4:00 p.m.–9:30 a.m.), AM (9:30–10:30), Mid-day (10:30–15:00) and PM (15:00–16:00). — [CXO Advisory summary](https://www.cxoadvisory.com/calendar-effects/buy-at-the-close-and-sell-at-the-open) [secondary]
- S&P 500 stocks, 1993–2006 (gross):
  - Average overnight return: **0.028% to 0.048% per day**, depending on the averaging method.
  - Average daytime return: **−0.028% to +0.002% per day**.
  - The same pattern holds for equity indexes, index futures and ETFs.
  - — [CXO Advisory](https://www.cxoadvisory.com/calendar-effects/buy-at-the-close-and-sell-at-the-open) [secondary]

**Kelly & Clark (2011), "Returns in trading versus non-trading hours: The difference is day and night"** (Journal of Asset Management 12(2): 132–145)
- Broad-index ETFs, QQQ, 1999–2006 (gross): the close-to-open risk premium was "strongly positive" and the open-to-close premium "strongly negative".
- The close-to-open premium also had lower volatility, so overnight holding had the higher Sharpe ratio. — [Lafayette DSpace](https://dspace.lafayette.edu/handle/10385/1012); [RePEc author page](https://ideas.repec.org/f/pke205.html) [abstract]

**SPY and QQQ, longer samples (practitioner sources, price-only, gross)**
- SPY, 29 Jan 1993 – 15 Nov 2025, log-return decomposition:
  - Cumulative overnight gain ≈ **1,105.6%**; cumulative intraday gain ≈ **26.8%**.
  - Overnight-minus-intraday test: p ≈ 0.054.
  - — [TradingView / EdgeTools](https://www.tradingview.com/chart/SPY/5fk9yQhZ-The-Overnight-Wealth-Machine/) [secondary; non-peer-reviewed]
- Overnight-only holding captured about **90.6%** of SPY's buy-and-hold return (1993–2024) and about **93%** of QQQ's (from 1999). The figures reported were SPY 530.5 vs 480.6 and QQQ ~462 vs ~429; the units are unclear. — [Redfame journal paper](https://redfame.com/journal/index.php/aef/article/download/7705/6965) [secondary; low-tier journal]
- SPY 1993–2024: overnight-only ≈ **865%** vs buy-and-hold ≈ **996%**. — [Spintwig backtest](https://spintwig.com/long-spy-day-of-week-equity-backtest) [secondary]
- CXO Advisory (SPY, Jan 1993 – Aug 2017): the overnight advantage over intraday "is not stable over time". — [CXO Advisory](https://www.cxoadvisory.com/calendar-effects/spy-by-day-of-week-and-overnight/) [secondary]

**Lou, Polk & Skouras (2019), "A tug of war: Overnight versus intraday expected returns"** (JFE 134(1): 192–213)
- US stocks, 1993–2013 (gross). Firm-level overnight and intraday returns each show continuation that lasts for years, offset by a cross-period reversal effect.
- Across 14 strategies, "profits are either earned entirely overnight (for reversal and a variety of momentum strategies) or entirely intraday, typically with profits of opposite signs across these components."
- The smoothed overnight-minus-intraday spread of a strategy forecasts its close-to-close performance.
- — [LSE Research Online](https://researchonline.lse.ac.uk/id/eprint/87481) [abstract]
- Working-paper figures for momentum:
  - Overnight momentum monthly standard deviation **4.02%** vs **7.85%** close-to-close; Sharpe **0.77 vs 0.31**.
  - Conditioning variables move the overnight-minus-intraday momentum spread by about **2% per month**.
  - Momentum is overnight-only in both 1993–2002 and 2003–2013, and is stronger in large caps and high-price stocks.
  - — [NBER conference draft](https://conference.nber.org/confer/2015/APf15/Lou_Polk_Skouras.pdf); [Internet Appendix](https://personal.lse.ac.uk/loud/ATugofWar_appendix.pdf); [FMG DP744](https://www.fmg.ac.uk/sites/default/files/publications/DP744.pdf) [secondary extracts of working paper]
- I did **not** find a market-level "share of equity premium earned overnight" number from this paper.

**Hendershott, Livdan & Rösch (2020), "Asset pricing: A tale of night and day"** (JFE 138(3): 635–662)
- Beta is **positively** related to overnight returns and **negatively** related to trading-day returns, in the US and internationally.
- The CAPM "holds overnight", and its failure comes entirely from open-to-close returns. — [IDEAS/RePEc](https://ideas.repec.org/a/eee/jfinec/v138y2020i3p635-662.html); [AEA 2019 listing](https://aeaweb.org/conference/2019/preliminary/paper/G852NrtR) [abstract]

**Boyarchenko, Larsen & Whelan, "The Overnight Drift"** (RFS 36(9), 2023, 3502–47)
- E-mini S&P 500 futures: **almost 100% of the US equity premium** was earned between 2:00 and 3:00 a.m. ET.
- The NY Fed 2021 summary gives about **3.6% annualized** for that hour, 1998–2019.
- Mechanism: the drift is tied to dealer inventory risk from **closing order imbalances**.
- Selloffs are followed by robust positive overnight reversals; rallies by much weaker ones. — [NY Fed SR917](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr917.pdf); [IDEAS](https://ideas.repec.org/p/fip/fednls/103479.html); [CXO](https://www.cxoadvisory.com/?p=33743) [abstract/secondary]

**Post-publication decay (Liberty Street Economics, 1 July 2026, "The Disappearing Overnight Drift", same authors)**
- With five more years of data, the 2–3 a.m. window, previously about **3.7% p.a.** and **more than 60% of the contract's 5.9% annualized close-to-close return**, has averaged **close to zero since 2021**.
- The same holds in **E-mini Nasdaq-100 (NQ)** and Dow (YM) futures.
- The main explanation is less-dispersed closing order imbalances. A third-party summary says imbalance dispersion fell from 6.5% to 2.9% [unverified]. — [Liberty Street Economics](https://libertystreeteconomics.newyorkfed.org/2026/07/the-disappearing-overnight-drift/) [primary blog by the authors]

**Harvesting the overnight effect directly, net of costs**
- Alpha Architect guest study: buy SPY at the close and sell at the open, Jan 1993 – Jan 2020, with historical bid-ask spreads plus a $0.01/share commission.
  - Overnight still beats intraday gross and net, but statistical robustness is low.
  - The authors conclude the anomaly is "more of a random walk than it is a repeatable trading strategy".
  - — [Alpha Architect](https://alphaarchitect.com/trading-costs-wipe-out-the-overnight-return-anomaly/) [secondary]
- Other sources agree that small trading costs "almost totally eliminate" the gains of an overnight-only strategy. — [Nasdaq](https://www.nasdaq.com/articles/like-night-and-day); [QuantConnect](https://quantconnect.com/research/15296/overnight-anomaly); [Elm Wealth 2025](https://elmwealth.com/night-shift/) [secondary]
- NightShares launched overnight-only ETFs in late 2022 to exploit the drift. — [Elm Wealth](https://elmwealth.com/night-shift/) [secondary]

### Inferences
- **The TradingView SPY numbers are internally consistent.**
  - (1 + 11.056) × (1 + 0.268) − 1 ≈ 14.3×, which matches SPY's price rise from about $44 (1993) to about $670 (Nov 2025).
  - In log terms, overnight is ln(12.06) ≈ 2.49 and intraday is ln(1.27) ≈ 0.24, so **about 91% of price appreciation was overnight and about 9% intraday**.
  - These are price returns. Ex-dividend drops happen at the open (inside the overnight window), so in total-return terms the overnight share would be even higher.
- **What a flat-every-night QQQ strategy gives up.** Over 1993–2025 it would have forfeited roughly 90% of the passive drift. Its benchmark should be intraday buy-and-hold (open-to-close), not close-to-close buy-and-hold. Otherwise, comparing against QQQ buy-and-hold in "up" quarters will look bad mostly because of the missed overnight drift, not because of poor timing.
- **The risk side cuts the other way.**
  - Kelly & Clark find the overnight leg of QQQ had lower volatility as well as higher returns (1999–2006).
  - Lou, Polk & Skouras find overnight momentum legs have about half the volatility of close-to-close.
  - So on these samples, overnight holding was not the "riskier" half on average. Gap risk shows up mainly as tail and jump risk (earnings, macro news, weekends), not as higher average variance.
- **Regime relevance.** Boyarchenko et al. find strong overnight rebounds after selloffs. So in "down" or high-volatility quarters, a strategy that is flat at the close may miss the overnight rebound after down days. This was true in 1998–2019; the 2–3 a.m. component has faded since 2021.
- **Beta and holding period.** Hendershott et al. find high-beta exposure is compensated overnight but not intraday. That points the same way for a high-beta index like QQQ vs SPY: intraday long exposure to beta has historically not been rewarded on its own. This is an analogy from cross-sectional results, not a tested QQQ time-series claim.

### Gaps
- No primary-source number was found for the share of QQQ's total variance (or drawdowns) that comes from overnight gaps vs intraday moves. I also found no published comparison of tail risk (largest gaps) vs intraday drawdowns for QQQ.
- No peer-reviewed SPY/QQQ overnight vs intraday decomposition covering 2020–2026 was found. The 2025 TradingView series is non-peer-reviewed. Whether the whole overnight premium (not just the 2–3 a.m. futures window) has shrunk after 2021 is unverified.
- The exact Cliff/Cooper/Gulen ETF-level (SPY/QQQ) numbers and their published-journal citation could not be confirmed. The task lists it as 2008 "Cooper, Cliff & Gulen"; the sources list the author order as Cliff, Cooper, Gulen.
- I could not confirm whether the NightShares ETFs were liquidated (I believe they were closed in 2023, but this is unverified).

## Q2. Intraday momentum: Gao–Han–Li–Zhou (2018), Baltussen–Da–Lammers–Martens (2021), and leveraged-ETF rebalancing (Cheng & Madhavan 2009)

### Takeaway
Two return windows predict the last half-hour on SPY:
- The first half-hour return, measured from the prior close, has in-sample R² ≈ 1.6% and out-of-sample R² ≈ 1.4% (1993–2013).
- The rest-of-day return predicts the last 30 minutes across more than 60 futures (1974–2020).

The effect is stronger on high-volatility, high-volume, recession and macro-news days. It is concentrated when option dealers are net **short gamma**, and leveraged-ETF rebalancing adds to it. When dealers are **long gamma**, the effect weakens or turns into mean reversion. Evidence on decay is thin, but one non-peer-reviewed test finds the unconditional effect gone on SPX in 2022–2026.

### Cited Findings
**Gao, Han, Li & Zhou (2018), "Market intraday momentum"** (JFE 129(2): 394–414)
- SPY, 1993–2013: the first half-hour return since the previous close predicts the last half-hour return.
- The effect is "stronger on more volatile days, on higher volume days, on recession days, and on major macroeconomic news release days".
- It also exists in ten other actively traded domestic and international ETFs.
- The authors explain it by infrequent-rebalancing traders and late-informed traders trading late in the day.
- — [EconPapers](https://econpapers.repec.org/article/eeejfinec/v_3a129_3ay_3a2018_3ai_3a2_3ap_3a394-414.htm); [SSRN 2440866](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2440866) [abstract]
- Predictive R² (gross, no costs):
  - First half-hour alone, in sample: **1.6%**. — [SSRN/ResearchGate listing](https://www.researchgate.net/publication/272303487_Intraday_Momentum_The_First_Half-Hour_Return_Predicts_the_Last_Half-Hour_Return) [abstract-level]
  - Out of sample: **1.4%** with the first half-hour alone, **2.0%** when combined with the 12th half-hour return. — [Klagenfurt/SSRN-hosted copies via search](https://www.smallake.kr/wp-content/uploads/2015/01/SSRN-id2440866.pdf) [secondary extract]
- Earlier working paper (SPY, Jan 1999 – Dec 2012):
  - First half-hour R² ≈ **0.02**.
  - First plus 12th half-hour R² ≈ **0.035**.
  - On high first-half-hour-volatility days R² ≈ **0.048**.
  - — [CXO Advisory](https://cxoadvisory.com/calendar-effects/first-and-last-half-hours-of-trading-linked) [secondary]
- The annual return and Sharpe ratio of the paper's market-timing strategy could **not** be verified in this session (see Gaps).

**Baltussen, Da, Lammers & Martens (2021), "Hedging demand and market intraday momentum"** (JFE 142(1): 377–403)
- Sample: more than 60 futures, 1974–2020 (17 equity index, 16 government bond, 21 commodity and 8 currency futures).
- The last 30 minutes before the close are positively predicted by the rest-of-day return. The effect is "economically and statistically highly significant" and **reverts over the next days**.
- The authors link it to gamma hedging by option market makers and **leveraged ETFs**: hedging a short-gamma position means trading in the direction of the price move. — [IDEAS](https://ideas.repec.org/a/eee/jfinec/v142y2021i1p377-403.html); [EUR repository](https://pure.eur.nl/en/publications/hedging-demand-and-market-intraday-momentum/); [SSRN 3760365](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3760365) [abstract]
- Momentum is concentrated on **negative net-gamma days**. Positive-gamma days show a "dampening… relative mean reversion" (wording from a related follow-up paper). — [EFMA 2021 "End-of-Day Momentum in the Cross-Section and Option Hedging"](https://www.efmaefm.org/0EFMAMEETINGS/EFMA%20ANNUAL%20MEETINGS/2021-Leeds/papers/EFMA%202021_stage-2049_question-Full%20Paper_id-237.pdf) [secondary]
- A secondary write-up reports, for negative-gamma days, coefficient **6.63** (t = 4.78) and R² **3.58%**, with an insignificant positive-gamma coefficient. — [danfin.net](https://danfin.net/intraday-momentum-final-30-minutes) [**unverified**; not checked against the paper]

**Cheng & Madhavan (2009), "The Dynamics of Leveraged and Inverse Exchange-Traded Funds"** (Journal of Investment Management 7(4))
- Daily re-leveraging "can exacerbate volatility towards the close".
- Leveraged ETF gross returns contain an embedded path-dependent option that can destroy value for buy-and-hold investors. — [JOIM](https://joim.com/dynamics-leveraged-inverse-exchange-traded-funds) [abstract]
- A Federal Reserve FEDS paper (2013-48) cites Cheng & Madhavan and Bai et al. (2012): leveraged ETFs rebalance in the **last hour of trading**, and aggregate rebalancing puts price pressure on end-of-day S&P 500 returns. — [Federal Reserve FEDS 2013-48](https://www.federalreserve.gov/pubs/feds/2013/201348/) [secondary]

**Decay and recent evidence**
- A vendor blog (gex.live, republished on dev.to) tested 1,085 SPX sessions in 2022–2026. Yearly slopes of the last half-hour on earlier returns are small and mostly insignificant (2025: +0.016, t = +1.0). The author concludes the unconditional effect is "dead in the 0DTE era". — [dev.to / FirmTape](https://dev.to/firmtape/intraday-momentum-is-dead-in-the-0dte-era-we-measured-it-on-1085-spx-sessions-43g0) [**unverified**, non-peer-reviewed]
- Cross-market evidence: intraday time-series momentum has been studied globally (Li, Sakkas & Urquhart) and in China. — [Reading accepted version](https://centaur.reading.ac.uk/95566/1/Accepted-Version.pdf); [QUB China paper](https://pureadmin.qub.ac.uk/ws/files/194643805/Intraday_Time_series_Momentum_Evidence_from_China.pdf) [titles only; numbers not extracted]

### Inferences
- **Mapping to 30-minute bars.** For a 13-bar QQQ day, the published signal is:
  - Predictor: bar 1 (09:30–10:00), measured from the **prior close** so the overnight gap is included. Optionally add bar 12 (15:00–15:30).
  - Target: bar 13 (15:30–16:00).
- **Measuring the signal from the open discards part of it.** Gao et al. define the first half-hour return from the previous close. A strategy that is flat overnight can still use the gap as information; it just doesn't hold the gap.
- **R² of 1.4–2.0% is economically meaningful but leaves a thin per-trade edge.** The strategy trades at most one 30-minute window per day, so the expected gross return per trade is a fraction of the last half-hour's volatility, which is only a few basis points. Costs therefore need to stay well under about 1 bp round trip for this signal alone to be worth trading (see Q5 for QQQ cost levels).
- **Regime implication.** Predictability is stronger in recessions and on high-volatility days, and dealers tend to be short gamma in selloffs. Expect intraday momentum on bars 1/12 → 13 to show up mainly in **down / high-volatility quarters**, and mean reversion or noise in calm up-trending, long-gamma regimes. This is consistent with Baltussen et al., but not directly tested on QQQ in the sources I found.
- **Leveraged-ETF rebalancing for QQQ.** The standard leveraged-ETF rebalancing formula is: rebalancing flow ≈ L(L−1) × AUM × (day's return).
  - TQQQ (L = 3): L(L−1) = 6. SQQQ (L = −3): L(L−1) = 12.
  - Both are positive, so both trade in the direction of the day's move near the close.
  - The formula is commonly attributed to Cheng & Madhavan, but I did not see it in the paper's text in this session.
  - This end-of-day flow is one of the hedging channels Baltussen et al. point to, which makes QQQ a natural candidate for last-bar momentum on large-move days.

### Gaps
- I could not verify the market-timing strategy's annualized return and Sharpe in Gao et al. A commonly repeated figure is about 6.7% p.a. with Sharpe about 1.1, but no source in this session confirmed it, so it is **not used**. The same goes for any net-of-cost results in that paper.
- Baltussen et al.'s exact R² numbers by gamma sign, their strategy Sharpe ratios, and their Nasdaq-100-specific results were not retrieved.
- No study was found that quantifies TQQQ/SQQQ rebalancing flow as a share of QQQ closing volume, or its incremental predictive power for QQQ's last bar.
- No peer-reviewed post-2020 out-of-sample test of Gao et al. on SPY or QQQ was found. Reports of decay rest on one vendor blog.

## Q3. Intraday periodicity: Heston, Korajczyk & Sadka (2010)

### Takeaway
In the cross-section of US stocks, a stock's return in a given half-hour interval predicts its return in the **same interval** on later days (lags of 13, 26, 39… half-hours). The effect lasts at least 40 trading days and is strongest in the first and last half-hours. At very short lags (within an hour) returns **reverse**, which the authors attribute to bid-ask bounce and temporary liquidity imbalances.

### Cited Findings
- Journal of Finance 65(4): 1369–1407 (2010). — [Kellogg](https://www.kellogg.northwestern.edu/academics-research/research/detail/2010/intraday-patterns-in-the-cross-section-of-stock-returns); [arXiv 1005.3535](https://ar5iv.arxiv.org/html/1005.3535) [abstract]
- Design and main result:
  - The trading day is split into **13 half-hour intervals**, the same structure as the user's 30-minute QQQ bars.
  - Returns show significant **positive** relations at lags of 13, 26, 39… intervals.
  - The effect lasts **at least 40 trading days**; the 2008 working paper said "over twenty".
  - — [UH working paper](https://www.bauer.uh.edu/departments/finance/documents/Heston_Korajczyk_Sadka_paper_UH.pdf); [arXiv](https://ar5iv.arxiv.org/html/1005.3535) [abstract]
- Interval and short-lag effects:
  - The continuation is "more pronounced for, but not restricted to, the first and last half-hour periods".
  - Within the day, returns are **negatively** related to recent returns. The authors attribute this to bid-ask bounce and lack of resiliency: temporary imbalances lasting under an hour.
  - — [arXiv](https://ar5iv.arxiv.org/html/1005.3535) [abstract]
- Explanations ruled out:
  - Volume, order imbalance and volatility show similar periodic patterns but do not explain the return pattern. Spreads do not explain it either.
  - The pattern is not driven by size, systematic risk premia or S&P 500 inclusion.
  - — [Kellogg](https://www.kellogg.northwestern.edu/academics-research/research/detail/2010/intraday-patterns-in-the-cross-section-of-stock-returns) [abstract]
- Replication: Chen et al. ("Investor clientele and intraday patterns…") find the pattern in the UK and Brazil but "lacklustre" evidence in China. — [Aston](https://research.aston.ac.uk/en/publications/investor-clientele-and-intraday-patterns-in-the-cross-section-of-); [Northampton](https://pure.northampton.ac.uk/en/publications/investor-clientele-and-intraday-patterns-in-the-cross-section-of-/) [abstract]

### Inferences
- **Relevance to a single-asset QQQ strategy.** HKS is a **cross-sectional** (relative-return) result for individual stocks, so its direct transfer to an index ETF's time series is untested here. A cheap feature to try is the same-bar return averaged over the past N days (e.g., N = 20–40), especially for bars 1 and 13.
- **Bar-to-bar reversal is mostly noise at QQQ's scale.** The within-hour reversal comes from bid-ask bounce and liquidity effects. For a $0.01-tick, sub-basis-point-spread ETF like QQQ that component should be tiny. Apparent 30-minute reversal "alpha" in a backtest built on last-trade prices could partly be bid-ask bounce; using mid-quote bars removes this artefact.
- **A daily-frequency periodic pattern implies little turnover if done right.** One trade per day in a fixed bar has the same cost profile as Gao et al.'s single-window strategy (see Q5 arithmetic).

### Gaps
- No published estimate was found of HKS-style same-interval continuation for SPY or QQQ themselves (index time series), nor post-2005 decay evidence for the US cross-section.
- Magnitudes (bps per half-hour, t-statistics) were not retrieved.

## Q4. Zarattini, Aziz & Barbon (2024), "Beat the Market", and QQQ applications

### Takeaway
The paper's intraday trend-following model on SPY checks for signals every :00 and :30, a 30-minute grid that matches the user's setup. It reports 19.6% annualized net, Sharpe 1.33, 2007–early 2024. Its cost assumptions are light ($0.0035/share commission plus $0.001/share slippage), and it uses leverage up to 4×.

Independent replications show large in-sample to out-of-sample drops, one to roughly zero. The authors' related QQQ opening-range-breakout paper reports large gains, but one replication finds them gross-only and about zero or negative after spread and slippage.

### Cited Findings
**Headline results and cost assumptions**
- SPY, 2007 – early 2024, **net of costs**: total return **1,985%**, annualized **19.6%**, **Sharpe 1.33**. — [SSRN 4824172](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4824172); [SFI Research Paper 24-97](https://www.sfi.ch/de/publications/n-24-97-beat-the-market-an-effective-intraday-momentum-strategy-for-s-p500-etf-spy); [St. Gallen repository](https://www.alexandria.unisg.ch/handle/20.500.14171/122124) [abstract]
- The model opens trend-following positions when intraday price action shows abnormal demand or supply imbalance, and uses dynamic trailing stops. The abstract says the authors "assess the impact of commissions and slippage". — [IDEAS](https://ideas.repec.org/p/chf/rpseri/rp2497.html) [abstract]
- Assumed costs: **$0.0035/share commission plus $0.001/share slippage**. The authors also study sensitivity to VIX, day of week, "level of trading frictions" and recent market direction. — [CXO Advisory](https://www.cxoadvisory.com/momentum-investing/complex-intraday-time-series-momentum-strategy-applied-to-spy/) [secondary]

**Mechanics, as described by replications**
- "Noise area": the average absolute move from the open at each minute over the prior **14 days**. The bands are anchored to max/min(today's open, yesterday's close) to handle gaps.
- Signal checks at every HH:00 and HH:30 from 10:00:
  - Long if price is above the upper band **and** above VWAP.
  - Short if below the lower band and below VWAP.
  - Flat otherwise.
- The trailing stop is the band or VWAP, whichever is tighter.
- Position sizing targets **2% daily volatility**, capped at **4× leverage**. All positions are closed by the end of the day.
- — [GitHub replications, e.g. svettelnova](https://github.com/svettelnova/intraday-momentum-spy); [nikolaosntinas18](https://github.com/nikolaosntinas18/spy-intraday-momentum) [secondary]

**Unresolved and replication evidence**
- A Concretum-hosted copy shows a 2007–2024 row with total return **178%**, **6.2%** annualized, **10.9%** volatility and **Sharpe 0.61**. It is unclear which variant or benchmark row this is, and it conflicts with the headline figures. — [St. Gallen bitstream](https://alexandria.unisg.ch/bitstreams/a99aba00-f967-49b3-aceb-f544dc386e0b/download) [**unverified**]
- Independent replications (non-peer-reviewed GitHub):
  - One reports Band+VWAP train Sharpe **1.43** vs test Sharpe **≈ −0.01** on 2020–2026 data.
  - Another reports baseline train **1.07** vs test **0.75**.
  - One repo runs **SPY and QQQ from 2016** with slippage and commissions; its results were not extracted.
  - Another tests with $0.01–$0.02/share slippage, which is 3–20× the paper's assumption.
  - — [codecat-ops replication](https://github.com/codecat-ops/zarattini-2024-momentum-spy); [patrickobirmingham PR](https://github.com/patrickobirmingham-eng/POB-CL-DT/pull/13); [Quant Macro review](https://quantmacro.substack.com/p/paper-review-an-effective-intraday) [**unverified**, low-authority]

**QQQ-specific related paper: Zarattini & Aziz (2023), "Can Day Trading Really Be Profitable?"** (SSRN 4416622)
- Design: 5-minute opening-range breakout on **QQQ, 2016–2023**. Go long or short in the direction of the first 5-minute candle.
- Results reported in the abstract:
  - Annualized alpha of **33% net of commissions**.
  - Implemented with **TQQQ** because of broker leverage limits: **1,484%** total return vs **169%** for QQQ buy-and-hold over the same period.
  - — [SSRN 4416622](https://papers.ssrn.com/abstract=4416622); [CXO](https://www.cxoadvisory.com/technical-trading/day-trading-with-an-opening-range-breakout-strategy) [abstract/secondary]
- A LinkedIn summary cites different numbers: Sharpe 2.1, max drawdown 9.4%, 8,242% with TQQQ. These probably come from a different (stocks-in-play) paper, so the sources conflict. — [search summary of LinkedIn](https://ch.linkedin.com/in/carlozarattini) [**unverified**]
- Independent critique (MQL5 blog): the rule was replicated on 5 index CFDs, 2015–2026.
  - Gross results reproduce on Nasdaq futures.
  - Net of costs, no market is distinguishable from zero, and 4 of 5 are negative.
  - The original charges commission but **no spread and no slippage**, and has **no out-of-sample period**.
  - — [MQL5 blog](https://www.mql5.com/en/blogs/post/776235) [secondary, non-peer-reviewed]

### Inferences
- **Treat Zarattini et al. as an upper bound.** Reasons:
  - The authors are practitioners selling courses and strategies (Concretum, Bear Bull Traders).
  - Costs are light, and leverage of up to 4× inflates returns relative to the 1× unlevered setup.
  - Independent replications show sharp out-of-sample deterioration.
- **For a 30-minute QQQ engine, the transferable design ideas are:**
  - A volatility-scaled "noise band" around the open/prior close (trade only on abnormal moves).
  - A VWAP filter.
  - Trailing stops.
  - Volatility-targeted sizing.
  - Flat at the close. This avoids the overnight gap but forfeits the drift (Q1).
- **Regime split to expect.** Trend-following intraday tends to make money on directional, high-volatility days (more common in down quarters) and bleed through stop-outs in range-bound, sideways quarters. The paper examined VIX and "recent market direction" sensitivity, but I did not retrieve those numbers.

### Gaps
- I did not retrieve the paper's max drawdown, number of trades per year, average holding time, cost-sensitivity table (net returns at higher slippage), or results by VIX regime.
- No peer-reviewed follow-up applying the noise-area/VWAP model to QQQ was found. Only GitHub replications claim to.

## Q5. Costs and turnover: Novy-Marx & Velikov (2016), realistic SPY/QQQ costs, and break-even cost

### Takeaway
Novy-Marx & Velikov show that, for stock anomalies, high turnover kills net returns: few strategies with one-sided monthly turnover above 50% survive costs. For QQQ the cost **per unit of turnover** is tiny: quoted spreads are around 0.2–0.4 bp, and commissions are at most a fraction of a basis point. But a 30-minute strategy's turnover is 10–100× higher than any anomaly portfolio.

The binding constraint is therefore **turnover × cost per trade versus gross edge per trade**. Break-even costs for 30-minute strategies often fall to just a few basis points, or below one.

### Cited Findings
**Novy-Marx & Velikov (2016), "A Taxonomy of Anomalies and Their Trading Costs"** (RFS 29(1): 104–147)
- "Most of the anomalies… with **one-sided monthly turnover lower than 50%** continue to generate statistically significant net spreads, at least when designed to mitigate transaction costs. Few of the strategies with higher turnover do." — [NBER w20721](https://www.nber.org/papers/w20721.pdf); [IDEAS](https://ideas.repec.org/a/oup/rfinst/v29y2016i1p104-147..html) [abstract]
- The most effective cost-mitigation technique is a **buy/hold spread**: stricter requirements for opening a position than for keeping it. — [NBER](https://nber.org/papers/w20721) [abstract]
- "Transaction costs always reduce strategy profitability, increasing data-snooping concerns". Capacity is inversely related to turnover. — [NBER](https://nber.org/papers/w20721) [abstract]
- Costs are measured with Hasbrouck (2009) effective spreads. This ignores price impact, so it is "the cost faced by a small liquidity demander". — [Alpha Architect](https://alphaarchitect.com/2017/05/trading-costs-destroy-factor-investing/) [secondary]

**SPY/QQQ spreads and cost assumptions**
- Quoted spreads: SPY **0.002%** (~0.2 bp) and QQQ **0.004%** (~0.4 bp), date and method not stated. — [ETF Central (TrackInsight data)](https://www.etfcentral.com/news/etf-comparison-qqq-etf-versus-spy-etf) [secondary]
- SPY average spread **0.0032%** (~0.32 bp). — [etf.com](https://www.etf.com/sections/news/etfs-highest-lowest-trading-spreads) [secondary]
- Cost assumptions used in SPY intraday research:
  - Zarattini et al.: $0.0035/share commission plus $0.001/share slippage. — [CXO](https://www.cxoadvisory.com/momentum-investing/complex-intraday-time-series-momentum-strategy-applied-to-spy/) [secondary]
  - Alpha Architect's overnight study: historical bid-ask spread plus $0.01/share commission. — [Alpha Architect](https://alphaarchitect.com/trading-costs-wipe-out-the-overnight-return-anomaly/) [secondary]
- The MQL5 replication of the QQQ ORB strategy shows that adding spread and slippage turned gross-positive results into roughly zero or negative net. — [MQL5](https://www.mql5.com/en/blogs/post/776235) [secondary]

### Inferences

**(a) Per-side cost for a retail-size QQQ order in regular hours.** Assume a price of about $500–600:
- A 1-cent tick is ≈ 0.17–0.20 bp of the quoted spread, so the half-spread is ≈ 0.1 bp.
- $0.0035/share commission ≈ 0.06–0.07 bp.
- $0.001/share slippage ≈ 0.02 bp.
- Total ≈ **0.2 bp per side, about 0.4–0.5 bp round trip** in normal conditions.

For robustness, model **1–2 bp round trip** as a base case and **5 bp** as a stress case. The extra margin covers:
- open and close auction prints;
- fast markets and news;
- stop orders filled through the stop;
- wider spreads in the first minutes after 09:30.

Commission-free retail brokers remove the explicit commission but route orders for payment for order flow, so execution quality is the hidden cost. All of this is my arithmetic from the cited spread and commission figures, not a published estimate.

**(b) Turnover arithmetic for 13 bars × 252 days = 3,276 bars per year.**

| Trading pattern | Round trips per year | Drag at 1 bp RT | Drag at 2 bp RT | Drag at 5 bp RT |
|---|---|---|---|---|
| One intraday trade per day, flat at the close | 252 | 2.5% / yr | 5.0% / yr | 12.6% / yr |
| Average holding 4 bars | ≈ 819 | ≈ 8.2% / yr | ≈ 16.4% / yr | — |
| Position changes every bar | ≈ 3,276 | ≈ 33% / yr | — | — |

Switching long↔short counts as two round trips. For comparison, QQQ's long-run buy-and-hold return is about 10–18%/yr. In Novy-Marx & Velikov terms, a daily round-trip strategy has about **2,000% one-sided monthly turnover** (≈ 21 round trips × 100%), roughly 40× their 50% survival threshold. It survives only because QQQ's per-trade cost is about 100× smaller than typical single-stock effective spreads.

**(c) Break-even cost per trade.**
- Per trade: c* (round trip) = average gross return per trade.
- Annual equivalent: c* = gross annual return ÷ round trips per year.
- Examples for a 15% gross annual return:
  - 252 trades → c* ≈ 6 bp.
  - 819 trades → ≈ 1.8 bp.
  - 3,276 trades → ≈ 0.46 bp.

Report c* alongside Sharpe for each regime (up / sideways / down quarters). A strategy whose c* falls below about 2 bp in any regime should be treated as cost-fragile.

**(d) Apply the Novy-Marx & Velikov buy/hold-spread idea.** Use hysteresis: enter only on a strong signal and exit only when the signal decays well past zero, rather than flipping at a single threshold. This is the cheapest way to cut 30-minute turnover without dropping the signal.

### Gaps
- No primary exchange or issuer source (Invesco, Nasdaq TAQ studies) was found giving QQQ **effective** spreads by time of day (open, midday, close), or market impact for retail size. The ETF Central and etf.com figures are undated quoted spreads.
- No published estimate was found of realistic QQQ slippage for stop or market orders at 30-minute decision points.
- The Gao et al. and Baltussen et al. papers' own net-of-cost or break-even cost numbers were not retrieved.

## Q6. Empirical record of short-horizon / day traders

### Takeaway
Large administrative datasets agree:
- **Taiwan:** fewer than 1% of day traders are predictably profitable net of fees.
- **Brazil:** 97% of persistent day traders lost money.
- **India:** about 70% of intraday cash-equity traders lost money in FY23.

Skill exists in a tiny right tail and persists (past winners keep outperforming), but most traders lose, costs magnify losses, and traders do not appear to learn.

### Cited Findings
**Barber, Lee, Liu & Odean (2014), "The cross-section of speculator skill: Evidence from day trading"** (Journal of Financial Markets)
- Taiwan Stock Exchange, 1992–2006. "**Less than 1%** of the day trader population is able to predictably and reliably earn positive abnormal returns net of fees." — [Berkeley/Odean working paper](https://faculty.haas.berkeley.edu/odean/papers/day%20traders/Day%20Trading%20Skill%20110523.pdf); [eScholarship](https://www.escholarship.org/uc/item/7k75v0qx) [abstract]
- Persistence, with traders ranked on the prior year:
  - Top 500 day traders earn next-period **61.3 bp/day before fees (37.9 bp after)**.
  - Bottom-ranked traders earn **−11.5 bp (−28.9 bp)**.
  - An earlier working paper reported 49.5 and 28.1 bp for the top group.
  - — [eScholarship](https://www.escholarship.org/content/qt7k75v0qx/qt7k75v0qx.pdf?t=ohrd1z) [abstract; figures differ by version]

**Barber, Lee, Liu, Odean & Zhang (2020), "Learning, fast or slow"** (Review of Asset Pricing Studies 10(1): 61–93)
- Taiwan, 1992–2006:
  - **97% of day traders are likely to lose money** in future day trading.
  - Aggregate day-trader performance is negative.
  - **74% of day-trading volume** comes from traders with a history of losses.
  - Unprofitable traders are more likely to quit, but too slowly. The results fit overconfidence and biased learning better than rational learning.
  - — [IDEAS](https://ideas.repec.org/a/oup/rasset/v10y2020i1p61-93..html); [PUC-Rio working paper](https://www.econ.puc-rio.br/uploads/adm/seminarios/Learning_fast_or_slow_180606.pdf) [abstract]

**Chague, De-Losso & Giovannetti, "Day Trading for a Living?"** (SSRN 3423101; FGV EESP TD 525)
- Brazil equity (index) futures. Individuals who started day trading in 2013–2015 and persisted for **more than 300 days**; the dataset covers **19,646** individuals.
- Results:
  - **97% lost money**.
  - Only **1.1%** earned more than the Brazilian minimum wage.
  - Only **0.5%** earned more than a bank teller's starting salary; another version says **0.4%** (about US$54/day).
  - No evidence of learning.
- — [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3423101); [FGV repository](https://repositorio.fgv.br/items/e87d04fc-4b4c-4a56-ab5a-1c84c1afde1b/full); [CXO](https://www.cxoadvisory.com/investing-expertise/day-trading-a-bust/) [abstract; versions differ]

**SEBI (India) study, released 24 July 2024**
- Sample: individual intraday traders in the equity cash segment, **FY2022-23**, about 7 million traders at the top-10 brokers (≈ 86% of individual clients).
- Results:
  - **70–71%** lost money; average loss ₹5,371.
  - Loss-makers made more trades than profit-makers.
  - Loss-makers spent an extra **57% of their trading losses** on trading costs; profit-makers spent **19% of their profits**.
  - Loss-makers were 76% of the youngest age group.
- — [Business Standard](https://www.business-standard.com/amp/markets/news/7-in-10-intraday-traders-in-equity-cash-suffered-losses-in-fy23-sebi-study-124072400975_1.html); [Cafemutual](https://cafemutual.com/news/industry/32681-7-out-of-10-intraday-traders-in-direct-stocks-incur-losses-sebi) [secondary reporting of SEBI release]

### Inferences
- **Base rates are harsh.** The base rate for a discretionary short-horizon trader beating costs is on the order of 1–3%, so a 30-minute QQQ backtest that looks profitable should be treated with strong prior skepticism. Overfitting and cost understatement are more likely explanations than durable skill.
- **Skill, where it exists, persists.** In Barber et al., past top performers continue to earn about 38 bp/day after fees. A systematic strategy should show the same persistence: stable out-of-sample, regime-by-regime net Sharpe, not just a strong full-sample number.
- **More trading predicts worse results.** In SEBI's data, loss-makers traded more and costs added more than half again to their losses. This is consistent with Q5: at 30-minute frequency, the decision on **how often to trade** matters more than the decision on **which signal**.
- **These are mostly single-stock and futures retail traders.** Taiwan and India trade stocks; Brazil trades mini-index futures. Brazil is the closest analogue to index day trading, and its outcomes are just as bad (97% lost money, the same as the Taiwan "likely to lose" share).

### Gaps
- No recent large-sample US study of retail day traders' net profitability was found in this session. Examples would be the post-2020 zero-commission era, or Robinhood/0DTE-era evidence on index ETFs specifically.
- SEBI's separate F&O study (often cited as about 9 in 10 individual F&O traders losing money) was not searched or verified here.
- No study was found isolating the profitability of **systematic** (algorithmic) retail strategies on SPY/QQQ, as opposed to discretionary day traders.
