# 券商 API、模拟盘与自动下单调研（小资金美股散户，截至 2026-10-20）

> 调研方法说明（重要）：本次调研环境的 WebFetch 和 curl 访问券商、FINRA、GitHub 文档域名都被网络策略拦截（DNS/代理 403），所以下面的事实**全部来自搜索引擎返回的页面摘要**，没有逐页打开原文核对。每条都附了来源 URL；标注"二手来源"的是券商博客或第三方文章，不是官方原文。价格、规则类事实注明了日期。正式依赖前，请到官方页面再确认一次。

## 1. Broker APIs: Alpaca, IBKR, Tradier, Schwab, Futu/moomoo, Tiger

### Takeaway
对"每天收盘后算信号、次日收盘附近用限价单成交、每月几笔、单笔 800–2,400 美元、要买碎股"的需求：**Alpaca** 的模拟盘最容易接入（REST、密钥、免费 IEX 数据、paper 端点和 live 端点分开），但碎股只能用 DAY 订单，不能挂 MOC/LOC。**IBKR** 功能最全（模拟盘、MOC/LOC、全球开户），但碎股是否支持 API 下单，各来源说法矛盾。**Futu/moomoo OpenAPI** 和 **Tiger Open API** 适合用港/新加坡账户的中文用户，两家都有美股模拟盘；但 Tiger 只有 Prime 账户能做碎股，文档里没找到 MOC 订单。**Schwab** 没有模拟盘，refresh token 每 7 天要人工重新登录。**Tradier** 有沙盒模拟盘，但数据延迟 15 分钟。

### Cited Findings

