# `composition` — 组织答案

当系统可能有部分信息或逻辑，但最终答案呈现失败时使用。

| L2 | 说明 | 典型受影响维度 |
|---|---|---|
| `key-conclusion-buried` | 核心结论、官方原因或主因埋在长文中，用户难以一眼看到 | composition_credibility, intent_understanding |
| `data-dump-without-synthesis` | 表格和指标很多，但没有主因排序、差额闭合或业务解释 | composition_credibility, causal_attribution_depth |
| `source-and-caliber-labels-missing` | 没有标注报告期、调整口径、来源、同比环比或单季/累计 | composition_credibility, report_data_accuracy |
| `overconfident-forecast-style` | 将股价走势或持续性判断说成确定结论，缺少情景和验证条件 | composition_credibility, forward_investment_judgment |
| `too-generic-template` | 套用"收入、利润、现金流、风险提示"模板，缺少公司特定重点 | composition_credibility, business_financial_linkage |
