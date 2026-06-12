# 专家案例基准

本文件沉淀人工评测文档和截图中的高频判分锚点。评分时先判断用户问题是否与下列案例语义匹配；匹配时，将对应 hard checks 作为证据核验清单。不要因为答案表面流畅、图表多或链路复杂而放松检查。

## 使用规则

- 语义匹配即可使用，不要求用户问题逐字相同。
- hard checks 优先于泛化表述：如果答案违反 hard checks，应在相应维度扣分并按需触发封顶规则。
- 截图里的好答案共同点：开头明确结论，列关键数据表，命中公告/官方披露原文，把财务数字转译为业务原因，并给出持续性或投资影响。
- 截图里的坏答案共同点：只做结构化财务字段分析，遗漏公告全文或特殊事件；逻辑自洽但答非所问；数字很多但没有主因；股价判断主观且缺少验证指标。

## Case 1: TCL 科技光伏业务对一季报影响

hard checks:
- 必须量化影响大小，如收入贡献约 15%、TCL 中环亏损约 16.47 亿元、环比减亏约 52.8% 等关键锚点。
- 需要区分集团整体盈利和光伏链条拖累，说明光伏亏损是否被半导体显示等业务覆盖。
- 坏回答模式：说"很难精确量化"但不给占比、亏损额或情景测算。

主要维度：`report_data_accuracy`, `causal_attribution_depth`, `business_financial_linkage`

## Case 2: 华润微 2025 利润为负、2026Q1 大增

hard checks:
- 必须纠正用户前提：2025 年并非全年亏损，归母净利润约 6.61 亿元。
- 必须拆解 Q1 大增的主因：非经常性损益/公允价值收益约 1.85 亿元 + 主业复苏。
- 解释应收敛到"大增的质量和可持续性"，不能散列多个原因。

主要维度：`intent_understanding`, `report_data_accuracy`, `causal_attribution_depth`

## Case 3: 中芯国际 2026Q1 快报市场预期

hard checks:
- 必须给出公司指引与市场一致预期的数字锚点，如营收环比持平、毛利率 18%-20%、彭博一致预期约 25.2 亿美元。
- 需要机构观点摘要与预期差判断，而非只讨论预期来源。
- 坏回答模式：缺失关键数字基准，用户无法判断业绩是否超预期。

主要维度：`report_data_accuracy`, `primary_evidence_quality`, `forward_investment_judgment`

## Case 4: 阳光电源一季报与股价影响

hard checks:
- 必须抓住"同比承压、环比修复"框架。
- 需要量化归因：沙特高基数、汇兑损失超 4 亿、财务费用约 3.28 亿元同比大增等。
- 股价影响应结合公告后数日走势复盘，而不是只说利好利空。

主要维度：`causal_attribution_depth`, `business_financial_linkage`, `forward_investment_judgment`

## Case 5: 五粮液 2025 年报和 2026Q1 利好利空

hard checks:
- 必须识别 2025 年报的核心是会计追溯调整 + 行业去库存，不是普通业绩波动。
- 需对比调整前后数据，如归母净利从约 215 亿调至 89.54 亿、调整后低基数带来 Q1 高增。
- 2025 年报和 2026Q1 应分别定性：前者重大利空，后者相对利好但含低基数和回购因素。

主要维度：`primary_evidence_quality`, `causal_attribution_depth`, `forward_investment_judgment`

## Case 6: 德福科技年报对股价利多利空

hard checks:
- 好答案要同时覆盖利多和利空：营收增长、扭亏为盈 vs 净利率约 0.9%、负债率约 72.76%、经营现金流为负。
- 可加分项：用净利率敏感度说明股价对价格或毛利率极度敏感。
- 股价判断不能只看盈利转正，要说明利润质量和现金流压力。

主要维度：`report_data_accuracy`, `causal_attribution_depth`, `forward_investment_judgment`

## Case 7: 300072 年报和一季报

hard checks:
- 必须识别业务主线，如生物能源业务爆发式增长、SAF/HVO 等具体驱动。
- 好答案应把财报数据讲成业务故事，而非只列指标。
- 结构清晰和叙事可读性是重要加分项。

