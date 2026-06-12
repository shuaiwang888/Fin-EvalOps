# 工具使用参考

当前可根据链路评估以下工具策略：

| 工具 | 合理用途 | 常见错误 | 详细规则 |
|---|---|---|---|
| Search | 查新题材、黑话、公开规则、实时背景 | 用泛新闻替代金融定义 | [search.md](search.md) |
| FinQuery | 查股票、基金、指标、财报、行情和持仓 | 未消歧相似实体；机械接受负 PE 等失真结果 | [finquery.md](finquery.md) |
| BackTest | 检验条件筛选或历史表现 | 用回测替代概念解释 | [backtest.md](backtest.md) |
| Forecast | 做走势或风险情景辅助 | 对定义类问题滥用预测 | [forecast.md](forecast.md) |
| AccessingFullText | 查公告、规则原文、研报、基金持仓明细 | 只摘数据不解释口径 | [accessingfulltext.md](accessingfulltext.md) |
| SearchImage | 图表或截图理解 | 不适合替代金融数据核验 | [searchimage.md](searchimage.md) |
| CustomerServiceFAQ | 查询同花顺 APP、问财、爱基金等产品客服类规则 | 把投资评价、条件选股、诊股等问题错当客服问题 | [customerservicefaq.md](customerservicefaq.md) |
| SaveUserProfile | 保存用户明确披露的偏好、财务背景或投资目标 | 对普通单次查询滥用用户画像保存 | [saveuserprofile.md](saveuserprofile.md) |
| CodeInterpreter | 计算、清洗、比较数据 | 对简单定义题过度使用 | [codeinterpreter.md](codeinterpreter.md) |

评分重点：
- 是否选择能回答该金融语义问题的工具。
- 是否核验实体、产品、指标口径和时间点。
- 是否避免把工具输出原样当作最终金融判断。
- 是否把工具证据转化为定义、边界、规则、口径和结论，而不是只堆数据。
