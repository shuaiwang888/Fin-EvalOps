# 交互澄清自研 vs 竞品最终回答比较评测协议

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

如果最终回答有问题，只描述问题在回答文本中的表现，例如该澄清未澄清、多轮补充未承接、实体识别错误、交易规则错误、口径不清、证据不足、行动方案不可执行或后续引导空泛。不得判断缺陷来自模型、数据源、检索或其他过程因素。

## 适用范围

仅在以下条件同时满足时使用：
- 题目属于交互澄清、多轮投资对话、金融规则纠错、错别字/异常代码实体识别、模糊条件口径化、后续引导闭环等场景；
- 输入中存在同一 `case_id` 对应的两份记录；
- 两份记录分别代表自研模型与一个竞品模型；
- 当前任务目标是比较双方最终回答谁更好、各自好坏、以及竞品答案中值得学习的优点。

适用题型包括：
- 用户意图模糊，需要主动澄清、口径化或给出分层方案，例如“能帮我回本的股票”“平安现在能买吗”“主力高度控盘的个股”。
- 多轮咨询中用户补充了持仓、成本、股票、亏损幅度、时间目标、风险偏好等信息，需要最终回答承接前文。
- 用户问题包含错误前提或交易规则陷阱，例如做空、北交所权限、科创板盘后固定价格交易、撤单时间、T+1/T+0、分红除权除息、国债逆回购计息。
- 用户输入包含错别字、拼音/同音误写、重复代码、股票代码多输一位、行业黑话或口语简称，需要识别最可能实体并在必要时澄清。
- 用户咨询金融术语、技术形态、策略条件或选股口径，需要把模糊词转成可核验定义。
- 答案应给出贴合当前咨询的后续引导、监控、提醒或继续追问，才能形成咨询闭环。

不适用于：
- 单模型质检；
- 不同问题之间的横向比较；
- 一次同时比较多个竞品模型；
- 需要诊断过程能力或失败来源的评测；
- 普通事件资讯问答、纯回测取数计算、财报业绩归因、KYC 投顾适配、文档/图片问答或严格指令遵循。

## 最终回答读取规则

- 自研模型：优先读取 `self_record.text_answer`。
- 竞品模型：优先读取 `competitor_record.text_answer`；若为空，可读取 `competitor_record.answer`。
- 若存在归一化字段，可读取 `normalized.self_final_answer` 与 `normalized.competitor_final_answer`。
- 若最终回答包含图片、截图、图表、卡片或表格图片，只能使用其中用户可见的信息作为答案内容；证据 pointer 仍必须回指最终回答字段。
- 证据必须通过 pointer 回指上述最终回答字段或 `question`，不能回指任何过程字段。

## 评估流程

0. **校验同题**  
   校验 `case_id`、用户问题和 pairing 是否一致。若 `same_question_verified=false`，不得输出胜负结论。

1. **建立共享评估框架**  
   阅读 [references/rubric/_index.md](references/rubric/_index.md)、活跃维度文件、[references/golden_cases/_index.md](references/golden_cases/_index.md) 与 [references/golden_cases/image_annotation_anchors.md](references/golden_cases/image_annotation_anchors.md)。仅依据用户问题判断维度适用性并分配动态权重。同一题下，自研与竞品必须使用同一套维度和权重。

2. **分别做绝对评分**  
   对自研最终回答和竞品最终回答分别按以下 9 个答案质量维度评分：
   - `intent_fulfillment`
   - `ambiguity_clarification`
   - `context_continuity`
   - `entity_resolution`
   - `financial_rule_and_premise`
   - `assumption_definition`
   - `actionability_and_risk_plan`
   - `evidence_grounding`
   - `guidance_and_retention`

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

6. **做答案层归因**  
   对自研和竞品的每条 weakness 和 shared_failure，标注归因标签（见下方「答案层归因标签」）。归因只描述最终回答文本中的表现，不归因到过程。

7. **序列化输出**  
   阅读 [references/output-schema_zh.md](references/output-schema_zh.md)。先输出结构化 JSON，再按需附简短自然语言评审。

## 答案质量硬要求

所有维度和 hard checks 必须覆盖以下 result-only 检查点：
- 用户真实意图是否被识别，而不是只按字面或模板回答。
- 该澄清时是否澄清；不能直接回答时是否给出关键追问、默认假设或分层方案。
- 多轮场景中，最终回答是否使用用户已经补充的股票、成本、买入时间、亏损幅度、目标价、权限和风险偏好。
- 错别字、同音、简称、重复代码、异常代码和黑话是否按股民输入习惯识别。
- 交易规则、权限门槛、税费、计息、清算和市场制度错误前提是否在答案开头纠正。
- 模糊词是否口径化，例如“近期”“短线”“适中”“回调较多”“业绩增长”“主力高度控盘”。
- 具体建议是否具备触发条件、仓位节奏、风险边界、复盘指标和可执行下一步。
- 关键事实、规则、行情、公告、数据和结论之间是否有可见支撑。
- 后续引导是否贴合当前咨询，而不是泛泛客套。

金融/投顾对话类答案还必须检查：
- 是否避免把“回本”偷换成“推荐新股票”。
- 是否避免在不可交易、无权限或规则错误前提上继续制定操作计划。
- 是否在标的不明确时处理多义候选，例如“中国平安/平安银行”。
- 是否在用户要求优先级、做 T、止盈、加仓、换股时给出可比较标准和风险约束。
- 是否尊重“今天、明天、下周三、近期、年底前、现在”等时间边界。

## 答案层归因标签

对自研和竞品的每条 weakness 和 shared_failure，必须标注一个归因标签：
- `intent_miss`：误解或遗漏用户真实意图、隐含需求或子问题
- `clarification_gap`：该澄清未澄清，模糊条件未口径化或分层方案缺失
- `context_continuity_gap`：多轮补充信息未承接，用户已提供的变量被丢弃
- `entity_resolution_gap`：错别字、同音误写、简称、异常代码或多义实体识别错误
- `rule_premise_gap`：交易规则错误或错误前提未纠正
- `fact_time_gap`：事实、日期、时效、口径问题
- `evidence_gap`：证据不足或不可验证
- `actionability_gap`：缺少可执行动作、触发条件、仓位节奏或复盘指标
- `risk_boundary_gap`：风险边界、限制、适当性不足
- `guidance_gap`：后续引导空泛或缺失，咨询闭环未形成
- `presentation_gap`：结构、表达、重点不清

归因只能指向最终回答文本中的表现，不得归因到模型、数据源、检索、规划、工具或其他过程因素。

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

通过 [references/MANIFEST.md](references/MANIFEST.md) 按需读取子文件。完整文件导航、依赖声明和协议步骤映射见 MANIFEST。
