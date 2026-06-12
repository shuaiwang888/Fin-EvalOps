# 专家案例基准

本文件沉淀 `02_stock-diagnosis-and-data-lookup.docx` 中的人工评测知识。评分时先判断用户问题是否与下列案例语义匹配；匹配时，将对应 hard checks 作为核验清单。不要因为答案表面流畅或图表多而放松检查。

## 使用规则

- 语义匹配即可使用，不要求逐字相同。
- hard checks 优先于泛化表述：违反 hard checks 时，应在相关维度扣分并按需触发质量标签。
- 专家文档的核心结论：诊股查数的好答案不仅要查对数，还要有多周期连续性、多维扩展性、市场常用框架和增量信息。
- 本文件只评价最终回答呈现出的质量，不评价过程路径、调用策略或耗时。

## Case 1: 同花顺上市以来每年分红

hard checks:
- 必须覆盖上市以来每年分红记录，年份、分红方案、股权登记/除权除息/派息口径应清楚。
- 若只问“每年分红”，核心是完整序列和准确口径；延伸分析不是必要但可加分。
- 简单分红查询若最终回答缺少完整年份序列或关键日期口径，应按数据覆盖和时间口径扣分。

主要维度：`data_accuracy_coverage`, `time_caliber_precision`, `result_verifiability`

## Case 2: 同花顺和东方财富分红总额对比

hard checks:
- 必须同口径计算两家公司分红总额，说明统计区间和币种/单位。
- 应给出总额差异，而非只分别列分红记录。
- 可视化分析是明确加分项，但不能替代准确总额和差距。

主要维度：`calculation_comparison`, `presentation_visualization`, `data_accuracy_coverage`

## Case 3: 同花顺和东方财富过去 5 年每年涨跌幅对比

hard checks:
- 必须给出过去 5 年每年两家公司涨跌幅，说明起止价格口径。
- 好答案应计算每年两者涨跌幅差距，并指出相对强弱年份。
- 可视化是加分项，但专家更重视差距计算和贴近用户需求的延伸分析。

主要维度：`calculation_comparison`, `presentation_visualization`, `insight_extension`

## Case 4: 仕佳光子主要客户

hard checks:
- 主要客户可能不在常规结构化数据中，不能因为最终答案未列出就用泛化描述替代。
- 应尽量给出公告、年报、招股书、调研纪要、券商研报、互动易或产业链资料中的可验证线索。
- 若仍无法确认，应说明数据缺口和可验证来源边界，不得编造客户。
- 专家判断：基本面分析大量依赖非公开或非结构化资料，缺少来源边界会造成数据覆盖和可验证性缺口。

主要维度：`data_accuracy_coverage`, `result_verifiability`, `insight_extension`

## Case 5: 兴业银行什么时候分红

hard checks:
- 用户未限定时间时，大概率问今年或最新分红；应先回答最近一次已确定分红事件，再说明最新年度/2025 年分红进展。
- 必须区分预案、股东大会通过、股权登记日、除权除息日和派息日。
- 模糊问句处理正确可以视为高质量；不应机械追问。

主要维度：`intent_fulfillment`, `time_caliber_precision`, `data_accuracy_coverage`

## Case 6: 内外盘原油比价与布油 120 美元时国内原油期货价格

hard checks:
- 必须处理国际油价、国内原油期货、汇率、计量单位、合约、税费/运费/品质差、基差等口径。
- 若测算会用到汇率，应查询或明确当前汇率，而不是只使用经验值。
- 必须说明内外盘价差和传导关系，不清楚专业业务知识会导致框架扣分。
- 情景测算要给公式和敏感性，而非单一拍脑袋数值。

主要维度：`analysis_framework_fit`, `time_caliber_precision`, `calculation_comparison`, `result_verifiability`

## Case 7: 新奥股份 4 月 10 日有主力进场吗

