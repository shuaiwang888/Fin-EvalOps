# `reasoning` — 推导投资逻辑

当信息可能存在，但模型没有形成专业投资逻辑、因果链或题型匹配的判断时使用。

| L2 | 说明 | 典型受影响维度 |
|---|---|---|
| `no-investment-thesis` | 没有提炼核心投资论点，只是资料拼接或指标罗列 | investment_logic_depth |
| `broken-causal-chain` | 缺少事实/事件 -> 传导机制 -> 公司/资产含义 -> 投资判断的闭环 | investment_logic_depth |
| `method-mismatch` | 分析方法与题型、标的属性或投资周期错位 | method_fit |
| `no-theme-fermentation-logic` | 题材股没有讲题材级别、发酵时间、持续性、空间和核心/边缘地位 | method_fit, investment_logic_depth |
| `no-business-model-valuation-logic` | 价值股没有讲商业模式、盈利逻辑、估值和风险 | investment_logic_depth, method_fit |
| `no-comparison-criterion` | 对比、切换、排序类问题没有比较标准或优先级逻辑 | comparison_quantification |
| `macro-variable-selection-weak` | 宏观/指数问题没有抓住关键变量，停留在新闻解读 | investment_logic_depth, method_fit |
| `stock-style-logic-missed` | 未识别标的是题材、游资、机构、价值、周期、避险等哪类逻辑，导致分析主轴错误 | method_fit, investment_logic_depth |
| `fund-flow-cause-unexplained` | 只描述资金流入/流出，没有解释资金为什么选择或放弃该标的 | investment_logic_depth |
| `unsuitable-personalization` | 推荐没有根据用户画像、风险目标、持仓处境和产品波动特征调整，导致适配性不足 | user_profile_suitability, actionability_risk |
| `risk-state-mishandled` | 对浮亏、套牢、迷茫、急于回本等风险状态处理错误，仍推动短线、追涨、加仓或高波动集中配置 | scenario_emotion_recognition, actionability_risk |

证据优先看 `text_answer`，再看 `chain.plan` 是否同样缺失。
