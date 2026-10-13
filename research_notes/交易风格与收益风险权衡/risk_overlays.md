# Risk-Control Overlays: Stop-Losses, Volatility Targeting, Trend/MA Filters, and Position Sizing. Quantified Effects on Return and Risk

> **How these numbers were checked.** WebFetch could not reach any host in this session (DNS failure on every domain, including dspace.mit.edu, people.duke.edu, lehigh.edu, nber.org and ssrn.com). Every number below therefore comes from search-engine extracts of the papers, their abstracts or repository copies, or secondary summaries (CXO Advisory, Alpha Architect, Quantpedia and similar). Each item says which kind of source it rests on. Items marked **[unverified]** are still waiting on a check against the paper's own tables. "Gross" means before transaction costs. Most of the academic results are gross unless stated otherwise.

---

## 1. Stop-loss rules: when do they add value, when do they subtract, and by how much?

### Takeaway
Theory (Kaminski & Lo 2014) says a stop-loss can only add expected return when returns are serially correlated in the right way: momentum (positive autocorrelation), or regime-switching where bad regimes persist. Under a random walk a simple 0/1 stop always lowers expected return, and under mean reversion it hurts more. The empirical record splits along the same line:
- Stops add value on slow-moving, trending exposures: US equity versus bonds at monthly frequency, and cross-sectional momentum portfolios.
- Tight, high-frequency stops on individual stocks lose money net of costs, because individual stocks mean-revert at short horizons (Lo & Remorov 2017).

