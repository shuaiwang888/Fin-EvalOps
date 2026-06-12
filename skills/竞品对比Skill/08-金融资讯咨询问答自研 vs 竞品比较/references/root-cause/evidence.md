# L1: evidence

系统没有找到正确、充分、时效匹配的信息。

| L2 | 说明 | 常见受影响维度 |
|---|---|---|
| `time_window_not_enforced` | 没落实最新、近两周、当天、截至某日等时间边界 | `timeliness_fact_boundary` |
| `outdated_evidence` | 用旧公告、旧新闻或长期主线替代当前事件 | `timeliness_fact_boundary`, `fact_evidence_quality` |
| `wrong_evidence_source` | 来源类型不匹配，如用研报替代当天催化，用传闻替代公告事实 | `fact_evidence_quality`, `nonstandard_source_awareness` |
| `insufficient_evidence` | 关键事实、数据口径、项目状态或原因证据不足 | `fact_evidence_quality` |
| `nonstandard_source_missing` | 需要小段子、调研纪要、大V文章、官媒截图时未覆盖 | `nonstandard_source_awareness`, `core_signal_extraction` |
| `source_boundary_blurred` | 没区分事实、传闻、纪要交流和观点 | `fact_evidence_quality`, `credibility_expression` |

