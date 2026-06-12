# 评分细则索引

## 维度列表

| 维度 | 建议权重 | 文件 | 适用性判断指南 |
|---|---:|---|---|
| `intent_fulfillment` 意图满足度 | 15 | [intent_fulfillment.md](intent_fulfillment.md) | **始终 relevant**。评估是否回答显性问题和隐含投资诉求 |
| `timeliness_fact_boundary` 时效性与事实边界 | 15 | [timeliness_fact_boundary.md](timeliness_fact_boundary.md) | **relevant**: 最新、近期、近两周、当天、截至某日、项目进展、政策年份。**supplementary**: 一般知识问答 |
| `fact_evidence_quality` 事实证据质量 | 15 | [fact_evidence_quality.md](fact_evidence_quality.md) | **始终 relevant**。评估事实、数据口径、来源类型和可核验性 |
| `information_integration` 资讯整合与比较 | 12 | [information_integration.md](information_integration.md) | **relevant**: 多政策/监管/产业/公司事件整合，或横向比较。**supplementary**: 单点事实查询 |
| `investment_mapping` 投资映射与落地 | 12 | [investment_mapping.md](investment_mapping.md) | **relevant**: 影响、受益标的、行业方向、A股映射。**not_applicable**: 纯百科事实且无金融落地需求 |
| `core_signal_extraction` 核心信号提炼 | 10 | [core_signal_extraction.md](core_signal_extraction.md) | **relevant**: 市场异动、热点、传闻、政策影响、比较判断。**supplementary**: 简单事实问答 |
| `nonstandard_source_awareness` 非标准资讯意识 | 8 | [nonstandard_source_awareness.md](nonstandard_source_awareness.md) | **relevant**: 市场小段子、调研纪要、大V文章、官媒截图、盘中异动。**supplementary**: 其他强时效资讯 |
| `credibility_expression` 可信表达 | 5 | [credibility_expression.md](credibility_expression.md) | **始终 supplementary**。评估语气、边界、风险提示和表达可读性 |
| `tool_usage` 工具使用合理性 | 8 | [tool_usage.md](tool_usage.md) | **始终 relevant**。评估检索、交叉验证、来源选择和工具链路 |

## 动态权重分配规则

1. 仅根据用户问题判断适用性。
2. `relevant` 维度获得较高权重；`supplementary` 保留低权重；`not_applicable` 为 0。
3. 若题目强依赖时间，优先提高 `timeliness_fact_boundary` 和 `fact_evidence_quality`。
4. 若题目要求解释市场异动或热点持续性，提高 `core_signal_extraction` 和 `nonstandard_source_awareness`。
5. 若题目要求"对应标的/影响/受益"，提高 `investment_mapping`。
6. 所有动态权重总和必须等于 100，并在输出中给出简短理由。

## 封顶规则

- [hard_time_or_fact_error（上限 40）](cap_hard_time_or_fact_error.md)
- [stale_or_wrong_evidence（上限 50）](cap_stale_or_wrong_evidence.md)
- [template_answer_without_signal（上限 55）](cap_template_answer_without_signal.md)
- [data_dump_without_judgment（上限 60）](cap_data_dump_without_judgment.md)
- [unverified_rumor_as_fact（上限 50）](cap_unverified_rumor_as_fact.md)

封顶限制最终分数，不替代维度评分。更好的隐藏规划不能覆盖最终答案触发的封顶。

