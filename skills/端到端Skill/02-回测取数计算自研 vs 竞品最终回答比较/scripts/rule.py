"""
02-backtesting-data-extraction-and-calculation result-only 自研 vs 竞品评测规则定义。

该比较 skill 只定义回测取数计算领域的最终回答质量维度、默认权重和质量标签。
pairwise 比较字段由输出 schema 约束。
"""

DIMENSIONS = [
    {
        "key": "intent_fulfillment",
        "label_zh": "意图满足度",
        "description": "评估最终回答是否完整、准确地满足用户的取数、统计、回测或计算需求。",
        "six_level_anchors": {
            0: "完全未响应用户的取数计算需求",
            20: "仅给出无关信息或极度不完整的回答，核心计算需求未满足",
            40: "部分满足但遗漏了关键数据/计算步骤，或理解有实质性偏差",
            60: "基本满足需求，但有明显可改进之处，如精度不足或个别指标遗漏",
            80: "很好地满足需求，数据完整、计算准确，仅有极小瑕疵",
            100: "完美满足，数据全覆盖、计算精确、展示清晰，无任何可挑剔之处",
        },
    },
    {
        "key": "data_retrieval_accuracy",
        "label_zh": "取数准确性",
        "description": "评估最终回答中引用的数据值、字段、样本和覆盖范围是否正确完整。",
        "six_level_anchors": {
            0: "完全没有给出需要的数据，或给出的数据完全错误",
            20: "给出了少量相关数据但核心字段缺失严重，或数据口径明显错误",
            40: "覆盖了主要数据但遗漏重要维度，或筛选条件使用有误",
            60: "数据覆盖基本完整，正确性良好，但个别字段或筛选精度不足",
            80: "数据准确完整，字段齐全，筛选条件精确",
            100: "数据完美，所有维度全覆盖，筛选条件精确无误，数据可复现",
        },
    },
    {
        "key": "time_inference",
        "label_zh": "时间推理正确性",
        "description": "评估最终回答中的日期、交易日、节假日、披露日、盘中时点和时间范围推理是否正确。",
        "six_level_anchors": {
            0: "时间推理完全错误，使用了完全错误的时间范围",
            20: "时间方向正确但具体日期/窗口存在严重偏差",
            40: "时间推理方向正确但精度不足，或遗漏交易日/节假日调整",
            60: "时间推理基本正确，但个别边界日期或节假日处理不够精确",
            80: "时间推理准确，交易日/节假日/倒推逻辑均正确处理",
            100: "时间推理完美，所有日期边界精确，节假日/交易日/复权日期全部正确处理",
        },
    },
    {
        "key": "calculation_accuracy",
        "label_zh": "计算准确性",
        "description": "评估最终回答中的涨跌幅、概率、盈亏、财务比率、复权收益等公式和算术是否正确。",
        "six_level_anchors": {
            0: "计算完全错误或使用了错误公式",
            20: "计算方向正确但核心结果存在实质错误",
            40: "主要计算正确但个别指标的计算方法或口径有误",
            60: "计算基本正确，但精度或中间步骤有轻微瑕疵",
            80: "计算完全正确，方法得当，结果精确",
            100: "计算完美，方法最优，精度最高，中间步骤可验证",
        },
    },
    {
        "key": "logical_decomposition",
        "label_zh": "逻辑拆解能力",
        "description": "评估最终回答是否将复杂多步/多条件查询拆解为完整、可执行、闭合的子任务。",
        "six_level_anchors": {
            0: "完全没有拆解，将复杂任务当作简单查询处理",
            20: "尝试了拆解但拆解方式与问题核心逻辑不匹配",
            40: "拆解方向正确但步骤遗漏或顺序不当，影响准确性",
            60: "拆解基本合理，但部分步骤可有更优方式",
            80: "拆解逻辑清晰，步骤合理，依赖关系正确",
            100: "拆解完美，最优步骤分解，依赖关系清晰，每一步都有明确目的",
        },
    },
    {
        "key": "result_verifiability",
        "label_zh": "结果可验证性",
        "description": "评估最终回答是否提供足够明细、样本、公式代入和中间结果，让用户能够复核。",
        "six_level_anchors": {
            0: "结果完全无法验证，无任何中间数据或计算过程",
            20: "给出了最终结果但中间步骤/数据来源几乎不可追溯",
            40: "部分中间信息可追溯但关键步骤缺失或数据来源不明确",
            60: "主要结果可验证，但个别中间数据或计算环节不够透明",
            80: "结果可验证，数据来源清晰，计算过程可追溯",
            100: "结果完全可复现，每一步都有明确的数据来源、样本和计算过程",
        },
    },
    {
        "key": "expression_quality",
        "label_zh": "表达与展示质量",
        "description": "评估最终回答的结构、表格、口径说明和关键结论呈现是否清晰专业。",
        "six_level_anchors": {
            0: "表达混乱，无法理解输出内容",
            20: "表达模糊，信息碎片化，难以提取有效结论",
            40: "表达基本可读但结构性差，关键信息被淹没",
            60: "表达清晰但格式或层次可优化，数据展示不够直观",
            80: "表达清晰准确，结构合理，数据展示直观",
            100: "表达完美，简洁有力，结构一目了然，可视化恰到好处",
        },
    },
]

