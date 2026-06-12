"""
08-information-and-knowledge-qa result-only 自研 vs 竞品评测规则定义。

该比较 skill 只定义金融资讯知识问答领域的最终回答质量维度、默认权重和封顶标签。
pairwise 比较字段由输出 schema 约束。
"""

# ── 维度定义 ────────────────────────────────────────────────────────────────

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
        "description": "评估答案能否把资讯转化为行业判断、影响链条、受益环节和 A 股标的映射。",
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
        "description": "评估答案是否理解市场小段子、调研纪要、金融大 V 文章、官媒截图等来源的价值与边界。",
        "six_level_anchors": {
            0: "该用非标准资讯时完全无意识，导致主因缺失",
            20: "泛泛提到传闻或文章，但没有利用核心信息",
            40: "使用了相关线索，但没有区分传闻、纪要、官媒、公告等来源边界",
            60: "能利用非标准资讯补充解释，但核验和表达边界一般",
            80: "能把非标准资讯作为线索并交叉验证，表达审慎",
            100: "能高效结合小段子、纪要、大 V、官媒截图抓重点，并清楚区分事实、传闻和观点",
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
]

# ── 权重规则 ────────────────────────────────────────────────────────────────

# 默认权重（总和 100），LLM 动态权重回退时使用。
DEFAULT_WEIGHTS = {
    "intent_fulfillment": 16,
    "timeliness_fact_boundary": 16,
    "fact_evidence_quality": 18,
    "information_integration": 13,
    "investment_mapping": 12,
    "core_signal_extraction": 11,
    "nonstandard_source_awareness": 8,
    "credibility_expression": 6,
}

WEIGHT_RULES: list[dict] = []

# ── 封顶标签（保留原类别标签语义，不直接修改分数）────────────────────────

CAP_RULES = [
    {
        "name": "hard_time_or_fact_error",
        "label_zh": "硬性时间或事实错误",
        "label_tag": "硬性时间/事实错误",
        "severity": "critical",
        "ceiling": 40,
        "score_effect": "tag_only",
        "description": "最终回答中的关键日期、年份、政策历史定位、数据口径、项目状态或公司事实错误，并实质影响结论。",
    },
    {
        "name": "stale_or_wrong_evidence",
        "label_zh": "证据过时或来源类型错误",
        "label_tag": "证据过时/来源错误",
        "severity": "critical",
        "ceiling": 50,
        "score_effect": "tag_only",
        "description": "强时效问题主要依赖旧公告、旧新闻、长期主线或错误来源类型。",
    },
    {
        "name": "template_answer_without_signal",
        "label_zh": "模板化回答未抓核心信号",
        "label_tag": "模板化/核心信号缺失",
        "severity": "warning",
        "ceiling": 55,
        "score_effect": "tag_only",
        "description": "最终回答套用固定模板，未抓住真实催化剂、市场主因或交易逻辑。",
    },
    {
        "name": "data_dump_without_judgment",
        "label_zh": "数据堆砌无判断",
        "label_tag": "数据堆砌无判断",
        "severity": "warning",
        "ceiling": 60,
        "score_effect": "tag_only",
        "description": "最终回答堆砌政策、新闻、股票、表格或数据，但没有形成主线和判断。",
    },
    {
        "name": "unverified_rumor_as_fact",
        "label_zh": "传闻当事实",
        "label_tag": "传闻当事实",
        "severity": "critical",
        "ceiling": 50,
        "score_effect": "tag_only",
        "description": "最终回答把市场小段子、群聊、纪要、大 V 观点或未确认传闻当作确定事实输出。",
    },
]

# ── 证据边界 ────────────────────────────────────────────────────────────────

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
