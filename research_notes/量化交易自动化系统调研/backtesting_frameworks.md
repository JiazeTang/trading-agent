# 回测与算法交易框架调研（截至 2026-10-20）

调研方法说明（给报告撰写者）：
- 本环境中 WebFetch 无法解析外部域名，quantconnect.com、nautilustrader.io、lumiwealth.com 等官网经代理也被拦截（403），GitHub REST API 也被拦截（所以**拿不到 star 数和 GitHub 提交历史**）。
- 能直接核实的一手来源是 **PyPI JSON API**（版本号与上传日期）和 **raw.githubusercontent.com**（各项目 README、文档源文件、源代码）。下文标"PyPI 核实"或"源码核实"的，都是本人直接读到的。
- 只能通过 WebSearch 摘要得到的内容（QuantConnect 定价、QC 数据集说明、backtrader 维护状态的评论），都已注明为二手来源。
- 以下 PyPI 日期都按 UTC 上传时间记录。

## 1. 各框架维护状态、最新版本、许可证（2025–2026 活跃度）

### Takeaway
截至 2026-10，LEAN（及 LEAN CLI）、NautilusTrader、vectorbt（开源版）、bt、Lumibot、Freqtrade、Jesse 都在密集发版；backtesting.py 和 zipline-reloaded 只是低频维护；backtrader 自 2023-04 起再没有发版，实际上已停更。NautilusTrader 正处于 v1→v2 的大版本迁移期，zipline-reloaded 官方已建议新项目改用 ml4t-backtest。

