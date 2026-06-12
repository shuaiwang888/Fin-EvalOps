# L1: evidence — 检索数据

获取的时间数据是否正确、完整。

| L2 | 适用失败 | 常见维度 |
|---|---|---|
| no-calendar-evidence | 需要交易日历但没有核验 | market_calendar_status |
| stale-data-not-detected | 工具/页面返回旧日期但未识别 | data_asof_freshness |
| report-period-evidence-mismatch | 财报/分红证据的报告期、披露日或实施日不匹配 | period_disclosure_mapping |
| insufficient-asof-evidence | 证据没有可确认的时间戳或 as-of | data_asof_freshness |

## 证据要求

证据可来自工具调用输出中的日期字段、数据页面的时间戳、财报报告期字段等。
