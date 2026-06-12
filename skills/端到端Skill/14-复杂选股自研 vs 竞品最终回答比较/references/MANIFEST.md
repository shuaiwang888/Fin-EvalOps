# 参考文件索引

本目录只导航 result-only 最终回答比较评估需要的文件。评分、证据、优缺点和最终结论只能来自用户问题与双方最终回答。

## 主协议

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [../SKILL_zh.md](../SKILL_zh.md) | 定义复杂选股 result-only 自研 vs 竞品最终回答比较协议 | 开始评测前必读 |
| [comparison_protocol.md](comparison_protocol.md) | 定义先绝对后相对、逐维比较、优势/缺点/共同失败点判定规则 | 逐维比较前必读 |

## 评分细则（rubric/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](rubric/_index.md) | 维度列表、动态权重分配、质量标签规则、证据边界 | 步骤 1 分析题目前通读 |
| [raw-score-scale.md](rubric/raw-score-scale.md) | 0/20/40/60/80/100 分制 | 评分前必读 |
| [intent_condition_extraction.md](rubric/intent_condition_extraction.md) | 意图与条件抽取维度 | 判断适用性与评分 |
| [financial_semantics_and_caliber.md](rubric/financial_semantics_and_caliber.md) | 金融语义与口径维度 | 判断适用性与评分 |
| [screening_plan_decomposition.md](rubric/screening_plan_decomposition.md) | 筛选规划拆解维度 | 判断适用性与评分 |
| [result_correctness_and_coverage.md](rubric/result_correctness_and_coverage.md) | 结果正确性与覆盖维度 | 判断适用性与评分 |
| [ranking_and_decision_actionability.md](rubric/ranking_and_decision_actionability.md) | 排序与决策可执行性维度 | 判断适用性与评分 |
| [data_logic_time_boundary.md](rubric/data_logic_time_boundary.md) | 数据逻辑与时间边界维度 | 判断适用性与评分 |
| [composition_credibility.md](rubric/composition_credibility.md) | 表达可信度维度 | 判断适用性与评分 |
| [cap_core_condition_omitted_or_rewritten.md](rubric/cap_core_condition_omitted_or_rewritten.md) | 质量标签：核心条件遗漏或改写 | 触发质量标签时 |
| [cap_hard_financial_semantics_or_caliber_error.md](rubric/cap_hard_financial_semantics_or_caliber_error.md) | 质量标签：硬性金融语义或口径错误 | 触发质量标签时 |
| [cap_unsupported_data_forced_output.md](rubric/cap_unsupported_data_forced_output.md) | 质量标签：不支持数据却强行输出 | 触发质量标签时 |
| [cap_wrong_evidence_strategy.md](rubric/cap_wrong_evidence_strategy.md) | 质量标签：证据或数据依据错误 | 触发质量标签时 |
| [cap_layered_or_temporal_screening_failure.md](rubric/cap_layered_or_temporal_screening_failure.md) | 质量标签：分层或先后筛选失败 | 触发质量标签时 |
| [cap_missing_required_ranking_or_fields.md](rubric/cap_missing_required_ranking_or_fields.md) | 质量标签：遗漏必要排序或字段 | 触发质量标签时 |
| [cap_unverifiable_result_or_data_hallucination.md](rubric/cap_unverifiable_result_or_data_hallucination.md) | 质量标签：结果不可验证或数据幻觉 | 触发质量标签时 |
| [cap_chart_or_table_without_decision_value.md](rubric/cap_chart_or_table_without_decision_value.md) | 质量标签：图表表格无决策价值 | 触发质量标签时 |

## 专家案例基准（golden_cases/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](golden_cases/_index.md) | 40 个专家案例 hard checks 与跨案例判分锚点 | 步骤 1 分析题目时读取 |
| [image_annotation_anchors.md](golden_cases/image_annotation_anchors.md) | docx 图片人工批注补充锚点 | 命中特定批注场景时读取 |

## 输出契约

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [output-schema_round1_zh.md](output-schema_round1_zh.md) | Round 1：同题校验、共享权重、双方最终回答证据摘要 | 步骤 1 后 |
| [output-schema_zh.md](output-schema_zh.md) | Pairwise JSON 输出契约、证据对象和比较结论格式 | 序列化时 |

## 协议步骤到文件的映射

| 协议步骤 | 操作 | 读取文件 |
|---|---|---|
| 步骤 0：校验同题 | case_id 与问题一致性校验 | `SKILL_zh.md` |
| 步骤 1：建立共享评估框架 | 维度适用性 + 动态权重 + 案例命中 | `rubric/_index.md` + 活跃维度文件 + `golden_cases/_index.md` + `golden_cases/image_annotation_anchors.md` |
| 步骤 2：分别做绝对评分 | 最终回答逐维评分 + 质量标签检查 | 活跃维度文件 + `rubric/raw-score-scale.md` + 对应 `rubric/cap_*.md` 文件 |
| 步骤 3：逐维比较 | 输出自研优势/弱点、竞品优点、共同失败点 | `comparison_protocol.md` |
| 步骤 4：序列化输出 | 双边绝对评分 + 逐维比较 + 总结结论 | `output-schema_zh.md` |
