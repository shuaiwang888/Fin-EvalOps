# 评分细则索引

本 rubric 只评估最终回答文本本身。所有维度的证据只能来自用户问题、自研最终回答或竞品最终回答。

## 维度列表

以下维度在评测时根据题目分析动态分配权重。表中“建议权重”仅作参考基准，实际权重由步骤 1 的题目分析决定。

| 维度 | 建议权重 | 文件 | 适用性判断指南 |
|---|---:|---|---|
| `intent_condition_extraction` 意图与条件抽取 | 21 | [intent_condition_extraction.md](intent_condition_extraction.md) | **始终 relevant**。复杂选股首先看最终回答是否完整保留用户条件 |
| `financial_semantics_and_caliber` 金融语义与口径 | 16 | [financial_semantics_and_caliber.md](financial_semantics_and_caliber.md) | **relevant**：涉及指标公式、资金流、龙虎榜、北向、ST/退市、主线题材等 |
| `screening_plan_decomposition` 筛选规划拆解 | 16 | [screening_plan_decomposition.md](screening_plan_decomposition.md) | **relevant**：长问句、多阶段、二次验证、前后依赖、跨领域筛选 |
| `result_correctness_and_coverage` 结果正确性与覆盖 | 19 | [result_correctness_and_coverage.md](result_correctness_and_coverage.md) | **始终 relevant**。最终候选池、字段、无结果说明是否可用 |
| `ranking_and_decision_actionability` 排序与决策可执行性 | 11 | [ranking_and_decision_actionability.md](ranking_and_decision_actionability.md) | **relevant**：用户要求排序、Top N、选一只、候选池或仅显示指定字段 |
| `data_logic_time_boundary` 数据逻辑与时间边界 | 11 | [data_logic_time_boundary.md](data_logic_time_boundary.md) | **relevant**：涉及日期、交易日、分时、K 线、回撤、涨跌幅区间、公式 |
| `composition_credibility` 表达可信度 | 6 | [composition_credibility.md](composition_credibility.md) | **supplementary**：所有题目都有表达可信度要求 |

## 动态权重分配规则

1. 仅阅读用户问题，对每个维度判断适用性：`relevant` / `supplementary` / `not_applicable`。
2. 活跃维度权重总和必须为 100。
3. 长问句和条件很多时，提高 `intent_condition_extraction` 与 `screening_plan_decomposition`。
4. 指标公式、资金、北向、龙虎榜、退市风险等口径复杂时，提高 `financial_semantics_and_caliber` 与 `data_logic_time_boundary`。
5. 含主线题材、合作关系、订单、极端利好、核心技术等非标条件时，提高 `result_correctness_and_coverage`、`financial_semantics_and_caliber` 或 `composition_credibility`，重点看最终回答是否给出可验证依据和边界。
6. 用户要求排序、Top N、选一只或候选池时，提高 `ranking_and_decision_actionability`。
7. 输出无结果或候选池很少时，提高 `result_correctness_and_coverage`，重点检查最终回答是否说明条件过严、数据边界或无结果原因。

## Result-only 通用检查项

每个活跃维度都必须能回指最终回答证据，并覆盖下列检查：
- 是否直接满足用户真实意图，而非只给背景、过程或泛泛建议。
- 是否完整保留显性条件、隐性条件、否定条件、范围条件、排序和输出字段。
- 是否给出明确候选池、排序、分层、无结果解释或可执行判断。
- 是否存在事实、时间、实体、数值、口径、定义或边界错误。
- 是否覆盖用户要求的关键子问题、对象范围、比较维度和必要字段。
- 结论与理由是否闭合，是否有跳步、偷换概念或因果断裂。
- 关键断言是否有证据支撑，是否可验证。
- 是否区分硬条件、软条件、二次验证、不可用数据和需要确认的边界。
- 是否尊重“最新/最近/截至某日/未来某区间”等时间边界。

## 质量标签

- [core_condition_omitted_or_rewritten（参考上限 45）](cap_core_condition_omitted_or_rewritten.md)
- [hard_financial_semantics_or_caliber_error（参考上限 45）](cap_hard_financial_semantics_or_caliber_error.md)
- [unsupported_data_forced_output（参考上限 50）](cap_unsupported_data_forced_output.md)
- [wrong_evidence_strategy（参考上限 55）](cap_wrong_evidence_strategy.md)
- [layered_or_temporal_screening_failure（参考上限 55）](cap_layered_or_temporal_screening_failure.md)
- [missing_required_ranking_or_fields（参考上限 60）](cap_missing_required_ranking_or_fields.md)
- [unverifiable_result_or_data_hallucination（参考上限 50）](cap_unverifiable_result_or_data_hallucination.md)
- [chart_or_table_without_decision_value（参考上限 65）](cap_chart_or_table_without_decision_value.md)

## 质量标签注意事项

- 本类别沿用标签式封顶：质量标签记录在 `applied_caps`，不直接修改 `final_score`。
- 质量标签不替代维度评分；触发标签后仍需完成逐维评分。
- 质量标签只能依据用户问题和最终回答文本触发。
