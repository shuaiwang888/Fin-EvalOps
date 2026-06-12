"""
03-stock-diagnosis-and-data-lookup result-only 自研 vs 竞品评测规则定义。

该比较 skill 只定义诊股查数领域的最终回答质量维度、默认权重和质量标签。
pairwise 比较字段由输出 schema 约束。
"""

DIMENSIONS = [
    {
        "key": "intent_fulfillment",
        "label_zh": "意图满足度",
        "description": "评估最终回答是否回答用户真正要问的诊股/查数问题。",
        "six_level_anchors": {
            0: "完全未响应用户的诊股/查数意图，答案与问题无关或直接拒答",
            20: "仅触及意图的某个边角，严重偏离了用户核心需求，只给出了表层或无关信息",
            40: "部分满足了意图，但关键诊股/查数需求缺失或存在实质性偏差",
            60: "基本满足用户意图，方向正确，但存在可改进的明显不足",
            80: "很好地满足用户意图，数据、框架、口径完整，仅有极轻微遗漏",
            100: "完美满足用户意图，显性和隐性需求均被覆盖，无任何可挑剔之处",
        },
    },
    {
        "key": "data_accuracy_coverage",
        "label_zh": "数据准确性与覆盖",
        "description": "评估最终回答中的数据值、样本、标的、年份和字段覆盖是否准确完整。",
        "six_level_anchors": {
            0: "完全没有给出需要的数据，或给出的数据完全错误",
            20: "给出了少量相关数据，但核心字段/标的/年份严重缺失，或数据口径明显错误",
            40: "覆盖了主要数据，但遗漏重要维度、标的或筛选条件使用有误",
            60: "数据覆盖基本完整，正确性良好，但个别字段或样本精度不足",
            80: "数据准确完整，字段齐全，标的和年份覆盖充分，筛选条件精确",
            100: "数据完美，所有维度全覆盖，筛选条件精确无误，数据可复现",
        },
    },
    {
        "key": "time_caliber_precision",
        "label_zh": "时间、口径与粒度",
        "description": "评估最终回答中的日期、过去 N 年、上市以来、分时、合约、汇率、单位、复权、交易日等口径是否正确。",
        "six_level_anchors": {
            0: "时间/口径完全错误，使用了完全错误的时间范围或单位/复权口径",
            20: "时间方向正确但具体日期/口径存在严重偏差，或遗漏了关键口径调整",
            40: "时间/口径方向正确但精度不足，或忽略了交易日/复权/合约等关键口径",
            60: "时间/口径基本正确，但个别边界日期或复权/单位处理不够精确",
            80: "时间/口径准确，交易日/复权/合约/单位/汇率均正确处理",
            100: "时间/口径完美，所有日期边界精确，复权/合约/单位/汇率全部正确无误",
        },
    },
    {
        "key": "calculation_comparison",
        "label_zh": "计算与对比",
        "description": "评估最终回答中的涨跌幅、差值、总额、比价、跑赢、排序、换算或多标的对比是否正确。",
        "six_level_anchors": {
            0: "计算/对比完全错误或使用了错误的公式/方法",
            20: "计算方向正确但核心结果存在实质性错误",
            40: "主要计算正确，但个别指标的计算方法或对比口径有误",
            60: "计算/对比基本正确，但精度或中间步骤有轻微瑕疵",
            80: "计算/对比完全正确，方法得当，结果精确",
            100: "计算/对比完美，方法最优，精度最高，中间步骤可验证",
        },
    },
    {
        "key": "analysis_framework_fit",
        "label_zh": "市场分析框架匹配度",
        "description": "评估主力、筹码、增长点、止盈位、客户、商品比价、行业跑赢、诊股类问题的分析框架是否匹配。",
        "six_level_anchors": {
            0: "完全没有使用市场认可的分析框架，或框架选择完全错误",
            20: "尝试使用了分析框架，但与问题场景严重不匹配，或框架理解有根本性错误",
            40: "使用了基本正确的框架大类，但框架应用层次过浅，遗漏了关键分析维度",
            60: "框架选择基本匹配，分析方向正确，但框架运用不够深入或缺少交叉验证",
            80: "框架选择恰当，分析维度合理，框架运用到位，仅轻微不足",
            100: "框架完美匹配市场语义，分析维度全面深入，框架运用精准且可复现",
        },
    },
    {
        "key": "insight_extension",
        "label_zh": "延伸洞察与增量信息",
        "description": "评估诊断、解释、对比、未来增长点或投资含义是否有增量价值。",
        "six_level_anchors": {
            0: "完全没有提供任何增量洞察，仅重复原始数据或问题",
            20: "提供了少量增量信息，但基本是无关扩展或信息增量极低",
            40: "有一定增量洞察，但深度不足或关键解释缺失",
            60: "提供了有用的增量分析，但洞察深度或证据支撑可以更充分",
            80: "增量洞察有实质性价值，解释清晰，证据支撑充分",
            100: "洞察力强，发现用户未明确问及但高度相关的关键点，证据链完整且可操作",
        },
    },
    {
        "key": "result_verifiability",
        "label_zh": "结果可验证性",
        "description": "评估最终回答中的统计、全市场筛选、历史序列、非公开/搜索补充、复杂判断是否可复核。",
        "six_level_anchors": {
            0: "结果完全无法验证，无任何中间数据、来源或计算过程",
            20: "给出了最终结果，但中间数据/来源几乎不可追溯",
            40: "部分中间信息可追溯，但关键步骤缺失或数据来源不明确",
            60: "主要结果可验证，但个别中间数据或计算环节不够透明",
            80: "结果可验证，数据来源清晰，计算过程可追溯",
            100: "结果完全可复现，每一步都有明确的数据来源和计算过程",
        },
    },
    {
        "key": "presentation_visualization",
        "label_zh": "呈现与可视化",
        "description": "评估最终回答中的多年份、多标的、趋势对比、图表等呈现是否提升理解。",
        "six_level_anchors": {
            0: "呈现完全混乱，无法从展示中提取任何有效信息",
            20: "呈现方式影响了信息理解，关键信息被淹没或缺失",
            40: "呈现基本可用但结构性差，或使用了图表但没有解释结论",
            60: "呈现清晰，但格式或可视化可优化，或缺少必要的图表解释",
            80: "呈现清晰准确，结构合理，可视化有效支撑理解",
            100: "呈现完美，简洁有力，可视化恰到好处且附有完整解释",
        },
    },
]

