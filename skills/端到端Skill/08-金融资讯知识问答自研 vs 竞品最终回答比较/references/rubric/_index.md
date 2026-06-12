# 评分细则索引

## 维度列表

以下维度在评测时根据题目分析动态分配权重。表中建议权重仅作参考基准，实际权重由步骤 0 的题目分析决定。该列表保留原 08 中不依赖工程链路数据的答案质量维度，并移除过程维度。

| 维度 | 建议权重 | 文件 | 适用性判断指南 |
|---|---:|---|---|
| `intent_fulfillment` 意图满足度 | 16 | [intent_fulfillment.md](intent_fulfillment.md) | **始终 relevant**。评估是否回答显性问题和隐含投资诉求 |
| `timeliness_fact_boundary` 时效性与事实边界 | 16 | [timeliness_fact_boundary.md](timeliness_fact_boundary.md) | **relevant**: 最新、近期、近两周、当天、截至某日、项目进展、政策年份。**supplementary**: 一般知识问答 |
| `fact_evidence_quality` 事实证据质量 | 18 | [fact_evidence_quality.md](fact_evidence_quality.md) | **始终 relevant**。评估事实、数据口径、来源类型和可核验性 |
| `information_integration` 资讯整合与比较 | 13 | [information_integration.md](information_integration.md) | **relevant**: 多政策/监管/产业/公司事件整合，或横向比较。**supplementary**: 单点事实查询 |
| `investment_mapping` 投资映射与落地 | 12 | [investment_mapping.md](investment_mapping.md) | **relevant**: 影响、受益标的、行业方向、A 股映射。**not_applicable**: 纯百科事实且无金融落地需求 |
| `core_signal_extraction` 核心信号提炼 | 11 | [core_signal_extraction.md](core_signal_extraction.md) | **relevant**: 市场异动、热点、传闻、政策影响、比较判断。**supplementary**: 简单事实问答 |
| `nonstandard_source_awareness` 非标准资讯意识 | 8 | [nonstandard_source_awareness.md](nonstandard_source_awareness.md) | **relevant**: 市场小段子、调研纪要、大 V 文章、官媒截图、盘中异动。**supplementary**: 其他强时效资讯 |
| `credibility_expression` 可信表达 | 6 | [credibility_expression.md](credibility_expression.md) | **始终 supplementary**。评估语气、边界、风险提示和表达可读性 |

## 动态权重分配规则

1. 仅阅读用户问题，对每个维度判断适用性：`relevant` / `supplementary` / `not_applicable`。
2. `relevant` 维度获得较高权重，并吸收 `not_applicable` 维度让出的权重。
3. `supplementary` 维度保留低权重，通常为 3-8。
4. `not_applicable` 维度权重 = 0，评分阶段跳过。
5. 所有动态权重之和必须 = 100。
6. 权重分配须附简短理由。
7. 自研与竞品必须使用同一套活跃维度和动态权重。

## 封顶标签

- [hard_time_or_fact_error](cap_hard_time_or_fact_error.md)
- [stale_or_wrong_evidence](cap_stale_or_wrong_evidence.md)
- [template_answer_without_signal](cap_template_answer_without_signal.md)
- [data_dump_without_judgment](cap_data_dump_without_judgment.md)
- [unverified_rumor_as_fact](cap_unverified_rumor_as_fact.md)

## 封顶标签注意事项

- 封顶规则作为质量标签写入 `applied_caps`，不要求 LLM 手工改写 `final_score`。
- 最终回答触发质量标签时，必须给出来自用户问题或最终回答的 evidence。
- 同一答案可以触发多个质量标签。
- 只有与活跃维度相关的封顶标签才触发。
