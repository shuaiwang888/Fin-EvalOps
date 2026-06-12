"""
06-compound-intent result-only 自研 vs 竞品评测规则定义。

该比较 skill 只定义复合意图类金融问答的最终回答质量维度、默认权重和质量标签。
pairwise 比较字段由输出 schema 约束。
"""

DIMENSIONS = [
    {
        "key": "intent_decomposition",
        "label_zh": "意图拆解",
        "description": "评估最终回答是否正确拆解复合意图中的子任务、时间窗口、对象和输出要求。",
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
        "key": "task_coverage_priority",
        "label_zh": "子任务覆盖与主次",
        "description": "评估最终回答是否完整覆盖关键子任务，并按用户决策价值组织主次。",
        "six_level_anchors": {
            0: "几乎所有子任务都没有被回答",
            20: "仅覆盖了少数次要子任务，核心子任务被忽略",
            40: "核心子任务有涉及但覆盖不全，或主次关系判断偏差较大",
            60: "主要子任务基本覆盖，但个别次要任务遗漏或优先级处理不当",
            80: "所有关键子任务全覆盖，主次分明，资源分配合理",
            100: "覆盖完美，每个子任务被充分展开，主次权重精确匹配用户意图",
        },
    },
    {
        "key": "multi_source_evidence_integration",
        "label_zh": "多源证据整合",
        "description": "评估最终回答是否把行情、新闻、公告、产业、政策、财务、资金等多源信息整合成统一结论。",
        "six_level_anchors": {
            0: "完全没有证据整合，纯文字推测",
            20: "仅使用单一或浅层信息，缺乏交叉验证",
            40: "使用了多源信息但没有有效整合，各自为阵",
            60: "多源信息基本整合，但对某些关键信息源的权重判断不当",
            80: "多源信息有效整合，相互印证，权重分配合理",
            100: "整合完美，多源信息形成立体证据体系，矛盾信息被解释处理",
        },
    },
    {
        "key": "analysis_chain_closure",
        "label_zh": "分析链路闭环",
        "description": "评估最终回答从事实到影响、传导、策略或结论的分析链路是否完整闭合。",
        "six_level_anchors": {
            0: "分析链路完全断裂，事实与结论无关联",
            20: "有分析意图但各个环节严重脱节，结论悬浮",
            40: "部分环节有分析但关键传导环节缺失或逻辑跳跃",
            60: "分析链路基本完整，但个别环节的论证深度不足",
            80: "分析链路完整闭环，各环节逻辑自洽，层层推进",
            100: "分析闭环完美，每个推理步骤有证据，结论有力且无明显漏洞",
        },
    },
    {
        "key": "data_logic_rigor",
        "label_zh": "数据与逻辑严谨性",
        "description": "评估最终回答的计算口径、时间窗口、案例真实性、比较口径和推演逻辑是否可靠。",
        "six_level_anchors": {
            0: "数据或逻辑存在致命错误，结论完全不可靠",
            20: "多处数据口径不一致或逻辑矛盾严重",
            40: "有一处关键数据的口径或时间窗口错误，或逻辑不自洽",
            60: "数据和逻辑基本严谨，但个别口径或假设说明不够清晰",
            80: "数据口径清晰，时间窗口正确，逻辑自洽，案例真实",
            100: "数据与逻辑完美，所有口径、时间窗口和假设明确说明，完全可复核",
        },
    },
    {
        "key": "decision_actionability",
        "label_zh": "决策表达与可执行性",
        "description": "评估最终回答是否给出可执行的策略、择股、布局、调仓、合约、价位、利润测算或操作框架。",
        "six_level_anchors": {
            0: "完全没有可执行的决策建议",
            20: "给了模糊方向但没有具体到可操作层面",
            40: "有可执行建议但缺少关键触发条件或执行细节",
            60: "操作建议基本可执行但个别条件或边界不够明确",
            80: "操作建议清晰可执行，触发条件、时机、仓位或方案明确",
            100: "决策建议完美，每项建议有明确执行方案、条件、风控和备选路径",
        },
    },
    {
        "key": "composition_readability",
        "label_zh": "结构与可读性",
        "description": "评估最终回答在复杂问题中是否结构清晰、重点突出、便于复核。",
        "six_level_anchors": {
            0: "结构完全混乱，无法阅读",
            20: "结构松散，信息碎片化，难以找到重点",
            40: "有基本结构但逻辑流不畅，读者需要来回跳跃",
            60: "结构基本清晰但部分段落组织可优化，重点不够突出",
            80: "结构清晰，层次分明，重点突出，易读性好",
            100: "结构完美，逻辑流自然，信息密度和可读性达到最佳平衡",
        },
    },
]

DEFAULT_WEIGHTS = {
    "intent_decomposition": 16,
    "task_coverage_priority": 15,
    "multi_source_evidence_integration": 16,
    "analysis_chain_closure": 18,
    "data_logic_rigor": 17,
    "decision_actionability": 13,
    "composition_readability": 5,
}

WEIGHT_RULES: list[dict] = []

CAP_RULES = [
    {
        "name": "missed_major_subtask",
        "label_zh": "遗漏主要子任务",
        "label_tag": "遗漏主要子任务",
        "severity": "critical",
        "ceiling": 65,
        "score_effect": "tag_only",
        "description": "复合问题中的主要子任务被最终回答遗漏。",
    },
    {
        "name": "data_or_case_unreliable",
        "label_zh": "数据或案例不可靠",
        "label_tag": "数据/案例不可靠",
        "severity": "critical",
        "ceiling": 55,
        "score_effect": "tag_only",
        "description": "最终回答引用的数据或案例不可靠、编造或错误。",
    },
    {
        "name": "calculation_or_time_window_error",
        "label_zh": "计算或时间窗口错误",
        "label_tag": "计算/时间窗口错误",
        "severity": "critical",
        "ceiling": 55,
        "score_effect": "tag_only",
        "description": "最终回答的计算逻辑或时间窗口处理存在实质错误。",
    },
    {
        "name": "information_pile_without_synthesis",
        "label_zh": "信息堆砌无综合",
        "label_tag": "信息堆砌无综合",
        "severity": "warning",
        "ceiling": 60,
        "score_effect": "tag_only",
        "description": "最终回答罗列多源信息，但未整合为事实、影响、传导和策略闭环。",
    },
    {
        "name": "missing_required_decision_output",
        "label_zh": "遗漏必要决策输出",
        "label_tag": "遗漏必要决策输出",
        "severity": "critical",
        "ceiling": 65,
        "score_effect": "tag_only",
        "description": "用户明确要求的策略、建议、择股、调仓、合约、价位或利润测算未提供。",
    },
    {
        "name": "wrong_or_shallow_evidence_mix",
        "label_zh": "证据组合错误或浅层",
        "label_tag": "证据组合错误/浅层",
        "severity": "warning",
        "ceiling": 60,
        "score_effect": "tag_only",
        "description": "最终回答中的多源证据权重、优先级或相关性判断错误，或证据浅层不足以支撑结论。",
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
