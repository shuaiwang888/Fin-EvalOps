# 工具使用参考

当前可根据链路评估以下工具策略：

| 工具 | 合理用途 | 指令遵循风险 | 详细规则 |
|---|---|---|---|
| Search | 查原因、政策、事件、定义背景 | 只贴新闻不回答原因 | [search.md](search.md) |
| FinQuery | 查行情、板块、个股、指标、时点数据 | 把查询结果误当最终答案 | [finquery.md](finquery.md) |
| AccessingFullText | 查公告、研报、基金文件和规则原文 | 摘录过多导致主问被淹没 | [accessingfulltext.md](accessingfulltext.md) |
| Forecast | 辅助建议和情景判断 | 用户问定义/原因时滥用预测 | [forecast.md](forecast.md) |
| CodeInterpreter | 计算或整理多项约束 | 用表格替代直接回答 | [codeinterpreter.md](codeinterpreter.md) |
| BackTest | 仅在用户明确要求历史验证、区间表现或策略回测时使用 | 用回测替代定义、原因、比较或约束回答 | [backtest.md](backtest.md) |
| SearchImage | 处理用户提供的截图、图片批注或图表 | 用图片理解替代文本主指令核验 | [searchimage.md](searchimage.md) |
| CustomerServiceFAQ | 查询同花顺 APP、问财、爱基金等产品客服类规则 | 把金融问答或指令执行错当客服问题 | [customerservicefaq.md](customerservicefaq.md) |
| SaveUserProfile | 保存用户明确披露且要求长期记忆的偏好 | 对普通单次查询滥用用户画像保存 | [saveuserprofile.md](saveuserprofile.md) |

评分重点：
- 工具是否围绕用户主指令设计。
- 工具输入是否覆盖用户的时间、对象、范围和排除条件。
- 工具结果是否被转化成用户要求的答案类型。
- 是否避免把数据表、行情事实或长摘录直接当成最终答案。
