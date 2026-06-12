# 输出格式规范

先输出结构化 JSON。在调用方需要可读摘要时，JSON 后附简短自然语言评审。

本 schema 遵循 01 的 result-only 输出风格：模型输出原始维度分、共享权重、质量标签、理由和证据；派生数值字段保留给评测引擎或代码填充/覆盖，LLM 不需要手算。

## JSON 结构

```json
{
  "schema_version": "stock-diagnosis-and-data-lookup-self-vs-competitor-result-only/v1",
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
    "intent_fulfillment": {
      "dynamic_weight": 12,
      "applicability": "relevant",
      "rationale": ""
    },
    "data_accuracy_coverage": {
      "dynamic_weight": 20,
      "applicability": "relevant",
      "rationale": ""
    },
    "time_caliber_precision": {
      "dynamic_weight": 13,
      "applicability": "relevant",
      "rationale": ""
    },
    "calculation_comparison": {
      "dynamic_weight": 11,
      "applicability": "relevant",
      "rationale": ""
    },
    "analysis_framework_fit": {
      "dynamic_weight": 18,
      "applicability": "relevant",
      "rationale": ""
    },
    "insight_extension": {
      "dynamic_weight": 11,
      "applicability": "relevant",
      "rationale": ""
    },
    "result_verifiability": {
      "dynamic_weight": 10,
      "applicability": "relevant",
      "rationale": ""
    },
    "presentation_visualization": {
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
      "intent_fulfillment": {
        "raw_score": 0,
        "dynamic_weight": 0,
        "rationale": "",
        "evidence": []
      },
      "data_accuracy_coverage": {
        "raw_score": 0,
        "dynamic_weight": 0,
        "rationale": "",
        "evidence": []
      },
      "time_caliber_precision": {
        "raw_score": 0,
        "dynamic_weight": 0,
        "rationale": "",
        "evidence": []
      },
      "calculation_comparison": {
        "raw_score": 0,
        "dynamic_weight": 0,
        "rationale": "",
        "evidence": []
      },
      "analysis_framework_fit": {
        "raw_score": 0,
        "dynamic_weight": 0,
        "rationale": "",
        "evidence": []
      },
      "insight_extension": {
        "raw_score": 0,
        "dynamic_weight": 0,
        "rationale": "",
        "evidence": []
      },
      "result_verifiability": {
        "raw_score": 0,
        "dynamic_weight": 0,
        "rationale": "",
        "evidence": []
      },
      "presentation_visualization": {
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
      "intent_fulfillment": {
        "raw_score": 0,
        "dynamic_weight": 0,
        "rationale": "",
        "evidence": []
      },
      "data_accuracy_coverage": {
        "raw_score": 0,
        "dynamic_weight": 0,
        "rationale": "",
        "evidence": []
      },
      "time_caliber_precision": {
        "raw_score": 0,
        "dynamic_weight": 0,
        "rationale": "",
        "evidence": []
      },
      "calculation_comparison": {
        "raw_score": 0,
        "dynamic_weight": 0,
        "rationale": "",
        "evidence": []
      },
      "analysis_framework_fit": {
        "raw_score": 0,
        "dynamic_weight": 0,
        "rationale": "",
        "evidence": []
      },
      "insight_extension": {
        "raw_score": 0,
        "dynamic_weight": 0,
        "rationale": "",
        "evidence": []
      },
      "result_verifiability": {
        "raw_score": 0,
        "dynamic_weight": 0,
        "rationale": "",
        "evidence": []
      },
      "presentation_visualization": {
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
    "intent_fulfillment": {
      "winner": "self | competitor | tie",
      "self_raw_score": 0,
      "competitor_raw_score": 0,
      "score_delta": 0,
      "rationale": "",
      "evidence": []
    },
    "data_accuracy_coverage": {
      "winner": "self | competitor | tie",
      "self_raw_score": 0,
      "competitor_raw_score": 0,
      "score_delta": 0,
      "rationale": "",
      "evidence": []
    },
    "time_caliber_precision": {
      "winner": "self | competitor | tie",
      "self_raw_score": 0,
      "competitor_raw_score": 0,
      "score_delta": 0,
      "rationale": "",
      "evidence": []
    },
    "calculation_comparison": {
      "winner": "self | competitor | tie",
      "self_raw_score": 0,
      "competitor_raw_score": 0,
      "score_delta": 0,
      "rationale": "",
      "evidence": []
    },
    "analysis_framework_fit": {
      "winner": "self | competitor | tie",
      "self_raw_score": 0,
      "competitor_raw_score": 0,
      "score_delta": 0,
      "rationale": "",
      "evidence": []
    },
    "insight_extension": {
      "winner": "self | competitor | tie",
      "self_raw_score": 0,
      "competitor_raw_score": 0,
      "score_delta": 0,
      "rationale": "",
      "evidence": []
    },
    "result_verifiability": {
      "winner": "self | competitor | tie",
      "self_raw_score": 0,
      "competitor_raw_score": 0,
      "score_delta": 0,
      "rationale": "",
      "evidence": []
    },
    "presentation_visualization": {
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

- `schema_version`：固定为 `stock-diagnosis-and-data-lookup-self-vs-competitor-result-only/v1`。
- `pairing.case_id`：同题配对键，自研与竞品共享的唯一标识。
- `pairing.self_model_id`：固定为 `"self"`，除非调用方提供明确自研模型名。
- `pairing.competitor_model_id`：竞品模型名称，取自输入数据。
- `pairing.same_question_verified`：若为 `false`，不得继续输出胜负结论。
- `answer_anchors`：记录双方最终回答实际读取位置。
- `weight_assignment`：同一题下双方共享的动态权重，必须完全一致，权重总和必须为 100。
- `skipped_dimensions`：仅当维度完全不适用于本题时加入。
- `matched_golden_cases`：命中的专家案例 ID 列表；不命中时留空。
- `dimension_scores`：每个活跃维度必须包含 `raw_score`、`dynamic_weight`、`rationale`、`evidence`。
- `raw_score`：只能使用 0/20/40/60/80/100 六档锚定值。
- `absolute_score_pre_cap`、`final_score`、`dimension_comparison[*].score_delta` 与 `comparison_summary` 中的分数字段：由评测引擎或代码根据原始分、权重和质量标签填充/覆盖，LLM 不需要手算或解释公式。
- `applied_caps`：记录触发的质量标签；LLM 只输出标签及其最终回答证据，具体限分由代码处理。
- `dimension_comparison`：逐维输出谁更强、理由和证据。
- `self_strengths`：只写自研真正成立的优势；若只是“比竞品稍好但仍未达标”，应优先放入 `shared_failures` 或 `self_weaknesses`。
- `self_weaknesses`：写自研相对竞品或相对专家标准的真实不足。
- `competitor_strengths`：写竞品最终回答中真正值得学习的地方。
- `shared_failures`：双方都未达到专家标准时必须填写。
- `comparison_summary.verdict`：若双方都明显不达标，即便一方相对略好，也应使用 `both_poor`。


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
