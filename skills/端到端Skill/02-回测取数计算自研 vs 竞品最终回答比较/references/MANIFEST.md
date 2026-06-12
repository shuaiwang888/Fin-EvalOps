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
| [data_retrieval_accuracy.md](rubric/data_retrieval_accuracy.md) | 取数准确性维度 | 判断适用性与评分 |
| [time_inference.md](rubric/time_inference.md) | 时间推理正确性维度 | 判断适用性与评分 |
| [calculation_accuracy.md](rubric/calculation_accuracy.md) | 计算准确性维度 | 判断适用性与评分 |
| [logical_decomposition.md](rubric/logical_decomposition.md) | 逻辑拆解能力维度 | 判断适用性与评分 |
| [result_verifiability.md](rubric/result_verifiability.md) | 结果可验证性维度 | 判断适用性与评分 |
| [expression_quality.md](rubric/expression_quality.md) | 表达与展示质量维度 | 判断适用性与评分 |
| [cap_data_fabrication.md](rubric/cap_data_fabrication.md) | 质量标签：数据虚构 | 触发质量标签时 |
| [cap_time_inference_error.md](rubric/cap_time_inference_error.md) | 质量标签：时间推理错误 | 触发质量标签时 |
| [cap_calculation_logic_error.md](rubric/cap_calculation_logic_error.md) | 质量标签：计算逻辑错误 | 触发质量标签时 |
| [cap_intraday_precision_missing.md](rubric/cap_intraday_precision_missing.md) | 质量标签：日内精度缺失 | 触发质量标签时 |
| [cap_missing_required_data.md](rubric/cap_missing_required_data.md) | 质量标签：必要数据缺失 | 触发质量标签时 |
| [cap_unverifiable_result.md](rubric/cap_unverifiable_result.md) | 质量标签：结果不可验证 | 触发质量标签时 |

## 专家案例基准（golden_cases/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](golden_cases/_index.md) | 12 个专家案例 hard checks 与跨案例判分锚点 | 步骤 1 分析题目时读取 |

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
