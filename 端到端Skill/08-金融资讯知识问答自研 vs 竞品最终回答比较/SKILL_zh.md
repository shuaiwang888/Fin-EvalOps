# 金融资讯知识问答自研 vs 竞品最终回答比较评测协议

本 skill 是 **result-only 自研 vs 竞品最终回答比较器**。它只比较同一 `case_id`、同一用户问题下，自研模型最终回答与一个竞品模型最终回答在金融资讯知识问答场景中的答案质量，不读取、不评分、不归因任何过程字段。

## 协议边界

评测输入包含：
- `case_id`
- 用户问题
- 当前评测 skill 标识或评测协议名
- 自研模型标识
- 竞品模型标识
- 自研模型最终回答
- 竞品模型最终回答

只允许使用用户问题、自研最终回答、竞品最终回答作为评分、证据和胜负结论依据。当前评测 skill 标识只用于确认本题是否应走 `08-information-and-knowledge-qa` 协议、选择对应输出 schema 与 rubric；不得把 skill 名称、调用方式或评测配置本身作为任何一方答案优劣的证据。

若原始输入中包含 `chain`、`tools`、`plan`、`function_call`、运行日志、隐藏思考、工具输入输出或其他过程字段，必须忽略；不得把它们作为评分、证据、归因、比较结论或优缺点来源。

如果最终回答有问题，只描述问题在回答文本中的表现，例如事实错误、时间窗口不符、证据不足、核心信号缺失、投资映射不可用、逻辑不闭合或表达不可验证。不得判断缺陷来自模型内部、数据源、查询策略、规划、工具选择或其他过程因素。

## 适用范围

仅在以下条件同时满足时使用本协议：
- 题目属于金融资讯、政策监管、产业事件、公司进展、市场异动、市场传闻、调研纪要、横向资讯比较、资讯影响或投资映射问答；
- 输入中存在同一 `case_id` 对应的两份记录；
- 两份记录分别代表自研模型与**一个**竞品模型；
- 当前任务目标是比较双方最终回答谁更好、自研模型好在哪和差在哪、竞品模型好在哪以及哪些点值得学习。

典型场景包括：
- 查询某政策、监管动态、宏观操作、行业新闻或公司事件的最新情况、特殊之处、原因和影响；
- 梳理近期政策、监管、产业、企业事件，并判断主线或市场关注点；
- 解释大盘、板块、题材或个股异动原因，尤其是盘中/近日热点；
- 比较多个主题的新闻密度、政策层级、产业落地和概念热度；
- 将资讯转化为行业判断、A 股标的映射、受益链条、风险点或后续观察指标；
- 判断市场小段子、调研纪要、金融大 V 文章、官媒截图等非标准资讯的可信边界和市场含义。

不适用于：
- 普通单模型质检；
- 不同问题之间的横向比较；
- 一次同时比较多个竞品模型；
- 纯行情查询、纯财务指标查询、纯回测计算、KYC 投顾建议、产品客服问答；
- 需要做非答案文本能力诊断的评测。

## 最终回答读取规则

- 自研模型：优先读取 `self_record.text_answer`；若为空，可读取 `self_record.answer`。
- 竞品模型：优先读取 `competitor_record.text_answer`；若为空，可读取 `competitor_record.answer`。
- 若存在归一化字段，可读取 `normalized.self_final_answer` 与 `normalized.competitor_final_answer`。
- 若输入包含 `evaluation_skill`、`skill_name` 或同义字段，只能用于确认评测协议，不得写入 evidence。
- 证据必须通过 pointer 回指上述最终回答字段或 `question`。

## 评估流程

0. **校验同题**
   校验 `case_id`、用户问题和 pairing 是否一致。若 `same_question_verified=false`，不得输出胜负结论。

1. **识别题目类别与核心任务**
   判断用户真正要什么：资讯解释、事实查询、政策/监管梳理、市场异动归因、横向比较、投资影响、受益标的、真假核验或可持续性判断等。不要只按表面词判断，要看用户最终需要的决策产物。将类别记录到输出的 `category`，将核心意图记录到 `core_user_intent`。

