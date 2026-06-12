# 参考文件导航

## 主流程

- `../SKILL.md` / `../SKILL_zh.md`：主评测协议。
- `output-schema_zh.md`：完整 JSON 输出格式。
- `output-schema_round1_zh.md`：轻量盲评输出格式。

## Rubric

- `rubric/_index.md`：维度、动态权重、适用性和封顶规则入口。
- `rubric/raw-score-scale.md`：0/20/40/60/80/100 六档分数标准。
- `rubric/intent_fulfillment.md`
- `rubric/ambiguity_clarification.md`
- `rubric/context_continuity.md`
- `rubric/entity_resolution.md`
- `rubric/financial_rule_and_premise.md`
- `rubric/assumption_definition.md`
- `rubric/actionability_and_risk_plan.md`
- `rubric/evidence_grounding.md`
- `rubric/guidance_and_retention.md`
- `rubric/tool_usage.md`
- `rubric/latency_efficiency.md`
- `rubric/cap_wrong_financial_rule_or_unhandled_invalid_premise.md`
- `rubric/cap_wrong_entity_resolution.md`
- `rubric/cap_fabricated_or_unsupported_specific_advice.md`
- `rubric/cap_context_break_after_clarification.md`
- `rubric/cap_missing_required_clarification.md`
- `rubric/cap_inconsistent_time_or_definition_scope.md`
- `rubric/cap_generic_template_without_clarification_value.md`

## 专家案例

- `golden_cases/_index.md`：07 文档 41 个专家案例 hard checks 和跨案例判分锚点。
- `golden_cases/image_annotation_anchors.md`：docx 图片批注中的红框/绿框专家知识锚点。

## 根因与工具

- `root-cause/_index.md`：根因选择流程和 L1/L2 分类入口。
- `root-cause/intent.md`
- `root-cause/context.md`
- `root-cause/evidence.md`
- `root-cause/tool.md`
- `root-cause/reasoning.md`
- `root-cause/composition.md`
- `tool_list/_index.md`：可用工具评分参考。
