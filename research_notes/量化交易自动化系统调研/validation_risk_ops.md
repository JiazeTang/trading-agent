# 策略验证、实盘孵化与自动化交易的运营风控（面向个人散户系统的可落地做法）

> 调研日期：2026-10-20。
> **来源可达性说明（写报告的人请注意）**：本环境的网络策略拦截了 sec.gov、papers.ssrn.com、davidhbailey.com、docs.alpaca.markets、qoppac.blogspot.com、nautilustrader.io、wikipedia、arxiv 等站点的直接抓取。因此：
> - NautilusTrader 的内容是从其 GitHub 仓库 `nautechsystems/nautilus_trader`（develop 分支 `docs/concepts/`）直接下载原文后阅读的，属一手资料。
> - Knight Capital、Deflated Sharpe、PBO、Alpaca 文档、Perold、MOC 截止时间等，是通过搜索引擎的摘要读到的，引文链接指向原始页面，但我没能逐字核对原文。凡标 **[未逐字核对]** 的，正式引用前应回原文确认。
> - Robert Carver（qoppac 博客）、Ernest Chan 的原文没能检索到；与他们有关的说法若出现，均放在 Gaps 或明确标为"我的背景知识，未核实"。

---

## 1. 专业验证流程里，哪些方法对"单策略、日线、散户"系统实际可用？

### Takeaway
最值得做的是：(1) 把所有试过的变体都记账，用 Deflated Sharpe / 最小样本长度（MinTRL）对"挑出来的那一个"打折；(2) 参数稳健性曲面加交易级 Monte Carlo（重抽样）看回撤分布；(3) 一次性留出样本。CPCV 和 PBO 主要是为"大量候选策略或 ML 模型"设计的，对只有一两个预注册规则的系统收益有限，但可以拿来跑"参数网格"的 PBO。

