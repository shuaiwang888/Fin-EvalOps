# `evidence` — 检索信息

当工具选择基本正确，但找到的信息错误、过时、不关键、来源过浅或没有被正确利用时使用。

| L2 | 说明 | 典型受影响维度 |
|---|---|---|
| `missing-key-catalyst` | 漏掉真正驱动行情或题材的关键政策、公告、价格变化、订单、业绩或事件 | evidence_source_quality, investment_logic_depth |
| `stale-key-evidence` | 使用旧消息、旧材料或过期背景解释当前股价和消息面 | recency_time_boundary, evidence_source_quality |
| `time-scope-mismatch` | 混入时间窗口外信息，报告期、交易日、年份或截止日期错误 | recency_time_boundary |
| `wrong-evidence-type` | 用研报冒充新闻、用行业科普替代公告/调研、用泛概念材料替代个股证据 | evidence_source_quality |
| `source-depth-insufficient` | 题目需要调研纪要、研报全文、iFind 类数据库或公司披露，但只用了浅层公开搜索 | evidence_source_quality, tool_usage |
| `missing-critical-metrics` | 漏掉基金、估值、财务、排名、回撤、分位等本题关键指标 | comparison_quantification |
| `evidence-output-misread` | 工具输出里有关键字段，但模型误读、漏读或解释错误 | evidence_source_quality, composition_credibility |
| `missing-deep-source` | 客户占比、供应链份额、调研纪要、隐含资产、订单细节等深层资料缺失 | evidence_source_quality, tool_usage |
| `materiality-misjudged` | 找到了信息但没有区分是否真正影响价格、基本面或用户决策 | evidence_source_quality, investment_logic_depth |
| `missing-user-profile-evidence` | 推荐需要画像、持仓、成本、风险目标或历史偏好支撑，但答案没有使用这些证据 | user_profile_suitability, evidence_source_quality |

证据优先看 `chain.tools[M].output`、`text_answer` 和最终答案引用的材料。
