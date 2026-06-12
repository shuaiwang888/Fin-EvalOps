# 评分细则索引

本 rubric 只评估最终回答文本本身。所有维度的证据只能来自用户问题、自研最终回答或竞品最终回答。

## 维度列表

以下维度在评测时根据题目分析动态分配权重。表中“建议权重”仅作参考基准，实际权重由步骤 1 的题目分析决定。

| 维度 | 建议权重 | 文件 | 适用性判断指南 |
|---|---:|---|---|
| `semantic_intent_alignment` 语义意图匹配 | 22 | [semantic_intent_alignment.md](semantic_intent_alignment.md) | **始终 relevant**。判断是否读懂用户真实对象、真实任务、错别字、黑话和隐含语义 |
| `financial_term_understanding` 金融术语/规则理解 | 22 | [financial_term_understanding.md](financial_term_understanding.md) | **relevant**: 涉及金融术语、交易规则、市场黑话、财务概念。**supplementary**: 只需少量基础常识解释 |
| `entity_product_boundary` 实体与产品边界 | 17 | [entity_product_boundary.md](entity_product_boundary.md) | **relevant**: 涉及同名公司、近名公司、股票/基金/ETF/指数/现货、基金公司及旗下产品。**supplementary**: 对象单一但仍需核对边界 |
| `metric_caliber_accuracy` 指标公式与数据口径 | 17 | [metric_caliber_accuracy.md](metric_caliber_accuracy.md) | **relevant**: 涉及 PE、ROE、主力控盘、ST、披露期、盘中价格等公式、规则或口径。**not_applicable**: 纯概念语义且无指标口径 |
| `timeliness_context` 时效上下文 | 11 | [timeliness_context.md](timeliness_context.md) | **relevant**: 涉及最新、近期、当下、盘中、报告期、截至某日。**supplementary**: 其他金融语义题 |
| `credibility_expression` 可信解释与表达 | 11 | [credibility_expression.md](credibility_expression.md) | **始终 supplementary**；用户要求解释、定义、区别、操作建议时可提高为 relevant |

## 动态权重分配规则

1. 仅阅读用户问题，对每个维度判断适用性：`relevant` / `supplementary` / `not_applicable`。
2. `relevant` 维度获得较高权重，从 `not_applicable` 或低相关维度让出权重。
3. `supplementary` 维度保留低权重，通常 3-12。
4. `not_applicable` 维度权重 = 0，评分阶段跳过。
5. 所有动态权重之和必须 = 100。
6. 权重分配须附简短理由，记录在输出的 `weight_assignment[*].rationale` 中。

## Result-only 通用检查项

每个活跃维度都必须能回指最终回答证据，并覆盖下列检查：
- 是否直接满足用户真实意图，而非只给背景、数据或泛泛建议。
- 是否给出明确的定义、边界、规则、判断或可执行建议。
- 是否存在金融术语、交易规则、实体、产品、指标、时间、事实或边界错误。
- 是否覆盖用户要求的关键子问题、对象范围、比较维度和必要解释。
- 结论与理由是否闭合，是否有跳步、偷换概念或因果断裂。
- 关键断言是否有证据支撑，是否可验证。
- 面对错别字、黑话、俚语和新题材时，是否能合理纠偏并说明不确定性。
- 涉及操作建议、筛选、排序或卖出/加仓时，是否给出条件、限制和风险。
- 是否尊重“最新/近期/当下/盘中/报告期/截至某日”等时间边界。

## 关键扣分方向

- 把用户真实对象理解错，例如黄金实物问成 ETF、豪威集团答成豪能股份。
- 概念只会给数，不会解释，例如问微盘股定义却只给流通市值数据。
- 规则硬错，例如集合竞价 9:20 当成已成交量、最新季度 ROE 使用未披露报告期。
- 指标口径失真，例如 PE 最小直接包含负 PE、主力控盘比例不解释定义。
- 新题材或黑话误判，例如 Token 只按区块链代币理解，老登股只按上市年限理解。
- 定义、边界和结论不清，只输出空泛风险提示或模板建议。

## 封顶标签

- `hard_concept_or_rule_error`：金融概念或交易规则硬错，参考上限 40。
- `wrong_entity_or_product`：实体或产品错配，参考上限 45。
- `missed_core_definition`：遗漏核心定义，参考上限 55。
- `metric_caliber_unexplained_or_invalid`：指标口径未解释或失真，参考上限 60。
- `stale_or_wrong_time_context`：时效上下文错误，参考上限 60。
- `empty_generic_advice`：泛泛建议，参考上限 65。

## 封顶标签注意事项

- 本类别沿用原规则：封顶规则作为质量标签记录在 `applied_caps`，不直接修改 `final_score`。
- 封顶标签不替代维度评分；触发标签后仍需完成逐维评分。
- 封顶标签只能依据用户问题和最终回答文本触发。

## 维度边界区分

- `semantic_intent_alignment` vs `financial_term_understanding`：前者看是否读懂用户真正问什么，后者看金融术语、规则和概念解释是否正确。
- `entity_product_boundary` vs `metric_caliber_accuracy`：前者看对象边界，后者看指标公式、数据口径、报告期和时点。
- `timeliness_context` vs `credibility_expression`：前者看时间语义是否正确，后者看最终回答是否结构清楚、证据充分、措辞审慎。
