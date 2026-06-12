# 评分细则索引

## 先识别推荐任务，不先套题型

KYC 推荐建议类问题要先判断：用户要解决什么投资决策、模型是否主动使用用户 KYC 数据、已知画像是什么、缺失画像如何处理、需要什么证据、推荐会带来什么风险责任。

步骤：
1. 从 `question` 和必要 `context` 抽取推荐目标：标的/资产、资金或持仓、风险偏好、投资期限、收益目标、亏损/套牢/迷茫状态、是否要求买卖动作。
2. 检查链路是否主动读取、调用、检索或引用用户 KYC 数据。KYC 数据可以来自画像工具、画像存储、历史 `context`、当前问题自述或链路中可见的画像检索结果；`context` 是否含画像不是触发评测的前提。
3. 若输入包含线上评测样本、失败统计、用户反馈或人工标注摘要，优先读取其中暴露的高频缺口，用于发现新维度或调整权重。
4. 从下方维度池选择适用维度；当线上数据暴露的关键缺口不能被现有维度清楚覆盖时，可新增临时评分维度，并直接并入 `weight_assignment` 与 `dimension_scores`。
5. 股票、ETF、基金、黄金、原油、行业方向等主题只用于检索专家案例、hard checks 和封顶规则，不作为权重模板。

## 维度池

| 维度 | 建议权重 | 文件 | 适用性判断指南 |
|---|---:|---|---|
| `intent_profile_understanding` 意图与画像理解 | 18 | [intent_profile_understanding.md](intent_profile_understanding.md) | **始终 relevant** |
| `scenario_emotion_recognition` 场景与情绪识别 | 10 | [scenario_emotion_recognition.md](scenario_emotion_recognition.md) | **relevant**: 亏损、套牢、迷茫、焦虑、急于回本、私人投顾感。**supplementary**: 普通推荐 |
| `suitability_personalization` 适当性与个性化 | 18 | [suitability_personalization.md](suitability_personalization.md) | **始终 relevant** |
| `evidence_integration` 多维证据整合 | 14 | [evidence_integration.md](evidence_integration.md) | **relevant**: 需要市场、宏观、行业、估值、技术、资金、历史阶段证据。**supplementary**: 纯原则性建议 |
| `decision_actionability` 决策可执行性 | 16 | [decision_actionability.md](decision_actionability.md) | **relevant**: 买卖、持有、加仓、减仓、配置、仓位。**supplementary**: 方向性讨论 |
| `risk_boundary_control` 风险控制与边界 | 12 | [risk_boundary_control.md](risk_boundary_control.md) | **始终 relevant** |
| `product_universe_fit` 产品池与配置角色适配 | 按需 5-10 | [product_universe_fit.md](product_universe_fit.md) | **relevant**: ETF/基金/资产组合/股票池推荐、核心-卫星配置。**supplementary**: 普通买卖建议中的候选池适配 |
| `recommendation_stability` 推荐稳定性与变化解释 | 按需 4-8 | [recommendation_stability.md](recommendation_stability.md) | **relevant**: 历史对话、多次同类推荐、用户反馈“每次不一样”、线上稳定性信号。**supplementary**: 普通“适合我”推荐 |
| `composition_credibility` 表达可信度 | 5 | [composition_credibility.md](composition_credibility.md) | **始终 supplementary** |
| `tool_usage` 工具使用合理性 | 7 | [tool_usage.md](tool_usage.md) | **始终 relevant**，在链路诊断阶段评分 |

`product_universe_fit` 和 `recommendation_stability` 是图片人工批注后固化的按需维度。启用时从 `evidence_integration`、`suitability_personalization`、`decision_actionability` 或 `composition_credibility` 中让出权重，动态权重总和仍为 100。

## 运行时新增维度

仅当线上数据或本题证据表明现有维度无法准确承载某个关键质量缺口时，才新增运行时维度。新增维度必须满足：
- 名称使用 `snake_case`，不能与现有维度语义重复。
- 写清定义、为什么本题需要、评分锚点和证据需求。
- 权重并入 `weight_assignment`，所有活跃维度权重总和仍为 100。
- 原始分仍使用 [raw-score-scale.md](raw-score-scale.md) 的 0/20/40/60/80/100 六档量表。

可新增的维度示例：
- `comparison_quantification`：多资产/多行业/多基金对比中，是否给出量化比较、排序和取舍依据。
- `private_advisor_continuity`：是否承接用户历史偏好、过往亏损/持仓和长期目标，形成连续的私人投顾体验。

## 动态权重分配规则

1. 仅基于 `question`、必要 `context` 和已提供的线上维度信号分配权重。
2. `relevant` 维度获得较高权重，`supplementary` 维度保留低权重，`not_applicable` 维度权重为 0。
3. 所有活跃维度的 `dynamic_weight` 之和必须为 100。
4. 权重应跟随本题推荐责任变化：适合我/结合我的风险目标提高画像和适当性权重；亏损/迷茫/套牢提高场景情绪、风险边界和可执行性权重；历史阶段/估值分位/宏观情景提高证据整合权重；明确买卖仓位提高可执行性权重。
5. 05 类适用问题默认要求模型使用用户 KYC 数据。若链路和最终答案都看不出主动使用 KYC，应在 `intent_profile_understanding`、`suitability_personalization`、`risk_boundary_control` 和 `tool_usage` 中体现扣分，并优先考虑 `missing_kyc_profile` 封顶。
6. 如果链路确实没有拿到可用 KYC，高质量答案应说明画像依据不足，并给出分层、条件化、低风险边界清晰的建议或必要追问；这只能缓解用户侧质量问题，不能抹除链路层“未取 KYC”的归因。
7. ETF/基金或组合推荐若产品池选择本身是主矛盾，启用 `product_universe_fit`；同类问题反复推荐且结果不一致，或线上信号暴露推荐漂移，启用 `recommendation_stability`。

## 封顶规则

- [missing_kyc_profile（上限 60）](cap_missing_kyc_profile.md)
- [misread_emotional_loss_context（上限 50）](cap_misread_emotional_loss_context.md)
- [fabricated_user_profile（上限 55）](cap_fabricated_user_profile.md)
- [missing_action_for_decision_request（上限 65）](cap_missing_action_for_decision_request.md)
- [missing_required_evidence（上限 60）](cap_missing_required_evidence.md)
- [overconfident_or_unsuitable_recommendation（上限 55）](cap_overconfident_or_unsuitable_recommendation.md)
- [template_generic_advice（上限 65）](cap_template_generic_advice.md)

封顶限制最终分数，不替代维度评分。更好的隐藏规划不能覆盖最终答案触发的封顶。