hard checks:
- “主力”至少有两层含义：大资金和大的游资/席位。
- 应检查资金流、成交量价、龙虎榜、知名游资席位、异常交易等证据。
- 只从资金数据回答是不完整的；只谈席位不看资金也不完整。
- 必须锚定 4 月 10 日及前后交易日，不要泛化成近期。

主要维度：`analysis_framework_fit`, `data_accuracy_coverage`, `time_caliber_precision`, `insight_extension`

## Case 8: 春秋电子筹码集中度

hard checks:
- 市场常用框架是股东户数变化、大股东持股比例、机构持仓、筹码分布和集中趋势。
- 仅查询“集中度90”这类冷门/难解释字段，不能视为好答案。
- 应解释筹码集中度变化对流动性、控盘、波动和风险的含义。

主要维度：`analysis_framework_fit`, `data_accuracy_coverage`, `insight_extension`

## Case 9: 英威腾未来增长点有哪些

hard checks:
- 增长点应聚焦业务边际变化：客户突破、市占率提升、新增订单、新产品放量、海外/新领域突破等。
- 公司业务优秀、产品线丰富、历史优势是存量信息，不等于增长点。
- 调研纪要、研报、订单信息、客户信息等非结构化资料非常关键。
- 好答案应总结增长点优先级和验证指标。

主要维度：`analysis_framework_fit`, `insight_extension`, `data_accuracy_coverage`, `result_verifiability`

## Case 10: 300207 股票 9:30 到 9:45 之间买入多少及卖出多少

hard checks:
- 用户要求分钟区间买入/卖出金额，应使用分时、逐笔或资金流区间数据口径。
- 如果无法取得对应粒度数据，应明确说明限制，不能用日线成交额或全天买卖额替代。
- 未给出该区间明细属于严重数据覆盖和日内精度问题。

主要维度：`time_caliber_precision`, `data_accuracy_coverage`, `result_verifiability`

## Case 11: 粤传媒乖离率

hard checks:
- 好答案应给出多个常见周期的乖离率，如 5 日、10 日、20 日、60 日等，并说明计算口径。
- 需要解释正负乖离、偏离程度和可能含义，而不是只给单个数值。
- 周期越多不是越好，必须围绕用户可理解的技术分析框架组织。

主要维度：`data_accuracy_coverage`, `analysis_framework_fit`, `insight_extension`

## Case 12: 黄金价格

hard checks:
- 必须明确价格品种和口径：现货黄金、COMEX、沪金、人民币/克、美元/盎司等。
- 用户未限定时，应给主流口径并说明差异，必要时给多个市场价格。
- 最新价格必须注意时效，过期价格应扣分。

主要维度：`time_caliber_precision`, `data_accuracy_coverage`, `presentation_visualization`

## Case 13: A 股开户数一览

hard checks:
- 必须说明数据口径：新增投资者数量、期末投资者数量、自然人/机构、月份或年度。
- 应给出时间序列和来源，不能只给单个点。
- 若最新数据有滞后，应说明披露频率和最新可得月份。

主要维度：`data_accuracy_coverage`, `time_caliber_precision`, `result_verifiability`

## Case 14: 目前国内新能源车渗透率

hard checks:
- “目前”需要最新月度或最近披露口径；应标明数据月份。
- 必须区分零售渗透率、批发渗透率、乘用车/汽车整体、新能源乘用车等口径。
- 好答案应给趋势和最近同比/环比，避免只给一个无来源数字。

主要维度：`time_caliber_precision`, `data_accuracy_coverage`, `insight_extension`

## Case 15: 2026 年 3 月单月涨幅跑赢沪深 300 的行业板块

hard checks:
- 必须列出所有跑赢沪深 300 的行业板块，并按涨幅降序。
- 应说明行业分类口径和 2026 年 3 月单月起止交易日。
- 加分项：列出板块中标志性成分股表现并给出简短分析。
- 只列板块虽可完成基本任务，但洞察性弱于补成分股和原因。

