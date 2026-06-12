# `evidence` — 检索信息

当系统找到的信息错误、过旧、遗漏关键来源或证据类型不匹配时使用。

| L2 | 说明 | 典型受影响维度 |
|---|---|---|
| `missing-primary-filing` | 未核验年报、季报、业绩快报、分红公告、官网公告、审计意见或附注原文 | primary_evidence_quality, report_data_accuracy |
| `missing-special-disclosure` | 遗漏会计差错更正、收入确认政策变化、问询函、业绩说明会等决定性披露 | primary_evidence_quality, causal_attribution_depth |
| `wrong-period-or-caliber-data` | 使用错误报告期、累计/单季、调整前/调整后、归母/扣非、经营/投资现金流口径 | report_data_accuracy |
| `industry-business-context-missing` | 缺少行业价格、成本机制、订单、产品结构、存储周期、电价煤价等业务背景 | business_financial_linkage, causal_attribution_depth |
| `key-number-missing` | 缺少足以回答问题的核心金额、占比、差额、估值对标、敏感度或官方披露数字 | report_data_accuracy, composition_credibility |
| `unverifiable-number-source` | 核心数字来源不明、无法复核、疑似幻觉或与披露口径不一致 | report_data_accuracy, primary_evidence_quality |
