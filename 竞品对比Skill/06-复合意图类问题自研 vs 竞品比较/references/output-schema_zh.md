# 输出格式规范

先输出结构化 JSON。在调用方需要可读摘要时，JSON 后附简短自然语言评审。

## JSON 结构

```json
{
  "schema_version": "compound-intent-self-vs-competitor/v1",
  "pairing": {
    "case_id": "",
    "self_model_id": "self",
    "competitor_model_id": "",
    "same_question_verified": true
  },
  "weight_assignment": {
    "intent_decomposition": {"dynamic_weight": 16, "applicability": "relevant", "rationale": "用户一句话包含多个明确子任务，需要先拆解"},
    "task_coverage_priority": {"dynamic_weight": 14, "applicability": "relevant", "rationale": "需要覆盖所有关键子任务并按主次组织"},
    "multi_source_evidence_integration": {"dynamic_weight": 14, "applicability": "relevant", "rationale": "问题需要整合新闻、行情、公告和产业证据"},
    "analysis_chain_closure": {"dynamic_weight": 16, "applicability": "relevant", "rationale": "需要形成事实、影响、传导、策略闭环"},
    "data_logic_rigor": {"dynamic_weight": 14, "applicability": "relevant", "rationale": "涉及时间窗口、数据口径和量化判断"},
    "decision_actionability": {"dynamic_weight": 10, "applicability": "relevant", "rationale": "用户要求投资结论和操作框架"},
    "composition_readability": {"dynamic_weight": 5, "applicability": "supplementary", "rationale": "复杂问题需要清晰结构降低理解成本"},
    "tool_usage": {"dynamic_weight": 7, "applicability": "relevant", "rationale": "链路需要核验工具是否支撑多子任务证据需求"}
  },
  "skipped_dimensions": [],
  "matched_golden_cases": [
    {
      "case_id": "case04_market_news_smic_impact",
      "matched_reason": "用户要求多个时间窗口新闻梳理并评估对单一公司的影响",
      "hard_checks_used": ["覆盖48小时市场热点", "覆盖7天中芯国际相关信息", "按短中长期评估影响", "image_anchor: 无依据资金数据会拖垮影响评估"]
    }
  ],
  "self_evaluation": {
    "dimension_scores": {
      "intent_decomposition": {"raw_score": 0, "evidence": []},
      "task_coverage_priority": {"raw_score": 0, "evidence": []},
      "multi_source_evidence_integration": {"raw_score": 0, "evidence": []},
      "analysis_chain_closure": {"raw_score": 0, "evidence": []},
      "data_logic_rigor": {"raw_score": 0, "evidence": []},
      "decision_actionability": {"raw_score": 0, "evidence": []},
      "composition_readability": {"raw_score": 0, "evidence": []},
      "tool_usage": {"raw_score": 0, "evidence": []}
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
        "raw_score": 40,
        "confidence": "high",
        "summary": "答案覆盖了年报解读和大跌原因，但漏掉用户要求的可核验历史先例，导致复合任务未完整闭环。",
        "evidence": []
      }
    ],
    "narrative_review": {"summary": "", "strengths": [], "weaknesses": [], "next_actions": []}
  },
  "competitor_evaluation": {
    "dimension_scores": {
      "intent_decomposition": {"raw_score": 0, "evidence": []},
      "task_coverage_priority": {"raw_score": 0, "evidence": []},
      "multi_source_evidence_integration": {"raw_score": 0, "evidence": []},
      "analysis_chain_closure": {"raw_score": 0, "evidence": []},
      "data_logic_rigor": {"raw_score": 0, "evidence": []},
      "decision_actionability": {"raw_score": 0, "evidence": []},
      "composition_readability": {"raw_score": 0, "evidence": []},
      "tool_usage": {"raw_score": 0, "evidence": []}
    },
    "caps": [],
    "root_causes": [],
    "narrative_review": {"summary": "", "strengths": [], "weaknesses": [], "next_actions": []}
  },
  "dimension_comparison": {
    "intent_decomposition": {
      "winner": "self | competitor | tie",
      "self_raw_score": 0,
      "competitor_raw_score": 0,
      "score_delta": 0,
      "rationale": "",
      "evidence": []
    }
  },
  "self_strengths": [
    {"dimension": "", "summary": "", "evidence": []}
  ],
  "self_weaknesses": [
    {"dimension": "", "summary": "", "evidence": []}
  ],
  "competitor_strengths": [
    {"dimension": "", "summary": "", "evidence": []}
  ],
  "shared_failures": [
    {"dimension": "", "summary": "", "evidence": []}
  ],
  "chain_attribution": {
    "self": [
      {"stage": "intent | coverage | evidence | tool | data_logic | reasoning | composition", "summary": "", "evidence": []}
    ],
    "competitor": [
      {"stage": "intent | coverage | evidence | tool | data_logic | reasoning | composition", "summary": "", "evidence": []}
    ],
    "cross_model_observations": []
  },
  "comparison_summary": {
    "absolute_summary": "",
    "relative_summary": "",
    "verdict": "self_better | competitor_better | tie | both_poor",
    "why": []
  }
}
```