2. **建立共享评估框架**
   阅读 [references/rubric/_index.md](references/rubric/_index.md)、活跃维度文件、[references/golden_cases/_index.md](references/golden_cases/_index.md) 和 [references/golden_cases/image_annotation_anchors.md](references/golden_cases/image_annotation_anchors.md)。仅依据用户问题判断维度适用性并分配动态权重。同一题下，自研与竞品必须使用同一套维度和权重。

3. **分别做绝对评分**
   对自研最终回答和竞品最终回答分别按以下 8 个答案质量维度评分：
   - `intent_fulfillment`
   - `timeliness_fact_boundary`
   - `fact_evidence_quality`
   - `information_integration`
   - `investment_mapping`
   - `core_signal_extraction`
   - `nonstandard_source_awareness`
   - `credibility_expression`

   每个活跃维度必须输出 `raw_score`、`dynamic_weight`、`rationale` 和至少一条 evidence（`weighted_score` 由评测引擎注入，LLM 无需输出）。不得因为另一方更差而抬高本方绝对分。

4. **记录封顶标签**
   每个活跃维度评分完成后，逐一检查是否触发封顶规则。封顶规则作为质量标签记录在 `applied_caps`，不要求 LLM 手工改写分数。必须完整列出触发的 `applied_caps` 及 evidence。

5. **逐维比较**
   阅读 [references/comparison_protocol.md](references/comparison_protocol.md)。在双方绝对评分完成后逐维比较谁更好、差异体现在哪里、证据来自哪段最终回答。

6. **输出结论**
   总结自研最终回答的优点和缺点、竞品最终回答中值得学习的优点、双方共同失败点，并给出 `verdict`：
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
- 时效与事实：是否尊重最新、近期、盘中、截至某日等时间窗口，事实、日期、数值、实体、口径是否准确。
- 证据质量：最终回答是否给出足够权威、贴题、可验证的证据，是否区分官方事实、市场观点和未核验传闻。
- 信息整合：是否能把多主题、多来源、多口径信息整合成判断，而不是机械罗列。
- 核心信号：是否抓住真正驱动价格、情绪、政策变化、产业变化或题材扩散的核心信号。
- 投资映射：是否把资讯转化为行业、环节、标的、风险和观察指标的可执行判断。
- 非标准资讯边界：是否正确处理市场小段子、调研纪要、金融大 V 文章、官媒截图、公告截图等来源的价值与不确定性。
- 逻辑闭环：结论与理由是否连贯，是否存在跳步、偷换概念或因果断裂。
- 表达可信度：结构是否清楚，措辞是否审慎，是否避免不可验证的夸张表述。

金融资讯/投资问答还必须检查：
- 强时效题必须检查时间锚点、发布日期、数据统计期和是否混入未来或窗口外信息。
- 基础事实错会直接压低可信度，包括政策年份、文件层级、利率期限、销量口径、项目进展、供应链关系和事件原因。
- 用户常常表面问“是什么/怎么样”，实际要“有什么影响、哪些标的受益、该怎么判断、是否真实推进、是否只是炒作”。
- 大盘、板块、热点票异动不能套用基本面/技术面/资金面模板；必须抓住当日或近日最能解释价格波动的催化剂、传闻、政策、海外事件或机构/市场观点。
- 给股票名单时必须说明“主线-催化-受益环节-核心标的/边缘标的-风险约束”，不能只罗列大市值、热门概念或宽泛产业链公司。

## 答案层归因标签

对自研和竞品的每条 weakness 和 shared_failure，必须标注一个归因标签：
- `intent_miss`：误解或遗漏用户意图
- `fact_time_gap`：事实、日期、时效、口径问题
- `evidence_gap`：证据不足或不可验证
- `calculation_gap`：公式、计算、样本、统计错误
- `logic_gap`：逻辑跳跃、因果不闭环
- `mapping_gap`：行业、概念、标的、受益链条映射不足
- `source_boundary_gap`：来源类型、传闻边界或非标准资讯边界处理不足
- `actionability_gap`：缺少可执行动作、条件、观察指标
- `risk_boundary_gap`：风险边界、限制、适当性不足
- `presentation_gap`：结构、表达、重点不清
- `unverifiable_claim`：关键断言不可验证

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
- 每条 `self_strengths`、`self_weaknesses`、`competitor_strengths`、`competitor_weaknesses`、`shared_failures` 都必须有 evidence。
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
