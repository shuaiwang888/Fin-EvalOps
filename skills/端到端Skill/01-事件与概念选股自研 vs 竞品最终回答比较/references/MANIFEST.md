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
| [_index.md](rubric/_index.md) | 维度列表、动态权重分配、封顶标签规则、证据边界 | 步骤 1 分析题目前通读 |
| [raw-score-scale.md](rubric/raw-score-scale.md) | 0/20/40/60/80/100 分制与加权公式 | 评分前必读 |
| [intent_fulfillment.md](rubric/intent_fulfillment.md) | 意图满足度维度 | 判断适用性与评分 |
| [event_abstraction.md](rubric/event_abstraction.md) | 事件抽象度维度 | 判断适用性与评分 |
| [industry_mapping.md](rubric/industry_mapping.md) | 产业链映射维度 | 判断适用性与评分 |
| [ranking_judgment.md](rubric/ranking_judgment.md) | 排序判断维度 | 判断适用性与评分 |
| [logic_closure.md](rubric/logic_closure.md) | 逻辑闭环维度 | 判断适用性与评分 |
| [timeliness_fact_boundary.md](rubric/timeliness_fact_boundary.md) | 时效性与事实边界维度 | 判断适用性与评分 |
| [credibility_expression.md](rubric/credibility_expression.md) | 可信度与表达维度 | 判断适用性与评分 |
| [cap_hard_time_or_fact_error.md](rubric/cap_hard_time_or_fact_error.md) | 封顶标签：硬性时间或事实错误 | 触发封顶标签时 |
| [cap_missing_required_ranking.md](rubric/cap_missing_required_ranking.md) | 封顶标签：遗漏必要排序 | 触发封顶标签时 |
| [cap_data_dump_without_core_rationale.md](rubric/cap_data_dump_without_core_rationale.md) | 封顶标签：数据堆砌无核心论证 | 触发封顶标签时 |
| [cap_wrong_evidence_type.md](rubric/cap_wrong_evidence_type.md) | 封顶标签：证据类型错误 | 触发封顶标签时 |
| [cap_unverifiable_subjective_expression.md](rubric/cap_unverifiable_subjective_expression.md) | 封顶标签：不可验证的主观表达 | 触发封顶标签时 |
| [cap_forced_mapping_or_entity_boundary_error.md](rubric/cap_forced_mapping_or_entity_boundary_error.md) | 封顶标签：强行映射或实体边界错误 | 触发封顶标签时 |

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
| 步骤 2：分别做绝对评分 | 最终回答逐维评分 + 封顶标签检查 | 活跃维度文件 + `rubric/raw-score-scale.md` + 对应 `rubric/cap_*.md` 文件 |
| 步骤 3：逐维比较 | 输出自研优势/弱点、竞品优点、共同失败点 | `comparison_protocol.md` |
| 步骤 4：序列化输出 | 双边绝对评分 + 逐维比较 + 总结结论 | `output-schema_zh.md` |
