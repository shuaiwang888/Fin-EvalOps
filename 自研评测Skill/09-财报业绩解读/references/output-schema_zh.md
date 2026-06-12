# 输出格式规范

先输出结构化 JSON。在调用方需要可读摘要时，JSON 后附简短的自然语言评审。

## JSON 结构

```json
{
  "schema_version": "financial-performance-interpretation/v3",
  "weight_assignment": {
    "intent_understanding": {"dynamic_weight": 15, "applicability": "relevant", "rationale": "用户要求解释现金流增长原因"},
    "report_data_accuracy": {"dynamic_weight": 15, "applicability": "relevant", "rationale": "需要核验2026Q1现金流和同比数据"},
    "primary_evidence_quality": {"dynamic_weight": 20, "applicability": "relevant", "rationale": "原因可能来自一季报披露原文"},
    "causal_attribution_depth": {"dynamic_weight": 20, "applicability": "relevant", "rationale": "用户问是什么原因"},
    "business_financial_linkage": {"dynamic_weight": 10, "applicability": "relevant", "rationale": "需解释应收票据兑付如何传导到经营现金流"},
    "forward_investment_judgment": {"dynamic_weight": 0, "applicability": "not_applicable", "rationale": "用户未问股价影响或持续性"},
    "composition_credibility": {"dynamic_weight": 5, "applicability": "supplementary", "rationale": "表达质量始终有参考价值"},
    "tool_usage": {"dynamic_weight": 15, "applicability": "relevant", "rationale": "需评估是否使用公告全文和金融查询工具"}
  },
  "skipped_dimensions": ["forward_investment_judgment"],
  "matched_golden_cases": [
    {
      "case_id": "case_14_mayinglong_cash_flow_growth",
      "matched_hard_checks": ["必须命中公司一季报官方披露：本部应收票据到期兑付较上年同期增加"]
    }
  ],
  "dimension_scores": {
    "intent_understanding": {"raw_score": 0, "evidence": []},
    "report_data_accuracy": {"raw_score": 0, "evidence": []},
    "primary_evidence_quality": {"raw_score": 0, "evidence": []},
    "causal_attribution_depth": {"raw_score": 0, "evidence": []},
    "business_financial_linkage": {"raw_score": 0, "evidence": []},
    "composition_credibility": {"raw_score": 0, "evidence": []},
    "tool_usage": {"raw_score": 0, "evidence": []}
  },
  "caps": [
    {
      "rule_id": "missing_primary_disclosure",
      "triggered": true,
      "score_ceiling": 55,
      "reason": "一季报已明确说明现金流增长主因，但答案未提及官方披露。",
      "evidence": []
    }
  ],
  "root_causes": [
    {
      "l1": "evidence",
      "l2": "missing-primary-filing",
      "dimension": "primary_evidence_quality",
      "raw_score": 1,
      "confidence": "high",
      "summary": "答案只做结构化报表推理，未核验一季报原文，遗漏官方披露的现金流增长主因。",
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

## 证据对象格式

```json
{
  "source": "question | final_answer | context | reasoning | function_call | function_call_output",
  "pointer": "context[0].answer | chain[0].plan | chain[0].tools[0] | chain[0].tools[0].output",
  "summary": "简短的证据摘要"
}
```

| source | pointer 格式 | 指向 |
|---|---|---|
| `question` | `question` | 用户当前问题 |
| `final_answer` | `text_answer` | 最终答案纯文本版本 |
| `context` | `context[N].answer` | 对话中第 N 轮历史答案 |
| `reasoning` | `chain[N].plan` | 第 N 步规划/推理文本 |
| `function_call` | `chain[N].tools[M]` | 第 N 步第 M 次工具调用 |
| `function_call_output` | `chain[N].tools[M].output` | 第 N 步第 M 次工具输出 |

评分时以 `text_answer` 为主锚点。仅在评估呈现或可视化质量时引用 `answer`（markdown 版本）。除非调用方明确要求，不要输出长引文。

## 字段规则

- `schema_version`：固定为 `financial-performance-interpretation/v3`。v3 将 `weighted_points`、`absolute_score_pre_cap`、`final_score` 移至调用方代码，LLM 只负责判断和打分。
- `weight_assignment`：每个维度的动态权重分配结果。包含 `dynamic_weight`、`applicability`、`rationale`。所有 `dynamic_weight` 之和必须 = 100。
- `skipped_dimensions`：`not_applicable` 维度名称列表。这些维度不出现在 `dimension_scores` 中。
- `matched_golden_cases`：记录命中的专家案例和实际使用的 hard checks；未命中时允许为空数组。
- `dimension_scores`：仅包含 `relevant` 和 `supplementary` 维度。每个维度只输出 `raw_score`（六档：0/20/40/60/80/100）和 `evidence`。不要输出 `weighted_points`、`absolute_score_pre_cap`、`final_score`。注意：`tool_usage` 虽始终 `relevant`，但在步骤 1 盲评阶段跳过，于步骤 2 链路诊断阶段评分后补入此对象。
- `caps`：包含所有触发的封顶规则，或所有与活跃维度相关且被显式检查过的封顶规则。
- `root_causes`：有序数组，按重要程度排列。仅在所有活跃维度 raw_score >= 60 且无封顶触发时允许为空数组，否则必须至少一个根因。
- `narrative_review`：保持简短、可执行。

## 叙事评审模板

- `summary`：一段话概括整体判断
- `strengths`：仅列真正优势
- `weaknesses`：驱动分数的主要不足
- `next_actions`：产品或算法团队可以执行的修复建议

## 序列化规则

在机器可读性和文字表现力之间选择时，优先保持 JSON 稳定，缩短叙事。
