# L1: intent

系统没有正确理解用户要什么。

| L2 | 说明 | 常见受影响维度 |
|---|---|---|
| `intent_misjudged` | 把资讯评价题当成普通知识问答，或把市场异动题当成行情复盘 | `intent_fulfillment`, `core_signal_extraction` |
| `implicit_investment_need_omitted` | 遗漏"影响、受益标的、怎么判断、是否可持续"等隐含诉求 | `intent_fulfillment`, `investment_mapping` |
| `sub_question_omitted` | 漏答用户明确问的子问题，如期限/利率/是否推迟/对应标的 | `intent_fulfillment` |
| `comparison_task_not_recognized` | 没识别横向比较或主导判断要求 | `information_integration`, `core_signal_extraction` |

