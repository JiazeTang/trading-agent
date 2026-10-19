# Professional momentum / breakout / growth-stock swing traders: public methods and independent evidence (as of Oct 2026)

> Method note: in this session WebFetch and curl could not reach any page (DNS failures / proxy 403), so every finding below comes from **search-result snippets**, not full pages. Primary sources (the traders' books, the USIC official site, full academic PDFs) could not be read directly. Treat exact numbers as "reported by the cited page" and check them against the books before coding rules. Each finding is tagged:
> **[RULE]** the trader's stated rule · **[VERIFIED]** third-party verified/contest result · **[CLAIM]** self-reported or marketing figure · **[TEST]** independent test or academic evidence.

## 1. Mark Minervini: SEPA, Trend Template, VCP, stops/sizing, USIC results

### Takeaway
Minervini has two contest wins that the organizer confirms: 1997 (+155%) and 2021 (+334.8%, $1M+ stock division). His widely repeated "~220%/yr over 5 years, 33,500% total" record is self-reported and unaudited. The Trend Template is well documented: price above a rising 200-day line, MA stacking, ≥25–30% above the 52-week low, within 25% of the high, RS ≥ 70. I found **no independent, cost-adjusted, survivorship-controlled backtest** of the Trend Template or the VCP. The only "tests" available are TradingView community scripts with no reported out-of-sample results.

### Cited Findings
- **[RULE] Trend Template (8 criteria), as summarized by secondary sources:**
  1. Price above the 150-day and 200-day MA.
  2. 150-day MA above the 200-day MA.
  3. 200-day MA trending up for at least 1 month, preferably 4–5 months.
  4. 50-day MA above both the 150-day and 200-day.
  5. Price above the 50-day MA.
  6. Price well off its 52-week low (most sources say ≥25%; the TwP script notes *Trade Like a Stock Market Wizard* uses **30%**).
  7. Price within 25% of its 52-week high (some say ideally within 15%).
  8. RS rating ≥ 70 (some practitioners prefer ≥ 85).

  Sources: [TradingView TwP Trend Template script](https://www.tradingview.com/script/88aL78Qh-TwP-Mark-Minervini-Trend-Template-Criteria); [sharpely](https://sharpely.in/blogs/minervini-trend-template-for-stage2-stocks/); [playbooks.com swing-trading](https://playbooks.com/skills/copyleftdev/sk1llz/swing-trading); [Tabby script](https://cn.tradingview.com/script/8t4aFPdQ-Minervini-Trend-Template-by-Tabby)
- **[RULE] The RS criterion cannot be computed on TradingView** because IBD-style RS ratings aren't available there. Any replication needs its own cross-sectional RS ranking. — [TwP script](https://il.tradingview.com/script/88aL78Qh-TwP-Mark-Minervini-Trend-Template-Criteria)
- **[RULE] The user's "Kova Score" is not the Trend Template.** Kova uses short EMAs (10>20>50) plus "within 10% of the high". That is much tighter than Minervini's 50/150/200 stack with "within 25%". The comparison is from the criteria above.
- **[RULE] VCP and SEPA are documented in vendor and educational guides**, which describe successive tighter pullbacks with drying volume and a pivot-buy entry. These are educational or vendor pages, not primary text. — [finermarketpoints SEPA & VCP guide](https://www.finermarketpoints.com/post/what-is-mark-minervini-s-trading-strategy-the-complete-sepa-vcp-guide); [finermarketpoints VCP glossary](https://www.finermarketpoints.com/post/vcp-trading-terminology-glossary); [Tradingsim VCP guide](https://www.tradingsim.com/blog/volatility-contraction-pattern)
- **[RULE] Stops and sizing attributed to Minervini (secondary, mostly social posts):**
  - Risk 1.25%–2.5% of equity per trade.
  - Maximum stop 10%.
  - Average loss of about 5–6%.
  - Never more than 50% of the portfolio in one position.
  - "Progressive exposure": trade smaller when results are poor, larger when results are good, starting with pilot buys.

  Sources: [Ameet Rai on X](https://x.com/AmeetRai/status/1864744561668423792); [MARKET INSIGHTS on X](https://x.com/IManghaila/status/2050391132660457786)
- **[RULE] Other sources describe a hard 7–8% maximum stop**, inherited from O'Neil. One VCP guide says to risk no more than 1% of the account per VCP trade, and a Japanese-market adaptation tightens the stop to about 6%. — [quantstrategy.io SEPA explainer](https://quantstrategy.io/blog/sepa-strategy-explained-mastering-trend-following-with-mark/); [Tradingsim](https://www.tradingsim.com/blog/volatility-contraction-pattern); [KAKIO note.com (Japan)](https://note.com/kaki0/n/n3072c99a1c45?hl=en)
- **[VERIFIED] 2021 USIC:** Minervini won the $1,000,000+ stock division with +334.8%, beating the prior division record of +119.1% (George Tkaczuk, 2020). — [BusinessWire, 2022-01-24](https://www.businesswire.com/news/home/20220124005241/en/2021-United-States-Investing-Championship-Winners-Minervini-Smashes-Record); [PR Newswire](https://www.prnewswire.com/news-releases/stock-trader-wins-us-investing-championship-a-second-time--breaks-record-301466652.html)
- **[VERIFIED, organizer press release] 1997 USIC:** Minervini finished first with a 155% annual return. — [PR Newswire](https://www.prnewswire.com/news-releases/stock-trader-wins-us-investing-championship-a-second-time--breaks-record-301466652.html); [Kagels Trading USIC overview](https://kagels-trading.com/blog/us-investing-championship/)
- **[CLAIM] Multi-year record:** about 220% per year over roughly 5.5 years, a 33,500% compounded total, with only one losing quarter. I found no independent audit; the figure comes from his marketing and secondary blogs. — [wallstreettrader substack](https://wallstreettrader.substack.com/p/how-mark-minervini-won-us-investing); [24hmoney.vn](https://24hmoney.vn/news/10-triet-ly-giao-dich-giup-mark-minervini-kiem-33-500-trong-hon-5-nam-c30a2407417.html)
- **[VERIFIED, secondary description] How USIC checks results:** performance is checked against brokerage statements for each entrant's designated account. This is a secondary description; I could not reach the organizer's site. — [wallstreettrader substack](https://wallstreettrader.substack.com/p/how-mark-minervini-won-us-investing)
- **[CLAIM / marketing]** Minervini says his MPA clients and students "consistently dominated" the USIC leader list, and that one of them won in three of the past five years. This is self-promotion. — [Minervini on X](https://x.com/markminervini/status/1750158079000215644?lang=en)
- **[TEST, weak] The only "backtests" found are TradingView community scripts:**
  - One "Pure Mark Minervini 10% TP / 5% CL" script presents itself as a starting point that needs further fine-tuning; it does not report validated results. — [TradingView H9HxZ9Zc](https://de.tradingview.com/script/H9HxZ9Zc-Pure-Mark-Minervini-10-TP-5-CL)
  - A "balanced" variant uses 6 of the 8 rules and reports about 5–10 signals per stock per year, with no out-of-sample performance. — [TradingView search page](https://th.tradingview.com/scripts/search/200元+股票大盘/page-17)

### Inferences
- The Trend Template is a **universe filter** (Stage-2 uptrend), not an entry signal. Minervini's claimed edge is supposed to come from three things layered on top: the VCP entry timing, a tight stop (average loss of about 5–6%), and asymmetric sizing and pyramiding. The user's Kova test isolated only the filter, which explains why it added little in a semiconductor group that was already in a strong uptrend; nearly every name passed.
- A contest-winning year (155%, 334.8%) shows what is possible in a favorable year. It does not show a long-run expected return. USIC lets many entrants self-select, and only winners are publicized (see Section 5 on survivorship).

### Gaps
- I could not read *Trade Like a Stock Market Wizard* (2013) or *Think & Trade Like a Champion* (2017) directly. Exact VCP rules (number of contractions, depth limits, pivot definition) and the exact maximum-stop wording (7–8% vs 10%) need checking against the books.
- I found no academic or reputable quant-blog backtest of the full Trend Template + VCP system with costs and delisted stocks.
- The USIC official site (financial-competitions.com) was unreachable, so I could not confirm Minervini's division for 1997 or the exact verification procedure.

## 2. William O'Neil / IBD: CAN SLIM, RS Rating, cup-with-handle, 7–8% rule, "M" (FTD / distribution days)

### Takeaway
CAN SLIM has more outside testing than any other method in this set, but the evidence is weak in quality:
- AAII screen tracking, which shows strong but variant-dependent returns.
- A small group of papers by Lutey and coauthors, including a live paper-trading test (2014–2017) that beat the S&P 500 by about 20 points.
- Student theses.

I found no peer-reviewed test of IBD's proprietary RS Rating itself. The academic support for the "near 52-week high / relative strength" idea comes from the broader momentum literature (Section 5). The FTD and distribution-day definitions found are secondary encodings, with conflicting thresholds.

### Cited Findings
- **[RULE] RS Rating:** a percentile rank (1–99) of a stock's trailing 12-month price performance against all other stocks. An RS of 96 means the stock outperformed 96% of them. A secondary description says the most recent 3-month window gets double weight. — [tapeboard glossary](https://tapeboard.com/glossary/what-is-relative-strength)
- **[RULE] IBD weights RS and EPS ratings most heavily** in its Composite Rating, and has also introduced a 3-month RS rating that reacts faster. — [IBD via Yahoo Finance](https://hk.finance.yahoo.com/m/37dfff7f-e46c-304b-8f1a-8cbe706d4e07/how-to-invest:-3-month.html)
- **[RULE] Distribution day and follow-through day (FTD), as encoded in a TradingView script:**
  - Distribution day: an index decline of at least 0.2% on volume higher than the prior day.
  - FTD: a gain of at least 1.2% on higher volume than the prior day.

  IBD's thresholds have changed over time (older material often cites about 1.5–2%), so verify against IBD Market School. — [TradingView Distribution/FTD marker](https://www.tradingview.com/script/mrsKTQdQ-Distribution-Follow-Through-Day-Marker)
- **[CLAIM, anecdotal]** On IBD Market School, "half of FTDs fail". — [Motley Fool discussion board](https://discussion.fool.com/t/ibd-market-school/112218?page=6)
- **[TEST] AAII CAN SLIM screen tracking:**
  - AAII has tracked a revised CAN SLIM screen since 1998.
  - Reported cumulative return through end-2007: 743.8% (about 23.8%/yr), vs 51.3% for the S&P 500.
  - Figures quoted by IBD and AAII conflict across sources and windows: 350.3% for 1998–2003; 35.3%/yr for 1998–2009; 2,487.3% for 1998–2010.
  - One study found the AAII revised screen about 9.9% less effective than O'Neil's original criteria, though it still beat the market.

  Source: [AAII "Investing in Proven Growth Using CAN SLIM Revised"](https://www.aaii.com/journal/article/investing-in-proven-growth-using-can-slim-revised)
- **[TEST] Live paper-traded CAN SLIM (Lutey & Rayome, *Journal of Accounting and Finance* 22(2), 2022):**
  - Built from O'Neil's 1988 stock-selection rules.
  - Outperformed the S&P 500 by 20%, the Nasdaq by 9% and the Dow by 17% from July 2014 to February 2017.
  - Tracking stopped in 2017; this was paper trading, not real money.

  Source: [articlegateway JAF 5134](https://mail.articlegateway.com/index.php/JAF/article/view/5134)
- **[TEST] Other Lutey-group papers:**
  - Lutey, Hassan & Rayome (2018, *Asian Journal of Economic Modelling* 6(3)): a modified, weighted CAN SLIM beat the Dow on a risk-adjusted basis over 5-, 10- and 16-year windows, with weaker statistical evidence in the longest window. — [IDEAS/RePEc](https://ideas.repec.org/a/asi/ajemod/v6y2018i3p274-286id320.html)
  - Mukherjee & Lutey (2023, *Applied Finance Letters*): a simplified CAN SLIM model that they say consistently beats the S&P 500. — [Applied Finance Letters](https://ojs.aut.ac.nz/applied-finance-letters/article/view/632)
  - All three papers come from the same author group, and I found no independent replication.
- **[TEST] Theses:**
  - A Mahidol University (Thailand) thesis covering 2004–2022 found CANSLIM gave the highest return in its comparison, about 22.52%/yr equal-weighted, and the best risk-adjusted return. — [Mahidol thesis PDF](https://archive.cm.mahidol.ac.th/bitstream/123456789/5460/1/TP%20FM.025%202566.pdf)
  - An NCCU (Taiwan) thesis reviews Deboeck & Ultsch (1998), who tested the screen on 1999 Morningstar data with mixed results across industries. — [NCCU thesis](https://ah.lib.nccu.edu.tw/bitstream/140.119/33992/6/35201006.pdf)
- **[TEST] An older commentary (Interactive Advisors, 2011)** examines the value of relative-strength indicators. I could not read it in full. — [Interactive Advisors](https://investing.interactiveadvisors.com/2011/10/on-the-value-of-relative-strength-indicators)

### Inferences
- The CAN SLIM tests are **stock-selection screens held passively**. They do not test O'Neil's trading layer: cup-with-handle pivots, the 7–8% stop, or the M-rule exposure changes. The trading layer therefore remains essentially untested in the found literature.
- The "M" rule is the piece most relevant to the user's chop problem: get out or reduce exposure after distribution-day clusters, and re-enter on an FTD. Even IBD-community anecdotes say about half of FTDs fail. Its value is mainly in avoiding big bear markets, not in getting through chop cheaply.

### Gaps
- I could not access *How to Make Money in Stocks* to quote:
  - the exact cup-with-handle geometry (cup depth 12–33%, handle in the upper half, about 1–2 weeks, buy at the handle high plus about 10 cents on volume ≥ 40–50% above average — commonly cited but **not verified here**);
  - the exact 7–8% rule text (commonly "cut every loss at 7–8% below purchase price", **not verified here**);
  - the current IBD FTD threshold and distribution-day count (commonly "4–6 distribution days within about 25 sessions", **not verified here**).
- I found no peer-reviewed test of IBD's proprietary RS Rating or Composite Rating specifically.

## 3. Kristjan Kullamägi (Qullamaggie): breakouts, episodic pivots (EP), parabolic shorts

### Takeaway
His rules are unusually explicit:
- Enter on the opening-range high (1-, 5- or 60-minute).
- Stop at the low of the day, and skip the trade if that stop is wider than about 1 ADR/ATR.
- Sell 1/3–1/2 after 3–5 days and move the stop to breakeven.
- Trail the rest on the 10- or 20-day MA.

Verification is partial. A fan-built "Deep Dive" site says it reconstructed his trades from broker statements (2014–2018), stream equity, and public Swedish tax returns (2014–2022). His reported win rate is low (about 25–35%), and he had a very large 2022 drawdown (reported at $25M to $60M). The "$5k to $100M" story is self-reported.

### Cited Findings
- **[RULE] Entry:** on the opening-range high (the high of the first 1-, 5- or 60-minute candle). Longer windows give worse fills but filter out more false breakouts. — [qullamaggie.com, "3 timeless setups"](https://qullamaggie.com/my-3-timeless-setups-that-have-made-me-tens-of-millions/); [snappchart summary](https://www.snappchart.app/blog/beginner-playbook/qullamaggie-trading-strategy)
- **[RULE] Stop:** always at the low of the day. The stop should not be wider than the stock's ATR/ADR, and if the day's low is more than one ADR below entry, he skips the trade. — [qullamaggie.com](https://qullamaggie.com/my-3-timeless-setups-that-have-made-me-tens-of-millions/); [breakoutshappen](https://breakoutshappen.com/stock-news/how-to-trade-like-qullamaggie-setups-strategy-and-screener)
- **[RULE] Exits:**
  - Sell 1/3–1/2 after 3–5 days, then move the stop to breakeven.
  - Trail the remainder with the 10-day MA (recommended for beginners and faster stocks) or the 20-day MA (slower stocks).
  - One secondary source says the trail exit is the first *close* below the 10-day.

  Sources: [qullamaggie.com](https://qullamaggie.com/my-3-timeless-setups-that-have-made-me-tens-of-millions/); [ebc.com explainer](https://www.ebc.com/forex/qullamaggie-strategy-3-trading-setups)
- **[RULE] Episodic pivot:** documented in his own post on gap-ups driven by a catalyst. I could not read the post in full. — [qullamaggie.com EP post](https://qullamaggie.com/how-to-master-a-setup-episodic-pivots/)
- **[RULE, secondary] Sizing:** risk about 0.3–0.5% of the account per trade, rarely more than 1%, with positions typically 10–15% of the account. This comes from a single social post. — [Krishan Kapoor on X](https://x.com/KrishanKapoor27/status/1922685621329383467)
- **[RULE, secondary] Market filter:** he trades breakouts in uptrending or sideways markets and avoids downtrends. I found no primary source for a specific index-MA filter (e.g., Nasdaq above its 10/20-day MA). — [search summary of tradingresourcehub / Chat With Traders notes](https://tradingresourcehub.substack.com/p/interview-qullamaggie-chat-with-traders-part1)
- **[VERIFIED, partial and third-party] Deep Dive reconstruction:** the site says its record draws on broker statements for 2014–2018, daily equity from his streams for 2014–2019, and public Swedish tax returns for 2014–2022, covering 1,300+ trades. It lists a mid-2022 drawdown of about −$60M. — [Qullamaggie Deep Dive stats](https://app.qullamaggiedeepdive.com/stats)
- **[CLAIM] Win rate and returns:**
  - Reported win rate about 25% in 2019 and about 35% in 2020. — [Deep Dive](https://app.qullamaggiedeepdive.com/stats)
  - "$5k to $100M" narrative. — [magica summary](https://magica.com/youtube-summarizer/understanding-the-qullamaggie-stock-trading-strategy-from-5k-to-100-million-we5LLjFlHCc)
  - Another source says his returns are not independently audited and should be treated as self-reported, and cites Swedish tax records suggesting a loss of about $25M in 2022. The 2022 figures ($25M vs $60M) conflict. — [search-summarized secondary sources](https://www.ebc.com/forex/qullamaggie-strategy-3-trading-setups)

### Inferences
- His profile is the extreme version of the "low win rate, large winners" model. A 25–35% hit rate is only viable with very tight stops (low of day, ≤1 ADR) and a long trailing exit. The 2022 drawdown shows the cost when the regime turns.
- **For an $8,000 account,** the rules translate as follows. Risk of 0.3–1% is $24–$80 per trade. A low-of-day stop of about 3–5% on a semiconductor stock then implies a position of about $600–$2,600. That is mechanically feasible for liquid names (NVDA, AMD, MU, TSM).
- **Caveat on the intraday entry:** the opening-range entry needs intraday data and real-time execution. On daily bars it would have to be approximated, for example with a buy-stop at the prior high.

### Gaps
- I could not read the full EP or parabolic-short rules from his site (fetch blocked). Commonly cited EP criteria, such as a gap of ≥10% on a catalyst with heavy volume, are not verified here.
- I found no independent quantitative backtest of his three setups with costs.

## 4. David Ryan, Dan Zanger, Nicolas Darvas (brief)

### Takeaway
- **David Ryan** (O'Neil protégé): three consecutive USIC stock-division wins in the mid-1980s are well attested. The exact years and the cumulative figure vary by source.
- **Dan Zanger's** record-return claims are inconsistent (29,000% vs 164,000%; $11k to $18M) and unverified.
- **Darvas's** "$2M" is a 1960 memoir claim with no independent verification and no rigorous backtest.

### Cited Findings
- **[VERIFIED, contemporaneous press] David Ryan:**
  - USIC stock division about +161% in 1985 (per Schwager and a 1985 Los Angeles Times report) and about +160% in 1986. A third win (1987, over 100%) is commonly cited.
  - Sources disagree on the years. Minervini's book recalls 1984–1986, and another site says 1985–1990.
  - The widely quoted 1,379% cumulative figure doesn't reconcile with the annual numbers.

  Sources: [completetradersedge USIC table](https://completetradersedge.com/us-investing-championship/); [TurtleTrader](https://www.turtletrader.com/trader-ryan/); [tradingreviewers](https://www.tradingreviewers.com/david-ryan/); [EverybodyWiki](https://en.everybodywiki.com/David_Ryan_(investor))
- **[RULE] Ryan's method is CAN SLIM-derived** (he worked at William O'Neil + Co.). — [financialwisdomtv](https://www.financialwisdomtv.com/post/david-ryan-champion-trader); [tradingresourcehub "Lesson of Humility"](https://tradingresourcehub.substack.com/p/lesson-of-humility-from-david-ryan)
- **[CLAIM] Dan Zanger:** a "world record one-year appreciation of over 29,000%", vs another claim of 164,000% ($11k to $18M in about 18 months, or in under a year, in the late 1990s). The figures are inconsistent and come from forum or bio pages. — [Elite Trader thread](https://www.elitetrader.com/et/threads/best-investors-ever-your-ranking.294033/page-2); [bookbot bio](https://bookbot.com/a/1762094)
- **[RULE / CLAIM] Nicolas Darvas:**
  - *How I Made $2,000,000 in the Stock Market* (1960).
  - Method: buy stocks at all-time highs when they break above a consolidation "box" on rising volume, with a stop just below the box.
  - Claimed $36,000 → about $2M in about 18 months in the late 1950s; some accounts say $2.25M.

  Sources: [Wikipedia: Nicolas Darvas](https://en.wikipedia.org/wiki/Nicolas_Darvas); [tradethatswing](https://tradethatswing.com/the-technical-foundations-of-nicolas-darvass-trading-strategy/); [Chaikin PowerFeed](https://chaikinanalytics.com/powerfeed/articles/how-a-dancers-rules-beat-the-market)
- **[TEST] None found for Darvas.** Only TradingView scripts exist, with no independent results. — [TradingView Darvas Box strategy (Whitebox)](https://www.tradingview.com/script/QsAX8uN5-Darvas-Box-strategy-Whitebox)

### Inferences
- Darvas's box is the ancestor of the "new high + tight base + stop just under the base" structure that all later traders share. It is single-bull-market anecdotal evidence (late-1950s US).

### Gaps
- I found no verified Zanger brokerage audit or USIC entry.
- I could not access Ryan's Market Wizards interview text (Schwager, *Market Wizards*, 1989) to quote his rules.

## 5. Common elements and the evidence on regime filters, tight stops, pyramiding, and win-rate/payoff

### Takeaway
All these methods share six elements:
1. Trade only Stage-2 stocks near highs with high RS.
2. Enter on a breakout from a tight base.
3. Use a small fixed risk per trade: about 0.3–2.5% of equity, with stops of about 1 ADR to 7–8% (max 10%).
4. Sell part into strength and trail the rest.
5. Add to winners.
6. Change exposure with the market regime.

The "near 52-week high / relative strength" core has strong academic support (George & Hwang 2004). Academic work also shows momentum is regime-dependent: it is profitable after up-markets, and it crashes after declines and in high-volatility rebounds. The exit, sizing and pyramiding layers have essentially no independent testing. Contest and celebrity track records carry heavy survivorship bias.

### Cited Findings
- **[TEST] George & Hwang (2004), *Journal of Finance* 59, 2145–2176:**
  - Nearness to the 52-week high explains a large portion of momentum profits.
  - It dominates past individual and industry returns in forecasting future returns.
  - Its forecasts do not reverse in the long run (sample 1963–2001).

  Sources: [SUFE academic newsletter](https://academicnewsletter.sufe.edu.cn/info/361244); [CXO Advisory summary](https://www.cxoadvisory.com/1284/technical-trading/the-52-week-high-as-a-momentum-indicator-for-individual-stocks/)
- **[TEST] Mixed replications of the 52-week-high effect:**
  - Momentum and reversals co-exist in international stock indexes. — [NAU: 52-week high in international indexes](https://experts.nau.edu/en/publications/the-52-week-high-and-momentum-investing-in-international-stock-in/)
  - Alpha Architect discusses the 52-week-high signal against the q-factor model. — [Alpha Architect](https://alphaarchitect.com/52-week-high-q-factor-investment-model/)
  - A 52-week-high strategy on emerging-market indices was reported unprofitable (per search summary). — [Griffith repository](https://research-repository.griffith.edu.au/items/41995ba4-ea62-565b-bc6a-9233b7978ae0)
  - A Marquette paper links momentum crashes to the 52-week-high anchor. — [Marquette "Momentum Crashes and the 52-Week High"](https://epublications.marquette.edu/cgi/viewcontent.cgi?article=1168&context=fin_fac)
- **[TEST] Cooper, Gutierrez & Hameed (2004), "Market States and Momentum":** momentum profits depend on the prior market state. They are significantly larger after up-markets and weak after down-markets. — [ResearchGate](https://www.researchgate.net/publication/4769366_Market_States_and_Momentum)
- **[TEST] Daniel & Moskowitz, "Momentum Crashes" (NBER w20439; *Journal of Financial Economics* 2016):**
  - Momentum suffers infrequent but persistent strings of large losses.
  - The crashes are partly forecastable: they occur in "panic" states after market declines with high volatility, coinciding with sharp market rebounds.
  - This is consistent with Cooper et al.

  Sources: [NBER PDF](https://www.nber.org/system/files/working_papers/w20439/w20439.pdf); [kentdaniel.net](https://www.kentdaniel.net/papers/published/mom12.pdf); [Columbia](https://business.columbia.edu/faculty/research/momentum-crashes)
- **[TEST] Momentum profitability varies with market illiquidity over time** (Avramov, Cheng & Hameed). — [QMUL conference PDF](https://www.qmul.ac.uk/business-school/media/qmbs/newsandevents/events/eventdownloads/bfwgconference2013acceptedpapers/Hameed---Time-Varying-Momentum.pdf)
- **[RULE] Shared risk rules** (secondary sources, compiled above):

  | Trader | Risk per trade | Stop | Other |
  |---|---|---|---|
  | Minervini | 1.25–2.5% | max 10%, average loss 5–6% | progressive exposure |
  | O'Neil (as adopted by Minervini) | — | 7–8% hard stop | — |
  | Qullamaggie | 0.3–0.5% | about 1 ADR | — |

  Sources: [X/AmeetRai](https://x.com/AmeetRai/status/1864744561668423792); [quantstrategy.io](https://quantstrategy.io/blog/sepa-strategy-explained-mastering-trend-following-with-mark/); [X/KrishanKapoor27](https://x.com/KrishanKapoor27/status/1922685621329383467)
- **[CLAIM] Payoff profile:** Qullamaggie's reported win rate is 25–35%, implying the edge is concentrated in a few large winners. — [Deep Dive](https://app.qullamaggiedeepdive.com/stats)
- **[VERIFIED] Contest results swing widely year to year:**
  - 2022 USIC stock-division winner: only +13.5% (Sam Bhatia). — [BusinessWire 2022 standings](https://www.businesswire.com/news/home/20230125005300/en/United-States-Investing-Championship-2022-Final-Standings)
  - 2023 winner: +805% (Goverdhan Gajjala).
  - 2024 $1M+ winner: +353.9% (Law Wai-Sum). This comes from a single aggregator page that I did not check against the organizer.
  - 2025 winners: Martin Luk +969.8%, Tito Adhikary +2,115.1%.

  Sources: [trading-tournaments USIC](https://trading-tournaments.com/tournaments/championships/usic); [trading-tournaments hall of fame](https://trading-tournaments.com/hall-of-fame)

### Inferences
- **Survivorship bias.** USIC publishes only the top of each division. Many entrants trading high-variance, concentrated momentum books will produce a few +300–2,000% years by chance plus skill, and the losers are not publicized. The 2022 winner's +13.5% shows that in a bad tape even the best momentum book roughly breaks even. Celebrity traders (Minervini, Qullamaggie, Zanger, Darvas) are selected precisely *because* they had outlier runs.
- **What the academic record does and doesn't support.** It supports the selection component (near the 52-week high, high RS, uptrend), conditional on a favorable market state. It does not separately test the trading component (base pattern + tight stop + partial sell + trail + pyramiding). That component is where these traders say their edge lies, and it is exactly what the user's Kova test did not include.
- **Profile to expect from a "tight stop + trail" momentum system:** 25–45% winners, average loss about 1R, and a few 3–10R+ winners. The edge depends on how many large winners occur, and those cluster in trending regimes.

### Gaps
- I found no independent, published study measuring the incremental value of the exit/sizing layer (partial sells, MA trail, pyramiding) over the plain selection screen. The user would have to backtest this personally.
- I found no verified Minervini win-rate or payoff-ratio statistics. The commonly quoted "about 50% batting average, average gain 2–3× average loss" is **not verified here**.

## 6. Why these methods struggle in range-bound / choppy markets, and how the traders say they handle it

### Takeaway
In sideways markets, breakouts fail more often; IBD-community anecdotes say about half of FTDs fail. Tight stops are hit repeatedly, and the few large winners that pay for the many small losses never arrive. Academically, momentum is weak after down-markets and crashes in high-volatility rebounds. Each trader's stated defense is a form of exposure control rather than a different signal:
- O'Neil's "M" rule (distribution days and FTDs).
- Minervini's progressive exposure (cut size after losses, add only after wins and pilot buys work).
- Qullamaggie's avoidance of downtrends, with small 0.3–0.5% risk.

### Cited Findings
- Momentum profits are concentrated after up-markets and weak after down-markets. — [Cooper, Gutierrez & Hameed](https://www.researchgate.net/publication/4769366_Market_States_and_Momentum)
- Momentum crashes cluster in post-decline, high-volatility rebound states. — [Daniel & Moskowitz, NBER](https://www.nber.org/system/files/working_papers/w20439/w20439.pdf)
- O'Neil/IBD defines exposure changes by counting distribution days (an index down ≥0.2% on higher volume) and confirms new uptrends with an FTD. Practitioners report about half of FTDs fail. — [TradingView FTD marker](https://www.tradingview.com/script/mrsKTQdQ-Distribution-Follow-Through-Day-Marker); [Motley Fool board](https://discussion.fool.com/t/ibd-market-school/112218?page=6)
- Minervini's "progressive exposure": trade smaller when results are poor, scale up only as trades work, and start with pilot buys. — [X/AmeetRai](https://x.com/AmeetRai/status/1864744561668423792); [X/IManghaila](https://x.com/IManghaila/status/2050391132660457786)
- Qullamaggie reportedly trades breakouts in uptrending or sideways markets and avoids downtrends. He skips setups whose stop would be wider than 1 ADR, which keeps the cost of failed breakouts small. — [qullamaggie.com](https://qullamaggie.com/my-3-timeless-setups-that-have-made-me-tens-of-millions/); [tradingresourcehub](https://tradingresourcehub.substack.com/p/interview-qullamaggie-chat-with-traders-part1)
- Even top momentum traders produce near-flat results in hostile tapes. The 2022 USIC stock-division winner made +13.5%, and Qullamaggie had a 2022 drawdown reported at $25–60M. — [BusinessWire 2022](https://www.businesswire.com/news/home/20230125005300/en/United-States-Investing-Championship-2022-Final-Standings); [Deep Dive](https://app.qullamaggiedeepdive.com/stats)

### Inferences
These connect the evidence above to the user's own tests.

- **Breakouts and mean reversion complement each other by regime.** The user's two results line up with the literature:
  - Breakout/momentum did worst right after sharp run-ups and in ranges, and best in sector uptrends.
  - Bollinger mean reversion (above the 200-day, below the lower band) helped in the sideways market.
  - A natural blend is a regime switch. Use a momentum/breakout sleeve only when the index or sector is in a confirmed uptrend: QQQ or SMH above a rising 50-day, few recent distribution days, or a fresh FTD. Use the mean-reversion sleeve when the index is above its 200-day but range-bound. Hold cash or reduce size when the index is below its 200-day.
  - This is an inference for the user to backtest, not a published result.
- **What to borrow is the trading layer, not another screen.** Kova/RS ≥ 90 already captures the selection. Candidates:
  - A tight stop (about 1 ADR, or 7–8% max).
  - Partial profit after 3–5 days with the stop moved to breakeven.
  - A 10/20-day MA trailing exit.
  - Fixed 0.5–1% account risk.
  - Progressive exposure: halve size after N consecutive stop-outs, restore after wins.
- **Avoid the "right after a sharp run-up" failure.** Consistent with Daniel & Moskowitz's crash states and Qullamaggie's emphasis on entering from a tight consolidation, require a base or contraction, e.g. a declining N-day range or ATR. Do not buy extended stocks just because they pass the trend filter.
- **Capital-size caveat.** With $8,000 and 0.5–1% risk ($40–$80 per trade), results will hinge on a few trades per year. Statistical confidence on any blended rule will be low, so keep rules few and pre-specified to limit overfitting.

### Gaps
- I found no independent backtest comparing breakout systems with and without an IBD-style M filter or a progressive-exposure rule in sideways regimes (e.g., 2015–2016, 2022, 2025).
- Primary-text quotes on how each trader handles chop could not be retrieved because fetching was blocked. Examples: Minervini's "trade only when the market lets you" passages, and O'Neil's "3 out of 4 stocks follow the market".
