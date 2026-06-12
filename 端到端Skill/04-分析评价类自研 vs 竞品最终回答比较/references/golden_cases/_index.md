# 专家案例基准

本文件沉淀人工精标文档中的高频评判锚点。评分时先判断用户问题是否与下列案例语义匹配；匹配时，将对应 hard checks 作为核验清单。不要因为答案表面流畅、指标很多而放松这些检查。

## 使用规则

- 语义匹配即可使用，不要求用户问题逐字相同。
- hard checks 优先于泛化表述。违反 hard checks 时，应在相应维度扣分并按需触发质量标签。
- 专家强调“用户是为了交易决策，不是为了学习知识”。消息面、题材和归因问题尤其要检查时效与交易价值。
- 若案例指出需要特殊资料来源，如调研纪要、研报全文、专业数据库，应检查最终回答是否使用或至少识别来源缺口。

## Case 1: 算力租赁板块为什么上涨

hard checks:
- 必须找到并解释真正的关键催化，例如近期政策、服务器价格变化、算力租赁价格或租金涨幅。
- 不能只做“算力需求增长、AI 发展”的泛泛解释。
- 好答案要把消息和价格/供需变化如何传导到板块上涨讲清楚，最好有量化信息。
- 截图专家特别强调：政策、产业链供需、服务器涨价/租金涨幅三类信息应合并成上涨解释；只给宽泛背景或长篇低密度信息，应明显扣分。

主要维度：`evidence_source_quality`, `recency_time_boundary`, `investment_logic_depth`


## Case 2: 现在的市盈率处于历史什么位置

hard checks:
- 必须明确标的口径。若用户说 A 股，不能只回答上证指数；应考虑深证、创业板、沪深全市场或说明口径选择。
- 必须回答“历史位置”，需要历史分位、历史区间、当前 PE 和时间窗口。
- 若只给当前 PE 或单一指数，属于意图和量化不足。

主要维度：`intent_scenario_recognition`, `comparison_quantification`, `recency_time_boundary`


## Case 3: 半导体国产替代有什么消息面

hard checks:
- 消息面类问题必须优先回答最新信息，因为旧消息对当前股价意义较弱。
- 应区分近期政策、公司公告、行业事件、订单或制裁动态，不能用长期背景科普替代消息。
- 旧信息即使没错，也不能给高分。

主要维度：`recency_time_boundary`, `evidence_source_quality`, `investment_logic_depth`

质量标签候选：`stale_or_wrong_time_evidence`, `wrong_or_shallow_source`

## Case 4: 易方达蓝筹精选混合怎么样，可以买吗

hard checks:
- 基金诊断至少包括：历史收益、最大回撤、夏普或风险收益指标。
- 必须有对比：与指数、同类基金、同类排名或同类分位比较。
- 必须分析前十大持仓和重仓股风格，并判断是否匹配用户风险偏好或投资目标。
- “可以买吗”需要条件化建议和风险，不应只介绍基金。
- 好答案还应回答“为什么推荐/不推荐、什么价格或场景下买、买入后看什么风险”；只列历史业绩和基金经理不够。

主要维度：`comparison_quantification`, `method_fit`, `actionability_risk`

质量标签候选：`missing_required_analysis_elements`

## Case 5: 同一题材中龙头强，小弟能不能跟

hard checks:
- 必须识别“龙头带动小弟”的题材股交易逻辑。
- 应比较龙头和跟随标的的业务纯度、弹性、资金地位、补涨空间和风险。
- 不能只分别分析三只股票，也不能把题材联动当作普通财务比较。

主要维度：`intent_scenario_recognition`, `method_fit`, `investment_logic_depth`


## Case 6: 典型题材股现在能不能买

hard checks:
- 必须围绕题材回答：题材是什么、什么时候发酵、逻辑有多大、能否持续、还有多大空间。
- 技术面、量价、资金可以补充，但不能成为主轴。
- 必须给出观察条件和风险，如题材退潮、关键位破坏、资金转向。

主要维度：`method_fit`, `investment_logic_depth`, `actionability_risk`

质量标签候选：`missed_core_investment_logic`, `method_mismatch`

## Case 7: 典型价值股能不能买

hard checks:
- 必须包括公司业务逻辑、财务分析、估值分析和风险提示。
- 对用户来说，价值股关键判断是“逻辑顺不顺、现在估值便不便宜”。
- 只做财务指标罗列或短期技术判断，不能高分。
- 对 CPO/光模块等机构成长股，应补充下游需求、客户结构、行业地位、业绩确定性、估值和资金偏好；财务分析不能替代核心产业逻辑。

主要维度：`investment_logic_depth`, `method_fit`, `comparison_quantification`

质量标签候选：`missed_core_investment_logic`, `method_mismatch`

## Case 8: 既有题材又有基本面的股票全面分析