主要维度：`business_financial_linkage`, `causal_attribution_depth`, `composition_credibility`

## Case 8: 科力远年报利空利好及下周走势

hard checks:
- 必须给出年报偏利好但有隐忧的双面判断：收入、利润、扣非改善 vs 毛利率、负债率、利润质量压力。
- 好答案截图特征：结合技术面给出三种情景推演，并给出 MA20/MA60 支撑等观察位。
- 坏答案模式：主观预测下周走势，没有用当前价格、均线、量能或利好兑现程度支撑。

主要维度：`forward_investment_judgment`, `report_data_accuracy`, `composition_credibility`

## Case 9: PCB 扩产对大族激光业绩影响

hard checks:
- 必须量化 PCB 设备业务占比和敏感度，如 PCB 设备收入约 57.73 亿，占总收入约 30.8%。
- 好答案截图特征：给出可复核情景测算，PCB 设备收入 +10%/+20%/+30% 对营收拉动约 +3.08/+6.15/+9.23 个百分点。
- 必须说明利润端不能简单同比例放大，受毛利率、费用、汇兑、验收节奏影响。

主要维度：`report_data_accuracy`, `causal_attribution_depth`, `forward_investment_judgment`

## Case 10: 南方精工 2025 年报和 2026Q1 差异

hard checks:
- 必须锁定非经常性损益是主因，特别是 2025 年泛亚微透公允价值变动收益约 3.10 亿元。
- 需要说明 2026Q1 非经常性损益约 -2492 万元如何抹平归母利润。
- 好答案可以从财报数据或搜索信息切入，但必须用具体数字证明差异。

主要维度：`causal_attribution_depth`, `report_data_accuracy`, `primary_evidence_quality`

## Case 11: 陕国投 A 一季度营收同比下降

hard checks:
- 必须拆解到具体科目同比变化金额，并排序主要拖累。
- 专家认可锚点：投资收益同比减少约 1.68 亿元是最大拖累，并可用现金流量表验证。
- 坏回答模式：只引用监管新规、减费让利等官方口径，未回答哪个科目拖累最大。

主要维度：`causal_attribution_depth`, `report_data_accuracy`, `composition_credibility`

## Case 12: 江苏国信一季度净利润下降

hard checks:
- 必须解释火电行业特性：电价下行 + 煤价未同步下降导致毛利率挤压。
- 好答案需要具体电价下滑百分比、成交电量变化等外部或公司披露数据。
- 只说"增收不增利"或只谈成本波动不够。

主要维度：`business_financial_linkage`, `primary_evidence_quality`, `causal_attribution_depth`

## Case 13: 华天科技净利润大增但偿债能力降低

hard checks:
- 必须同时解释利润端修复和偿债端恶化：短期借款、应付账款、存货等扩张。
- 专家认为两类答案都不够好的原因：光说数据，没有解释为什么负债扩张或扩产节奏导致偿债能力下降。
- 合格答案应连接重资产扩产、现金流/应收错配和利润质量。

主要维度：`causal_attribution_depth`, `business_financial_linkage`, `report_data_accuracy`

## Case 14: 马应龙一季度经营现金流同比增长

hard checks:
- 必须命中公司一季报官方披露：本部应收票据到期兑付较上年同期增加。
- 截图中的坏回答：营收、利润、应收、存货、应付拆得很细，但没有点出官方根本原因。
- 可辅助解释营运资本和回款节奏，但不能替代官方披露锚点。

主要维度：`primary_evidence_quality`, `causal_attribution_depth`, `tool_usage`

## Case 15: 先导基电营收大涨但利润亏损

hard checks:
- 必须拆解增收不增利：毛利率大幅下滑、高研发投入、股份支付拖累。
- 好答案应说明扣除股份支付后的盈利情况，并给出具体金额或比例。
- 需要给后续观察指标，如毛利率是否企稳、股份支付影响是否减弱。

主要维度：`causal_attribution_depth`, `report_data_accuracy`, `forward_investment_judgment`

## Case 16: 北方导航不提升毛利率