**Alpaca**
- 下 `time_in_force=cls` 加 market 或 limit 类型的订单，就是 MOC 或 LOC 单，只在收盘集合竞价中成交 — [Alpaca Docs: Placing Orders](https://docs.alpaca.markets/us/docs/orders-at-alpaca)
- 碎股单只支持 `time_in_force=day`。Alpaca 的报错指南写明，碎股单用了 DAY 以外的 TIF（比如 GTC）会返回 422 错误 — [Alpaca Learn: Fractional Shares API](https://alpaca.markets/learn/fractional-shares-api)；[Alpaca: How to Fix 30 Common Errors](https://alpaca.markets/learn/how-to-fix-common-trading-api-errors-at-alpaca)
- 碎股已经支持限价单和盘前盘后交易（条件：TIF=day、type=limit、带 limit price、extended_hours=true）。后来又加了碎股按金额（notional）下的 stop、stop-limit 等单型 — [Alpaca Blog: Fractional supports limit orders & extended hours](https://alpaca.markets/blog/fractional-shares-trading-supports-limit-orders-and-extended-hours/)；[Alpaca changelog](https://docs.alpaca.markets/us/v1.1/changelog/support-for-fractional-usd-stop-stop-limit-lct-stop-stop-limit-limit-with-extended-hours-orders)
- 没有找到明确说明"碎股 + cls"组合是否可用的文档。按"碎股只能用 DAY"推断，大概率会被拒（未验证，需要在模拟盘实测） — 同上
- 行情数据：Basic 档免费，paper 和 live 账户默认都是这一档，实时股票数据只有 IEX 一家交易所；REST 历史数据延迟 15 分钟，WebSocket 最多订阅 30 个代码。**Algo Trader Plus 档 $99/月**，覆盖全美所有交易所实时数据（价格日期：搜索摘要，2026 年） — [Alpaca Docs: About Market Data API](https://docs.alpaca.markets/us/docs/about-market-data-api)；[PyQuant News 二手来源](https://www.pyquantnews.com/free-python-resources/alpaca-pricing-plans-compared-python-data-examples-limits)
- 非美国居民开户：Alpaca 早期非美国个人账户是邀请制 beta，最低入金 $30,000，只能国际电汇；后来的公告说取消了这个门槛，"最低 $1 即可入金"。开户流程里要声明非美国税务居民，并签 W-8BEN。**没有找到当前的可开户国家清单**；有资料提到加拿大居民目前不能开户 — [Alpaca Learn: Live Trading Account as Non-US Resident](https://alpaca.markets/learn/live-trading-account-non-us/)；[Alpaca Blog: Non-US live trading beta](https://alpaca.markets/blog/non-us-live-trading-beta/)；[Alpaca Support: Is Alpaca available outside the US](https://alpaca.markets/support/is-alpaca-available-outside-the-us)
- 2026-07 Alpaca 完成了 29 个 EEA 国家的牌照通行（passporting），但这是面向在它上面搭建业务的金融科技公司和机构，不是零售开户 — [BusinessWire 2026-07-07](https://www.businesswire.com/news/home/20260707116782/en/Alpaca-Completes-EEA-Passporting-to-29-Countries-Expanding-Access-to-Regulated-Investment-Services-Across-Europe)

**Interactive Brokers (IBKR)**
- 每个真实账户配一个模拟账户。真实账户的行情订阅可以共享给模拟账户，但同一时间只能在其中一个账户上使用；不订阅的话，模拟盘只能看延迟的 Level 1 数据 — [IBKR Docs: Market Data Sharing](https://www.interactivebrokers.com/docs/general/market-data-subscriptions/market-data-users/market-data-sharing)；[IBKR KB article-1719](https://www.ibkrguides.com/kb/article-1719.htm)；[IBKR Campus: Using the Paper Trading Account](https://www.interactivebrokers.com/campus/trading-lessons/using-ibkrs-paper-trading-account/)
- 要先开一个真实账户（可以不入金）才能拿到完整的模拟账户；IBKR 没有最低入金要求（二手来源） — [brokerlistings 二手来源](https://brokerlistings.com/reviews/interactive-brokers/does-interactive-brokers-have-paper-trading)；[IBKR Campus: Requesting a Paper Trading Account](https://www.interactivebrokers.com/campus/trading-lessons/request-paper-trading-account/)
- MOC/LOC：IBKR 支持这两种单型。Campus 课程写明 Nasdaq 15:55 ET、NYSE 15:50 ET 停止接收 MOC；IBKR 的 MOC 页面要求"至少在收盘前 15 分钟提交" — [IBKR Campus: MOC](https://www.interactivebrokers.com/campus/trading-lessons/ibkr-desktop-market-on-close-order/)；[IBKR Campus: LOC](https://www.interactivebrokers.com/campus/trading-lessons/ibkr-desktop-limit-on-close/)；[IBKR: MOC Orders](https://www1.interactivebrokers.com/en/trading/orders/moc.php)
- **碎股能否通过 API 下单，说法矛盾**：IBKR Campus 页面的评论和 QuantConnect 论坛（旧帖）说碎股"可以走 FIX/CTCI，但目前不能走 API"；TradersPost 博客说通过它的集成可以下碎股。碎股能否用 MOC/LOC，一个来源说"不支持开盘/收盘单型"，另一个（supa.is 2026）说支持 MOC — [IBKR Campus: Fractional Shares](https://www.interactivebrokers.com/campus/trading-lessons/fractional-shares/)；[QuantConnect forum](https://www.quantconnect.com/forum/discussion/12955/fractional-shares-interactive-brokers-margin-account/)；[TradersPost 二手来源](https://blog.traderspost.io/article/the-availability-of-fractional-shares-for-traders)；[supa.is 二手来源](https://supa.is/article/interactive-brokers-fractional-shares-not-available-how-to-enable-permissions-2026)
- 碎股要先在 Client Portal 里开通对应的交易权限 — [IBKR Campus: Fractional Shares](https://www.interactivebrokers.com/campus/trading-lessons/fractional-shares/)

**Tradier**
- 沙盒（sandbox）用模拟资金，支持完整的交易 API；沙盒所有行情延迟 15 分钟，没有延迟版的流式接口 — [Tradier Docs: Trading](https://docs.tradier.com/docs/trading)；[Tradier FAQ](https://docs.tradier.com/docs/faq#/)；[TradersPost Tradier docs 二手来源](https://docs.traderspost.io/docs/core-concepts/brokers/tradier)

**Charles Schwab Trader API**
- 开发者应用要人工审核几天（状态先显示"Approved — Pending"，审核通过后变成"Ready for Use"）。个人权限只能操作自己的账户 — [Medium: Unofficial Guide to Schwab Trader APIs 二手来源](https://medium.com/@carstensavage/the-unofficial-guide-to-charles-schwabs-trader-apis-14c1f5bc1d57)
- access token 约 30 分钟过期；refresh token 从创建起固定 7 天失效，中途刷新也不延长，所以无人值守的程序每周都要人工重新登录一次。Schwab 说以后可能会改，但没给时间表 — [schwabr CRAN README](https://cran.r-project.org/web/packages/schwabr/readme/README.html)；[Lumibot Schwab docs](https://lumibot.lumiwealth.com/brokers.schwab.html)
- Schwab 的 sandbox 是合成数据测试环境，**没有模拟盘模式**（二手来源） — [MyLinedChart 二手来源](https://mylinedchart.com/resources/articles/schwab-api-for-technical-traders-workflow-fit-checklist)

**Futu / moomoo OpenAPI**
- OpenAPI 支持的券商主体有 FUTU HK、moomoo US、moomoo SG。市场表显示美股和 ETF 在各主体都能模拟交易；但 FAQ 的另一张表把 moomoo SG/AU 的美股实盘标为不支持。**两张官方表互相矛盾**，需要问客服确认 — [moomoo OpenAPI Intro](https://openapi.moomoo.com/moomoo-api-doc/en/intro/intro.html)；[moomoo OpenAPI FAQ: Transaction](https://openapi.moomoo.com/moomoo-api-doc/en/qa/trade.html)
- 碎股：只限部分美股和 ETF；只能在常规交易时段下单；只支持当日单（DAY）；最小 0.0001 股，买入至少 $5。美国主体的披露写碎股只能下市价单，新加坡帮助页写市价或限价 — [Moomoo US: Fractional Disclosure](https://www.moomoo.com/us/support/topic4_481)；[Moomoo SG: Fractional](https://www.moomoo.com/sg/support/topic5_755)；[Moomoo AU](https://www.moomoo.com/au/support/topic6_499)
- 没有找到 OpenAPI 是否支持美股 MOC/LOC、碎股单能用哪些单型的明确文档（见 Gaps）

**Tiger Open API（老虎）**
- 美股和 ETF 支持模拟盘和实盘；**碎股只限 Prime 账户**。单型有 MKT、LMT、STP、STP_LMT、TRAIL；AM/AL 竞价单只用于港股。**没有找到美股 MOC/LOC** — [Tiger Open API Docs Intro](https://docs-en.itigerup.com/)；[Place Order](https://quant.itigerup.com/openapi/en/python/operation/trade/placeOrder.html)；[Enumerations](https://quant.itigerup.com/openapi/en/csharp/appendix2/overview.html)
- 碎股的数量用 `quantity` 加 `quantity_scale` 表示；合约信息里有 `support_fractional_share` 字段。模拟账户在盘前盘后可能有额外限制 — [Place Order](https://quant.itigerup.com/openapi/en/python/operation/trade/placeOrder.html)；[Get Contract](https://quant.itigerup.com/openapi/en/python/operation/trade/getContract.html)；[Tiger FAQ Trading](https://quant.itigerup.com/openapi/en/csharp/FAQ/trade.html)

### Inferences
- 用户人在美国以外、写中文，最现实的路线是：已有 Futu/moomoo 或 Tiger 账户就先用它们的 OpenAPI 模拟盘；想要最简单的云端 REST 接入，就用 Alpaca 模拟盘（模拟盘不需要开实盘，注册就能用）。实盘要不要用 Alpaca，取决于用户所在国家能不能开户，当前清单查不到。
- 用户标的里单价 500–1,600 美元的股票，单笔 800 美元只能买碎股。但 Alpaca（碎股只能 DAY）和 moomoo（碎股只能 DAY，美国主体只能市价）都把碎股和收盘竞价单（cls/MOC/LOC）分开了。所以要么整股用 MOC/LOC，碎股用 15:50 前后提交的 DAY 限价单；要么把仓位调到能整股买的大小。
- Schwab 因为每 7 天要人工登录，基本不适合无人值守；Tradier 沙盒数据延迟 15 分钟，对"收盘附近限价"的模拟不真实。

### Gaps
- 无法打开各家佣金和费用页核对：Alpaca 美股免佣、IBKR Pro 每股费率、Futu/Tiger 美股佣金和平台费，都没有拿到 2026 年的官方数字。
- 没有找到 IBKR 新一代 API（IBKR Web API / OAuth 给零售用户）2026 年的状态和限制。
- 没有确认 Alpaca 非美国个人实盘当前开放哪些国家（中国内地、香港、台湾、新加坡等）。
- moomoo/Tiger OpenAPI 的美股 MOC/LOC 支持情况未找到。

## 2. MOC/LOC order types and exchange cutoffs

### Takeaway
NYSE 的 MOC 和 LOC 都在 **15:50 ET** 截止；Nasdaq 的 MOC 在 **15:55 ET** 截止，LOC 可以到 **15:58 ET**（Nasdaq 时间线存在不同版本的说法，见下）。收盘竞价单可以白天任何时间提前挂好，所以"次日收盘成交"不需要卡着 15:50 运行程序。

### Cited Findings
- NYSE：MOC 和 LOC 可以录入到 15:50；之后只允许录入抵消规定失衡（regulatory imbalance）方向的单；15:58 以后拒绝撤单，撤单只限有书面记录的错误 — [NYSE Opening & Closing Auctions Fact Sheet](https://WWW.NYSE.COM/publicdocs/nyse/markets/nyse/NYSE_Opening_and_Closing_Auctions_Fact_Sheet.pdf)；[NYSE Closing Process Fact Sheet](https://www.nyse.com/publicdocs/nyse/NYSE_Auctions_Closing_Process_Fact_Sheet.pdf)
- Nasdaq：MOC 15:55 截止，LOC 可以录入到 15:58，16:00 收盘集合竞价（Closing Cross） — [Nasdaq Closing Cross FAQ](https://www.nasdaqtrader.com/content/productsservices/Trading/ClosingCrossfaq.pdf)；[Nasdaq Open/Close Quick Guide](https://www.nasdaqtrader.com/content/technicalsupport/specifications/TradingProducts/openclosequickguide.pdf)
- 时间线有冲突：Nasdaq 2017 年的说明写 LOC 15:55 截止；2021 年《联邦公报》（Federal Register）上有一份提案，拟把 MOC/LOC 接收延长到 15:59。**没能确认现行版本** — [Nasdaq 2017 Closing Cross Enhancements](https://www.nasdaqtrader.com/content/newsalerts/2017/eta/ClosingCrossEnhancementsFS.pdf)；[Federal Register 2021-07274](https://www.govinfo.gov/content/pkg/FR-2021-04-09/pdf/2021-07274.pdf)
- IBKR 自己要求 MOC 在收盘前至少 15 分钟提交（券商的截止可能比交易所早） — [IBKR: MOC Orders](https://www1.interactivebrokers.com/en/trading/orders/moc.php)
- Alpaca 用 `cls` 表示 MOC/LOC；碎股不能用（碎股只能 DAY） — [Alpaca Docs: Placing Orders](https://docs.alpaca.markets/us/docs/orders-at-alpaca)；[Alpaca Learn: Fractional](https://alpaca.markets/learn/fractional-shares-api)
- Tiger 文档的单型里没有美股 MOC/LOC — [Tiger Enumerations](https://quant.itigerup.com/openapi/en/csharp/appendix2/overview.html)

### Inferences
- 规则 A 可以完整改写成"早上提前挂好的收盘竞价单"，不依赖 15:50 准时运行：
  - **买入**：信号由前一天收盘确定，次日收盘买入就是无条件的 MOC（或宽一点的 LOC）。
  - **卖出**（收盘回到 20 日均线）：MA20 里包含当天收盘价 C。条件 C ≥ MA20 等价于 C ≥ (前 19 日收盘之和 + C)/20，也就是 C ≥ 前 19 日收盘均值。所以可以挂一张 **LOC 卖单，限价设为前 19 个交易日收盘均值**，在收盘竞价中自动满足这条规则。这是代数推导，不是外部来源；收盘竞价价格就是官方收盘价，这一点建议实测确认。
  - **20% 止损**：可以用同样的 LOC 卖单（限价设为 0.8 × 买入价，方向是"跌破才卖"，需要另一张 MOC 单配合条件判断），也可以改用盘中止损单。具体取决于回测里的止损是按收盘价还是盘中价判断，要和回测口径对齐。
- 这个做法只适用于整股。碎股要在 15:45–15:55 之间用 DAY 限价单近似，这时调度的可靠性就成了关键（见第 4 节）。

### Gaps
- 没有拿到 Nasdaq 现行规则手册里 LOC 的确切截止时间，也没有 Alpaca 自己对 cls 单的截止时间（以前有"15:50 后拒绝"的说法，未验证）。
- 没有任何来源说明 moomoo OpenAPI 是否支持美股收盘竞价单。

## 3. Regulatory constraints: PDT, T+1, good-faith violations

### Takeaway
SEC 已于 **2026-04-14** 批准 FINRA 修改 Rule 4210：取消"Pattern Day Trader"认定和 $25,000 最低权益要求，换成新的日内保证金规则，**2026-06-04 生效**，券商最晚 **2027-10-20** 前完成合规（以上都来自二手来源，没能打开 FINRA 原文核对）。所以有的券商可能还在执行旧规则。对这个用户来说，每月几笔、隔夜持仓的策略本来就几乎不涉及日内交易；更要注意的是现金账户 T+1 结算和 good-faith violation（GFV）。

### Cited Findings
- SEC 于 2026-04-14 批准 FINRA Rule 4210 修订（Release No. 34-105226，SR-FINRA-2025-017），取消 PDT 认定、日内交易次数计数和 $25,000 门槛，也取消 4 倍日内购买力，改为 Rule 4210(d)(2) 下的日内保证金要求；FINRA Regulatory Notice 26-10 定 2026-06-04 生效，需要更多时间的券商最晚 2027-10-20 合规（也有来源写批准日是 04-15） — [King & Spalding](https://www.kslaw.com/insights/articles/finra-adopts-sweeping-changes-to-margin-requirements-for-day-trading)；[E*TRADE: PDT Rule Change](https://us.etrade.com/knowledge/library/margin/pattern-day-trading-rule-change)；[TradeZero blog](https://tradezero.com/en-us/blog/the-usd25-000-day-trading-minimum-is-gone-here-s-what-it-means-for-you)；[QuantInsti](https://www.quantinsti.com/articles/finra-pdt-rule-removal-2026/)
- 辩护律师的观点：PDT 规则取消后，FINRA Rule 2130、2270 等日内交易相关的义务仍然有效 — [SECLaw](https://seclaw.com/pattern-day-trader-rule-elimination-defense-view/)
- 美股自 2024-05 起实行 T+1 结算（E*TRADE 的某个页面还写 T+2，已经过时） — [Mudrex](https://mudrex.com/learn/good-faith-violation-gfv-what-it-is/)；[E*TRADE 过时页面](https://US.eTrade.com/knowledge/library/stocks/understanding-cash-account-violations)
- GFV：在现金账户里用未结算资金买入，又在资金结算前把这笔股票卖出。12 个月内累计 3 次，一般会被限制 90 天、只能用已结算资金交易（Schwab：前两次警告，第三次限制）；Fidelity 只要一次 freeride 就限制 90 天；M1 是 4–5 次 — [Schwab SG](https://www.schwab.com.sg/story/understanding-stock-settlement-dates-violations)；[Fidelity](https://www.fidelity.com/webxpress/help/topics/learn_cash_account_trading_freeride_restrictions.shtml)；[M1](https://help.m1.com/en/articles/9331978-what-is-a-good-faith-violation)
- Free riding：没有足够的已结算资金就买入，再卖掉同一只股票来付款。违反 Reg T，通常一次就限制 90 天 — [Hapi](https://help.hapi.trade/en/articles/8976318-cash-account-violations)；[Fidelity](https://www.fidelity.com/webxpress/help/topics/learn_cash_account_trading_freeride_restrictions.shtml)

### Inferences
- 规则 A 的典型场景：卖出 A 股票，资金 T+1 到账；同一天收盘又用这笔钱买 B 股票，B 必须持有到那笔卖出资金结算后再卖，否则就是 GFV。规则 A 的持有期通常有好几天，风险低，但自动化程序最好在下单前检查"已结算现金"（broker API 通常会返回 settled cash 或 non-marginable buying power）。
- 非美国券商（Futu HK、Tiger 等）不一定适用 FINRA PDT 规则，看具体主体的监管辖区（未验证）。

### Gaps
- 没有打开 FINRA Regulatory Notice 26-10 和 SEC 批准令原文；Alpaca、IBKR、moomoo US 等具体在哪天停止执行 PDT，也没有查到。
- 没有拿到 SEC 官方关于 GFV 和 T+1 的投资者公告原文。

## 4. Hosted automation alternatives and scheduling reliability

### Takeaway
GitHub Actions 的 `schedule` 官方就写明高负载时会延迟、整点最忙、负载太高时会丢任务，**不适合卡在 15:45–15:55 这个窗口下单**；适合做"收盘后算信号 → 早上提前挂 MOC/LOC 单"这种对时间不敏感的步骤。要精确定时，可以用外部调度器通过 `repository_dispatch` 或 `workflow_dispatch` 触发 Actions。托管平台方面：QuantConnect 支持 Alpaca、IBKR、Tradier、Schwab 等 20 多家券商的实盘，但要付月费；TradingView 的 webhook 要付费套餐并开启 2FA；Composer 按策略数量收费，各来源报价不一。

### Cited Findings
- GitHub 官方：scheduled 事件在 Actions 高负载时可能延迟，高负载时段包括每个整点；负载足够高时，部分排队任务可能被丢弃。建议改用非整点的分钟（Flutter 文档举的例子是 :40） — [GitHub Docs troubleshooting workflows (GHES 3.14)](https://docs.github.com/es/enterprise-server@3.14/actions/how-tos/troubleshooting-workflows)；[Flutter infra docs](https://flutter.googlesource.com/mirrors/flutter/+/refs/heads/main/docs/infra/Scheduled-Recurring-Tasks.md)
- 社区案例：一个新仓库的每日 cron 延迟了 8–14 小时，还有一天整个丢失（个例，未经 GitHub 证实）；有博客说整点延迟 5–30 分钟（作者经验） — [GitHub Community #201738](https://github.com/orgs/community/discussions/201738)；[DEV Community](https://dev.to/morinaga/four-github-actions-cron-timing-bugs-that-silently-broke-my-daily-pipelines-4935)；[runhooks 博客](https://runhooks.app/blog/github-actions-scheduled-workflows-unreliable/)
- 可以用外部调度器通过 `repository_dispatch` API 触发 workflow，按时性比内置 cron 好 — [crontap 博客](https://crontap.com/blog/github-actions-cron-drift-problem)；[itime.day](https://itime.day/articles/github-actions-cron-delays)
- QuantConnect：支持 20 多家券商实盘，包括 IBKR、Alpaca、Tradier、Charles Schwab、TradeStation；用 Alpaca 交易股票免佣，QuantConnect 的实时数据免费 — [QuantConnect Docs: Alpaca](https://www.quantconnect.com/docs/v2/cloud-platform/live-trading/brokerages/alpaca)；[QuantConnect: Alpaca brokerage](https://www.quantconnect.com/brokerages/alpaca)；[QuantConnect Docs: Tradier](https://www.quantconnect.com/docs/v2/cloud-platform/live-trading/brokerages/tradier)
- QuantConnect 价格有冲突：一篇注明 2026-10-10 核对过的评测写 Researcher 档 $84/月（含 2 个实盘节点）、Team 档 $168/月；其他来源写 Researcher 档 $60/月。没有在官方定价页确认 — [newyorkcityservers 评测](https://newyorkcityservers.com/blog/quantconnect-review)；[newtrading.io](https://www.newtrading.io/quantconnect-review/)
- TradingView：webhook 告警要求开启 2FA；免费 Basic 档不能发 webhook；最低能用的付费档，多数来源说是 Essential，也有说 Plus 或 Pro 的（全是第三方来源） — [TradersPost blog](https://blog.traderspost.io/article/tradingview-webhook-alerts-documentation)；[PickMyTrade](https://blog.pickmytrade.trade/tradingview-plan-you-need-for-webhook-automated-trading/)；[tv-hub](https://www.tv-hub.org/guide/tradingview-alerts-setup)
- Composer 2026 年报价各来源不一致：一个来源（2026-10 读取）写 Starter $0（1 个自动策略）、Advanced $10/月、Pro $32/月（按年付）；其他来源写 $24–40/月。有来源提醒：回测按收盘价成交，低档套餐的再平衡时点可能和回测不一致 — [alphagaindaily](https://alphagaindaily.com/en/blog/composer-ai-trading-review)；[anygen](https://www.anygen.io/showcase/composer-trade-fees/index.html)；[insigtrade](https://insigtrade.com/blog/composer-ai-investing-review-automated-strategies-tested)

### Inferences
- 对规则 A 来说，最稳妥的组合是：收盘后的 Actions 任务计算信号（时间不敏感）；同一个任务或第二天早上的任务直接向券商提交当天的 MOC/LOC 单，比如 Alpaca 的 `cls` 单（整股）；再加一个收盘后的对账任务。这样即使 Actions 延迟几小时，只要在 15:50 前跑完都没问题。
- QuantConnect 和 Composer 要把策略移植到它们的框架里，每月 $10–84 的费用相对 8,000 本金每年 1.5%–12%，成本不低；TradingView 也要付费订阅，而且信号逻辑要用 Pine Script 重写。

### Gaps
- 没有打开 GitHub 公有云版（docs.github.com）的 schedule 文档原文，上面引用的是 GHES 3.14 的同款文字；"公有仓库 60 天无活动会自动停用 scheduled workflow"这一条没有在本轮搜索里核实。
- 没有找到 TradingView 官方定价页、Composer 官方定价页的直接内容。

## 5. Paper trading realism

### Takeaway
各家模拟盘都是"按报价撮合"的简化模型：Alpaca 官方承认不模拟市场冲击、延迟滑点、限价单排队位置、价格改善、监管费和分红；Tradier 沙盒用的是 15 分钟延迟数据；IBKR 模拟盘不订阅行情时只有延迟的 L1 数据。模拟盘里 MOC/LOC 是怎么成交的，各家都没有找到说明，需要实测对比。

### Cited Findings
- Alpaca：模拟盘订单由模拟模型撮合，不完全反映真实供求。官方列出模拟盘**不考虑**的项目：市场冲击、信息泄露、延迟导致的滑点、非可成交限价单的排队位置、价格改善、监管费、分红 — [Alpaca Learn: Start Paper Trading](https://alpaca.markets/learn/start-paper-trading)；[TradersPost: Alpaca Paper Trading 二手来源](https://blog.traderspost.io/article/alpaca-paper-trading)
- Alpaca 模拟盘按当前 NBBO 最优价成交，并有 10% 的概率随机部分成交（二手来源，没能在官方文档里核实） — [TradersPost 二手来源](https://blog.traderspost.io/article/alpaca-paper-trading)
- Alpaca 社区用户反映，模拟盘和实盘环境不同，模拟盘里的滑点不能代表实盘 — [Alpaca Forum](https://forum.alpaca.markets/t/slippage-paper-trading-vs-real-trading/2801)
- Tradier 沙盒全部行情延迟 15 分钟；第三方指出，依赖精确入场条件的策略会按过时报价触发 — [Tradier FAQ](https://docs.tradier.com/docs/faq#/)；[TradersPost: Broker Paper Trading Compared](https://blog.traderspost.io/article/broker-paper-trading-comparison)
- IBKR 模拟盘不订阅行情时只有延迟的 L1 和历史数据，没有逐笔和 L2 — [IBKR Campus](https://www.interactivebrokers.com/campus/trading-lessons/using-ibkrs-paper-trading-account/)；[IBKR KB article-1719](https://www.ibkrguides.com/kb/article-1719.htm)
- Tiger 模拟账户在盘前盘后交易某些品种时有额外限制 — [Tiger FAQ Trading](https://quant.itigerup.com/openapi/en/csharp/FAQ/trade.html)
- moomoo 模拟盘支持限价单和碎股单，股票不能卖空（文章约 4 年前，可能已经过时） — [moomoo Learn: Paper Trading](https://www.moomoo.com/us/learn/detail-how-to-use-moomoo-paper-trading-83143-221170093)

### Inferences
- 规则 A 交易的都是大市值、流动性好的半导体股，单笔几百到两千美元，市场冲击可以忽略。模拟盘和实盘的主要差异会来自：收盘竞价单在模拟盘里是否按官方收盘价成交；碎股单的成交价；分红没有入账（REGN、VRTX 这类长期持仓有影响）。建议模拟盘运行期间，每天把成交价和官方收盘价对比记录，量化这个偏差。

### Gaps
- 没有找到任何券商对"模拟盘里 MOC/LOC 如何成交"的官方说明。
- 没有 Futu/moomoo OpenAPI 模拟盘撮合规则的具体文档。

## 6. API key security for automated jobs

### Takeaway
Alpaca 的交易 API key 能下单、撤单、平仓，但**不能发起出入金**，泄露后的最坏情况是被乱下单，而不是资金被转走。模拟盘和实盘的 key 是分开的。用 GitHub Actions 时应该把 key 放在 Secrets 里，实盘 key 放进带人工审批的 environment；不过 GitHub environment 保护规则的官方文档本轮没有检索到。

### Cited Findings
- Alpaca 官方安全指南：拿到 key 对的人可以提交订单、撤销挂单、平掉持仓、查询组合数据；Direct Trading API 的 key 不能发起 ACH 入金或电汇出金 — [Alpaca Learn: API Key Security Best Practices](https://alpaca.markets/learn/api-key-security-best-practices-for-alpaca-builders)
- Alpaca CLI 建议在 CI 里用环境变量，不要把 key 写进磁盘文件；环境变量里的 key 默认指向模拟盘 — [alpacahq/cli](https://github.com/alpacahq/cli)
- 有第三方文章说 Alpaca 可以创建只读行情、不能下单的受限 key（与官方指南的说法不完全一致，需要到控制台确认） — [trading-strategies.academy 二手来源](https://trading-strategies.academy/archives/48245)；[apispine 二手来源](https://apispine.com/alpaca/authentication)
- Schwab 的 refresh token 7 天失效，每周要人工 OAuth 登录（这对无人值守也算一种安全"闸门"，但会造成运维负担） — [schwabr README](https://cran.r-project.org/web/packages/schwabr/readme/README.html)

### Inferences
- 建议做法：(1) 模拟盘 key 和实盘 key 分开存放（比如 `ALPACA_PAPER_KEY` 放在仓库 Secrets，实盘 key 放在名为 `live` 的 environment 里，并配置 required reviewers，每次实盘下单都要手机上点一下批准，相当于半自动）；(2) 代码里写死 base URL 的切换逻辑，并做单笔金额上限检查（例如单笔不超过 2,400、每天不超过 2 笔），超过就拒绝下单；(3) 下单任务只提交汇总，不在日志里打印 key 或完整的账户信息；(4) 券商侧开启 2FA、关闭不需要的权限（如期权、保证金）。以上是通用的安全实践推断，GitHub 的具体功能需要对照官方文档。

### Gaps
- 没有检索到 GitHub 官方关于 environment protection rules、required reviewers 的文档（以及它们对私有仓库、免费账户的可用性）。
- 没有检索到 IBKR 只读 API 权限设置、Futu/Tiger API 权限分级（如只交易不出金）的官方说明。Futu OpenAPI 需要本地运行 OpenD 网关，Tiger 用 RSA 私钥签名，都没有在本轮核实，不能算作已核实事实。
