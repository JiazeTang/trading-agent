# Risk-Management, Position-Sizing and Process Principles of Famous Discretionary Traders — and What the Evidence Says

(Research notes, compiled 2026-10-19. Context: retail account of about 8,000 USD. Plan: ~50% in 3 semiconductor mean-reversion positions with -15% to -20% stops; ~30% in REGN/VRTX; ~20% cash. Backtest win rate 60–78%, holding-period drawdowns 6–10%, occasional gap-through-stop losses of about -25%.)

**Source-quality legend used below:**
- **[Q]**: direct quote, wording confirmed in a primary or near-primary source (book excerpt, author's own site, paper abstract).
- **[P]**: paraphrase, or a quote that circulates only on secondary sites with varying wording. Check it against the book before citing it verbatim.
- **[E]**: empirical or academic evidence.
- **[I]**: my own inference or arithmetic, not sourced.

**Survivorship-bias caveat (applies to the whole first section).** The traders interviewed in *Market Wizards* were picked *because* they survived and became famous. Many traders who followed the same rules (5:1 setups, concentration "when conviction is high", pyramiding) blew up and were never interviewed. Their rules are therefore **hypotheses, not evidence**. The academic evidence on what makes ordinary traders fail is more reliable than the stories about what made these few succeed. Livermore is the clearest cautionary case: the book about him, *Reminiscences of a Stock Operator*, is a thinly fictionalised biography written by Edwin Lefèvre, so the narrator's words are Lefèvre's rendering ([Project Gutenberg edition](https://gutenberg.org/files/60979/60979-h/60979-h.htm); characterization via [secondary summary](https://completetradersedge.com/jesse-livermore-greatest-speculator/)). It is widely reported that Livermore went bankrupt several times and died by suicide in 1940. I did not fetch a source for that in this session; it is common knowledge, so verify it before citing.

---

## Q1. What concrete rules have PTJ, Druckenmiller, Thorp, Kovner, Marcus, Brandt and Livermore stated?

### Takeaway
Almost every one of these traders says some version of three things: (a) keep the risk on any single trade small and known in advance (Brandt and Kovner: ≤1% of capital); (b) cut losers fast and never add to them (PTJ: "Losers average losers"); (c) only go big after you have a cushion and very high conviction (Druckenmiller, Soros). The concrete numbers are 1% maximum risk per trade, 0.5–0.7% in practice for Brandt, 5:1 reward/risk for PTJ, and fractional Kelly for Thorp. None of these rules has been validated as causing their success.

### Cited Findings

**Paul Tudor Jones (PTJ)**
- [P] **5:1 reward/risk.** He describes "risking one dollar to make five", which lets him be right only 20% of the time; "I can be wrong 80% of the time, and I'm still not going to lose." This comes from a Tony Robbins interview transcript (published in Robbins' *Money: Master the Game*, 2014) as reproduced on [trendfollowing.com](https://www.trendfollowing.com/paul-tudor-jones/) and quote collections ([TraderLion](https://traderlion.com/quotes/paul-tudor-jones-quotes/)). Wording varies across sites.
- [P] **200-day moving average.** He is quoted as saying: "My metric for everything I look at is the 200-day moving average of closing prices… If you use the 200-day moving average rule, then you get out. You play defense, and you get out." Same Robbins interview, via [trendfollowing.com](https://www.trendfollowing.com/paul-tudor-jones/) and [25iq](https://25iq.com/2015/07/25/a-dozen-things-ive-learned-from-paul-tudor-jones-about-investing-and-trading/). A claim that his 1987 short was triggered by the 200-day average is unsourced. LuxAlgo-type marketing pages add RSI and MACD details that are not verifiable ([LuxAlgo](https://www.luxalgo.com/blog/paul-tudor-jones-macro-playbook-for-traders/)).
- [P] **Scaling with performance.** Quote sites say he "scales down when he's losing and scales up when he's winning" ([TraderLion](https://traderlion.com/quotes/paul-tudor-jones-quotes/)).
- [P] **"Losers average losers."** This was a sheet of paper on the wall of his office, visible in a well-known photo. It is not from a speech ([TurtleTrader](https://www.turtletrader.com/losers-average-losers/), [habrador blog](https://blog.habrador.com/2011/08/paul-tudor-jones-losers-average-losers.html)).
- **Correction to the brief:** I found **no source for a 2009 UVA talk**. The well-documented UVA appearance is an April 2013 McIntire School of Commerce symposium, best known for his remarks about women in macro trading ([ABC News](https://abcnews.go.com/blogs/politics/2013/05/investor-paul-tudor-jones-says-mothers-cant-be-top-traders), [KERA/NPR](https://www.keranews.org/2013-05-24/hedge-fund-manager-apologizes-for-comments-on-female-traders)). Popular "PTJ defense first" lessons are often attributed to a UVA talk. Treat that attribution as unverified.

**Stanley Druckenmiller**
- [Q, via book excerpt summary] "George Soros has a philosophy that I have also adopted: The way to build long-term returns is through preservation of capital and home runs." From Schwager, *The New Market Wizards*, reproduced by [MarketFolly](https://marketfolly.com/2013/03/lessons-from-stanley-druckenmiller.html?m=0) and [Hedgeye](https://app.hedgeye.com/insights/48502-preservation-of-capital). The variant "superior long-term returns" appears to be a later rewording.
- [P] **Concentration only after a cushion.** "Grind it out until you're up 30 or 40 percent, and then if you have the convictions, go for a 100 percent year" ([MarketFolly summary](https://marketfolly.com/2013/03/lessons-from-stanley-druckenmiller.html?m=0)).
- [P] **Conviction.** Soros taught him "when you have tremendous conviction on a trade, you have to go for the jugular" ([MarketFolly](https://marketfolly.com/2013/03/lessons-from-stanley-druckenmiller.html?m=0); [Antoine Buteau profile](https://www.antoinebuteau.com/lessons-from-stanley-druckenmiller.md)).
- [I] For this trader, the key structural point is that Druckenmiller makes concentration conditional on two things: a prior profit cushion and capital preservation coming first. His "home runs" come from a professional with decades of record. A small account that concentrates *before* it has a cushion is doing the opposite of what he describes.

**Ed Thorp**
- [Q, headings only] Thorp's paper "The Kelly Criterion in Blackjack, Sports Betting and the Stock Market" (1997; Ch. 9 of *Finding the Edge*) contains a section titled "The case for 'fractional Kelly'" and analyzes the probability of falling to a fraction of the starting bankroll ([Oxy mirror](https://sites.oxy.edu/lengyel/M330/thorp/paper.htm), [Gwern PDF](https://www.Gwern.net/doc/statistics/decision/2006-thorp.pdf)). I saw the headings, not the full text.
- [E] MacLean, Thorp and Ziemba (2010, *Quantitative Finance*), "Good and bad properties of the Kelly and fractional Kelly criteria":
  - Kelly maximizes long-run growth.
  - "Its suggested wagers may be very large, so the Kelly criterion is relatively risky in the short term."
  - Fractional Kelly, which blends the Kelly bet with cash, reduces this risk at the cost of lower expected final wealth ([Berkeley PDF](https://www.stat.berkeley.edu/~aldous/157/Papers/Good_Bad_Kelly.pdf)).
- [P] Practitioners commonly bet ½ or ¼ Kelly because overbetting is penalized more heavily than underbetting. In the idealized model, the chance that a full-Kelly bettor's bankroll halves at some point is about 50% ([LuxAlgo explainer](https://www.luxalgo.com/library/concept/kelly-criterion.md); this is a secondary, commercial source).
- [I] Under the standard approximation, a bettor at fraction f of Kelly earns about (2f − f²) of the maximum growth rate. Half Kelly therefore keeps about 75% of the growth with about 25% of the variance. This is my derivation and is not confirmed verbatim in the fetched sources.

**Bruce Kovner**
- [P] "Undertrade, undertrade, undertrade is my second piece of advice." He also advises cutting whatever position size you were planning "at least in half" ([TurtleTrader quotes](https://www.turtletrader.com/?p=1161); [Antoine Buteau](https://www.antoinebuteau.com/lessons-from-bruce-kovner/)).
- [P] Kovner caps the risk on each individual trade at **≤1% of total capital** (per a [Shortform summary of Market Wizards](https://www.shortform.com/pdf/market-wizards-pdf-jack-d-schwager)). The exact "never risk more than 1 percent" wording is not verified.
- [P] He also places stops beyond technical levels so that the stop marks the point where the trade idea is proven wrong (widely repeated; not verified in this session).

**Michael Marcus**
- [P] The only Marcus-linked rule I could confirm is indirect. Kovner credits Marcus with teaching him that a trader should make a best judgment, accept being wrong, and keep making fresh judgments ([TurtleTrader](https://www.turtletrader.com/?p=1161); [AAO Research on Kovner](https://aaoresearch.substack.com/p/breaking-it-down-bruce-kovner)). I did not verify the commonly cited Marcus advice to cut losses and not over-trade against his *Market Wizards* chapter.

**Peter Brandt**
- [Q, own blog, via search snippet] He limits risk to "1% of capital max per trade," with trade size based on this. His initial risk per trade "seldom exceeds 70 basis points" and is limited to 100 bp ([peterlbrandt.com, Nov 2017](https://www.peterlbrandt.com/2017/11)). Direct fetch failed with a DNS error, so this is from search snippets of his own site.
- [P] In recent podcasts he says he risks less than 1% per trade (60–70 bp), cuts losses quickly, and "never pyramids" ([Podwise episode summary](https://podwise.ai/episodes/8611791)).
- [P] A secondary compilation quotes him: "if more than 3% risk per trade then plan to go bust," and says he personally uses about 0.5% ([PursuitOfEdge wiki](https://github-wiki-see.page/m/PursuitOfEdge/books/wiki/*Drawdown)). Not verified.
- **Gap:** I found **no source for a Brandt weekly or monthly loss limit**. Do not attribute one to him.

**Jesse Livermore (via Lefèvre)**
- [Q] "Prices, like everything else, move along the line of least resistance" (*Reminiscences*; [Gutenberg](https://gutenberg.org/files/60979/60979-h/60979-h.htm); [trendfollowing.com excerpt](https://www.trendfollowing.com/2006/12/27/jesse-livermore-reminiscences-of-a-stock-operator/)).
- [P] **Pyramiding and probing.** He would take a partial initial position and add only after price moved in his favour to confirm the thesis ([LuxAlgo pyramiding](https://www.luxalgo.com/library/concept/pyramiding.md); [TheStreet "How to probe for profits"](https://pro.thestreet.com/market-commentary/how-to-probe-for-profits89)). The exact word "probing" is not confirmed in the book's text.

### Inferences
- [I] **Pyramiding into winners conflicts with this trader's strategy.** Livermore's adding-on-confirmation and PTJ's "scale up when winning" are trend-following ideas. A mean-reversion entry *buys weakness*, so "never average losers" applies directly: do not add to a semiconductor name that keeps falling toward the -15% stop.
- [I] **PTJ's 5:1 is incompatible with a high-win-rate strategy.** The trader's backtest has a 60–78% win rate, with exits at the 20-day mean and stops at -15% to -20%, which implies average win < average loss. The PTJ logic to borrow is *expectancy*: know your payoff ratio. A 70% win rate with avg win of +8% and avg loss of -18% gives 0.7×8 − 0.3×18 = +0.2% per trade, which is barely positive. One -25% gap per 10 trades then wipes out a large share of the edge. This is illustrative arithmetic with hypothetical payoff sizes.
- [I] **The PTJ 200-day rule could serve as a regime filter.** For example, take no new semiconductor longs when SOXX/SMH or QQQ is below its 200-day MA. This is a testable hypothesis in the trader's own backtest, not a proven rule.

### Gaps
- No verified primary text for PTJ's "defense first" talk; the 2009 UVA date appears to be wrong.
- No Brandt monthly or weekly loss limit found.
- Kovner's exact "1%" wording and Marcus's own rules are not verified against the book text.
- Fetches of peterlbrandt.com, trendfollowing.com and faculty.haas.berkeley.edu failed with DNS errors, so some items rely on search-engine snippets of those primary pages.

---

## Q2. Which position-sizing framework works best for a small account with a few correlated positions?

### Takeaway
The best evidence supports two approaches: **volatility-scaled sizing**, which reduces left-tail events and maximum drawdowns, and **fractional (not full) Kelly**, which cuts short-run risk at a modest cost to growth. Fixed-fractional risk of 0.5–1% per trade is the practitioner standard (Brandt, Kovner), but it is supported by arithmetic and anecdote rather than controlled studies. For correlated positions, sizing must be done at the **portfolio/sector level**, and the risk budget must be computed from the **gap loss, not the stop distance**.

### Cited Findings
- [E] **Volatility targeting.** Harvey et al. (2018, *JPM*) studied 60+ assets, with data back to 1926. Volatility targeting:
  - lowers the probability of extreme returns across all asset classes;
  - reduces maximum drawdowns for balanced and risk-parity portfolios;
  - improves Sharpe ratios only for risk assets such as equities and credit.
  The mechanism: "left-tail events tend to be less severe, as they typically occur at times of elevated volatility," when a vol-targeted position is smaller ([Duke PDF](https://people.duke.edu/~charvey/Research/Published_Papers/P135_The_impact_of.pdf); [Alpha Architect summary](https://alphaarchitect.com/volatility-targeting-improves-risk-adjusted-returns/); [Quantpedia](https://quantpedia.com/the-impact-of-volatility-targeting-on-equities-bonds-commodities-and-currencies)).
- [E] **Fractional Kelly.** Full Kelly is "relatively risky in the short term". Fractional Kelly (Kelly blended with cash) trades growth for lower risk ([MacLean, Thorp & Ziemba 2010](https://www.stat.berkeley.edu/~aldous/157/Papers/Good_Bad_Kelly.pdf)). An experimental review of betting strategies found that drawdown-constrained Kelly performed similarly to simple fractional Kelly, which supports using the simple version ([arXiv 2107.08827](https://arxiv.org/pdf/2107.08827)).
- [E] **Stop-loss rules.** Kaminski & Lo ("When Do Stop-Loss Rules Stop Losses?", *J. Financial Markets* 2014) show that under a random walk, simple 0/1 stop-loss rules always reduce expected return. They add value only when returns have momentum. Empirically, some stop policies on US equities raised returns and cut volatility at longer sampling frequencies ([MIT DSpace](https://dspace.mit.edu/handle/1721.1/114876); [RePEc](https://ideas.repec.org/a/eee/finmar/v18y2014icp234-254.html)).
- [P] **Practitioner fixed-fractional numbers.** Brandt: ≤1% maximum, typically 0.6–0.7% ([peterlbrandt.com](https://www.peterlbrandt.com/2017/11)). Kovner: ≤1% ([Shortform](https://www.shortform.com/pdf/market-wizards-pdf-jack-d-schwager)). PTJ: cut size when losing ([TraderLion](https://traderlion.com/quotes/paul-tudor-jones-quotes/)).

### Inferences
- [I] **Kaminski–Lo applied to mean reversion.** Their result implies that tight stops on a *mean-reverting* strategy systematically cut winners: in a mean-reverting process, falling further raises the expected rebound. This is consistent with the trader's backtest finding that wide stops (-15% to -20%) are needed. The consequence is that **the stop is mainly a disaster brake, not the risk-control tool**. Risk must instead be controlled through **position size**.
- [I] **Current-plan arithmetic (8,000 USD, 3 semiconductor positions ≈ 1,333 USD each ≈ 16.7% of equity):**
  - Stop at -15% → about 2.5% of equity at risk per position. Stop at -20% → 3.3%.
  - A -25% gap → about 4.2% of equity per position.
  - Combined "portfolio heat" (all stops hit) = 7.5–10% of equity; all three gapping -25% together = 12.5%.
  - The three semiconductor positions are highly correlated (same sector, same macro and earnings factor), so treat them as roughly **one bet of about 50% of equity**. An NVDA or TSMC earnings shock, or an export-control headline, can hit all three at once.
  - Compared with the 0.5–1% per-trade risk Brandt and Kovner use, this plan is **2.5–4x more aggressive per trade**.
- [I] **Gap-adjusted fixed-fractional sizing example.** Position size = (equity × risk%) / (worst plausible loss %). Using the observed -25% gap as the worst plausible loss and 1% risk: 8,000 × 1% / 25% = 320 USD per position (4% of equity). At 2% risk: 640 USD (8%). This shows the trade-off clearly: Brandt-level risk makes positions small, so either accept higher per-trade risk explicitly or reduce the number of correlated names.
- [I] **A more practical middle ground:**
  - Cap combined semiconductor gap risk at about 6–8% of equity. Example: 3 × 2,000 USD × 25% gap = 1,500 USD = 18.75%, which is too high; 3 × 700 USD → 525 USD ≈ 6.6%.
  - Or hold 1–2 semiconductor names instead of 3.
  - Scale each position inversely to its recent volatility (e.g., 20-day ATR or realized vol), in line with Harvey et al. This means smaller positions in a high-volatility name (SMCI-type) and larger ones in lower-volatility names (QQQ, TXN-type).
- [I] **Kelly numbers are hard to use here.** The edge is small and its estimate is noisy: a 60–78% backtest win rate is in-sample, and the gap tail is fat. Overestimating edge leads to overbetting, and the Kelly penalty for overbetting is asymmetric. If Kelly is used at all, use ≤¼ Kelly on *out-of-sample* estimates, and treat it as an upper bound, not a target.
- [I] **Drawdown-based de-risking.** Example: halve the risk unit after a 10% equity drawdown, and halve again at 15%. This is consistent with PTJ's practice and with the general logic of vol targeting. I found no controlled study showing that it improves outcomes for discretionary equity traders; its main proven benefit is mechanical (it caps ruin probability).

### Gaps
- No academic study found that directly compares fixed-fractional, ATR/vol-based and Kelly sizing for *small retail accounts with a few correlated positions*.
- No empirical evidence found specifically on "maximum portfolio heat" limits (practitioner concept only).

---

## Q3. Do trading journals, pre-defined plans and process rules help?

### Takeaway
Direct causal evidence that journals or checklists improve retail trading P&L is **thin to absent** in what I found. The indirect evidence is strong, though: investors learn slowly from experience, much apparent "learning" is really bad traders quitting, and pre-committed exit rules (stop orders) are associated with a weaker disposition effect. A journal that records R-multiples is mainly the tool to detect *whether you have an edge at all* before attrition does it for you.

### Cited Findings
- [E] **Learning by trading.** Seru, Shumway & Stoffman ("Learning by Trading", *RFS* 2010, 23(2):705–739) used nine years of individual-investor records. Some investors improve with experience, but **a substantial part of aggregate "learning" comes from poor traders quitting** after discovering low ability. Ignoring attrition "significantly overestimates" how quickly investors improve ([RePEc](https://ideas.repec.org/a/oup/rfinst/v23y2010i2p705-739.html); [Stanford GSB](https://www.gsb.stanford.edu/faculty-research/publications/learning-trading)).
- [E] **Day traders in Taiwan.** Barber, Lee, Liu & Odean found that the aggregate performance of day traders is negative, and "over half of day trading can be traced to traders with considerable experience and a history of losses." This is inconsistent with rational learning ([Barber et al. working paper](https://faculty.haas.berkeley.edu/odean/papers/day%20traders/day%20trading%20and%20learning%20110217.pdf); [CXO summary](https://www.cxoadvisory.com/individual-investing/do-day-traders-make-money/)). Traders keep going despite losses, so feedback alone does not correct behavior.
- [E] **Experience and the disposition effect.** A Finnish study finds an asymmetric relationship: experience reduces the tendency to ride losses, but "no amount of trading experience is capable of eradicating" the propensity to realize gains early ([USyd repository](https://ses.library.usyd.edu.au/handle/2123/4073)).
- [E] **Pre-commitment.** A 2019 *Journal of Behavioral and Experimental Finance* paper studies "the disposition effect, performance, stop loss orders and education". Its title and indexing indicate it tests whether stop orders and education reduce the bias ([RePEc](https://ideas.repec.org/a/eee/beexfi/v24y2019ics2214635019300863.html)). I did not read the full findings, so I cannot state the direction or size of the effect.

### Inferences
- [I] **Why a journal matters.** Most "learning" is attrition, and experienced losers keep trading. A journal with R-multiples (P&L ÷ initial planned risk) creates the objective, falsifiable record that, by the evidence above, most retail traders lack. The relevant output is the *live* expectancy after 30–50 trades, compared against the backtest.
- [I] **Minimum journal fields for this strategy:**
  - entry signal value and planned exit (20-day mean or 2-month time stop);
  - stop price and planned R;
  - position size as a percentage of equity;
  - sector exposure at entry;
  - days to next earnings;
  - realized R, maximum adverse excursion, and whether the trade gapped through the stop;
  - deviations from the plan.

### Gaps
- No RCT or large-sample study found showing that journaling or checklists improve retail trading returns. Practitioner endorsements (e.g., Brandt and Schwager interviewees) are anecdotal.
- The direction and magnitude of the stop-order and disposition-effect result in the 2019 JBEF paper are unconfirmed (full text not read).

---

## Q4. Behavioral evidence on retail traders: disposition effect, overtrading, attention-buying, performance-chasing — and how professionals counter them

### Takeaway
The evidence is robust:
- Retail investors sell winners about 1.5x as readily as losers.
- The most active quintile under-performs the market by about 6.5 points a year.
- Retail investors net-buy attention-grabbing stocks, which then under-perform.

The professional rules (cut losers, don't average down, undertrade, pre-defined stops) target these documented biases directly. That makes them better supported than the "legend" stories themselves.

### Cited Findings
- [E] **Disposition effect (Odean 1998, *J. Finance* 53:1775–1798).** Based on 10,000 discount-brokerage accounts:
  - Investors show "a strong preference for realizing winners rather than losers."
  - The pattern is not justified by subsequent performance and lowers after-tax returns ([Odean paper page](https://faculty.haas.berkeley.edu/odean/papers/disposition/disposition.html); [CFA digest](https://rpc.cfainstitute.org/research/cfa-digest/1999/05/are-investors-reluctant-to-realize-their-losses-digest-summary)).
  - Proportion of gains realized (PGR) is about 14.8% versus proportion of losses realized (PLR) at about 9.8% outside December, a ratio of about 1.5 ([Wikipedia summary](https://en.wikipedia.org/wiki/Disposition_effect); [NTU repository](https://scholars.lib.ntu.edu.tw/handle/123456789/414550)).
  - December tax-loss selling reverses the pattern ([CFA digest](https://rpc.cfainstitute.org/research/cfa-digest/1999/05/are-investors-reluctant-to-realize-their-losses-digest-summary)).
- [E] **Overtrading (Barber & Odean 2000, *J. Finance*, "Trading Is Hazardous to Your Wealth").** Across 66,465 households, 1991–96:
  - The most active traders earned about 11.4% a year against 17.9% for the market.
  - The average household earned 16.4%, with about 75% annual turnover.
  - The authors attribute this to overconfidence ([Odean full-text PDF](https://faculty.haas.berkeley.edu/odean/Papers%20current%20versions/Individual_Investor_Performance_Final.pdf); [Hedge Fund Alpha summary](https://hedgefundalpha.com/strategies/common-stock-investment-performance-individual-investors/)).
  - **Counter-view:** Bonaparte, Cooper & Sha argue that rational agents facing adjustment costs can reproduce the same patterns ([NBER w25838](https://www.nber.org/system/files/working_papers/w25838/revisions/w25838.rev0.pdf)).
- [E] **Aggregate losses (Taiwan).** Barber, Lee, Liu & Odean (2009, *RFS*) find the aggregate portfolio of individuals suffers an annual performance penalty of 3.8 percentage points ([paper](https://faculty.haas.berkeley.edu/odean/papers%20current%20versions/justhowmuchdoindividualinvestorslose_rfs_2009.pdf)). Day trading was more than 20% of volume, and about 1% of individuals accounted for 50% of day trading ([CXO](https://www.cxoadvisory.com/individual-investing/do-day-traders-make-money/)). The figures "more than 80% lose in a typical 6-month period" and "fewer than 1% are predictably profitable" come only from a secondary statistics site ([Walnut Invest](https://walnutinvest.com/stats/day-trading-statistics)). They are consistent with Barber et al.'s skill papers ([Day Trading Skill PDF](https://faculty.haas.berkeley.edu/odean/papers/day%20traders/Day%20Trading%20Skill%20110523.pdf)), but I did not verify them against those papers.
- [E] **Attention-driven buying (Barber & Odean 2008, *RFS* 21(2):785–818, "All That Glitters").** Individuals are net buyers of attention-grabbing stocks: stocks in the news, with abnormal volume, or with extreme one-day returns. The cause is the search problem in buying, which does not arise when selling. Professionals are the least influenced by attention ([RePEc abstract](https://ideas.repec.org/a/oup/rfinst/v21y2008i2p785-818.html); [CXO summary](https://www.cxoadvisory.com/individual-investing/use-the-cone-of-silence-when-buying-stocks/)). Stocks bought on high-attention days subsequently under-perform, per the [CXO summary](https://www.cxoadvisory.com/individual-investing/use-the-cone-of-silence-when-buying-stocks/) (secondary).
- [P] **Professional counters** map onto these biases:
  - "Losers average losers" (PTJ) counters riding and adding to losers ([TurtleTrader](https://www.turtletrader.com/losers-average-losers/)).
  - "Undertrade" (Kovner) counters overconfidence and over-sizing ([TurtleTrader](https://www.turtletrader.com/?p=1161)).
  - Fixed ≤1% risk with sizing derived from the stop (Brandt) is a pre-commitment ([peterlbrandt.com](https://www.peterlbrandt.com/2017/11)).
  - Accepting being wrong and making a fresh judgment (Marcus → Kovner) counters anchoring on the entry price ([TurtleTrader](https://www.turtletrader.com/?p=1161)).

### Inferences
- [I] **This strategy carries built-in disposition risk.** Mean reversion *by design* takes profits quickly (exit at the 20-day mean) and holds losers through a wide stop. That is behaviorally identical to the disposition effect. It is legitimate here only because the backtest says so. The danger is *discretionary* override: widening the stop beyond -20%, adding to a loser, or "giving it another week" past the 2-month time stop. Those overrides are exactly the biases documented above. Make the stop and time-stop non-negotiable: hard orders, logged in the journal.
- [I] **Attention bias in the universe.** Semiconductors are the most attention-grabbing sector of the 2024–26 market. Requiring a written signal (Z-score, RSI, etc.) before *any* buy, and never buying on a news day without one, is a direct counter to the Barber–Odean attention effect.
- [I] **Overtrading.** With three concurrent positions and ~2-month holds, turnover is moderate. The risk is *adding* unplanned trades. A cap on the number of open positions and on new entries per week enforces this.

### Gaps
- Odean's commonly quoted figure that winners sold out-perform losers held by about 3.4% over the following year was **not verified** in this session; the paper page fetch failed. Check it before citing.
- No specific evidence found on retail *performance-chasing* in individual stocks, beyond the attention effect and fund-flow literature not searched here.

---

## Q5. How do professionals handle earnings/event risk and gap risk?

### Takeaway
Earnings gaps happen overnight, when liquidity is thin, so **stop orders do not cap the loss**. That is exactly the trader's observed -25% gap-through. The practical defenses are:
- size so that the *gap* loss, not the stop loss, fits the risk budget;
- cut or exit short-term positions before earnings (including bellwether earnings such as NVDA or TSMC for semiconductors);
- use the options-implied move as a guide to event size.

### Cited Findings
- [E] **Overnight information.** Post-announcement information arrives largely overnight, when market liquidity is low. Researchers link this to a higher overnight risk premium and post-earnings drift ([OptionMetrics-hosted paper](https://optionmetrics.com/?p=2410)).
- [E] **Options as an event-size guide.** Arjun, Lipkin & Tatevossian (*Journal of Risk*, Jan 2025) derive the implied variance of the earnings window from pre-announcement implied vol. They find the options market generally predicts the price impact of earnings well, with outliers ([RePEc](https://ideas.repec.org/a/rsk/journ4/7960706.html)).
- [P/vendor] **Illustrative event sizes.** Market Chameleon reports average earnings gaps against implied moves:
  - GS: about 2.0% average opening gap versus ±3.8% implied; options overestimated the move 83% of the time since 2023.
  - C: about 1.8% gap versus ±5.4% implied.
  - LULU: median absolute move 6.9% versus 9.3% implied.
  Sources: [GS](https://marketchameleon.com/articles/i/2026/1/14/28117-traders-are-pricing-gs-earnings-move-at-4pct), [C](https://marketchameleon.com/articles/i/2025/4/14/25049-c-markets-are-pricing-a-large-earnings-move), [gap guide](https://marketchameleon.com/Instructional-Stock-and-Options-Trading-Videos/472/-How-to-Analyze-Historical-Earnings-Gap-Moves-|-Stock-Earnings-Strategy). Vendor data, not peer-reviewed. Semiconductor and small/mid-cap biotech moves are typically much larger than these bank examples; I found no specific figures in this session.
- [P] Brandt sizes every trade so the initial risk is ≤0.7–1% ([peterlbrandt.com](https://www.peterlbrandt.com/2017/11)). By construction, a gap of 2x the stop then costs ≤1.4–2%, not a catastrophe.

### Inferences
- [I] **Earnings rule for a 2-month holding period.** A ~2-month hold will almost always span one earnings report per name. Options:
  - (a) Exit or halve the position 1–2 days before the company's own earnings, and re-enter afterwards if the signal persists.
  - (b) Hold through earnings only at a size where a gap of about 2x the implied move fits the risk budget (e.g., ≤1–1.5% of equity).
  - (c) Also watch sector bellwethers (NVDA, TSMC, ASML, AMD earnings; export-control and tariff news), because the three semiconductor positions will gap together.
- [I] **Earnings in the "diversifiers".** REGN and VRTX are not event-free. Drug-trial readouts, FDA decisions and their own earnings can produce large single-day gaps. Their low correlation with semiconductors helps the portfolio but not the single-name tail. Size them with the same gap logic, and check the biotech catalyst calendar (PDUFA dates, trial readouts).
- [I] **Backtest the gap tail explicitly.** In the trader's backtest, measure the distribution of open-versus-stop slippage and the frequency of a -25% outcome. Then use, for example, the 95th–99th percentile gap loss (not the stop level) in the position-size formula.

### Gaps
- No peer-reviewed average absolute earnings-gap statistics found for semiconductors or large-cap biotech specifically.
- No primary quotes from the named legends specifically on holding through earnings. Most are futures/macro traders (PTJ, Kovner, Marcus, Brandt), for whom single-stock earnings are not central.

---

## Q6. A short list of concrete rules for a small retail trader (evidence-tagged)

### Takeaway
The rules with the best evidence or arithmetic support are:
1. Size by gap risk, with a small per-trade risk budget.
2. Treat correlated positions as one bet.
3. Pre-commit exits and never average down.
4. Scale size inversely to volatility.
5. Journal in R-multiples to test whether the live edge matches the backtest.
6. Avoid attention-driven unplanned trades.

Concentration "when conviction is high" and 5:1 setups are anecdotal and mismatched to a high-win-rate mean-reversion system.

### Cited Findings
(Each rule below reuses citations from Q1–Q5.)

1. **Per-trade risk budget of 0.5–1.5% of equity, measured at the *gap* loss rather than the stop.** Support: [P] Brandt ≤1% ([peterlbrandt.com](https://www.peterlbrandt.com/2017/11)) and Kovner ≤1% ([Shortform](https://www.shortform.com/pdf/market-wizards-pdf-jack-d-schwager)), plus [I] arithmetic. **Status: practitioner consensus plus arithmetic; no RCT.**
2. **Sector cap: total semiconductor gap-risk ≤ about 6–8% of equity, i.e. treat three semiconductor names as one bet.** Support: [I], building on the vol-targeting tail evidence ([Harvey et al. 2018](https://people.duke.edu/~charvey/Research/Published_Papers/P135_The_impact_of.pdf)). **Status: inference.**
3. **Volatility-scaled sizing: smaller positions in higher-ATR names and when market volatility (e.g., VIX or SOX realized vol) is elevated.** Support: [E] [Harvey et al. 2018](https://people.duke.edu/~charvey/Research/Published_Papers/P135_The_impact_of.pdf), which shows reduced left tail and max drawdown. **Status: evidence-backed, at asset and portfolio level.**
4. **Hard exits: the -15% to -20% stop is placed as an order at entry, plus the 2-month time stop and the 20-day-mean target. No widening and no adding to losers.** Support: [P] PTJ "Losers average losers" ([TurtleTrader](https://www.turtletrader.com/losers-average-losers/)); [E] the disposition effect harms returns ([Odean 1998](https://faculty.haas.berkeley.edu/odean/papers/disposition/disposition.html)); [E] Kaminski–Lo say stops cost return under no momentum, which is why the stop should be wide and size small ([MIT](https://dspace.mit.edu/handle/1721.1/114876)). **Status: partly evidence-backed.**
5. **Earnings rule: exit or halve before own earnings; be aware of bellwether earnings dates for the sector.** Support: [E] overnight information and low liquidity ([OptionMetrics paper](https://optionmetrics.com/?p=2410)); [E] options price the event size ([J. Risk 2025](https://ideas.repec.org/a/rsk/journ4/7960706.html)). **Status: evidence on the existence of gap risk; the rule itself is practitioner practice.**
6. **Drawdown circuit-breaker: after a -10% equity drawdown, halve the risk unit; after -15%, pause new entries and review.** Support: [P] PTJ scales down when losing ([TraderLion](https://traderlion.com/quotes/paul-tudor-jones-quotes/)); Kovner "undertrade" ([TurtleTrader](https://www.turtletrader.com/?p=1161)). **Status: anecdotal; mechanically limits ruin.**
7. **Kelly as a ceiling only: if computed at all, use ≤¼ Kelly on out-of-sample edge estimates.** Support: [E] [MacLean, Thorp & Ziemba 2010](https://www.stat.berkeley.edu/~aldous/157/Papers/Good_Bad_Kelly.pdf); [Thorp's "case for fractional Kelly"](https://sites.oxy.edu/lengyel/M330/thorp/paper.htm). **Status: theory-backed.**
8. **Trade journal with R-multiples and planned-versus-actual; compare live expectancy with the backtest after about 30 trades; stop or shrink if live R-expectancy is ≤0.** Support: [E] learning is slow and mostly attrition ([Seru et al. 2010](https://ideas.repec.org/a/oup/rfinst/v23y2010i2p705-739.html)); experienced losers keep trading ([Barber et al.](https://faculty.haas.berkeley.edu/odean/papers/day%20traders/day%20trading%20and%20learning%20110217.pdf)). **Status: indirect evidence that feedback is needed; no direct evidence that journals help.**
9. **No unplanned "news" buys: every entry needs the written signal; cap new entries per week.** Support: [E] attention-buying under-performs ([Barber & Odean 2008](https://ideas.repec.org/a/oup/rfinst/v21y2008i2p785-818.html)); overtrading under-performs ([Barber & Odean 2000](https://faculty.haas.berkeley.edu/odean/Papers%20current%20versions/Individual_Investor_Performance_Final.pdf)). **Status: evidence-backed (observational).**
10. **Optional regime filter: no new semiconductor longs when SMH or QQQ is below its 200-day MA. Backtest before adopting.** Support: [P] PTJ 200-day rule ([trendfollowing.com](https://www.trendfollowing.com/paul-tudor-jones/)). **Status: anecdotal; must be tested on the trader's own data.**

### Inferences
- [I] **Do not adopt "concentrate when conviction is high" yet.** Druckenmiller conditions it on a prior profit cushion and on capital preservation ([MarketFolly](https://marketfolly.com/2013/03/lessons-from-stanley-druckenmiller.html?m=0)). The current plan already has about 50% in one correlated sector, so it is already concentrated by sector.
- [I] **The biggest single change the evidence points to** is resizing the semiconductor block so that a simultaneous -25% gap across all semiconductor positions costs roughly 6–8% of equity rather than about 12.5%. A plausible version is 2 names at about 15% each, or 3 names at about 9–10% each, with the remainder in cash or QQQ. The second change is an earnings-avoidance rule.
- [I] **Expectancy check.** With a 60–78% win rate, the payoff ratio is below 1. A small decline in live win rate relative to the backtest (regime change, overfitting) can flip expectancy negative. This argues for smaller size during the first 30–50 live trades, until live R-expectancy confirms the backtest.

### Gaps
- No direct evidence that any specific numerical rule (1% vs 2% risk, -10% drawdown trigger) is optimal for a retail equity mean-reversion trader. The numbers are practitioner conventions.
- The legend quotes are subject to survivorship bias and to wording drift across secondary sites. For publication-grade citation, check the exact quotes against Schwager's *Market Wizards* (1989), *The New Market Wizards* (1992) and Robbins' *Money: Master the Game* (2014).
