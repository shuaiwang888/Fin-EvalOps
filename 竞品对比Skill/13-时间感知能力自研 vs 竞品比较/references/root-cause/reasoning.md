# reasoning

系统是否把自然日、交易日、报告期、披露期、请求时间和市场状态推导成正确结论。

| L2 | 适用失败 | 常见维度 |
|---|---|---|
| natural-day-trading-day-confusion | 混淆自然日、工作日、交易日、下一交易日 | market_calendar_status |
| fiscal-year-calendar-year-confusion | 混淆自然年、财政年、报告期和披露期 | period_disclosure_mapping |
| premise-not-rejected | 明知或应知用户前提不成立仍顺着回答 | premise_correction_clarification |
| date-weekday-inconsistency | 日期和星期推导不自洽 | anchor_date_resolution |
| template-overrides-time-check | 固定行情/分析模板压倒时间核验 | answer_composition_credibility |

## 比较使用

当双方工具证据接近但最终结论不同，优先检查本阶段：谁把时间证据正确转化为答案，谁被模板或错误推理带偏。
