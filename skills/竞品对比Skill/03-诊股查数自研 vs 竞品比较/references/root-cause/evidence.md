# `evidence` — 检索数据/证据

当工具选择基本合理，但获取的数据或证据本身不足、错误或不新时使用。

| L2 | 说明 | 典型受影响维度 |
|---|---|---|
| `wrong-data-value` | 数据值、字段、标的、价格、客户、行业、宏观指标错误 | data_accuracy_coverage |
| `data-depth-insufficient` | 历史深度不足，如上市以来、多年序列、连续 K 线只取部分样本 | data_accuracy_coverage, result_verifiability |
| `data-completeness-gap` | 覆盖不全，遗漏年份、标的、指标、分红事件、行业板块或样本 | data_accuracy_coverage, intent_fulfillment |
| `nonpublic-source-gap` | 对客户、增长点、调研纪要、产业数据等非结构化/非公开资料没有补充证据 | data_accuracy_coverage, insight_extension |
| `stale-evidence` | 使用过期价格、过期宏观数据、旧分红进展或旧行业数据 | data_accuracy_coverage, time_caliber_precision |
| `source-quality-weak` | 证据来源质量弱，关键判断缺少公告、研报、龙虎榜、调研纪要或可定位来源 | result_verifiability, insight_extension |
