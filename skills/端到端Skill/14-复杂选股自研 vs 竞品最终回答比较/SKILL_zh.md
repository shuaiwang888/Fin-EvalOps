# 复杂选股自研 vs 竞品最终回答比较评测协议

本 skill 是 **result-only 自研 vs 竞品最终回答比较器**。它只比较同一 `case_id`、同一用户问题下，自研模型最终回答与一个竞品模型最终回答的答案质量，不读取、不评分、不归因任何过程字段。

## 协议边界

只允许使用以下信息作为评分、证据和结论依据：
- `case_id`
- 用户问题
- 自研模型标识
- 竞品模型标识
- 自研模型最终回答
- 竞品模型最终回答

若原始输入中包含 `chain`、`tools`、`plan`、`function_call`、`context` 或其他过程字段，必须忽略；不得把它们作为评分、证据、归因、比较结论或优缺点来源。

如果最终回答有问题，只描述问题在回答文本中的表现，例如核心条件遗漏、金融口径错误、候选池不可验证、排序缺失、字段不全、时间边界错误、表达过度确定。不得判断缺陷来自模型、数据源、检索、工具或其他过程因素。

## 适用范围

仅在以下条件同时满足时使用：
- 题目属于复杂选股任务，包括长条件量化选股、复杂交易形态筛选、带定性约束的推理选股、结构化条件与非标信息混合筛选、跨领域或分层筛选；
- 输入中存在同一 `case_id` 对应的两份记录；
- 两份记录分别代表自研模型与一个竞品模型；
- 当前任务目标是比较双方最终回答谁更好、各自好坏、以及竞品答案中值得学习的优点。

不适用于：
- 单模型质检；
- 不同问题之间的横向比较；
- 一次同时比较多个竞品模型；
- 需要诊断过程能力或失败来源的评测；
- 普通单只股票诊断、简单行情查询、纯事件概念受益排序、投资组合/KYC 推荐或一般知识问答。

若问题核心是“事件/概念受益标的排序”，优先使用 `01-event-and-concept-stock-selection` 的 result-only 协议；若核心是长条件、多阶段、技术形态或结构化+非标混合筛选，用本协议。

## 最终回答读取规则

- 自研模型：优先读取 `self_record.text_answer`；若为空，可读取 `self_record.answer`。
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
   - `intent_condition_extraction`
   - `financial_semantics_and_caliber`
   - `screening_plan_decomposition`
   - `result_correctness_and_coverage`
   - `ranking_and_decision_actionability`
   - `data_logic_time_boundary`
   - `composition_credibility`

   每个活跃维度必须输出 `raw_score`、`dynamic_weight`、`rationale` 和至少一条 evidence。不得因为另一方更差而抬高本方绝对分。

3. **记录封顶标签**
   - 每个活跃维度评分完成后，逐一检查是否触发封顶规则。
   - 本类别沿用标签式封顶：封顶规则作为质量标签记录在 `applied_caps`，不直接改写分数。
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
- 用户意图满足：是否完整保留长问句中的显性条件、隐性条件、否定条件、范围条件、排序和输出字段。
- 金融口径：是否正确理解均线、MACD、KDJ、资金流、龙虎榜、北向、退市风险、主线题材、分时/K 线等语义。
- 结论有效性：是否给出明确候选池、无结果解释、排序或可执行判断，而非只给背景、条件复述或模糊建议。
- 正确性：是否存在事实、时间、实体、数值、公式、指标口径、业务边界或数据可用性错误。
- 完整性：是否覆盖关键子问题、对象范围、比较维度、分层关系和必要字段。
- 筛选拆解可见性：复杂条件是否在最终回答中被组织成硬条件、软条件、二次验证、先后关系和排序逻辑。
- 结果可核验性：候选股、字段、数值、公式、排序依据和边界说明是否能从最终回答文本中看出。
- 可执行性：回答是否能帮助用户继续筛选、复核或交易准备，是否说明核心对象、理由、限制和风险。
- 表达可信度：结构是否清楚，措辞是否审慎，是否避免不可验证的夸张表述。

复杂选股答案还必须检查：
- 是否把“或”关系拆成“且”关系，或把重复强调当成额外条件。
- 是否区分硬条件、软条件、非标信息、不可用数据和需要确认的边界。
- 是否保留先后依赖，例如横盘后突破、前一日成交量、指定日期窗口、多周期条件。
- 是否说明排序依据，例如主力资金、区间涨幅、条件满足度、题材纯度、结果可信度或后续验证优先级。
- 是否避免用漂亮表格、候选名单或条件复述替代核心判断。

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