hard checks:
- 应同时从短期题材和长期基本面两条线分析。
- 短期看催化、资金、题材持续性；长期看业务、业绩、估值、风险。
- 好答案应区分短期交易结论和长期配置结论。

主要维度：`method_fit`, `investment_logic_depth`, `actionability_risk`


## Case 9: 下游客户占比

hard checks:
- 这类信息通常公开资料难查，但对基本面分析很重要，常见于调研纪要、研报全文、公司交流纪要等。
- 若没有可靠来源，应明确说明来源限制，不能用泛泛客户名单替代占比。
- 应评估最终回答是否使用专业来源，或是否说明来源限制。

主要维度：`evidence_source_quality`, `investment_logic_depth`, `composition_credibility`

质量标签候选：`wrong_or_shallow_source`

## Case 10: 离岸人民币趋势或复杂宏观趋势

hard checks:
- 宏观问题考验关键信息选择和推理能力，不能只是资讯拼接。
- 应抓住美元指数、利差、央行政策、贸易/资本流动、风险偏好等关键变量。
- 应给出时间区间和情景推演，不宜给单一确定性结论。
- 好答案要给关键阈值或观察点，例如美元指数、美元/人民币关键位、利差方向和中美政策节奏；否则容易沦为新闻摘要。

主要维度：`investment_logic_depth`, `method_fit`, `actionability_risk`


## Case 11: 为什么个股没跟板块上涨

hard checks:
- 不能只说“资金没选它”或技术面弱，必须解释资金为什么不选。
- 应分析业务纯度、赛道差异、筹码结构、事件催化、板块核心/边缘地位。
- 应给出操作建议和风险点。
- 若是油气板块带动但个股不涨，应区分油气开采、海工/FPSO、设备服务、订单兑现周期和市场领涨方向；不能把“油价涨”机械外推到所有相关股。

主要维度：`investment_logic_depth`, `method_fit`, `actionability_risk`

质量标签候选：`missed_core_investment_logic`

## Case 12: 冲高回落和是否切换到更强标的

hard checks:
- 用户关心的是投资逻辑是否变了、是否有未看到的利空、是否获利了结、是否要切换。
- 必须比较原标的和候选标的在产业地位、业务纯度、业绩确定性、资金抱团和赔率上的差异。
- 只做 K 线解读不够。
- 对“同题材为什么 A 弱 B 强”类问题，必须建立同一口径比较表：业务占比/题材纯度、龙头地位、业绩兑现、估值、资金抱团和切换成本；反复解释 A 的冲高回落属于低价值回答。

主要维度：`intent_scenario_recognition`, `comparison_quantification`, `investment_logic_depth`


## Case 13: 避险资产对比

hard checks:
- 表面上都是分红稳定资产时，必须讲清商业模式本质差异。
- 例如稳定现金流资产和制造业核心竞争力资产，风险来源和估值逻辑不同。
- 不能只从行业、估值、波动表层比较。
- 例如长江电力 vs 格力电器，核心差异不是简单“分红股对比”，而是水电现金流/监管价格机制 vs 制造业品牌、渠道和竞争力。

主要维度：`investment_logic_depth`, `comparison_quantification`, `method_fit`


## Case 14: 内在价值但近期被特殊事件重估

hard checks:
- 必须识别近期市场炒作或价值重估的真正原因，如隐含股权价值、资产重估、财报预期。
- 不能只根据过去业绩给出看似合理但偏题的价值判断。
- 应说明隐藏资产或事件如何影响市值和估值。
- 对“内在价值”问题，应优先检查是否存在持股平台、并购、资产重估、拟上市资产等隐含价值；若市场交易的就是这条线，传统利润估值会严重偏题。

主要维度：`evidence_source_quality`, `investment_logic_depth`, `recency_time_boundary`


## Case 15: 黄金和原油现在投资价值

hard checks:
- 不应写成纯新闻解读报告，要有资产配置视角。
- 必须说明时间区间：短线交易、中期趋势、长期配置。
- 应给出关键变量和风险，例如美元、利率、地缘、供需、库存、通胀预期。

主要维度：`method_fit`, `investment_logic_depth`, `actionability_risk`


## Case 16: 个股深度分析

hard checks:
- 不能所有股票都套同一模板。不同票有不同投资逻辑：游资票、机构票、热点票、价值票的分析顺序不同。
- 热点票要看刚开始拉升的一两天信息、热点级别、板块持续性，再看技术和资金。
- 机构票要看业绩预测、各业务增长逻辑、PE 对比、券商研报推票逻辑。
- 深度分析要做到“千股千评”：先判断股票当下由题材、机构成长、周期、隐含资产、避险分红还是事件驱动定价，再决定证据和结构。

主要维度：`method_fit`, `investment_logic_depth`, `composition_credibility`

质量标签候选：`template_data_dump`, `method_mismatch`

