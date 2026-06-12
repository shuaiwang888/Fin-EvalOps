# evidence

系统找到的时间证据是否正确、充分、可追溯，是否覆盖交易日历、行情日期、公告日期、报告期和披露期。

| L2 | 适用失败 | 常见维度 |
|---|---|---|
| no-calendar-evidence | 需要交易日历但没有核验 | market_calendar_status |
| stale-data-not-detected | 工具/页面返回旧日期但未识别 | data_asof_freshness |
| report-period-evidence-mismatch | 财报/分红证据的报告期、披露日或实施日不匹配 | period_disclosure_mapping |
| insufficient-asof-evidence | 证据没有可确认的时间戳或 as-of | data_asof_freshness |

## 比较使用

比较时优先引用工具输出中的日期、市场状态、报告期和公告时间。若缺少请求时间或工具输出，必须降低置信度。
