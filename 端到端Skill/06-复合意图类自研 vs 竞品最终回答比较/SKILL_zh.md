# 复合意图类自研 vs 竞品最终回答比较评测协议

本 skill 是 **result-only 自研 vs 竞品最终回答比较器**。它只比较同一 `case_id`、同一用户问题下，自研模型最终回答与一个竞品模型最终回答的 QA 质量，不读取、不评分、不归因任何过程字段。

## 协议边界

只允许使用以下信息作为评分、证据和结论依据：
- `case_id`
- 用户问题
- 自研模型标识
- 竞品模型标识
- 自研模型最终回答
- 竞品模型最终回答

若原始输入中包含 `context`、截图 OCR、人工批注、线上维度信号、`chain`、`tools`、`plan`、`function_call`、`tool_output`、耗时或其他过程字段，必须忽略；不得把它们作为评分、证据、归因、比较结论或优缺点来源。

如果最终回答有问题，只描述问题在回答文本中的表现，例如复合意图漏拆、关键子任务漏答、主次错位、多源证据没有综合、时间窗口或计算口径错误、案例不可核验、分析链路没有闭环、缺少策略/合约/价位/操作输出、结构像资料拼盘等。不得判断缺陷来自模型、检索、工具、规划、执行链路或其他过程因素。

## 适用范围

仅在以下条件同时满足时使用：
- 题目属于复合意图或复杂投研推理任务；
- 输入中存在同一 `case_id` 对应的两份记录；
- 两份记录分别代表自研模型与一个竞品模型；
- 当前任务目标是比较双方最终回答谁更好、各自好坏、以及竞品答案中值得学习的优点。

复合意图类问题包括：
- 一句话包含多个子任务、多个时间窗口、多个资产/公司/行业或多个输出要求；
- 复杂问句，尤其是字数较长、包含“现状/未来/影响/传导/策略/标的/估值/利润/案例/怎么做”等多层要求；
- 深度调研、行业竞争格局、产业链映射、事件影响评估、热点板块归纳、复杂交易方案；
- 需要把行情、新闻、公告、产业、政策、财务、资金、舆情等多源信息串成统一投资结论。

不适用于：
- 单模型质检；
- 不同问题之间的横向比较；
- 一次同时比较多个竞品模型；
- 纯单一意图行情查询、单步取数计算、普通 KYC 推荐、简单事件概念选股或客服问题；
- 需要诊断过程能力或失败来源的评测。

## 最终回答读取规则

- 自研模型：优先读取 `self_record.text_answer`；若为空，可读取 `self_record.answer`。
- 竞品模型：优先读取 `competitor_record.text_answer`；若为空，可读取 `competitor_record.answer`。
- 若存在归一化字段，可读取 `normalized.self_final_answer` 与 `normalized.competitor_final_answer`。
- 证据必须通过 pointer 回指上述最终回答字段或 `question`，不能回指任何过程字段、上下文字段、截图字段或批注字段。

## 评估流程

0. **校验同题**
   校验 `case_id`、用户问题和 pairing 是否一致。若 `same_question_verified=false`，不得输出胜负结论。



1. **识别题目类别与核心任务**
   判断用户真正要什么：查数、计算、诊股、选股、资讯解释、投资建议、KYC 适配、复合意图、澄清需求等。
   不要只按表面词判断，要看用户最终需要的决策产物。
   将类别记录到输出的 `category`，将核心意图记录到 `core_user_intent`。

2. **建立共享评估框架**
   阅读 [references/rubric/_index.md](references/rubric/_index.md)、[references/golden_cases/_index.md](references/golden_cases/_index.md) 和 [references/golden_cases/image_output_anchors.md](references/golden_cases/image_output_anchors.md)。仅依据用户问题判断复合子任务、主次关系、证据需求、时间窗口、数据口径、决策输出和结构要求。同一题下，自研与竞品必须使用同一套维度和权重。

3. **分别做绝对评分**
   对自研最终回答和竞品最终回答分别按以下 7 个答案质量维度评分：
   - `intent_decomposition`
   - `task_coverage_priority`
   - `multi_source_evidence_integration`
   - `analysis_chain_closure`
   - `data_logic_rigor`
   - `decision_actionability`
   - `composition_readability`

   每个活跃维度必须输出 `raw_score`、`dynamic_weight`、`rationale` 和至少一条 evidence。不得因为另一方更差而抬高本方绝对分。派生数值结果由评测引擎或代码注入，LLM 不需要手算。

4. **记录质量标签**
   若最终回答触发 hard checks，将对应质量标签记录在 `applied_caps`，并给出只能回指最终回答的 evidence。`ceiling`、限分和总分处理由调用方代码根据 `scripts/rule.py` 完成，本 skill 不输出计算过程。

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
- 意图拆解：是否拆出用户问题中的全部关键子任务、时间窗口、对象范围和输出要求。
- 子任务覆盖与主次：是否逐一回应关键问题，并把最影响用户判断的任务放在主线位置。
- 多源证据整合：是否把行情、新闻、公告、产业、政策、财务、资金、舆情等信息综合成统一结论，而不是并列罗列。
- 分析链路闭环：是否形成“事实-影响-传导-策略/结论”的闭环。
- 数据与逻辑严谨：计算口径、时间窗口、案例真实性、比较口径、盈亏公式和推演逻辑是否可靠。
- 决策表达与可执行性：是否回答“哪个更好、是否布局、如何调仓、怎么择股、做哪个合约、价位是多少”等用户真正要的输出。
- 结构与可读性：复杂问题是否先给总判断，再按子任务展开，避免报告式堆料遮蔽主结论。


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
- 若一方覆盖了更多子任务但主任务判断错误，不能只按覆盖面判胜。
- 双方都没有真正完成用户任务时，优先写 `shared_failures`。
- 自研优势必须同时满足：自研最终回答相对竞品更好、自研本身达到该维度基本标准、有自研最终回答证据。
- 竞品优点只写竞品最终回答中值得学习的地方。

## 参考索引

通过 [references/MANIFEST.md](references/MANIFEST.md) 按需读取子文件。