### Cited Findings
**QuantConnect LEAN / LEAN CLI**
- LEAN CLI（PyPI 包名 `lean`）最新版 1.0.230，2026-10-15 发布；2025 年以来发了 17 个版本；PyPI 分类器标注许可证为 Apache — [PyPI lean](https://pypi.org/project/lean/#history)（PyPI 核实）
- `quantconnect-stubs`（跟随 LEAN 引擎构建发布的 Python 类型存根）最新版 18196，2026-10-19 发布；2025 年以来发了 721 个版本，说明引擎几乎每天都有构建 — [PyPI quantconnect-stubs](https://pypi.org/project/quantconnect-stubs/#history)（PyPI 核实）
- LEAN 自述为"event-driven, professional-caliber algorithmic trading platform"，模块化设计，"each component pluggable and customizable" — [LEAN README](https://github.com/QuantConnect/Lean/blob/master/readme.md)（源码核实）
- LEAN 引擎许可证为 Apache-2.0。此条未能直接打开 LICENSE 文件核实，依据是 Lumibot README 中第三方对比表里 Zipline 一栏同样写着 Apache-2.0，LEAN 本身没有出现在那张表中 → **本条未核实**，见 Gaps。

**NautilusTrader**
- PyPI 最新稳定版 1.231.0（2026-08-02）；v2 预发布版 2.0.0rc3–rc7 于 2026-08-21 至 2026-10-15 之间陆续发布；2025 年以来共 29 个版本；许可证 LGPL-3.0-or-later；1.231.0 要求 Python >=3.12,<3.15 — [PyPI nautilus_trader](https://pypi.org/project/nautilus_trader/#history)（PyPI 核实）
- README 原文："Python bindings are provided via PyO3 for the Rust-native v2 runtime. During the v2 transition, v1 receives only critical security backports on the `develop_v1` branch." develop 分支的平台表写的是 Python 3.13–3.14、Rust 1.99.0 — [NautilusTrader README](https://github.com/nautechsystems/nautilus_trader/blob/develop/README.md)（源码核实）
- 路线图原文："The open-source project focuses on single-node backtesting and live trading for individual and small-team quantitative traders. UI dashboards, distributed orchestration, and built-in AI/ML tooling are out of scope" — [NautilusTrader README / Roadmap](https://github.com/nautechsystems/nautilus_trader/blob/develop/README.md)

**backtrader**
- PyPI 最新版 1.9.78.123，2023-04-19 发布；上一版 1.9.77.123 是 2023-04-16；再往前是 2020-07；2025 年以来 0 个版本；许可证 GPLv3+ — [PyPI backtrader](https://pypi.org/project/backtrader/#history)（PyPI 核实）
- 社区分支 `backtrader2` 在 PyPI 上的最新版是 1.9.76.123，2020-07-30 发布，同样停滞 — [PyPI backtrader2](https://pypi.org/project/backtrader2/#history)（PyPI 核实）
- Snyk 把 backtrader 的维护状态评为"Inactive" — [Snyk Advisor](https://snyk.io/advisor/python/backtrader)；TradingStrategy.ai 称其"No longer maintained" — [TradingStrategy.ai glossary](https://tradingstrategy.ai/glossary/backtrader)（二手来源）
- README 至今还停留在 2018 年的 "Yahoo API Note"，CI 徽章指向 travis-ci.org — [backtrader README](https://github.com/mementum/backtrader/blob/master/README.rst)（源码核实，可作为停更的侧面证据）

**vectorbt（开源版）/ VectorBT PRO**
- vectorbt 在 2026-04-22 发布 1.0.0，之后依次是 1.1.0（2026-07-05）、1.1.1、1.1.2，到 1.2.0（2026-10-19）；2025 年以来 13 个版本；要求 Python >=3.11,<3.15 — [PyPI vectorbt](https://pypi.org/project/vectorbt/#history)（PyPI 核实）
- 新增可选 Rust 引擎 `vectorbt-rust`（当前 1.2.0）："Use precompiled kernels for supported operations without JIT compilation" — [vectorbt README](https://github.com/polakowo/vectorbt/blob/master/README.md)（源码核实）
- 许可证为 "Apache 2.0 with Commons Clause"，禁止 "Sell"，即禁止向第三方提供主要价值来自该软件的收费产品或服务。README 徽章写作 "Fair Code"。个人自用不受这一限制 — [vectorbt LICENSE.md](https://github.com/polakowo/vectorbt/blob/master/LICENSE.md)（源码核实）
- PRO 版在开源版基础上增加了 "parallelization, additional data integrations, portfolio optimization, pattern recognition, event projections, limit orders, leverage, and over 100 other features" — [vectorbt README](https://github.com/polakowo/vectorbt/blob/master/README.md)
- PRO 版价格：搜索没有找到可信的当前价格；二手来源称 PRO 通过 invite-only 的 GitHub 访问方式销售 — [IBKR Campus vectorbt guide](https://www.interactivebrokers.com/campus/ibkr-quant-news/vectorbt-an-introductory-guide/)（二手来源，未核实价格）

**zipline-reloaded**
- 最新版 3.2.0，2026-10-18 发布；上一版 3.1.1 是 2025-07-19，3.1 是 2024-09-26（大约一年一版）；许可证 Apache-2.0 — [PyPI zipline-reloaded](https://pypi.org/project/zipline-reloaded/#history)（PyPI 核实）
- README 原文："We continue to maintain Zipline Reloaded for bug, security and compatibility fixes. Our new feature development focuses on ML4T Backtest… For new projects, we recommend evaluating Backtest through the migration guide"；另外 "Package metadata constrains pandas to versions below 3.0" — [zipline-reloaded README](https://github.com/stefan-jansen/zipline-reloaded/blob/main/README.md)（源码核实）

**bt（pmorissette）**
- 最新版 1.4.1，2026-10-10 发布；2026-09 到 10 月接连发了 1.2.2、1.2.3、1.3.0、1.4.0、1.4.1；2025 年以来 12 个版本；许可证 MIT — [PyPI bt](https://pypi.org/project/bt/#history)（PyPI 核实）
- 定位："combine algorithms for scheduling, security selection, weighting, and rebalancing… nest strategies and securities in a common tree… configure commissions and transaction cost models"，统计和图表由 ffn 提供 — [bt README](https://github.com/pmorissette/bt/blob/master/README.md)（源码核实）

**backtesting.py（kernc）**
- 最新版 0.6.6，2026-07-22 发布；之前是 0.6.5（2025-07-30）和 0.6.2–0.6.4（2025 年 2–3 月）；2025 年以来 9 个版本；许可证 AGPL-3.0 — [PyPI backtesting](https://pypi.org/project/backtesting/#history)（PyPI 核实）

**Lumibot（Lumiwealth）**
- 最新版 4.6.22，2026-10-19 发布；2025 年以来 **314 个版本**（2026-10-10 一天就发了两版）；许可证 GPL-3.0；要求 Python >=3.10 — [PyPI lumibot](https://pypi.org/project/lumibot/#history)（PyPI 核实）
- README 现在以 AI 智能体交易为卖点（"AI agents that actually place the trade"），默认 AI 模板需要 `OPENAI_API_KEY`，模型调用按量计费；同时提供 `--template python`，用于不依赖 AI 的普通规则策略 — [Lumibot README](https://github.com/Lumiwealth/lumibot/blob/dev/README.md)（源码核实）

**Freqtrade / Jesse（加密货币，仅作设计参考）**
- Freqtrade 2026.9（2026-09-29），基本每月一版（2026.5.1、2026.6、2026.7、2026.8、2026.9）；许可证 GPLv3；要求 Python >=3.11 — [PyPI freqtrade](https://pypi.org/project/freqtrade/#history)（PyPI 核实）
- Jesse 3.4.0（2026-10-16），2025 年以来 109 个版本；PyPI 分类器写的是 MIT — [PyPI jesse](https://pypi.org/project/jesse/#history)（PyPI 核实）

**2025–2026 值得关注的新框架或替代品**
- **ml4t-backtest**（Stefan Jansen，zipline-reloaded 官方推荐的接班项目）：MIT 许可证，PyPI 首版 2026-01-04，最新 0.1.12（2026-09-24），仍处 0.x 阶段 — [PyPI ml4t-backtest](https://pypi.org/project/ml4t-backtest/#history)（PyPI 核实）。README 写明的特性："Event-driven architecture with point-in-time correctness"、"Exit-first order processing"、"Configurable execution modes (same-bar or next-bar fills)"、仓位级止损/止盈/移动止损、组合级约束（最大持仓数、回撤上限）、"40+ behavioral knobs for framework-specific parity"，以及 "The same Strategy class used in backtesting works unchanged in ml4t-live"。用 polars 作数据结构；支持 CPython 3.12–3.14 — [ml4t-backtest README](https://github.com/ml4t/backtest/blob/main/README.md)（源码核实）
- **PyBroker**（`lib-pybroker`）：2.0.0（2026-08-17）、2.0.1（2026-08-28）；PyPI 分类器为 "Free for non-commercial use" — [PyPI lib-pybroker](https://pypi.org/project/lib-pybroker/#history)。特性：NumPy+Numba 引擎，数据源支持 Alpaca、Yahoo、AKShare 和自定义源，walkforward analysis，用 bootstrapping 算指标，用 Optuna 调参，带缓存、可并行 — [PyBroker README](https://github.com/edtechre/pybroker/blob/master/README.md)（源码核实）。二手来源称其"no live trading" — [brightcoding blog](https://www.blog.brightcoding.dev/2026/09/29/edtechrepybroker-python-backtesting-with-ml-for-trading-strategies)
- **hftbacktest** 2.4.4（2025-12-10）：面向高频和订单簿，和本项目需求不匹配 — [PyPI hftbacktest](https://pypi.org/project/hftbacktest/#history)
- **TradeSight**：只有一篇 gist 提到，约 30 星，不建议考虑 — [gist 对比](https://gist.github.com/rmbell09-lang/01281551ac4672bd5d1a42bb58575144)（二手来源）

**可单独借用的周边组件（2026 年仍在维护）**
- `alpaca-py` 0.44.0（2026-08-11），Apache-2.0 — [PyPI alpaca-py](https://pypi.org/project/alpaca-py/#history)
- `ib_async` 2.1.0（2025-12-08），BSD；它是 `ib_insync` 的后继，后者最后一版 0.9.86 停在 2023-07 — [PyPI ib_async](https://pypi.org/project/ib_async/#history)；[PyPI ib_insync](https://pypi.org/project/ib_insync/#history)
- `pandas-market-calendars` 5.5.0（2026-10-05，MIT）；`exchange-calendars` 4.13.2（2026-03-10，Apache-2.0）；`quantstats` 0.0.86（2026-09-27，Apache-2.0）— [PyPI pandas-market-calendars](https://pypi.org/project/pandas-market-calendars/#history)；[PyPI exchange-calendars](https://pypi.org/project/exchange-calendars/#history)；[PyPI quantstats](https://pypi.org/project/quantstats/#history)

### Inferences
- backtrader 的停滞（最后发版 2023-04）以 PyPI 为准即可确认。新项目不宜再以它为底座。它的 IB 实盘适配器依赖的生态（IbPy、ib_insync）也都已停更或换代，这一点是推断。
- NautilusTrader 正处在 v2 迁移窗口期。现在上手意味着要么学 v1（只剩安全补丁），要么用 2.0.0rc（API 可能还会变）。对个人用户来说，这个时间点不理想。
- Lumibot 一年 300 多个版本，说明迭代极快，同时也意味着 API 和行为变动频繁，需要锁定版本。另外它现在的重心是 AI agent 和 BotSpot 托管，和用户"先定规则、防过拟合"的风格不完全一致。
- vectorbt 开源版 2026 年进入 1.x，并新增 Rust 引擎，复兴明显，可以重新纳入研究工具的候选。

### Gaps
- GitHub API 被拦截，拿不到各仓库的 star 数、最近提交日期、issue 活跃度。特别是 backtrader 在 GitHub 上是否还有零星提交，未能核实。
- LEAN 引擎仓库的 LICENSE 文件没能直接读取。普遍认知是 Apache-2.0，但本次未核实。
- VectorBT PRO 的当前价格和购买方式未能核实。

## 2. 架构：事件驱动还是向量化、防前视偏差、成本建模、公司行动、风控、调参，以及回测与实盘是否同一套代码

### Takeaway
事件驱动框架（LEAN、NautilusTrader、Lumibot、zipline、backtrader、ml4t-backtest）在结构上默认"下一根 bar 成交"，能天然避免用同一根收盘价既出信号又成交，回测和实盘也能共用策略代码。向量化框架（vectorbt、PyBroker 的 NumPy 引擎、bt 的再平衡树）速度快、适合扫参数，但成交时点需要用户自己移位，vectorbt 默认按**当根收盘价**成交。用户的规则 A 是"t 日收盘出信号、t+1 日收盘买入"，在任何框架里都需要显式表达为"信号滞后 1 天、按收盘成交"（MOC），这和多数框架默认的"下一根开盘成交"并不一样。

### Cited Findings
**成交时点与前视偏差**
- backtesting.py 源码注释原文："Unless you're running `Backtest(..., trade_on_close=True)`, market orders are filled on next bar's open"；`trade_on_close` 默认 False；开启后市价单按 `prev_close` 成交 — [backtesting.py source](https://github.com/kernc/backtesting.py/blob/master/backtesting/backtesting.py)（源码核实）
- backtesting.py 下单时按 `int(...)` 把股数取整，资金不足一股时会取消订单。`backtesting.lib` 提供 `FractionalBacktest`（碎股）和 `MultiBacktest` 两个类 — [backtesting.py source](https://github.com/kernc/backtesting.py/blob/master/backtesting/backtesting.py)；[backtesting/lib.py](https://github.com/kernc/backtesting.py/blob/master/backtesting/lib.py)（源码核实）
- backtesting.py `Backtest.optimize(method='grid', max_tries=...)`：默认网格搜索，另有 'sambo' 方法 — [backtesting.py source](https://github.com/kernc/backtesting.py/blob/master/backtesting/backtesting.py)（源码核实）
- vectorbt 的 `Order.price` 默认是 `np.inf`。源码原文："If `np.inf`, replaced by the current close"、"If `-np.inf`, replaced by the current open (if available) or the previous close" — [vectorbt portfolio/enums.py](https://github.com/polakowo/vectorbt/blob/master/vectorbt/portfolio/enums.py)（源码核实）。vectorbt 官方示例里也明确写了 `# Don't look into the future` / `result = result.vbt.fshift(1)` — [vectorbt portfolio/base.py](https://github.com/polakowo/vectorbt/blob/master/vectorbt/portfolio/base.py)（源码核实）
- vectorbt 自己的文档把 `from_order_func` 这种回调式模拟称作 "Realistic simulation as it follows the event-driven approach - less risk of exposure to the look-ahead bias" — [vectorbt portfolio/base.py](https://github.com/polakowo/vectorbt/blob/master/vectorbt/portfolio/base.py)（源码核实）
- NautilusTrader 的 bar 时间戳约定原文："each bar's initialization timestamp (`ts_init`) must represent the close of the interval. This prevents the complete bar from becoming visible before it formed." 每根 bar 被拆成 O→H→L→C 四个合成报价逐个撮合，"Orders submitted from `on_bar` arrive only after all four points for that bar have been processed"；`bar_adaptive_high_low_ordering` 可选择先走离开盘价更近的极值 — [Nautilus docs: bar-execution.md](https://github.com/nautechsystems/nautilus_trader/blob/develop/docs/concepts/backtesting/bar-execution.md)（源码核实）
- NautilusTrader 支持 `AT_THE_OPEN`、`AT_THE_CLOSE` 两种 time-in-force，也支持 OCO/OTO 等条件单 — [NautilusTrader README](https://github.com/nautechsystems/nautilus_trader/blob/develop/README.md)（源码核实）
- LEAN `EquityFillModel` 源码包含 "Do not fill on stale data" 逻辑：数据陈旧时 "wait for fresh prices instead of filling at an already past, stale bar's price"；止损单遇到不利跳空时按开盘价成交（`FilledWithOpenDueToUnfavorableGap`）— [LEAN EquityFillModel.cs](https://github.com/QuantConnect/Lean/blob/master/Common/Orders/Fills/EquityFillModel.cs)（源码核实）
- QuantConnect 公告（日期未显示）称：日线、小时线上的市价单现在会等新数据到来，再按交易恢复时那根 bar 的开盘价成交；休市期间下的单照旧转为 MarketOnOpen — [QC announcement: Closing the Stale-Price Loophole](https://www.quantconnect.com/announcements/20949/closing-the-stale-price-loophole-on-daily-and-hourly-data)（经搜索摘要获得，二手）。早期论坛讨论中有用户报告日线订单被拒（"Exchange closed"）— [QC forum 17951](https://www.quantconnect.com/forum/discussion/17951/order-rejected-on-daily-resolution/)
- Freqtrade 在文档里列出了全部回测假设："Entries happen at open-price"、"Exit-signal exits happen at open-price of the consecutive candle"、"All orders are filled at the requested price (no slippage) as long as the price is within the candle's high/low range"、"Stoploss exits happen exactly at stoploss price… but the loss will be `2 * fees` higher"、"Low happens before high for stoploss"，并说明同一根 K 线内多个信号的评估顺序 — [Freqtrade docs: backtesting.md](https://github.com/freqtrade/freqtrade/blob/develop/docs/backtesting.md)（源码核实）
- Freqtrade 文档还专门提醒显著性检验的局限："because backtesting and hyperopt evaluate many strategies, some will score a low p-value by chance alone" — [Freqtrade docs: backtesting.md](https://github.com/freqtrade/freqtrade/blob/develop/docs/backtesting.md)（源码核实）
- ml4t-backtest 把 "Configurable execution modes (same-bar or next-bar fills)" 和 "Exit-first order processing" 作为一等配置项 — [ml4t-backtest README](https://github.com/ml4t/backtest/blob/main/README.md)
- Jesse 宣称 "Backtest and livetrade multiple timeframes and symbols simultaneously without look-ahead bias"，并内置 "Rule Significance Testing" 和 Monte Carlo 分析 — [Jesse README](https://github.com/jesse-ai/jesse/blob/master/README.md)（源码核实；属于宣传性表述）

**成本、组合、风控、调参**
- NautilusTrader 回测文档分章讲解 Fill models（"Configure slippage and probabilistic fills"）、Accounts and margin、`MakerTakerFeeModel`，账户类型分 CASH 和 MARGIN，OMS 分 NETTING 等 — [Nautilus docs: backtesting index](https://github.com/nautechsystems/nautilus_trader/blob/develop/docs/concepts/backtesting/index.md)；[bar-execution.md](https://github.com/nautechsystems/nautilus_trader/blob/develop/docs/concepts/backtesting/bar-execution.md)（源码核实）
- bt 的核心设计是 Algo 栈加策略树（调度、选股、加权、再平衡），可配置佣金和交易成本模型 — [bt README](https://github.com/pmorissette/bt/blob/master/README.md)
- PyBroker 内置 walkforward analysis、bootstrap 指标、Optuna 调参 — [PyBroker README](https://github.com/edtechre/pybroker/blob/master/README.md)
- Jesse 用 Optuna 加 Ray 并行做调参 — [Jesse README](https://github.com/jesse-ai/jesse/blob/master/README.md)

**公司行动（拆股、分红、退市）**
- QuantConnect 的 US Equity Security Master 记录拆股、分红、退市、并购和代码变更，"split, dividend, and survivorship bias free US Equities backtesting is enabled by" 该数据集 — [QC US Equity Security Master](https://www.quantconnect.com/data/quantconnect-us-equity-security-master)（经搜索摘要获得，二手）
- 其余开源框架（backtesting.py、vectorbt、bt、backtrader）都依赖用户提供的已复权价格，没有内置公司行动处理。这是根据各 README 和 API 只接受 OHLCV DataFrame 得出的推断，未见官方明确声明。

**回测与实盘同一套代码**
- NautilusTrader README："The same strategy and execution-algorithm code can run across backtest and live systems"，同时坦承 "Live execution still introduces venue, transport, timing, persistence, external-activity, and reconciliation behavior that a simulation may not reproduce"，并单列一节 "Backtest and live differences"，逐项讲 Venue、Transport、Timing、Persistence、External activity、Reconciliation — [NautilusTrader README](https://github.com/nautechsystems/nautilus_trader/blob/develop/README.md)；[docs/concepts/live.md](https://github.com/nautechsystems/nautilus_trader/blob/develop/docs/concepts/live.md)（源码核实）
- Lumibot："`Strategy.backtest(...)` always backtests; `Trader.run_all()` or `strategy.run_live()` starts a configured broker"，并强调 "Keep strategy logic separate from broker configuration" — [Lumibot README](https://github.com/Lumiwealth/lumibot/blob/dev/README.md)（源码核实）
- Lumibot README 中的对比表（**厂商自制，有利益相关**）把"同一套代码跑回测和实盘"标为：Lumibot Yes、Backtrader Yes、Freqtrade Yes（crypto）、Zipline No、Backtesting.py No、Jesse "Yes (paid)"、vectorbt No、NautilusTrader Yes — [Lumibot README](https://github.com/Lumiwealth/lumibot/blob/dev/README.md)
- Freqtrade 原文："backtesting will **never** replace running a strategy in dry-run mode" — [Freqtrade docs](https://github.com/freqtrade/freqtrade/blob/develop/docs/backtesting.md)

### Inferences
- 用户规则 A 是"t 日收盘确认信号 → t+1 日收盘买入 → 收盘回到 20 日均线卖出 → -20% 止损"，全部按收盘价执行。各框架的映射方式如下：
  - vectorbt：`entries.vbt.fshift(1)` 或 `shift(1)`，再用默认 close 价成交；
  - backtesting.py：`trade_on_close=True`，并在 `next()` 里延迟一天下单；
  - NautilusTrader：`AT_THE_CLOSE` 时间有效期；
  - LEAN：MarketOnClose 订单。
- 这些都可以实现，但都需要显式配置。默认的"下一根开盘"会和现有 pandas 结果系统性不一致。
- 迁移时要做一个"对账测试"：同一组合成数据，现有 riskeval 循环和新框架的成交记录必须逐笔一致。这正好对应 ml4t-backtest 所说的 "framework-parity validation" 思路。
- 值得直接借用的设计（不必整体换框架）：
  1. 像 Freqtrade 那样把所有成交假设写成一张显式清单，放进每个研究模块的开头说明；
  2. 像 Nautilus 那样约定"bar 的时间戳代表收盘"；
  3. 像 LEAN 那样拒绝用陈旧价格成交；
  4. 像 ml4t-backtest 那样采用 exit-first 处理顺序，并把同 bar 或次 bar 成交做成配置项；
  5. 像 Nautilus 那样做实盘状态对账（reconciliation），对应用户手工维护的 holdings.csv 和券商实际持仓之间的对账。

### Gaps
- vectorbt、bt 对拆股和分红的处理，没有找到官方表述。
- LEAN 当前版本在日线数据下市价单的确切行为（是转 MOO、MOC 还是等新 bar），只拿到二手公告摘要，且公告日期不明。
- 各框架的默认佣金和滑点模型（例如 LEAN 默认使用哪家券商的费率模型）未能逐一核实。

## 3. 美股模拟盘与实盘的券商连接

### Takeaway
支持美股券商最全的是 LEAN（经 CLI 本地部署或云端部署，支持 IB、Tradier、Alpaca、Charles Schwab、TradeStation、Tastytrade、Webull、Public 等）和 Lumibot（Alpaca、IBKR、Tradier、Schwab 等）。NautilusTrader 的美股实盘只有 Interactive Brokers 一个渠道，**没有 Alpaca、Tradier、Schwab 适配器**。backtesting.py、vectorbt 开源版、bt、zipline-reloaded 都不提供实盘。

### Cited Findings
- LEAN CLI `lean live deploy` 的 `--brokerage` 可选项为：Paper Trading、Interactive Brokers、Tradier、Oanda、Bitfinex、Coinbase Advanced Trade、Binance、Zerodha、Samco、Terminal Link、Trading Technologies、Kraken、CharlesSchwab、Bybit、TradeStation、Alpaca、Tastytrade、Eze、dYdX、Webull、Public、ClearStreet。命令说明为 "Start live trading a project locally using Docker"，支持 `--detach` 后台运行 — [lean-cli README](https://github.com/QuantConnect/lean-cli/blob/master/README.md)（源码核实）
- NautilusTrader 集成列表中，Interactive Brokers 为 "Brokerage (multi-venue)"、状态 stable；Databento 为数据提供商、stable。其余集成均为加密货币交易所、DEX、Betfair、Polymarket 等，**列表里没有 Alpaca、Tradier、Schwab** — [Nautilus docs: integrations](https://github.com/nautechsystems/nautilus_trader/blob/develop/docs/integrations/index.md)（源码核实）
- Lumibot 支持的券商："Alpaca, IBKR, Tradier, Schwab, Tradovate, TopstepX (via ProjectX), Bitunix, Polymarket, selected CCXT"；`lumibot run my-bot --paper` 需要 Alpaca 模拟盘凭证（`ALPACA_API_KEY`、`ALPACA_API_SECRET`）— [Lumibot README](https://github.com/Lumiwealth/lumibot/blob/dev/README.md)（源码核实）
- Lumibot 对比表称 backtrader 有 "IB and other integrations; verify adapter maintenance"；Zipline、Backtesting.py、vectorbt 的券商执行均为 "None/No" — [Lumibot README](https://github.com/Lumiwealth/lumibot/blob/dev/README.md)（厂商自制表）
- ml4t-backtest 宣称回测用的 Strategy 类可以原样用于 `ml4t-live`，但 README 没有列出具体券商 — [ml4t-backtest README](https://github.com/ml4t/backtest/blob/main/README.md)
- QuantConnect 论坛有用户报告"日线级别交易配合 Alpaca 时出现问题" — [QC forum 18268](https://www.quantconnect.com/forum/discussion/18268/day-resolution-trade-and-have-issue-with-alpaca/)（只看到标题，内容未核实）
- 如果不用框架、自己直连券商：`alpaca-py` 0.44.0（2026-08）和 `ib_async` 2.1.0（2025-12）都在维护 — [PyPI alpaca-py](https://pypi.org/project/alpaca-py/#history)；[PyPI ib_async](https://pypi.org/project/ib_async/#history)

### Inferences
- 对一个 8000 美元、日线频率、已有 GitHub Actions 每日流程的账户，最轻的"模拟盘"路径是：在现有 Actions 任务末尾，用 `alpaca-py` 把当日操作单提交到 Alpaca paper 账户，下一交易日再拉回成交和持仓，与 holdings.csv 对账。这不需要换框架。
- 如果想要"框架托管的持续运行模拟盘"，可选 LEAN（云端 live node 或本地 Docker）或 Lumibot（自托管进程或 BotSpot）。这两条路都需要常驻进程，而 GitHub Actions 不适合常驻，这是推断。
- NautilusTrader 只能经 IB 接美股；IB 需要常驻 TWS 或 IB Gateway，单人运维负担较大。

### Gaps
- Lumibot 和 LEAN 的 Alpaca、Schwab 适配器是否支持碎股和 MOC 订单，未能核实。
- backtrader 现有 IB 适配器能否在当前 IB API 下工作，未能核实。
- Alpaca 本身的模拟盘、碎股、MOC 订单规则，不在本次范围内，见其他研究员的笔记。

## 4. 数据处理：集成的数据源、时点正确与无幸存者偏差的股票池

### Takeaway
只有 QuantConnect（云端或付费的本地数据）开箱提供 1998 年起、无幸存者偏差的美股全市场数据和每日股票池，这正好能解决本项目"16 只半导体股按今天的市值挑选"带来的幸存者偏差。开源框架基本都是"自带数据"，NautilusTrader 通过 Databento，PyBroker 和 Lumibot 通过 Alpaca 或 Yahoo，都不含历史成分股和退市股信息。

### Cited Findings
- QuantConnect 的 AlgoSeek US Equities 数据覆盖 1998 年以来所有 SIP 上市股票，约 27,500 只，"survivorship bias-free"，分辨率从 tick 到日线，不含 OTC — [QC data: AlgoSeek US Equities](https://quantconnect.com/data/algoseek-us-equities)；[QC docs](https://www.quantconnect.com/docs/v2/writing-algorithms/datasets/algoseek/us-equities)（二手：经搜索摘要获得）
- US Equity Coarse Universe 是每日全市场股票池，从 1998-01 开始，总计约 30,000 只，每天约 8,000 只，带收盘价和成交量，运行时与 Morningstar 基本面数据合并 — [QC data: US Equity Coarse Universe](https://www.quantconnect.com/data/quantconnect-us-coarse-universe-constituents)（二手）
- Morningstar 基本面数据覆盖约 8,000 只、从 1998-01 开始，不含 ETF、ADR、OTC。较早的标的，filing date 按 as-of 日期后约 45 天估算；数据采用 "As Original Reported"，即不回填后来的更正 — [QC docs: Morningstar US Fundamentals](https://www.quantconnect.com/docs/v2/writing-algorithms/datasets/morningstar/us-fundamental-data)（二手）
- LEAN CLI 的 `--data-provider-historical` 可选：Interactive Brokers、Oanda、Bitfinex、Coinbase Advanced Trade、Binance、Kraken、CharlesSchwab、IQFeed、Polygon、FactSet、AlphaVantage、CoinApi、ThetaData、QuantConnect、Local、Terminal Link、Bybit、TradeStation、Alpaca、Tastytrade、Eze、dYdX、Databento、Webull、Public。另有 `--data-purchase-limit`，用于限制下载 QuantConnect 数据时花费的 QCC — [lean-cli README](https://github.com/QuantConnect/lean-cli/blob/master/README.md)（源码核实）
- NautilusTrader 的数据提供商以 Databento（stable）为主，另有 Tardis（加密）、CoinAPI（beta）；本地用 Parquet/Arrow 格式的数据目录（data catalog）— [Nautilus integrations](https://github.com/nautechsystems/nautilus_trader/blob/develop/docs/integrations/index.md)；[backtesting index](https://github.com/nautechsystems/nautilus_trader/blob/develop/docs/concepts/backtesting/index.md)
- PyBroker 内置 Alpaca、Yahoo Finance、AKShare 数据源，可自定义数据源，带缓存 — [PyBroker README](https://github.com/edtechre/pybroker/blob/master/README.md)
- Lumibot 默认用 Yahoo 免费日线回测（"Historical prices come from Yahoo"、`BACKTESTING_DATA_SOURCE=yahoo`），宣传上还有 BotSpot 托管数据 — [Lumibot README](https://github.com/Lumiwealth/lumibot/blob/dev/README.md)
- zipline 用 data bundle 机制和 `exchange_calendars` 交易日历（2.4 版起要求 >=4.2）— [zipline-reloaded README](https://github.com/stefan-jansen/zipline-reloaded/blob/main/README.md)

### Inferences
- 本项目已在 CLAUDE.md 中承认幸存者偏差（16 只半导体按今天的市值挑选）。要量化这一偏差，最低成本的办法是在 QuantConnect 免费云端，用 Coarse Universe 按"当时"的市值或行业重建半导体股票池，复跑规则 A，与现有结果对比。这是一次性研究，不需要迁移整个项目。
- 本地开源框架不能解决幸存者偏差；数据才是瓶颈，框架不是。

### Gaps
- QuantConnect 免费账户在云端回测时，能否不限量使用 Coarse Universe 和 Morningstar 数据，没有拿到官方定价页确认。
- Morningstar 基本面对已退市公司是否同样时点正确，未找到明确说明（搜索摘要也指出了这一点）。
- 是否存在价格合理、面向个人的无幸存者偏差美股数据源（如 Norgate、Sharadar），可供本地框架使用，不在本次检索范围内。

## 5. 学习曲线与单人运维成本；QuantConnect 托管定价是否适合个人

### Takeaway
QuantConnect 免费层只能做云端回测，不能做模拟盘或实盘；最便宜的可实盘方案大约是每月 34–84 美元（二手来源，数字有冲突）。本地 LEAN CLI 需要付费组织，美股本地数据还要额外买 Security Master（约 1,200 美元/年，二手来源）。对本金约 8000 美元的账户，每年 400–1000 美元的固定成本约占本金的 5–12%，显著侵蚀收益。开源方案中，backtesting.py、vectorbt、bt 上手最快；NautilusTrader 和 LEAN 本地版学习曲线最陡。

### Cited Findings
- QuantConnect 定价（**均为二手，且相互冲突**）：
  - 2026-10 的评测称最便宜的付费方案 Researcher 为 84 美元/月（888 美元/年），1 个用户、2 个 live 节点；另一来源把 84 美元拆成 10 美元席位 + 14 美元回测节点 + 12 美元研究节点 + 24 美元 live 节点 + 24 美元 assistant 节点，并指出这是可配置的资源包；
  - 另有来源称"10 美元席位 + 24 美元 L-MICRO live 节点 = 34 美元/月"；
  - 2025 年及更早的评测写的是 60 美元/月；
  - 免费层"unlimited backtesting with minute, hourly, and daily data"，但不含 tick/second 数据，也不含模拟盘和实盘。
  - 来源：[newtrading.io review](https://www.newtrading.io/quantconnect-review/)；[pickuma review](https://pickuma.com/for-investor/quantconnect-review/)；[newyorkcityservers review](https://newyorkcityservers.com/blog/quantconnect-review)；[quantt review](https://www.quantt.co.uk/resources/quantconnect-review)
  - 官方定价页 quantconnect.com/pricing 未能直接访问。
- LEAN CLI：官方文档称"you must be a member in an organization on a paid tier to use the CLI"；本地使用美股数据需要 US Equity Security Master，官方文档示例标价 1,200 美元/年；示例算法的美股数据为首次 7.05 美元、之后每天 0.05 美元；论坛用户称 `lean backtest` 每遇到新数据都会扣 QCC，`--data-purchase-limit 0` 可以阻止下载 — [QC docs: lean-cli backtesting deployment](https://www.quantconnect.com/docs/v2/lean-cli/backtesting/deployment)；[QC forum 14609](https://www.quantconnect.com/forum/discussion/14609/my-notes-on-payment-for-local-historical-data-using-lean-cli/)；[QC forum 19776](https://www.quantconnect.com/forum/discussion/19776/bare-minimum-subscription-to-backtest-intraday-strategy-with-lean-cli-and-use-optimization/)（经搜索摘要获得，二手）
- LEAN CLI 本地运行依赖 Docker（"Start live trading a project locally using Docker"）— [lean-cli README](https://github.com/QuantConnect/lean-cli/blob/master/README.md)
- NautilusTrader 的 develop 分支要求 Python 3.13–3.14；策略需要按 Actor/Strategy、MessageBus、Cache、Venue、OMS 等概念组织；回测文档仅"阅读指南"就有 8 个子页面 — [README](https://github.com/nautechsystems/nautilus_trader/blob/develop/README.md)；[backtesting index](https://github.com/nautechsystems/nautilus_trader/blob/develop/docs/concepts/backtesting/index.md)
- backtesting.py 一个 `Strategy` 子类只需写 `init()` 和 `next()` 两个方法，十几行代码就能跑出完整统计 — [backtesting.py README](https://github.com/kernc/backtesting.py/blob/master/README.md)
- Lumibot 一条命令即可回测（"runs a real backtest on free daily data… No API key, no broker account"），但 AI 模板需要付费的 OpenAI API — [Lumibot README](https://github.com/Lumiwealth/lumibot/blob/dev/README.md)
- zipline-reloaded 的 pandas 必须 <3.0，配置 data bundle 有一定门槛 — [zipline-reloaded README](https://github.com/stefan-jansen/zipline-reloaded/blob/main/README.md)

### Inferences
- 只用 QuantConnect **免费层**做云端研究（例如上面的幸存者偏差复核），对个人很划算；持续付费做实盘则不划算。用户的规则频率极低（一年寥寥数笔），GitHub Actions 加券商 API 的现有架构，在成本上明显占优。
- NautilusTrader 适合未来做日内或多券商的专业化系统，不适合"每天收盘后算一张单"这种需求。

### Gaps
- QuantConnect 官方定价页未能直接访问，84、60、34 美元几个数字互相冲突，需要用户自己打开 quantconnect.com/pricing 确认。
- QCC 与美元的换算、免费层的云端数据配额，均未核实。

## 6. 推荐相关事实：(a) 快速移植现有日线 pandas 规则；(b) 持续运行模拟盘；(c) 未来日内实验

### Takeaway
(a) 移植成本最低的是 vectorbt（pandas 原生，信号矩阵加 `shift(1)` 就能复现）和 backtesting.py（单标的规则验证）；bt 适合核心仓与分散仓的再平衡框架。(b) 最省事的持续模拟盘方式，是在现有 GitHub Actions 中直接接入 alpaca-py。如果一定要框架，Lumibot（Alpaca paper 一条命令）和 LEAN（需要付费 live 节点或本地 Docker）可选。(c) 日内实验的长期首选是 NautilusTrader（纳秒级事件驱动、同码实盘），但它 v2 尚在 RC 阶段，美股只能接 IB；LEAN 是付费的替代。

### Cited Findings
- vectorbt：pandas-native API（"custom accessors… directly on pandas objects"），NumPy+Numba，可选 Rust 引擎，定位是 "compare thousands of ideas across assets and timeframes" — [vectorbt README](https://github.com/polakowo/vectorbt/blob/master/README.md)
- backtesting.py：内置 `FractionalBacktest` 和 `MultiBacktest`，可选 `trade_on_close`，`optimize` 支持网格和 sambo 两种方法 — [backtesting.py source](https://github.com/kernc/backtesting.py/blob/master/backtesting/backtesting.py)；[lib.py](https://github.com/kernc/backtesting.py/blob/master/backtesting/lib.py)
- bt：用于调度、选股、加权、再平衡的策略树 — [bt README](https://github.com/pmorissette/bt/blob/master/README.md)
- Lumibot：`lumibot backtest my-bot --days 90` 和 `lumibot run my-bot --paper`（使用 Alpaca paper）— [Lumibot README](https://github.com/Lumiwealth/lumibot/blob/dev/README.md)
- LEAN CLI：`lean live deploy --brokerage Alpaca|"Interactive Brokers"|Tradier|CharlesSchwab ... --detach` — [lean-cli README](https://github.com/QuantConnect/lean-cli/blob/master/README.md)
- NautilusTrader："Backtesting: Multiple venues, instruments, and strategies simultaneously using historical quote tick, trade tick, bar, order book… with nanosecond resolution"；"Live: Identical strategy implementations between research and live deployment" — [NautilusTrader README](https://github.com/nautechsystems/nautilus_trader/blob/develop/README.md)
- ml4t-backtest：同一 Strategy 类可用于 ml4t-live，可选同 bar 或次 bar 成交，有组合级回撤限制，但版本仅 0.1.x — [ml4t-backtest README](https://github.com/ml4t/backtest/blob/main/README.md)；[PyPI](https://pypi.org/project/ml4t-backtest/#history)

### Inferences（供撰写者参考的结论草稿；均为规则输出加历史回测层面的工程判断，不是投资建议）
- **不建议整体迁移到某个框架。** 现有 riskeval 加 GitHub Actions 已经满足日线、低频、单人的需求，换框架的主要收益不在回测能力本身，而在三处：(1) 用 vectorbt 做参数稳健性扫描（例如 z 阈值、均线长度的热力图），但要警惕这本身会增加过拟合风险，必须遵守"留出数据只用一次"；(2) 接券商模拟盘，直接用 alpaca-py 即可；(3) 用 QuantConnect 免费云端，在无幸存者偏差的股票池上做一次复核。
- **可直接借鉴的设计清单：**
  1. 把成交假设写成显式清单，参考 Freqtrade 的 "Assumptions made by backtesting"；
  2. 订单类型显式区分 MOC/MOO，避免隐式的"按收盘价成交"；
  3. 处理顺序 exit-first、止损优先（Freqtrade："Low happens before high for stoploss"）；
  4. 拒绝在陈旧数据上成交（LEAN）；
  5. 实盘与本地账本的对账（Nautilus reconciliation）；
  6. 把策略逻辑和券商配置分离（Lumibot）；
  7. 用交易日历库（pandas-market-calendars / exchange-calendars）判断交易日；
  8. 用 quantstats 生成 tearsheet。
- 如果以后要做日内实验，优先评估 NautilusTrader，且等 v2 正式版发布后再上手；需要的数据源（Databento）和券商（IB）都要另外付费或开户。

### Gaps
- 没有找到 2025–2026 年独立、可信、横向测评这些框架回测准确性（同策略跨框架对账）的第三方研究。ml4t-backtest 声称做了 framework-parity validation，但具体结果未读取。
- Lumibot 和 LEAN 在 Alpaca 上能否碎股下 MOC 单（对 8000 美元账户买 SMH 等较贵标的很重要），未能核实。
