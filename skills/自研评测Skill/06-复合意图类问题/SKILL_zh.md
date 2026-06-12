---
name: compound-intent
description: 用于评测自研模型在复合意图类金融问题上的最终答案和完整链路质量。适用于一句话包含多个子任务、跨行情/新闻/公告/产业/政策/财务/交易策略的信息整合、复杂推演、深度调研、事件影响评估、热点择股和衍生品交易方案等场景，输入包括用户 query、context、plan、工具调用输入输出、耗时证据和最终回答，输出与 self_judge 体系一致的 JSON 评测结果。
---

# 复合意图类问题评测协议

用稳定协议评测我方模型在复合意图类金融问题上的表现。以用户问题和最终答案 `text_answer` 为评分主锚点，以完整链路数据用于解释问题发生在哪里；`tool_usage` 和 `latency_efficiency` 可使用链路与耗时证据评分。

## 适用范围

仅在用户问题属于复合意图或复杂投研推理任务时使用，包括：
- 一句话包含多个子任务、多个时间窗口、多个资产/公司/行业或多个输出要求
- 复杂问句，尤其是字数较长、包含“现状/未来/影响/传导/策略/标的/估值/利润/案例/怎么做”等多层要求
- 深度调研、行业竞争格局、产业链映射、事件影响评估、热点板块归纳、复杂交易方案
- 需要把行情、新闻、公告、产业、政策、财务、资金、舆情等多源信息串成统一投资结论

不用于纯单一意图的行情查询、单步取数计算、普通 KYC 推荐、简单事件概念选股或客服问题。若问题既有单一领域特征又包含多个强子任务，以“是否需要拆解、整合、推演并输出决策闭环”为准。

## 期望输入

每次评测获取以下材料：
- 用户问题 `question`
- 我方最终答案，优先使用 `text_answer`
- 完整对话上下文 `context`
- 完整规划链路 `chain`，包括 `plan`、工具调用、工具输入和工具输出
- 可用工具清单 `tools`
- 可选响应耗时、工具调用时间戳或每步耗时
- 可选线上维度信号 `online_dimension_signals`，如近期线上失败样本、用户反馈、人工标注摘要或维度统计

## 执行协议

0. **拆解复合任务并分配动态权重**
   先阅读 [references/rubric/_index.md](references/rubric/_index.md) 和 [references/golden_cases/_index.md](references/golden_cases/_index.md)。
   若题目命中 10 个专家样例、或输入里包含问财/豆包截图 OCR、人工批注、竞品对比摘要，继续读取 [references/golden_cases/image_output_anchors.md](references/golden_cases/image_output_anchors.md)，用其中的“好答案/差答案”锚点校准评分。
   仅根据 `question`、必要 `context` 和已提供的线上维度信号，抽取子任务清单、主次关系、证据需求、时间窗口、量化要求、决策输出要求和效率要求。
   不要先把问题强行归入固定题型；主题只用于检索专家案例、hard checks 和封顶规则。
   对维度判断适用性：
   - `relevant`：本题核心判断依据
   - `supplementary`：有参考价值但不是主矛盾
   - `not_applicable`：该维度与题目无关，跳过评分
   动态权重总和必须为 100，并记录到输出的 `weight_assignment`。若线上数据暴露的关键缺口无法被现有维度清楚覆盖，可新增临时评分维度，并直接并入 `weight_assignment` 与 `dimension_scores`。
   命中专家案例或同类语义时，必须使用对应 hard checks。

1. **盲评最终答案**
   以 `text_answer` 为主锚点评分，不因为隐藏链路更好而给最终答案加分。
   对所有 `relevant` 和 `supplementary` 维度输出 `raw_score`，不要计算加权分或总分。
   例外：`tool_usage` 需要阅读链路，在步骤 2 中评分；`latency_efficiency` 可使用耗时证据，若无耗时证据则给中性分并说明证据缺口。

2. **链路诊断和根因归因**
   阅读 [references/root-cause/_index.md](references/root-cause/_index.md)。
   再阅读 [references/tool_list/_index.md](references/tool_list/_index.md)，按需读取具体工具规则。
   用 `chain.plan` 判断是否正确拆解子任务、排序主次和编排信息源；用 `chain.tools[*].input/output` 判断工具选择、时间窗口、证据质量、数据口径和是否误读结果。
   此时评分 `tool_usage`。
   根因必须回答：如果答案不好，具体问题发生在意图拆解、任务覆盖、证据、工具、数据口径、推理闭环、表达还是效率。

3. **应用封顶规则**
   按需读取 [references/rubric/](references/rubric/_index.md) 中的 `cap_*.md` 文件。
   封顶规则限制最终分，不替代维度评分。若多个封顶同时触发，取最低上限。

4. **序列化输出**
   阅读 [references/output-schema_zh.md](references/output-schema_zh.md)。
   先输出结构化 JSON，再附简短自然语言评审。

## 保守评分

- 最终答案决定用户侧质量，链路只用于归因。
- 不要把“回答很长、表格很多、工具调用很多”自动视为高质量。
- 复合意图的第一性目标是：识别所有关键子任务，按主次组织答案，并把事实、影响、传导和策略形成闭环。
- 截图型或 OCR 型输入中若出现人工批注（如“口径存在偏差”“数据错误”“案例失实”“操作建议模糊”），必须把批注作为高优先级专家信号；除非最终答案或链路证据能明确推翻批注，否则不要忽略。
- 严惩漏答关键子任务、用资料拼盘替代综合结论、数据口径错误、案例失实、时间窗口错配、结论没有操作价值。
- 对复杂任务要同时记录效率。若耗时极长但结果没有明显质量收益，应暴露 `latency_efficiency` 问题。

## 参考索引

通过 [references/MANIFEST.md](references/MANIFEST.md) 按需读取子文件。工具列表直接复用事件概念选股 skill 的工具定义，当前复制在 [references/tool_list/_index.md](references/tool_list/_index.md)。
