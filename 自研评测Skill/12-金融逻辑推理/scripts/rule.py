"""
12-financial-logical-reasoning 评测规则定义 (v5)。

金融逻辑推理类问题：评估模型在投资逻辑链、市场驱动识别、证据到结论连接方面的表现。
"""

DIMENSIONS = [
    {
        "key": "financial_logic_chain", "label_zh": "金融逻辑链完整性",
        "description": "评估是否形成从事实到结论的闭环。始终考察。",
        "six_level_anchors": {
            0: "完全无金融推理、严重误导或给出无依据确定性承诺",
            20: "结论与证据大幅脱节，或使用明显错误的筛选逻辑",
            40: "主要靠指标罗列或模板化分析，关键驱动缺失",
            60: "方向部分正确，但推理链有断点，证据和结论连接一般",
            80: "主逻辑正确，少量证据、风险或表达不够充分",
            100: "逻辑链完整，驱动识别准确，证据充分支撑结论，有排序/情景/风险和可执行建议",
        },
    },
    {
        "key": "market_driver_identification", "label_zh": "市场驱动识别",
        "description": "评估是否准确识别热点、催化或价格驱动因素。",
        "six_level_anchors": {
            0: "完全未识别任何市场驱动因素",
            20: "关键市场驱动遗漏，导致分析方向根本错误",
            40: "识别到部分驱动但主驱动缺失或方向偏差",
            60: "主要驱动基本识别，但个别催化因素分析不够深入",
            80: "市场驱动识别准确，热点和催化分析到位",
            100: "市场驱动完美识别，所有核心催化和情绪因素均被覆盖",
        },
    },
    {
        "key": "evidence_to_conclusion", "label_zh": "证据到结论连接",
        "description": "评估数据、新闻、公告、资金是否充分支撑结论。始终考察。",
        "six_level_anchors": {
            0: "结论完全无证据支撑或证据与结论矛盾",
            20: "关键结论缺少证据，或使用了明显不相关的数据",
            40: "有部分证据但连接不紧密，存在逻辑跳跃",
            60: "证据基本支撑结论，但个别连接不够紧密",
            80: "证据充分，与结论连接清晰，逻辑自洽",
            100: "每一个结论都有精准证据支撑，证据链完整可追溯",
        },
    },
    {
        "key": "comparison_and_ranking", "label_zh": "个股比较与排序",
        "description": "评估多股选择、推荐、排序是否有统一比较标准和依据。",
        "six_level_anchors": {
            0: "完全未做比较或排序依据错误",
            20: "有比较但无统一标准，或排序逻辑严重混乱",
            40: "比较方向大致正确但标准不统一或维度缺失",
            60: "比较基本合理但个别标准或维度不够清晰",
            80: "比较标准统一，排序依据清晰，维度选择合理",
            100: "比较完美，标准统一可复现，所有关键维度覆盖，排序自洽",
        },
    },
    {
        "key": "scenario_risk_reasoning", "label_zh": "情景与风险推演",
        "description": "评估是否给出多情景分析和风险考量。",
        "six_level_anchors": {
            0: "完全没有风险或情景考量",
            20: "对高风险建议完全无风险提示",
            40: "有基本的风险提及但缺少具体情景推演",
            60: "给出了基本风险考量但情景分析不够全面",
            80: "情景分析到位，风险考量充分，有明确的触发条件",
            100: "多情景推演完整，风险量化清晰，有明确的应对策略和验证节点",
        },
    },
    {
        "key": "decision_value_expression", "label_zh": "决策价值表达",
        "description": "评估答案是否有可执行的决策参考价值。",
        "six_level_anchors": {
            0: "答案无任何决策参考价值",
            20: "表达模糊，用户无法基于答案做任何判断",
            40: "有基本方向但缺少可执行的具体判断",
            60: "给出了基本判断但可执行细节不足",
            80: "决策参考清晰，有可执行的判断和建议",
            100: "决策价值极高，判断明确、可执行、有验证路径",
        },
    },
    {
        "key": "tool_usage", "label_zh": "工具使用合理性",
        "description": "评估工具选择、调用参数和链路效率。始终考察。",
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
    "financial_logic_chain": 25,
    "market_driver_identification": 20,
    "evidence_to_conclusion": 20,
    "comparison_and_ranking": 15,
    "scenario_risk_reasoning": 10,
    "decision_value_expression": 5,
    "tool_usage": 5,
}

WEIGHT_RULES: list[dict] = []

CAP_RULES = [
    {
        "name": "unsupported_prediction_or_recommendation", "label_zh": "无支撑预测或推荐",
        "label_tag": "无支撑预测/推荐", "severity": "critical", "ceiling": 45,
        "description": "对涨停、走势、买卖给出强结论但缺少证据和风险。",
    },
    {
        "name": "wrong_core_investment_logic", "label_zh": "核心投资逻辑错误",
        "label_tag": "核心投资逻辑错误", "severity": "critical", "ceiling": 50,
        "description": "核心筛选逻辑违背金融常识，如把负PE当便宜潜力。",
    },
    {
        "name": "market_driver_missing", "label_zh": "市场驱动缺失",
        "label_tag": "市场驱动缺失", "severity": "critical", "ceiling": 55,
        "description": "短线/热点题遗漏主要市场驱动，只看静态指标。",
    },
    {
        "name": "data_dump_without_reasoning", "label_zh": "数据堆砌无推导",
        "label_tag": "数据堆砌无推导", "severity": "warning", "ceiling": 55,
        "description": "大量技术面/资金面/基本面堆砌但没有推导。",
    },
    {
        "name": "comparison_without_standard", "label_zh": "比较无统一标准",
        "label_tag": "比较无统一标准", "severity": "warning", "ceiling": 60,
        "description": "多股选择没有统一比较标准或排序依据。",
    },
    {
        "name": "risk_scenario_missing_for_high_risk_advice", "label_zh": "高风险建议缺风险情景",
        "label_tag": "高风险建议缺风险情景", "severity": "warning", "ceiling": 65,
        "description": "追高、明日涨停、下周走势等高风险建议没有风险情景。",
    },
]

ROOT_CAUSE_TAXONOMY = [
    {"l1": "intent", "l1_zh": "理解问题", "description": "是否识别用户的决策任务类型和时间范围", "l2": ["decision_task_misidentified", "time_horizon_misread", "comparison_scope_misjudged"]},
    {"l1": "evidence", "l1_zh": "检索数据", "description": "获取的数据是否支撑投资推理", "l2": ["missing_key_driver_evidence", "insufficient_comparison_data", "outdated_market_data"]},
    {"l1": "tool", "l1_zh": "选择与执行工具", "description": "是否选对工具、写对参数", "l2": ["wrong_tool_selection", "insufficient_tool_chain", "tool_param_error"]},
    {"l1": "reasoning", "l1_zh": "投资逻辑推导", "description": "逻辑链是否完整、驱动识别是否准确", "l2": ["broken_logic_chain", "wrong_investment_logic", "missing_risk_scenario", "no_comparison_standard"]},
    {"l1": "composition", "l1_zh": "组织答案", "description": "答案是否清晰呈现推理和判断", "l2": ["data_dump_without_synthesis", "unclear_decision_path", "missing_actionable_output"]},
]

ROOT_CAUSE_DIM_MAP = {
    "financial_logic_chain": "reasoning",
    "market_driver_identification": "reasoning",
    "evidence_to_conclusion": "evidence",
    "comparison_and_ranking": "reasoning",
    "scenario_risk_reasoning": "reasoning",
    "decision_value_expression": "composition",
    "tool_usage": "tool",
}

CONFIDENCE_THRESHOLD = 3
