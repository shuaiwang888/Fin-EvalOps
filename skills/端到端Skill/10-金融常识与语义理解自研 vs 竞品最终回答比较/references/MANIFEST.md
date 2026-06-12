# 参考文件索引

本目录只导航 result-only 最终回答比较评估需要的文件。评分、证据、优缺点和最终结论只能来自用户问题与双方最终回答。

## 主协议

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [../SKILL_zh.md](../SKILL_zh.md) | 定义金融常识与语义理解 result-only 自研 vs 竞品最终回答比较协议 | 开始评测前必读 |
| [comparison_protocol.md](comparison_protocol.md) | 定义先绝对后相对、逐维比较、优势/缺点/共同失败点判定规则 | 逐维比较前必读 |

## 评分细则（rubric/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [rubric/_index.md](rubric/_index.md) | 维度列表、动态权重分配、封顶标签规则、证据边界 | 步骤 1 分析题目前通读 |
| [rubric/raw-score-scale.md](rubric/raw-score-scale.md) | 0/20/40/60/80/100 分制与加权公式 | 评分前必读 |
| [rubric/semantic_intent_alignment.md](rubric/semantic_intent_alignment.md) | 语义意图匹配维度 | 判断适用性与评分 |
| [rubric/financial_term_understanding.md](rubric/financial_term_understanding.md) | 金融术语/规则理解维度 | 判断适用性与评分 |
| [rubric/entity_product_boundary.md](rubric/entity_product_boundary.md) | 实体与产品边界维度 | 判断适用性与评分 |
| [rubric/metric_caliber_accuracy.md](rubric/metric_caliber_accuracy.md) | 指标公式与数据口径维度 | 判断适用性与评分 |
| [rubric/timeliness_context.md](rubric/timeliness_context.md) | 时效上下文维度 | 判断适用性与评分 |
| [rubric/credibility_expression.md](rubric/credibility_expression.md) | 可信解释与表达维度 | 判断适用性与评分 |
| [rubric/cap_rules.md](rubric/cap_rules.md) | 金融概念、实体产品、定义、指标口径、时效和泛泛建议封顶标签 | 触发封顶标签时 |

## 专家案例基准（golden_cases/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [golden_cases/_index.md](golden_cases/_index.md) | 金融常识与语义理解专家案例 hard checks | 步骤 1 分析题目时读取 |
| [golden_cases/image_annotation_anchors.md](golden_cases/image_annotation_anchors.md) | docx 图片人工批注补充锚点 | 命中特定批注场景时读取 |

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
| 步骤 2：分别做绝对评分 | 最终回答逐维评分 + 封顶标签检查 | 活跃维度文件 + `rubric/raw-score-scale.md` + `rubric/cap_rules.md` |
| 步骤 3：逐维比较 | 输出自研优势/弱点、竞品优点、共同失败点 | `comparison_protocol.md` |
| 步骤 4：序列化输出 | 双边绝对评分 + 逐维比较 + 总结结论 | `output-schema_zh.md` |
