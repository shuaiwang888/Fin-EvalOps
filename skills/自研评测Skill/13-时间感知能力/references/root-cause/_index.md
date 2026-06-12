# 时间感知根因归因

根因必须解释“为什么最终答案的时间判断错了”，并绑定证据。优先选择最能压低分数的维度；若触发封顶规则，封顶违规维度通常是主根因。

## L1/L2 根因

### intent

| L2 | 适用失败 | 常见维度 |
|---|---|---|
| missed-temporal-intent | 把“今天/去年/下周”等时间词当作普通修饰语 | temporal_intent_recognition |
| wrong-relative-time-anchor | 没有使用请求时间/时区解析相对时间 | anchor_date_resolution |
| ambiguous-time-not-clarified | 时间口径模糊但未追问或分情形 | premise_correction_clarification |
| wrong-market-entity | 未识别标的所属市场或交易品种 | market_calendar_status |

### evidence

| L2 | 适用失败 | 常见维度 |
|---|---|---|
| no-calendar-evidence | 需要交易日历但没有核验 | market_calendar_status |
| stale-data-not-detected | 工具/页面返回旧日期但未识别 | data_asof_freshness |
| report-period-evidence-mismatch | 财报/分红证据的报告期、披露日或实施日不匹配 | period_disclosure_mapping |
| insufficient-asof-evidence | 证据没有可确认的时间戳或 as-of | data_asof_freshness |

### tool

| L2 | 适用失败 | 常见维度 |
|---|---|---|
| calendar-tool-missing | 应查交易日历、行情日历或市场状态但未调用 | tool_usage |
| wrong-tool-date-input | 工具输入日期、市场、代码或报告期错误 | tool_usage |
| tool-output-date-misread | 工具返回日期正确但链路误读 | data_asof_freshness |
| fallback-without-disclosure | 工具无数据后使用替代数据但未在答案披露 | data_asof_freshness |

### reasoning

| L2 | 适用失败 | 常见维度 |
|---|---|---|
| natural-day-trading-day-confusion | 混淆自然日、工作日、交易日、下一交易日 | market_calendar_status |
| fiscal-year-calendar-year-confusion | 混淆自然年、财政年、报告期和披露期 | period_disclosure_mapping |
| premise-not-rejected | 明知或应知用户前提不成立仍顺着回答 | premise_correction_clarification |
| date-weekday-inconsistency | 日期和星期推导不自洽 | anchor_date_resolution |
| template-overrides-time-check | 固定行情/分析模板压倒时间核验 | answer_composition_credibility |

### composition

| L2 | 适用失败 | 常见维度 |
|---|---|---|
| asof-not-visible | 链路可能知道数据日期，但最终答案没有写清 | data_asof_freshness |
| correction-buried | 纠错信息被放在后文或弱化，用户仍会误解 | premise_correction_clarification |
| misleading-current-tense | 用“今天/当前/最新”等措辞包装旧数据 | answer_composition_credibility |

### capability_gap

| L2 | 适用失败 | 常见维度 |
|---|---|---|
| market-calendar-coverage-gap | 工具或数据源缺少目标市场日历，且模型未说明限制 | tool_usage |
| disclosure-data-coverage-gap | 财报/分红数据源缺少目标报告期或字段，且模型未说明限制 | period_disclosure_mapping |

### cap

| L2 | 适用失败 | 常见维度 |
|---|---|---|
| hard-wrong-anchor-date | 核心相对日期/星期/年份解析错误且影响主结论 | anchor_date_resolution |
| market-closed-answered-as-open | 休市日仍给出当日交易结论 | market_calendar_status |
| stale-data-masquerading-as-today | 旧数据冒充当前事实且未标注 as-of | data_asof_freshness |
| missing-premise-correction | 用户时间前提明显错误但答案未先纠错 | premise_correction_clarification |
| fiscal-period-disclosure-error | 财报/分红报告期与披露日/实施日混淆 | period_disclosure_mapping |
| fabricated-time-fact | 编造市场日历、公告日期或报告期事实 | temporal_intent_recognition |

## 证据规则

- 证据可来自 `question`、`text_answer`、`context`、`chain[N].plan`、`chain[N].tools[M]`、`chain[N].tools[M].output`。
- 不要用长引文；证据摘要写清“日期/市场/数据时点/报告期”即可。
- 如果缺少请求时间，涉及相对日期的评测应降低置信度，并在根因中说明证据不足。

## 置信度规则

- `high`：问题和答案中直接出现冲突日期、休市、旧数据或错误报告期。
- `medium`：链路证据显示较可能出错，但最终答案未暴露所有细节。
- `low`：缺少请求时间、工具输出或市场日历证据，只能判断风险。
