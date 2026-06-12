# 参考文件索引

本文件是自研 vs 竞品最终回答比较评测协议的导航地图。

- **绝对评分层**：rubric 与 golden cases 提供单模型最终回答质量标准。
- **compare 专属层**：comparison protocol 负责定义同题比较、我方优劣/竞品优点/shared failures 判定规则。

## compare 专属参考

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [comparison_protocol.md](comparison_protocol.md) | 定义 pairwise 比较流程、先绝对后相对、我方优劣/竞品优点/shared failures 判定规则 | 步骤 4 比较前必读 |

## 评分细则（rubric/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](rubric/_index.md) | 维度列表 + 动态权重分配规则 + 封顶规则注意事项 | 步骤 1 分析题目前通读 |
| [raw-score-scale.md](rubric/raw-score-scale.md) | 六档原始分量表 | 评分前必读 |
| [financial_logic_chain.md](rubric/financial_logic_chain.md) | 金融逻辑链维度 | 步骤 1 判断适用性 + 步骤 2 评分 |
| [market_driver_identification.md](rubric/market_driver_identification.md) | 市场驱动识别维度 | 步骤 1 判断适用性 + 步骤 2 评分 |
| [evidence_to_conclusion.md](rubric/evidence_to_conclusion.md) | 证据到结论维度 | 步骤 1 判断适用性 + 步骤 2 评分 |
| [comparison_and_ranking.md](rubric/comparison_and_ranking.md) | 比较与排序维度 | 步骤 1 判断适用性 + 步骤 2 评分 |
| [scenario_risk_reasoning.md](rubric/scenario_risk_reasoning.md) | 情景与风险推理维度 | 步骤 1 判断适用性 + 步骤 2 评分 |
| [decision_value_expression.md](rubric/decision_value_expression.md) | 决策价值表达维度 | 步骤 1 判断适用性 + 步骤 2 评分 |
| [cap_unsupported_prediction_or_recommendation.md](rubric/cap_unsupported_prediction_or_recommendation.md) | 封顶规则：无支撑预测或推荐 | 封顶检查时 |
| [cap_evidence_conclusion_disconnect.md](rubric/cap_evidence_conclusion_disconnect.md) | 封顶规则：结论与证据脱节 | 封顶检查时 |
| [cap_missing_key_market_driver.md](rubric/cap_missing_key_market_driver.md) | 封顶规则：关键市场驱动缺失 | 封顶检查时 |
| [cap_overconfident_risk_commitment.md](rubric/cap_overconfident_risk_commitment.md) | 封顶规则：收益/风险承诺过度 | 封顶检查时 |
| [cap_comparison_logic_error.md](rubric/cap_comparison_logic_error.md) | 封顶规则：比较或排序逻辑错误 | 封顶检查时 |
| [cap_data_dump_without_reasoning.md](rubric/cap_data_dump_without_reasoning.md) | 封顶规则：数据堆砌替代推理 | 封顶检查时 |

## 专家案例基准（golden_cases/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](golden_cases/_index.md) | 第 12 类当前未内置具体专家案例；用于记录外部命中案例的读取规则 | 步骤 1 分析题目时读取 |
| [image_annotation_anchors.md](golden_cases/image_annotation_anchors.md) | 图片批注锚点读取规则 | 步骤 1 与 `_index.md` 一并读取 |

## 输出契约

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [output-schema_round1_zh.md](output-schema_round1_zh.md) | Round 1：同题校验、共享权重、两边最终回答证据摘要 | 步骤 1 后 |
| [output-schema_zh.md](output-schema_zh.md) | Pairwise JSON 输出契约、双边证据对象和比较结论格式 | 步骤 6 序列化时 |

## 协议步骤到文件的映射

| 协议步骤 | 操作 | 读取文件 |
|---|---|---|
| 步骤 1：分析题目 | 决策任务识别 + 适用性判断 + 动态权重 + 案例命中 | `rubric/_index.md` + 各维度文件 `## 适用性判断` + `golden_cases/_index.md` + `golden_cases/image_annotation_anchors.md` |
| 步骤 2：分别做绝对评分 | 逐维度评分（仅活跃维度）+ 封顶检查 | `rubric/_index.md` + 各维度文件 + `rubric/raw-score-scale.md` + 对应 `rubric/cap_*.md` 文件 |
| 步骤 4：逐维比较 | 先绝对后相对，输出我方优势/弱点、竞品优点、shared failures | `comparison_protocol.md` |
| 步骤 6：序列化输出 | 双边绝对评分 + 逐维比较 + 自然语言 | `output-schema_zh.md` |
