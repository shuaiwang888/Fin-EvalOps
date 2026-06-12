"""
02-backtesting-data-extraction-and-calculation-self-vs-competitor 评测规则定义。

该比较 skill 复用原 02 skill 的绝对评分维度、默认权重、封顶标签和根因体系；
pairwise 比较字段由 references/output-schema_zh.md 约束。
"""

DIMENSIONS = [
    {
        "key": "intent_fulfillment", "label_zh": "意图满足度",
        "description": "评估答案是否完整、准确地满足了用户的取数计算需求。始终考察。",
        "six_level_anchors": {
            0: "完全未响应用户的取数计算需求",
            20: "仅给出无关信息或极度不完整的回答，核心计算需求未满足",
            40: "部分满足但遗漏了关键数据/计算步骤，或理解有实质性偏差",
            60: "基本满足需求，但有明显可改进之处（如精度不足、个别指标遗漏）",
            80: "很好地满足需求，数据完整、计算准确，仅有极小瑕疵",
            100: "完美满足，数据全覆盖、计算精确、展示清晰，无任何可挑剔之处",
        },
    },
    {
        "key": "data_retrieval_accuracy", "label_zh": "取数准确性",
        "description": "评估数据获取的正确性和覆盖完整性。所有取数计算题目均需考察。",
        "six_level_anchors": {
            0: "完全没有取到需要的数据，或取到的数据完全错误",
            20: "取到了少量相关数据但核心字段缺失严重，或数据源选择错误",
            40: "覆盖了主要数据但遗漏了重要维度或筛选条件使用有误",
            60: "数据覆盖基本完整，正确性良好，但个别字段或筛选精度不足",
            80: "数据获取准确完整，字段齐全，筛选条件精确",
            100: "数据获取完美，所有维度全覆盖，筛选条件精确无误，数据可复现",
        },
    },
    {
        "key": "time_inference", "label_zh": "时间推理正确性",
        "description": "评估日期/交易日/节假日倒推/时间范围推理是否正确。",
        "six_level_anchors": {
            0: "时间推理完全错误，使用了完全错误的时间范围",
            20: "时间方向正确但具体日期/窗口存在严重偏差",
            40: "时间推理方向正确但精度不足，或遗漏了交易日/节假日调整",
            60: "时间推理基本正确，但个别边界日期或节假日处理不够精确",
            80: "时间推理准确，交易日/节假日/倒推逻辑均正确处理",
            100: "时间推理完美，所有日期边界精确，节假日/交易日/复权日期全部正确处理",
        },
    },
    {
        "key": "calculation_accuracy", "label_zh": "计算准确性",
        "description": "评估涨跌幅/概率/盈亏/衍生指标等计算是否正确。",
        "six_level_anchors": {
            0: "计算完全错误或使用了错误的公式",
            20: "计算方向正确但核心结果存在实质错误",
            40: "主要计算正确但有个别指标的计算方法或口径有误",
            60: "计算基本正确，但精度或中间步骤有轻微瑕疵",
            80: "计算完全正确，方法得当，结果精确",
            100: "计算完美，方法最优，精度最高，中间步骤可验证",
        },
    },
    {
        "key": "logical_decomposition", "label_zh": "逻辑拆解能力",
        "description": "评估多步/多条件复合查询的拆解是否合理。",
        "six_level_anchors": {
            0: "完全没有拆解，将复杂任务当作简单查询处理",
            20: "尝试了拆解但拆解方式与问题核心逻辑不匹配",
            40: "拆解方向正确但步骤遗漏或顺序不当，影响计算效率或准确性",
            60: "拆解基本合理，但部分步骤可有更优的拆解方式",
            80: "拆解逻辑清晰，步骤合理，依赖关系正确",
            100: "拆解完美，最优步骤分解，依赖关系清晰，每一步都有明确目的",
        },
    },
    {
        "key": "result_verifiability", "label_zh": "结果可验证性",
        "description": "评估输出结果是否可被复现和验证。",
        "six_level_anchors": {
            0: "结果完全无法验证，无任何中间数据或计算过程",
            20: "给出了最终结果但中间步骤/数据来源几乎不可追溯",
            40: "部分中间信息可追溯但关键步骤缺失或数据来源不明确",
            60: "主要结果可验证，但个别中间数据或计算环节不够透明",
            80: "结果可验证，数据来源清晰，计算过程可追溯",
            100: "结果完全可复现，每一步都有明确的数据来源和计算过程",
        },
    },
    {
        "key": "expression_quality", "label_zh": "表达与展示质量",
        "description": "评估答案的表达是否清晰、准确。始终为辅助维度。",
        "six_level_anchors": {
            0: "表达混乱，无法理解输出内容",
            20: "表达模糊，信息碎片化，难以提取有效结论",
            40: "表达基本可读但结构性差，关键信息被淹没",
            60: "表达清晰但格式或层次可优化，数据展示不够直观",
            80: "表达清晰准确，结构合理，数据展示直观",
            100: "表达完美，简洁有力，结构一目了然，可视化恰到好处",
        },
    },
    {
        "key": "tool_usage", "label_zh": "工具使用合理性",
        "description": "评估工具选择和使用是否合理、高效。",
        "six_level_anchors": {
            0: "工具完全未使用而应该使用，或每次调用都产生了错误结果",
            20: "工具选择明显错误，或关键步骤本该使用工具但未使用",
            40: "工具选择基本合理但调用参数有误或遗漏了必要的交叉验证",
            60: "工具使用合理但效率不高，或有个别冗余调用",
            80: "工具选择精准，调用高效，交叉验证到位",
            100: "工具使用完美，最小化调用次数达到最大信息覆盖，参数精确",
        },
    },
]

