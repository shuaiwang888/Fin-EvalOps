# Round 1 输出规范

Round 1 用于建立共享评测框架并形成 pairwise 比较前的分析底稿。输出为**自然语言分析报告**，不是 JSON。报告末尾必须附 `<<ANALYSIS_END>>`。

## 必须包含的小节

### 1. 配对与同题校验

说明：
- `case_id`
- 竞品模型名称
- 自研与竞品是否为同一用户问题
- 若问题不一致，说明不得继续输出胜负结论

### 2. 用户问题类型

判断属于以下哪一类或混合型：
- 标准量化条件选股
- 复杂交易形态筛选
- 带定性约束的推理选股
- 结构化条件与非标信息混合筛选
- 跨领域或分层筛选

### 3. 条件清单

从用户问题中抽取并分组列出：
- 显性筛选条件
- 隐性金融语义和业务口径
- 否定条件、排除条件、范围条件
- 先后关系、分层筛选关系、交集/并集关系
- 排序、Top N、选一只、输出字段或格式要求
- 不可用、停更、低频或需要用户确认的数据边界

### 4. 工具需求

说明哪些条件应使用：
- FinQuery
- Search
- BackTest
- CodeInterpreter
- AccessingFullText
- SearchImage
- 其他可用工具

同时说明哪些条件需要公告/研报/新闻/互动易/合作关系等非标信源，哪些应使用结构化行情、财务、资金或技术指标数据。

### 5. 专家案例命中

列出命中的 `standard_caseXX` / `reasoning_caseXX` / 图片批注锚点，以及本题实际使用的 hard checks。未命中时写明“未命中具体专家案例，使用跨案例判分锚点”。

### 6. 共享权重表

列出以下 8 个维度的适用性和动态权重，权重总和必须为 100。同一题下自研与竞品必须共用这一套权重。

| 维度 | 适用性 | 权重 | 理由 |
|---|---|---:|---|
| intent_condition_extraction | relevant | 18 | 示例 |
| financial_semantics_and_caliber | relevant | 14 | 示例 |
| screening_plan_decomposition | relevant | 14 | 示例 |
| tool_usage | relevant | 12 | 示例 |
| result_correctness_and_coverage | relevant | 16 | 示例 |
| ranking_and_decision_actionability | relevant | 10 | 示例 |
| data_logic_time_boundary | relevant | 10 | 示例 |
| composition_credibility | supplementary | 6 | 示例 |

适用性只能是：
- `relevant`
- `supplementary`
- `not_applicable`

### 7. 双方绝对评分预判

分别概述自研和竞品的关键证据信号：
- 最终答案是否保留核心条件
- 金融口径和时间边界是否正确
- 候选池、排序、字段和无结果解释是否可用
- 表格、图表或可视化呈现是否真正有决策价值
- 链路是否使用了正确工具并把工具结果转化为答案质量

本节可以写 raw_score 预判，但不要输出最终 JSON。

### 8. 封顶候选

列出可能触发的 cap rule id，并分别标注自研/竞品/双方：
- `core_condition_omitted_or_rewritten`
- `hard_financial_semantics_or_caliber_error`
- `unsupported_data_forced_output`
- `wrong_tool_strategy`
- `layered_or_temporal_screening_failure`
- `missing_required_ranking_or_fields`
- `unverifiable_result_or_data_hallucination`
- `chart_or_table_without_decision_value`

如果未观察到致命缺陷，写明“未观察到致命缺陷”。

### 9. Pairwise 比较焦点

列出 Round 2 需要重点比较的差异：
- 自研可能领先的维度
- 自研可能落后的维度
- 竞品可能值得学习的做法
- 双方共同失败点
- 需要用链路解释的关键差异

## 禁止事项

- 不要输出最终结构化 JSON。
- 不要给双方使用不同权重。
- 不要因为一方更差就抬高另一方的绝对评分。
- 不要把链路长度、表格长度或表达流畅度直接等同于高质量。
- 不要在同题校验失败时输出胜负结论。

最后一行必须为：

`<<ANALYSIS_END>>`
