"""
09-financial-performance-interpretation result-only 自研 vs 竞品评测规则定义。

该比较 skill 只定义财报业绩解读领域的最终回答质量维度、默认权重和封顶标签。
pairwise 比较字段由输出 schema 约束。
"""

# ── 维度定义 ────────────────────────────────────────────────────────────────

DIMENSIONS = [
    {
        "key": "intent_understanding",
        "label_zh": "意图理解与任务完成",
        "description": "评估最终回答是否理解用户表层问题、隐含财报任务和报告期约束。始终考察。",
        "six_level_anchors": {
            0: "完全未回应用户的财报问题，答非所问",
            20: "把财报分析问题当做简单数据查询，严重偏离用户需求",
            40: "只回答部分财报问题，遗漏关键任务或报告期",
            60: "基本回应了用户意图，但财报任务或时间范围可更精准",
            80: "准确理解财报问题意图，回应完整且紧扣报告期",
            100: "完美理解所有显性和隐性财报需求，报告期约束精准",
        },
    },
    {
        "key": "report_data_accuracy",
        "label_zh": "财报数据与口径准确性",
        "description": "评估最终回答中的财务指标、报告期、同比环比和会计口径是否准确。",
        "six_level_anchors": {
            0: "核心财务数据完全错误或编造",
            20: "关键指标出现实质性错误，报告期映射错误严重",
            40: "数据大致可接受但有多处口径不一致或报告期混淆",
            60: "关键数据正确，但个别指标口径说明不够清晰",
            80: "财报数据准确，口径清楚，报告期对应正确",
            100: "数据完美准确，所有口径、报告期、会计政策处理恰当",
        },
    },
    {
        "key": "primary_evidence_quality",
        "label_zh": "公告全文与证据质量",
        "description": "评估最终回答是否呈现了公告、年报附注、业绩说明会等足够权威且贴近问题的证据。",
        "six_level_anchors": {
            0: "最终回答完全没有可验证证据",
            20: "仅给二手摘要或泛泛判断，缺少一手披露信息",
            40: "提到部分披露信息但遗漏附注、说明会或公告中的关键细节",
            60: "主要证据来自公告或年报，但个别关键证据的引用或定位不够精确",
            80: "充分呈现公告全文、附注和说明会信息，证据定位准确",
            100: "证据来自多层一手信息，关键披露与结论之间互相印证",
        },
    },
    {
        "key": "causal_attribution_depth",
        "label_zh": "归因深度",
        "description": "评估最终回答是否把财务变化推到真实业务原因、会计处理和特殊事件。",
        "six_level_anchors": {
            0: "完全没有归因分析，只罗列财务数据",
            20: "只做了同比/环比的方向描述，没有解释背后的业务原因",
            40: "有归因但停留在表面，没有区分量/价/成本/结构/会计/特殊事件",
            60: "归因方向正确但深度不足，部分关键驱动因素未拆解",
            80: "归因深入，区分了主要驱动因素，有数据支撑",
            100: "归因完美，量价成本结构逐层拆解，会计和特殊事项影响被精准剥离",
        },
    },
    {
        "key": "business_financial_linkage",
        "label_zh": "业务财务联动",
        "description": "评估最终回答是否把财务变化连接到业务、行业、订单、产品结构等经营层面。",
        "six_level_anchors": {
            0: "完全没有将财务与业务联系起来",
            20: "只讲了财务数据变化，没有联系行业景气、订单或产品",
            40: "有业务方向暗示但缺少具体的行业对比、订单节奏或产品周期分析",
            60: "基本的业务财务联动，但个别经营变量未充分考虑",
            80: "业务财务联动清晰，行业地位、订单、产能或产品结构与财务变化对应",
            100: "业务财务一体化解读完美，财务变化被精确映射到经营变量和产业逻辑",
        },
    },
    {
        "key": "forward_investment_judgment",
        "label_zh": "前瞻与投资判断",
        "description": "评估最终回答是否给出了利好利空判断、业绩持续性评估和后续观察指标。",
        "six_level_anchors": {
            0: "用户明确问前景/股价影响但完全未涉及",
            20: "给了模糊的方向但没有具体分析业绩持续性或市场预期",
            40: "有前瞻方向但缺少市场预期对比、基线判断或后续观察指标",
            60: "给出了基本的前瞻判断但深度不够，或风险提示不充分",
            80: "前瞻判断具体，有业绩持续性和市场预期分析，观察指标清晰",
            100: "前瞻判断完美，多情景推演完整，市场预期差和后续验证节点明确",
        },
    },
    {
        "key": "composition_credibility",
        "label_zh": "表达可信度",
        "description": "评估最终回答表达是否可信、客观、重点突出。始终为辅助维度。",
        "six_level_anchors": {
            0: "输出完全不可信或无法阅读",
            20: "表达混乱，数据堆砌，结论被淹没",
            40: "有基本结构但重点不够突出或个别表述过于绝对",
            60: "表达基本清晰，可信度可接受，个别组织可优化",
            80: "结构清晰、措辞审慎，关键结论突出",
            100: "表达完美，数据与结论一目了然，专业审慎无可挑剔",
        },
    },
]