> **注意**：`weighted_points`、`absolute_score_pre_cap`、`final_score` 由调用方代码自动计算，你不需要输出这些字段。你只需在 `self_evaluation.dimension_scores` 与 `competitor_evaluation.dimension_scores` 中输出每个活跃维度的 `raw_score`（六档：0/20/40/60/80/100）和 `evidence`。

## 字段规则

- `schema_version`：固定为 `compound-intent-self-vs-competitor/v1`。
- `pairing.case_id`：同题配对键，自研与竞品共享的唯一标识，用于回溯原始样本。
- `pairing.self_model_id`：固定为 `"self"`（被评测的自研模型）。
- `pairing.competitor_model_id`：竞品模型名称，取自输入数据。
- `pairing.same_question_verified`：若为 `false`，不得继续输出胜负结论。
- `weight_assignment`：同一题下双方共享的动态权重，必须完全一致。权重由 Round 1 确定，Round 2 照抄。
- `skipped_dimensions`：标记为 `not_applicable` 的维度列表。仅当该维度完全不适用于本题时才加入。
- `matched_golden_cases`：记录命中的专家案例和实际使用的 hard checks；未命中时允许为空数组。若使用了截图锚点，可在 `hard_checks_used` 中用 `image_anchor: ...` 简写记录。
- `self_evaluation` / `competitor_evaluation`：分别是两边的绝对评测结果，结构遵循本 skill 定义的维度、封顶和根因体系。
- `dimension_scores`：仅包含 `relevant` 和 `supplementary` 维度，不含 `skipped_dimensions` 中的维度。每个维度只需输出 `raw_score` 和 `evidence`。
- `caps`：包含所有考虑过的封顶规则（仅与活跃维度相关的），或至少包含所有触发的封顶规则。
- `root_causes`：有序数组，按重要程度排列。仅在合格通过（所有活跃维度 raw_score >= 60 且无封顶触发）时允许返回空数组。否则必须返回至少一个根因。
- `dimension_comparison`：逐维输出谁更强、分差、理由和证据。`score_delta = self_raw_score - competitor_raw_score`。
- `self_strengths`：只写自研真正成立的优势；若只是“比竞品稍好但仍未达标”，应优先放入 `shared_failures` 或 `self_weaknesses`。
- `self_weaknesses`：写自研相对竞品或相对专家标准的真实不足。
- `competitor_strengths`：写竞品真正值得学习的地方，必须有答案或链路证据。
- `shared_failures`：双方都未达到专家标准时必须填写。
- `chain_attribution`：解释链路如何导致最终答案更好/更差；不要脱离答案单独评价链路“是否漂亮”。
- `comparison_summary.absolute_summary`：先写双方按专家标准各自好不好。
- `comparison_summary.relative_summary`：再写双方谁相对更好。
- `comparison_summary.verdict`：若双方都明显不达标，即便一方分数略高，也应使用 `both_poor`。

## 最终答案锚点

- 自研模型最终答案：优先 `self_record.text_answer`；
- 竞品模型最终答案：若 `competitor_record.text_answer` 为空，则使用 `competitor_record.answer`；
- 若编排层已生成统一字段，可读取归一化字段，但证据仍需回指原始字段。

## 证据对象格式

```json
{
  "source": "question | self_final_answer | competitor_final_answer | self_context | competitor_context | self_reasoning | competitor_reasoning | self_function_call | competitor_function_call | self_function_call_output | competitor_function_call_output | self_screenshot_ocr | competitor_screenshot_ocr | self_expert_annotation | competitor_expert_annotation | online_signal",
  "pointer": "question | self_record.text_answer | competitor_record.answer | self_record.chain[0].plan | competitor_record.chain[0].tools[0].output | competitor_record.annotations[0]",
  "summary": "简短的证据摘要"
}
```

## 证据使用原则

- 评分主锚点仍是双方各自最终答案。
- 工具调用证据统一从 `self_record.chain[N].tools[M]` / `competitor_record.chain[N].tools[M]` 读取。
- 当竞品 `plan` 为空时，不要臆造不可见推理；可直接引用工具调用、工具输出和最终答案。
- 截图 OCR、人工批注、线上维度信号可用于校准 hard checks 和根因，但不得覆盖最终答案锚点。
- 输出优势/劣势时，优先用短证据摘要，不要复制长段原文。
- 若一条差异无法追溯到答案或链路证据，不要写成确定结论。

## 叙事评审模板

- `absolute_summary`：先说明双方按专家标准各自是否合格。
- `relative_summary`：再说明自研相对竞品领先/落后在哪里。
- `why`：仅列真正驱动结论的高信号原因。
