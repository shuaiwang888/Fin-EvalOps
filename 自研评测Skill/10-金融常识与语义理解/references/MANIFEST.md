# 参考文件索引

## 评分细则

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [rubric/_index.md](rubric/_index.md) | 维度列表、动态权重、适用性 | 步骤 0 |
| [rubric/raw-score-scale.md](rubric/raw-score-scale.md) | 六档分制定义（0/20/40/60/80/100） | 步骤 1 |
| [rubric/semantic_intent_alignment.md](rubric/semantic_intent_alignment.md) | 语义意图匹配维度评分细则 | 步骤 1 |
| [rubric/financial_term_understanding.md](rubric/financial_term_understanding.md) | 金融术语/规则理解维度评分细则 | 步骤 1 |
| [rubric/entity_product_boundary.md](rubric/entity_product_boundary.md) | 实体与产品边界维度评分细则 | 步骤 1 |
| [rubric/metric_caliber_accuracy.md](rubric/metric_caliber_accuracy.md) | 指标公式与数据口径维度评分细则 | 步骤 1 |
| [rubric/timeliness_context.md](rubric/timeliness_context.md) | 时效上下文维度评分细则 | 步骤 1 |
| [rubric/credibility_expression.md](rubric/credibility_expression.md) | 可信解释与表达维度评分细则 | 步骤 1 |
| [rubric/tool_usage.md](rubric/tool_usage.md) | 工具使用合理性维度评分细则 | 步骤 2 |
| [rubric/cap_hard_concept_or_rule_error.md](rubric/cap_hard_concept_or_rule_error.md) | 金融概念或规则硬错封顶规则 | 步骤 3 |
| [rubric/cap_wrong_entity_or_product.md](rubric/cap_wrong_entity_or_product.md) | 实体或产品错误封顶规则 | 步骤 3 |
| [rubric/cap_missed_core_definition.md](rubric/cap_missed_core_definition.md) | 遗漏核心定义封顶规则 | 步骤 3 |
| [rubric/cap_metric_caliber_unexplained_or_invalid.md](rubric/cap_metric_caliber_unexplained_or_invalid.md) | 指标口径未解释或无效封顶规则 | 步骤 3 |
| [rubric/cap_stale_or_wrong_time_context.md](rubric/cap_stale_or_wrong_time_context.md) | 时效错误或过时封顶规则 | 步骤 3 |
| [rubric/cap_empty_generic_advice.md](rubric/cap_empty_generic_advice.md) | 空泛通用建议封顶规则 | 步骤 3 |

## 专家案例

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [golden_cases/_index.md](golden_cases/_index.md) | 专家文本案例 hard checks | 步骤 0 |
| [golden_cases/image_annotation_anchors.md](golden_cases/image_annotation_anchors.md) | docx 图片和截图中的补充锚点 | 步骤 0 |

## 根因与工具

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [root-cause/_index.md](root-cause/_index.md) | 根因选择规则 | 步骤 2 |
| [root-cause/intent.md](root-cause/intent.md) | 意图理解根因 | 按需 |
| [root-cause/evidence.md](root-cause/evidence.md) | 信息证据根因 | 按需 |
| [root-cause/tool.md](root-cause/tool.md) | 工具策略根因 | 按需 |
| [root-cause/reasoning.md](root-cause/reasoning.md) | 金融语义推理根因 | 按需 |
| [root-cause/composition.md](root-cause/composition.md) | 答案组织根因 | 按需 |
| [tool_list/_index.md](tool_list/_index.md) | 工具使用评分参考 | 评分 `tool_usage` 前 |

## 输出契约

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [output-schema_zh.md](output-schema_zh.md) | JSON 输出格式 | 步骤 4 |
| [output-schema_round1_zh.md](output-schema_round1_zh.md) | Round 1 分析输出格式 | 步骤 0-1 |