# ── 权重规则 ────────────────────────────────────────────────────────────────

# 默认权重（总和 100），LLM 动态权重回退时使用
DEFAULT_WEIGHTS = {
    "intent_understanding": 15,
    "report_data_accuracy": 18,
    "primary_evidence_quality": 20,
    "causal_attribution_depth": 18,
    "business_financial_linkage": 12,
    "forward_investment_judgment": 12,
    "composition_credibility": 5,
}

# 按 skill_name 匹配的权重规则，按顺序匹配第一个命中
WEIGHT_RULES: list[dict] = []

# ── 封顶标签（保留原类别标签语义，不直接修改分数）────────────────────────

CAP_RULES = [
    {
        "name": "hard_fact_or_caliber_error",
        "label_zh": "硬性事实或口径错误",
        "label_tag": "硬性事实/口径错误",
        "severity": "critical",
        "ceiling": 40,
        "score_effect": "tag_only",
        "description": "最终回答中的关键财务数据、报告期、会计口径或基础事实有实质性错误。",
    },
    {
        "name": "missing_primary_disclosure",
        "label_zh": "遗漏核心公告披露",
        "label_tag": "遗漏核心公告披露",
        "severity": "critical",
        "ceiling": 55,
        "score_effect": "tag_only",
        "description": "最终回答推理自洽但遗漏了公司明确披露的核心事件或数据。",
    },
    {
        "name": "wrong_special_event_explanation",
        "label_zh": "特殊事件解释错误",
        "label_tag": "特殊事件解释错误",
        "severity": "critical",
        "ceiling": 45,
        "score_effect": "tag_only",
        "description": "最终回答对减值、重组、会计变更、出售资产等特殊事项的解释出现实质错误。",
    },
    {
        "name": "surface_financial_formula_only",
        "label_zh": "仅停留在财务公式表层",
        "label_tag": "仅财务公式表层",
        "severity": "warning",
        "ceiling": 60,
        "score_effect": "tag_only",
        "description": "最终回答仅做了同比/环比计算，没有深入到业务原因和投资含义。",
    },
    {
        "name": "unverifiable_or_hallucinated_numbers",
        "label_zh": "不可验证或幻觉数字",
        "label_tag": "不可验证/幻觉数字",
        "severity": "critical",
        "ceiling": 50,
        "score_effect": "tag_only",
        "description": "最终回答引用了无法在披露材料中找到的财务数据或编造数字。",
    },
    {
        "name": "missing_required_conclusion",
        "label_zh": "遗漏必要结论",
        "label_tag": "遗漏必要结论",
        "severity": "warning",
        "ceiling": 65,
        "score_effect": "tag_only",
        "description": "用户明确要求利好利空判断或前景分析但最终回答未给出。",
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
