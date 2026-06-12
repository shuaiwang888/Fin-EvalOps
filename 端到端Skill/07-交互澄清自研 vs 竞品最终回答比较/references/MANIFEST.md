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
| [ambiguity_clarification.md](rubric/ambiguity_clarification.md) | 模糊意图澄清维度 | 判断适用性与评分 |
| [context_continuity.md](rubric/context_continuity.md) | 多轮承接闭环维度 | 判断适用性与评分 |
| [entity_resolution.md](rubric/entity_resolution.md) | 标的与语义纠错维度 | 判断适用性与评分 |
| [financial_rule_and_premise.md](rubric/financial_rule_and_premise.md) | 金融规则与前提纠错维度 | 判断适用性与评分 |
| [assumption_definition.md](rubric/assumption_definition.md) | 假设口径与条件定义维度 | 判断适用性与评分 |
| [actionability_and_risk_plan.md](rubric/actionability_and_risk_plan.md) | 澄清后落地与风险边界维度 | 判断适用性与评分 |
| [evidence_grounding.md](rubric/evidence_grounding.md) | 事实证据与数据支撑维度 | 判断适用性与评分 |
| [guidance_and_retention.md](rubric/guidance_and_retention.md) | 后续引导闭环维度 | 判断适用性与评分 |
| [cap_wrong_financial_rule_or_unhandled_invalid_premise.md](rubric/cap_wrong_financial_rule_or_unhandled_invalid_premise.md) | 封顶标签：金融规则错误或错误前提未纠正 | 触发封顶标签时 |
| [cap_wrong_entity_resolution.md](rubric/cap_wrong_entity_resolution.md) | 封顶标签：标的识别错误 | 触发封顶标签时 |
| [cap_fabricated_or_unsupported_specific_advice.md](rubric/cap_fabricated_or_unsupported_specific_advice.md) | 封顶标签：缺证据的具体交易建议 | 触发封顶标签时 |
| [cap_context_break_after_clarification.md](rubric/cap_context_break_after_clarification.md) | 封顶标签：澄清后二轮承接断裂 | 触发封顶标签时 |
| [cap_missing_required_clarification.md](rubric/cap_missing_required_clarification.md) | 封顶标签：遗漏必要澄清 | 触发封顶标签时 |
| [cap_inconsistent_time_or_definition_scope.md](rubric/cap_inconsistent_time_or_definition_scope.md) | 封顶标签：时间或定义口径不一致 | 触发封顶标签时 |
| [cap_generic_template_without_clarification_value.md](rubric/cap_generic_template_without_clarification_value.md) | 封顶标签：模板化答复无咨询价值 | 触发封顶标签时 |

## 专家案例基准（golden_cases/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](golden_cases/_index.md) | 41 个专家案例 hard checks 与跨案例判分锚点 | 步骤 1 分析题目时读取 |
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
