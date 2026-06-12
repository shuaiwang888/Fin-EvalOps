# 时间感知工具使用参考

评分 `tool_usage` 时只看链路是否使用了适合本题的工具、输入是否正确、是否正确读取工具返回的日期和 as-of。

## 常见工具期望

| 工具 | 适用 | 正确用法 | 常见错误 |
|---|---|---|---|
| Search | 节假日、交易所公告、港股/海外休市、最新新闻、公告披露 | 查询目标市场 + 目标日期 + 休市/公告/节假日；核验发布日期 | 泛搜后拿旧新闻当最新；未区分市场 |
| FinQuery | 行情、涨跌幅、财务数据、分红、证券基础信息 | 输入正确代码、市场、日期、报告期；读取返回日期/as-of | 查询上一交易日却回答今天；报告期字段用错 |
| BackTest | 前 N 个交易日、历史区间收益、策略窗口 | 使用交易日窗口而不是自然日窗口；说明区间起止 | 把“近 20 个交易日”当自然日 |
| Forecast | 未来走势预测 | 先确认目标日是否交易，再预测；休市日不应输出开盘走势 | 非交易日仍预测开盘 |
| AccessingFullText | 公告、年报、分红方案、披露文件 | 核验报告期、披露日、实施日 | 把公告发布日期当报告期 |
| CodeInterpreter | 日期/星期推导、节假日表计算、批量时间窗口核验 | 用请求时间和时区计算，结果用于复核 | 没有市场日历时只用 weekday 替代交易日 |
| SearchImage | 截图/图表题中识别界面时间、红框日期 | 用于辅助识别图片中的日期/as-of | 只看图表趋势，不看截图时间 |

## 详细工具文件

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [search.md](search.md) | Search 搜索工具用法规则 | 节假日、交易所公告、休市、最新新闻、公告披露 |
| [finquery.md](finquery.md) | FinQuery 金融查询工具用法规则 | 行情、涨跌幅、财务数据、分红、证券基础信息 |
| [backtest.md](backtest.md) | BackTest 回测工具用法规则 | 前 N 个交易日、历史区间、交易日窗口 |
| [forecast.md](forecast.md) | Forecast 预测工具用法规则 | 未来走势、开盘走势、下一个交易日预测 |
| [accessingfulltext.md](accessingfulltext.md) | AccessingFullText 全文读取规则 | 公告、年报、分红方案、披露文件 |
| [codeinterpreter.md](codeinterpreter.md) | CodeInterpreter 日期计算规则 | 日期/星期推导、时区换算、批量窗口核验 |
| [searchimage.md](searchimage.md) | SearchImage 截图识别规则 | 截图/图表中的日期、红框和 as-of |
| [customerservicefaq.md](customerservicefaq.md) | CustomerServiceFAQ 非主工具边界 | 产品规则或平台说明问题 |
| [saveuserprofile.md](saveuserprofile.md) | SaveUserProfile 非主工具边界 | 用户明确表达时区或市场偏好 |

## 评分锚点

- 5 分：选择合适工具，输入日期/市场/报告期正确，输出日期被正确带入最终答案。
- 4 分：工具选择和主要输入正确，存在次要字段遗漏但不影响结论。
- 3 分：工具方向对，但没有充分核验市场日历或 as-of。
- 2 分：工具调用不足或输入有明显瑕疵，导致答案时间边界含混。
- 1 分：应查却不查，或查错市场/日期/报告期。
- 0 分：工具证据与答案相反，仍输出错误结论；或编造工具不可支持的时间事实。
