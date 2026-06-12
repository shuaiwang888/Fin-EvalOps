# 输出格式规范

先输出结构化 JSON。在调用方需要可读摘要时，JSON 后附简短自然语言评审。

## JSON 结构

```json
{
  "schema_version": "financial-logical-reasoning-self-vs-competitor-result-only/v1",
  "category": "",
  "core_user_intent": "",
  "pairing": {
    "case_id": "",
    "self_model_id": "self",
    "competitor_model_id": "",
    "same_question_verified": true
  },
  "absolute_quality_flag": "both_good | self_poor | competitor_poor | both_poor",
  "answer_anchors": {
    "self_final_answer_pointer": "",
    "competitor_final_answer_pointer": ""
  },
  "weight_assignment": {
    "financial_logic_chain": {
      "dynamic_weight": 25,
      "applicability": "relevant",
      "rationale": ""
    },
    "market_driver_identification": {
      "dynamic_weight": 20,
      "applicability": "relevant",
      "rationale": ""
    },
    "evidence_to_conclusion": {
      "dynamic_weight": 25,
      "applicability": "relevant",
      "rationale": ""
    },
    "comparison_and_ranking": {
      "dynamic_weight": 15,
      "applicability": "relevant",
      "rationale": ""
    },
    "scenario_risk_reasoning": {
      "dynamic_weight": 10,
      "applicability": "supplementary",
      "rationale": ""
    },
    "decision_value_expression": {
      "dynamic_weight": 5,
      "applicability": "supplementary",
      "rationale": ""
    }
  },
  "skipped_dimensions": [],
  "matched_golden_cases": [],
  "score_summary": {
    "self_score": 0,
    "competitor_score": 0,
    "score_delta": 0,
    "tie_threshold": 8,
    "key_dimension_override": false
  },
  "self_evaluation": {
    "dimension_scores": {
      "financial_logic_chain": {
        "raw_score": 0,
        "dynamic_weight": 0,
        "rationale": "",
        "evidence": []
      },
      "market_driver_identification": {
        "raw_score": 0,
        "dynamic_weight": 0,
        "rationale": "",
        "evidence": []
      },
      "evidence_to_conclusion": {
        "raw_score": 0,
        "dynamic_weight": 0,
        "rationale": "",
        "evidence": []
      },
      "comparison_and_ranking": {
        "raw_score": 0,
        "dynamic_weight": 0,
        "rationale": "",
        "evidence": []
      },
      "scenario_risk_reasoning": {
        "raw_score": 0,
        "dynamic_weight": 0,
        "rationale": "",
        "evidence": []
      },
      "decision_value_expression": {
        "raw_score": 0,
        "dynamic_weight": 0,
        "rationale": "",
        "evidence": []
      }
    },
    "absolute_score_pre_cap": 0,
    "applied_caps": [],
    "final_score": 0,
    "summary": "",
    "strengths": [],
    "weaknesses": []
  },
  "competitor_evaluation": {
    "dimension_scores": {
      "financial_logic_chain": {
        "raw_score": 0,
        "dynamic_weight": 0,
        "rationale": "",
        "evidence": []
      },
      "market_driver_identification": {
        "raw_score": 0,
        "dynamic_weight": 0,
        "rationale": "",
        "evidence": []
      },
      "evidence_to_conclusion": {
        "raw_score": 0,
        "dynamic_weight": 0,
        "rationale": "",
        "evidence": []
      },
      "comparison_and_ranking": {
        "raw_score": 0,
        "dynamic_weight": 0,
        "rationale": "",
        "evidence": []
      },
      "scenario_risk_reasoning": {
        "raw_score": 0,
        "dynamic_weight": 0,
        "rationale": "",
        "evidence": []
      },
      "decision_value_expression": {
        "raw_score": 0,
        "dynamic_weight": 0,
        "rationale": "",
        "evidence": []
      }
    },
    "absolute_score_pre_cap": 0,
    "applied_caps": [],
    "final_score": 0,
    "summary": "",
    "strengths": [],
    "weaknesses": []
  },
  "dimension_comparison": {
    "financial_logic_chain": {
      "winner": "self | competitor | tie",
      "self_raw_score": 0,
      "competitor_raw_score": 0,
      "score_delta": 0,
      "rationale": "",
      "evidence": []
    },
    "market_driver_identification": {
      "winner": "self | competitor | tie",
      "self_raw_score": 0,
      "competitor_raw_score": 0,
      "score_delta": 0,
      "rationale": "",
      "evidence": []
    },
    "evidence_to_conclusion": {
      "winner": "self | competitor | tie",
      "self_raw_score": 0,
      "competitor_raw_score": 0,
      "score_delta": 0,
      "rationale": "",
      "evidence": []
    },
    "comparison_and_ranking": {
      "winner": "self | competitor | tie",
      "self_raw_score": 0,
      "competitor_raw_score": 0,
      "score_delta": 0,
      "rationale": "",
      "evidence": []
    },
    "scenario_risk_reasoning": {
      "winner": "self | competitor | tie",
      "self_raw_score": 0,
      "competitor_raw_score": 0,
      "score_delta": 0,
      "rationale": "",
      "evidence": []
    },
    "decision_value_expression": {
      "winner": "self | competitor | tie",
      "self_raw_score": 0,
      "competitor_raw_score": 0,
      "score_delta": 0,
      "rationale": "",
      "evidence": []
    }
  },
  "self_strengths": [
    {
      "dimension": "",
      "summary": "",
      "evidence": []
    }
  ],
  "self_weaknesses": [
    {
      "dimension": "",
      "summary": "",
      "attribution_tag": "",
      "evidence": []
    }
  ],
  "competitor_strengths": [
    {
      "dimension": "",
      "summary": "",
      "evidence": []
    }
  ],
  "competitor_weaknesses": [
    {
      "dimension": "",
      "summary": "",
      "attribution_tag": "",
      "evidence": []
    }
  ],
  "shared_failures": [
    {
      "dimension": "",
      "summary": "",
      "attribution_tag": "",
      "evidence": []
    }
  ],
  "comparison_summary": {
    "absolute_summary": "",
    "relative_summary": "",
    "verdict": "self_better | competitor_better | tie",
    "self_final_score": 0,
    "competitor_final_score": 0,
    "score_delta": 0,
    "why": []
  },
  "final_explanation": {
    "short_answer": "",
    "why": "",
    "what_self_should_learn_from_competitor": "",
    "what_self_must_fix": ""
  }
}
```

