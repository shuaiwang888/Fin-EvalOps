"""
8_consultation-and-qa self-judge rule definitions (v1).

The evaluator LLM emits raw_score values and evidence. Caller-side scoring code
can use this module for dimensions, default weights, cap metadata, and root-cause
taxonomy.
"""

DIMENSIONS = [
    {
        "key": "intent_fulfillment",
        "label_zh": "意图满足度",
        "description": "评估答案是否覆盖用户显性问题和隐含的影响、判断、标的或可持续性诉求。",
        "six_level_anchors": {
            0: "完全跑题或拒答",
            20: "只触及边角，核心意图大部分缺失",
            40: "回答了表面问题，但遗漏关键子问题或隐含投资诉求",
            60: "基本回答问题，但深度、完整性或落地性不足",
            80: "显性和主要隐含诉求均覆盖，结构清楚",
            100: "完整覆盖问题、背景、判断、影响和可执行结论",
        },
    },
    {
        "key": "timeliness_fact_boundary",
        "label_zh": "时效性与事实边界",
        "description": "评估答案是否严格遵守时间范围、事实边界、数据口径和事件进展。",
        "six_level_anchors": {
            0: "时间范围完全错误，或关键事实错误导致结论不可用",
            20: "大量旧信息、未来口径或未经核验信息混入",
            40: "有时效意识，但关键时间点、年份、数据口径或进展状态不准",
            60: "大体符合时间要求，但个别日期、口径或进展说明不清",
            80: "时间线清楚，事实边界可靠，能区分已发生、即将发生和传闻",
            100: "精确匹配时间窗口，所有关键事实可核验且边界审慎",
        },
    },
    {
        "key": "fact_evidence_quality",
        "label_zh": "事实证据质量",
        "description": "评估事实、数据口径、来源类型和证据链是否可靠。",
        "six_level_anchors": {
            0: "关键事实大量错误或无证据编造",
            20: "证据极弱，主要依赖笼统表述或过时材料",
            40: "有证据但来源类型不匹配，或数据口径缺失",
            60: "事实基本可靠，但关键数据、来源、口径或可核验性不足",
            80: "证据类型匹配，事实准确，重要数据有口径",
            100: "证据充分、来源分层清楚，事实和推断边界明确",
        },
    },
    {
        "key": "information_integration",
        "label_zh": "资讯整合与比较",
        "description": "评估答案能否把政策、监管、产业、公司事件、市场情绪和数据口径整合成主线。",
        "six_level_anchors": {
            0: "信息碎片无组织",
            20: "简单罗列，主线缺失",
            40: "有分类但层次混乱、主次不清",
            60: "结构基本清楚，但比较维度或结论收敛不足",
            80: "按合理维度整合，能形成清晰主线和判断",
            100: "多源信息互相校验，比较维度完整，结论高度收敛",
        },
    },
    {
        "key": "investment_mapping",
        "label_zh": "投资映射与落地",
        "description": "评估答案能否把资讯转化为行业判断、影响链条、受益环节和A股标的映射。",
        "six_level_anchors": {
            0: "完全没有金融落地或映射错误",
            20: "只给宽泛板块或概念名",
            40: "有标的但主线、受益环节、催化剂对应关系泛化",
            60: "能给出基本映射，但核心/次级、直接/间接、确定/弹性分层不足",
            80: "映射清楚，有主线、环节和标的层级",
            100: "映射精准，能说明影响路径、受益纯度、风险边界和后续验证点",
        },
    },
    {
        "key": "core_signal_extraction",
        "label_zh": "核心信号提炼",
        "description": "评估答案能否抓住真正驱动市场或判断的核心信号，而不是套模板或堆素材。",
        "six_level_anchors": {
            0: "完全没抓到核心催化剂",
            20: "提到相关方向，但主因缺失",
            40: "抓到部分线索，但重点不突出或判断不收敛",
            60: "能指出主因，但解释力度、证据或影响链条不足",
            80: "主信号明确，能解释为什么它比其他因素更重要",
            100: "核心信号、证据、传播链、市场心理和影响路径均清晰",
        },
    },
    {
        "key": "nonstandard_source_awareness",
        "label_zh": "非标准资讯意识",
        "description": "评估答案是否理解市场小段子、调研纪要、金融大V文章、官媒截图等来源的价值与边界。",
        "six_level_anchors": {
            0: "该用非标准资讯时完全无意识，导致主因缺失",
            20: "泛泛提到传闻或文章，但没有利用核心信息",
            40: "使用了相关线索，但没有区分传闻、纪要、官媒、公告等来源边界",
            60: "能利用非标准资讯补充解释，但核验和表达边界一般",
            80: "能把非标准资讯作为线索并交叉验证，表达审慎",
            100: "能高效结合小段子、纪要、大V、官媒截图抓重点，并清楚区分事实、传闻和观点",
        },
    },
    {
        "key": "credibility_expression",
        "label_zh": "可信表达",
        "description": "评估答案表达是否专业、审慎、可读，是否避免把不确定内容说成确定事实。",
        "six_level_anchors": {
            0: "表达严重误导或虚假确定",
            20: "空泛、绝对化、主观断言多",
            40: "可读但可信边界弱，缺少必要限定",
            60: "基本可信，但有啰嗦、泛化或证据表达不足",
            80: "结构清楚，语气审慎，事实与判断区分良好",
            100: "表达简洁有力，结论、证据、风险和验证点都清晰",
        },
    },
    {
        "key": "tool_usage",
        "label_zh": "工具使用合理性",
        "description": "评估规划链路中的工具选择、检索策略、交叉验证和来源覆盖。",
        "six_level_anchors": {
            0: "明显需要检索或查询却完全未使用工具，或工具结果全错",
            20: "工具选择错误，遗漏关键来源",
            40: "有检索但时间过滤、关键词、来源类型或交叉验证不足",
            60: "工具使用基本合理，但效率或覆盖有明显改进空间",
            80: "工具选择精准，能覆盖官方、数据、新闻、公司、市场线索",
            100: "最小调用获得最大覆盖，时间边界、来源类型和证据交叉验证都到位",
        },
    },
]

