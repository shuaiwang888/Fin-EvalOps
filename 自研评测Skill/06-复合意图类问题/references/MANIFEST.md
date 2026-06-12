# 复合意图评测 skill 参考清单

## 主协议

- [../SKILL_zh.md](../SKILL_zh.md)：评测执行协议、适用范围、输入假设和保守评分原则。

## 输出规范

- [output-schema_zh.md](output-schema_zh.md)：沿用 self_judge JSON schema，`schema_version` 为 `compound-intent/v1`。

## 评分细则

- [rubric/_index.md](rubric/_index.md)：维度池、动态权重和封顶索引。
- [rubric/raw-score-scale.md](rubric/raw-score-scale.md)：六档原始分量表（0/20/40/60/80/100）。
- [rubric/intent_decomposition.md](rubric/intent_decomposition.md)
- [rubric/task_coverage_priority.md](rubric/task_coverage_priority.md)
- [rubric/multi_source_evidence_integration.md](rubric/multi_source_evidence_integration.md)
- [rubric/analysis_chain_closure.md](rubric/analysis_chain_closure.md)
- [rubric/data_logic_rigor.md](rubric/data_logic_rigor.md)
- [rubric/decision_actionability.md](rubric/decision_actionability.md)
- [rubric/composition_readability.md](rubric/composition_readability.md)
- [rubric/tool_usage.md](rubric/tool_usage.md)
- [rubric/latency_efficiency.md](rubric/latency_efficiency.md)

## 封顶规则

- [rubric/cap_missed_major_subtask.md](rubric/cap_missed_major_subtask.md)
- [rubric/cap_data_or_case_unreliable.md](rubric/cap_data_or_case_unreliable.md)
- [rubric/cap_calculation_or_time_window_error.md](rubric/cap_calculation_or_time_window_error.md)
- [rubric/cap_information_pile_without_synthesis.md](rubric/cap_information_pile_without_synthesis.md)
- [rubric/cap_missing_required_decision_output.md](rubric/cap_missing_required_decision_output.md)
- [rubric/cap_wrong_or_shallow_evidence_mix.md](rubric/cap_wrong_or_shallow_evidence_mix.md)
- [rubric/cap_severe_latency_without_quality_gain.md](rubric/cap_severe_latency_without_quality_gain.md)

## 专家案例

- [golden_cases/_index.md](golden_cases/_index.md)：10 个专家案例基准和 hard checks。
- [golden_cases/image_output_anchors.md](golden_cases/image_output_anchors.md)：从问财/豆包截图和人工批注提取的好答案、差答案、封顶和归因锚点。

## 根因归因

- [root-cause/_index.md](root-cause/_index.md)
- [root-cause/intent.md](root-cause/intent.md)
- [root-cause/coverage.md](root-cause/coverage.md)
- [root-cause/evidence.md](root-cause/evidence.md)
- [root-cause/tool.md](root-cause/tool.md)
- [root-cause/data_logic.md](root-cause/data_logic.md)
- [root-cause/reasoning.md](root-cause/reasoning.md)
- [root-cause/composition.md](root-cause/composition.md)
- [root-cause/latency.md](root-cause/latency.md)

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
