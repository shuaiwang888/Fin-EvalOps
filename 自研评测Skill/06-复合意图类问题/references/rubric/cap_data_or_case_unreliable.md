# 封顶规则：`data_or_case_unreliable`

## 触发条件

最终答案使用了明显无依据、失实或不可核验的数据/案例，并据此支撑关键结论，例如：
- 案例先例不存在或与题目不匹配
- 榜单、涨跌幅、资金净流入、龙虎榜、新闻时间等基础数据错漏
- 声称某数据来自市场或工具，但输入材料无法支持
- 失真数据进一步支撑热点、龙头、策略或共性结论

## 分数上限

`score_ceiling = 55`

## 不触发条件

- 小的非关键数据瑕疵，且不影响主结论。
- 答案明确标注为估算，并说明口径限制。
- 数据源本身可信，但计算方法或时间窗口有误（应由 `calculation_or_time_window_error` 覆盖）。

## 与 `calculation_or_time_window_error` 的边界

本规则聚焦"数据/案例本身失实或不可核验"，即源头问题；`calculation_or_time_window_error` 聚焦"数据源可信但计算口径或时间窗口有误"，即方法问题。若数据既失实又算错，按更严重者封顶，不叠加。

## 关联维度

- `data_logic_rigor`
- `multi_source_evidence_integration`
- `composition_readability`
