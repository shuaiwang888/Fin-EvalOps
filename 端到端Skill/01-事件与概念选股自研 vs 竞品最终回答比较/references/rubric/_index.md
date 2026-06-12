# 评分细则索引

本 rubric 只评估最终回答文本本身。所有维度的证据只能来自用户问题、自研最终回答或竞品最终回答。

## 维度列表

以下维度在评测时根据题目分析动态分配权重。表中"建议权重"仅作参考基准，实际权重由步骤 1 的题目分析决定。

| 维度 | 建议权重 | 文件 | 适用性判断指南 |
|---|---|---|---|
| `intent_fulfillment` 意图满足度 | 22 | [intent_fulfillment.md](intent_fulfillment.md) | **始终 relevant**。所有题目均考察意图完成度 |
| `event_abstraction` 事件抽象度 | 16 | [event_abstraction.md](event_abstraction.md) | **relevant**: 涉及具体事件/催化剂/政策/地缘/主题驱动。**supplementary**: 一般概念、产业主题或海外映射。**not_applicable**: 纯条件筛选无事件层 |
| `industry_mapping` 产业链映射 | 14 | [industry_mapping.md](industry_mapping.md) | **relevant**: 需要产业链、产能份额、主营产品、客户供货、上下游、海外映射或受益链条。**not_applicable**: 纯数据查询无产业链需求 |
| `ranking_judgment` 排序判断 | 16 | [ranking_judgment.md](ranking_judgment.md) | **relevant**: 用户明确要求排序/排名/优先级/最受益/龙头/弹性最大。**supplementary**: 隐含排序或核心标的筛选需求 |
| `logic_closure` 逻辑闭环 | 17 | [logic_closure.md](logic_closure.md) | **始终 relevant**。所有题目均考察逻辑完整性 |
| `timeliness_fact_boundary` 时效性与事实边界 | 10 | [timeliness_fact_boundary.md](timeliness_fact_boundary.md) | **relevant**: 涉及"最新/近期/截至某日"等时效要求。**supplementary**: 其他题目 |
| `credibility_expression` 可信度与表达 | 5 | [credibility_expression.md](credibility_expression.md) | **始终 supplementary**。表达质量始终有参考价值 |

## 动态权重分配规则

1. 仅阅读用户问题，对每个维度判断适用性：`relevant` / `supplementary` / `not_applicable`。
2. `relevant` 维度获得较高权重，从 `not_applicable` 或低相关维度让出权重。
3. `supplementary` 维度保留低权重，通常 3-10。
4. `not_applicable` 维度权重 = 0，评分阶段跳过。
5. 所有动态权重之和必须 = 100。
6. 权重分配须附简短理由，记录在输出的 `weight_assignment[*].rationale` 中。

## Result-only 通用检查项

每个活跃维度都必须能回指最终回答证据，并覆盖下列检查：
- 是否直接满足用户真实意图，而非只给背景、过程或泛泛建议。
- 是否给出明确结论、排序、分层或可执行判断。
- 是否存在事实、时间、实体、数值、口径、定义或边界错误。
- 是否覆盖用户要求的关键子问题、对象范围、比较维度和必要步骤。
- 结论与理由是否闭合，是否有跳步、偷换概念或因果断裂。
- 关键断言是否有证据支撑，是否可验证。
- 需要推荐、排名、最受益、最相关时，是否给出清晰优先级标准。
- 是否区分核心受益、次级受益、弱关联、概念蹭边。
- 是否区分主营/副业、直接/间接、上游/中游/下游、品牌/代工、核心产品/边缘产品。
- 是否避免只用概念标签、涨跌幅、市值、成交额替代投资逻辑。
- 是否尊重“最新/最近/截至某日/未来某区间”等时间边界。

## 封顶标签

- [hard_time_or_fact_error（参考上限 40）](cap_hard_time_or_fact_error.md)
- [missing_required_ranking（参考上限 60）](cap_missing_required_ranking.md)
- [data_dump_without_core_rationale（参考上限 55）](cap_data_dump_without_core_rationale.md)
- [wrong_evidence_type（参考上限 50）](cap_wrong_evidence_type.md)
- [unverifiable_subjective_expression（参考上限 65）](cap_unverifiable_subjective_expression.md)
- [forced_mapping_or_entity_boundary_error（参考上限 50）](cap_forced_mapping_or_entity_boundary_error.md)

## 封顶标签注意事项

- 本类别沿用原规则：封顶规则作为质量标签记录在 `applied_caps`，不直接修改 `final_score`。
- 封顶标签不替代维度评分；触发标签后仍需完成逐维评分。
- 封顶标签只能依据最终回答文本触发。

## 维度边界区分

- `industry_mapping` vs `logic_closure`：`industry_mapping` 侧重映射准确性（事件是否正确对应到受益产业链、环节、公司），`logic_closure` 侧重推理完整性（从事件到股票的因果链是否闭合、数据是否服务论点）。映射对但推理断裂扣 `logic_closure`；映射错但推理自洽扣 `industry_mapping`。
- `event_abstraction` vs `logic_closure`：`event_abstraction` 侧重驱动因素提取（是否识别了真正的催化剂、供给/需求拐点），`logic_closure` 侧重逻辑链完整性（提取出的驱动因素是否完整传导到个股结论）。提取正确但传导断裂扣 `logic_closure`；提取错误或停留在表面复述扣 `event_abstraction`。
