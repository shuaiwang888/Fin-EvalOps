# 封顶规则

| rule_id | 上限 | 触发条件 |
|---|---:|---|
| `hard_concept_or_rule_error` | 40 | 金融概念或交易规则硬错，如集合竞价成交时点、财报披露期、ST 状态、PE 负值处理 |
| `wrong_entity_or_product` | 45 | 把用户对象答成另一个实体或产品，如豪威集团/豪能股份、实物黄金/黄金 ETF、基金公司/旗下基金 |
| `missed_core_definition` | 55 | 用户问定义、含义、区别，却主要给行情、指数或数据表 |
| `metric_caliber_unexplained_or_invalid` | 60 | 使用自定义或失真指标但不解释口径，或指标筛选与投资常识相悖 |
| `stale_or_wrong_time_context` | 60 | 忽略近期、最新、盘中、报告期等时间要求 |
| `empty_generic_advice` | 65 | 答案是泛泛建议，缺少与该金融语义场景绑定的解释、案例或数据 |

若多条同时触发，取最低上限。封顶后仍需输出各维度 raw score 和根因。
