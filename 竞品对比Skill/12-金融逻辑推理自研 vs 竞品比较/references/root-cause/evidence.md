# `evidence` — 证据收集

当系统证据不足、证据口径错误或证据无法覆盖金融逻辑推理需求时使用。

| L2 | 说明 | 典型受影响维度 |
|---|---|---|
| `market-driver-evidence-missing` | 缺少热点、事件催化、资金承接、技术形态或基本面变化证据 | market_driver_identification |
| `stock-attribute-evidence-missing` | 缺少主营、业务占比、订单、产能、客户、盈利质量、估值或安全边际证据 | financial_logic_chain, evidence_to_conclusion |
| `stale-or-wrong-evidence` | 证据过时、时间窗口不匹配或关键事实错误 | market_driver_identification, evidence_to_conclusion |
| `single-indicator-overused` | 过度依赖单一指标，如 PE、涨幅、资金流或技术形态 | financial_logic_chain, evidence_to_conclusion |
| `conflicting-evidence-unresolved` | 多来源证据冲突但未解释口径或优先级 | evidence_to_conclusion, decision_value_expression |
| `risk-evidence-missing` | 缺少支撑风险判断、失效条件或情景推演的证据 | scenario_risk_reasoning |

若证据存在于工具输出中但没有进入最终答案，优先考虑 `reasoning` 或 `composition` 根因。
