# Data snooping, backtest overfitting and out-of-sample decay of trading strategies (with tools for a QQQ 30-minute, regime-split study)

How these notes were checked: WebFetch could not resolve any host in this session (DNS errors on ssrn/duke/repec/fmg/davidhbailey), so I could not open full PDFs. I verified figures against abstracts and abstract-level summaries that web search returned. Each figure says how it was checked. Numbers labelled "my calculation" come from standard formulas I ran myself (Python, iid-normal assumptions). They are not quotes from the papers.

---

## 1. Technical trading rules on equity indices: what survives a data-snooping correction and out-of-sample testing?

### Takeaway
On the DJIA, the best moving-average and breakout rules looked significant in the 1897–1986 sample even after a data-snooping correction. They then failed out of sample after 1986. Using false-discovery-rate control and realistic costs makes it worse: the rules can't be picked in advance, and small transaction costs wipe out the gains even in-sample. The one large study that found surviving profits located them in then-"young" markets, the NASDAQ Composite and Russell 2000 around 1990–2003, and not in mature indices.

### Cited Findings
- **Sullivan, Timmermann & White (1999, JF 54(5):1647–1691):** they took Brock, Lakonishok & LeBaron's (1992) 26 rules, expanded the set to a full universe, ran it on about 100 years of daily DJIA data, and used White's Reality Check bootstrap to adjust for searching across the whole universe — [IDEAS/RePEc](https://ideas.repec.org/a/bla/jfinan/v54y1999i5p1647-1691.html); [Wiley](https://onlinelibrary.wiley.com/doi/10.1111/0022-1082.00163)
  - The universe had 7,846 rules. This count comes from later citing papers; I did not check it against STW's tables — [paper copy (K. Sheppard course page)](https://www.kevinsheppard.com/files/teaching/mfe/advanced-econometrics/Sullivan_Timmermann_White.pdf)
  - In the BLL sample period the best rule (a 5-day moving average) still beat the benchmark after the data-snooping adjustment, with a Reality Check p-value below about 0.002. The rule chosen at the end of 1986 "did not continue to generate valuable economic signal in the subsequent 10-year period" (1987–1996). This comes from search excerpts of the paper and a critique of it — [paper copy](https://par.cse.nsysu.edu.tw/resource/paper/2015/150930/Data-Snooping,%20Technical%20Trading%20Rule.pdf); [Hsu & Kuan working paper discussing STW](https://homepage.ntu.edu.tw/~ckuan/pdf/snoop01.pdf)
  - A later paper reports the 1987–1996 best-rule result as a statistically insignificant mean return of 8.63% per year before transaction costs. This is a secondary report that I did not check against STW — [AgEcon futures paper](https://ageconsearch.umn.edu/record/19039/files/cp05pa01.pdf)
  - A replication on DJIA 1990–2000 found the best rule earned 14.67% a year (0.00058 per day), but its Reality Check p-value was 0.386, so it was not significant — [Hsu & Kuan working paper](https://homepage.ntu.edu.tw/~ckuan/pdf/snoop01.pdf)
  - The Reality Check method itself is in White (2000, Econometrica) — [Wiley](https://onlinelibrary.wiley.com/doi/abs/10.1111/1468-0262.00152)
- **Bajgrowicz & Scaillet (2012, JFE 106(3):473–491):** daily DJIA 1897–2011, with false discovery rate (FDR) control in place of the familywise Reality Check. Abstract claims, verified from the abstract as returned by search:
  - FDR selects more outperforming rules than earlier methods, which helps diversify against model uncertainty.
  - Even with this more powerful method, "an investor would never have been able to select ex ante the future best-performing rules."
  - "Even in-sample, the apparent performance is completely offset by low transaction costs."
  - The results "seriously call into question the economic value of technical trading rules that has been reported for early periods."
  - Sources: [IDEAS/RePEc](https://ideas.repec.org:443/a/eee/jfinec/v106y2012i3p473-491.html); [CFA Institute digest](https://rpc.cfainstitute.org/research/cfa-digest/2013/02/technical-trading-revisited-false-discoveries-persistence-tests-and-transaction-costs-digest)
- **Park & Irwin (2007, Journal of Economic Surveys 21(4):786–826):**
  - Of 95 "modern" studies, 56 found positive results, 20 negative and 19 mixed (verified from the abstract as returned by search) — [Wiley](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1467-6419.2007.00519.x)
  - The abstract warns that most studies have problems in their testing procedures, including "data snooping, ex post selection of trading rules or search technologies" and difficulty estimating risk and transaction costs — [Wiley](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1467-6419.2007.00519.x)
  - The 2004 working-paper version counted 92 studies: 58 positive and 24 negative — [AgMAS 2004-04](https://ageconsearch.umn.edu/record/37487/files/AgMAS04_04.pdf)
- **Hsu & Kuan (2005, J. Financial Econometrics 3(4):606–628):**
  - They used White's Reality Check and Hansen's SPA test on a much larger universe that included "complex" strategies (learning, voting and channel-type rules), about 39,832 rules according to a secondary source. The indices were DJIA, S&P 500, NASDAQ Composite and Russell 2000, over roughly 1989/1990–2002/2003; summaries disagree on the exact window — [IDEAS](https://ideas.repec.org/a/oup/jfinec/v3y2005i4p606-628.html); [HKU/CORE copy](https://core.ac.uk/download/pdf/37964017.pdf)
  - Significant profitable rules exist in the "young" markets (NASDAQ Composite, Russell 2000) but not in the "mature" ones (DJIA, S&P 500). After costs, the best NASDAQ and Russell rules beat buy-and-hold in most in- and out-of-sample periods — [IDEAS](https://ideas.repec.org/a/oup/jfinec/v3y2005i4p606-628.html)
  - A practitioner re-test on the Russell 2000 using post-2003 data was "quite disappointing." This is informal and not peer-reviewed — [CXO Advisory](https://www.cxoadvisory.com/technical-trading/technical-trading-thoroughly-tested)
- **Hsu, Taylor & Wang (2016, J. International Economics 102:188–208):** this is FX, not equities. They tested 21,000+ rules on 30 currencies over about 45 years with a stepwise-SPA correction and empirical bid-ask costs. They found "substantial predictability and excess profitability," with variation over time and across countries that they read as consistent with "temporary irrationality and market immaturity" — [IDEAS](https://ideas.repec.org/a/eee/inecon/v102y2016icp188-208.html); [WUSTL profile](https://profiles.wustl.edu/en/publications/technical-trading-is-it-still-beating-the-foreign-exchange-market/)

### Inferences
- In this literature the pattern is consistent: once you correct for multiple testing, any surviving profitability sits in older samples or less mature markets, and it fades as markets mature. The Nasdaq-100 is now one of the most liquid and heavily arbitraged markets in the world, and QQQ has only traded since 1999. A daily or intraday MA or breakout rule on QQQ should therefore start with a strong prior of no edge after costs.
- Hsu & Kuan's NASDAQ result covers about 1990–2003 and includes the dot-com bubble and crash, which is a strongly trending regime. It does not support expecting the same rules to work on QQQ from 2015 to 2025.
- Bajgrowicz & Scaillet's "completely offset by low transaction costs" matters a lot for 30-minute bars. Higher turnover means costs and slippage can erase gross edges that are small per trade.
- The methods used here (Reality Check, SPA, stepwise SPA/Romano–Wolf, FDR) are the standard tools for testing "the best of K rules" against a benchmark. They are usable for this project (see section 5).

### Gaps
- I could not open STW's tables. The exact 1987–1996 Reality Check p-value, the S&P 500 futures result (STW also tested S&P 500 futures, as I recall) and the Sharpe-criterion results are not verified here.
- I could not verify Bajgrowicz & Scaillet's break-even cost level (in basis points) or their subperiod counts of significant rules.
- Hsu, Taylor & Wang's subperiod results (whether FX profitability fell over time) were not available from abstracts.
- I found no peer-reviewed study that applies a Reality Check/SPA/FDR correction specifically to QQQ or Nasdaq-100 intraday (30-minute) technical rules.

---

## 2. How much performance decays out of sample and after publication?

### Takeaway
Across academic anomalies, returns fall about 26% out of sample (a rough upper bound on the data-mining component) and about 58% after publication. Replicated systematic equity strategies keep roughly half of their in-sample Sharpe. Practitioner backtests do worse: commercially promoted "alternative beta" indices lost a median 73% of their backtested Sharpe in live trading. Across 888 retail-quant algorithms, backtest Sharpe explained almost none of the variation in out-of-sample Sharpe (R² < 0.025).

### Cited Findings
- **McLean & Pontiff (2016, JF):**
  - Across 97 predictors, returns are 26% lower out of sample (after the sample end, before publication) and 58% lower after publication. The authors attribute the 32-percentage-point gap to publication-informed trading. They treat the 26% out-of-sample decline as an upper bound on data-mining effects. Verified from the published abstract as returned by search — [paper PDF (gwern mirror)](https://www.gwern.net/doc/economics/2016-mclean.pdf); [SUFE abstract](https://academicnewsletter.sufe.edu.cn/info/359722)
  - Predictors with higher in-sample returns decline more. Post-publication returns are higher for portfolios concentrated in high-idiosyncratic-risk, low-liquidity stocks, consistent with limits to arbitrage — [paper PDF](https://www.gwern.net/doc/economics/2016-mclean.pdf)
  - Earlier working-paper versions had different figures (82 characteristics with ~35% post-publication decay; 95 characteristics with 56%). Cite the 2016 published numbers — [Ivey WP copy](https://ivey.uwo.ca/media/3775549/pontiff.pdf)
- **Falck, Rej & Thesmar (CFM; arXiv 2105.01380; published as "When do systematic strategies decay?", Quantitative Finance 2022):** they replicated 72 published US equity strategies (all published before 2011). Abstract-level summaries report:
  - Out-of-sample Sharpe is about 50% of in-sample.
  - Publication year alone explains about 30% of the variance in Sharpe decay. Each later publication year adds about 5 percentage points of decay.
  - Proxies for overfitting add about another 15% of explanatory power.
  - Secondary readers disagree on how much arbitrage-capital variables add.
  - Sources: [IDEAS/arXiv listing](https://ideas.repec.org/p/arx/papers/2105.01380.html); [CFM](https://cfm.com/why-and-how-systematic-strategies-decay/); [Evidence Investor summary](https://www.evidenceinvestor.com/post/why-and-how-systematic-strategies-decay)
- **Suhonen, Lennkh & Perez (2017, J. Portfolio Management, "Quantifying backtest overfitting in alternative beta strategies"):** ~215 bank-sponsored alternative-beta strategy indices across 5 asset classes.
  - Median Sharpe was ~1.20 in backtests and ~0.31 live, a median 73% deterioration.
  - The most complex strategies took an extra Sharpe haircut of more than 30% compared with simpler ones.
  - Secondary summaries disagree on the sponsor count (15 or 17 banks).
  - Sources: [Alpha Architect](https://alphaarchitect.com/beware-of-backtest-overfitting/); [CXO Advisory](https://www.cxoadvisory.com/big-ideas/live-performance-of-alternative-beta-products/)
- **Wiecki, Campbell, Lent & Stauth (2016, Quantopian, SSRN 2745220, "All that glitters is not gold"):** 888 algorithms, each with at least 6 months of out-of-sample trading.
  - Backtest Sharpe had R² < 0.025 for predicting out-of-sample Sharpe.
  - The more a strategy was backtested, the larger its in-sample to out-of-sample gap.
  - Volatility and maximum drawdown predicted out-of-sample results better than Sharpe. A non-linear classifier reached R² = 0.17.
  - Sources: [Quantpedia summary](https://quantpedia.com/quantopians-academic-paper-about-in-vs-out-of-sample-performance-of-trading-alg/); [CXO Advisory](https://www.cxoadvisory.com/big-ideas/in-sample-vs-out-of-sample-performance-of-888-trading-strategies)
- **Intraday evidence:**
  - **Gao, Han, Li & Zhou (2018, JFE, "Market intraday momentum"):** on SPY 1993–2013, the first half-hour return predicts the last half-hour return. Out-of-sample R² is up to 1.8% (2.7% when the 12th half-hour return is added). A timing rule earned a gross 6.3% a year, compared with −0.5% for holding SPY through every last half-hour. These figures come from an earlier working-paper sample. The effect is stronger on volatile, high-volume, recession and some news days — [SUFE abstract](https://academicnewsletter.sufe.edu.cn/info/356150); [CXO Advisory](https://www.cxoadvisory.com/?p=25481)
  - **Baltussen, Da, Lammers & Martens (2021, JFE 142(1):377–403):** this is an independent extension. They find "strong market intraday momentum everywhere" across 60+ futures (equities, bonds, commodities, FX) from 1974–2020, and link it to gamma hedging by options market makers and leveraged ETFs — [IDEAS](https://ideas.repec.org/a/eee/jfinec/v142y2021i1p377-403.html); [working paper](https://www3.nd.edu/~zda/intramom.pdf)

### Inferences
- For a published or backtested strategy, a reasonable working prior is that about half of the in-sample Sharpe survives for published academic strategies. A typical practitioner backtest keeps about a quarter or less. The decay is larger when the in-sample result was stronger, when the strategy is more complex, and when it was backtested more times.
- The two decay sources lead to different defenses:
  - Arbitrage after publication: QQQ is extremely liquid and widely traded, so published intraday patterns on it are especially exposed. Prefer effects that have a structural flow mechanism (such as hedging demand or index rebalancing) over purely statistical patterns.
  - Overfitting: the user's logic-before-backtest approach and pre-registration address this directly.
- Intraday momentum is the most relevant published 30-minute-scale effect for QQQ. It has an economic mechanism (gamma and leveraged-ETF hedging), which fits the "analyze logic first" workflow. Its out-of-sample R² is around 1–3%, so per-trade edges are small and cost-sensitive.

### Gaps
- I found no peer-reviewed post-publication decay study specifically for intraday or technical strategies. In particular, nothing tests intraday momentum after Gao et al.'s 2013 sample end or after its 2018 publication. This is the main evidence gap for the project.
- I could not check from primary text the Falck et al. figures (~50% survival, 5 points per year, 30% and 15% variance shares) or the exact Suhonen et al. sample counts.
- I did not search for Hou, Xue & Zhang (2020) "Replicating anomalies" or Jensen, Kelly & Pedersen (2023) "Is there a replication crisis in finance?", which give other views on replication rates.

---

## 3. Multiple-testing thresholds and Sharpe haircuts

### Takeaway
After accounting for the number of strategies tried, the field's recommended significance bar is t > 3.0 (Harvey–Liu–Zhu) and up to t ≈ 3.4–3.8 (Chordia–Goyal–Saretto), not 2.0. Harvey & Liu show the right Sharpe haircut is nonlinear rather than a flat 50%: marginal Sharpe ratios lose most or all of their value, while very high ones lose little.

### Cited Findings
- **Harvey, Liu & Zhu (2016, RFS 29(1):5–68):** they catalogued 316 factors from 313 papers. Under a multiple-testing framework, "a newly discovered factor needs to clear a much higher hurdle, with a t-ratio greater than 3.0," and "most claimed research findings in financial economics are likely false." Verified from the NBER abstract as returned by search — [NBER w20592](https://www.nber.org/papers/w20592); [SSRN](https://papers.ssrn.com/abstract=2513152)
  - Counterpoint: Chen (arXiv 2206.15365), "Most claimed statistical findings in cross-sectional return predictability are likely true," disputes the "most are false" reading. I read only the title and listing — [arXiv](https://arxiv.org/pdf/2206.15365)
- **Chordia, Goyal & Saretto (2020, RFS 33(5):2134–2179, "Anomalies and false rejections"):** using a lab of more than 2 million strategies, the multiple-testing t-thresholds are 3.84 for time-series and 3.38 for cross-sectional tests (3.8 and 3.4 in the abstract). Without a multiple-testing adjustment, the expected share of false rejections is 45.3% — [IDEAS](https://ideas.repec.org/a/oup/rfinst/v33y2020i5p2134-2179..html); [SFI](https://www.sfi.ch/en/publications/anomalies-and-false-rejections)
- **Harvey & Liu (2015, J. Portfolio Management 41(1):13–28, "Backtesting"):**
  - Discounting backtested Sharpe by 50% is "only a rule of thumb."
  - The haircut is computed in three steps: convert the Sharpe ratio to a t-ratio, adjust its p-value for the number of tests (Bonferroni, Holm or BHY), and convert back.
  - The haircut is nonlinear: "the highest Sharpe ratios are only moderately penalized while the marginal Sharpe ratios are heavily penalized."
  - The paper also gives a minimum "profit hurdle" a strategy must reach to count as significant.
  - Sources: [paper PDF (Duke)](https://people.duke.edu/~charvey/Research/Published_Papers/P120_Backtesting.PDF); [CME copy](https://www.cmegroup.com/education/files/backtesting.pdf)
  - Worked example in Harvey's slides: with 10 trials the multiple-testing p-value rises to 0.029 and the haircut is about 27%. More trials mean a larger haircut — [Harvey slides, Wharton Jacobs Levy](https://jacobslevycenter.wharton.upenn.edu/wp-content/uploads/2015/05/3-Campbell-Harvey.pdf)
  - Bonferroni is the strictest of the three. BHY controls FDR and is the most lenient. For the single top-ranked strategy, Holm is identical to Bonferroni — [same slides](https://jacobslevycenter.wharton.upenn.edu/wp-content/uploads/2015/05/3-Campbell-Harvey.pdf); [quantstrat haircutSharpe docs](https://www.rdocumentation.org/packages/quantstrat/versions/0.16.7/topics/haircutSharpe)
  - MATLAB code (Haircut_SR.m, Profit_Hurdle.m) is on Harvey's site, and R implementations are in quantstrat (`haircutSharpe`, `profitHurdle`) — [Duke code page](https://people.duke.edu/~charvey/backtesting/); [rdrr profitHurdle](https://rdrr.io/github/braverock/quantstrat/man/profitHurdle.html)
- **My calculation: Harvey–Liu-style Bonferroni haircut for a 10-year sample.** This uses iid returns, a two-sided test, and annualized SR × √years ≈ t.
  - Backtested SR 1.0 (t = 3.16): haircut is 24% with 10 variants, 44% with 50, 55% with 100, and 77% with 300.
  - Backtested SR 0.75 (t = 2.37): haircut is 43% with 10 variants and 94% with 50.
  - Backtested SR 0.5 (t = 1.58, nominal p = 0.11): not significant even as a single test, so the haircut is 100% with any multiple testing.
  - Backtested SR 1.5: haircut is only 10% with 10 variants and 22% with 100. This is the nonlinearity Harvey & Liu describe.

### Inferences
- Reading t > 3.0 as a Sharpe threshold: with about 10 years of data, it needs an annualized Sharpe of about 0.95 (3/√10). The Chordia–Goyal–Saretto 3.84 bar needs about 1.21. Those thresholds were calibrated on a whole field's worth of tests. For a personal project the more honest step is to count your own variants and apply Holm, BHY or a deflated Sharpe ratio with that count.
- The 50% rule of thumb is too lenient for marginal strategies (SR 0.5–0.8 over 10 years) and too harsh for very strong ones.

### Gaps
- I could not open Harvey & Liu's Exhibits to quote their own haircut tables. A third-party replication mentions an Exhibit 5 value (corrected SR 0.912, 74.6% haircut), but I could not confirm its inputs, so I left it out.
- I could not verify the exact BHY/Holm settings used in HLZ's t > 3.0 derivation, or how much it depends on their assumed number of untried or unpublished tests.

---

## 4. Overfitting diagnostics: Deflated Sharpe, PBO/CSCV, and minimum backtest length

### Takeaway
With 5 years of daily data, trying about 45 independent configurations is enough to expect at least one with an in-sample annualized Sharpe of 1.0 when the true Sharpe is zero. With 2 years, about 7 is enough. The Deflated Sharpe Ratio raises the benchmark to the Sharpe you'd expect from the best of N noise strategies and corrects for skew and kurtosis. PBO, estimated by CSCV, gives the probability that the in-sample winner falls below median out of sample.

### Cited Findings
- **Bailey, Borwein, López de Prado & Zhu (2014, Notices of the AMS, "Pseudo-mathematics and financial charlatanism"):**
  - "If only five years of data are available, no more than forty-five independent model configurations should be tried." Beyond that, you should expect an in-sample annualized Sharpe ≥ 1 with an expected out-of-sample Sharpe of 0. This is quoted from a lecture excerpt of the paper — [lecture notes quoting the paper](https://cs.runi.ac.il/~kipnis/notes/STATS_207_L18.pdf); [paper PDF (carmamaths)](https://carmamaths.org/jon/backtest.pdf); [CXO summary](https://www.cxoadvisory.com/big-ideas/insidiousness-of-overfitting-investment-strategies-via-iterative-backtests)
  - Assuming independent trials makes this a conservative estimate. Correlated trials have a smaller effective N — [lecture notes](https://cs.runi.ac.il/~kipnis/notes/STATS_207_L18.pdf)
  - López de Prado's seminar abstract: after only 7 configurations, one is expected to find a 2-year backtest with annualized Sharpe above 1 when the expected out-of-sample Sharpe is 0 — [IAQF](https://iaqf.org/event-813217)
  - **My calculation, as a cross-check.** I used E[max of N standard normals] ≈ (1−γ)·Φ⁻¹(1−1/N) + γ·Φ⁻¹(1−1/(Ne)), with γ ≈ 0.5772 the Euler–Mascheroni constant, and SE(annualized SR) ≈ 1/√years. N = 45 over 5 years gives an expected maximum Sharpe of 1.00, which reproduces the paper's figure. Expected maximum annualized Sharpe when the true Sharpe is 0:

    | Years of data | N = 10 | N = 45 | N = 100 | N = 1000 |
    |---|---|---|---|---|
    | 10 | 0.50 | 0.71 | 0.80 | 1.03 |
    | 3 | 0.91 | 1.29 | 1.46 | 1.88 |
    | 2 | 1.11 | 1.58 | 1.79 | 2.30 |

  - Minimum backtest length (MinBTL) follows by inverting this: MinBTL ≈ (E[max_N] / target SR)² years — [paper PDF](https://carmamaths.org/jon/backtest.pdf)
- **Bailey & López de Prado (2014, J. Portfolio Management 40(5):94–107, "The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and Non-Normality"):**
  - It corrects two sources of inflation: selection bias under multiple testing and non-normal returns. Failing to report the number of trials inflates expectations — [SSRN abstract](https://papers.ssrn.com/abstract=2460551)
  - Mechanics, from secondary descriptions: DSR is the Probabilistic Sharpe Ratio evaluated against a benchmark SR₀ = √Var(SR across trials) × [(1−γ)Φ⁻¹(1−1/N) + γΦ⁻¹(1−1/(Ne))]. Its standard error uses skewness and kurtosis (the Mertens form). The effective N should be estimated, for example by clustering correlated trials. A common reading treats DSR ≥ 0.95 as significant — [Wikipedia](https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio); [MetricGate](https://metricgate.com/docs/deflated-johnson-sharpe-ratio/); [tradingstrategy.ai glossary](https://tradingstrategy.ai/glossary/probabilistic-sharpe-ratio)
- **Bailey, Borwein, López de Prado & Zhu, "The Probability of Backtest Overfitting" (J. Computational Finance, 2017; SSRN 2326253):**
  - It proposes a framework for estimating PBO and argues that "standard statistical techniques such as hold-out tend to be unreliable and inaccurate in the context of investment backtests." The model-free, nonparametric implementation is called combinatorially symmetric cross-validation (CSCV) — [SSRN](https://papers.ssrn.com/abstract=2326253); [WMU ScholarWorks](https://scholarworks.wmich.edu/math_pubs/42)
  - The R package `pbo` implements it. It reports PBO and performance degradation, using the Omega ratio by default where the paper used Sharpe — [CRAN pbo README](https://packages.oit.ncsu.edu/cran/web/packages/pbo/readme/README.html)
  - How CSCV works (from the method as described in the paper and package):
    1. Split the T×N matrix of returns (time periods × strategy variants) into S equal time blocks.
    2. For every way of choosing S/2 blocks as in-sample, pick the in-sample best variant.
    3. Record its relative rank among all variants on the complementary out-of-sample blocks.
    4. PBO is the share of combinations where that rank is below the median (logit ≤ 0).
    5. With S = 16 there are C(16,8) = 12,870 combinations (arithmetic).
- **Lo (2002, Financial Analysts Journal 58(4):36–52, "The Statistics of Sharpe Ratios"):**
  - Monthly Sharpe ratios generally cannot be annualized by multiplying by √12. Serial correlation can overstate an annual Sharpe by as much as 65% (hedge fund example) — [CFA Institute](https://rpc.cfainstitute.org/research/financial-analysts-journal/2002/the-statistics-of-sharpe-ratios); [IDEAS](https://ideas.repec.org/a/taf/ufajxx/v58y2002i4p36-52.html)
  - Under iid normality, SE(SR̂) ≈ √((1 + SR²/2)/n), with SR measured per period and n the number of periods. This form is from a secondary source — [QuantVault](https://quantvault.org/problem-1904-asymptotic-distribution-of-the-sharpe-ratio.html)

### Inferences
- The diagnostics answer different questions:
  - DSR: given N trials, is the selected strategy's Sharpe credible? It needs an honest trial count and the variance of Sharpe across trials.
  - PBO/CSCV: is the selection process overfit? It needs the full returns matrix of every variant tried, so log every variant's per-period P&L, not just the winner's.
  - MinBTL: is the sample long enough for the number of trials? This is a planning tool to use before backtesting.
- For 30-minute bars, compute Sharpe on daily (or per-trade) P&L. Do not annualize 30-minute bar Sharpe by √(13 × 252): intraday autocorrelation and the gaps between days make that scaling unreliable (Lo 2002).
- PBO's warning that hold-out is unreliable matters for the dev/holdout design. A single holdout of a few years has low power (see section 5). It is better treated as a check that the strategy doesn't collapse than as proof of edge. CSCV inside the development set adds information.

### Gaps
- I could not access the full Notices paper. Its claim that overfitting under memory effects such as mean reversion produces negative expected out-of-sample performance is from my memory and unverified here.
- I did not check PBO values from the paper's own examples or the exact DSR formula against the JPM text; the formula above comes from secondary sources.

---

## 5. Practical power and trial accounting for one instrument (about 10 years of QQQ 30-minute bars, about 40 quarters, few down quarters)

### Takeaway
Statistical power depends on calendar time and the annualized Sharpe, not on the number of bars. With 10 years, only an annualized Sharpe of about 1.0 or higher can clear t = 3. A Sharpe of 0.5 can't reach even t = 2: that needs 16 years, or 25–31 years for 80% power. In a down-market regime with only about 2 years of data, the standard error of the Sharpe is about ±0.7, so regime-level conclusions are close to anecdotal unless the regime Sharpe is above about 1.4. Every variant tried has to be counted and fed into Holm/BHY, DSR or PBO.

### Cited Findings
- **Basis for the power numbers:** SE(SR̂) ≈ √((1+SR²/2)/n) under iid (Lo 2002), so t ≈ annualized SR × √years — [QuantVault on Lo's result](https://quantvault.org/problem-1904-asymptotic-distribution-of-the-sharpe-ratio.html); [Lo 2002 abstract](https://ideas.repec.org/a/taf/ufajxx/v58y2002i4p36-52.html)
- **Thresholds the study should be measured against:** t > 3.0 ([HLZ](https://www.nber.org/papers/w20592)) or 3.4–3.8 ([Chordia–Goyal–Saretto](https://ideas.repec.org/a/oup/rfinst/v33y2020i5p2134-2179..html))
- **Accounting for variants (both from Bailey et al.):**
  - Effective N falls when trials are correlated, so count and cluster the trials — [lecture notes on Bailey et al.](https://cs.runi.ac.il/~kipnis/notes/STATS_207_L18.pdf); [Wikipedia DSR](https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio)
  - Hold-out alone is unreliable — [PBO SSRN](https://papers.ssrn.com/abstract=2326253)
- **Tools that test "the best of K rules":**
  - White's Reality Check: bootstrap, controls familywise error — [White 2000](https://onlinelibrary.wiley.com/doi/abs/10.1111/1468-0262.00152)
  - Hansen's SPA: more powerful, less sensitive to poor rules — [Hsu & Kuan 2005](https://ideas.repec.org/a/oup/jfinec/v3y2005i4p606-628.html)
  - Stepwise SPA / Romano–Wolf: identifies which rules are significant — [Hsu, Taylor & Wang 2016](https://ideas.repec.org/a/eee/inecon/v102y2016icp188-208.html)
  - FDR (Benjamini–Hochberg/BHY, or Barras–Scaillet–Wermers style): more lenient and gives a set of rules — [Bajgrowicz & Scaillet 2012](https://ideas.repec.org:443/a/eee/jfinec/v106y2012i3p473-491.html)
- **Persistence:** Bajgrowicz & Scaillet found that even rules flagged by FDR could not be selected ex ante to persist. Selecting on past winners is the step that fails — [IDEAS](https://ideas.repec.org:443/a/eee/jfinec/v106y2012i3p473-491.html)

**My calculations (iid normal; real intraday P&L with fat tails or negative skew will be worse):**

Years of data needed, by true annualized Sharpe:

| True annualized SR | for t = 2 | for t = 3 | for 80% power, one-sided 5% | for 80% power, two-sided 5% |
|---|---|---|---|---|
| 0.5 | 16 | 36 | 24.7 | 31.4 |
| 1.0 | 4 | 9 | 6.2 | 7.8 |
| 1.5 | 1.8 | 4 | 2.7 | 3.5 |
| 2.0 | 1.0 | 2.2 | 1.5 | 2.0 |

t-statistic achieved for a given true Sharpe and sample length:

| True annualized SR | 2 years (≈ 8 down quarters) | 3 years (≈ 12-quarter holdout) | 7 years | 10 years |
|---|---|---|---|---|
| 0.5 | 0.71 | 0.87 | 1.32 | 1.58 |
| 1.0 | 1.41 | 1.73 | 2.65 | 3.16 |

**Trades needed:** per-trade Sharpe = annual SR / √(trades per year), so trades needed for t = 2 = 4 × trades per year / SR². The calendar time needed is the same whatever the trade frequency:

| Annualized SR | Trades per year | Trades needed for t = 2 | Trades needed for t = 3 |
|---|---|---|---|
| 1.0 | 25 | 100 | 225 |
| 1.0 | 100 | 400 | 900 |
| 1.0 | 250 | 1,000 | 2,250 |
| 0.5 | 25 | 400 | 900 |
| 0.5 | 100 | 1,600 | 3,600 |
| 0.5 | 250 | 4,000 | 9,000 |

Trading more often helps only if it actually raises the annualized Sharpe through more independent bets.

### Inferences
- **What power to expect:** with about 10 years, the study can separate "Sharpe ≥ about 1 after costs" from zero. It cannot separate 0.5 from 0. Most honest single-instrument QQQ strategies will probably land in the inconclusive zone. The write-up should say so and not over-interpret t ≈ 1.5–2.
- **Regime splits:** with about 8 down quarters (≈ 2 years), the standard error of the regime Sharpe is about 0.7. A strategy needs a down-regime Sharpe of about 1.4 or more just to reach t = 2.
  - Report regime results as descriptive, with confidence intervals (block-bootstrap by day or by quarter).
  - Don't treat them as tests, and don't pick or tune strategies on regime-conditional performance. Every regime cut multiplies the effective number of tests.
  - Regime labels (up / sideways / down quarter) are defined after the fact. That is fine for description but not a tradeable signal, unless the strategy's regime detection uses only data available at the time.
- **The pre-registered holdout:** a 3-year (12-quarter) holdout has a Sharpe standard error of about 0.58. It can reject "this was pure overfitting" only for strategies whose development-set Sharpe was well above 1. Use it once, and report it however it turns out.
- **Accounting for variants:**
  1. Keep a trial log with every parameter set, filter and exit rule tried, including ones dropped after "logic analysis" that were still looked at on data.
  2. Estimate the effective N by clustering variant return correlations.
  3. Report the deflated Sharpe ratio using that N, and the Harvey–Liu haircut (Holm/BHY).
  4. Where a grid of variants exists, report PBO from CSCV on the development set.
  5. Use a Reality Check or SPA bootstrap when comparing a family of rules with buy-and-hold QQQ. Use a stationary or block bootstrap (by day) to keep intraday dependence intact.
  6. Use MinBTL before testing: with 10 years and a target spurious-Sharpe ceiling of about 0.7, keep effective independent trials to about 45 or fewer; for a ceiling of about 0.5, about 10 or fewer.
- **Benchmarks and costs:** compare with buy-and-hold QQQ on a risk-adjusted basis, and with exposure-matched passive positions for strategies that are only partly invested. Include spread, commission and slippage for each 30-minute round trip. Costs are what killed the DJIA results (Bajgrowicz & Scaillet).
- **Expected decay:** treat any backtested Sharpe as an upper bound and plan on roughly 25–75% decay. That range runs from McLean & Pontiff's 26% out-of-sample decline, through Falck et al.'s ~50%, to Suhonen et al.'s 73% for practitioner backtests. Use the larger end for complex or heavily iterated strategies.

### Gaps
- All power figures assume iid normal returns. I did not compute Mertens/non-normal standard errors for actual QQQ 30-minute strategy P&L. Negative skew and fat tails (common in mean-reversion and option-like intraday strategies) widen the intervals.
- I found no published power analysis specific to intraday single-ETF strategies.
- I found no published guidance on the right block length for bootstrapping 30-minute bar P&L. Practical choices (block by day or by week) are judgment calls, not sourced findings.