DEFAULT_WEIGHTS = {
    "intent_fulfillment": 15,
    "timeliness_fact_boundary": 15,
    "fact_evidence_quality": 15,
    "information_integration": 12,
    "investment_mapping": 12,
    "core_signal_extraction": 10,
    "nonstandard_source_awareness": 8,
    "credibility_expression": 5,
    "tool_usage": 8,
}

WEIGHT_RULES: list[dict] = []

CAP_RULES = [
    {
        "name": "hard_time_or_fact_error",
        "label_zh": "硬性时间或事实错误",
        "label_tag": "硬性时间/事实错误",
        "severity": "critical",
        "ceiling": 40,
        "description": "关键日期、年份、数据口径、项目状态或公司事实错误，并实质影响结论。",
    },
    {
        "name": "stale_or_wrong_evidence",
        "label_zh": "证据过时或来源类型错误",
        "label_tag": "证据过时/来源错误",
        "severity": "critical",
        "ceiling": 50,
        "description": "强时效问题主要依赖旧公告、旧新闻、长期主线或错误来源类型。",
    },
    {
        "name": "template_answer_without_signal",
        "label_zh": "模板化回答未抓核心信号",
        "label_tag": "模板化/核心信号缺失",
        "severity": "warning",
        "ceiling": 55,
        "description": "答案套用固定模板，未抓住真实催化剂、市场主因或交易逻辑。",
    },
    {
        "name": "data_dump_without_judgment",
        "label_zh": "数据堆砌无判断",
        "label_tag": "数据堆砌无判断",
        "severity": "warning",
        "ceiling": 60,
        "description": "堆砌政策、新闻、股票、表格或数据，但没有形成主线和判断。",
    },
    {
        "name": "unverified_rumor_as_fact",
        "label_zh": "传闻当事实",
        "label_tag": "传闻当事实",
        "severity": "critical",
        "ceiling": 50,
        "description": "把市场小段子、群聊、纪要、大V观点或未确认传闻当作确定事实输出。",
    },
]

ROOT_CAUSE_TAXONOMY = [
    {
        "l1": "intent",
        "l1_zh": "意图理解",
        "description": "系统是否正确理解了资讯问答中的显性问题与隐含投资诉求？",
        "l2": [
            "intent_misjudged",
            "implicit_investment_need_omitted",
            "sub_question_omitted",
            "comparison_task_not_recognized",
        ],
    },
    {
        "l1": "evidence",
        "l1_zh": "信息证据",
        "description": "系统找到的信息是否正确、充分、时效匹配，且来源边界清楚？",
        "l2": [
            "time_window_not_enforced",
            "outdated_evidence",
            "wrong_evidence_source",
            "insufficient_evidence",
            "nonstandard_source_missing",
            "source_boundary_blurred",
        ],
    },
    {
        "l1": "tool",
        "l1_zh": "工具选择与执行",
        "description": "系统是否选对工具、参数和交叉验证策略？",
        "l2": [
            "missing_tool_call",
            "wrong_tool_selection",
            "wrong_tool_params",
            "no_cross_validation",
            "image_or_fulltext_not_used",
        ],
    },
    {
        "l1": "reasoning",
        "l1_zh": "推理判断",
        "description": "系统是否从资讯推导出正确主线、影响链和投资映射？",
        "l2": [
            "core_signal_missed",
            "weak_causal_chain",
            "mapping_too_broad",
            "comparison_not_converged",
            "progress_stage_confused",
            "template_reasoning",
        ],
    },
    {
        "l1": "composition",
        "l1_zh": "答案组织",
        "description": "答案是否把已有信息以清晰、可信、重点突出的方式呈现？",
        "l2": [
            "data_dump_no_judgment",
            "key_signal_not_prominent",
            "unclear_structure",
            "source_uncertainty_not_marked",
            "overlong_or_generic_expression",
        ],
    },
]

ROOT_CAUSE_DIM_MAP = {
    "intent_fulfillment": "intent",
    "timeliness_fact_boundary": "evidence",
    "fact_evidence_quality": "evidence",
    "information_integration": "reasoning",
    "investment_mapping": "reasoning",
    "core_signal_extraction": "reasoning",
    "nonstandard_source_awareness": "evidence",
    "credibility_expression": "composition",
    "tool_usage": "tool",
}

