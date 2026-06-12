# 图片批注锚点

来源：`07_interactive-clarification.docx` 中 `word/media/image1.png` 至 `image89.png`。图片主要是问财/豆包回答截图和人工红绿批注。正文已抽取多数专家结论，但截图里还有可直接用于评分的微观判断。

## 图片与案例映射

| Case | 图片 |
|---|---|
| 1 | image1, image2 |
| 2 | image3, image4 |
| 3 | image5, image6 |
| 4 | image7, image8 |
| 5 | image9, image10 |
| 6 | image11, image12 |
| 7 | image13, image14 |
| 8 | image15, image16 |
| 9 | image17, image18 |
| 10 | image19, image20 |
| 11 | image21, image22 |
| 12 | image23, image24, image25 |
| 13 | image26, image27 |
| 14 | image28, image29 |
| 15 | image30, image31 |
| 16 | image32, image33 |
| 17 | image34, image35 |
| 18 | image36, image37 |
| 19 | image38, image39 |
| 20 | image40, image41 |
| 21 | image42, image43 |
| 22 | image44, image45 |
| 23 | image46, image47, image48 |
| 24 | image49, image50 |
| 25 | image51, image52, image53 |
| 26 | image54, image55, image56 |
| 27 | image57, image58 |
| 28 | image59, image60 |
| 29 | image61, image62 |
| 30 | image63, image64 |
| 31 | image65, image66, image67 |
| 32 | image68, image69, image70 |
| 33 | image71, image72, image73 |
| 34 | image74, image75 |
| 35 | image76, image77 |
| 36 | image78, image79 |
| 37 | image80, image81 |
| 38 | image82, image83 |
| 39 | image84, image85 |
| 40 | image86, image87 |
| 41 | image88, image89 |

## 可复用批注规则

### A. 回本类问题不是新机会推荐

图片锚点：case01 image1/image2。  
人工批注指出：
- 好的首轮应"给出不同回本方案，供用户选择"，不是一上来做股票推荐。
- 需要要求用户输入更详细信息来定义解决方案：持仓、成本、亏损幅度、仓位、买入日期、回本时间。
- 用户目标是"扭亏回本"，不是"买一个新的股票"。即使推荐新票，也必须解释它与原亏损修复路径的关系。
- 当用户第二轮给出股票和亏损信息后，必须围绕该单票/组合的回本概率、所需涨幅、可行路径和风险边界回答。

评分应用：
- 首轮只荐股：`intent_fulfillment` <= 40，`ambiguity_clarification` <= 40。
- 二轮忽略补充信息：触发 `context_break_after_clarification`，`context_continuity` <= 20。

### B. 答案后引导不能只问"要不要"

图片锚点：case12 image23/image24/image25。  
截图显示用户第三轮才问"光隔离器A股的是那几只股票"，说明首轮行业地位回答没有主动满足投资用户的潜在标的需求。图片末尾只问"需要我帮你整理一份核心企业清单吗"，专家认为启迪不足。

评分应用：
- 行业地位/产业链地位类问题，应主动补充代表环节和核心公司，至少给出最小可用清单。
- 只做知识科普、不落到产业链标的：扣 `intent_fulfillment`、`actionability_and_risk_plan`、`guidance_and_retention`。
- 结尾泛问"要不要清单"不等于高质量后续引导。

### C. 红框多标关键变量缺口，绿框多标可保留优点

图片中红色批注通常标出缺失变量、错误前提、错误实体、口径不一致或答案无效处；绿色批注通常标出可保留优点。评测时：
- 不能只按最终胜负评估；问财胜的 case 也可能有红框缺陷。
- 若最终答案保留了绿框优点但触发红框硬错，仍按硬错封顶。
- 根因归因时优先选择红框对应的低分维度。

### D. 错别字识别要考虑"市场概率 + 输入习惯"

图片组 case23-case33 多次呈现错别字/异常代码。人工知识不是简单"相似度最高"，而是：
- A 股用户默认问 A 股概率高于新三板等低频实体。
- 同音/近音和拼音输入习惯优先，如`盛世`->`盛视`、`华成`->`华胜`、`心质`->`新质`。
- 异常代码应检查多输、重复、粘连，如 6004520、0024002400。
- 若存在两个合理候选，应先选择最可能的一个并说明备选，而不是两个混着答。

### E. 规则陷阱应在答案开头纠错

图片组 case34-case41 反复出现交易制度陷阱。人工批注的核心不是"风险提示要多"，而是"错误前提会让整个方案无效"：
- 市价单不能用于科创板盘后固定价格交易。
- 正股 T+1 与转债 T+0 不能混同。
- 分红现金到账不等于落袋为安，卖出时红利税可能补缴。
- 买科创 50 ETF 不需要科创板股票权限。
- 9:22 撤不了应直接绑定集合竞价不可撤规则。

评分应用：
- 错误前提未纠正，`financial_rule_and_premise` <= 20。
- 在错误前提上继续给计划，触发 `wrong_financial_rule_or_unhandled_invalid_premise`。

### F. 模糊条件的"默认口径"必须对用户可见

图片组 case13-case21 显示，专家更认可能显式定义筛选口径的答案：
- `上升通道`可用 MA5 > MA10 > MA20 等定义。
- `近期`需明确近 20 日、近 1 月等，且同答前后一致。
- `股息率高`不能只看静态数值，还要考虑连续分红稳定性。
- `主力高度控盘`若用平台指标，必须解释指标定义。

评分应用：
- 口径清楚即使排序不完美，也应在 `assumption_definition` 给较高分。
- 口径前后不一致，触发 `inconsistent_time_or_definition_scope`。
