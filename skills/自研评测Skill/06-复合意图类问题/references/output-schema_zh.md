# 输出格式规范

先输出结构化 JSON。在调用方需要可读摘要时，JSON 后附简短的自然语言评审。

## JSON 结构

```json
{
  "schema_version": "compound-intent/v1",
  "weight_assignment": {
    "intent_decomposition": {"dynamic_weight": 16, "applicability": "relevant", "rationale": "用户一句话包含多个明确子任务，需要先拆解"},
    "task_coverage_priority": {"dynamic_weight": 14, "applicability": "relevant", "rationale": "需要覆盖所有关键子任务并按主次组织"},
    "multi_source_evidence_integration": {"dynamic_weight": 14, "applicability": "relevant", "rationale": "问题需要整合新闻、行情、公告和产业证据"},
    "analysis_chain_closure": {"dynamic_weight": 16, "applicability": "relevant", "rationale": "需要形成事实、影响、传导、策略闭环"},
    "data_logic_rigor": {"dynamic_weight": 14, "applicability": "relevant", "rationale": "涉及时间窗口、数据口径和量化判断"},
    "decision_actionability": {"dynamic_weight": 10, "applicability": "relevant", "rationale": "用户要求投资结论和操作框架"},
    "composition_readability": {"dynamic_weight": 5, "applicability": "supplementary", "rationale": "复杂问题需要清晰结构降低理解成本"},
    "tool_usage": {"dynamic_weight": 7, "applicability": "relevant", "rationale": "链路需要核验工具是否支撑多子任务证据需求"},
    "latency_efficiency": {"dynamic_weight": 4, "applicability": "supplementary", "rationale": "有耗时证据时评估复杂问句的响应效率"}
  },
  "skipped_dimensions": [],
  "matched_golden_cases": [
    {
      "case_id": "case04_market_news_smic_impact",
      "matched_reason": "用户要求多个时间窗口新闻梳理并评估对单一公司的影响",
      "hard_checks_used": ["覆盖48小时市场热点", "覆盖7天中芯国际相关信息", "按短中长期评估影响", "image_anchor: 无依据资金数据会拖垮影响评估"]
    }
  ],
  "dimension_scores": {
    "intent_decomposition": {"raw_score": 0, "evidence": []},
    "task_coverage_priority": {"raw_score": 0, "evidence": []},
    "multi_source_evidence_integration": {"raw_score": 0, "evidence": []},
    "analysis_chain_closure": {"raw_score": 0, "evidence": []},
    "data_logic_rigor": {"raw_score": 0, "evidence": []},
    "decision_actionability": {"raw_score": 0, "evidence": []},
    "composition_readability": {"raw_score": 0, "evidence": []},
    "tool_usage": {"raw_score": 0, "evidence": []},
    "latency_efficiency": {"raw_score": 0, "evidence": []}
  },
  "caps": [
    {
      "rule_id": "missed_major_subtask",
      "triggered": true,
      "score_ceiling": 65,
      "reason": "用户明确要求案例先例，但最终答案没有真正展开举例。",
      "evidence": []
    }
  ],
  "root_causes": [
    {
      "l1": "coverage",
      "l2": "major-subtask-missing",
      "dimension": "task_coverage_priority",
      "raw_score": 60,
      "confidence": "high",
      "summary": "答案覆盖了年报解读和大跌原因，但漏掉用户要求的可核验历史先例，导致复合任务未完整闭环。",
      "evidence": []
    }
  ],
  "narrative_review": {
    "summary": "",
    "strengths": [],
    "weaknesses": [],
    "next_actions": []
  }
}
```

> **注意**：`weighted_points`、`absolute_score_pre_cap`、`final_score` 由调用方代码自动计算，你不需要输出这些字段。你只需输出每个维度的 `raw_score`（六档：0/20/40/60/80/100）和 `evidence`。

## 证据对象格式

使用紧凑的证据条目：

```json
{
  "source": "question | final_answer | context | reasoning | function_call | function_call_output | latency | screenshot_ocr | expert_annotation | online_signal",
  "pointer": "question | text_answer | context[0].answer | chain[0].plan | chain[0].tools[0] | chain[0].tools[0].output | latency.total_seconds | screenshots[N].ocr | annotations[N] | online_dimension_signals[N]",
  "summary": "简短的证据摘要"
}
```

指针格式对应输入数据结构：

| source | pointer 格式 | 指向 |
|---|---|---|
| `question` | `question` | 用户当前问题 |
| `final_answer` | `text_answer` | 最终答案的纯文本版本 |
| `context` | `context[N].question` / `context[N].answer` | 对话中第 N 轮历史问题或答案 |
| `reasoning` | `chain[N].plan` | 第 N 步的规划/推理文本 |
| `function_call` | `chain[N].tools[M]` | 第 N 步第 M 次工具调用（含 name + input） |
| `function_call_output` | `chain[N].tools[M].output` | 第 N 步第 M 次工具调用的输出 |
| `latency` | `latency.total_seconds` / `chain[N].duration_ms` | 总耗时或链路耗时证据 |
| `screenshot_ocr` | `screenshots[N].ocr` / `context[N].screenshot_ocr` | 原始截图 OCR 文本 |
| `expert_annotation` | `annotations[N]` / `context[N].annotation` | 人工专家批注、红字标注或胜负结论 |
| `online_signal` | `online_dimension_signals[N]` | 线上维度统计、失败样本摘要或用户反馈 |

评分时以 `text_answer` 为主锚点。仅 `tool_usage` 和 `latency_efficiency` 可使用链路或耗时证据直接评分。

除非调用方明确要求，不要输出长引文。

## 字段规则

- `schema_version`：固定为 `compound-intent/v1`。
- `weight_assignment`：每个维度的动态权重分配结果。包含 `dynamic_weight`、`applicability`、`rationale`。所有 `dynamic_weight` 之和必须 = 100。
- `skipped_dimensions`：`not_applicable` 维度名称列表。这些维度不出现在 `dimension_scores` 中。
- `matched_golden_cases`：记录命中的专家案例和实际使用的 hard checks；未命中时允许为空数组。若使用了截图锚点，可在 `hard_checks_used` 中用 `image_anchor: ...` 简写记录。
- `dimension_scores`：仅包含 `relevant` 和 `supplementary` 维度，不含 `skipped_dimensions` 中的维度。每个维度只需输出 `raw_score` 和 `evidence`。
- `caps`：包含所有考虑过的封顶规则（仅与活跃维度相关的），或至少包含所有触发的封顶规则。
- `root_causes`：有序数组，按重要程度排列。仅在合格通过（所有活跃维度 raw_score >= 60 且无封顶触发）时允许返回空数组。否则必须返回至少一个根因。
- `narrative_review`：保持简短且可执行。

## 叙事评审模板

保持可读且简洁：
- `summary`：一段话概括整体判断
- `strengths`：仅列出真正的优势
- `weaknesses`：驱动分数的主要不足
- `next_actions`：产品和算法团队可以执行的修复建议

## 序列化规则

在机器可读性和文字表现力之间选择时，优先保持 JSON 稳定，缩短叙事。
