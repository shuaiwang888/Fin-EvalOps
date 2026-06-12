"""
06-compound-intent 评测规则定义 (v5)。

复合意图类问题：用户一句话包含多个子任务，评测重点在拆得准、答得全、证据能支撑。
"""

DIMENSIONS = [
    {
        "key": "intent_decomposition", "label_zh": "意图拆解",
        "description": "评估是否正确拆解了复合意图中的子任务清单。始终考察。",
        "six_level_anchors": {
            0: "完全没有拆解，将复合意图当作单一问题处理",
            20: "只识别了其中一个子任务，遗漏了大部分意图",
            40: "识别了主要子任务但遗漏了次要任务或子任务间依赖关系",
            60: "子任务拆解基本完整，但优先级判断或分解粒度可优化",
            80: "拆解精准完整，子任务清单清晰，优先级正确",
            100: "拆解完美，所有显性和隐性子任务均被识别，依赖关系明确",
        },
    },
    {
        "key": "task_coverage_priority", "label_zh": "子任务覆盖与主次",
        "description": "评估子任务覆盖完整性及主次优先级判断。始终考察。",
        "six_level_anchors": {
            0: "几乎所有子任务都没有被回答",
            20: "仅覆盖了少数次要子任务，核心子任务被忽略",
            40: "核心子任务有涉及但覆盖不全，或主次关系判断偏差较大",
            60: "主要子任务基本覆盖，但个别次要任务遗漏或优先级处理不当",
            80: "所有子任务全覆盖，主次分明，资源分配合理",
            100: "覆盖完美，每个子任务被充分展开，主次权重精确匹配用户意图",
        },
    },
    {
        "key": "multi_source_evidence_integration", "label_zh": "多源证据整合",
        "description": "评估行情/新闻/产业/政策/财务/资金等多源信息的整合质量。",
        "six_level_anchors": {
            0: "完全没有证据整合，纯文字推测",
            20: "仅使用了单一信息源，缺乏多源交叉验证",
            40: "使用了多源信息但没有有效整合，各自为阵",
            60: "多源信息基本整合但对某些关键信息源的权重判断不当",
            80: "多源信息有效整合，相互印证，权重分配合理",
            100: "整合完美，多源信息形成立体证据体系，矛盾信息被解释处理",
        },
    },
    {
        "key": "analysis_chain_closure", "label_zh": "分析链路闭环",
        "description": "评估从事实到影响、传导、策略的分析链路是否完整。始终考察。",
        "six_level_anchors": {
            0: "分析链路完全断裂，事实与结论无关联",
            20: "有分析意图但各个环节严重脱节，结论悬浮",
            40: "部分环节有分析但关键传导环节缺失或逻辑跳跃",
            60: "分析链路基本完整，但个别环节的论证深度不足",
            80: "分析链路完整闭环，各环节逻辑自洽，层层推进",
            100: "分析闭环完美，每个推理步骤有证据，结论有力且无懈可击",
        },
    },
    {
        "key": "data_logic_rigor", "label_zh": "数据与逻辑严谨性",
        "description": "评估计算口径、时间窗口、案例真实性、推演自洽性。",
        "six_level_anchors": {
            0: "数据或逻辑存在致命错误，结论完全不可靠",
            20: "多处数据口径不一致或逻辑矛盾严重",
            40: "有一处关键数据的口径或时间窗口错误，或逻辑不自洽",
            60: "数据和逻辑基本严谨，但个别口径或假设的说明不够清晰",
            80: "数据口径清晰，时间窗口正确，逻辑自洽，案例真实",
            100: "数据与逻辑完美，所有口径/时间窗口/假设明确说明，完全可复现",
        },
    },
    {
        "key": "decision_actionability", "label_zh": "决策表达与可执行性",
        "description": "评估是否给出了可执行的策略/择股/布局/调仓建议。",
        "six_level_anchors": {
            0: "完全没有可执行的决策建议",
            20: "给了模糊的方向但没有具体到可操作的层面",
            40: "有可执行建议但缺少关键的触发条件或执行细节",
            60: "操作建议基本可执行但个别条件或边界不够明确",
            80: "操作建议清晰可执行，触发条件/时机/仓位明确",
            100: "决策建议完美，每项建议有明确执行方案、条件和备选路径",
        },
    },
    {
        "key": "composition_readability", "label_zh": "结构与可读性",
        "description": "评估答案结构是否清晰、可读。始终为辅助维度。",
        "six_level_anchors": {
            0: "结构完全混乱，无法阅读",
            20: "结构松散，信息碎片化，难以找到重点",
            40: "有基本结构但逻辑流不畅，读者需要来回跳跃",
            60: "结构基本清晰但部分段落组织可优化，重点不够突出",
            80: "结构清晰，层次分明，重点突出，易读性好",
            100: "结构完美，逻辑流自然，信息密度和可读性达到最佳平衡",
        },
    },
    {
        "key": "tool_usage", "label_zh": "工具使用合理性",
        "description": "评估工具选择、编排和使用是否合理。始终考察。",
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
        "key": "latency_efficiency", "label_zh": "响应效率",
        "description": "评估复杂问句的响应耗时是否合理。",
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
    "intent_decomposition": 16,
    "task_coverage_priority": 14,
    "multi_source_evidence_integration": 14,
    "analysis_chain_closure": 16,
    "data_logic_rigor": 14,
    "decision_actionability": 10,
    "composition_readability": 5,
    "tool_usage": 7,
    "latency_efficiency": 4,
}

WEIGHT_RULES: list[dict] = []

CAP_RULES = [
    {
        "name": "missed_major_subtask", "label_zh": "遗漏主要子任务",
        "label_tag": "遗漏主要子任务", "severity": "critical", "ceiling": 65,
        "description": "复合问题中的主要子任务被遗漏。",
    },
    {
        "name": "data_or_case_unreliable", "label_zh": "数据或案例不可靠",
        "label_tag": "数据/案例不可靠", "severity": "critical", "ceiling": 55,
        "description": "引用的数据或案例不可靠、编造或错误。",
    },
    {
        "name": "calculation_or_time_window_error", "label_zh": "计算或时间窗口错误",
        "label_tag": "计算/时间窗口错误", "severity": "critical", "ceiling": 55,
        "description": "计算逻辑或时间窗口处理存在实质错误。",
    },
    {
        "name": "information_pile_without_synthesis", "label_zh": "信息堆砌无综合",
        "label_tag": "信息堆砌无综合", "severity": "warning", "ceiling": 60,
        "description": "多源信息被罗列但未整合为综合判断。",
    },
    {
        "name": "missing_required_decision_output", "label_zh": "遗漏必要决策输出",
        "label_tag": "遗漏必要决策输出", "severity": "critical", "ceiling": 65,
        "description": "用户明确要求的策略/建议/决策输出未提供。",
    },
    {
        "name": "wrong_or_shallow_evidence_mix", "label_zh": "证据组合错误或浅层",
        "label_tag": "证据组合错误/浅层", "severity": "warning", "ceiling": 60,
        "description": "多源证据的权重、优先级或相关性判断错误。",
    },
    {
        "name": "severe_latency_without_quality_gain", "label_zh": "严重延迟无质量增益",
        "label_tag": "严重延迟无质量增益", "severity": "warning", "ceiling": 75,
        "description": "响应耗时过长且质量收益不足。",
    },
]

ROOT_CAUSE_TAXONOMY = [
    {"l1": "intent", "l1_zh": "意图拆解", "description": "未正确拆解复合意图、时间窗口、对象或输出要求", "l2": ["decomposition_error", "missed_subtask", "wrong_priority"]},
    {"l1": "coverage", "l1_zh": "子任务覆盖", "description": "子任务漏答、主次错位、展开不足", "l2": ["subtask_omitted", "priority_misplaced", "insufficient_depth"]},
    {"l1": "evidence", "l1_zh": "证据整合", "description": "多源证据浅、错、无关或没有整合", "l2": ["shallow_evidence", "wrong_evidence_source", "no_integration"]},
    {"l1": "tool", "l1_zh": "工具编排", "description": "工具选择、输入、读取或编排问题", "l2": ["wrong_tool_selection", "insufficient_tool_chain", "tool_output_misread"]},
    {"l1": "data_logic", "l1_zh": "数据逻辑", "description": "计算口径、时间窗口、案例真实性、推演自洽性问题", "l2": ["calculation_error", "time_window_error", "case_unreliable"]},
    {"l1": "reasoning", "l1_zh": "推理闭环", "description": "事实到影响、传导、策略没有闭环", "l2": ["weak_causal_chain", "missing_synthesis", "no_actionable_conclusion"]},
    {"l1": "composition", "l1_zh": "答案组织", "description": "结构混乱、信息拼盘、结论不凝练", "l2": ["disorganized", "info_pile", "unclear_conclusion"]},
    {"l1": "latency", "l1_zh": "响应延迟", "description": "耗时过长且质量收益不足", "l2": ["slow_response", "inefficient_tool_chain"]},
]

ROOT_CAUSE_DIM_MAP = {
    "intent_decomposition": "intent",
    "task_coverage_priority": "coverage",
    "multi_source_evidence_integration": "evidence",
    "analysis_chain_closure": "reasoning",
    "data_logic_rigor": "data_logic",
    "decision_actionability": "reasoning",
    "composition_readability": "composition",
    "tool_usage": "tool",
    "latency_efficiency": "latency",
}


