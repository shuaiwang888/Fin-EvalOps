# 参考文件索引

本文件是交互澄清自研 vs 竞品比较评测协议的导航地图。

- **绝对评分层**：rubric、golden cases、root cause、tool list 提供单模型绝对评分标准，沿用 `07-interactive-clarification`。
- **compare 专属层**：comparison protocol 与 whole-chain comparison 负责定义同题比较和整体链路差异解释。

## compare 专属参考

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [comparison_protocol.md](comparison_protocol.md) | 定义 pairwise 比较流程、先绝对后相对、我方优劣/竞品优点/shared failures 判定规则 | 步骤 3 比较前必读 |
| [whole_chain_comparison.md](whole_chain_comparison.md) | 说明真实输入结构、答案锚点、`chain[*].tools[*]` 读取路径和整体链路差异解释方法 | 步骤 2 链路诊断前必读 |

## 评分细则（rubric/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](rubric/_index.md) | 维度列表 + 动态权重分配规则 + 封顶规则注意事项 | 步骤 0 分析题目前通读 |
| [raw-score-scale.md](rubric/raw-score-scale.md) | 0/20/40/60/80/100 六档分数标准 | 评分前必读 |
| [intent_fulfillment.md](rubric/intent_fulfillment.md) | 意图满足度维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [ambiguity_clarification.md](rubric/ambiguity_clarification.md) | 模糊意图澄清维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [context_continuity.md](rubric/context_continuity.md) | 多轮承接闭环维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [entity_resolution.md](rubric/entity_resolution.md) | 标的与语义纠错维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [financial_rule_and_premise.md](rubric/financial_rule_and_premise.md) | 金融规则与前提纠错维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [assumption_definition.md](rubric/assumption_definition.md) | 假设口径与条件定义维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [actionability_and_risk_plan.md](rubric/actionability_and_risk_plan.md) | 澄清后落地与风险边界维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [evidence_grounding.md](rubric/evidence_grounding.md) | 事实证据与数据支撑维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [guidance_and_retention.md](rubric/guidance_and_retention.md) | 后续引导闭环维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [tool_usage.md](rubric/tool_usage.md) | 工具使用合理性维度 | 步骤 0 判断适用性 + 步骤 2 评分 |
| [latency_efficiency.md](rubric/latency_efficiency.md) | 响应耗时与执行效率维度 | 步骤 0 判断适用性 + 步骤 1/2 评分 |
| [cap_wrong_financial_rule_or_unhandled_invalid_premise.md](rubric/cap_wrong_financial_rule_or_unhandled_invalid_premise.md) | 封顶规则：金融规则错误或错误前提未纠正 | 步骤 1/2 封顶时 |
| [cap_wrong_entity_resolution.md](rubric/cap_wrong_entity_resolution.md) | 封顶规则：标的识别错误 | 步骤 1/2 封顶时 |
| [cap_fabricated_or_unsupported_specific_advice.md](rubric/cap_fabricated_or_unsupported_specific_advice.md) | 封顶规则：缺证据的具体交易建议 | 步骤 1/2 封顶时 |
| [cap_context_break_after_clarification.md](rubric/cap_context_break_after_clarification.md) | 封顶规则：澄清后二轮承接断裂 | 步骤 1/2 封顶时 |
| [cap_missing_required_clarification.md](rubric/cap_missing_required_clarification.md) | 封顶规则：遗漏必要澄清 | 步骤 1/2 封顶时 |
| [cap_inconsistent_time_or_definition_scope.md](rubric/cap_inconsistent_time_or_definition_scope.md) | 封顶规则：时间或定义口径不一致 | 步骤 1/2 封顶时 |
| [cap_generic_template_without_clarification_value.md](rubric/cap_generic_template_without_clarification_value.md) | 封顶规则：模板化答复无咨询价值 | 步骤 1/2 封顶时 |

## 专家案例基准（golden_cases/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](golden_cases/_index.md) | 07 文档 41 个专家案例 hard checks + 跨案例判分锚点 | 步骤 0 分析题目时读取，用于命中检测 |
| [image_annotation_anchors.md](golden_cases/image_annotation_anchors.md) | docx 图片人工批注补充锚点：截图批注、模型答复高亮、上下文承接、首轮澄清和二轮落地差异 | 步骤 0 与 `_index.md` 一并读取 |