## Case 17: 长线走势或中长线持有潜力

hard checks:
- 中长线问题不能主要使用短期技术面数据解释。
- 应分析长期业务空间、竞争格局、盈利质量、估值、安全边际和风险。
- 技术面只能作为辅助买点或风控。
- 对 2-3 年持有潜力，应重点看业务空间、客户/产品、国产替代或行业景气、利润率、估值相对同业和业绩兑现风险；MACD、均线、近日涨跌只能辅助择时。

主要维度：`method_fit`, `investment_logic_depth`, `actionability_risk`

质量标签候选：`method_mismatch`

## Case 18: 最近三天重要资讯

hard checks:
- 如果确实没有重大消息，应直接说明“没有发现重大消息”，再补充技术或交易分析。
- 不能为了填充答案而罗列不重要或不在时间窗口内的资讯。
- 需要严格时间边界。
- 对“最近三天重要资讯”，普通涨跌、主力资金和技术波动不是“重大资讯”；可作为解释补充，但不能冒充新闻事件。

主要维度：`recency_time_boundary`, `evidence_source_quality`, `composition_credibility`


## Case 19: 指数回撤和未来突破/跌破推演

hard checks:
- 必须正确计算回撤幅度和时间范围。
- 仅给均线、BOLL、支撑压力是常规回答；更好答案应有情景推演和增量逻辑。
- 可以结合技术结构、政策、资金、宏观变量，但必须说明推演条件。
- 情景推演可以使用波浪结构、政策/资金/宏观变量或关键点位组合；关键是给出突破/跌破的触发条件、路径和风险，而不是只堆技术指标。

主要维度：`comparison_quantification`, `investment_logic_depth`, `actionability_risk`


## Case 20: 推荐适合我的 ETF 或基金

hard checks:
- “适合我”不是收益榜推荐，必须检查用户风险偏好、投资期限、资金规模、波动承受和配置目的；若没有画像，应说明并给分层假设。
- ETF/基金推荐应说明组合角色，例如核心宽基、红利防守、行业卫星，而不是默认推荐医疗、5G 等窄行业高波动主题。
- 至少需要基金/ETF 的风险收益、回撤、费率、流动性、持仓/指数风格和同类或替代品比较。
- 好答案可以直接给两个候选，但必须解释为什么这两个更适合当前用户，并给仓位和持有期限边界。

主要维度：`user_profile_suitability`, `comparison_quantification`, `actionability_risk`

质量标签候选：`missing_user_profile_fit`, `missing_required_analysis_elements`, `overconfident_or_unsuitable_action`

## Case 21: 当前宏观环境下怎么投资

hard checks:
- 必须先判断“当前宏观环境是什么”，再映射到资产类别、仓位和策略；不能只给通用配置模板。
- 应解释为什么现在这样配，尤其是利率、通胀、政策、风险偏好、行业景气和市场估值如何影响配置。
- 对新手或画像不明用户，应优先给稳健、分层、可执行的配置框架，而不是泛泛标的清单。

主要维度：`investment_logic_depth`, `method_fit`, `actionability_risk`


## Case 22: 个股已有浮盈，是否继续持有

hard checks:
- 用户核心需求是“持有、减仓、止盈还是继续看”，必须给条件化动作。
- 好答案应结合趋势、估值/基本面、资金或情绪指标，并细化到减仓、止损、反弹确认和观察条件。
- 不能只做行业或公司宽泛分析，也不能无条件鼓励继续持有。

主要维度：`actionability_risk`, `evidence_source_quality`, `method_fit`

质量标签候选：`missing_decision_action_for_recommendation`

## Case 23: 现在买黄金还是买原油

hard checks:
- 不应写成纯新闻解读，必须有资产配置和风险偏好视角。
- 应区分稳健配置与进攻博弈：黄金通常承担避险/配置角色，原油更依赖供需、地缘和价格弹性。
- 应给时间区间、近端走势或波动比较、关键变量和风险；最好用近 20/60 日收益、波动率或趋势对比支撑。

主要维度：`comparison_quantification`, `method_fit`, `actionability_risk`


## Case 24: 有资金规模并要求结合目标风险推荐股票

hard checks:
- 必须先使用或询问用户目标、风险承受、期限和交易风格；有历史画像时必须承接。
- 好答案应有组合框架，例如核心/卫星、观察仓/交易仓、单票上限、买入/持有/卖出规则。
- 如果直接给股票，必须说明筛选标准、仓位、风险边界和为什么适合用户，不能只给概念或热股。

主要维度：`user_profile_suitability`, `actionability_risk`, `method_fit`

质量标签候选：`missing_user_profile_fit`, `missing_decision_action_for_recommendation`, `overconfident_or_unsuitable_action`

## Case 25: 弱复苏、低通胀、利率下行环境下选四个行业中的两个

