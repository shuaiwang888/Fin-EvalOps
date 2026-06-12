# `intent` — 理解问题

当系统误解用户根本需求、投资场景或必备分析要素时使用。

| L2 | 说明 | 典型受影响维度 |
|---|---|---|
| `problem-type-misclassified` | 将题材股当普通诊股，将价值股当短线票，将基金问题当股票问题，或把分析题降级成事实查询 | intent_scenario_recognition, method_fit |
| `hidden-investment-need-missed` | 未识别用户实际需要买卖、持有、切换、避险、验证逻辑或判断空间 | intent_scenario_recognition, actionability_risk |
| `required-elements-missed` | 漏掉该题型必备要素，如基金回撤/夏普/同类排名，价值股商业模式/估值，消息面最新催化 | intent_scenario_recognition, comparison_quantification |
| `context-carryover-missed` | 没有承接上下文中的标的、筛选结果、时间范围、用户偏好或上一轮约束 | intent_scenario_recognition |
| `user-profile-need-missed` | 用户要求适合我、结合目标风险、持仓成本或资金规模，但系统没有识别个人化适配需求 | intent_scenario_recognition, user_profile_suitability |
| `emotional-loss-context-missed` | 用户表达亏损、套牢、迷茫或买什么都亏，但系统误判为普通荐股或普通市场分析 | intent_scenario_recognition, scenario_emotion_recognition |

证据优先看 `question`、`context`、`chain.plan` 和 `text_answer`。
