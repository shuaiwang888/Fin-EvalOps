# `intent` — 理解问题

当系统没有正确理解用户真正要什么时使用。

| L2 | 说明 | 典型受影响维度 |
|---|---|---|
| `surface-financial-question-only` | 只回答指标定义或通用财务逻辑，没有识别用户要具体公司具体报告期的原因 | intent_understanding, causal_attribution_depth |
| `false-premise-not-corrected` | 未纠正用户对亏损、报告期、累计/单季、调整前/调整后等前提错误 | intent_understanding, report_data_accuracy |
| `decision-conclusion-missed` | 用户问利好利空、股价影响、能否维持或是否真实，但答案没有明确结论 | intent_understanding, forward_investment_judgment |
| `period-and-caliber-constraint-missed` | 未识别年报/Q1/三季报/官网公告/分红方案等报告期和来源约束 | intent_understanding, report_data_accuracy |
| `company-specific-context-missed` | 把公司特定问题处理成行业或教科书问题，忽略公司近期特殊公告或业务背景 | intent_understanding, primary_evidence_quality |
