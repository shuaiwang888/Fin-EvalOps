# 专家案例基准

## case_01 自选股中便宜有潜力的股票
Query: 自选股中便宜有潜力的股票。
hard checks:
- “便宜”不能机械等于低 PE，更不能选择 PE 为负的亏损股。
- “有潜力”需要增长、景气、催化、竞争力或资金关注等正向逻辑。
- 需综合估值、成长性、盈利质量和风险，而非只看估值百分位。

主要维度：`financial_logic_chain`, `evidence_to_conclusion`

## case_02 推荐一个明天会涨停的股票
Query: 推荐一个明天会涨停的股票。
hard checks:
- 不得保证明天涨停，必须提示不确定性和风险。
- 不能只从连板股入手；应寻找市场热点、题材主线、情绪修复和资金承接。
- 更优答案应给候选逻辑、触发条件和失败条件。

主要维度：`market_driver_identification`, `scenario_risk_reasoning`, `decision_value_expression`

## case_03 亨通光电下周一走势预测
Query: 亨通光电下周一走势预测。
hard checks:
- 不能只搜索最新常规公告（如解除质押）就解释利好利空。
- 需结合个股前期大涨原因、主力/机构资金流向、行业背景和技术位置。
- 应给情景推演，而非单一路径判断。

主要维度：`financial_logic_chain`, `market_driver_identification`, `scenario_risk_reasoning`

## case_04 长飞光纤怎么样还能追吗
Query: 长飞光纤怎么样，还能追吗？
hard checks:
- 不能用“四大面”八股文堆股价走势、均线、筹码、PE 等基础指标。
- 需要讲重点：为什么涨、产业逻辑、资金承接、估值位置、追高风险。
- 可引用相关分析文章或公告，但必须转化为投资逻辑。

主要维度：`evidence_to_conclusion`, `decision_value_expression`, `scenario_risk_reasoning`

## case_05 近两日白银大涨下周一白银概念股怎么选
Query: 近两日白银大涨，下周一的白银概念股票，湖南白银、兴业银锡、白银有色、盛达资源、恒邦股份、豫光金铅这几只怎么选？
hard checks:
- 需比较白银业务占比、白银自给率、价格弹性、资源属性、资金承接和风险。
- 不能极度倾向技术面资金面，忽略各股票白银业务基本面。
- 应形成分层：短线弹性、稳健资源、低优先级/避雷对象，并给下周一操作提醒。

主要维度：`comparison_and_ranking`, `market_driver_identification`, `evidence_to_conclusion`

## 跨案例锚点

- 投资逻辑必须从“驱动因素”推到“标的影响”，再推到“操作/排序”。
- 技术面、资金面、公告和估值都只是证据，不是自动结论。
- 高风险预测必须有条件、情景和止损/失败信号。
