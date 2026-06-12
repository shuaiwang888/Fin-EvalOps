# 分析评价类自研 vs 竞品最终回答比较评测协议

本 skill 是 **result-only 自研 vs 竞品最终回答比较器**。它只比较同一 `case_id`、同一用户问题下，自研模型最终回答与一个竞品模型最终回答的 QA 质量，不读取、不评分、不归因任何过程字段。

## 协议边界

只允许使用以下信息作为评分、证据和结论依据：
- `case_id`
- 用户问题
- 自研模型标识
- 竞品模型标识
- 自研模型最终回答
- 竞品模型最终回答

若原始输入中包含 `context`、用户画像、历史提问、持仓记录、`chain`、`tools`、`plan`、`function_call`、`tool_output`、耗时或其他过程字段，必须忽略；不得把它们作为评分、证据、归因、比较结论或优缺点来源。

如果最终回答有问题，只描述问题在回答文本中的表现，例如投资场景识别错误、证据浅层或过时、核心投资逻辑缺失、方法错位、缺少量化比较、行动建议不可执行、未处理用户在问题中明示的画像/亏损/情绪处境、模板化表达等。不得判断缺陷来自模型、数据源或其他过程因素。

## 适用范围

仅在以下条件同时满足时使用：
- 题目属于分析评价类金融问答，包括股票、指数、基金、ETF、宏观资产、行业题材、消息面、估值、持仓去留、仓位控制、切换、解套、适合我买什么等分析、评价、诊断或决策支持任务；
- 输入中存在同一 `case_id` 对应的两份记录；
- 两份记录分别代表自研模型与一个竞品模型；
- 当前任务目标是比较双方最终回答谁更好、各自好坏、以及竞品答案中值得学习的优点。

不适用于：
- 单模型质检；
- 不同问题之间的横向比较；
- 一次同时比较多个竞品模型；
- 纯条件选股、纯行情查询、客服问题、图片搜索或不需要投资分析的简单事实查询；
- 需要诊断过程能力或失败来源的评测。

若用户问题混合了筛选、分析和推荐，以用户是否要求解释、判断、评价、个人化适配或决策支持为准。若问题明显属于专门的 KYC 推荐建议评测，可优先使用 `05-kyc-recommendation-suggestions`；本 skill 仍覆盖分析评价中夹带的“适合我/我的持仓/我的风险目标”类最终回答质量缺口。

## 最终回答读取规则

- 自研模型：优先读取 `self_record.text_answer`；若为空，可读取 `self_record.answer`。
- 竞品模型：优先读取 `competitor_record.text_answer`；若为空，可读取 `competitor_record.answer`。
- 若存在归一化字段，可读取 `normalized.self_final_answer` 与 `normalized.competitor_final_answer`。
- 证据必须通过 pointer 回指上述最终回答字段或 `question`，不能回指任何过程字段或上下文字段。

## 评估流程

0. **校验同题**
   校验 `case_id`、用户问题和 pairing 是否一致。若 `same_question_verified=false`，不得输出胜负结论。



1. **识别题目类别与核心任务**
   判断用户真正要什么：查数、计算、诊股、选股、资讯解释、投资建议、KYC 适配、复合意图、澄清需求等。
   不要只按表面词判断，要看用户最终需要的决策产物。
   将类别记录到输出的 `category`，将核心意图记录到 `core_user_intent`。

2. **建立共享评估框架**
   阅读 [references/rubric/_index.md](references/rubric/_index.md)、[references/rubric/expert_answer_patterns.md](references/rubric/expert_answer_patterns.md)、活跃维度文件与 [references/golden_cases/_index.md](references/golden_cases/_index.md)。仅依据用户问题判断维度适用性并分配动态权重。同一题下，自研与竞品必须使用同一套维度和权重。

3. **分别做绝对评分**
   对自研最终回答和竞品最终回答分别按以下 10 个答案质量维度评分：
   - `intent_scenario_recognition`
   - `evidence_source_quality`
   - `recency_time_boundary`
   - `investment_logic_depth`
   - `method_fit`
   - `comparison_quantification`
   - `actionability_risk`
   - `user_profile_suitability`
   - `scenario_emotion_recognition`
   - `composition_credibility`

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
- 投资场景识别：是否准确识别用户是问买卖、持有、切换、归因、估值、消息面、基金诊断、资产配置还是个人化建议。
- 证据来源质量：是否提供与问题匹配的专业证据类型，如最新消息、公告、研报、财报、估值、资金、行业景气、同类比较或风险变量。
- 时效边界：是否处理“现在”“最近”“今天”“最近三天”、题材发酵窗口、宏观环境和过时信息风险。
- 投资逻辑深度：是否从信息罗列进入因果链、投资主线、业务/估值/资金/情绪传导和多情景推演。
- 方法匹配：题材票、价值股、基金、ETF、宏观资产、长线持有、短线交易、浮亏解套应使用不同分析框架。
- 对比量化：是否给出同类、指数、历史分位、估值、回撤、风险收益、业务纯度或替代标的对比。
- 可执行性与风险：是否给出仓位、条件、触发点、止损/止盈、观察指标、风险边界，而不是泛泛“看好/谨慎”。
- 用户画像适配：若用户问题明示风险目标、资金规模、持仓成本、投资期限或“适合我”，答案是否据此约束建议；若缺少画像，是否说明依据不足并分层假设或追问。
- 场景与情绪识别：对浮亏、套牢、腰斩、迷茫、急于回本等信号，是否优先降风险、重建纪律，而不是直接推荐高风险短线机会。
- 表达可信度：是否避免模板化堆砌、绝对化断言、低密度长答案和无证据结论。

金融分析类答案还必须检查：
- 消息面和题材问题不能用长期背景科普替代当前催化。
- “可以买吗/要不要持有/是否切换”必须给条件化动作和风险边界。
- 基金/ETF 诊断不能只列收益，必须覆盖回撤、风格、持仓、同类对比和适配边界。
- 个股深度分析不能千股一面；要识别题材、机构成长、价值、周期、避险分红或事件驱动等主线。
- 画像不明或处于亏损焦虑时，不能默认推荐窄行业、高波动主题、单票重仓或短线追涨。


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
- 核心投资逻辑、证据、时效、方法、可执行动作、用户适配任一关键环节错误，都不能被流畅表达或长篇结构掩盖。
- 双方都差时，优先写 `shared_failures`。
- 自研优势必须同时满足：自研最终回答相对竞品更好、自研本身达到该维度基本标准、有自研最终回答证据。
- 竞品优点只写竞品最终回答中值得学习的地方。

## 参考索引

通过 [references/MANIFEST.md](references/MANIFEST.md) 按需读取子文件。
