# `intent` — 理解问题

当系统误解了用户的根本需求时使用。

| L2 | 说明 | 典型受影响维度 |
|---|---|---|
| `hidden-intent-missed` | 回答了相关概念而非最受益标的，或列出范围但无决策支持 | intent_fulfillment |
| `constraint-missed` | 忽略了必要排序、明确时间范围或用户指定的筛选条件 | intent_fulfillment, ranking_judgment |
| `comparison-target-misread` | 将对标、映射、类比、最像谁等任务理解成泛概念介绍，遗漏关键比较维度 | intent_fulfillment, industry_mapping |
| `scope-too-narrow` | 只回答单一标的、单一环节或单一国内口径，未覆盖用户要求的全球/国内、上下游、主板、产能最高等范围 | intent_fulfillment, industry_mapping |
