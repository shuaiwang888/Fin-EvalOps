# 工具列表

| 工具 | 功能 | 详细规则 |
|---|---|---|
| Search | 搜索交易规则、公告、新闻、公开资料、公司事件、市场解释等非结构化数据 | [search.md](search.md) |
| FinQuery | 获取标的相关的结构化金融数据，包括行情、财务、资金、事件、筛选条件等 | [finquery.md](finquery.md) |
| CustomerServiceFAQ | 获取同花顺 APP、账户权限、交易规则、撤单、客服类说明 | [customerservicefaq.md](customerservicefaq.md) |
| AccessingFullText | 根据网址 url 获取网页完整文本，用于公告、规则文件、研报或长文深度阅读 | [accessingfulltext.md](accessingfulltext.md) |
| BackTest | 个股事件回测、交易策略回测等 | [backtest.md](backtest.md) |
| Forecast | 基于多维预测因子进行标的预测和诊断 | [forecast.md](forecast.md) |
| SaveUserProfile | 保存用户偏好、持仓、风险偏好或财务背景信息 | [saveuserprofile.md](saveuserprofile.md) |
| SearchImage | 搜索相关图片 | [searchimage.md](searchimage.md) |
| CodeInterpreter | Python 3 沙箱解释器，用于数据处理、科学计算和可视化 | [codeinterpreter.md](codeinterpreter.md) |

## 07 交互澄清补充规则

评分时根据实际 `tools` 清单和 `chain` 调整，不能机械要求所有工具都出现。

### Search

适合：
- 科创板盘后交易规则、北交所权限、国债逆回购计息、分红税费、撤单时间等规则核验；
- 最新公告、业绩预告、季报、公司事件；
- 用户问题中带有“最新、今天、最近、目前”等强时效表达时补充公开资料。

扣分点：
- 需要规则核验却未搜索；
- 搜索到资料但没有进入最终答案；
- 引用旧资料解释最新问题；
- 把传闻或非权威来源当确定规则。

### FinQuery

适合：
- 个股行情和技术位、候选股筛选、资金流、股息率、财务指标；
- 错别字标的、异常代码、同音简称的候选确认；
- 用户补充持仓、成本、股票后，核验标的现价和基础行情。

扣分点：
- 错别字/异常代码只信单次结果；
- 筛选条件口径不透明；
- 查询时间窗与问题不匹配；
- 查到了行情但没有用于回本、止盈、加仓或风险方案。

### CustomerServiceFAQ

适合：
- 撤单失败、权限开通、ETF/科创板/北交所规则、交易时间；
- 同花顺产品入口、账户功能、交易操作说明。

扣分点：
- 客服规则问题不用规则类工具；
- 答案把规则说错；
- 工具结果与最终答案冲突。

### AccessingFullText

适合：
- 业绩预告、正式季报、分红公告、交易规则文件等需要原文的场景；
- Search 摘要不足以确认关键限制或日期时。

扣分点：
- 只用摘要导致关键事实错漏；
- 全文读取后没有提取核心条款或公告口径。

### BackTest / Forecast

交互澄清中通常不是首选。只有用户明确要求历史统计、回测或预测模型时才适用。若用户要求“年底翻倍”“涨到目标价”，不能把 Forecast 输出当确定结论，必须保留假设、风险边界和不确定性。

### SearchImage

用于用户提供图像或需要图像证据的场景。07 文档本身的图片批注用于评测参考，不代表被评测模型必须调用 SearchImage。

### SaveUserProfile

适合长期用户偏好、持仓、风险偏好等记忆场景。若输入链路显示用户长期信息可用但未使用，可作为 `context_continuity` 或 `tool_usage` 证据。

### CodeInterpreter

适合复杂计算、筛选后复核、表格处理。普通交互澄清不应滥用；若只是简单规则纠错或首轮澄清，过度使用可作为效率扣分证据。
