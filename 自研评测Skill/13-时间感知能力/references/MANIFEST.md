# 参考文件索引

本文件是时间感知评测 skill 的导航地图。根据评测协议步骤按需读取子文件。

## 评分细则（rubric/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](rubric/_index.md) | 维度列表、适用性、动态权重、封顶规则索引 | 步骤 0 分析题目前通读；步骤 1/3 回查 |
| [raw-score-scale.md](rubric/raw-score-scale.md) | 六档分制定义（0/20/40/60/80/100） | 评分前读取 |
| [temporal_intent_recognition.md](rubric/temporal_intent_recognition.md) | 时间意图识别维度评分细则 | 步骤 1 |
| [anchor_date_resolution.md](rubric/anchor_date_resolution.md) | 锚点日期解析维度评分细则 | 步骤 1 |
| [market_calendar_status.md](rubric/market_calendar_status.md) | 交易日历状态维度评分细则 | 步骤 1 |
| [data_asof_freshness.md](rubric/data_asof_freshness.md) | 数据时点新鲜度维度评分细则 | 步骤 1 |
| [period_disclosure_mapping.md](rubric/period_disclosure_mapping.md) | 财报期间映射维度评分细则 | 步骤 1 |
| [premise_correction_clarification.md](rubric/premise_correction_clarification.md) | 前提纠错与澄清维度评分细则 | 步骤 1 |
| [answer_composition_credibility.md](rubric/answer_composition_credibility.md) | 答案可信表达维度评分细则 | 步骤 1 |
| [tool_usage.md](rubric/tool_usage.md) | 工具使用合理性维度评分细则 | 步骤 2 |
| [cap_hard_wrong_anchor_date.md](rubric/cap_hard_wrong_anchor_date.md) | 硬性锚点日期错误封顶规则 | 步骤 3 |
| [cap_market_closed_answered_as_open.md](rubric/cap_market_closed_answered_as_open.md) | 休市按交易作答封顶规则 | 步骤 3 |
| [cap_stale_data_masquerading_as_today.md](rubric/cap_stale_data_masquerading_as_today.md) | 旧数据冒充当前封顶规则 | 步骤 3 |
| [cap_missing_required_premise_correction.md](rubric/cap_missing_required_premise_correction.md) | 缺失必要前提纠错封顶规则 | 步骤 3 |
| [cap_fiscal_period_disclosure_error.md](rubric/cap_fiscal_period_disclosure_error.md) | 财报期间披露错误封顶规则 | 步骤 3 |
| [cap_fabricated_time_fact.md](rubric/cap_fabricated_time_fact.md) | 编造时间事实封顶规则 | 步骤 3 |

## 专家案例基准（golden_cases/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](golden_cases/_index.md) | docx 正文沉淀的 3 个时间感知 hard checks 和跨案例锚点 | 步骤 0 命中检测 |
| [image_annotation_anchors.md](golden_cases/image_annotation_anchors.md) | docx 图片截图中的补充专家知识：休市、旧数据、财报披露期、去年/年中映射 | 步骤 0 与 `_index.md` 一并读取 |

## 根因归因体系（root-cause/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](root-cause/_index.md) | L1/L2 根因总览、证据规则、置信度规则和选择规则 | 步骤 2 诊断前通读 |
| [intent.md](root-cause/intent.md) | 理解问题：时间意图和锚点识别根因 | 按需 |
| [evidence.md](root-cause/evidence.md) | 检索数据：时间数据核验根因 | 按需 |
| [tool.md](root-cause/tool.md) | 选择与执行工具：时间核验工具使用根因 | 按需 |
| [reasoning.md](root-cause/reasoning.md) | 时间逻辑推理：日期、星期、报告期推理根因 | 按需 |
| [composition.md](root-cause/composition.md) | 组织答案：时间口径表达根因 | 按需 |

## 工具列表（tool_list/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](tool_list/_index.md) | 时间感知题常见工具用途和错误模式 | 步骤 2 评分 `tool_usage` 前读取 |

## 输出契约

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [output-schema_zh.md](output-schema_zh.md) | JSON 优先输出契约和证据对象格式 | 步骤 4 序列化时 |
| [output-schema_round1_zh.md](output-schema_round1_zh.md) | Round 1 分析输出格式 | 步骤 0-1 |

## 协议步骤到文件映射

| 协议步骤 | 操作 | 读取文件 |
|---|---|---|
| 步骤 0：分析题目 | 抽取时间锚点、适用性判断、动态权重、案例命中 | `rubric/_index.md` + `golden_cases/_index.md` + `golden_cases/image_annotation_anchors.md` |
| 步骤 1：盲评最终答案 | 逐维度评分 | `rubric/_index.md` + 对应维度 `.md` + `rubric/raw-score-scale.md` |
| 步骤 2：链路诊断 | 工具评分、根因选择 | `tool_list/_index.md` + `root-cause/_index.md` + 按需 L1 文件 |
| 步骤 3：应用封顶 | 检查硬性时间错误、旧数据冒充、错误年份、缺失纠错 | `rubric/_index.md` 的封顶规则 + 对应 cap `.md` |
| 步骤 4：序列化输出 | JSON + 简短自然语言评审 | `output-schema_zh.md` |