## 字段规则

- `schema_version`：固定为 `financial-logical-reasoning-self-vs-competitor-result-only/v1`。
- `pairing.case_id`：同题配对键，自研与竞品共享的唯一标识。
- `pairing.self_model_id`：固定为 `"self"`，除非调用方提供明确自研模型名。
- `pairing.competitor_model_id`：竞品模型名称，取自输入数据。
- `pairing.same_question_verified`：若为 `false`，不得继续输出胜负结论。
- `answer_anchors`：记录双方最终回答实际读取位置。
- `weight_assignment`：同一题下双方共享的动态权重，必须完全一致，权重总和必须为 100。
- `skipped_dimensions`：仅当维度完全不适用于本题时加入。
- `matched_golden_cases`：命中的专家案例 ID 列表；不命中时留空。
- `dimension_scores`：每个活跃维度必须包含 `raw_score`、`dynamic_weight`、`rationale`、`evidence`（`weighted_score` 由评测引擎注入，LLM 无需输出）。
- `absolute_score_pre_cap`：由评测引擎根据活跃维度的 raw_score 和 dynamic_weight 自动计算。
- `applied_caps`：记录触发的封顶标签。本类别沿用标签式封顶：`applied_caps` 不直接改写分数。
- `final_score`：由评测引擎根据 `absolute_score_pre_cap` 和 `applied_caps` 自动计算。
- `dimension_comparison`：逐维输出谁更强、分差、理由和证据；`score_delta = self_raw_score - competitor_raw_score`。
- `self_strengths`：只写自研真正成立的优势；若只是“比竞品稍好但仍未达标”，应优先放入 `shared_failures` 或 `self_weaknesses`。
- `self_weaknesses`：写自研相对竞品或相对专家标准的真实不足。
- `competitor_strengths`：写竞品最终回答中真正值得学习的地方。
- `shared_failures`：双方都未达到专家标准时必须填写。
- `comparison_summary.verdict`：只允许 `self_better | competitor_better | tie` 三个值。`both_poor` 场景通过 `absolute_quality_flag` 表达，不进入 verdict。


- `category`：题目所属评测类别标识。
- `core_user_intent`：一句话描述用户的核心决策需求。
- `absolute_quality_flag`：绝对质量标记，独立于 verdict。`both_good` 表示双方都达标；`self_poor` / `competitor_poor` 表示一方不达标；`both_poor` 表示双方都不达标。
- `score_summary`：汇总双方加权总分、分差、tie 判定阈值和关键维度覆盖标记。
- `score_summary.tie_threshold`：默认 8。加权总分差绝对值 < 8 时默认判 tie。
- `score_summary.key_dimension_override`：若某关键维度分差 >= 20 且该维度对题目核心任务重要且证据明确，可覆盖总分判定；此时为 `true`。
- `competitor_weaknesses`：竞品相对专家标准的不足，每条含 `attribution_tag`。
- `final_explanation`：自然语言总结，含 `short_answer`（一句结论）、`why`（核心原因）、`what_self_should_learn_from_competitor`（值得学习的点）、`what_self_must_fix`（必须修复的问题）。
- `comparison_summary.verdict`：只允许 `self_better | competitor_better | tie` 三个值。`both_poor` 场景通过 `absolute_quality_flag` 表达。

## 证据对象格式

```json
{
  "source": "question | self_final_answer | competitor_final_answer",
  "pointer": "question | self_record.text_answer | self_record.answer | competitor_record.text_answer | competitor_record.answer | normalized.self_final_answer | normalized.competitor_final_answer",
  "quote_or_summary": "",
  "rationale": ""
}
```

## 证据使用原则

- 每个维度评分至少一条 evidence。
- 每条 `self_strengths`、`self_weaknesses`、`competitor_strengths`、`shared_failures` 至少一条 evidence。
- evidence 只能指向用户问题、自研最终回答或竞品最终回答。
- `quote_or_summary` 优先使用短原文；原文过长时可以摘要，但必须通过 pointer 回指。
- 如果最终回答没有体现某个信息，不能把它写成评分依据、优点、缺点、共同失败点或胜负原因。

封顶规则在本类别中作为标签保留，不修改 `final_score`。
