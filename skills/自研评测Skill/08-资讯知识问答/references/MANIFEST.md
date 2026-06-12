# 参考文件索引

本文件是 8_consultation-and-qa 自评 skill 的导航地图。评测时根据协议步骤按需读取子文件。

## 评分细则（rubric/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](rubric/_index.md) | 维度列表、动态权重、封顶规则总览 | 步骤 0 |
| [raw-score-scale.md](rubric/raw-score-scale.md) | 六档分制定义 | 步骤 1 前 |
| [intent_fulfillment.md](rubric/intent_fulfillment.md) | 意图满足度 | 步骤 0/1 |
| [timeliness_fact_boundary.md](rubric/timeliness_fact_boundary.md) | 时效性与事实边界 | 步骤 0/1 |
| [fact_evidence_quality.md](rubric/fact_evidence_quality.md) | 事实证据质量 | 步骤 0/1 |
| [information_integration.md](rubric/information_integration.md) | 资讯整合与比较 | 步骤 0/1 |
| [investment_mapping.md](rubric/investment_mapping.md) | 投资映射与落地 | 步骤 0/1 |
| [core_signal_extraction.md](rubric/core_signal_extraction.md) | 核心信号提炼 | 步骤 0/1 |
| [nonstandard_source_awareness.md](rubric/nonstandard_source_awareness.md) | 非标准资讯意识 | 步骤 0/1 |
| [credibility_expression.md](rubric/credibility_expression.md) | 可信表达 | 步骤 0/1 |
| [tool_usage.md](rubric/tool_usage.md) | 工具使用合理性 | 步骤 2 |
| [cap_hard_time_or_fact_error.md](rubric/cap_hard_time_or_fact_error.md) | 封顶：硬性时间或事实错误 | 步骤 3 |
| [cap_stale_or_wrong_evidence.md](rubric/cap_stale_or_wrong_evidence.md) | 封顶：证据过时或来源类型错误 | 步骤 3 |
| [cap_template_answer_without_signal.md](rubric/cap_template_answer_without_signal.md) | 封顶：模板化回答未抓核心信号 | 步骤 3 |
| [cap_data_dump_without_judgment.md](rubric/cap_data_dump_without_judgment.md) | 封顶：数据堆砌无判断 | 步骤 3 |
| [cap_unverified_rumor_as_fact.md](rubric/cap_unverified_rumor_as_fact.md) | 封顶：传闻当事实 | 步骤 3 |

## 专家案例基准（golden_cases/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](golden_cases/_index.md) | 21 个专家案例 hard checks 与跨案例锚点 | 步骤 0 |
| [image_annotation_anchors.md](golden_cases/image_annotation_anchors.md) | docx 图片中的市场小段子、调研纪要、大V/官媒截图补充锚点 | 步骤 0 |

## 根因归因（root-cause/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](root-cause/_index.md) | 根因选择规则、证据规则、置信度规则 | 步骤 2 |
| [intent.md](root-cause/intent.md) | L1: intent | 步骤 2 |
| [evidence.md](root-cause/evidence.md) | L1: evidence | 步骤 2 |
| [tool.md](root-cause/tool.md) | L1: tool | 步骤 2 |
| [reasoning.md](root-cause/reasoning.md) | L1: reasoning | 步骤 2 |
| [composition.md](root-cause/composition.md) | L1: composition | 步骤 2 |

## 工具列表（tool_list/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](tool_list/_index.md) | 工具和来源类型总览 | 步骤 2 |

## 输出契约

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [output-schema_zh.md](output-schema_zh.md) | 完整 JSON 输出 schema 与字段规则 | 步骤 4 |
| [output-schema_round1_zh.md](output-schema_round1_zh.md) | 轻量盲评输出格式 | Round 1 |


## 协议步骤到文件映射

| 协议步骤 | 操作 | 读取文件 |
|---|---|---|
| 步骤 0 | 题目分析、动态权重、案例命中 | `rubric/_index.md` + 相关维度文件 + `golden_cases/_index.md` + `golden_cases/image_annotation_anchors.md` |
| 步骤 1 | 逐维度评分 | `rubric/raw-score-scale.md` + 活跃维度文件 |
| 步骤 2 | 工具评分与根因归因 | `tool_list/_index.md` + `rubric/tool_usage.md` + `root-cause/_index.md` + 对应 L1 文件 |
| 步骤 3 | 封顶检查 | 相关 `rubric/cap_*.md` |
| 步骤 4 | 序列化输出 | `output-schema_zh.md` |

