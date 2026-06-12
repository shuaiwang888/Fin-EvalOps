# 评分细则索引

## 维度列表

以下维度在评测时根据题目分析动态分配权重。表中“默认权重”是 result-only 基准权重；实际权重可按题目适用性调整，但双方必须使用同一套权重且总和为 100。

| 维度 | 默认权重 | 文件 | 适用性判断指南 |
|---|---:|---|---|
| `intent_scenario_recognition` 意图和场景识别 | 14 | [intent_scenario_recognition.md](intent_scenario_recognition.md) | **始终 relevant**。所有分析评价题均需判断用户真实投资场景和决策需求 |
| `evidence_source_quality` 证据来源质量 | 14 | [evidence_source_quality.md](evidence_source_quality.md) | **relevant**: 需要最新消息、研报、公告、调研、财务、行情、估值、资金等证据支撑。**supplementary**: 纯概念解释 |
| `recency_time_boundary` 时效性和时间边界 | 9 | [recency_time_boundary.md](recency_time_boundary.md) | **relevant**: 最新、最近、今天、消息面、为什么涨跌、题材发酵。**supplementary**: 长期基本面 |
| `investment_logic_depth` 投资逻辑深度 | 18 | [investment_logic_depth.md](investment_logic_depth.md) | **始终 relevant**。所有分析评价题都必须把信息转化为投资判断和因果链 |
| `method_fit` 分析方法匹配 | 11 | [method_fit.md](method_fit.md) | **始终 relevant**。不同标的、资产、周期和问题类型必须使用不同分析方法 |
| `comparison_quantification` 对比和量化 | 8 | [comparison_quantification.md](comparison_quantification.md) | **relevant**: 基金、估值、指数、对比、排序、历史位置、切换。**supplementary**: 一般诊断 |
| `actionability_risk` 可执行性和风险 | 9 | [actionability_risk.md](actionability_risk.md) | **relevant**: 能不能买、持有、切换、配置、仓位。**supplementary**: 归因或消息查询 |
| `user_profile_suitability` 用户画像适配 | 8 | [user_profile_suitability.md](user_profile_suitability.md) | **relevant**: 适合我、结合目标/风险/持仓/成本、推荐标的或配置。**supplementary**: 普通买卖分析。**not_applicable**: 完全客观事实查询 |
| `scenario_emotion_recognition` 场景与情绪识别 | 4 | [scenario_emotion_recognition.md](scenario_emotion_recognition.md) | **relevant**: 浮亏、套牢、腰斩、迷茫、买什么都亏、急于回本。**supplementary**: 普通推荐。**not_applicable**: 无个人处境信号 |
| `composition_credibility` 表达可信度 | 5 | [composition_credibility.md](composition_credibility.md) | **始终 supplementary**。考察表达是否可信、审慎、非模板化 |

必读辅助文件：
- [expert_answer_patterns.md](expert_answer_patterns.md)：人工精标截图提炼的场景化答案模式和强判分锚点。

## 动态权重分配规则

1. 仅阅读用户问题，对每个维度判断适用性：`relevant` / `supplementary` / `not_applicable`。
2. `relevant` 维度获得较高权重，`supplementary` 维度保留低权重，`not_applicable` 维度权重为 0。
3. 所有活跃维度的 `dynamic_weight` 之和必须为 100。
4. 权重应跟随本题评价需求变化：最新消息提高时效和证据权重；可买可卖提高可执行性和风险权重；历史位置、对比、切换提高量化和比较权重；“适合我/结合我的风险目标/我的持仓成本”提高用户画像适配权重；亏损、迷茫、套牢提高场景情绪、风险边界和可执行性权重。
5. 权重理由必须写清“为什么本题这个维度重要”，不要只写“该题属于某类型”。

## 质量标签

以下标签只记录最终回答命中的严重质量问题。LLM 输出 `applied_caps` 与最终回答证据；`ceiling`、限分和总分计算由代码根据 `scripts/rule.py` 处理。

- [missed_core_investment_logic](cap_missed_core_investment_logic.md)：遗漏核心投资逻辑
- [stale_or_wrong_time_evidence](cap_stale_or_wrong_time_evidence.md)：时效错误或过时证据
- [method_mismatch](cap_method_mismatch.md)：分析方法不匹配
- [template_data_dump](cap_template_data_dump.md)：模板化数据堆砌
- [missing_required_analysis_elements](cap_missing_required_analysis_elements.md)：遗漏必要分析要素
- [wrong_or_shallow_source](cap_wrong_or_shallow_source.md)：证据来源错误或浅层
- [missing_user_profile_fit](cap_missing_user_profile_fit.md)：个人化建议缺少画像适配
- [misread_loss_or_emotion_context](cap_misread_loss_or_emotion_context.md)：误读亏损/情绪场景
- [overconfident_or_unsuitable_action](cap_overconfident_or_unsuitable_action.md)：过度确定或不适当行动建议
- [missing_decision_action_for_recommendation](cap_missing_decision_action_for_recommendation.md)：推荐/交易请求缺少行动输出

## 质量标签注意事项

- 质量标签不替代维度评分。
- 标签必须由最终回答文本直接支持，不能根据过程信息推断。
- 核心投资逻辑缺失、方法错位、过时消息和模板化堆砌是分析评价类答案的高优先级硬伤。
- 对个人化推荐、亏损、套牢、迷茫、急于回本等场景，必须严格检查用户适配、降风险和行动边界。

## 证据边界

证据只能来自：
- 用户问题；
- 自研最终回答；
- 竞品最终回答。

不得引用或评价任何过程字段、上下文字段或过程记录。
