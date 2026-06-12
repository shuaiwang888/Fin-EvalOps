# `reasoning` — 财务与业务推理

当系统有信息但没有完成财报解读所需的推理链时使用。

| L2 | 说明 | 典型受影响维度 |
|---|---|---|
| `formula-only-reasoning` | 只用指标公式解释 ROE、现金流、毛利率等变化，没有回答真实原因 | causal_attribution_depth, business_financial_linkage |
| `causal-chain-broken` | 科目变化、业务事实、会计处理和最终结论之间链条断裂 | causal_attribution_depth |
| `main-driver-not-ranked` | 多个因素并列罗列，未区分主因、次因、对冲项和金额贡献 | causal_attribution_depth, composition_credibility |
| `special-accounting-event-missed` | 未识别会计差错更正、收入确认、非经常损益、公允价值、套保、补税等特殊机制 | causal_attribution_depth, primary_evidence_quality |
| `business-translation-missing` | 有财务数据但未说明对应的产品、价格、订单、成本、回款、行业机制或公司战略 | business_financial_linkage |
| `quantitative-bridge-missing` | 有结论但没有占比、差额、敏感度、估值对标或计算闭合 | report_data_accuracy, causal_attribution_depth |
| `sustainability-not-modeled` | 对毛利率、现金流、业绩增长、股价影响的持续性没有条件和观察指标 | forward_investment_judgment |
| `market-impact-one-sided` | 股价影响只讲风险或只讲利好，没有结合预期、已反映程度、估值和行情反应 | forward_investment_judgment |
