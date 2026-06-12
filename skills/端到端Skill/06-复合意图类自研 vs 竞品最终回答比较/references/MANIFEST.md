# 参考文件索引

本目录只导航 result-only 最终回答比较评估需要的文件。评分、证据、优缺点和最终结论只能来自用户问题与双方最终回答。

## 主协议

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [../SKILL_zh.md](../SKILL_zh.md) | 定义 result-only 自研 vs 竞品最终回答比较协议 | 开始评测前必读 |
| [comparison_protocol.md](comparison_protocol.md) | 定义先绝对后相对、逐维比较、优势/缺点/共同失败点判定规则 | 逐维比较前必读 |

## 评分细则（rubric/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](rubric/_index.md) | 维度列表、动态权重分配、质量标签规则、证据边界 | 步骤 1 分析题目前通读 |
| [raw-score-scale.md](rubric/raw-score-scale.md) | 0/20/40/60/80/100 原始分锚点 | 评分前必读 |
| [intent_decomposition.md](rubric/intent_decomposition.md) | 意图拆解 | 判断适用性与评分 |
| [task_coverage_priority.md](rubric/task_coverage_priority.md) | 子任务覆盖与主次 | 判断适用性与评分 |
| [multi_source_evidence_integration.md](rubric/multi_source_evidence_integration.md) | 多源证据整合 | 判断适用性与评分 |
| [analysis_chain_closure.md](rubric/analysis_chain_closure.md) | 分析链路闭环 | 判断适用性与评分 |
| [data_logic_rigor.md](rubric/data_logic_rigor.md) | 数据与逻辑严谨性 | 判断适用性与评分 |
| [decision_actionability.md](rubric/decision_actionability.md) | 决策表达与可执行性 | 判断适用性与评分 |
| [composition_readability.md](rubric/composition_readability.md) | 结构与可读性 | 判断适用性与评分 |
| [cap_missed_major_subtask.md](rubric/cap_missed_major_subtask.md) | 质量标签：遗漏主要子任务 | 触发质量标签时 |
| [cap_data_or_case_unreliable.md](rubric/cap_data_or_case_unreliable.md) | 质量标签：数据或案例不可靠 | 触发质量标签时 |
| [cap_calculation_or_time_window_error.md](rubric/cap_calculation_or_time_window_error.md) | 质量标签：计算或时间窗口错误 | 触发质量标签时 |
| [cap_information_pile_without_synthesis.md](rubric/cap_information_pile_without_synthesis.md) | 质量标签：信息堆砌无综合 | 触发质量标签时 |
| [cap_missing_required_decision_output.md](rubric/cap_missing_required_decision_output.md) | 质量标签：遗漏必要决策输出 | 触发质量标签时 |
| [cap_wrong_or_shallow_evidence_mix.md](rubric/cap_wrong_or_shallow_evidence_mix.md) | 质量标签：证据组合错误或浅层 | 触发质量标签时 |

## 专家案例基准（golden_cases/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](golden_cases/_index.md) | 10 个专家案例 hard checks 和典型失败模式 | 步骤 1 分析题目时读取 |
| [image_output_anchors.md](golden_cases/image_output_anchors.md) | 人工批注沉淀的复合意图答案质量锚点 | 步骤 1 分析题目时读取 |

## 输出契约

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [output-schema_round1_zh.md](output-schema_round1_zh.md) | Round 1：同题校验、共享权重、双方最终回答证据摘要 | 步骤 1 后 |
| [output-schema_zh.md](output-schema_zh.md) | Pairwise JSON 输出契约、证据对象和比较结论格式 | 序列化时 |

## 协议步骤到文件的映射

| 协议步骤 | 操作 | 读取文件 |
|---|---|---|
| 步骤 0：校验同题 | case_id 与问题一致性校验 | `SKILL_zh.md` |
| 步骤 1：建立共享评估框架 | 维度适用性 + 动态权重 + 案例命中 | `rubric/_index.md` + 活跃维度文件 + `golden_cases/_index.md` + `golden_cases/image_output_anchors.md` |
| 步骤 2：分别做绝对评分 | 最终回答逐维评分 + 质量标签检查 | 活跃维度文件 + `rubric/raw-score-scale.md` + 对应 `rubric/cap_*.md` 文件 |
| 步骤 3：逐维比较 | 输出自研优势/弱点、竞品优点、共同失败点 | `comparison_protocol.md` |
| 步骤 4：序列化输出 | 双边绝对评分 + 逐维比较 + 总结结论 | `output-schema_zh.md` |