主要维度：`calculation_comparison`, `data_accuracy_coverage`, `insight_extension`, `presentation_visualization`

## Case 16: 瑞尔特止盈位

hard checks:
- 用户问止盈位，不能只给一个价格。
- 应给出止盈逻辑：技术压力位/均线/前高、基本面催化、风险收益比、仓位策略、持仓成本和投资周期。
- 如果缺少用户成本/周期，应提出需要补充信息，同时给出分层参考方案。
- 好答案应提醒可进一步制定具体止盈计划。

主要维度：`analysis_framework_fit`, `insight_extension`, `intent_fulfillment`

## Case 17: 张雪机车

hard checks:
- 用户只输入实体/热词时，应识别可能的概念股、事件主体或关联标的需求，而不是等用户明确说“概念股”。
- 需要先确认实体含义，再给相关标的、关联逻辑和证据边界。
- 若实体歧义较强，应说明假设或追问。

主要维度：`intent_fulfillment`, `analysis_framework_fit`, `data_accuracy_coverage`

## Case 18: 沪深 A 股，一个月前上市，今日涨幅超过 7%，非 ST 非科创

hard checks:
- “在一个月前上市”通常表示上市时间早于一个月前或至少上市满一个月，不能解析为上市日期刚好等于一个月前那一天。
- 必须正确处理沪深 A 股、非 ST、非科创、今日涨幅超过 7% 等条件。
- 若实际存在符合标的却输出无结果，应触发硬性数据/条件解析错误。

主要维度：`intent_fulfillment`, `data_accuracy_coverage`, `time_caliber_precision`, `result_verifiability`

## Case 19: 连续 500 根 K 线收盘价大于 10 元的股票

hard checks:
- “连续 500 根 K 线”必须检查连续性和 500 根样本，不能只检查最新一个交易日。
- 若无法完整覆盖 500 根样本，必须说明限制并避免给确定结果。
- 只用短周期样本或单日条件替代连续 500 根 K 线，应视为数据覆盖和可验证性硬伤。

主要维度：`data_accuracy_coverage`, `time_caliber_precision`, `result_verifiability`

## Case 20: 长江电力连续 5 年蓄能电量

hard checks:
- 这类上市公司企业宏观经营数据可能不在常规结构化库中，应引用公告、社会责任报告、年报、行业报告或券商研报等可验证来源。
- 可通过研报和公开资料测算推理，但必须标明估算口径和来源。
- 不能因答案缺少直接数据就用泛化业务描述替代。

主要维度：`data_accuracy_coverage`, `result_verifiability`, `insight_extension`

## Case 21: 5 月 6 日前 5 日股价一共涨幅大于 10%

hard checks:
- “前 5 日”在股价语境下应优先理解为前 5 个交易日，不是包含假期的自然日区间。
- “一共涨幅”要求累计区间涨幅，不是某一天涨跌幅。
- 五一假期等非交易日必须从交易日历中排除。
- 时间推移错误会导致筛选结果整体失效，应触发 `time_or_caliber_error`。

主要维度：`time_caliber_precision`, `calculation_comparison`, `data_accuracy_coverage`

## 跨案例判分锚点

- 数据正确只是及格线。专家更看重多周期连续性、多维扩展、市场常用框架和贴近用户真实需求的增量分析。
- 简单事实题：准确、完整、口径清楚。
- 对比题：必须给差异、排序、强弱和口径；图表是加分，不是核心替代品。
- 诊断题：必须把字段转译为市场判断。主力、筹码、增长点、止盈位都有特定市场框架。
- 非结构化资料题：客户、增长点、企业经营数据、调研纪要不能只写成无法验证的泛化结论。
- 条件查询题：条件解析错误、时间推移错误、样本覆盖不足、空结果不复核是主要硬伤。
- 模糊问句：应合理推断用户最可能意图并说明假设，不能机械回避。