### Cited Findings
**Kaminski & Lo, "When do stop-loss rules stop losses?" (Journal of Financial Markets 18 (2014) 234–254; SSRN WP 2007)**
- **Framework.** A stop-loss rule is defined as a "predetermined policy that reduces a portfolio's exposure after reaching a certain threshold of cumulative losses." The paper measures its effect on expected return and volatility by comparing the portfolio with and without the overlay. The marginal effect on expected return is called the "stopping premium." — [MIT DSpace record](https://dspace.mit.edu/handle/1721.1/114876); [IDEAS/RePEc](https://ideas.repec.org/a/eee/finmar/v18y2014icp234-254.html)
- **Analytical result.** Under the Random Walk Hypothesis, simple 0/1 stop-loss rules *always decrease* a strategy's expected return. With momentum (positive serial correlation), stop-loss rules can add value. The paper also covers regime-switching processes. — [SSRN abstract 968338](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=968338); [SIFR WP abstract](https://swopec.hhs.se/sifrwp/abs/sifrwp0063.htm)
- **Empirical test, working-paper version.**
  - Data: monthly US stocks, switching into long-term US government bonds on a stop, 1950–2004.
  - Result: certain stop-loss rules add **50–100 bp per month** to buy-and-hold *during stop-out periods*. This is not 50–100 bp/month unconditionally.
  - Sources: [quant-investing summary](https://www.quant-investing.com/blog/truths-about-stop-losses-that-nobody-wants-to-believe); [SSRN 968338](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=968338). **[Unverified]:** the parameter combinations behind 50–100 bp and the size of the volatility reduction.
- **Stopped-out periods (secondary, unverified).** For a simple 10% stop that moves into long-term bonds, stocks beat bonds only about 30% of the time while the investor was stopped out. — [quant-investing summary](https://www.quant-investing.com/blog/truths-about-stop-losses-that-nobody-wants-to-believe)
- **Published JFM version.**
  - Data: daily index-futures prices, roughly 1993–2011 per a search extract.
  - Result: "at longer sampling frequencies, certain stop-loss policies can increase expected return while substantially reducing volatility."
  - This implies the benefit weakens at higher sampling frequencies.
  - Sources: [MIT DSpace](https://dspace.mit.edu/handle/1721.1/114876); [IDEAS](https://ideas.repec.org/a/eee/finmar/v18y2014icp234-254.html). Transaction-cost treatment not verified.

**Lo & Remorov, "Stop-loss strategies with serial correlation, regime switching, and transaction costs" (Journal of Financial Markets 34 (2017) 1–15)**
- **Sample.** Daily returns and bid-ask spreads for a broad sample of US common stocks, 1964–2014. Measurement windows of 1 day and 10 days; stop thresholds of 0% to −6% and 0% to −14%. — [CXO Advisory summary](https://www.cxoadvisory.com/equity-premium/stop-losses-on-stock-positions-in-depth); [ScienceDirect abstract](https://www.sciencedirect.com/science/article/abs/pii/S1386418117300472)
- **Headline result.** Tight stop-loss rules generally *underperform buy-and-hold* in a mean-variance sense, mainly because of trading costs. Stocks with high enough serial correlation can do better with stops. The reduction in downside risk is "only modest." — [ScienceDirect abstract](https://www.sciencedirect.com/science/article/abs/pii/S1386418117300472); [MIT DSpace](https://dspace.mit.edu/handle/1721.1/107017)
- **Detail (secondary).**
  - Tight daily stops underperformed because of trading costs *and negative autocorrelation (mean reversion)* in individual-stock returns.
  - Wide 10-day stops roughly *matched* buy-and-hold on a risk-adjusted basis, consistently raised skewness, and reduced maximum drawdown.
  - In simulation, tight stops improve risk-adjusted returns only when volatility and autocorrelation are high enough.
  - Wide stops can beat buy-and-hold for assets that switch between low-volatility bull regimes and high-volatility bear regimes, as long as switches are infrequent.
  - Source: [CXO Advisory](https://www.cxoadvisory.com/equity-premium/stop-losses-on-stock-positions-in-depth)

**Han, Zhou & Zhu, "Taming Momentum Crashes: A Simple Stop-Loss Strategy" (SSRN 2407199, WP 2014–2016)**
- **Rule.** For each stock held in the monthly-rebalanced cross-sectional momentum portfolio (winners minus losers), sell the stock if it falls 10% (or 15% in a later version) below its start-of-month price, and hold cash until month-end. — [SSRN copy](https://smallake.kr/wp-content/uploads/2017/03/SSRN-id2407199.pdf); [CXO Advisory](https://www.cxoadvisory.com/technical-trading/stop-losses-to-avoid-stock-momentum-crashes/)
- **Worst monthly loss, 10% stop, 1926–2011/2013 depending on version.**
  - Equal-weighted momentum: **−49.79% → −11.36%**.
  - Value-weighted momentum: **−64.97% → −23.28%**; about −14.85% if 1932 is excluded.
  - Sources: [Alpha Architect review](https://alphaarchitect.com/2016/08/taming-the-momentum-roller-coaster-fact-or-fiction/); [SSRN copy](https://smallake.kr/wp-content/uploads/2017/03/SSRN-id2407199.pdf)
- **Worst monthly loss, 15% stop.** Equal-weighted −49.79% → −17.43%; value-weighted −64.97% → −22.10%. — [SSRN copy](https://smallake.kr/wp-content/uploads/2017/03/SSRN-id2407199.pdf)
- **Return and Sharpe (the figures differ across versions).**
  - Sharpe ratio rises from **0.165 to 0.369–0.399**, i.e. more than double.
  - Average monthly return rises from about **0.99–1.01% to 1.69–1.93%**.
  - Sources: [SSRN copy](https://smallake.kr/wp-content/uploads/2017/03/SSRN-id2407199.pdf); [CICF conference version](https://www.cicfconf.org/sites/default/files/paper_811.pdf); [quant-investing summary](https://www.quant-investing.com/blog/truths-about-stop-losses-that-nobody-wants-to-believe)
- **Costs and practicality.**
  - Results are gross, hypothetical backtests.
  - The 15% version liquidates about 10% (long side) and 11% (short side) of stocks per month, which raises turnover. — [CXO Advisory](https://www.cxoadvisory.com/technical-trading/stop-losses-to-avoid-stock-momentum-crashes/)
  - The rule needs daily monitoring of every position, and Alpha Architect calls it hard for ordinary investors to implement. — [Alpha Architect](https://alphaarchitect.com/2016/08/taming-the-momentum-roller-coaster-fact-or-fiction/)

**Intraday stop-losses on index ETFs: practitioner working papers, not peer-reviewed**
- **SPY intraday momentum (Zarattini, Aziz & Barbon, "Beat the Market: An Effective Intraday Momentum Strategy for S&P500 ETF (SPY)", SFI WP 24-97).**
  - Design: trend-following entries on intraday demand/supply imbalance, with exits by "dynamic trailing stops."
  - Results, 2007 to early 2024: **1,985% total return net of costs, 19.6% annualized, Sharpe 1.33**.
  - The paper tests volatility regimes and commission/slippage sensitivity.
  - The trailing stop is not ablated in what I could see, so its marginal contribution is unknown.
  - Source: [SFI abstract](https://www.sfi.ch/fr/publications/n-24-97-beat-the-market-an-effective-intraday-momentum-strategy-for-s-p500-etf-spy)
- **QQQ 5-minute opening-range breakout (Zarattini & Aziz 2023, SSRN 4416622).**
  - Results, 2016–2023: **1,484%** for a leveraged version, against **169%** total for QQQ buy-and-hold over the same window, and a 33% annualized alpha net of commissions.
  - Uses a stop based on the opening range.
  - Source: [SSRN 4416622](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4416622)
- **Critiques of the QQQ result.**
  - An independent replication finds the edge breaks even at about **2.2¢/share slippage**. — [GitHub replication](https://github.com/giovannibrusco/zarattini-2023-orb-qqq)
  - The same replication finds that 76% of the PnL of an NQ-confirmation filter came from 2022 alone. — [GitHub replication](https://github.com/giovannibrusco/zarattini-2023-orb-qqq)
  - A review notes the model assumes no slippage and that a 9,350% variant came from a parameter search. — [Danfin review](https://danfin.net/opening-range-breakout-research)

### Inferences
- The sign of a stop-loss overlay is determined by the **autocorrelation of the underlying strategy's P&L at the stop's measurement horizon**, not by the asset.
  - For a **mean-reversion** strategy on QQQ 30-minute bars, the strategy profits from short-horizon negative autocorrelation. A stop that exits after an adverse move sells exactly when the expected reversal is largest. Theory (Kaminski-Lo random walk / mean-reversion case) and evidence (Lo-Remorov tight daily stops on mean-reverting stocks) both predict a negative stopping premium, plus extra transaction costs.
  - The exception is a *catastrophic*, wide stop, which works as insurance against regime breaks such as gap events or trend days. It costs little expected return if hit rarely.
- For a **momentum/breakout** intraday strategy, a stop matches the Kaminski-Lo momentum case and is more likely to add value. That fits the trailing-stop designs in the Zarattini et al. papers, though those papers do not isolate the stop's contribution.
- **Frequency matters.**
  - Kaminski-Lo's benefit appears "at longer sampling frequencies."
  - Lo-Remorov's daily tight stops fail while 10-day wide stops break even.
  - So 30-minute-bar stops are likely to be noise-dominated unless they are wide relative to intraday volatility, for example a multiple of ATR or realized volatility.
- **Regime view.**
  - Stops help in persistent **down** quarters, because losses compound and a stop exits early.
  - They hurt in **sideways/choppy** quarters, where the strategy gets stopped out and then sees the reversal.
  - In **up** quarters they cost a small amount: the stop-out probability times the forgone drift.
- The large Han-Zhou-Zhu improvements in average return rest on intra-month price paths of individual stocks during crash months such as 1932 and 2009. Fills at the stop price are assumed, and gap risk and costs are ignored. Treat the gains as an upper bound.

### Gaps
- Exact Kaminski-Lo numbers (stopping premium by threshold and re-entry parameter, volatility change, Sharpe change) and whether the JFM futures results are net of costs. The PDF could not be retrieved.
- Lo-Remorov's quantitative tables (Sharpe or return deltas per threshold): only secondary summaries were available.
- No peer-reviewed study found that isolates the effect of a stop-loss on an *intraday mean-reversion* strategy on an index ETF. The user should measure the autocorrelation of their own strategy's 30-minute P&L and run an ablation with and without the stop.
- Alpha Architect's "fact or fiction" post on Han-Zhou-Zhu: its full replication verdict was not retrieved.

---

## 2. Volatility targeting / volatility-managed exposure: Sharpe, alpha, left tail, and out-of-sample critiques

### Takeaway
Scaling equity (and equity-factor) exposure by inverse recent volatility reliably **shrinks the left tail**: worst months, maximum drawdown and kurtosis all fall. It **modestly raises in-sample Sharpe for equities and credit, but not for bonds, FX or commodities**. Most of the large published "alpha" depends on look-ahead in the scaling constant and on structural instability. In real-time and net-of-cost tests:
- Sharpe gains are coin-flips across factors (Cederburg et al.: 53 of 103 strategies improve, 8 significantly).
- They disappear after costs for every factor except the market (Barroso & Detzel).
- They can *increase* expected shortfall and drawdown in several non-US equity markets (Bongaerts et al.).

The biggest effect is for momentum strategies, where vol-scaling roughly doubles the Sharpe ratio and removes most crash risk.

### Cited Findings
**Moreira & Muir, "Volatility-Managed Portfolios" (Journal of Finance 72(4), 2017; NBER w22208)**
- **Core claim.** Managed portfolios that take less risk when volatility is high produce large alphas, substantially raise factor Sharpe ratios, and produce large utility gains for mean-variance investors. Shown for the market, value, momentum, profitability, ROE and investment factors, plus the currency carry trade. — [NBER w22208](https://www.nber.org/papers/w22208)
- **Market portfolio.** Alpha **4.9% per year**, appraisal ratio **0.33**, and about a **25% increase** in the buy-and-hold Sharpe ratio. — [Yale workshop version](https://law.yale.edu/sites/default/files/area/workshop/leo/leo17_moreira.pdf)
- **Across factors (2016 WP).**
  - Sharpe ratios increase by **50–100%** of the original factor Sharpe.
  - Utility gains equal **50–90% of lifetime utility** for a mean-variance investor.
  - Source: [NBER WP PDF](https://www.nber.org/papers/w22208.pdf)
- **Weighting.** The managed portfolio weights the factor by c / σ²(previous month's realized variance from daily returns). The constant c is chosen so that full-sample volatility equals the unmanaged factor's, which is the source of the look-ahead critique below.
- **[Unverified]** The exact sample end date and whether any table is net of costs. My understanding is that the market sample starts in 1926 and that the main results are gross, but I could not confirm this here.

**Harvey, Hoyle, Korgaonkar, Rattray, Sargaison & Van Hemert, "The Impact of Volatility Targeting" (Journal of Portfolio Management 45(1):14–33, 2018; Man Group authors)**
- **Sample.** 60 assets, with daily data starting as early as 1926 and ending in 2017. — [Quantpedia summary](https://quantpedia.com/the-impact-of-volatility-targeting-on-equities-bonds-commodities-and-currencies); [Duke PDF](https://people.duke.edu/~charvey/Research/Published_Papers/P135_The_impact_of.pdf)
- **Sharpe.** The improvement holds only for "risk assets" (equity and credit) and is attributed to the leverage effect, i.e. the negative return–volatility correlation. For bonds, currencies and commodities the effect on Sharpe is negligible. — [Duke PDF](https://people.duke.edu/~charvey/Research/Published_Papers/P135_The_impact_of.pdf); [Alpha Architect](https://alphaarchitect.com/volatility-targeting-improves-risk-adjusted-returns/)
- **US equities (secondary summary).** Sharpe goes from **0.40 unscaled to 0.48–0.51 vol-scaled**. — [Alpha Architect](https://alphaarchitect.com/volatility-targeting-improves-risk-adjusted-returns/)
- **Left tail.**
  - Volatility targeting reduces the likelihood of extreme returns *across all asset classes*.
  - Left-tail events are less severe because they usually occur when volatility is already elevated and notional exposure is already small.
  - Vol-scaling a risk asset effectively adds some momentum.
  - Sources: [Quantpedia](https://quantpedia.com/the-impact-of-volatility-targeting-on-equities-bonds-commodities-and-currencies); [Duke PDF](https://people.duke.edu/~charvey/Research/Published_Papers/P135_The_impact_of.pdf)
- **Portfolios.** For a 60/40 portfolio and an equity-bond-credit-commodity risk-parity portfolio, scaling at both the asset and portfolio level improves Sharpe and reduces tail events. — [ResearchGate abstract](https://www.researchgate.net/publication/328870981_The_Impact_of_Volatility_Targeting). **[Unverified]:** drawdown figures, the volatility estimator's half-life, and cost treatment.

**Cederburg, O'Doherty, Wang & Yan, "On the performance of volatility-managed portfolios" (Journal of Financial Economics 138 (2020) 95–117)**
- **Setup.** 103 equity anomaly and factor strategies. — [Lehigh PDF](https://www.lehigh.edu/~xuy219/research/COWY.pdf)
- **Direct comparison.** The vol-managed version has a higher *gross* Sharpe ratio for only **53 of 103** strategies, and only **8 of those 53** margins are statistically significant. — [Lehigh PDF](https://www.lehigh.edu/~xuy219/research/COWY.pdf); [Alpha Architect](https://alphaarchitect.com/does-portfolio-timing-based-on-volatility-signals-outperform-buy-and-hold/)
- **Spanning-regression alphas.**
  - Positive for **77 of 103** strategies.
  - But scaling to equalize full-sample volatility "unrealistically requires full-sample foresight."
  - Reasonable real-time, out-of-sample mean-variance combinations give **lower Sharpe ratios and certainty-equivalent returns for 72 of 103** strategies than the unmanaged portfolio.
  - The authors attribute this mainly to *structural instability* in the spanning regressions.
  - All figures are gross of costs.
  - Sources: [Lehigh PDF](https://www.lehigh.edu/~xuy219/research/COWY.pdf); [CXO Advisory](https://www.cxoadvisory.com/volatility-effects/does-volatility-management-work-for-equity-factor-portfolios/)
- **Replication.** An Erasmus master's thesis found "numerical differences" but "very similar" conclusions. — [EUR thesis](https://thesis.eur.nl/pub/49941/Visser_443480.pdf)

**Liu, Tang & Zhou, "Volatility-Managed Portfolio: Does It Really Work?" (Journal of Portfolio Management 46(1):38–51, 2019)**
- Volatility timing of the stock market suffers from look-ahead bias.
- After correcting for it, the strategy's maximum drawdown is about **68–93%** in nearly all cases, presumably because of embedded leverage.
- It beats the market only during the financial crisis.
- Three alternative volatility-timing rules also fail to outperform.
- Source: [WUSTL profile/abstract](https://profiles.wustl.edu/en/publications/volatility-managed-portfolio-does-it-really-work/)

**Barroso & Detzel, "Do limits to arbitrage explain the benefits of volatility-managed portfolios?" (Journal of Financial Economics 140 (2021) 744–767)**
- After transaction costs, vol-managing the **market** portfolio still gives abnormal returns.
- For the other factors, abnormal returns are roughly zero and Sharpe ratios are *lower*, even after six cost-mitigation methods.
- The market-portfolio benefit appears only in **high-sentiment** periods.
- Sources: [UCP record](https://ciencia.ucp.pt/en/publications/do-limits-to-arbitrage-explain-the-benefits-of-volatility-managed/); confirmed by [DeMiguel, Martín-Utrera & Uppal](https://wp.lancs.ac.uk/fofi2022/files/2022/08/FoFI-2022-076-Alberto-Martin-Utrera.pdf)

**Bongaerts, Kang & van Dijk, "Conditional Volatility Targeting" (Financial Analysts Journal 76(4):54–71, 2020)**
- **Main finding.** Conventional volatility targeting "does not reliably" help in global equities and can enlarge drawdowns. A *conditional* variant that changes exposure only in the high and low volatility extremes improves Sharpe and reduces drawdowns and tail risk across major equity markets and momentum factors, with low turnover and leverage. — [SSRN 3636727](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3636727); [T&F](https://www.tandfonline.com/doi/full/10.1080/0015198X.2020.1790853)
- **Detail (secondary, unverified).**
  - Sample: 10 equity markets, 1982–2019.
  - Conventional real-time targeting **raised max drawdown** in the UK, Canada, Australia and Hong Kong.
  - It **raised expected shortfall in 8 of 10 markets**, including the US.
  - Only the US Sharpe gain was significant.
  - Out-of-sample 1977–2020, net of costs: conditional Sharpe **1.062 vs 0.940** for unconditional. Which portfolio this refers to is unclear.
  - The paper argues Harvey et al.'s scaling factor is built ex post, which introduces look-ahead.
  - Source: [Summitward summary](https://summitward.com/learn/volatility-targeting)

**Momentum-specific evidence**
- **Barroso & Santa-Clara, "Momentum has its moments" (Journal of Financial Economics 116(1), 2015, 111–120).**
  - Abstract: managing momentum's predictable, time-varying risk "virtually eliminates crashes and nearly doubles the Sharpe ratio." — [IDEAS](https://ideas.repec.org/a/eee/jfinec/v116y2015i1p111-120.html); [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0304405X14002566)
  - Sample: monthly 1927:03–2011:12.
  - Method: scale by six-month realized variance of daily returns, with a 12% volatility target.
  - Worst monthly return **−78.96% → −28.40%**; maximum drawdown **−96.69% → −45.20%**. — [paper copy](http://www.snifferquant.com/gyantal/Incode/papers/Momentum%20Has%20Its%20Moments(scaling%20Momentum%20by%20vol),2014.pdf)
  - **[Unverified]:** Sharpe going from 0.53 to 0.97, and the specific kurtosis and skewness values.
- **Daniel & Moskowitz, "Momentum crashes" (Journal of Financial Economics 122(2), 2016, 221–247).**
  - When crashes happen: they are partly forecastable and occur in "panic" states after market declines, when volatility is high, and *coincide with market rebounds*.
  - Why: loser-portfolio betas can exceed 3.
  - Fix: a dynamic strategy that scales by forecast mean and variance "approximately doubles the alpha and Sharpe ratio," and the result is robust across periods, countries and asset classes.
  - Source: [NBER w20439](https://www.nber.org/papers/w20439)

**When vol-based de-risking hurts: V-shaped recoveries**
- **MSCI (2020) simulation of volatility risk limits.**
  - In a V-shaped recovery that happens while volatility is still high, a vol limit has a net adverse effect.
  - *Intermediate* thresholds did worst: they cut exposure late and missed the rebound.
  - Very strict or very loose limits did better.
  - A US equity portfolio with a 20% volatility limit fell **17.7%** at the COVID trough versus **30.5%** for the market, but did not necessarily outperform over the long run.
  - Source: [MSCI "The Risk of Risk Limits"](https://www.msci.com/research-and-insights/blog-post/the-risk-of-risk-limits)
- **Man Group.** In V-shaped recoveries from 2000 to April 2025, vol-scaled strategies' outcomes were mostly between **−4% and +4%**, centred near zero. April 2025 was a notable outlier. Man's own program adds fast stress overlays on top of vol scaling. — [Man Group, "V-shaped recoveries"](https://www.man.com/special/v-shaped-recoveries)

### Inferences
- For a single equity index such as QQQ, the evidence that holds up is about **risk shape, not return**:
  - Vol targeting cuts left-tail severity and drawdown fairly reliably for US equities, because of the leverage effect.
  - Sharpe gains are modest: about +0.1 in-sample per Harvey et al., about +25% per Moreira-Muir for the market.
  - Those Sharpe gains are fragile out-of-sample: look-ahead in the scaling constant, regime instability, and higher expected shortfall in most non-US markets.
- If the overlay is **capped at 1× (no leverage)**, it can only reduce exposure. In calm up-trending quarters it is fully invested and costs nothing. In high-volatility quarters it cuts exposure.
- **Regime view.**
  - Helps in **down** quarters with persistent high volatility (2000–02, 2008, 2022-style grinding bears).
  - Hurts in **V-shaped** quarters where volatility spikes and the price rebounds quickly (Q1–Q2 2020, April 2025): the overlay de-risks near the low.
  - Roughly neutral in **sideways** low-volatility quarters.
- For **intraday** strategies, the same logic applies if volatility is estimated from recent intraday or daily realized volatility. Turnover from re-scaling at 30-minute frequency could erase the benefit. Barroso-Detzel and Bongaerts both point to costs and low turnover as decisive, so a banded or conditional scheme (resize only when volatility leaves a band) is the evidence-backed design choice.
- The momentum results (Barroso-Santa-Clara, Daniel-Moskowitz) are far stronger than results for the equity index itself. They apply to the user's *trend/momentum-style* strategies more than to plain long-QQQ exposure.

### Gaps
- The Harvey et al. full tables (maximum drawdown change, the 1% worst-day changes, volatility estimator, turnover) and Moreira-Muir's exact sample period and net-of-cost results could not be retrieved.
- Barroso-Santa-Clara Sharpe values (0.53 → 0.97) are not verified.
- No study found that tests vol targeting specifically on QQQ or the Nasdaq-100, or at intraday rebalancing frequency.
- Cederburg et al.'s result for the market factor alone (as opposed to all 103 strategies) was not retrieved.

---

## 3. Trend / moving-average filters on equity index exposure: drawdown reduction versus lag and whipsaw cost

### Takeaway
A slow moving-average filter, such as Faber's 10-month SMA or a 200-day MA, on a US equity index has historically **cut maximum drawdown by roughly half and volatility by about a third, at a similar or slightly lower compound return**:
- Faber's S&P 500 numbers for 1901–2012 are gross: CAGR 10.18% vs 9.32%, volatility 12.0% vs 17.9%, max drawdown −50.3% vs −83.5%.
- The risk-adjusted improvement comes almost entirely from avoiding long bear markets (1929–32, 2000–02, 2008).

Out-of-sample, cost-inclusive and look-ahead-free tests by Zakamulin find the gains "highly overstated":
- Risk-adjusted outperformance is only marginal.
- Long-run capital growth is lower.
- Outperformance in the second half of the sample is not statistically significant.
- The cost is many false signals (whipsaws) in both bull and sideways markets.

### Cited Findings
**Faber, "A Quantitative Approach to Tactical Asset Allocation" (Journal of Wealth Management 2007; SSRN 962461; February 2013 update)**
- **Rule.** At each month-end, hold the index if price is above its 10-month SMA, otherwise hold cash. In GTAA this is applied separately to 5 asset classes. — [SSRN copy on mebfaber.com](https://mebfaber.com/wp-content/uploads/2016/05/SSRN-id962461.pdf); [CXO Advisory](https://www.cxoadvisory.com/technical-trading/long-term-outperformance-from-trends-defined-by-moving-averages/)
- **S&P 500, 1901–2012, timing vs buy-and-hold (gross).**
  - CAGR **10.18% vs 9.32%**.
  - Standard deviation **12.0% vs 17.9%**; one secondary source gives 17.87% for buy-and-hold.
  - Maximum drawdown **−50.3% vs −83.5%**.
  - Sharpe **0.55 vs 0.32**.
  - Sources: [Faber blog, 2013 update](https://mebfaber.com/2013/06/07/qtaa-paper-update-manage-your-risk-4/); [CXO Advisory](https://www.cxoadvisory.com/technical-trading/long-term-outperformance-from-trends-defined-by-moving-averages/); [Bogleheads citing paper](https://www.bogleheads.org/forum/viewtopic.php?t=173980&start=200)
- **Exposure and trading.** Invested about 70% of the time, with fewer than one round trip per year, so cost drag is low at monthly frequency. — [SSRN copy](https://mebfaber.com/wp-content/uploads/2016/05/SSRN-id962461.pdf)
- **Rebalance-timing sensitivity.** The model implicitly trades on the first day of each month, and results vary with the rebalance day. — [Newfound Research](https://blog.thinknewfound.com/tag/rebalance)

**Zakamulin critiques**
- **"The real-life performance of market timing with moving average and time-series momentum rules" (Journal of Asset Management 15(4):261–278, 2014; SSRN title "Fooled by Data-Mining").**
  - Reported performance "usually contains a considerable data-mining bias and ignores important market frictions."
  - Out-of-sample tests with transaction costs show performance is "highly overstated, to say the least."
  - Covers the S&P Composite, DJIA, and long- and intermediate-term Treasuries, with MA windows of 2–24 months.
  - Sources: [IDEAS](https://ideas.repec.org/a/pal/assmgt/v15y2014i4d10.1057_jam.2014.25.html); [SSRN 2242795](https://doi.org/10.2139/ssrn.2242795)
  - A secondary summary by Swedroe adds that, over the long run, timing gives only marginally better risk-adjusted returns than buy-and-hold with *substantially lower long-term capital growth*. The "9 to 26 percentage points lower mean returns" in that summary has unclear units and horizon and is **[unverified]**. — [Swedroe/ETF.com](https://www.etf.com/sections/index-investor-corner/swedroe-beware-lure-market-timing)
- **"Revisiting the Profitability of Market Timing with Moving Averages" (2016).** Earlier reported gains, notably Glabadanidis (2015), came from look-ahead bias. Without it, MA strategy performance is "only marginally better" than buy-and-hold. — [paper copy](https://c.mql5.com/forextsd/forum/205/Revisiting%20the%20Profitability%20of%20Market%20Timing%20with%20Moving%20Averages__1.pdf)
- **"A Comprehensive Look at the Empirical Performance of Moving Average Trading Strategies" (SSRN 2677212).**
  - All timing rules generate many false signals in *both* bullish and bearish trends, but tend to outperform in bear states.
  - No statistically significant outperformance in the second half of the sample.
  - Source: [SSRN 2677212](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2677212)
- **Zakamulin S&P 500 analysis (Alpha Architect series).** Maximum drawdown and average maximum drawdown fall by about **1/2**, but cumulative return is *slightly less* than buy-and-hold over a **65-year out-of-sample** period. — [Alpha Architect, Part 7](https://alphaarchitect.com/trend-following-valeriy-zakamulin-trading-sp-500-index-part-7/)

**Multi-asset trend-following context (AQR)**
- **Hurst, Ooi & Pedersen, "A Century of Evidence on Trend-Following Investing" (Journal of Portfolio Management 44(1):15–29, 2017).**
  - Design: 67 markets, 1880–2016, equal-weighted 1/3/12-month time-series momentum.
  - Result: positive average returns in every decade.
  - Smile: returns are best in *extreme up or down* equity years, and the strategy did well in 8 of the 10 largest crisis periods.
  - Sources: [AQR](https://www.aqr.com/Insights/Research/Journal-Article/A-Century-of-Evidence-on-Trend-Following-Investing); [PDF copy](https://www.trendfollowing.com/whitepaper/Century_Evidence_Trend_Following.pdf)
  - **[Unverified]:** the exact fee and cost assumptions.

### Inferences
- **Regime view for a long-QQQ trend filter.**
  - **Down** quarters inside long bear markets (2000–02, 2008, 2022): the filter's whole benefit is here. It exits after the first leg down and avoids the rest.
  - **Sideways** quarters: the main cost, because repeated crossings mean buy high, sell low, plus costs. Zakamulin's "many false signals in both bull and bear trends" points the same way.
  - **Up** quarters: a small give-up from lag at re-entry after corrections. The 70% time-in-market in Faber implies missed upside after sharp V-shaped reversals such as 1987, 2020 and April 2025. In those cases the filter sells near the bottom and buys back higher.
- QQQ's history is dominated by the 2000–02 drawdown of about −83%, which an MA filter largely avoided. A backtest starting in 1999 will therefore flatter the filter, the same look-ahead or sample-selection issue Zakamulin warns about. Results from 2003 onward are a more honest test.
- On 30-minute bars, an MA filter with an equivalent lookback, e.g. 10 months ≈ 200 trading days ≈ 2,600 thirty-minute bars, behaves like the daily or monthly literature. Short intraday MAs are a different animal: much higher turnover and whipsaw, and the monthly-frequency evidence above does not transfer.
- Expected effect to report: maximum drawdown down about 40–60% and volatility down about 30%, with the CAGR change somewhere between slightly positive and moderately negative depending on sample, and statistically weak.

### Gaps
- No primary source verified for Nasdaq-100 or QQQ specifically (e.g., a 200-day MA on the Nasdaq Composite).
- Faber's table could not be opened directly; numbers come from Faber's blog, CXO and Bogleheads.
- The quantified whipsaw cost (trades per year, average loss per false signal) in Zakamulin's 2017 book *Market Timing with Moving Averages* (Palgrave) was not retrieved.

---

## 4. Position sizing: fixed fraction / Kelly vs volatility-based sizing for single-instrument strategies (brief)

### Takeaway
I found no rigorous, peer-reviewed head-to-head test of fractional-Kelly versus volatility-based sizing on a single instrument. Practitioner literature treats volatility targeting as a form of fractional Kelly. The well-established result is the growth-versus-drawdown trade-off of fractional Kelly. Estimation error in the edge makes full Kelly dangerous.

### Cited Findings
- **Vol targeting as fractional Kelly.** A 2026 arXiv paper (seen only as a search snippet) states that practitioners describe volatility targeting as fractional-Kelly sizing (citing Carver 2023) and "make the link explicit." I could not open it to confirm which paper made the claim; candidates are [arXiv 2608.01494 "Conformal Kelly"](https://arxiv.org/pdf/2608.01494) and [arXiv 2607.19497](https://arxiv.org/pdf/2607.19497).
- **Fractional-Kelly trade-off (practitioner table).**
  - Half-Kelly keeps about **75%** of full-Kelly growth, with about a **12.5%** chance of ever halving capital versus **50%** at full Kelly.
  - Quarter-Kelly keeps about **44%** of growth, with about a **0.8%** chance of halving.
  - Source: [practitioner summary](https://iotdigitaltwinplm.com/kelly-criterion-position-sizing-risk-engine-implementation-fractional-kelly-2026/)
  - These values match the closed-form results for geometric Brownian motion. At fraction c of Kelly, growth is c(2−c) of full Kelly and P(ever halving) = 0.5^(2/c − 1). For example, c = 0.5 gives 0.75 and 0.125, and c = 0.25 gives 0.4375 and 0.0078.
- **Estimation error.** Practitioner sources note that small errors in the estimated edge sharply cut realized growth under full Kelly. They suggest 200–500 trades as a rule of thumb before Kelly inputs are reliable. This is opinion, not a controlled test. — [darkbot practitioner note](https://darkbot.io/blog/kelly-criterion-crypto)

### Inferences
- The Kelly fraction for a single asset is μ/σ². If expected return is roughly constant, Kelly sizing is variance-scaled exposure (∝ 1/σ²). That is the Moreira-Muir weight, so the vol-managed evidence in Section 2 is effectively the evidence on "Kelly with a constant edge."
- The practical difference is that Kelly also scales by the estimated edge μ. For a backtested intraday strategy, μ is very noisy and in-sample-biased. Fractional (¼–½) Kelly, or simply a fixed volatility target with a leverage cap, is more robust.
- **Fixed-fraction (constant notional) sizing** makes realized risk swing with QQQ's volatility. Volatility-based sizing (ATR or realized volatility) equalizes risk per trade across high- and low-volatility quarters, which will compress the dispersion of results across the user's up, sideways and down regime buckets.

### Gaps
- No academic out-of-sample comparison of Kelly versus volatility sizing for a single ETF or intraday strategy was found.
- The arXiv source of the "vol targeting = fractional Kelly" claim is not confirmed.

---

## 5. What each overlay implies for up, sideways and down markets

### Takeaway
All three overlays are **short-volatility-of-trend insurance**: they pay off in persistent, high-volatility down markets and charge a premium in choppy sideways markets and fast V-shaped reversals. In steady up markets:
- Vol targeting is near-free and can even help with leverage.
- A trend filter costs a little from lag.
- A tight stop costs more, the more mean-reverting the underlying is.

### Cited Findings
**Down markets: all three help, with conditions**
- **Trend filters.** They outperform in bear states. — [Zakamulin SSRN 2677212](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2677212)
- **Trend following.** It does best in extreme down (and up) equity years, and did well in 8 of 10 crises. — [AQR](https://www.aqr.com/Insights/Research/Journal-Article/A-Century-of-Evidence-on-Trend-Following-Investing)
- **Volatility targeting.** Left-tail events are milder because exposure is already low when volatility is high. — [Harvey et al. PDF](https://people.duke.edu/~charvey/Research/Published_Papers/P135_The_impact_of.pdf)
- **Stop-losses.** Wide stops beat buy-and-hold when bear regimes are high-volatility and persistent. — [CXO on Lo-Remorov](https://www.cxoadvisory.com/equity-premium/stop-losses-on-stock-positions-in-depth)

**V-shaped down-then-up markets: volatility and stop overlays hurt**
- **Volatility limits.** Intermediate thresholds miss the rebound. — [MSCI](https://www.msci.com/research-and-insights/blog-post/the-risk-of-risk-limits)
- **Momentum.** Momentum crashes coincide with rebounds after declines. — [Daniel & Moskowitz](https://www.nber.org/papers/w20439)
- **Vol-scaled strategies.** In V-shaped recoveries since 2000, outcomes were about ±4%, centred near zero. — [Man Group](https://www.man.com/special/v-shaped-recoveries)

**Sideways markets: trend filters and stops whipsaw**
- **Trend filters.** Many false signals in both bull and bear trends. — [Zakamulin SSRN 2677212](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2677212)
- **Stops.** Tight daily stops underperform under negative autocorrelation. — [CXO on Lo-Remorov](https://www.cxoadvisory.com/equity-premium/stop-losses-on-stock-positions-in-depth)

**Up markets: overlays mostly cost return**
- **Trend filter.** Slightly lower cumulative return than buy-and-hold over 65 years out-of-sample. — [Alpha Architect / Zakamulin](https://alphaarchitect.com/trend-following-valeriy-zakamulin-trading-sp-500-index-part-7/)
- **Stops.** Under a random walk they always cut expected return. — [Kaminski & Lo SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=968338)

### Inferences
**Suggested hypotheses for the user's quarterly split**

| Overlay | Up quarters | Sideways quarters | Down quarters |
|---|---|---|---|
| Stop-loss on a **mean-reversion** strategy | Small cost | Clear cost: stopped out before the reversion pays | Benefit only if the down quarter is a persistent trend; a wide "disaster" stop works best |
| Stop-loss on a **momentum/breakout** strategy | Roughly neutral | Moderate cost from whipsaw | Benefit |
| **Vol targeting, capped at 1×** | About neutral, since volatility is usually low | About neutral | Benefit in grinding high-volatility bears; cost in V-shaped quarters (e.g. 2020Q1→Q2) |
| **Long-only MA filter on QQQ** | Small cost from lag | Largest cost from whipsaw | Largest benefit, but only in multi-month bears (2000–02, 2008, 2022) |

- Because quarters are short, an MA filter or a slow volatility estimator may not react *within* a down quarter. Some of the benefit may land in the following quarter, and some of the cost (missed rebound) may land in a quarter classified as "up." The user should report the overlay's effect conditional on the *previous* quarter's regime as well.
- Turnover rises in all three overlays, most of all for intraday stops and frequent vol re-scaling. Report results net of a realistic QQQ cost: about 1¢/share or about 1 bp, plus slippage. The Zarattini-Aziz replication shows a QQQ intraday edge can vanish at about 2.2¢/share.

### Gaps
- No academic source was found that conditions overlay performance on *quarterly* up/sideways/down labels for QQQ. The table above is inference from the mechanism-level evidence.
- No evidence was retrieved on how these overlays behaved specifically in QQQ's 2022 bear market or the April 2025 V-shaped episode beyond Man Group's note that April 2025 was an outlier.
