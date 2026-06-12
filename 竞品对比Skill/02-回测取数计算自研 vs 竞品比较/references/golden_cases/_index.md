# 专家案例基准

本文件沉淀专家文档中的高频评判锚点。评分时先判断用户问题是否与下列案例语义匹配；匹配时，将对应 hard checks 作为证据核验清单。不要因为答案表面流畅、规划链路漂亮或耗时较短而放松这些检查。

## 使用规则

- 语义匹配即可使用，不要求用户问题逐字相同。
- hard checks 优先于泛化表述：如果答案违反 hard checks，应在相应维度扣分并按需触发封顶规则。
- 已给出明确日期、口径或公式的案例，必须据此核验；未给出最终数值的案例，重点核验样本完整性、时间锚点、公式和明细可验证性。
- 如专家文档存在疑似笔误，不能机械沿用，应回到交易日历或结构化数据核验。

## Case 1: 2026 年一季度名称含"顺"的 A 股及区间涨跌幅

hard checks:
- 必须全市场筛选 A 股名称中包含"顺"的股票，不能只列少量样本。
- 必须计算 2026 年一季度区间涨跌幅，并说明起止交易日或价格口径。
- 若样本严重不全，后续排序、均值或结论均不可靠，应扣 `data_retrieval_accuracy` 并可触发 `missing_required_data`。

主要维度：`data_retrieval_accuracy`, `calculation_accuracy`, `result_verifiability`

## Case 2: 2026-03-09 13:11 买入一手中国石油的当时价值

hard checks:
- 2026-03-09 是交易日，不能声称该日不是交易日。
- 用户要求 13:11 的日内精度，应使用分时/逐笔价格；只用日线收盘价或开盘价不能视为精确回答。
- 若无法取得分时数据，必须明确说明限制，只能给近似估算。
- 用日线价格包装成确定金额时，应触发 `intraday_precision_missing`；若还误判交易日，应触发 `time_inference_error`。

主要维度：`time_inference`, `data_retrieval_accuracy`, `tool_usage`

## Case 3: 2025 年五一节前 5 日股价一共涨幅大于 10% 的股票

hard checks:
- "五一节前 5 日"应按节前 5 个实际交易日理解，而非简单日历日前 5 天。
- 2025 年五一长假前 5 个交易日应核验为 2025-04-24、2025-04-25、2025-04-28、2025-04-29、2025-04-30。
- 错解为 2025-04-21 至 2025-04-25 会导致后续选股和涨幅计算全部失效，应触发 `time_inference_error`。
- 必须全市场筛选并展示必要明细，不能只给无法核验的少量示例。

主要维度：`time_inference`, `data_retrieval_accuracy`, `calculation_accuracy`

## Case 4: 过去 5 年同花顺发布年报次日涨跌幅大于 3% 的概率

hard checks:
- 必须锚定"年报披露日期/发布日期"，不能用报告期末、年报标题年份或其他公告日期替代。
- "次日"应指披露日后的下一个交易日。
- 概率需要列出每年披露日期、次日交易日、次日涨跌幅、是否大于 3%。

主要维度：`time_inference`, `data_retrieval_accuracy`, `calculation_accuracy`, `result_verifiability`

## Case 5: 同花顺 2025 年报指标提取、毛利率和期间费用率、与 2024 年同比

hard checks:
- 必须提取营业收入、营业成本、销售费用、管理费用、研发费用，2024 与 2025 均要覆盖。
- 毛利率公式：`(营业收入 - 营业成本) / 营业收入`。
- 期间费用率公式：`(销售费用 + 管理费用 + 研发费用) / 营业收入`。
- "变化超过 5 个百分点"必须按百分点差值筛选，并完整列出所有超阈值指标；不能漏掉研发费用率等关键指标。
- 取错基础字段如 2024 年营业成本，会级联污染毛利率和同比判断。

