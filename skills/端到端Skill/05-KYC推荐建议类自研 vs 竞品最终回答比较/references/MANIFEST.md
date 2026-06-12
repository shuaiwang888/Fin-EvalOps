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
| [intent_profile_understanding.md](rubric/intent_profile_understanding.md) | 意图与画像理解 | 判断适用性与评分 |
| [scenario_emotion_recognition.md](rubric/scenario_emotion_recognition.md) | 场景与情绪识别 | 判断适用性与评分 |
| [suitability_personalization.md](rubric/suitability_personalization.md) | 适当性与个性化 | 判断适用性与评分 |
| [evidence_integration.md](rubric/evidence_integration.md) | 多维证据整合 | 判断适用性与评分 |
| [decision_actionability.md](rubric/decision_actionability.md) | 决策可执行性 | 判断适用性与评分 |
| [risk_boundary_control.md](rubric/risk_boundary_control.md) | 风险控制与边界 | 判断适用性与评分 |
| [product_universe_fit.md](rubric/product_universe_fit.md) | 产品池与配置角色适配 | 判断适用性与评分 |
| [recommendation_stability.md](rubric/recommendation_stability.md) | 推荐稳定性与变化解释 | 判断适用性与评分 |
| [composition_credibility.md](rubric/composition_credibility.md) | 表达可信度 | 判断适用性与评分 |
| [cap_missing_kyc_profile.md](rubric/cap_missing_kyc_profile.md) | 质量标签：个人化建议缺少画像适配 | 触发质量标签时 |
| [cap_misread_emotional_loss_context.md](rubric/cap_misread_emotional_loss_context.md) | 质量标签：误读亏损/情绪场景 | 触发质量标签时 |
| [cap_fabricated_user_profile.md](rubric/cap_fabricated_user_profile.md) | 质量标签：虚构用户画像 | 触发质量标签时 |
| [cap_missing_action_for_decision_request.md](rubric/cap_missing_action_for_decision_request.md) | 质量标签：决策请求无操作建议 | 触发质量标签时 |
| [cap_missing_required_evidence.md](rubric/cap_missing_required_evidence.md) | 质量标签：遗漏必要证据 | 触发质量标签时 |
| [cap_overconfident_or_unsuitable_recommendation.md](rubric/cap_overconfident_or_unsuitable_recommendation.md) | 质量标签：过度确定/不合适推荐 | 触发质量标签时 |
| [cap_template_generic_advice.md](rubric/cap_template_generic_advice.md) | 质量标签：模板化通用建议 | 触发质量标签时 |

## 专家案例基准（golden_cases/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](golden_cases/_index.md) | 人工精标案例 hard checks 和典型失败模式 | 步骤 1 分析题目时读取 |
| [image_annotation_anchors.md](golden_cases/image_annotation_anchors.md) | 人工批注沉淀的私人投顾感、产品池、稳定性、情绪场景和可执行动作 hard checks | 步骤 1 分析题目时读取 |

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
