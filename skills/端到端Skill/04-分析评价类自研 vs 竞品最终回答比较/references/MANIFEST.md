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
| [expert_answer_patterns.md](rubric/expert_answer_patterns.md) | 人工精标提炼的好/差答案模式和场景化判分锚点 | 步骤 1 分析题目前通读 |
| [raw-score-scale.md](rubric/raw-score-scale.md) | 0/20/40/60/80/100 原始分锚点 | 评分前必读 |
| [intent_scenario_recognition.md](rubric/intent_scenario_recognition.md) | 意图和投资场景识别 | 判断适用性与评分 |
| [evidence_source_quality.md](rubric/evidence_source_quality.md) | 证据来源质量和充分性 | 判断适用性与评分 |
| [recency_time_boundary.md](rubric/recency_time_boundary.md) | 时效性和时间边界 | 判断适用性与评分 |
| [investment_logic_depth.md](rubric/investment_logic_depth.md) | 投资逻辑深度 | 判断适用性与评分 |
| [method_fit.md](rubric/method_fit.md) | 分析方法匹配 | 判断适用性与评分 |
| [comparison_quantification.md](rubric/comparison_quantification.md) | 对比、排名、量化和历史分位 | 判断适用性与评分 |
| [actionability_risk.md](rubric/actionability_risk.md) | 可执行性、条件和风险 | 判断适用性与评分 |
| [user_profile_suitability.md](rubric/user_profile_suitability.md) | 用户画像、风险目标、持仓背景与建议适配 | 判断适用性与评分 |
| [scenario_emotion_recognition.md](rubric/scenario_emotion_recognition.md) | 亏损、套牢、迷茫等真实投资处境识别 | 判断适用性与评分 |
| [composition_credibility.md](rubric/composition_credibility.md) | 表达可信度和非模板化 | 判断适用性与评分 |
| [cap_missed_core_investment_logic.md](rubric/cap_missed_core_investment_logic.md) | 质量标签：遗漏核心投资逻辑 | 触发质量标签时 |
| [cap_stale_or_wrong_time_evidence.md](rubric/cap_stale_or_wrong_time_evidence.md) | 质量标签：时效错误或过时证据 | 触发质量标签时 |
| [cap_method_mismatch.md](rubric/cap_method_mismatch.md) | 质量标签：分析方法不匹配 | 触发质量标签时 |
| [cap_template_data_dump.md](rubric/cap_template_data_dump.md) | 质量标签：模板化数据堆砌 | 触发质量标签时 |
| [cap_missing_required_analysis_elements.md](rubric/cap_missing_required_analysis_elements.md) | 质量标签：遗漏必要分析要素 | 触发质量标签时 |
| [cap_wrong_or_shallow_source.md](rubric/cap_wrong_or_shallow_source.md) | 质量标签：证据来源错误或浅层 | 触发质量标签时 |
| [cap_missing_user_profile_fit.md](rubric/cap_missing_user_profile_fit.md) | 质量标签：个人化建议缺少画像适配 | 触发质量标签时 |
| [cap_misread_loss_or_emotion_context.md](rubric/cap_misread_loss_or_emotion_context.md) | 质量标签：误读亏损/情绪场景 | 触发质量标签时 |
| [cap_overconfident_or_unsuitable_action.md](rubric/cap_overconfident_or_unsuitable_action.md) | 质量标签：过度确定或不适当行动建议 | 触发质量标签时 |
| [cap_missing_decision_action_for_recommendation.md](rubric/cap_missing_decision_action_for_recommendation.md) | 质量标签：推荐/交易请求缺少行动输出 | 触发质量标签时 |

## 专家案例基准（golden_cases/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](golden_cases/_index.md) | 人工精标案例 hard checks 和典型失败模式 | 步骤 1 分析题目时读取 |

## 输出契约

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [output-schema_round1_zh.md](output-schema_round1_zh.md) | Round 1：同题校验、共享权重、双方最终回答证据摘要 | 步骤 1 后 |
| [output-schema_zh.md](output-schema_zh.md) | Pairwise JSON 输出契约、证据对象和比较结论格式 | 序列化时 |

## 协议步骤到文件的映射

| 协议步骤 | 操作 | 读取文件 |
|---|---|---|
| 步骤 0：校验同题 | case_id 与问题一致性校验 | `SKILL_zh.md` |
| 步骤 1：建立共享评估框架 | 维度适用性 + 动态权重 + 案例命中 | `rubric/_index.md` + `rubric/expert_answer_patterns.md` + 活跃维度文件 + `golden_cases/_index.md` |
| 步骤 2：分别做绝对评分 | 最终回答逐维评分 + 质量标签检查 | 活跃维度文件 + `rubric/raw-score-scale.md` + 对应 `rubric/cap_*.md` 文件 |
| 步骤 3：逐维比较 | 输出自研优势/弱点、竞品优点、共同失败点 | `comparison_protocol.md` |
| 步骤 4：序列化输出 | 双边绝对评分 + 逐维比较 + 总结结论 | `output-schema_zh.md` |
