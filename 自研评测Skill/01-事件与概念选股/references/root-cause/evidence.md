# `evidence` — 检索信息

当系统找到了错误的信息、遗漏了关键信息、或使用了过时/超出范围的材料——但工具选择和使用本身是正确的。

| L2 | 说明 | 典型受影响维度 |
|---|---|---|
| `wrong-evidence-type` | 用券商报告充当突发新闻，用通用主题简报替代事件证据，或用过时材料处理近期事件 | timeliness_fact_boundary |
| `time-scope-mismatch` | 混入时间窗口外信息，使用错误截止日期，或年份锚定错误 | timeliness_fact_boundary |
| `entity-linking-error` | 遗漏核心标的，关联弱相关标的，或行业实体边界划定错误 | industry_mapping |
| `quant-evidence-missing` | 对产能、市占率、订单、客户、价格、成本、现金流、股价表现等关键断言缺少量化或可验证证据。归因时区分：若数据未解释如何支撑结论→归 `logic_closure`；若断言本身缺少可验证来源→归 `credibility_expression` | logic_closure, credibility_expression |
| `benchmark-evidence-missing` | 需要国际巨头、国内龙头、竞品或历史案例对比时，缺少对照组证据，导致"最强/最高/对标"无法成立 | industry_mapping, ranking_judgment |
| `data-hallucination` | 使用错误或无法核验的涨幅、区间表现、产能、市占率、订单、供货关系等数据支撑核心结论 | timeliness_fact_boundary, credibility_expression |
