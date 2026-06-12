# 根因分类索引

根因用于解释为什么答案失分，不能替代维度评分。每个根因必须绑定证据。

## 选择流程

1. 先检查是否触发封顶规则。若触发 critical 封顶，优先把封顶违规维度作为主根因。
2. 再按活跃维度 `raw_score` 升序排序；并列时按动态权重降序，再按维度名字母序。
3. 最低分维度映射到默认 L1，但允许根据证据调整。
4. 每个根因选择一个 L1/L2，并写一句能解释本题失败机制的 summary。
5. 最多返回 8 个根因。所有活跃维度 raw_score >= 60 且无封顶触发时允许为空，否则至少一个根因。

## L1 分类

- [intent.md](intent.md)：真实咨询目标、隐含需求、子问题遗漏。
- [context.md](context.md)：多轮承接、用户补充、前轮承诺。
- [evidence.md](evidence.md)：实体、规则、行情、公告、数据证据。
- [tool.md](tool.md)：工具选择、参数、候选验证、链路效率。
- [reasoning.md](reasoning.md)：错误前提、规则推理、口径定义、因果顺序。
- [composition.md](composition.md)：答案组织、直接回答、模板化、后续引导。

## 维度默认映射

| 维度 | 默认 L1 |
|---|---|
| `intent_fulfillment` | intent |
| `ambiguity_clarification` | reasoning |
| `context_continuity` | context |
| `entity_resolution` | evidence |
| `financial_rule_and_premise` | reasoning |
| `assumption_definition` | reasoning |
| `actionability_and_risk_plan` | composition |
| `evidence_grounding` | evidence |
| `guidance_and_retention` | composition |
| `tool_usage` | tool |
| `latency_efficiency` | tool |
