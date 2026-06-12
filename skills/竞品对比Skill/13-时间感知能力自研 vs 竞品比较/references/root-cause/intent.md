# intent

系统是否正确理解了用户问题中的时间意图、相对日期、市场/品种和需要核验的时间锚点。

| L2 | 适用失败 | 常见维度 |
|---|---|---|
| missed-temporal-intent | 把“今天/去年/下周”等时间词当作普通修饰语 | temporal_intent_recognition |
| wrong-relative-time-anchor | 没有使用请求时间/时区解析相对时间 | anchor_date_resolution |
| ambiguous-time-not-clarified | 时间口径模糊但未追问或分情形 | premise_correction_clarification |
| wrong-market-entity | 未识别标的所属市场或交易品种 | market_calendar_status |

## 比较使用

若一方在 `plan` 或最终答案中明确抽取了时间词、请求日期和目标市场，而另一方直接进入普通行情/分析流程，可将差异归因到本阶段。
