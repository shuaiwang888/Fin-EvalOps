# 评分细则索引

## 先识别评价需求，不先套题型

分析评价类问题不需要先归入固定题型。固定题型容易让评测套模板，真正要先判断的是：本题要解决什么投资决策、需要什么证据、哪些评价维度决定答案质量。

步骤：
1. 从 `question` 和必要 `context` 抽取评价需求：标的/资产、用户任务、决策强度、时间窗口、证据类型、比较/量化要求、风险责任。
2. 若输入包含线上评测样本、失败统计、用户反馈或人工标注摘要，优先读取其中暴露的高频缺口，用于发现新维度或调整权重。
3. 从下方“种子维度池”选择适用维度；当线上数据暴露的关键缺口不能被现有维度清楚覆盖时，可新增 `runtime_dimensions`。
4. 主题标签只用于检索专家案例、hard checks 和封顶规则，不作为权重模板。
5. 读取 [expert_answer_patterns.md](expert_answer_patterns.md)，用人工精标中的好/差答案模式校准评分，尤其检查低密度长答案、方法错位和表面资讯拼接。

## 种子维度池

| 维度 | 建议权重 | 文件 | 适用性判断指南 |
|---|---:|---|---|
| `intent_scenario_recognition` 意图和场景识别 | 13 | [intent_scenario_recognition.md](intent_scenario_recognition.md) | **始终 relevant** |
| `evidence_source_quality` 证据来源质量 | 13 | [evidence_source_quality.md](evidence_source_quality.md) | **relevant**: 需要搜索、研报、公告、调研、财务、行情等证据支撑。**supplementary**: 纯概念解释 |
| `recency_time_boundary` 时效性和时间边界 | 8 | [recency_time_boundary.md](recency_time_boundary.md) | **relevant**: 最新、最近、今天、消息面、为什么涨跌、题材发酵。**supplementary**: 长期基本面 |
| `investment_logic_depth` 投资逻辑深度 | 17 | [investment_logic_depth.md](investment_logic_depth.md) | **始终 relevant** |
| `method_fit` 分析方法匹配 | 10 | [method_fit.md](method_fit.md) | **始终 relevant** |
| `comparison_quantification` 对比和量化 | 8 | [comparison_quantification.md](comparison_quantification.md) | **relevant**: 基金、估值、指数、对比、排序、历史位置。**supplementary**: 一般诊断 |
| `actionability_risk` 可执行性和风险 | 8 | [actionability_risk.md](actionability_risk.md) | **relevant**: 能不能买、持有、切换、配置。**supplementary**: 归因或消息查询 |
| `user_profile_suitability` 用户画像适配 | 8 | [user_profile_suitability.md](user_profile_suitability.md) | **relevant**: 适合我、结合目标/风险/持仓/成本、推荐标的或配置。**supplementary**: 普通买卖分析。**not_applicable**: 完全客观事实查询 |
| `scenario_emotion_recognition` 场景与情绪识别 | 4 | [scenario_emotion_recognition.md](scenario_emotion_recognition.md) | **relevant**: 浮亏、套牢、腰斩、迷茫、买什么都亏、急于回本。**supplementary**: 普通推荐。**not_applicable**: 无个人处境信号 |
| `composition_credibility` 表达可信度 | 5 | [composition_credibility.md](composition_credibility.md) | **始终 supplementary** |
| `tool_usage` 工具使用合理性 | 6 | [tool_usage.md](tool_usage.md) | **始终 relevant**，在链路诊断阶段评分 |

必读辅助文件：
- [expert_answer_patterns.md](expert_answer_patterns.md)：人工精标截图提炼的场景化答案模式和强判分锚点。

## 运行时新增维度

仅当线上数据或本题证据表明现有维度无法准确承载某个关键质量缺口时，才新增运行时维度。新增维度必须满足：
- 名称使用 `snake_case`，不能与现有维度语义重复。
- 写清定义、为什么本题需要、评分锚点和证据需求。
- 权重并入 `weight_assignment`，所有活跃维度权重总和仍为 100。
- 原始分仍使用 [raw-score-scale.md](raw-score-scale.md) 的六档锚定值（0/20/40/60/80/100）。

可新增的维度示例：
- `business_purity`：题材或产业链问题中，标的业务与主题的真实相关度是否被准确判断。
- `holding_style_fit`：基金或组合建议中，持仓风格是否匹配用户风险偏好和投资周期。
- `event_materiality`：消息面问题中，事件对价格或基本面的实质影响是否被区分。
- `product_universe_fit`：ETF/基金/组合推荐中，产品池是否覆盖合理，是否避免过窄、高波动或不适合普通用户的集中暴露。
- `recommendation_consistency`：同一用户画像和同类问题下，多次推荐是否稳定；变化是否有新信息、市场变化或假设变化支撑。
- `stock_style_logic_fit`：个股分析是否识别游资/题材/机构/价值/周期/避险等不同交易逻辑，并改变分析主轴。
- `source_depth_fit`：问题所需资料深度是否被识别，尤其是调研纪要、研报全文、客户占比、供应链份额和隐含资产。

## 动态权重分配规则

1. 仅基于 `question`、必要 `context` 和已提供的线上维度信号分配权重，不根据固定题型表套权重。
2. `relevant` 维度获得较高权重，`supplementary` 维度保留低权重，`not_applicable` 维度可跳过。
3. 所有活跃维度的 `dynamic_weight` 之和必须为 100。
4. 权重应跟随本题评价需求变化：最新消息提高时效和证据权重；可买可卖提高可执行性和风险权重；历史位置、对比、切换提高量化和比较权重；深层资料提高证据来源和工具使用权重；“适合我/结合我的风险目标/我的持仓成本”提高用户画像适配权重；亏损、迷茫、套牢提高场景情绪、风险边界和可执行性权重。
5. 线上数据若显示某类失败高频且影响用户决策，应调高对应维度；若现有维度承载不清，应新增运行时维度。
6. 权重理由必须写清“为什么本题这个维度重要”，不要只写“该题属于某类型”。

## 封顶规则

- [missed_core_investment_logic（上限 60）](cap_missed_core_investment_logic.md)
- [stale_or_wrong_time_evidence（上限 50）](cap_stale_or_wrong_time_evidence.md)
- [method_mismatch（上限 55）](cap_method_mismatch.md)
- [template_data_dump（上限 60）](cap_template_data_dump.md)
- [missing_required_analysis_elements（上限 65）](cap_missing_required_analysis_elements.md)
- [wrong_or_shallow_source（上限 55）](cap_wrong_or_shallow_source.md)
- [missing_user_profile_fit（上限 60）](cap_missing_user_profile_fit.md)
- [misread_loss_or_emotion_context（上限 50）](cap_misread_loss_or_emotion_context.md)
- [overconfident_or_unsuitable_action（上限 55）](cap_overconfident_or_unsuitable_action.md)
- [missing_decision_action_for_recommendation（上限 65）](cap_missing_decision_action_for_recommendation.md)

封顶限制最终分数，不替代维度评分。更好的隐藏规划不能覆盖最终答案触发的封顶。
