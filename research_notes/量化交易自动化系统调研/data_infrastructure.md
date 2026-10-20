# 个人自动化交易系统：数据源与轻量基础设施调研（截至 2026-10-20）

> 研究方法说明（给报告撰写者）：本轮共约 20 次搜索/抓取。**这个环境的 WebFetch 对多数厂商官网直接 DNS 失败**（docs.github.com、massive.com、docs.alpaca.markets、quantrocket.com 均报 `getaddrinfo ENOTFOUND`），`gh api` 读 github/docs 仓库也被会话权限拒绝（403）。所以下面大部分数字来自**搜索引擎摘要**：有的是官方页面的摘要（Alpaca docs、Norgate、Databento、IBKR、QuantConnect、GitHub enterprise-server docs），有的是第三方汇总。每条都标了来源类型；标"第三方/未核实"的价格，下单前要去官网再看一次。

## Q1. 美股数据源：覆盖范围、复权、退市股、历史成分股、业余用户价格、限流和条款

### Takeaway
对这个项目（约 20 个代码、日线为主、偶尔用小时线）来说，最省事的升级路径是：日线和小时线换成 **Alpaca 免费档的历史 SIP 数据**（有官方 API，限 200 次/分钟，只是最近 15 分钟的数据拿不到），yfinance 降级为备份；要做"无幸存者偏差"的宽基研究，再单独买一年 **Norgate Platinum（约 630 美元/年）** 或 QuantConnect Security Master。Polygon.io 确实已经改名为 **Massive**。Databento 按 GB 计费，新用户送 125 美元额度，适合一次性拉取高质量分钟或逐笔数据，不适合当作日常订阅。

### Cited Findings