hard checks:
- 必须反驳"低价引市场再配套收费"假设，核心原因是军品成本加成定价机制与成本端压力。
- 好答案截图特征：引用材料及燃动成本占比从 86.44% 升至 89.09%、成本增速 72.62% 高于收入增速 52.56%、毛利率降至 15.68%。
- 需要解释军品价格由军方/兵器集团核定，公司无自主提价权。

主要维度：`primary_evidence_quality`, `business_financial_linkage`, `causal_attribution_depth`

## Case 17: 中谷物流一季报毛利率好且能否维持

hard checks:
- 必须用营收和营业成本对比解释毛利率提升：营收约 +0.38%，营业成本约 -9.88%。
- 需要判断成本下降驱动是否可持续，结合运价/附加费、燃油成本等因素。
- 坏回答模式：只泛泛说成本因素，没有量化拆解成本端改善。

主要维度：`report_data_accuracy`, `causal_attribution_depth`, `forward_investment_judgment`

## Case 18: 江波龙一季度毛利率能否保持

hard checks:
- 必须把毛利率拆成存储超级周期、低价库存、结构升级等驱动，并尽量量化贡献。
- 需要行业背景数据，如 DRAM 合约价 Q1 环比涨 90%-95%、NAND 涨 55%-60%。
- 只用江波龙财务数据而没有存储价格周期背景，归因深度不足。

主要维度：`primary_evidence_quality`, `business_financial_linkage`, `forward_investment_judgment`

## Case 19: 铜陵有色归母与扣非差距

hard checks:
- 必须精确解释差额构成：套期保值亏损、境外分红补税、其他收益对冲等。
- 专家锚点：10.46 亿元差距可由"套期保值亏损 16.12 亿 + 境外分红补税拖累 9.52 亿 - 其他收益对冲 5.66 亿"闭合。
- 坏回答模式：只指出公允价值变动约 -17.06 亿，未拆解税务补缴和传导机制。

主要维度：`causal_attribution_depth`, `report_data_accuracy`, `business_financial_linkage`

## Case 20: 寒武纪高股价与营收市值差异

hard checks:
- 必须量化估值极端程度，如市盈率约 263 倍 vs 英伟达 50-60 倍、市销率约 86 倍 vs 英伟达约 12 倍。
- 需要拆解成长股定价、从 0 到 1 爆发期、国产 AI 芯片稀缺性溢价。
- 横向同业估值锚缺失时，"到底多贵"判断不足。

主要维度：`report_data_accuracy`, `business_financial_linkage`, `forward_investment_judgment`

## Case 21: 一汽解放官网年度分红方案

hard checks:
- 必须回答每 10 股派 0.45 元，并给出分红总额约 221,457,643.87 元及计算基数。
- 官网公告/分红公告全文是关键来源，只有摘要或每股股利不完整。
- 简单事实题也要求结论完整、口径清楚。

主要维度：`primary_evidence_quality`, `report_data_accuracy`, `intent_understanding`

## Case 22: 招商积余经营现金流为负 20 亿

hard checks:
- 必须给出精确数据，如经营现金流约 -20.20 亿元，并说明发生了什么。
- 好答案要结合官方解释，如非住宅回款放缓、付款节奏等，而不是只做现金流科目勾稽。
- 用户问"发生了什么"时，公司业务语境比公式更重要。

主要维度：`primary_evidence_quality`, `causal_attribution_depth`, `business_financial_linkage`

## Case 23: 泸州老窖收入确认核算方式

hard checks:
- 必须给出核心口径：控制权转移时点法。
- 好答案还要给出按时点确认收入占比约 99.8%，并说明不同销售模式的确认条件。
- 只回答通用会计政策，未落到公司财报附注，完整性不足。

主要维度：`primary_evidence_quality`, `report_data_accuracy`, `composition_credibility`

## Case 24: 五粮液 ROE 下降且财报真实吗

hard checks:
- 必须捕捉核心事件：收入确认政策变更/前期会计差错更正导致追溯调减利润。
- 必须结合审计意见回应财报真实性，区分"真实合规"与"调整幅度引发争议"。
- 坏回答截图特征：只从 ROE 分子/分母、净利率、周转率公式解释，完全未触及 2026 年刚发生的特殊事件。

