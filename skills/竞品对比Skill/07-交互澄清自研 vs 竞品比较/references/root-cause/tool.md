# L1：选择与执行工具

用于解释工具选择、参数或链路效率问题。

L2：
- `wrong_tool_selection`：选择了不能解决本题的工具。
- `wrong_tool_params`：股票、时间窗、指标、市场或查询条件参数错误。
- `missing_tool_call`：本应查规则、行情、公告或候选实体但未查。
- `inefficient_tool_chain`：调用冗余、重复或耗时明显偏高。
- `overreliance_on_nlu`：过度相信单次 NLU/FinQuery，未复核错别字或异常代码。

证据常来自 `chain[N].tools[M]` 和 `timing`。