hard checks:
- 用户明确要求历史类似宏观阶段表现、当前估值分位和盈利确定性，关键数据缺失会明显降低质量。
- 必须横向比较银行、家电、白酒、创新药等方向的弹性、确定性、估值和风险收益，不应只给宏观框架。
- 思路“高级”不能抵消数据缺口；大规模评测应把缺数据的漂亮框架判为中低分。

主要维度：`evidence_source_quality`, `comparison_quantification`, `investment_logic_depth`

质量标签候选：`missing_required_analysis_elements`, `wrong_or_shallow_source`

## Case 26: 市场潜在风险、对算力租赁冲击，并结合风格推荐股票

hard checks:
- 必须拆解宏观、政策、行业风险，并分别说明对算力租赁短期和中期的冲击路径。
- 最后还要完成“结合我的风格推荐现在适合买入的股票”，不能只停在风险分析。
- 好答案既要有风险传导，又要有具体标的、仓位、买入区间或观察条件。

主要维度：`intent_scenario_recognition`, `investment_logic_depth`, `actionability_risk`

质量标签候选：`missing_decision_action_for_recommendation`, `missing_user_profile_fit`

## Case 27: 稳增长周期下优先看哪些板块

hard checks:
- 必须围绕过去几轮稳增长周期，比较上游资源、工程机械、建材、券商、银行的启动顺序、弹性、持续性和回撤。
- 好答案应结合当前周期位置、区间表现或图表验证，结论和分析证据要一致。
- 只分别介绍各行业政策或景气，不给优先级和取舍依据，不能高分。

主要维度：`comparison_quantification`, `evidence_source_quality`, `investment_logic_depth`


## Case 28: 震荡上行后的短期反弹分歧，如何控制仓位和参与标的

hard checks:
- 必须先定义市场阶段，例如上涨/下跌家数、涨跌停、成交、情绪和主线分歧，而不是直接给常规配置清单。
- 仓位建议要和当前盘面状态联动，并区分科技成长、资源品的核心/卫星或进攻/防守角色。
- 短线参与标的必须给原因、风险和退出条件。

主要维度：`recency_time_boundary`, `actionability_risk`, `investment_logic_depth`

质量标签候选：`template_data_dump`, `missing_decision_action_for_recommendation`

## Case 29: 个股成本接近腰斩，房地产何时触底，该割肉还是加仓

hard checks:
- 必须识别深套和情绪压力，不能急着给抄底、加仓或确定触底时间。
- 好答案应拆分政策底、市场底、基本面底，并结合个股估值、技术位置、流动性和经营风险。
- 必须给“什么条件下才补仓/减仓/止损/等待”的分步框架；过度确定的底部时间应扣分。

主要维度：`scenario_emotion_recognition`, `actionability_risk`, `method_fit`

质量标签候选：`misread_loss_or_emotion_context`, `overconfident_or_unsuitable_action`

## Case 30: 你觉得我适合投资什么股票

hard checks:
- 这是私人投顾感测试。必须根据历史提问、风险偏好、持仓、关注行业和交易风格做推断；不能只给一串股票代码。
- 若画像不足，应说明“不足以定制”，并用分层偏好或追问处理；不能编造用户画像。
- 好答案应说明适合的股票类型：有产业逻辑、能跟踪验证、允许中期持有，或其他与用户历史一致的风格。

主要维度：`user_profile_suitability`, `intent_scenario_recognition`, `composition_credibility`

质量标签候选：`missing_user_profile_fit`

## Case 31: 多次询问“给我推荐两只适合我的 ETF”

hard checks:
- 同一用户画像下，推荐应相对稳定；若多次回答完全不同，必须有新信息、市场变化或假设变化解释。
- 推荐不能脱离用户画像，尤其不能默认给高波动、窄行业主题 ETF 作为普通用户通用配置。
- 推荐应优先从核心底仓、防守增强、行业卫星等角色出发，而不是单纯按近年收益或主题热度筛选。

主要维度：`user_profile_suitability`, `composition_credibility`, `comparison_quantification`

质量标签候选：`missing_user_profile_fit`, `template_data_dump`, `overconfident_or_unsuitable_action`

## Case 32: 我很迷茫，不知道买什么股票，感觉买什么都是亏

hard checks:
- 这不是普通选股需求，而是持续亏损后的无力感、信心受挫和决策失灵。
- 好答案应先建议暂停盲目选股、降低仓位、复盘交易、分散到宽基/红利/低波动或先建立筛选框架，再谈具体机会。
- 直接切到短线综合推荐、技术抓反弹、筛强势股，是严重误读用户处境。

主要维度：`scenario_emotion_recognition`, `user_profile_suitability`, `actionability_risk`

质量标签候选：`misread_loss_or_emotion_context`, `overconfident_or_unsuitable_action`
