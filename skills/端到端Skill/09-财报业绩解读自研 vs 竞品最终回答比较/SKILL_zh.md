# 财报业绩解读自研 vs 竞品最终回答比较评测协议

本 skill 是 **result-only 自研 vs 竞品最终回答比较器**。它只比较同一 `case_id`、同一用户问题下，自研模型最终回答与一个竞品模型最终回答的答案质量，不读取、不评分、不归因任何过程字段。

## 协议边界

只允许使用以下信息作为评分、证据和结论依据：
- `case_id`
- 用户问题
- 自研模型标识
- 竞品模型标识
- 自研模型最终回答
- 竞品模型最终回答

若原始输入中包含 `chain`、`tools`、`plan`、`function_call` 或其他过程字段，必须忽略；不得把它们作为评分、证据、归因、比较结论或优缺点来源。

如果最终回答有问题，只描述问题在回答文本中的表现，例如财务数据或口径错误、遗漏公告披露、归因表层化、业务财务联动不足、投资判断不可验证、表达不可信。不得判断缺陷来自模型、数据源、检索或其他过程因素。

## 适用范围

仅在以下条件同时满足时使用：
- 题目属于财报、业绩公告、经营指标、会计口径、分红方案、现金流、利润质量、财务影响或业绩持续性解释任务；
- 输入中存在同一 `case_id` 对应的两份记录；
- 两份记录分别代表自研模型与一个竞品模型；
- 当前任务目标是比较双方最终回答谁更好、各自好坏、以及竞品答案中值得学习的优点。

典型场景包括：
- 年报、季报、业绩快报、业绩预告、分红公告、官网公告的内容解读；
- 营收、净利润、扣非净利润、毛利率、ROE、现金流、负债、偿债能力、收入确认等指标变化原因；
- 财报利好/利空、业绩对股价影响、持续性、估值与市场预期判断；
- 会计差错更正、收入确认政策变更、非经常性损益、公允价值变动、套期保值、税务补缴等特殊事件解释；
- 将财务数据与真实业务、行业周期、价格、订单、成本、产品结构、政策或公司公告原文连接起来。

不适用于：
- 单模型质检；
- 不同问题之间的横向比较；
- 一次同时比较多个竞品模型；
- 普通条件选股、普通资讯问答、无财务报告语境的个股诊断、KYC 投顾建议或同花顺产品客服问答；
- 需要诊断过程能力或失败来源的评测。

## 最终回答读取规则

- 自研模型：优先读取 `self_record.text_answer`；若为空，可读取 `self_record.answer`。
- 竞品模型：优先读取 `competitor_record.text_answer`；若为空，可读取 `competitor_record.answer`。
- 若存在归一化字段，可读取 `normalized.self_final_answer` 与 `normalized.competitor_final_answer`。
- 证据必须通过 pointer 回指上述最终回答字段或 `question`，不能回指任何过程字段。

## 评估流程

0. **校验同题**
   校验 `case_id`、用户问题和 pairing 是否一致。若 `same_question_verified=false`，不得输出胜负结论。



1. **识别题目类别与核心任务**
   判断用户真正要什么：查数、计算、诊股、选股、资讯解释、投资建议、KYC 适配、复合意图、澄清需求等。
   不要只按表面词判断，要看用户最终需要的决策产物。
   将类别记录到输出的 `category`，将核心意图记录到 `core_user_intent`。

2. **建立共享评估框架**
   阅读 [references/rubric/_index.md](references/rubric/_index.md)、活跃维度文件与 [references/golden_cases/_index.md](references/golden_cases/_index.md)。仅依据用户问题判断维度适用性并分配动态权重。同一题下，自研与竞品必须使用同一套维度和权重。

3. **分别做绝对评分**
   对自研最终回答和竞品最终回答分别按以下 7 个答案质量维度评分：
   - `intent_understanding`
   - `report_data_accuracy`
   - `primary_evidence_quality`
   - `causal_attribution_depth`
   - `business_financial_linkage`
   - `forward_investment_judgment`
   - `composition_credibility`

   每个活跃维度必须输出 `raw_score`、`dynamic_weight`、`rationale` 和至少一条 evidence（加权分、绝对分和最终分由评测引擎注入，LLM 无需手算）。不得因为另一方更差而抬高本方绝对分。

4. **记录封顶标签**
   - 每个活跃维度评分完成后，逐一检查是否触发封顶规则。
   - 本类别沿用原规则语义：封顶规则作为质量标签记录在 `applied_caps`，不直接改写分数。
   - 必须完整列出触发的 `applied_caps` 及 evidence。

5. **逐维比较**
   阅读 [references/comparison_protocol.md](references/comparison_protocol.md)。在双方绝对评分完成后逐维比较谁更好、差异体现在哪里、证据来自哪段最终回答。

