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
| [intent_fulfillment.md](rubric/intent_fulfillment.md) | 意图满足度维度 | 判断适用性与评分 |
| [data_accuracy_coverage.md](rubric/data_accuracy_coverage.md) | 数据准确性与覆盖维度 | 判断适用性与评分 |
| [time_caliber_precision.md](rubric/time_caliber_precision.md) | 时间、口径与粒度维度 | 判断适用性与评分 |
| [calculation_comparison.md](rubric/calculation_comparison.md) | 计算与对比维度 | 判断适用性与评分 |
| [analysis_framework_fit.md](rubric/analysis_framework_fit.md) | 市场分析框架匹配度维度 | 判断适用性与评分 |
| [insight_extension.md](rubric/insight_extension.md) | 延伸洞察与增量信息维度 | 判断适用性与评分 |
| [result_verifiability.md](rubric/result_verifiability.md) | 结果可验证性维度 | 判断适用性与评分 |
| [presentation_visualization.md](rubric/presentation_visualization.md) | 呈现与可视化维度 | 判断适用性与评分 |
| [cap_hard_data_or_fact_error.md](rubric/cap_hard_data_or_fact_error.md) | 质量标签：硬性数据/事实错误 | 触发质量标签时 |
| [cap_missing_required_data.md](rubric/cap_missing_required_data.md) | 质量标签：必要数据缺失 | 触发质量标签时 |
| [cap_time_or_caliber_error.md](rubric/cap_time_or_caliber_error.md) | 质量标签：时间/口径错误 | 触发质量标签时 |
| [cap_intraday_precision_missing.md](rubric/cap_intraday_precision_missing.md) | 质量标签：日内精度缺失 | 触发质量标签时 |
| [cap_wrong_analysis_framework.md](rubric/cap_wrong_analysis_framework.md) | 质量标签：分析框架错误 | 触发质量标签时 |
| [cap_data_dump_without_insight.md](rubric/cap_data_dump_without_insight.md) | 质量标签：数据堆砌无洞察 | 触发质量标签时 |
| [cap_unverifiable_or_fabricated_result.md](rubric/cap_unverifiable_or_fabricated_result.md) | 质量标签：不可验证或疑似编造 | 触发质量标签时 |

## 专家案例基准（golden_cases/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](golden_cases/_index.md) | 21 个专家案例 hard checks 与跨案例判分锚点 | 步骤 1 分析题目时读取 |
| [image_annotation_anchors.md](golden_cases/image_annotation_anchors.md) | 截图/图表沉淀的最终回答呈现、好坏答案特征和可视化锚点 | 题目涉及图表、截图、多周期展示或表格呈现时读取 |

## 输出契约

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [output-schema_round1_zh.md](output-schema_round1_zh.md) | Round 1：同题校验、共享权重、双方最终回答证据摘要 | 步骤 1 后 |
| [output-schema_zh.md](output-schema_zh.md) | Pairwise JSON 输出契约、证据对象和比较结论格式 | 序列化时 |

## 协议步骤到文件的映射

| 协议步骤 | 操作 | 读取文件 |
|---|---|---|
| 步骤 0：校验同题 | case_id 与问题一致性校验 | `SKILL_zh.md` |
| 步骤 1：建立共享评估框架 | 维度适用性 + 动态权重 + 案例命中 | `rubric/_index.md` + 活跃维度文件 + `golden_cases/_index.md` |
| 步骤 2：分别做绝对评分 | 最终回答逐维评分 + 质量标签检查 | 活跃维度文件 + `rubric/raw-score-scale.md` + 对应 `rubric/cap_*.md` 文件 |
| 步骤 3：逐维比较 | 输出自研优势/弱点、竞品优点、共同失败点 | `comparison_protocol.md` |
| 步骤 4：序列化输出 | 双边绝对评分 + 逐维比较 + 总结结论 | `output-schema_zh.md` |
