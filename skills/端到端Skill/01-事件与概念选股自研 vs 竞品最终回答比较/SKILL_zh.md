# 事件与概念选股自研 vs 竞品最终回答比较评测协议

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

如果最终回答有问题，只描述问题在回答文本中的表现，例如事实错误、排序缺失、证据不足、逻辑不闭环、表达不可验证。不得判断缺陷来自模型、数据源、检索或其他过程因素。

## 适用范围

仅在以下条件同时满足时使用：
- 题目属于事件/概念驱动的选股、排序、产业映射、主题受益标的判断或海外映射任务；
- 输入中存在同一 `case_id` 对应的两份记录；
- 两份记录分别代表自研模型与一个竞品模型；
- 当前任务目标是比较双方最终回答谁更好、各自好坏、以及竞品答案中值得学习的优点。

不适用于：
- 单模型质检；
- 不同问题之间的横向比较；
- 一次同时比较多个竞品模型；
- 需要诊断过程能力或失败来源的评测。

## 最终回答读取规则

- 自研模型：优先读取 `self_record.text_answer`。
- 竞品模型：优先读取 `competitor_record.text_answer`；若为空，可读取 `competitor_record.answer`。
- 若存在归一化字段，可读取 `normalized.self_final_answer` 与 `normalized.competitor_final_answer`。
- 证据必须通过 pointer 回指上述最终回答字段或 `question`，不能回指任何过程字段。

## 评估流程

0. **校验同题**
   校验 `case_id`、用户问题和 pairing 是否一致。若 `same_question_verified=false`，不得输出胜负结论。

1. **建立共享评估框架**
   阅读 [references/rubric/_index.md](references/rubric/_index.md)、活跃维度文件、[references/golden_cases/_index.md](references/golden_cases/_index.md) 与 [references/golden_cases/image_annotation_anchors.md](references/golden_cases/image_annotation_anchors.md)。仅依据用户问题判断维度适用性并分配动态权重。同一题下，自研与竞品必须使用同一套维度和权重。

2. **分别做绝对评分**
   对自研最终回答和竞品最终回答分别按以下 7 个答案质量维度评分：
   - `intent_fulfillment`
   - `event_abstraction`
   - `industry_mapping`
   - `ranking_judgment`
   - `logic_closure`
   - `timeliness_fact_boundary`
   - `credibility_expression`

   每个活跃维度必须输出 `raw_score`、`dynamic_weight`、`rationale` 和至少一条 evidence（`weighted_score` 由评测引擎注入，LLM 无需输出）。不得因为另一方更差而抬高本方绝对分。

3. **记录封顶标签**
   - 每个活跃维度评分完成后，逐一检查是否触发封顶规则。
   - 本类别沿用原规则：封顶规则作为质量标签记录在 `applied_caps`，不直接改写分数。
   - 必须完整列出触发的 `applied_caps` 及 evidence。

4. **逐维比较**
   阅读 [references/comparison_protocol.md](references/comparison_protocol.md)。在双方绝对评分完成后逐维比较谁更好、差异体现在哪里、证据来自哪段最终回答。

5. **输出结论**
   总结自研最终回答的优点和缺点，竞品最终回答中值得学习的优点，双方共同失败点，并给出 `verdict`：
   - `self_better`
   - `competitor_better`
   - `tie`
   - `both_poor`

6. **序列化输出**
   阅读 [references/output-schema_zh.md](references/output-schema_zh.md)。先输出结构化 JSON，再按需附简短自然语言评审。

## 答案质量硬要求

所有维度和 hard checks 必须覆盖以下 result-only 检查点：
- 用户意图满足：是否直接回答真正问题，是否遗漏显性或隐含约束。
- 结论有效性：是否给出明确结论，而非只给背景、列表或模糊建议。
- 正确性：是否存在事实、时间、实体、数值、口径、定义或边界错误。
- 完整性：是否覆盖关键子问题、对象范围、比较维度和必要步骤。
- 逻辑闭环：结论与理由是否连贯，是否存在跳步、偷换概念或因果断裂。
- 证据支撑：关键断言是否有足够依据，是否只是主观判断或空泛表达。
- 排序/优先级：涉及选择、推荐、排名、最优、最相关、最受益时，是否给出清晰排序、分层或优先级标准。
- 可执行性：回答是否能帮助用户决策，是否说明核心对象、理由、限制和风险。
- 表达可信度：结构是否清楚，措辞是否审慎，是否避免不可验证的夸张表述。

金融/选股类答案还必须检查：
- 是否区分核心受益、次级受益、弱关联或概念蹭边。
- 是否区分主营/副业、直接/间接、上游/中游/下游、品牌/代工、核心产品/边缘产品。
- 是否说明排序依据，例如受益纯度、业绩弹性、确定性、产业地位、交易性价比。
- 是否避免只用概念标签、涨跌幅、市值、成交额替代投资逻辑。
- 是否尊重“最新/最近/截至某日/未来某区间”等时间边界。

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