## 根因归因体系（root-cause/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](root-cause/_index.md) | 链路阶段、证据规则、置信度规则、选择规则 | 步骤 2 诊断前通读 |
| [intent.md](root-cause/intent.md) | L1: intent — 真实咨询目标、隐含需求、子问题遗漏 | 步骤 2 归因时 |
| [context.md](root-cause/context.md) | L1: context — 多轮承接、用户补充、前轮承诺 | 步骤 2 归因时 |
| [evidence.md](root-cause/evidence.md) | L1: evidence — 实体、规则、行情、公告、数据证据 | 步骤 2 归因时 |
| [tool.md](root-cause/tool.md) | L1: tool — 工具选择、参数、候选验证、链路效率 | 步骤 2 归因时 |
| [reasoning.md](root-cause/reasoning.md) | L1: reasoning — 错误前提、规则推理、口径定义、因果顺序 | 步骤 2 归因时 |
| [composition.md](root-cause/composition.md) | L1: composition — 答案组织、直接回答、模板化、后续引导 | 步骤 2 归因时 |

## 工具列表（tool_list/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](tool_list/_index.md) | 完整工具总览列表（名称 + 功能描述）和 07 场景补充规则 | 步骤 2 评分 tool_usage 前必读 |
| [search.md](tool_list/search.md) | Search 搜索工具用法规则 | 按需 |
| [finquery.md](tool_list/finquery.md) | FinQuery 金融查询工具用法规则 | 按需 |
| [customerservicefaq.md](tool_list/customerservicefaq.md) | CustomerServiceFAQ 客服/交易规则工具用法规则 | 按需 |
| [accessingfulltext.md](tool_list/accessingfulltext.md) | AccessingFullText 全文读取工具用法规则 | 按需 |
| [backtest.md](tool_list/backtest.md) | BackTest 回测工具用法规则 | 按需 |
| [forecast.md](tool_list/forecast.md) | Forecast 预测工具用法规则 | 按需 |
| [saveuserprofile.md](tool_list/saveuserprofile.md) | SaveUserProfile 用户画像/偏好保存工具用法规则 | 按需 |
| [searchimage.md](tool_list/searchimage.md) | SearchImage 图片搜索工具用法规则 | 按需 |
| [codeinterpreter.md](tool_list/codeinterpreter.md) | CodeInterpreter 计算工具用法规则 | 按需 |

## 输出契约

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [output-schema_round1_zh.md](output-schema_round1_zh.md) | Round 1：同题校验、共享权重、两边证据摘要 | 步骤 0 后 |
| [output-schema_zh.md](output-schema_zh.md) | Pairwise JSON 输出契约、双边证据对象和比较结论格式 | 步骤 4 序列化时 |

## 关键依赖

- 步骤 0 题目分析 → 依赖 `rubric/_index.md`（维度列表 + 适用性指南）+ 各维度文件（`## 适用性判断`）+ `golden_cases/_index.md` + `golden_cases/image_annotation_anchors.md`
- `tool_usage` 维度评分 → 依赖 `tool_list/_index.md` + 各工具详细规则；真实工具调用从 `chain[*].tools[*]` 读取
- 根因 L2 的“典型受影响维度”列 → 反向映射到 rubric 各维度文件
- 封顶规则触发 → 影响根因选择规则（`root-cause/_index.md` 选择规则第 1 步）

## 协议步骤到文件的映射

| 协议步骤 | 操作 | 读取文件 |
|---|---|---|
| 步骤 0：分析题目 | 适用性判断 + 动态权重 + 案例命中 | `rubric/_index.md` + 各维度文件 `## 适用性判断` + `golden_cases/_index.md` + `golden_cases/image_annotation_anchors.md` |
| 步骤 1：分别做绝对评分 | 逐维度评分（仅活跃维度）+ 封顶检查 | `rubric/_index.md` + 各维度文件 + `rubric/raw-score-scale.md` + 对应 `rubric/cap_*.md` 文件 |
| 步骤 2：诊断整体链路 | tool_usage 评分 + 整体链路差异解释 + 根因选择 | `whole_chain_comparison.md` + `rubric/tool_usage.md` + `tool_list/_index.md` + 相关工具文件 + `root-cause/_index.md` + 对应 L1 文件 |
| 步骤 3：逐维比较 | 先绝对后相对，输出我方优势/弱点、竞品优点、shared failures | `comparison_protocol.md` |
| 步骤 4：序列化输出 | 双边绝对评分 + 逐维比较 + 自然语言 | `output-schema_zh.md` |