DEFAULT_WEIGHTS = {
    "intent_fulfillment": 12,
    "data_accuracy_coverage": 20,
    "time_caliber_precision": 13,
    "calculation_comparison": 11,
    "analysis_framework_fit": 18,
    "insight_extension": 11,
    "result_verifiability": 10,
    "presentation_visualization": 5,
}

WEIGHT_RULES: list[dict] = []

CAP_RULES = [
    {
        "name": "hard_data_or_fact_error",
        "label_zh": "硬性数据/事实错误",
        "label_tag": "硬性数据/事实错误",
        "severity": "critical",
        "ceiling": 35,
        "score_effect": "tag_only",
        "description": "最终回答中的核心数据值、标的、行业、客户、分红事件、价格、涨跌幅或宏观指标明显错误。",
    },
    {
        "name": "missing_required_data",
        "label_zh": "必要数据缺失",
        "label_tag": "必要数据缺失",
        "severity": "warning",
        "ceiling": 60,
        "score_effect": "tag_only",
        "description": "最终回答遗漏用户明确要求的关键数据，或历史序列/全市场筛选/多标的样本明显不全。",
    },
    {
        "name": "time_or_caliber_error",
        "label_zh": "时间/口径错误",
        "label_tag": "时间/口径错误",
        "severity": "critical",
        "ceiling": 45,
        "score_effect": "tag_only",
        "description": "最终回答中的交易日、年份、日期、复权、单位、合约、汇率、行业分类等核心口径错误。",
    },
    {
        "name": "intraday_precision_missing",
        "label_zh": "日内精度缺失",
        "label_tag": "日内精度缺失",
        "severity": "warning",
        "ceiling": 55,
        "score_effect": "tag_only",
        "description": "用户明确要求日内精度，但最终回答只使用日线、收盘价、开盘价等粗粒度数据。",
    },
    {
        "name": "wrong_analysis_framework",
        "label_zh": "分析框架错误",
        "label_tag": "分析框架错误",
        "severity": "critical",
        "ceiling": 55,
        "score_effect": "tag_only",
        "description": "最终回答采用明显不符合市场习惯的诊断框架，导致答案虽有数据但用户难以使用。",
    },
    {
        "name": "data_dump_without_insight",
        "label_zh": "数据堆砌无洞察",
        "label_tag": "数据堆砌无洞察",
        "severity": "warning",
        "ceiling": 65,
        "score_effect": "tag_only",
        "description": "对诊断、对比或解释题，最终回答只堆砌数据表，没有结论、差异、原因或观察点。",
    },
    {
        "name": "unverifiable_or_fabricated_result",
        "label_zh": "不可验证或疑似编造",
        "label_tag": "不可验证或疑似编造",
        "severity": "critical",
        "ceiling": 50,
        "score_effect": "tag_only",
        "description": "最终回答给出精确统计、筛选结果、客户名单、增长点、主力判断或行业排名，但没有可定位证据、明细、来源或计算过程。",
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
