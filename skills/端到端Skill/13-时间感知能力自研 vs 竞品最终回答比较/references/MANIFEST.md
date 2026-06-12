# 参考文件索引

本文件是时间感知能力自研 vs 竞品最终回答比较评测协议的导航地图。该版本只评估双方最终回答质量，不读取或归因过程字段。

## compare 专属参考

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [comparison_protocol.md](comparison_protocol.md) | 定义 result-only pairwise 比较流程、先绝对后相对、我方优劣/竞品优点/shared failures 判定规则 | 逐维比较前必读 |

## 评分细则（rubric/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](rubric/_index.md) | 维度列表 + 动态权重分配规则 + 封顶规则注意事项 | 建立共享评估框架前通读 |
| [raw-score-scale.md](rubric/raw-score-scale.md) | 六档原始分量表 | 评分前必读 |
| [temporal_intent_recognition.md](rubric/temporal_intent_recognition.md) | 时间意图识别维度 | 判断适用性 + 评分 |
| [anchor_date_resolution.md](rubric/anchor_date_resolution.md) | 锚定日期解析维度 | 判断适用性 + 评分 |
| [market_calendar_status.md](rubric/market_calendar_status.md) | 市场交易日历状态维度 | 判断适用性 + 评分 |
| [data_asof_freshness.md](rubric/data_asof_freshness.md) | 数据时点与新鲜度维度 | 判断适用性 + 评分 |
| [period_disclosure_mapping.md](rubric/period_disclosure_mapping.md) | 报告期与披露期映射维度 | 判断适用性 + 评分 |
| [premise_correction_clarification.md](rubric/premise_correction_clarification.md) | 时间前提纠错与澄清维度 | 判断适用性 + 评分 |
| [answer_composition_credibility.md](rubric/answer_composition_credibility.md) | 答案组织与可信边界维度 | 判断适用性 + 评分 |
| [cap_hard_wrong_anchor_date.md](rubric/cap_hard_wrong_anchor_date.md) | 封顶标签：核心日期锚点错误 | 封顶检查时 |
| [cap_market_closed_answered_as_open.md](rubric/cap_market_closed_answered_as_open.md) | 封顶标签：休市日按开盘回答 | 封顶检查时 |
| [cap_stale_data_masquerading_as_today.md](rubric/cap_stale_data_masquerading_as_today.md) | 封顶标签：旧数据冒充今天/最新 | 封顶检查时 |
| [cap_missing_required_premise_correction.md](rubric/cap_missing_required_premise_correction.md) | 封顶标签：缺失必要前提纠错 | 封顶检查时 |
| [cap_fiscal_period_disclosure_error.md](rubric/cap_fiscal_period_disclosure_error.md) | 封顶标签：财报/分红/报告期映射错误 | 封顶检查时 |
| [cap_fabricated_time_fact.md](rubric/cap_fabricated_time_fact.md) | 封顶标签：编造时间事实 | 封顶检查时 |

## 专家案例基准（golden_cases/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](golden_cases/_index.md) | docx 正文沉淀的时间感知 hard checks 和跨案例锚点 | 案例命中检测 |
| [image_annotation_anchors.md](golden_cases/image_annotation_anchors.md) | docx 图片截图中的补充专家知识：休市、旧数据、财报披露期、去年/年中映射 | 与 `_index.md` 一并读取 |

## 输出契约

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [output-schema_round1_zh.md](output-schema_round1_zh.md) | Round 1：同题校验、共享时间锚点、共享权重、两边最终回答证据摘要 | 建立共享框架后 |
| [output-schema_zh.md](output-schema_zh.md) | Pairwise JSON 输出契约、双边证据对象和比较结论格式 | 序列化时 |

## 协议步骤到文件的映射

| 协议步骤 | 操作 | 读取文件 |
|---|---|---|
| 步骤 0：校验同题 | 核对 `case_id`、用户问题和最终回答锚点 | `output-schema_round1_zh.md` |
| 步骤 1：建立共享时间框架 | 时间锚点抽取 + 适用性判断 + 动态权重 + 案例命中 | `rubric/_index.md` + 各维度文件 `## 适用性判断` + `golden_cases/_index.md` + `golden_cases/image_annotation_anchors.md` |
| 步骤 2：分别做绝对评分 | 逐维度评分（仅活跃维度）+ 封顶检查 | `rubric/_index.md` + 各维度文件 + `rubric/raw-score-scale.md` + 对应 `rubric/cap_*.md` 文件 |
| 步骤 3：逐维比较 | 先绝对后相对，输出我方优势/弱点、竞品优点、shared failures | `comparison_protocol.md` |
| 步骤 4：序列化输出 | 双边绝对评分 + 逐维比较 + 自然语言 | `output-schema_zh.md` |