6. **输出结论**
   总结自研最终回答的优点和缺点，竞品最终回答中值得学习的优点，双方共同失败点，并给出 `verdict`：
   - `self_better`
   - `competitor_better`
   - `tie`

   并输出 `absolute_quality_flag`（独立于 verdict）：
   - `both_good`：双方都达标
   - `self_poor`：自研不达标
   - `competitor_poor`：竞品不达标
   - `both_poor`：双方都不达标

   胜负判定规则：
   - 若加权总分差绝对值 < 8，默认 `tie`。
   - 若总分差 >= 8，分高者胜。
   - 若关键维度分差 >= 20，且该维度对题目核心任务重要，且证据明确，可覆盖总分判定。
   - 将判定结果记录到 `score_summary` 中。


7. **做答案层归因**
   对自研和竞品的每条 weakness 和 shared_failure，标注归因标签（见下方「答案层归因标签」）。归因只描述最终回答文本中的表现，不归因到过程。

8. **序列化输出**
   阅读 [references/output-schema_zh.md](references/output-schema_zh.md)。先输出结构化 JSON，再按需附简短自然语言评审。

## 答案质量硬要求

所有维度和 hard checks 必须覆盖以下 result-only 检查点：
- 用户意图满足：是否直接回答真正问题，是否遗漏显性或隐含约束。
- 结论有效性：是否给出明确结论，而非只给背景、数据或模糊建议。
- 正确性：是否存在报告期、指标、金额、同比环比、单季/累计、归母/扣非、会计政策、事实或边界错误。
- 完整性：是否覆盖关键子问题、对象范围、比较维度和必要解释。
- 逻辑闭环：结论与理由是否连贯，是否存在跳步、偷换口径或因果断裂。
- 证据支撑：关键断言是否有足够依据，是否只是主观判断或空泛表达。
- 财报穿透：是否把数字变化解释到业务、行业、成本、订单、产品结构、会计处理或特殊事件。
- 投资判断：涉及利好利空、股价影响、持续性或估值时，是否给出有条件、可验证、审慎的判断。
- 表达可信度：结构是否清楚，措辞是否审慎，是否避免不可验证的夸张表述。

金融/财报类答案还必须检查：
- 是否区分报告期、同比/环比、累计/单季、调整前/调整后、归母/扣非、经营/投资现金流等口径。
- 是否优先呈现公司披露、年报附注、季报变动原因、分红公告、审计意见等关键证据在最终回答中的体现。
- 是否说明主因、次因和对冲项，避免只做公式解释或表格堆砌。
- 是否识别会计差错更正、收入确认政策变更、非经常性损益、公允价值、套期保值、税务补缴、股份支付等高危特殊事项。
- 是否尊重“最新/最近/截至某日/报告期/公告后走势”等时间边界。


## 答案层归因标签

对自研和竞品的每条 weakness 和 shared_failure，必须标注一个归因标签：
- `intent_miss`：误解或遗漏用户意图
- `fact_time_gap`：事实、日期、时效、口径问题
- `evidence_gap`：证据不足或不可验证
- `calculation_gap`：公式、计算、样本、统计错误
- `logic_gap`：逻辑跳跃、因果不闭环
- `mapping_gap`：行业、概念、标的、受益链条映射不足
- `personalization_gap`：未处理用户画像、风险、持仓、期限
- `actionability_gap`：缺少可执行动作、条件、观察指标
- `risk_boundary_gap`：风险边界、限制、适当性不足
- `presentation_gap`：结构、表达、重点不清
- `unverifiable_claim`：关键断言不可验证

归因只能指向最终回答文本中的表现，不得归因到模型、数据源、检索、规划或其他过程因素。

## 证据规则

证据对象统一使用：

```json
{
  "source": "question | self_final_answer | competitor_final_answer",
  "pointer": "question | self_record.text_answer | self_record.answer | competitor_record.text_answer | competitor_record.answer | normalized.self_final_answer | normalized.competitor_final_answer",
  "quote_or_summary": "",
  "rationale": ""
}
```

要求：
- 每个维度评分至少有一条 evidence。
- 每条 `self_strengths`、`self_weaknesses`、`competitor_strengths`、`shared_failures` 都必须有 evidence。
- evidence 只能指向用户问题或双方最终回答。
- `quote_or_summary` 优先摘录最终回答中的短原文；原文过长时可摘要，但必须通过 pointer 指明位置。
- 如果某个判断无法从最终回答文本中看出，不能写入本 skill 的评分或结论。

## 保守评分

- 自研与竞品使用同一维度、同一权重、同一 hard checks。
- 先绝对评分，再相对比较。
- 不因为竞品更差就把自研绝对短板写成优势。
- 不因为自研更差就忽略竞品也没达标。
- 双方都差时，优先写 `shared_failures`。
- 自研优势必须同时满足：自研最终回答相对竞品更好、自研本身达到该维度基本标准、有自研最终回答证据。
- 竞品优点只写竞品最终回答中值得学习的地方。

## 参考索引

通过 [references/MANIFEST.md](references/MANIFEST.md) 按需读取子文件。