主要维度：`primary_evidence_quality`, `causal_attribution_depth`, `business_financial_linkage`

## Case 25: 亿道信息消费电子低迷下营收净利高增

hard checks:
- 必须识别增长主因是业务结构区别于传统消费电子周期，如加固终端、AIoT 等。
- 更好答案要量化业务结构变化如何传导到净利高增。
- 只说"景气脱钩"或结构化归纳但无传导数据，均不算优秀。

主要维度：`business_financial_linkage`, `causal_attribution_depth`, `report_data_accuracy`

## Case 26: 五粮液三季报 600 亿但年报 400 亿

hard checks:
- 必须识别用户真实指向：五粮液 2025 年前期会计差错更正，追溯调减前三季度营收。
- 好答案截图特征：给出调整前 609.45 亿 vs 调整后 306.38 亿，说明收入确认政策变化。
- 坏回答截图特征：用累计 vs 单季、营收 vs 净利、误读其他年份等常规方法论解释，完全答非所问。

主要维度：`intent_understanding`, `primary_evidence_quality`, `causal_attribution_depth`

## Case 27: 五粮液一季报收入确认核算方式

hard checks:
- 必须回答控制权转移时点。
- 好答案要把该口径与前期会计差错更正/新收入确认口径关联，说明这是更正后的公司特定背景。
- 只给教科书式标准回答，缺少公司背景，扣 `business_financial_linkage`。

主要维度：`primary_evidence_quality`, `business_financial_linkage`, `composition_credibility`

## Case 28: 万向钱潮 Q1 净利润下降对股价影响

hard checks:
- 合理结论是短期偏空但非毁灭式，需说明已反映程度和基本面质量。
- 好答案要挖掘积极信号，如毛利率逆势提升至约 22.52%，并提出"利空出尽"观察框架。
- 只聚焦风险、不做辩证分析，投资指导性不足。

主要维度：`forward_investment_judgment`, `causal_attribution_depth`, `composition_credibility`

## Case 29: 华润置地投资性房地产评估减值是否充分

hard checks:
- 必须抓住公允价值模式下不计提传统减值的核心。
- 需要说明近三年无减值、整体增值，并最好给出增值金额数据。
- 概念辨析、方法论和验证证据链均可加分。

主要维度：`report_data_accuracy`, `primary_evidence_quality`, `causal_attribution_depth`

## Case 30: 岩山科技经营现金流负、投资现金流正

hard checks:
- 必须根据财报说明投资现金流正的根本原因：赎回大量交易性金融资产/理财产品，资金回到账上。
- 经营现金流为负要结合公司实际，如 AI 业务投入、转型期、回款和营运资金占用。
- 坏回答截图特征：停留在资产负债表科目变化，没有接上公司实际情况；好答案直接点出赎回投资和业务转型。

主要维度：`primary_evidence_quality`, `business_financial_linkage`, `causal_attribution_depth`

## 跨案例判分锚点

未命中具体案例时，仍按以下锚点评估：

- **好回答必须有结论锚点**：开头明确回答利好/利空、原因、影响大小、是否真实、能否维持或后续怎么看。
- **数字不是越多越好**：关键是数字能闭合主因，如差额拆解、收入占比、利润拖累、敏感度、估值对标。
- **公告全文优先级高于泛化推理**：季报已写明原因时，不能用应收/存货/应付的推理替代官方披露。
- **特殊事件是高危点**：会计差错更正、收入确认政策变化、套期保值、税务补缴、股份支付、公允价值变动、分红方案、审计意见必须主动核验。
- **业务解释要穿透报表**：优秀答案会说明价格、成本、订单、产品结构、行业机制和公司战略如何传导到财务指标。
- **股价影响要可验证**：用公告后走势、估值、市场预期、支撑位、观察指标和情景推演，不要给单向主观预测。
- **问财式常见弱点**：结构化取数强，但公告全文、非结构化披露、特殊事件识别和行业背景检索不足；评测时要据此检查 `tool_usage` 和 `primary_evidence_quality`。
