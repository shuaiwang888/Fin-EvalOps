# 参考文件索引

本文件是金融资讯知识问答自研 vs 竞品最终回答比较评测协议的导航地图。

- **绝对评分层**：rubric 与 golden cases 提供最终回答质量评估标准。
- **compare 专属层**：comparison protocol 定义同题 pairwise 比较规则。
- **输出层**：output schema 定义 Round 1 与最终 JSON 结构。

## compare 专属参考

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [comparison_protocol.md](comparison_protocol.md) | 定义 result-only pairwise 比较流程、先绝对后相对、自研优劣/竞品优点/shared failures 判定规则 | 逐维比较前必读 |

## 评分细则（rubric/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](rubric/_index.md) | 维度列表、动态权重、封顶标签总览 | 分析题目前通读 |
| [raw-score-scale.md](rubric/raw-score-scale.md) | 六档原始分量表 | 评分前必读 |
| [intent_fulfillment.md](rubric/intent_fulfillment.md) | 意图满足度 | 判断适用性 + 评分 |
| [timeliness_fact_boundary.md](rubric/timeliness_fact_boundary.md) | 时效性与事实边界 | 判断适用性 + 评分 |
| [fact_evidence_quality.md](rubric/fact_evidence_quality.md) | 事实证据质量 | 判断适用性 + 评分 |
| [information_integration.md](rubric/information_integration.md) | 资讯整合与比较 | 判断适用性 + 评分 |
| [investment_mapping.md](rubric/investment_mapping.md) | 投资映射与落地 | 判断适用性 + 评分 |
| [core_signal_extraction.md](rubric/core_signal_extraction.md) | 核心信号提炼 | 判断适用性 + 评分 |
| [nonstandard_source_awareness.md](rubric/nonstandard_source_awareness.md) | 非标准资讯意识 | 判断适用性 + 评分 |
| [credibility_expression.md](rubric/credibility_expression.md) | 可信表达 | 判断适用性 + 评分 |
| [cap_hard_time_or_fact_error.md](rubric/cap_hard_time_or_fact_error.md) | 封顶标签：硬性时间或事实错误 | 绝对评分时 |
| [cap_stale_or_wrong_evidence.md](rubric/cap_stale_or_wrong_evidence.md) | 封顶标签：证据过时或来源类型错误 | 绝对评分时 |
| [cap_template_answer_without_signal.md](rubric/cap_template_answer_without_signal.md) | 封顶标签：模板化回答未抓核心信号 | 绝对评分时 |
| [cap_data_dump_without_judgment.md](rubric/cap_data_dump_without_judgment.md) | 封顶标签：数据堆砌无判断 | 绝对评分时 |
| [cap_unverified_rumor_as_fact.md](rubric/cap_unverified_rumor_as_fact.md) | 封顶标签：传闻当事实 | 绝对评分时 |

## 专家案例基准（golden_cases/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](golden_cases/_index.md) | 专家案例 hard checks 和最终回答失败模式 | 分析题目时读取，用于命中检测 |
| [image_annotation_anchors.md](golden_cases/image_annotation_anchors.md) | 市场小段子、调研纪要、大 V/官媒截图等图片类补充锚点 | 分析题目时按需读取 |

## 输出契约

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [output-schema_round1_zh.md](output-schema_round1_zh.md) | Round 1：同题校验、最终回答锚点、共享权重、双方最终回答证据摘要 | 建立共享评测框架时 |
| [output-schema_zh.md](output-schema_zh.md) | Pairwise JSON 输出契约、双边证据对象和比较结论格式 | 序列化时 |

## 关键依赖

- 题目分析依赖 `rubric/_index.md`、各维度文件的适用性判断、`golden_cases/_index.md` 和 `golden_cases/image_annotation_anchors.md`。
- 绝对评分依赖活跃维度文件、`rubric/raw-score-scale.md` 与相关 `cap_*.md` 文件。
- 逐维比较依赖 `comparison_protocol.md`。
- 所有证据只能来自用户问题、自研最终回答或竞品最终回答。

## 协议步骤到文件的映射

| 协议步骤 | 操作 | 读取文件 |
|---|---|---|
| 步骤 0：校验同题 | 同题校验 + 最终回答锚点确认 | `output-schema_round1_zh.md` |
| 步骤 1：建立共享框架 | 适用性判断 + 动态权重 + 案例命中 | `rubric/_index.md` + 各维度文件 + `golden_cases/_index.md` + `golden_cases/image_annotation_anchors.md` |
| 步骤 2：绝对评分 | 对自研和竞品最终回答逐维评分 + 封顶标签检查 | `rubric/_index.md` + 各维度文件 + `rubric/raw-score-scale.md` + 对应 `rubric/cap_*.md` 文件 |
| 步骤 3：逐维比较 | 先绝对后相对，输出自研优势/弱点、竞品优点、shared failures | `comparison_protocol.md` |
| 步骤 4：序列化输出 | 双边绝对评分 + 逐维比较 + 自然语言摘要 | `output-schema_zh.md` |
