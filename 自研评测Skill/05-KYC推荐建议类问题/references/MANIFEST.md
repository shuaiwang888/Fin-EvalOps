# KYC 推荐建议评测 skill 参考清单

## 主协议

- [../SKILL_zh.md](../SKILL_zh.md)：评测执行协议、适用范围、输入假设和保守评分原则。

## 输出规范

- [output-schema_zh.md](output-schema_zh.md)：沿用 self_judge JSON schema，`schema_version` 为 `kyc-recommendation-suggestions/v1`。

## 评分细则

- [rubric/_index.md](rubric/_index.md)：维度池、动态权重、运行时维度和封顶索引。
- [rubric/raw-score-scale.md](rubric/raw-score-scale.md)：0/20/40/60/80/100 六档原始分量表。
- [rubric/intent_profile_understanding.md](rubric/intent_profile_understanding.md)
- [rubric/scenario_emotion_recognition.md](rubric/scenario_emotion_recognition.md)
- [rubric/suitability_personalization.md](rubric/suitability_personalization.md)
- [rubric/evidence_integration.md](rubric/evidence_integration.md)
- [rubric/decision_actionability.md](rubric/decision_actionability.md)
- [rubric/risk_boundary_control.md](rubric/risk_boundary_control.md)
- [rubric/product_universe_fit.md](rubric/product_universe_fit.md)
- [rubric/recommendation_stability.md](rubric/recommendation_stability.md)
- [rubric/composition_credibility.md](rubric/composition_credibility.md)
- [rubric/tool_usage.md](rubric/tool_usage.md)

## 封顶规则

- [rubric/cap_missing_kyc_profile.md](rubric/cap_missing_kyc_profile.md)
- [rubric/cap_misread_emotional_loss_context.md](rubric/cap_misread_emotional_loss_context.md)
- [rubric/cap_fabricated_user_profile.md](rubric/cap_fabricated_user_profile.md)
- [rubric/cap_missing_action_for_decision_request.md](rubric/cap_missing_action_for_decision_request.md)
- [rubric/cap_missing_required_evidence.md](rubric/cap_missing_required_evidence.md)
- [rubric/cap_overconfident_or_unsuitable_recommendation.md](rubric/cap_overconfident_or_unsuitable_recommendation.md)
- [rubric/cap_template_generic_advice.md](rubric/cap_template_generic_advice.md)

## 专家案例

- [golden_cases/_index.md](golden_cases/_index.md)：13 个专家案例基准和 hard checks。
- [golden_cases/image_annotation_anchors.md](golden_cases/image_annotation_anchors.md)：docx 截图红绿批注沉淀的私人投顾感、产品池、稳定性、情绪场景和可执行动作 hard checks。

## 根因归因

- [root-cause/_index.md](root-cause/_index.md)
- [root-cause/intent.md](root-cause/intent.md)
- [root-cause/context.md](root-cause/context.md)
- [root-cause/evidence.md](root-cause/evidence.md)
- [root-cause/tool.md](root-cause/tool.md)
- [root-cause/reasoning.md](root-cause/reasoning.md)
- [root-cause/composition.md](root-cause/composition.md)
- [root-cause/safety_or_compliance.md](root-cause/safety_or_compliance.md)

## 工具列表

工具列表直接复用 `00-event-and-concept-stock-selection` 的工具定义，已复制到当前目录：
- [tool_list/_index.md](tool_list/_index.md)
- [tool_list/search.md](tool_list/search.md)
- [tool_list/finquery.md](tool_list/finquery.md)
- [tool_list/backtest.md](tool_list/backtest.md)
- [tool_list/forecast.md](tool_list/forecast.md)
- [tool_list/accessingfulltext.md](tool_list/accessingfulltext.md)
- [tool_list/searchimage.md](tool_list/searchimage.md)
- [tool_list/customerservicefaq.md](tool_list/customerservicefaq.md)
- [tool_list/saveuserprofile.md](tool_list/saveuserprofile.md)
- [tool_list/codeinterpreter.md](tool_list/codeinterpreter.md)
