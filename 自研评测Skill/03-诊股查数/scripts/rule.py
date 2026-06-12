"""
03-stock-diagnosis-and-data-lookup 评测规则定义 (v5)。

诊股查数类问题：评估模型在个股诊断、数据查询、计算对比和市场分析框架匹配方面的表现。
"""

DIMENSIONS = [
    {
        "key": "intent_fulfillment", "label_zh": "意图满足度",
        "description": "评估答案是否完整、准确地满足了用户的诊股/查数意图。始终考察。",
        "six_level_anchors": {
            0: "完全未响应用户意图，答案与问题无关或直接拒答",
            20: "仅触及意图的某个边角，遗漏了用户的核心诊股/查数需求",
            40: "部分满足意图但关键需求缺失或偏差较大",
            60: "基本满足意图，有可改进的明显不足但方向正确",
            80: "很好地满足意图，数据完整、框架匹配，仅有极轻微遗漏",
            100: "完美满足意图，所有显性和隐性需求均被覆盖，无任何可挑剔之处",
        },
    },
    {
        "key": "data_accuracy_coverage", "label_zh": "数据准确性与覆盖",
        "description": "评估答案的数据值、样本、标的、年份和字段覆盖是否准确完整。始终考察。",
        "six_level_anchors": {
            0: "核心数据完全错误或编造",
            20: "关键数据出现实质性错误，遗漏主要标的或年份",
            40: "数据大致可接受但有明显缺失或部分字段错误",
            60: "关键数据正确，但个别字段或样本覆盖不够全面",
            80: "数据准确，覆盖全面，字段选择恰当",
            100: "数据完美准确，所有相关标的、年份、字段全覆盖，可复核",
        },
    },
    {
        "key": "time_caliber_precision", "label_zh": "时间、口径与粒度",
        "description": "评估答案是否严格处理时间窗口、数据口径和粒度。",
        "six_level_anchors": {
            0: "完全无视时间或口径要求",
            20: "时间窗口或口径出现严重影响结论的错误",
            40: "时间或口径有大方向但部分细节偏差较大",
            60: "时间和口径基本正确，个别粒度和复权/单位细节可优化",
            80: "时间窗口精确，口径清晰，粒度匹配用户需求",
            100: "时间、口径、粒度完美精确，所有细节（复权、汇率、单位、交易日）处理到位",
        },
    },
    {
        "key": "calculation_comparison", "label_zh": "计算与对比",
        "description": "评估涨跌幅、差值、总额、比价、排序、换算或多标的对比的正确性。",
        "six_level_anchors": {
            0: "计算完全错误或用户要求计算/对比但未提供",
            20: "计算方向正确但数值有实质性错误",
            40: "计算有结果但方法、口径或对比维度有偏差",
            60: "计算基本正确但呈现不够清晰或缺少关键对比维度",
            80: "计算准确，对比维度清晰，呈现易读",
            100: "计算完美精确，对比维度全面，逻辑自洽且可复现",
        },
    },
    {
        "key": "analysis_framework_fit", "label_zh": "市场分析框架匹配度",
        "description": "评估答案使用的分析框架是否与用户问的诊股/市场问题匹配。",
        "six_level_anchors": {
            0: "分析框架完全错误或不适用",
            20: "套用了无关的分析框架，方向根本不对",
            40: "框架大致可接受但与问题的最优分析维度存在明显偏差",
            60: "框架基本匹配，但部分分析维度的选择可优化",
            80: "分析框架与问题类型高度匹配，维度选择准确",
            100: "分析框架完美匹配，且创造性地组合多个维度以达最优分析效果",
        },
    },
    {
        "key": "insight_extension", "label_zh": "延伸洞察与增量信息",
        "description": "评估答案是否在取数基础上给出了诊断、解释、对比或投资含义。",
        "six_level_anchors": {
            0: "完全没有洞察，仅做了最基本的取数罗列",
            20: "仅有少量额外信息但缺乏实质分析",
            40: "有延伸意图但深度不足，或关键洞察方向缺失",
            60: "给出了基本的延伸洞察，但可进一步展开关键方向",
            80: "延伸洞察有价值，抓住了核心诊断逻辑和关键增量信息",
            100: "洞察深刻，在取数基础上给出了差异化判断和清晰的下一步行动指引",
        },
    },
    {
        "key": "result_verifiability", "label_zh": "结果可验证性",
        "description": "评估答案的结果是否可以被复核验证。",
        "six_level_anchors": {
            0: "结果完全不可验证，没有引用任何数据来源",
            20: "仅给出了结论性判断，缺少支撑数据和来源",
            40: "有部分数据但缺少足够的明细使读者可自行复核",
            60: "结果基本可验证，但个别数据的追溯路径不够清晰",
            80: "结果可验证性好，数据来源明确，明细可追溯",
            100: "结果完全可验证，每一步计算和数据来源均可独立复核",
        },
    },
    {
        "key": "presentation_visualization", "label_zh": "呈现与可视化",
        "description": "评估答案的呈现方式是否清晰、易读，图表是否恰当。",
        "six_level_anchors": {
            0: "呈现完全混乱，无法阅读",
            20: "结构松散，信息碎片化，或图表严重误导",
            40: "有基本结构但逻辑流不畅，或图表与内容脱节",
            60: "呈现基本清晰但部分组织可优化，图表基本可用",
            80: "结构清晰，层次分明，图表与文字配合良好",
            100: "呈现完美，信息密度和可读性达到最佳平衡，图表精准有力",
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
    {
        "key": "latency_efficiency", "label_zh": "响应耗时与执行效率",
        "description": "评估响应耗时是否合理。仅在耗时数据可用且异常时主要考察。",
        "six_level_anchors": {
            0: "耗时严重超时或系统无法完成",
            20: "耗时远超出合理范围，存在明显的效率问题",
            40: "耗时偏长，有可优化的冗余步骤或重复调用",
            60: "耗时基本合理，但个别环节可以更高效",
            80: "耗时合理，调用链路高效",
            100: "耗时最优，以最少步骤和最短等待完成了全部需求",
        },
    },
]

DEFAULT_WEIGHTS = {
    "intent_fulfillment": 12,
    "data_accuracy_coverage": 18,
    "time_caliber_precision": 12,
    "calculation_comparison": 10,
    "analysis_framework_fit": 16,
    "insight_extension": 10,
    "result_verifiability": 8,
    "presentation_visualization": 5,
    "tool_usage": 6,
    "latency_efficiency": 3,
}

WEIGHT_RULES: list[dict] = []

CAP_RULES = [
    {
        "name": "hard_data_or_fact_error", "label_zh": "硬性数据或事实错误",
        "label_tag": "硬性数据/事实错误", "severity": "critical", "ceiling": 35,
        "description": "关键数据值、标的名、日期或基础事实有实质性错误，打破结论可信度。",
    },
    {
        "name": "missing_required_data", "label_zh": "遗漏必要数据",
        "label_tag": "遗漏必要数据", "severity": "critical", "ceiling": 60,
        "description": "用户明确要求的数据项或字段未提供，导致诊断/查询不完整。",
    },
    {
        "name": "time_or_caliber_error", "label_zh": "时间或口径错误",
        "label_tag": "时间/口径错误", "severity": "critical", "ceiling": 45,
        "description": "时间窗口、数据口径、复权、单位或粒度出现实质错误。",
    },
    {
        "name": "intraday_precision_missing", "label_zh": "盘中精度缺失",
        "label_tag": "盘中精度缺失", "severity": "warning", "ceiling": 55,
        "description": "涉及分时、盘中、实时行情但未提供对应精度的数据。",
    },
    {
        "name": "wrong_analysis_framework", "label_zh": "分析框架错误",
        "label_tag": "分析框架错误", "severity": "critical", "ceiling": 55,
        "description": "使用的市场分析框架与用户问题类型不匹配，导致判断偏差。",
    },
    {
        "name": "data_dump_without_insight", "label_zh": "数据堆砌无洞察",
        "label_tag": "数据堆砌无洞察", "severity": "warning", "ceiling": 65,
        "description": "答案主要输出数据罗列，没有给出诊断、解释或投资含义。",
    },
    {
        "name": "unverifiable_or_fabricated_result", "label_zh": "不可验证或编造结果",
        "label_tag": "不可验证/编造结果", "severity": "critical", "ceiling": 50,
        "description": "结论无法从公开数据中验证，或明显编造了不存在的统计结果。",
    },
]

ROOT_CAUSE_TAXONOMY = [
    {"l1": "intent", "l1_zh": "理解问题", "description": "是否识别用户的真实诊股/查数需求和隐含分析任务", "l2": ["intent_misjudged", "missing_implicit_task", "wrong_output_form"]},
    {"l1": "evidence", "l1_zh": "检索数据", "description": "获取的数据是否正确、完整、时效对、口径匹配", "l2": ["missing_required_data", "outdated_data", "wrong_caliber_or_field"]},
    {"l1": "tool", "l1_zh": "选择与执行工具", "description": "是否选对工具、写对参数、用足链路", "l2": ["wrong_tool_selection", "insufficient_tool_chain", "tool_param_error"]},
    {"l1": "reasoning", "l1_zh": "计算与诊断推理", "description": "计算是否正确、框架是否匹配、诊断是否有逻辑", "l2": ["calculation_error", "wrong_analysis_framework", "no_insight_extension"]},
    {"l1": "composition", "l1_zh": "组织答案", "description": "逻辑可能存在但答案是否清晰地呈现出来", "l2": ["data_dump", "unclear_structure", "missing_verifiability"]},
]

ROOT_CAUSE_DIM_MAP = {
    "intent_fulfillment": "intent",
    "data_accuracy_coverage": "evidence",
    "time_caliber_precision": "evidence",
    "calculation_comparison": "reasoning",
    "analysis_framework_fit": "reasoning",
    "insight_extension": "reasoning",
    "result_verifiability": "composition",
    "presentation_visualization": "composition",
    "tool_usage": "tool",
    "latency_efficiency": "tool",
}

CONFIDENCE_THRESHOLD = 3