主要维度：`intent_fulfillment`, `data_retrieval_accuracy`, `calculation_accuracy`, `logical_decomposition`

## Case 6: 上市以来同花顺涨停后第二天高开的概率

hard checks:
- "上市以来"要求完整历史样本，不能只统计最近一年或最近几次涨停。
- 必须列出每次涨停日期、次日开盘价/前收盘或对应高开判断、分子分母和概率。
- 专家文档指出"声称 65%"且无可信明细属于虚构风险，核验记录显示该类错误应按数据虚构严惩；如答案无明细，不得仅凭表面统计接受概率。

主要维度：`data_retrieval_accuracy`, `calculation_accuracy`, `result_verifiability`

## Case 7: 2025 年连续两个交易日全市场下跌家数超过 4000 后买入沪深 300 的收益率

hard checks:
- 必须先找出 2025 年全市场下跌家数超过 4000 的交易日，再识别连续两个交易日同时满足条件的窗口。
- 必须把触发窗口传递到交易策略：在满足条件时收盘买入沪深 300，第二个交易日收盘卖出。
- 不能直接回答"没有满足日期"而不展示筛选过程。
- 专家文档中个别日期表述可能存在笔误，评测时应以交易日历和全市场涨跌家数核验，不机械沿用疑似错误日期。

主要维度：`logical_decomposition`, `data_retrieval_accuracy`, `calculation_accuracy`, `tool_usage`

## Case 8: 过去 10 年 3 月 A 股上涨概率最高和下跌概率最高的三个行业

hard checks:
- 必须覆盖过去 10 年每年 3 月的行业区间涨跌统计，行业分类口径需一致。
- 上涨概率和下跌概率不能方向颠倒；专家核验指出有色金属在该案例中是上涨概率最低方向，而非上涨概率最高。
- 若链路明显低效且仍给出反向结论，应同时扣 `tool_usage` 和 `data_retrieval_accuracy`。

主要维度：`data_retrieval_accuracy`, `calculation_accuracy`, `tool_usage`

## Case 9: 10 年前今天买入同花顺和东方财富并分红再投资到今天

hard checks:
- "今天"必须锚定评测上下文日期，"10 年前的今天"需处理非交易日顺延/前推口径。
- 分红再投资场景应使用前复权收盘价或等价复权收益方法，不能用未复权价直接比较。
- 必须列出买入日期、买入价格口径、当前价格口径、股数或资产价值计算过程。

主要维度：`time_inference`, `calculation_accuracy`, `data_retrieval_accuracy`

## Case 10: 2026-03-10 开盘买入贵州茅台和中国石油，到 2026-03-25 收盘盈亏

hard checks:
- 必须使用 2026-03-10 开盘价和 2026-03-25 收盘价。
- 一手 A 股通常按 100 股计算，"两手"为 200 股；若口径不同必须说明。
- 必须分别计算单股、单标的总额和组合总盈亏。
- 应用汇总表展示买入价、卖出价、股数、初始金额、期末金额、盈亏金额和盈亏方向。

主要维度：`calculation_accuracy`, `data_retrieval_accuracy`, `expression_quality`

## Case 11: 复合回测必须先规划中间条件

hard checks:
- 对"先发生市场条件，再按条件买入卖出"的问法，必须显式拆成条件发现、信号生成、交易执行、收益计算。
- 只停留在一步信息抽取或直接给策略结论，属于多步规划缺失。

主要维度：`logical_decomposition`, `tool_usage`

## Case 12: 历史上博迈科涨停后连续涨停天数

hard checks:
- 必须输出涨停日明细：日期、对应连板天数、统计口径、涨停类型。
- 仅输出"一般几天"、"最多几天"等宏观结论不可验证，应触发或接近触发 `unverifiable_result`。
- 若统计结果与明细不能相互复算，应同时扣 `calculation_accuracy`。

主要维度：`result_verifiability`, `data_retrieval_accuracy`, `calculation_accuracy`