DEFAULT_WEIGHTS = {
    "intent_fulfillment": 13,
    "data_retrieval_accuracy": 23,
    "time_inference": 17,
    "calculation_accuracy": 18,
    "logical_decomposition": 10,
    "result_verifiability": 12,
    "expression_quality": 7,
}

WEIGHT_RULES: list[dict] = []

CAP_RULES = [
    {
        "name": "data_fabrication",
        "label_zh": "数据虚构",
        "label_tag": "数据虚构",
        "severity": "critical",
        "ceiling": 35,
        "score_effect": "tag_only",
        "description": "最终回答包含编造的统计数据、历史价格、财务数据、事件日期或看似精确但不可验证的计算结果。",
    },
    {
        "name": "time_inference_error",
        "label_zh": "时间推理错误",
        "label_tag": "时间推理错误",
        "severity": "critical",
        "ceiling": 45,
        "score_effect": "tag_only",
        "description": "最终回答中的日期、交易日、节假日、披露日或时间范围推理存在实质性错误。",
    },
    {
        "name": "calculation_logic_error",
        "label_zh": "计算逻辑错误",
        "label_tag": "计算逻辑错误",
        "severity": "critical",
        "ceiling": 50,
        "score_effect": "tag_only",
        "description": "最终回答中的公式选择、算术运算、分子分母、复权口径或衍生指标计算存在逻辑错误。",
    },
    {
        "name": "intraday_precision_missing",
        "label_zh": "日内精度缺失",
        "label_tag": "日内精度缺失",
        "severity": "warning",
        "ceiling": 55,
        "score_effect": "tag_only",
        "description": "用户要求盘中或具体时点精度，但最终回答只使用日线、开收盘或均价口径并输出确定结论。",
    },
    {
        "name": "missing_required_data",
        "label_zh": "遗漏必要数据",
        "label_tag": "遗漏必要数据",
        "severity": "warning",
        "ceiling": 60,
        "score_effect": "tag_only",
        "description": "最终回答遗漏用户明确要求的数据维度、关键标的、字段、样本范围或统计明细。",
    },
    {
        "name": "unverifiable_result",
        "label_zh": "结果不可验证",
        "label_tag": "结果不可验证",
        "severity": "warning",
        "ceiling": 65,
        "score_effect": "tag_only",
        "description": "最终回答给出统计结论、概率、盈亏或宏观判断，但缺少明细数据、公式代入或计算过程，无法复现或校验。",
    },
]

ALLOWED_EVIDENCE_SOURCES = {
    "question",
    "self_final_answer",
    "competitor_final_answer",
}

ALLOWED_EVIDENCE_POINTERS = {
    "question",
    "self_record.text_answer",
    "self_record.answer",
    "competitor_record.text_answer",
    "competitor_record.answer",
    "normalized.self_final_answer",
    "normalized.competitor_final_answer",
}