### Cited Findings
- **Deflated Sharpe Ratio（DSR）**：Bailey & López de Prado (2014, *Journal of Portfolio Management*) 提出，用于同时校正多重检验带来的选择偏差和收益的非正态 — [SSRN 2460551](https://papers.ssrn.com/abstract=2460551) [未逐字核对，只读到摘要]
- DSR 的门槛 SR* 是"N 次纯运气试验里预期能拿到的最大 Sharpe"：SR* = √V × [(1−γ)·Φ⁻¹(1−1/N) + γ·Φ⁻¹(1−1/(N·e))]。V 是各次试验 Sharpe 的方差，γ 是 Euler–Mascheroni 常数（≈0.5772）。DSR 就是以 SR* 为基准的 Probabilistic Sharpe Ratio — [LuxAlgo 概念页](https://www.luxalgo.com/library/concept/deflated-sharpe-ratio.md)（二手资料）；[Wikipedia: Deflated Sharpe ratio](https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio)
- DSR 是否可信，关键在于 N（试验次数）有没有如实统计，而研究者常常少报 N。试验之间相关时，需要用聚类或特征值方法估计"有效 N" — [LuxAlgo](https://www.luxalgo.com/library/concept/deflated-sharpe-ratio.md)；[Wikipedia](https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio)
- **Minimum Track Record Length（MinTRL）**：在给定置信度下，要让观察到的 Sharpe 与某个门槛在统计上可区分，所需的样本长度。有资料给出的形式是 MinTRL = 1 + [1 − γ₃·SR + ((γ₄−1)/4)·SR²]·(Φ⁻¹(1−α)/SR)²，其中 γ₃ 为偏度、γ₄ 为峰度，α 通常取 0.05 — [Journal of Risk 摘要（Bailey & López de Prado, "The Sharpe Ratio Efficient Frontier"）](https://risk.net/node/2223785)；公式引自 [arXiv 2608.23808](https://arxiv.org/pdf/2608.23808)（二手转述）
- 负偏度加正超额峰度会拉长所需的样本长度；按典型对冲基金的收益分布，MinTRL 很容易超过几年的月度数据 — [Trading Strategy glossary](https://tradingstrategy.ai/glossary/probabilistic-sharpe-ratio)；[IDEAS/RePEc](https://ideas.repec.org/a/rsk/journ4/2223785.html)
- 经验法则：t 统计量 ≈ Sharpe × √年数。所以 Sharpe 为 1 的策略要大约 4 年数据才能让 t 达到 2，而一年 Sharpe 为 1 在统计上与 0 无法区分 — [Tradermath](https://www.tradermath.org/courses/basics-of-quantitative-finance/sharpe-ratio-and-risk-adjusted-metrics)
- **Haircut Sharpe**：业内常把回测 Sharpe 打五折，Harvey & Liu 称之为"rule of thumb"，并提出按多重检验做解析折扣。被检验的策略越多、彼此越相关，折扣越大；Sharpe 高的策略折扣比例反而比边际策略小 — [Harvey & Liu, "Backtesting" (Duke PDF)](https://people.duke.edu/~charvey/Research/Published_Papers/P120_Backtesting.PDF)；[CFA Institute digest](https://rpc.cfainstitute.org/research/cfa-digest/2016/03/backtesting-digest-summary)
- **PBO / CSCV**：Bailey、Borwein、López de Prado、Zhu 提出用组合对称交叉验证（CSCV）估计"回测过拟合概率"（PBO）。做法是把 T×N（时间 × 试验配置）的收益矩阵切成 S 块，枚举所有"一半做样本内、一半做样本外"的组合，看样本内最优的配置在样本外排名的 logit 分布。PBO 就是样本内最优者在样本外跌到中位数以下的比例 — [davidhbailey.com 论文 PDF](https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf) [抓取被拦截，方法描述来自我的背景知识，未逐字核对；写报告时只能写成"据该论文"并提示核对]
- **Walk-forward 与 CPCV**：walk-forward 只有一条历史路径，结果依赖于这条路径，估计方差大。CPCV 在许多训练/测试块组合上做 purging 和 embargo，得到多条回测路径，也就是绩效的分布而不是单个数。例如 6 折、每次取 2 块做测试，共 15 种组合 — [Wikipedia: Purged cross-validation](https://en.wikipedia.org/wiki/Purged_cross-validation)；[LuxAlgo](https://www.luxalgo.com/library/concept/purged-cross-validation.md)
- Purging 指删掉标签窗口与测试集重叠的训练样本；embargo 是在每个测试块之后再留一段缓冲。有一条实践经验是 embargo 取测试集 bar 数的约 1%，但这只是经验值 — [tradinginterview.com](https://www.tradinginterview.com/courses/machine-learning/lessons/cross-validation-for-financial-data-purging-and-embargoing/)
- 有从业者评论：对短期研究，CPCV 是"overkill"，但对生产模型它是标杆。CPCV 各路径之间互相重叠、并不独立，这一点我没在一手资料里核实 — [Return on Effort (beehiiv)](https://returnoneffort.beehiiv.com/p/mitigating-overfitting-advanced-crossvalidation)
- Kevin Davey 的流程是：walk-forward、Monte Carlo、再到 incubation（实时纸面交易）。Monte Carlo 的结果用来给实盘"统计上合理的区间" — [AlgoAdvantage 访谈 #036](https://algoadvantage.substack.com/p/036-kevin-davey-part-i-its-all-about-process-in-algo-trading)；[IBKR Campus 转载](https://www.interactivebrokers.com/campus/ibkr-quant-news/algo-advantage-036-kevin-davey-part-i-its-all-about-process-in-algo-trading/)
- 用随机组合（random portfolios）检验"策略是否优于随机"，也可以用在实盘监控上 — [Burns Statistics](https://www.burns-stat.com/documents/random-portfolios-for-evaluating-trading-strategies/)

### Inferences
- 针对本项目，各方法的性价比排序如下（我的判断）：
  1. **试验台账加 DSR**（高价值、低成本）：把 `src/riskeval/` 里所有跑过的规则变体（不同 z 阈值、均线长度、止损幅度、股票池）都记成 N。用这些变体的 Sharpe 方差 V 算 SR*，再报 DSR。因为规则是事先定死的，N 可能不大，但"16 只、SMH、QQQ、不同风格对比"也都算试验。
  2. **参数稳健性曲面**（高价值）：z ∈ {−1.5, −1.75, −2, −2.25, −2.5}、出场均线 ∈ {10, 20, 30}、止损 ∈ {10%, 15%, 20%, 无}，画热力图。如果只有 (−2, 20, 20%) 这一个孤立高点，而周围都差，就是过拟合信号。这个网格也可以直接用来跑 PBO/CSCV，因为 PBO 的输入正好就是"多配置 × 时间"的收益矩阵。
  3. **交易级 bootstrap / Monte Carlo**（高价值）：对约 10 年的交易做有放回重抽样或打乱顺序，得到最大回撤、连续亏损次数、年化收益的分布。第 2 节的 kill 标准要从这里取数。
  4. **相对随机入场的检验**（已在做）：用"同样持仓天数、同样频率的随机入场"作零分布。这和 Burns 的随机组合思路一致。
  5. **Walk-forward**：规则没有被拟合的参数，所以 walk-forward 的意义主要是"分年份看稳定性"，即按年拆收益，看是否集中在少数年份。
  6. **CPCV**：对没有拟合参数的预注册规则，CPCV 基本退化为分块重抽样，可以不做。
- 约 10 年日线，加上"相对随机入场优势很薄"，按 t ≈ SR·√年 推算：假设超额 Sharpe 为 0.3，10 年的 t ≈ 0.95，远低于 2。所以只靠回测无法证明这个优势存在，这一点应写进报告。
- 幸存者偏差（按今天市值挑的 16 只）无法靠统计方法修正，只能用 ETF（SMH）版本的结果作为主证据，或在 GitHub Actions 里构建按历史时点成分的股票池（需要历史成分数据，可能拿不到）。

### Gaps
- 没能读到 Bailey & López de Prado DSR、PBO 原文（域名被拦截），公式取自二手来源；PBO 的阈值解读（例如 PBO > 0.5 意味着什么）未核实。
- 没找到专门针对"单一预注册规则、交易笔数少"场景的 CPCV 评估文献。
- 没检索到 Ernest Chan 关于样本外检验的原文。

---

## 2. 纸面交易 / 孵化：要多久、多少笔？如何统计地比较实盘与回测？何时停掉策略？

### Takeaway
从业者常见的孵化期是 6–9 个月的实时纸面交易（Kevin Davey），但对日线、低频的均值回归规则，"多少个月"不如"多少笔交易"重要，而且几个月的数据在统计上几乎证明不了优势。所以孵化期的目标应设为**验证执行一致性**（信号、成交、成本是否与回测吻合），不是证明盈利；kill 标准要事先写死，并以 Monte Carlo 给出的回撤和连亏分布为界。

### Cited Findings
- Davey 的 incubation：通常做 **6–9 个月**实时纸面交易，确认实时表现与回测预测一致；被称为他"最终的稳健性检验" — [AlgoAdvantage #036](https://algoadvantage.substack.com/p/036-kevin-davey-part-i-its-all-about-process-in-algo-trading)（二手访谈摘要，非 Davey 本人书面规则）
- Davey 的 Strategy Factory 学员在论坛上描述的孵化期是 6 个月；有学员称完成孵化的 6 个策略中 3 个失败，而且失败时的回撤并没有接近历史最大回撤 — [NexusFi](https://nexusfi.com/vendors-product-reviews/37240-kj-trading-systems-strategy-factory-2.html)（论坛轶事）
- 对 Davey《Building Winning Algorithmic Trading Systems》的书评摘要：上线是分阶段的，先纸面或小资金，比较预期成交与实际成交，再随信心逐步加仓；要持续监控实盘是否落在回测和 Monte Carlo 给出的统计合理区间内，并事先定好干预规则，而不是对短期亏损情绪化反应 — [financialwisdomtv 摘要](https://www.financialwisdomtv.com/post/building-winning-algorithmic-trading-systems-kevin-davey-s-complete-framework-for-trading-success)（二手）
- Carver 在一次英国技术分析师协会（STA）活动上说，应该给实盘表现更多权重，而非回测 — [STA blog](https://technicalanalysts.com/sta-blog/tom-hicks-and-robert-carvers-fireside-chat-in-june-and-no-fireplace)（会议纪要，二手）
- Probabilistic Sharpe / MinTRL 可以用来回答"要多长的记录才能以给定置信度拒绝 Sharpe 低于门槛" — [Journal of Risk](https://risk.net/node/2223785)
- t ≈ SR·√年：Sharpe 为 1 的策略需要约 4 年才能达到 t=2 — [Tradermath](https://www.tradermath.org/courses/basics-of-quantitative-finance/sharpe-ratio-and-risk-adjusted-metrics)
- Advisor Perspectives 有一份题为 "What to do when a strategy performs poorly"（2020 年 1 月）的演示稿，讨论策略表现差时如何决策 — [PDF](https://api.advisorperspectives.com/pdfs/2020/Slides/Presentation-What-to-do-when-a-strategy-performs-poorly-January-2020.pdf)（只看到标题，未读内容）

### Inferences
- **孵化期建议**（推断，给报告作者参考）：
  - 阶段 0，"影子模式"：GitHub Actions 每日操作单照常生成，用户不下单，系统记录"如果按收盘价成交"的虚拟结果。已经在做，可以把它正式定义为孵化日志。
  - 阶段 1，券商纸面账户（如 Alpaca paper）自动下单：目标至少 3 个月，**并且**加码仓至少有 N_min 笔完整的进出场。N_min 可以按回测的年均交易次数推算，例如约 20 笔。条件是"两者都满足"，因为日线均值回归一年可能只有十几次信号。
  - 阶段 2，小额实盘：例如加码仓只用 1 个仓位或 1/4 资金，同样有时间和笔数的门槛。
- **比较方法（可直接实现）**：
  1. **信号一致性**：每天把实盘/纸面的信号列表与回测引擎在同一天、同一数据上重算的信号逐笔比对，不一致率应为 0。不为 0 说明数据或时序有 bug。这一项最快出结果，也最有用。
  2. **成交偏差**：每笔记录"回测假设价格"（信号日下一交易日收盘价）与实际成交价之差，单位为 bp，累积均值和标准差。这就是第 3 节的 implementation shortfall。
  3. **收益落在分布内**：用第 1 节交易级 bootstrap 生成"孵化期同样笔数下"的累计收益和最大回撤分布，看实盘位于哪个分位。低于第 5 百分位就触发复查。
  4. **CUSUM / 序贯检验**（经典统计质控方法，我的背景知识，未在本次检索中找到交易领域的一手出处）：对每笔交易 R 值减去回测期望 R 做累计和，越过事先设定的下界就报警。好处是自然适应笔数少的场景。
  5. **Bayesian 更新**（同为背景知识，未找到交易一手出处）：以回测的每笔期望收益为先验，但按 Harvey–Liu 的思路先打折，再用实盘交易更新；后验"期望 ≤ 0"的概率超过事先定的阈值就停。
- **kill 标准示例（应事先写入规则文件）**：
  - 硬性：加码仓自高点回撤超过 Monte Carlo 第 95 百分位最大回撤（或超过回测最大回撤的 1.5 倍），立即停止新开仓、复查。
  - 硬性：连续亏损笔数超过 bootstrap 第 99 百分位。
  - 软性：滚动 20 笔的平均 R 低于 bootstrap 第 5 百分位，降为半仓。
  - 执行性：信号不一致或对账不一致，当天暂停（见第 4 节）。
  - 不因"某一个月亏钱"就停；也不因"某几个月赚钱"就加大仓位，加仓同样要满足事先定的笔数门槛。

### Gaps
- 没找到 Carver 关于"实盘多久才能判断策略失效"的原文（qoppac 被拦截、搜索未命中）。我的背景知识是他写过用统计检验比较实盘与回测 Sharpe，但未核实，不应引用。
- 没找到 Ernest Chan 关于纸面交易时长的原文。
- 没有权威来源给出"最少交易笔数"的标准数字；常见说法（如 30 笔、100 笔）均无一手出处，未收录。
- Alpaca 学习中心有一篇 "Paper Trading vs. Live Trading: A Data-Backed Guide on When to Start Trading Real Money"（[链接](https://alpaca.markets/learn/paper-trading-vs-live-trading-a-data-backed-guide-on-when-to-start-trading-real-money)），没能读到正文。

---

## 3. 回测与实盘的差距：来源，以及如何度量 implementation shortfall

### Takeaway
对本策略（"信号日下一交易日收盘买入，回到均线收盘卖出"）来说，最大的差距来源是：收盘价能否真正成交（MOC 截止时间与信号时序）、纸面账户本身不模拟的成本（滑点、冲击、分红、费用）、以及数据或公司行动。用 Perold 的 implementation shortfall（以决策价为基准的纸面组合与实际组合之差）逐笔记账，就能把"信号收益"和"执行损耗"分开。

### Cited Findings
- **NYSE MOC 截止**：MOC 单可在 **15:50** 前提交；此后到 16:00 只能提交与监管失衡方向相反的单，撤单只限正当错误 — [NYSE Closing Auction Fact Sheet](https://www.nyse.com/publicdocs/nyse/NYSE_Auctions_Closing_Process_Fact_Sheet.pdf) [未逐字核对]。15:50 截止取代了此前的 15:45，见 SEC 批准 Rule 123C 修改的文件 — [Federal Register 2019-01175](https://public-inspection.federalregister.gov/2019-01175.pdf)
- **Nasdaq MOC 截止**：15:55 — [SEC filing 34-100129 (2024)](https://www.sec.gov/files/rules/sro/cboebzx/2024/34-100129.pdf) [二手摘要，未逐字核对]
- QuantConnect 论坛报告：该平台会拒绝在收盘前 16 分钟之外提交的 MOC 单，比交易所实际允许的时间更早 — [QuantConnect forum](https://www.quantconnect.com/forum/discussion/11140/can-marketoncloseorder-be-adjusted-to-allow-submission-closer-to-actual-exchange-moc-cutoff-times/)
- **Alpaca 纸面交易不模拟**：自身订单的市场冲击、信息泄露、延迟导致的滑点、非可成交限价单的队列位置、价格改善、监管费用、**分红**。Alpaca 称纸面交易是"good approximation"，但不能替代实盘，表现可能不同 — [Alpaca Docs: Paper Trading](https://docs.alpaca.markets/docs/paper-trading) [未逐字核对]
- Alpaca 员工在论坛说：纸面环境用实时报价，市价买单按 ask 成交、卖单按 bid；可成交订单有约 10% 的概率随机部分成交 — [Alpaca forum](https://forum.alpaca.markets/t/slippage-paper-trading-vs-real-trading/2801)
- 只开纸面账户的用户只能使用 IEX 行情 — [Alpaca Docs: Paper Trading](https://docs.alpaca.markets/us/docs/paper-trading)
- 第三方称 Alpaca 纸面交易不按 NBBO 数量检查订单大小，未经 Alpaca 文档证实 — [TradersPost blog](https://blog.traderspost.io/article/alpaca-paper-trading)
- NautilusTrader 文档列出实盘相对回测新增的差异：venue 规则、网络传输导致命令结果未知、多输入交错的时序、持久化与传输不同步、外部订单活动、需要对账 — [nautilus_trader docs/concepts/live.md (GitHub)](https://github.com/nautechsystems/nautilus_trader/blob/develop/docs/concepts/live.md)
- 回测衰减的常见原因：偷看了当时尚未公开的信息、是众多尝试中挑出的最好者、成本假设低于真实。这些叠加可以让回测 Sharpe 4 变成实盘 0–1 — [techinterview.org](https://www.techinterview.org/post/3233477314/why-backtest-sharpe-collapses-live/)（非正式来源）
- **Implementation shortfall（Perold 1988）**：比较"纸面组合"与实际交易组合的收益。纸面组合假设在决策时按当时价格瞬间建仓；成本包括延迟成本和未完成交易的机会成本 — [Quantitative Brokers: A Brief History of IS](https://quantitativebrokers.com/blog/a-brief-history-of-implementation-shortfall)；[NYU Stern 课件 (Hasbrouck)](https://pages.stern.nyu.edu/~jhasbrou/Teaching/POST%202015%20Fall/classNotes/STPPTradingCosts.pdf)（二手）
- 未指定决策价时，一般用中间价作默认基准；实践中 IS 通常逐单计算，而不是在组合层面计算 — [Ryan O'Connell Finance](https://ryanoconnellfinance.com/implementation-shortfall/)（二手）

### Inferences
- **本策略的具体差距清单**（推断）：
  1. **信号时序**：规则是"收盘跌破下轨，下一个交易日收盘买入"，信号用的是 T 日收盘价，T+1 日收盘执行，所以有一整天的时间提交 MOC 单。这比"当日收盘信号、当日收盘成交"安全得多，后者必须在 15:50 前用盘中价估算信号。**卖出规则"收盘回到 20 日均线卖出"**如果是当日收盘判断、当日收盘成交，就存在这个问题；如果是 T+1 收盘成交，也要与回测假设一致。报告应核对回测代码的时序假设。
  2. **止损 −20%**：回测若用收盘价判断止损，实盘就不应挂盘中止损单，否则两者不一致。
  3. **收盘价与 MOC 成交价**：官方收盘价就是收盘集合竞价价，MOC 成交价通常等于它，但 Alpaca 纸面账户是否模拟收盘竞价未核实，需在孵化期实测"纸面成交价减官方收盘价"。
  4. **分红**：Alpaca 纸面交易不计分红，而 SMH、REGN、VRTX 的长期持有部分（REGN 近年开始派息，未核实）会因此偏离回测（若回测用调整后价格）。比较时应统一用总收益或统一用价格收益。
  5. **公司行动与数据修订**：Yahoo 调整价会随新分红或拆股回溯改变历史，同一规则在不同日期重跑可能给出不同的历史信号。应保存每日运行时的数据快照哈希（见第 5 节）。
  6. **零碎股或整数股**：8000 本金下，1600 加码仓分 2 个仓位，每仓约 800。如果券商不支持零碎股的 MOC，整股取整会带来仓位偏差，也就是机会成本的一部分。
- **最简 IS 记账**：每笔记录决策价 P_d（信号日收盘价，或回测假设的成交价）、实际成交价 P_f、成交数量 q、计划数量 q*。成交差异为 (P_f − P_d)·q·方向，机会成本为 (P_close_later − P_d)·(q* − q)·方向，另加费用。月度汇总成"回测收益 = 实盘收益 + 执行损耗 + 成本 + 未成交机会成本"。

### Gaps
- 未找到 Alpaca 是否支持零碎股 MOC、纸面账户如何模拟收盘集合竞价的官方说明。
- 未找到 Interactive Brokers 纸面账户局限的官方文档（interactivebrokers.com 被代理拦截）。
- Perold 1988 原文未读到，定义来自二手资料。

---

## 4. 自动化交易的运营风控：事前检查、日亏损限额、kill switch、对账、心跳；Knight Capital 教训的个人版

### Takeaway
Knight Capital 的 4.6 亿美元损失，核心是部署不一致（旧代码在一台服务器上被重新激活）、预警邮件没人看、缺少按资本设限的自动拦截。个人 bot 可以用约 10 条硬规则覆盖同类风险：事前检查（金额、数量、仓位、价格带、白名单）、幂等订单 ID、每日"只跑一次"锁、启动时和下单前对账、出错即停（fail closed）、一键停止开关、失败即通知。

### Cited Findings
- **Knight Capital（2012-08-01 事件；SEC 于 2013-10-16 发出命令）**：开盘后前 45 分钟，一个运行已废弃代码的路由器为了处理 212 笔小额零售订单，发出了 400 多万笔订单，成交超过 3.97 亿股，形成数十亿美元的非意图头寸，交易亏损超过 4.6 亿美元；Knight 支付 1200 万美元和解，这是 SEC 依据 Rule 15c3-5（Market Access Rule，2010 年通过）采取的第一起执法行动 — [SEC Press Release 2013-222](https://www.sec.gov/news/press-release/2013-222)；[WilmerHale client alert](https://www.wilmerhale.com/en/insights/client-alerts/knight-capital-settles-rule-15c3-5-violations-with-sec-agrees-to-pay-12-million)；[Mondaq](https://www.mondaq.com/unitedstates/credit-control-and-cashflow/270572/knight-capital-settles-rule-15c3-5-violations-with-sec-agrees-to-pay-%2412-million)
- 开盘前系统自动发出了 **97 封**提示错误的邮件，但它们不是按系统告警设计的，一般没人看，所以没人采取行动 — [WilmerHale](https://www.wilmerhale.com/en/insights/client-alerts/knight-capital-settles-rule-15c3-5-violations-with-sec-agrees-to-pay-12-million)（命令原文摘要）
- SEC 认定 Knight 没有足够的保障措施来限制其市场接入带来的风险，也没有对控制措施的有效性做足够的复查 — [Mondaq](https://www.mondaq.com/unitedstates/credit-control-and-cashflow/270572/knight-capital-settles-rule-15c3-5-violations-with-sec-agrees-to-pay-%2412-million)；SEC 命令全文 — [Justia 存档](https://contracts.justia.com/companies/kcg-holdings-inc-18985/contract/555902)
- （背景细节，我的背景知识，未在本次检索中核实：新代码部署到 8 台服务器时漏了 1 台；新功能复用了旧 "Power Peg" 功能的标志位；旧代码的累计成交计数逻辑已被移走。写报告时如要引用，需回 SEC 命令原文核对。）
- **NautilusTrader RiskEngine**（一手，GitHub 文档）：位于下单和改单路径上，除非在 `RiskEngineConfig` 中设为 bypass，否则检查价格精度、正价、数量精度和上下限、GTD 是否已过期、`reduce_only` 单不得增加仓位、引擎级 `max_notional_per_order` 和品种的 min/max notional、现金账户余额影响、下单和改单频率限制，以及交易状态（`ACTIVE` / `REDUCING` / `HALTED`）。检查失败时生成 `OrderDenied` 事件，并带标准化原因码 — [nautilus_trader docs/concepts/execution/index.md](https://github.com/nautechsystems/nautilus_trader/blob/develop/docs/concepts/execution/index.md)
- NautilusTrader 交易状态：`HALTED` 只允许撤单和查询，不允许新下单和改单；`REDUCING` 只允许符合条件的减仓单。文档警告，开启 bypass 时交易状态不会被强制执行 — [同上](https://github.com/nautechsystems/nautilus_trader/blob/develop/docs/concepts/execution/index.md)
- **NautilusTrader 对账**：实盘会把本地状态与 venue 回报对齐。启动时，"明确的仓位回报是权威的；引擎要么在容差内对齐，要么 fail closed"；**缺失的回报、空数量、或 venue 不发布仓位，都不能作为"空仓"的证据** — [nautilus_trader docs/concepts/execution/reconciliation.md](https://github.com/nautechsystems/nautilus_trader/blob/develop/docs/concepts/execution/reconciliation.md)
- NautilusTrader：网络故障可能使订单命令的结果"未知"；对账在启动阶段和运行期都会检查；对账失败会中止启动；错误日志即使被过滤也仍会触发关停请求 — [nautilus_trader docs/concepts/live.md](https://github.com/nautechsystems/nautilus_trader/blob/develop/docs/concepts/live.md)
- NautilusTrader 心跳：WebSocket 或 TCP 客户端在心跳超时后重连，默认超时为 3 个心跳间隔 — [同上](https://github.com/nautechsystems/nautilus_trader/blob/develop/docs/concepts/live.md)
- **Alpaca `client_order_id`**：可用于在客户端程序中组织和跟踪订单，可为不同策略使用不同的前缀；SDK 提供 `get_order_by_client_id` 按客户端 ID 查询 — [Alpaca Docs: Working with /orders](https://docs.alpaca.markets/docs/working-with-orders) [未逐字核对]
- 第三方项目的做法：每个动作生成稳定的 client order ID，执行前持久化，超时后重试前先与券商状态对账，避免重复下单 — [lablab.ai 项目描述](https://lablab.ai/ai-hackathons/alpaca-ai-trading-agents-hackathon/life-manager/life-manager-autonomous-options-money-loop)（非官方）

### Inferences
- **Knight 教训的个人版映射**（推断）：
  | Knight 失败点 | 个人 bot 对应控制 |
  |---|---|
  | 部署不一致，旧代码复活 | 只从带 tag 的 git 提交运行；运行时记录 commit SHA 和规则版本；删除废弃代码，不用"开关标志"复用旧逻辑 |
  | 97 封预警邮件没人看 | 告警只发"需要行动"的事件（下单失败、对账不符、kill 触发），用手机推送；日常成功不发或汇总成一条，避免告警疲劳 |
  | 无按资本设限的自动拦截 | 事前硬限额，见下面清单 |
  | 45 分钟内 400 万笔 | 每日下单笔数上限，例如不超过 4 笔，超过即 `HALTED` |
  | 未复查控制有效性 | 每季度在纸面账户里故意触发每一条限额，确认会拦截（相当于"消防演习"） |
- **个人 bot 的最小控制清单**（参照 NautilusTrader RiskEngine 的检查项缩小而成）：
  1. 标的白名单 = `TARGETS` 加 SMH、REGN、VRTX；其他代码一律拒绝。
  2. 单笔金额不超过 min(计划仓位 × 1.1, 账户净值 × 15%)；单笔股数也设上限。
  3. 单标的持仓不超过计划值的 110%；加码仓同时持有不超过 2 个。
  4. 价格带：下单前参考价与上一收盘价偏离超过 ±15% 就拒绝（防坏数据，比如未调整的拆股）。
  5. 现金检查：买入金额不超过可用现金，不使用融资。
  6. 幂等：client_order_id = `{策略}-{规则版本}-{交易日}-{标的}-{买或卖}`，提交前先按该 ID 查询，已存在就不再提交；网络超时后先查再决定是否重试。
  7. 每日"一次性"锁：同一交易日的执行任务只能成功运行一次（GitHub Actions 的 `concurrency` 加上提交回仓库的执行记录文件）。
  8. 对账：下单前取券商持仓和挂单，与本地 `portfolio/holdings.csv` 比较。不一致时 fail closed（不下单）并告警；券商返回空或报错时**不能**当成空仓。
  9. 账户级熔断：单日账户净值跌幅超过 X%（例如 5%），或加码仓回撤触发第 2 节的 kill 标准，就进入 `REDUCING`（只允许卖出）或 `HALTED`。
  10. 手动 kill switch：仓库里放一个 `KILL` 文件或 GitHub 变量，存在时 bot 只撤单、不下单。
  11. 心跳：每个交易日收盘后必须产出一条运行记录；第二天早上没有就推送告警（"沉默"本身就是故障）。
  12. 纸面和实盘使用不同的 API key 和配置文件；默认指向纸面，切实盘需要显式开关。

### Gaps
- SEC 命令原文（34-70694）无法访问，未逐字核对 Power Peg、8 台服务器等细节。
- Alpaca 是否拒绝重复的 `client_order_id`、ID 保留多久，未从官方文档核实；建议在纸面账户里实测。
- 未获取 Interactive Brokers 的风控设置文档（如 precautionary settings），被代理拦截。
- 未获取 QuantConnect 风险管理模块文档原文。

---

## 5. 记录保存：交易日志字段、R 倍数、收益归因、代码与参数版本化

### Takeaway
每笔交易都应能追溯到"哪个规则版本、哪份数据、哪次运行"产生的信号，并能把盈亏拆成"信号（回测假设价格下的收益）、执行（相对决策价的偏差）、成本"三部分。R 倍数以开仓时事先定好的风险（本策略为 −20% 止损距离）为单位，可以跨笔比较，也是第 2 节 CUSUM 和 bootstrap 监控的输入。

### Cited Findings
- Implementation shortfall 的框架天然把"纸面组合收益"和"实际组合收益"分开，差额就是执行成本，包括延迟和未成交的机会成本 — [Quantitative Brokers](https://quantitativebrokers.com/blog/a-brief-history-of-implementation-shortfall)；[NYU Stern 课件](https://pages.stern.nyu.edu/~jhasbrou/Teaching/POST%202015%20Fall/classNotes/STPPTradingCosts.pdf)
- NautilusTrader 采用事件溯源（event-sourced）的内部状态，并与 venue 回报对账；`OrderDenied` 带标准化原因码 — [nautilus_trader execution docs](https://github.com/nautechsystems/nautilus_trader/blob/develop/docs/concepts/execution/reconciliation.md)
- DSR 和 haircut 的可信度依赖完整记录试验次数 N — [LuxAlgo](https://www.luxalgo.com/library/concept/deflated-sharpe-ratio.md)；[Harvey & Liu](https://people.duke.edu/~charvey/Research/Published_Papers/P120_Backtesting.PDF)
- Davey 强调比较预期成交与实际成交 — [financialwisdomtv 摘要](https://www.financialwisdomtv.com/post/building-winning-algorithmic-trading-systems-kevin-davey-s-complete-framework-for-trading-success)

### Inferences
- **建议的交易日志字段**（每笔一行，CSV 或 parquet，提交到 `reports/` 或 `portfolio/`）：
  - 追溯类：`trade_id`、`client_order_id`、`rule_id`（例如 `MR-A`）、`rule_version`（语义化版本号，对应 git tag）、`code_sha`、`params_hash`（z 阈值、均线、止损的 JSON 哈希）、`data_snapshot_hash`（当日价格数据的哈希）、`run_id`（GitHub Actions run 编号）、`mode`（shadow / paper / live）。
  - 信号类：`signal_date`、`symbol`、`z_score`、`rank`、`ma200_ok`、`decision_price`（信号收盘价）、`backtest_assumed_fill`（回测假设的 T+1 收盘价）。
  - 执行类：`order_type`（MOC 等）、`submit_ts`、`fill_ts`、`fill_price`、`qty_planned`、`qty_filled`、`fees`。
  - 风险类：`stop_price`（开仓价 × 0.8）、`R_unit`（= 开仓价 × 0.2 × 股数）。
  - 结果类：`exit_date`、`exit_reason`（均线回归、止损、手动、kill）、`exit_price`、`pnl`、`R_multiple`（= pnl / R_unit）、`holding_days`、`MAE`、`MFE`（持有期最大不利和最大有利波动）。
  - 归因类：`pnl_signal`（按回测假设价格算的盈亏）、`pnl_execution`（实际成交相对假设价格的差）、`pnl_costs`、`pnl_missed`（未成交或取整的机会成本），四项相加等于实际盈亏。
  - 主观类：`override`（是否人工干预及理由）、`notes`。
- **版本化做法**：
  - 规则文件（例如 `rules/mr_a.yaml`）与代码一起做 git tag，例如 `mr-a-v1.0.0`；任何参数改动都要升版本，并在 `docs/归档/` 决策记录里写明原因和"改之前是否已看过留出数据"。
  - **试验台账**（`research_log.csv`）：每次回测都记录日期、假设、参数、数据范围、结果 Sharpe、是否用了留出数据。这同时就是 DSR 所需的 N 和 V 的来源。
  - 留出数据"只用一次"的规则可以写成代码断言：留出期的结果文件一旦存在，再次运行就报错，除非升主版本号。
- **R 倍数的意义**：本策略止损很宽（−20%），而大多数出场是回归均线，所以 R 倍数会集中在 0 附近的小正值，止损时是 −1R。孵化期关注"平均 R"和"止损频率"是否落在回测分布内，比看金额更稳定。

### Gaps
- 没找到 Davey、Carver、Chan 关于交易日志字段的一手清单；上面的字段表是我综合推断的。
- 没找到权威的散户级收益归因标准；"信号、执行、成本"的拆法是 Perold 框架的简化。

---

## 6. 平台与知名从业者的相关指引汇总（QuantConnect、IB、Alpaca、NautilusTrader、Chan、Carver、Davey）

### Takeaway
能核实的一手平台资料中，NautilusTrader 的文档最完整地描述了"实盘不同于回测"的工程问题（命令结果未知、对账 fail closed、交易状态机）；Alpaca 明确列出纸面交易不模拟的因素；QuantConnect 社区可见 MOC 提交时间的平台限制；Davey 的"walk-forward、Monte Carlo、6–9 个月孵化"流程有二手资料佐证。Carver 和 Chan 的具体论述本次未能检索到原文。

### Cited Findings
- NautilusTrader：同一份策略代码可以在回测和实盘运行，但实盘引入 venue、传输、时序、持久化、外部活动、对账等回测无法复现的行为；文档开头明确警告实盘有真实风险，部署前要理解配置、节点运维、对账和回测与实盘的差异 — [live.md](https://github.com/nautechsystems/nautilus_trader/blob/develop/docs/concepts/live.md)
- Alpaca：纸面交易不模拟冲击、滑点、队列、价格改善、监管费、分红；只开纸面账户的用户只能用 IEX 数据 — [Alpaca Docs](https://docs.alpaca.markets/docs/paper-trading)
- QuantConnect：MOC 单需在收盘前约 16 分钟以上提交，早于交易所规定 — [QuantConnect forum](https://www.quantconnect.com/forum/discussion/11140/can-marketoncloseorder-be-adjusted-to-allow-submission-closer-to-actual-exchange-moc-cutoff-times/)
- Davey：流程依次为 walk-forward、Monte Carlo、6–9 个月实时纸面孵化，然后分阶段上线 — [AlgoAdvantage #036](https://algoadvantage.substack.com/p/036-kevin-davey-part-i-its-all-about-process-in-algo-trading)；第二部分谈策略选择 — [AlgoAdvantage #037](https://algoadvantage.substack.com/p/037-kevin-davey-ii-selecting-optimal)
- Carver：实盘表现应获得比回测更多的权重 — [STA blog](https://technicalanalysts.com/sta-blog/tom-hicks-and-robert-carvers-fireside-chat-in-june-and-no-fireplace)；他 2026 年 3 月在伦敦的研讨课涵盖统计显著性和"三种过拟合" — [WBS Training](https://www.wbstraining.com/?p=15809)（课程页面，未见内容细节）
- Man Group / Oxford-Man 关于回测的文章 — [man.com/insights/backtesting](https://www.man.com/insights/backtesting)（未读正文）
- CME 关于回测的教育材料 — [cmegroup.com backtesting PDF](https://www.cmegroup.com/content/dam/cmegroup/education/files/backtesting.pdf)（未读正文）

### Inferences
- 对个人系统来说，NautilusTrader 本身可能太重（Rust 和 Python 混合、事件驱动、多 venue），但它的**风控检查项和对账原则**可以直接照搬成几十行 Python。在 GitHub Actions 加 Alpaca 的架构里，自己实现上面第 4 节的清单更合适。
- 由于这些平台的纸面交易都不能完整模拟成本，孵化期应把"纸面盈亏"当作信号和流程的验证，执行成本的真实估计要等小额实盘阶段才能得到。

### Gaps
- Ernest Chan（《Quantitative Trading》《Algorithmic Trading》）关于纸面交易和实盘监控的论述未检索到。
- Carver《Systematic Trading》关于回测 Sharpe 预期折扣、何时放弃策略的原文未检索到；qoppac 被拦截。
- QuantConnect 官方文档的 Risk Management / Reality Modeling 章节、Interactive Brokers 的风控与纸面账户文档均未能访问。
- López de Prado《Advances in Financial Machine Learning》（2018）原书未读到，CPCV 的描述来自二手资料。
