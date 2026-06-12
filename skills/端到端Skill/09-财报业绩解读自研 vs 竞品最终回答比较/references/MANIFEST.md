# 参考文件索引

本目录只导航 result-only 最终回答比较评估需要的文件。评分、证据、优缺点和最终结论只能来自用户问题与双方最终回答。

## 主协议

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [../SKILL_zh.md](../SKILL_zh.md) | 定义 result-only 自研 vs 竞品最终回答比较协议 | 开始评测前必读 |
| [comparison_protocol.md](comparison_protocol.md) | 定义先绝对后相对、逐维比较、优势/缺点/共同失败点判定规则 | 逐维比较前必读 |

## 评分细则（rubric/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](rubric/_index.md) | 维度列表、动态权重分配、封顶标签规则、证据边界 | 步骤 1 分析题目前通读 |
| [raw-score-scale.md](rubric/raw-score-scale.md) | 0/20/40/60/80/100 分制与权重规则 | 评分前必读 |
| [intent_understanding.md](rubric/intent_understanding.md) | 意图理解与任务完成维度 | 判断适用性与评分 |
| [report_data_accuracy.md](rubric/report_data_accuracy.md) | 财报数据与口径准确性维度 | 判断适用性与评分 |
| [primary_evidence_quality.md](rubric/primary_evidence_quality.md) | 公告全文与证据质量维度 | 判断适用性与评分 |
| [causal_attribution_depth.md](rubric/causal_attribution_depth.md) | 归因深度维度 | 判断适用性与评分 |
| [business_financial_linkage.md](rubric/business_financial_linkage.md) | 业务财务联动维度 | 判断适用性与评分 |
| [forward_investment_judgment.md](rubric/forward_investment_judgment.md) | 前瞻与投资判断维度 | 判断适用性与评分 |
| [composition_credibility.md](rubric/composition_credibility.md) | 表达可信度维度 | 判断适用性与评分 |
| [cap_hard_fact_or_caliber_error.md](rubric/cap_hard_fact_or_caliber_error.md) | 封顶标签：硬性事实或口径错误 | 触发封顶标签时 |
| [cap_missing_primary_disclosure.md](rubric/cap_missing_primary_disclosure.md) | 封顶标签：遗漏关键原始披露 | 触发封顶标签时 |
| [cap_wrong_special_event_explanation.md](rubric/cap_wrong_special_event_explanation.md) | 封顶标签：特殊事件解释错误 | 触发封顶标签时 |
| [cap_surface_financial_formula_only.md](rubric/cap_surface_financial_formula_only.md) | 封顶标签：只做表层财务公式解释 | 触发封顶标签时 |
| [cap_unverifiable_or_hallucinated_numbers.md](rubric/cap_unverifiable_or_hallucinated_numbers.md) | 封顶标签：不可验证或幻觉数字 | 触发封顶标签时 |
| [cap_missing_required_conclusion.md](rubric/cap_missing_required_conclusion.md) | 封顶标签：缺少必要结论 | 触发封顶标签时 |

## 专家案例基准（golden_cases/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](golden_cases/_index.md) | 30 个专家案例 hard checks 与跨案例判分锚点 | 步骤 1 分析题目时读取 |

## 输出契约

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [output-schema_round1_zh.md](output-schema_round1_zh.md) | Round 1：同题校验、共享权重、双方最终回答证据摘要 | 步骤 1 后 |
| [output-schema_zh.md](output-schema_zh.md) | Pairwise JSON 输出契约、证据对象和比较结论格式 | 序列化时 |

## 协议步骤到文件的映射

| 协议步骤 | 操作 | 读取文件 |
|---|---|---|
| 步骤 0：校验同题 | case_id 与问题一致性校验 | `SKILL_zh.md` |
| 步骤 1：建立共享评估框架 | 维度适用性 + 动态权重 + 案例命中 | `rubric/_index.md` + 活跃维度文件 + `golden_cases/_index.md` |
| 步骤 2：分别做绝对评分 | 最终回答逐维评分 + 封顶标签检查 | 活跃维度文件 + `rubric/raw-score-scale.md` + 对应 `rubric/cap_*.md` 文件 |
| 步骤 3：逐维比较 | 输出自研优势/弱点、竞品优点、共同失败点 | `comparison_protocol.md` |
| 步骤 4：序列化输出 | 双边绝对评分 + 逐维比较 + 总结结论 | `output-schema_zh.md` |
