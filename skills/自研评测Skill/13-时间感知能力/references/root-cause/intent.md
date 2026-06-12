# L1: intent — 理解问题

是否识别用户问题中的时间意图和锚点需求。

| L2 | 适用失败 | 常见维度 |
|---|---|---|
| missed-temporal-intent | 把"今天/去年/下周"等时间词当作普通修饰语 | temporal_intent_recognition |
| wrong-relative-time-anchor | 没有使用请求时间/时区解析相对时间 | anchor_date_resolution |
| ambiguous-time-not-clarified | 时间口径模糊但未追问或分情形 | premise_correction_clarification |
| wrong-market-entity | 未识别标的所属市场或交易品种 | market_calendar_status |

## 证据要求

证据可来自 `question` 中的时间词、`text_answer` 中的日期处理、`chain` 中是否出现时间锚点识别步骤。
