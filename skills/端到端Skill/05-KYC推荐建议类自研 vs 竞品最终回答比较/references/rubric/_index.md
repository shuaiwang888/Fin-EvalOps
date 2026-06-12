# 评分细则索引

## 维度列表

以下维度在评测时根据题目分析动态分配权重。表中“默认权重”是 result-only 基准权重；实际权重可按题目适用性调整，但双方必须使用同一套权重且总和为 100。

| 维度 | 默认权重 | 文件 | 适用性判断指南 |
|---|---:|---|---|
| `intent_profile_understanding` 意图与画像理解 | 17 | [intent_profile_understanding.md](intent_profile_understanding.md) | **始终 relevant**。所有 KYC 推荐建议题均需判断用户真实推荐/决策目标和问题中明示的个人化约束 |
| `scenario_emotion_recognition` 场景与情绪识别 | 9 | [scenario_emotion_recognition.md](scenario_emotion_recognition.md) | **relevant**: 亏损、套牢、迷茫、焦虑、急于回本、私人投顾感。**supplementary**: 普通推荐 |
| `suitability_personalization` 适当性与个性化 | 17 | [suitability_personalization.md](suitability_personalization.md) | **始终 relevant**。推荐必须解释为什么适合用户明示的风险、期限、目标、资金或处境 |
| `evidence_integration` 多维证据整合 | 13 | [evidence_integration.md](evidence_integration.md) | **relevant**: 需要市场、宏观、行业、估值、技术、资金、产品或历史阶段证据。**supplementary**: 纯原则性建议 |
| `decision_actionability` 决策可执行性 | 15 | [decision_actionability.md](decision_actionability.md) | **relevant**: 买卖、持有、加仓、减仓、配置、仓位、标的推荐。**supplementary**: 方向性讨论 |
| `risk_boundary_control` 风险控制与边界 | 12 | [risk_boundary_control.md](risk_boundary_control.md) | **始终 relevant**。所有推荐建议都必须有风险边界和不确定性表达 |
| `product_universe_fit` 产品池与配置角色适配 | 7 | [product_universe_fit.md](product_universe_fit.md) | **relevant**: ETF/基金/资产组合/股票池推荐、核心-卫星配置。**supplementary**: 普通买卖建议中的候选池适配 |
| `recommendation_stability` 推荐稳定性与变化解释 | 5 | [recommendation_stability.md](recommendation_stability.md) | **relevant**: 历史推荐变化、用户质疑“每次不一样”、同类推荐稳定性。**supplementary**: 普通“适合我”推荐中的可延续原则 |
| `composition_credibility` 表达可信度 | 5 | [composition_credibility.md](composition_credibility.md) | **始终 supplementary**。考察表达是否可信、审慎、非模板化 |

## 动态权重分配规则

1. 仅阅读用户问题，对每个维度判断适用性：`relevant` / `supplementary` / `not_applicable`。
2. `relevant` 维度获得较高权重，`supplementary` 维度保留低权重，`not_applicable` 维度权重为 0。
3. 所有活跃维度的 `dynamic_weight` 之和必须为 100。
4. 权重应跟随本题推荐责任变化：适合我/结合我的风险目标提高画像理解和适当性权重；亏损、迷茫、套牢提高场景情绪、风险边界和可执行性权重；历史阶段、估值分位、宏观情景提高证据整合权重；明确买卖仓位提高可执行性权重；ETF/基金/组合推荐提高产品池权重；推荐变化或用户质疑一致性时提高稳定性权重。
5. 权重理由必须写清“为什么本题这个维度重要”，不要只写“该题属于某类型”。

## 质量标签

以下标签只记录最终回答命中的严重质量问题。LLM 输出 `applied_caps` 与最终回答证据；`ceiling`、限分和总分计算由代码根据 `scripts/rule.py` 处理。

- [missing_kyc_profile](cap_missing_kyc_profile.md)：个人化建议缺少画像适配
- [misread_emotional_loss_context](cap_misread_emotional_loss_context.md)：误读亏损/情绪场景
- [fabricated_user_profile](cap_fabricated_user_profile.md)：虚构用户画像
- [missing_action_for_decision_request](cap_missing_action_for_decision_request.md)：决策请求无操作建议
- [missing_required_evidence](cap_missing_required_evidence.md)：遗漏必要证据
- [overconfident_or_unsuitable_recommendation](cap_overconfident_or_unsuitable_recommendation.md)：过度确定/不合适推荐
- [template_generic_advice](cap_template_generic_advice.md)：模板化通用建议

## 质量标签注意事项

- 质量标签不替代维度评分。
- 标签必须由最终回答文本直接支持，不能根据过程信息推断。
- 对“适合我”“结合我的风险目标”“我的持仓/成本/亏损/期限”等场景，必须严格检查答案是否处理用户问题中的明示约束；若信息不足，答案应说明不足、分层假设或追问。
- 对亏损、套牢、迷茫、急于回本等场景，必须严格检查降风险、复盘纪律和行动边界。
- 对 ETF/基金/股票池推荐，必须严格检查产品池、配置角色、仓位和风险边界。

## 证据边界

证据只能来自：
- 用户问题；
- 自研最终回答；
- 竞品最终回答。

不得引用或评价任何过程字段、上下文字段或过程记录。