**yfinance / Yahoo（现有方案）**
- yfinance README 自述：它是使用 Yahoo"公开可用 API"的开源工具，"intended for research and educational purposes"；数据使用权要看 Yahoo 的条款；另有一句 "the Yahoo! finance API is intended for personal use only"；项目"not affiliated, endorsed, or vetted by Yahoo"；代码采用 Apache 许可，但这个许可不覆盖数据 — [yfinance README (jsDelivr mirror)](https://cdn.jsdelivr.net/gh/ranaroussi/yfinance@main/README.md)、[GitHub ranaroussi/yfinance](https://github.com/ranaroussi/yfinance)
- 限流问题：用户反映 0.2.49 到 0.2.57 版本都出现过 `YFRateLimitError`（"Too Many Requests"），时间从 2024 年底延续到 2025 年 4 月；有人批量下载约 950 个代码后开始收到 429 — [yfinance issue #2128](https://github.com/ranaroussi/yfinance/issues/2128)；有人换了 IP 仍然被限 — [issue #2422](https://github.com/ranaroussi/yfinance/issues/2422)；QuantConnect 论坛有人说约 2025-02-21 开始频繁出现，提供方没有任何公告 — [QuantConnect forum 18702](https://www.quantconnect.com/forum/discussion/18702)；另见 [yfinance discussion #2431](https://github.com/ranaroussi/yfinance/discussions/2431)
- Yahoo 没有公布限额。issue 里提到的"360 次/小时"只是用户自己的说法，不是官方数字 — [issue #2128](https://github.com/ranaroussi/yfinance/issues/2128)
- 有报告说 Colab 这类共享云 IP 和家用 IP 的限流待遇不一样 — [Quantra community](https://quantra.quantinsti.com/community/t/yfratelimiterror/26462)（属于轶事）

**Alpaca Market Data（官方文档摘要）**
- Basic/Free 是模拟盘和实盘账户的默认档位：实时股票数据只有 IEX；websocket 最多 30 个代码；历史数据从 2016 年开始；历史请求拿不到最近 15 分钟；历史 API 200 次/分钟 — [Alpaca docs: About Market Data API](https://docs.alpaca.markets/docs/about-market-data-api)
- Algo Trader Plus 每月 99 美元：覆盖全美所有交易所的实时数据（SIP，即合并行情），websocket 订阅不限数量，历史数据不受限制，历史 API 10,000 次/分钟 — [Alpaca docs](https://docs.alpaca.markets/docs/about-market-data-api)、[Alpaca Market Data FAQ](https://docs.alpaca.markets/us/docs/market-data-faq)
- 新版文档把 Basic 改叫 "Free"，另有面向券商的 Broker Professional（每台设备每月 99 美元）；免费档只是查不到最近 15 分钟的 SIP 数据，其余历史数据不受限 — [Alpaca docs (market-data)](https://docs.alpaca.markets/docs/market-data)
- 论坛回复称 IEX 只占全部成交的 2% 到 3% 左右，所以免费档的实时报价可能和全市场价格差得比较明显；免费用户可以请求延迟 15 分钟的 SIP — [Alpaca forum](https://forum.alpaca.markets/t/alcapa-current-quote-price-is-way-off-from-market-price/18063)（论坛，非官方声明）

**Polygon.io → Massive（已核实改名，价格有冲突）**
- Polygon.io 于 **2025-10-30** 正式更名为 Massive.com，原有账户、API key 和接口继续可用，过渡期内 api.polygon.io 和 api.massive.com 并行 — [apicostcalc blog](https://apicostcalc.com/blog/polygon-massive-rebrand-api-pricing.html)（第三方）；同一来源（2026-09-12 的文章）又说 polygon.io/pricing 当时"刚开始"跳转到 massive.com/pricing，和前面的日期有些矛盾
- 股票 Basic 档免费，限 5 次/分钟，只有日终数据；Starter 每月 29 美元；Advanced 每月 199 美元；Developer 档一处写 79 美元/月 — [apicostcalc](https://apicostcalc.com/blog/polygon-massive-rebrand-api-pricing.html)，另一处写 99 美元/月（改名前的快照）— [QVeris guide](https://qveris.ai/zh-cn/guides/polygon-pricing-optimized)。**冲突，未解决**
- 按资产类别分别计费（股票、期权各自订阅）— [apicostcalc](https://apicostcalc.com/blog/polygon-massive-rebrand-api-pricing.html)

**Norgate Data（官方页面摘要）**
- 美股套餐价格（美元，6 个月 / 12 个月）：Silver 148.50 / 270；Gold 198 / 360；Platinum 346.50 / 630；Diamond 433.13 / 787.50 — [Norgate Stock Market Packages](https://norgatedata.com/stockmarketpackages.php)
- 退市股和历史指数成分股**只有 Platinum 和 Diamond 才有**；Platinum 日线从 1990 年起，Diamond 从 1950 年起 — [Norgate packages](https://norgatedata.com/stockmarketpackages.php)、[Norgate subscribe](https://norgatedata.com/subscribe/subscribe.php)；有免费试用 — [Norgate free trial](https://norgatedata.com/subscribe/freetrial.php)
- Norgate 有 Python 读取历史成分股的用法示例；该文还指出，对基于指数的策略，只消除"退市偏差"不够，还要有历史成分股 — [Concretum Group](https://concretumgroup.com/historical-constituents-of-an-equity-index-in-python-norgate-data/)

**Databento（官方 FAQ 摘要）**
- 按用量计费，每个数据集按每 GB 定价，按量付费没有月费；历史数据按"二进制编码下未压缩的大小"计量，CSV/JSON 格式导出不另收费 — [Databento FAQ: usage pricing](https://databento.com/docs/faqs/usage-pricing-and-data-credits)、[Databento pricing](https://databento.com/pricing)
- 新用户送 125 美元额度，6 个月内有效，可以用于历史数据或抵扣第一个月的订阅费 — [Databento FAQ](https://databento.com/docs/faqs/usage-pricing-and-data-credits)
- 美股覆盖 15 家交易所和 30 个 ATS，统一定价 — [NexusFi listing](https://nexusfi.com/d/data-providers/databento/)（第三方）

**Sharadar（Nasdaq Data Link）**
- Nasdaq Data Link 部分数据只面向机构，"not available for academic or personal use"；价格在各产品页的 "View Pricing" 里，某些数据对个人账户只显示 "Contact Sales" — [Nasdaq Data Link help](https://help.data.nasdaq.com/article/568-how-much-does-nasdaq-data-link-data-cost-how-do-i-find-pricing)
- QuantRocket 称专业用户必须直接向 Nasdaq Data Link 购买 Sharadar — [QuantRocket Sharadar pricing](https://www.quantrocket.com/pricing/data/sharadar)（页面没能抓取，只看到摘要）
- 旧报道提到 Quandl 时代个人访问从 50 美元/月起，日期不明，很可能已经过时 — [Waters Technology](https://waterstechnology.com/node/2382777)

**Tiingo / EODHD / FMP（只有第三方汇总，均未核实）**
- EODHD：G2 页面（2026-02-04 更新）列出日终基础档 19.99 欧元/月，更高档 29.99、59.99、99.99 欧元 — [G2](https://www.g2.com/products/eodhd-financial-data-apis/pricing)；EODHD 自家页面写"19.99 美元起" — [EODHD](https://eodhd.com/financial-summary/TRFOX.US)（币种不一致）。免费档一说 20 次/天 — [MEXC](https://www.mexc.com/news/476023)，另一说 8 次/分钟、800 次/天 — [Stackademic](https://blog.stackademic.com/stock-price-api-best-free-vs-paid-options-2026-82370a377819)（冲突）
- EODHD 有关于 S&P 500 历史成分股数据的博客或产品 — [EODHD blog](https://eodhistoricaldata.com/blog/sp-500-historical-constituents-data)
- FMP：免费档为仅限美国的日终沙盒，250 次/天；付费档 Starter、Premium、Ultimate，全球覆盖只有最高档 — [Stackademic](https://blog.stackademic.com/stock-price-api-best-free-vs-paid-options-2026-82370a377819)；价格区间 0 到 99 美元/月 — [Lambda Finance](https://www.lambdafin.com/articles/financial-data-api-2026)
- Tiingo：0 到 30 美元/月，含 IEX 盘中数据 — [Lambda Finance](https://www.lambdafin.com/articles/financial-data-api-2026)；EOD 端点覆盖美股和 ETF — [QVeris](https://www.qveris.ai/tools/tiingo.core.eod.v1)

**Interactive Brokers（IBKR 知识库摘要）**
- 非专业用户的基础包 "US Securities Snapshot and Futures Value Bundle" 每月 10 美元，当月佣金满 30 美元即免；快照报价另收每次 0.01 美元（美股/ETF），不在免除范围内，但每个账户每月有 1 美元快照额度 — [IBKR KB: Subscription considerations for U.S. market data](https://ibkb.interactivebrokers.com/fr/node/2840)、[IBKR market data pricing](https://www.interactivebrokers.ie/en/index.php?f=37645)
- 非专业用户的定义：没有在金融监管机构注册、不担任投资顾问、不受雇于金融机构从事豁免注册职能的个人 — [IBKR KB](https://ibkb.interactivebrokers.com/fr/node/2840)
- 有用户反映满足条件也被收了 10 美元；最便宜的纯美股选项约 11 美元 — [EliteTrader](https://www.elitetrader.com/et/threads/snapshot-fee.373288/)（轶事）

### Inferences
- 对本金约 8000 美元、只用日线的散户，**Alpaca 免费历史数据是 yfinance 最自然的替代品**：有官方 API 和 key，限流有公开文档，日线和小时线都有，又是同一家券商的模拟盘和实盘接口（数据和下单同源）。缺点是只能回溯到 2016 年，而项目研究从 2015 年开始，2015 年这段还得靠 yfinance 或其他来源补。
- yfinance 在 GitHub Actions 共享 IP 上更容易被限流（推测，依据是上面 Colab 和家用 IP 的对比报告）。现有工作流应保留重试、退避、缓存，并在数据缺失时发"数据异常"告警，而不是悄悄沿用旧数据。
- 复权口径要统一：Alpaca 的 bars 有 adjustment 参数（raw/split/dividend/all，根据训练知识，本次未核实到官方原文）；yfinance 的 `auto_adjust` 默认值曾经改过（同样未核实）。切换数据源时，应该对 16 只股票做一次逐日收盘价对比（同一复权口径），差异超过阈值就报警。
- "规则 A"依赖 20 日 z 值和 200 日均线，对复权口径（分红复权与否）比较敏感。建议在研究模块开头事先写死"用哪种复权"。

### Gaps
- 没能直接抓到 massive.com/pricing 和 Alpaca 官方页面全文，Massive 的 Developer 档价格（79 还是 99 美元）未解决；Massive 免费档的历史深度和复权说明没拿到。
- Yahoo 正式的服务条款（ToS）原文没拿到。"personal use only"这一句来自 yfinance README，不是 Yahoo 自己的表述。
- Sharadar 当前对个人用户的价格、是否还能个人购买，没有找到官方数字。
- Tiingo、EODHD、FMP 的 2026 年官方价格，以及它们是否含退市股、复权方式、再分发条款，没有拿到一手来源。
- 各厂商的再分发条款（例如能否把数据汇总后提交到公开 GitHub 仓库）都没核实到原文。

## Q2. 低成本避免幸存者偏差

### Takeaway
三档方案：免费档用社区维护的 S&P 500 历史成分股表（fja05680/sp500、hanshof/sp500_constituents，1996 年起）加任意价格源，但退市股的价格仍然缺；中档用 **Norgate Platinum（630 美元/年，含退市股和历史成分股，1990 年起）**；或者用 **QuantConnect US Equity Security Master**（旧报价约 600 美元/年，只能在 LEAN 引擎里用）。只补退市股价格不够，还要有成分股是哪天进、哪天出的时间点数据。

### Cited Findings
- fja05680/sp500：S&P 500 当前及历史成分股列表，1996 年起，约 525 star — [GitHub topic sp500](https://github.com/topics/sp500)、[repos.ecosyste.ms](https://repos.ecosyste.ms/topics/sp500)；同一作者还有 1927 年以来的 S&P 500 指数点位序列（这是点位，不是成分股）— [fja05680/dow-sp500-100-years](https://github.com/fja05680/dow-sp500-100-years)
- hanshof/sp500_constituents：1996-01-02 至今按日期的成分股 CSV — [GitHub hanshof/sp500_constituents](https://github.com/hanshof/sp500_constituents)
- 可以用 Wikipedia 修订历史重建历史成分股 — [Medium (Kestel)](https://medium.com/@beni.kestel001/how-to-get-historical-s-p-500-components-using-wikipedias-api-8ef58f657c4f)
- Norgate 的退市股和历史成分股只在 Platinum 和 Diamond 档 — [Norgate](https://norgatedata.com/stockmarketpackages.php)；对基于指数的策略，只消除退市偏差不够 — [Concretum Group](https://concretumgroup.com/historical-constituents-of-an-equity-index-in-python-norgate-data/)
- QuantConnect：用 LEAN CLI 在本地下载美股数据，需要订阅 US Equity Security Master，并且组织必须在付费档；2022 年的论坛回复提到 600 美元/年；批量订阅可下载完整数据集，一年内每日更新，文档称这样可以避免选择偏差；数据"designed to be used in the LEAN Engine and cannot be consumed another way" — [QuantConnect LEAN CLI datasets key concepts](https://www.quantconnect.com/docs/v2/lean-cli/datasets/quantconnect/key-concepts)、[QC forum 15611](https://www.quantconnect.com/forum/discussion/15611/downloading-lean-data/)、[QC forum 14378](https://www.quantconnect.com/forum/discussion/14378/how-to-use-qcc-to-purchase-download-and-use-data-locally/)
- Security Master 包含拆股、分红和代码变更（map/factor 文件），LEAN 会自动处理这些公司行为 — [QuantConnect docs](https://www.quantconnect.com/docs/v2/lean-cli/datasets/quantconnect/key-concepts)
- EODHD 提供 S&P 500 历史成分股数据（具体哪一档包含，未核实）— [EODHD blog](https://eodhistoricaldata.com/blog/sp-500-historical-constituents-data)

### Inferences
- 免费的成分股表配 yfinance 有一个根本问题：退市代码在 Yahoo 上往往已经没有历史数据，所以只能减轻幸存者偏差，消除不了。
- 对本项目：16 只半导体股是"按今天市值挑的"，偏差主要来自挑选，而不是成分股。一个便宜的修正办法是用 SMH 或 SOXX 的**历史持仓**按时间点定义股票池（数据来源未核实），或者干脆以 ETF 层面的结果为准（这和 CLAUDE.md 里已知的局限一致）。
- 如果只想一次性验证"规则 A 在无幸存者偏差的半导体或 S&P 500 股票池里是否还成立"，Norgate 的免费试用或买 6 个月 Platinum（346.50 美元）是成本最低的严谨方案。但它依赖 Windows 上的 Norgate Data Updater（根据训练知识，未核实），**不能直接在 GitHub Actions 的 Linux runner 上跑**，需要在本地机器上导出汇总结果。

### Gaps
- QuantConnect Security Master 的 2026 年价格，以及是否明确包含退市股，没有一手确认。
- fja05680/sp500 的更新频率和最新维护状态，没有抓到仓库原页。
- 没找到 SMH 或 SOXX 历史持仓的免费来源。

## Q3. 调度和运行环境：GitHub Actions cron 的可靠性、VPS/云函数/家用机、时区与夏令时、交易所日历

### Takeaway
GitHub Actions 的 `schedule` 官方承认在高负载时会延迟，**整点尤其严重，极端情况下任务会被直接丢弃**；公共仓库 60 天没有活动会被自动停用（多个第三方来源一致，与官方文档措辞相符，但本次没抓到官方原文）。对"收盘后跑日报"可以接受；对"收盘前 10 分钟下单"**不可靠**，应该改用 VPS 或家用机的 systemd timer/cron，或者把 Actions 只当作兜底。cron 用 UTC，美东夏令时切换要自己处理：同时排两个 UTC 时间，或在脚本里用交易所日历判断。

### Cited Findings
- GitHub 官方 docs（enterprise-server 教程页）：schedule 事件在 Actions 高负载时可能延迟，高负载时段包括每个整点开始时；负载足够高时，部分排队的任务可能被丢弃；建议把 cron 分钟设在非整点 — [GitHub Docs: close inactive issues (GHES 3.19)](https://docs.github.com/en/enterprise-server@3.19/actions/tutorials/manage-your-work/close-inactive-issues)、[GHES 3.21](https://docs.github.com/en/enterprise-server@3.21/actions/tutorials/manage-your-work/close-inactive-issues)
- 第三方称高峰期典型延迟为 5 到 30 分钟（GitHub 没有公布官方数字）— [runhooks.app](https://runhooks.app/blog/github-actions-scheduled-workflows-unreliable/)、[cronping](https://cronping.com/solutions/github-actions)
- 公共仓库 60 天没有仓库活动，计划工作流会被自动停用；停用时**静默**（没有邮件，Actions 日志里也没有记录）；issue 评论和 star 不算活动；可以在 Actions 页面或用 CLI 重新启用 — [cronuru guide](https://cronuru.com/guides/github-actions-scheduled-workflows)、[runhooks.app](https://runhooks.app/blog/github-actions-scheduled-workflows-unreliable/)（第三方；"静默停用"这一说法未核实）
- 时区：默认 UTC；有第三方称 **2026 年 3 月起**可以在 cron 条目旁加可选的 `timezone:` 字段（IANA 名）— [cronuru: GitHub Actions cron dialect](https://cronuru.com/dialects/github-actions)。**只有这一个来源，未在官方 docs 核实**
- NYSE 使用 America/New_York 时区；常规时段 9:30 到 16:00；提前收盘日包括圣诞前一天、独立日前一天（2025-07-03）、感恩节次日（2025-11-28）— [TradingHours NYSE](https://www.tradinghours.com/exchanges/nyse)、[FXEmpire XNYS](https://fxempire.com/stock-exchanges/xnys)
- 有临时休市的先例（例如飓风 Sandy）— [TradingHours](https://www.tradinghours.com/exchanges/nyse/market-holidays/closed-due-to-hurricane-sandy)

### Inferences
- **"收盘后"任务**：可以继续用 GitHub Actions，但 cron 分钟不要设在 0（例如用 `17 21 * * 1-5`、`17 22 * * 1-5` 两条覆盖 EDT 和 EST），在脚本里用交易所日历判断"今天是否交易日、是否已收盘、是否已经跑过"（幂等），并且一定要配外部的心跳监控（见 Q5）。
- **"收盘前 10 分钟"任务**（规则 A 是"下一交易日收盘买入"，需要接近收盘时执行）：Actions 有 5 到 30 分钟延迟和丢任务的风险，不适合。备选方案：(a) 用券商的 MOC/LOC 收盘竞价单，提前（例如 15:00 ET 前）提交，让执行时刻不依赖调度准点（NYSE、Nasdaq 的 MOC 截止时间需另外核实）；(b) 便宜的 VPS 或家用机，用 systemd timer 加 `TZ=America/New_York`；(c) Actions 多排几个时间点加幂等。
- 交易所日历库：Python 常用 `exchange_calendars`（XNYS）和 `pandas_market_calendars`。它们能处理节假日、提前收盘和 DST（依据训练知识，本次搜索没拿到它们的文档）。Alpaca 也有 `/v2/calendar` 和 `/v2/clock` 接口，可以返回当日开收盘时间（训练知识，未核实）。
- 60 天停用的风险：这个仓库的日报工作流每天都会提交 `reports/`，提交本身算仓库活动，所以一般不会触发停用。但如果哪天数据下载失败、没有产生提交，就可能慢慢累积到 60 天，所以仍然需要心跳监控。

### Gaps
- 没能抓到 GitHub 官方 "Events that trigger workflows" 页面（DNS 失败），60 天停用规则和 `timezone:` 新字段都没有一手确认。
- 没有拿到 `exchange_calendars` 和 `pandas_market_calendars` 的官方文档原文，以及 NYSE 2026、2027 年的官方休市和提前收盘日历。
- VPS 价格（Hetzner、DigitalOcean 等）以及云函数（AWS Lambda + EventBridge Scheduler、Cloud Run Jobs）的定价和时区支持，本轮没有搜索。

## Q4. 存储：提交到仓库的 parquet 缓存 vs SQLite/DuckDB；数据版本化和原始快照

### Takeaway
对约 20 个代码的日线和小时线数据（总量只有几十 MB），**Parquet 文件加 DuckDB 直接查询**就足够了：DuckDB 不用先导入就能读 Parquet，适合回测扫描；交易日志、信号、成交这类逐行写入的数据更适合放 SQLite（DuckDB 还能直接 ATTACH SQLite 文件联合查询）。可复现性靠"按日期保存原始下载快照，加记录内容哈希的清单"，而不是覆盖写入。

### Cited Findings
- DuckDB 不需要导入就能直接读 Parquet；SQLite 没有原生 Parquet 支持，要先导入 — [MotherDuck: DuckDB vs SQLite](https://motherduck.com/learn-more/duckdb-vs-sqlite-databases)、[DataCamp](https://www.datacamp.com/blog/duckdb-vs-sqlite-complete-database-comparison)
- 大数据量的分析型查询（聚合、连接）DuckDB 更快；有索引的简单点查 SQLite 可能更快 — [Analytics Vidhya (2026-01)](https://www.analyticsvidhya.com/blog/2026/01/duckdb-vs-sqlite/)、[MotherDuck](https://motherduck.com/learn-more/duckdb-vs-sqlite-databases)
- DuckDB 是列式存储，单行 UPDATE/DELETE 代价较高；频繁的小写入更适合 SQLite — [Kanaries](https://docs.kanaries.net/ja/topics/DuckDB/duckdb-vs-sqlite)、[chat2db](https://chat2db.ai/resources/blog/duckdb-vs-sqlite)
- 两者都是多读单写；DuckDB 的 ACID 只保证在单进程内 — [chat2db](https://chat2db.ai/resources/blog/duckdb-vs-sqlite)
- DuckDB 可以 ATTACH SQLite 文件直接查询 — [MotherDuck](https://motherduck.com/learn-more/duckdb-vs-sqlite-databases)
- （来源质量提示：这些多是厂商相关的博客，其中一篇的基准数据标注为"示意结果"）

### Inferences
- 本仓库的规定是"原始价格不提交"（CLAUDE.md），可能出于数据条款考虑。可复现性的替代做法：在 Actions 里把原始下载以 Parquet 形式存进 **Actions artifacts 或 cache**，或私有存储（例如私有仓库或 Cloudflare R2/S3），公开仓库只提交"数据清单"：每个代码的行数、首尾日期、最后收盘价和内容 SHA256。这样回测结果出现差异时，可以先确认是不是数据变了。
- 建议采用"追加不覆盖"的布局：`raw/{source}/{YYYY-MM-DD}/{ticker}.parquet` 存当日抓取的快照，`clean/` 存统一复权后的数据。复权数据在除权除息时会整段改写，覆盖写入就丢掉了"当时看到的数据"。
- 信号、委托、成交、持仓对账这类"日志"类数据用 SQLite（或追加写的 CSV/Parquet）。现有的 `portfolio/holdings.csv` 可以保留作为人工维护的真相来源。
- 更重的数据版本化工具（DVC、lakeFS、Git LFS）对这个规模属于过度设计（推断，未搜索）。

### Gaps
- 没有找到个人或小团队交易系统数据版本化实践的一手工程博客。
- GitHub Actions artifacts 和 cache 的保留期与容量上限，本轮没有核实（官方 docs 抓取失败）。

## Q5. 监控和通知：机器人与推送、心跳（死人开关）、信号和成交日志、券商持仓对账

### Takeaway
成熟做法是两层：**(1) 主动通知**（Telegram/Discord/ntfy/邮件/GitHub Issue 评论），告诉你"跑了，结果是什么"；**(2) 被动心跳**（Healthchecks.io 这类死人开关，免费档 20 个检查），在任务"根本没跑"时报警。仅靠第 1 层发现不了 cron 被延迟、丢弃或静默停用。另外每日对账"券商实际持仓 vs 系统预期持仓"是独立的第三道防线。

### Cited Findings
- Healthchecks.io 的模型：每个任务结束时 ping 一个唯一 URL，规定时间窗口内没收到就报警；可以用"周期加宽限期"，也可以用"cron 表达式加时区"定义预期时间 — [crontap blog](https://crontap.com/blog/healthchecks-dead-man-pair-with-scheduler)、[sumguy (self-hosted)](https://www.sumguy.com/healthchecks-self-hosted-cron/)
- 免费云端档 20 个检查；开源、可以自建 — [openalternative](https://openalternative.co/healthchecks)、[cronping alternatives](https://cronping.com/alternatives/healthchecks-io)、[tools.fun (2026)](https://tools.fun/resources/best-free-cron-monitoring)
- 告警渠道包括邮件、Slack、PagerDuty、Webhook 等 — [cronping](https://cronping.com/alternatives/healthchecks-io)
- "调度器只能报告失败的运行，死人开关才能发现没发生的运行"，建议两者搭配（厂商观点）— [crontap](https://crontap.com/blog/healthchecks-dead-man-pair-with-scheduler)
- 也有针对 GitHub Actions 的专门监控服务 — [cronping: GitHub Actions monitoring](https://cronping.com/solutions/github-actions)

### Inferences
- 对本项目的具体建议（推断）：
  1. 在每日工作流最后一步 `curl https://hc-ping.com/<uuid>`，失败时 ping `/fail`；Healthchecks 里设置 cron `30 17 * * 1-5`、时区 America/New_York，宽限期 2 到 3 小时。这一步可以同时发现 Actions 延迟或丢弃、60 天静默停用和数据源故障。注意：节假日不跑也会报警，需要在非交易日也 ping 一次"跳过"，或接受偶尔的误报。
  2. 通知渠道：GitHub Issue 评论适合留档，手机上看不够及时。ntfy（自建或 ntfy.sh 主题，`curl -d` 一行即可）或 Telegram Bot 适合推送"今天有买或卖信号"。Pushover 是一次性付费的推送服务（训练知识，价格未核实）。
  3. 日志：每次运行把"输入数据清单哈希 → 计算出的信号 → 计划委托 → 券商返回的委托 ID 和成交 → 成交后持仓"写成一行（JSONL 或 SQLite），作为交易日志；日报从这份日志生成。
  4. 对账：每天收盘后从券商 API 拉取实际持仓，与 `portfolio/holdings.csv`（人工维护）以及按规则算出的"应有持仓"做三方比对，数量不一致就单独告警。
- 告警只在"有动作或有异常"时发出，否则用户会习惯性忽略（推断）。

### Gaps
- 没有核实 Healthchecks.io 是否原生集成 ntfy 或 Telegram（搜索结果没有提到 ntfy）。
- 没有搜索 ntfy、Pushover、Telegram Bot API 的官方限额和价格。
- 没有找到个人量化系统做"持仓对账"的一手工程文章。

## Q6. 开源"个人交易机器人"参考架构（数据 → 信号 → 下单 → 成交 → 日志 → 报告）

### Takeaway
这次没找到一个文档完整、覆盖到日志和对账的个人系统参考架构。现成的组件是：**Lumibot**（MIT 许可，回测和实盘同一套代码，支持 Alpaca 等券商，官方推荐部署到 Render）和 **QuantConnect LEAN CLI**（本地回测和实盘引擎，但美股数据要付费订阅 Security Master）。日志、对账、报告这几层大多需要自己写。

### Cited Findings
- Lumibot：Python 交易框架，MIT 许可，PyPI 页面提供文档和示例策略，推荐用 "Deploy to Render" 部署（备选 Repl.it）— [PyPI lumibot](https://pypi.org/project/lumibot/)
- Lumibot 配 Alpaca 的入门流程：先开模拟盘账户，再把 API_KEY 和 API_SECRET 写入凭据文件 — [PyPI lumibot](https://pypi.org/project/lumibot/)
- 社区示例 MLTradingBot（Lumibot + Alpaca，基于新闻情绪交易，MIT）— [GitHub fuzzyhead8/MLTradingBot](https://github.com/fuzzyhead8/MLTradingBot)
- LEAN CLI 在本地使用 QuantConnect 美股数据需要 Security Master 订阅和付费组织；数据只能在 LEAN 引擎里用 — [QuantConnect LEAN CLI docs](https://www.quantconnect.com/docs/v2/lean-cli/datasets/quantconnect/key-concepts)
- Alpaca 官方 Python SDK 和相关开源项目集合 — [GitHub topic alpaca-api](https://github.com/topics/alpaca-api)

### Inferences
- 对本项目来说，引入 Lumibot 或 LEAN 的收益有限：规则 A 是日频规则，逻辑很简单，现有的 `src/riskeval/` 加 GitHub Actions 已经覆盖"数据 → 信号 → 报告"。缺的是"下单 → 成交 → 日志 → 对账"这一段。用 `alpaca-py` 直接调用模拟盘 API（提交 MOC/LOC 单、读取订单和持仓）再加 SQLite 日志，比迁移到新框架更轻（推断）。
- 一个最小化的完整流水线示意（推断，供报告撰写者参考）：
  `收盘后 Actions（UTC 两档 cron 加日历判断）→ 拉 Alpaca 日线（yfinance 备份）→ 写 raw 快照和数据清单 → 计算规则 A 信号 → 写 signals 表 → 生成次日计划 → 第二天 ET 15:30 前由 VPS 或家用机（或多次触发的 Actions）提交 MOC 单到模拟盘 → 收盘后拉取成交和持仓 → 对账 → 写 journal → 更新 reports/ → ntfy 或 Telegram 推送 → Healthchecks 心跳`。
- 先在 Alpaca 模拟盘跑 1 到 3 个月，比较"模拟成交价 vs 回测假设的收盘价"，这是验证回测成交假设最便宜的办法（推断）。

### Gaps
- 没有拿到 Lumibot 官方文档中关于部署和日志的细节，也没有核实 Lumibot 最新版本号。
- 没有找到 Alpaca 官方的端到端示例仓库（含日志和对账）的具体链接。
- 没有搜索 NautilusTrader、Backtrader 或 vectorbt 的实盘部署案例。
