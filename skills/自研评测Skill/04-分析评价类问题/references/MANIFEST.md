# 参考文件索引

本文件是分析评价类评测 skill 的导航地图。根据评测协议步骤按需读取子文件。

## 评分细则（rubric/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](rubric/_index.md) | 种子维度池、运行时新增维度规则、动态权重分配、封顶规则总览 | 步骤 0 分析题目前通读 |
| [expert_answer_patterns.md](rubric/expert_answer_patterns.md) | 从人工精标截图提炼的好/差答案模式、用户交易心理和场景化评判锚点 | 步骤 0 分析题目前通读 |
| [raw-score-scale.md](rubric/raw-score-scale.md) | 0-5 原始分定义和加权公式 | 评分前必读 |
| [intent_scenario_recognition.md](rubric/intent_scenario_recognition.md) | 意图和投资场景识别 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [evidence_source_quality.md](rubric/evidence_source_quality.md) | 证据来源质量和充分性 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [recency_time_boundary.md](rubric/recency_time_boundary.md) | 时效性和时间边界 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [investment_logic_depth.md](rubric/investment_logic_depth.md) | 投资逻辑深度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [method_fit.md](rubric/method_fit.md) | 分析方法和题型/标的/周期匹配 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [comparison_quantification.md](rubric/comparison_quantification.md) | 对比、排名、量化和历史分位 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [actionability_risk.md](rubric/actionability_risk.md) | 可执行性、条件和风险 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [user_profile_suitability.md](rubric/user_profile_suitability.md) | 用户画像、风险目标、持仓背景与建议适配 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [scenario_emotion_recognition.md](rubric/scenario_emotion_recognition.md) | 亏损、套牢、迷茫等真实投资处境识别 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [composition_credibility.md](rubric/composition_credibility.md) | 表达可信度和非模板化 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [tool_usage.md](rubric/tool_usage.md) | 工具使用合理性 | 步骤 2 评分 |
| [cap_missed_core_investment_logic.md](rubric/cap_missed_core_investment_logic.md) | 封顶：缺失核心投资逻辑 | 步骤 3 |
| [cap_stale_or_wrong_time_evidence.md](rubric/cap_stale_or_wrong_time_evidence.md) | 封顶：旧消息或时间边界错误 | 步骤 3 |
| [cap_method_mismatch.md](rubric/cap_method_mismatch.md) | 封顶：分析方法明显错位 | 步骤 3 |
| [cap_template_data_dump.md](rubric/cap_template_data_dump.md) | 封顶：模板化数据堆砌 | 步骤 3 |
| [cap_missing_required_analysis_elements.md](rubric/cap_missing_required_analysis_elements.md) | 封顶：题型必需分析要素缺失 | 步骤 3 |
| [cap_wrong_or_shallow_source.md](rubric/cap_wrong_or_shallow_source.md) | 封顶：证据来源类型错误或来源过浅 | 步骤 3 |
| [cap_missing_user_profile_fit.md](rubric/cap_missing_user_profile_fit.md) | 封顶：个人化建议缺少画像适配 | 步骤 3 |
| [cap_misread_loss_or_emotion_context.md](rubric/cap_misread_loss_or_emotion_context.md) | 封顶：误读亏损/迷茫/套牢场景 | 步骤 3 |
| [cap_overconfident_or_unsuitable_action.md](rubric/cap_overconfident_or_unsuitable_action.md) | 封顶：过度确定或不适当行动建议 | 步骤 3 |
| [cap_missing_decision_action_for_recommendation.md](rubric/cap_missing_decision_action_for_recommendation.md) | 封顶：推荐/交易请求缺少行动输出 | 步骤 3 |

## 专家案例基准（golden_cases/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](golden_cases/_index.md) | 人工精标案例 hard checks 和典型失败模式 | 步骤 0 分析题目时读取 |

## 根因归因体系（root-cause/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](root-cause/_index.md) | L1 阶段、证据规则、根因选择规则 | 步骤 2 诊断前通读 |
| [intent.md](root-cause/intent.md) | L1: intent | 步骤 2 |
| [evidence.md](root-cause/evidence.md) | L1: evidence | 步骤 2 |
| [tool.md](root-cause/tool.md) | L1: tool | 步骤 2 |
| [reasoning.md](root-cause/reasoning.md) | L1: reasoning | 步骤 2 |
| [composition.md](root-cause/composition.md) | L1: composition | 步骤 2 |
| [capability_gap.md](root-cause/capability_gap.md) | L1: capability_gap | 步骤 2 |

## 工具列表（tool_list/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](tool_list/_index.md) | 工具总览 | 步骤 2 评分 tool_usage 前必读 |
| [search.md](tool_list/search.md) | Search 规则 | 按需 |
| [finquery.md](tool_list/finquery.md) | FinQuery 规则 | 按需 |
| [accessingfulltext.md](tool_list/accessingfulltext.md) | 全文阅读规则 | 按需 |
| [codeinterpreter.md](tool_list/codeinterpreter.md) | CodeInterpreter 规则 | 按需 |

## 输出契约

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [output-schema_zh.md](output-schema_zh.md) | JSON 优先的输出 schema、证据对象格式和字段规则 | 步骤 4 |