DEFAULT_WEIGHTS = {
    "intent_fulfillment": 13,
    "data_retrieval_accuracy": 20,
    "time_inference": 15,
    "calculation_accuracy": 15,
    "logical_decomposition": 10,
    "result_verifiability": 10,
    "expression_quality": 7,
    "tool_usage": 10,
}

WEIGHT_RULES: list[dict] = []

CAP_RULES = [
    {
        "name": "data_fabrication", "label_zh": "数据编造",
        "label_tag": "数据编造", "severity": "critical", "ceiling": 35,
        "description": "答案包含编造或虚构的数据。",
    },
    {
        "name": "time_inference_error", "label_zh": "时间推理错误",
        "label_tag": "时间推理错误", "severity": "critical", "ceiling": 45,
        "description": "日期/交易日/时间范围推理存在实质性错误。",
    },
    {
        "name": "calculation_logic_error", "label_zh": "计算逻辑错误",
        "label_tag": "计算逻辑错误", "severity": "critical", "ceiling": 50,
        "description": "公式选择、算术运算或衍生指标计算存在逻辑错误。",
    },
    {
        "name": "intraday_precision_missing", "label_zh": "盘中精度缺失",
        "label_tag": "盘中精度缺失", "severity": "warning", "ceiling": 55,
        "description": "需要盘中数据精度但未提供。",
    },
    {
        "name": "missing_required_data", "label_zh": "遗漏必要数据",
        "label_tag": "遗漏必要数据", "severity": "warning", "ceiling": 60,
        "description": "用户明确要求的数据维度/字段未覆盖。",
    },
    {
        "name": "unverifiable_result", "label_zh": "结果不可验证",
        "label_tag": "结果不可验证", "severity": "warning", "ceiling": 65,
        "description": "输出结果缺少明细数据，无法被复现或验证。",
    },
]

ROOT_CAUSE_TAXONOMY = [
    {"l1": "intent", "l1_zh": "理解问题", "description": "系统是否正确理解了用户的取数计算需求？", "l2": ["intent_misjudged", "sub_question_omitted"]},
    {"l1": "evidence", "l1_zh": "检索数据", "description": "系统获取的数据是否正确、完整、时效对？", "l2": ["insufficient_data", "wrong_data_source", "outdated_data"]},
    {"l1": "tool", "l1_zh": "选择与执行工具", "description": "系统是否选对了工具、用对了工具？", "l2": ["wrong_tool_selection", "wrong_tool_params", "inefficient_tool_chain"]},
    {"l1": "reasoning", "l1_zh": "计算与推理", "description": "公式选择、算术运算、多步拆解、时间推理是否正确？", "l2": ["calculation_error", "time_inference_error", "logic_decomposition_error"]},
    {"l1": "composition", "l1_zh": "组织答案", "description": "逻辑可能存在但答案是否呈现出来了？", "l2": ["unclear_structure", "missing_detail", "data_presentation_poor"]},
]

ROOT_CAUSE_DIM_MAP = {
    "intent_fulfillment": "intent",
    "data_retrieval_accuracy": "evidence",
    "time_inference": "reasoning",
    "calculation_accuracy": "reasoning",
    "logical_decomposition": "reasoning",
    "result_verifiability": "composition",
    "expression_quality": "composition",
    "tool_usage": "tool",
}


