"""
11-instruction-following-ability result-only 自研 vs 竞品评测规则定义。

该比较 skill 只定义指令遵循能力的最终回答质量维度、默认权重和封顶标签。
pairwise 比较字段由输出 schema 约束。
"""

# ── 维度定义 ────────────────────────────────────────────────────────────────

DIMENSIONS = [
    {
        "key": "explicit_instruction_completion",
        "label_zh": "显式指令完成",
        "description": "评估最终回答是否完成用户明确提出的主指令。",
        "six_level_anchors": {
            0: "完全没有回应主指令或对象错误",
            20: "大部分答非所问，仅有零散相关信息",
            40: "只完成相关任务，未真正完成用户要求的主任务",
            60: "大方向相关，但主指令执行不完整，用户仍需追问",
            80: "主指令完成，少量约束或证据补充不充分",
            100: "完整执行主指令和关键约束，答案类型、焦点、证据均匹配",
        },
    },
    {
        "key": "task_type_alignment",
        "label_zh": "任务类型对齐",
        "description": "评估最终回答是否对齐原因、定义、比较、排序、建议、核实等用户要求的任务类型。",
        "six_level_anchors": {
            0: "任务类型完全错误，最终回答与用户要求的动作无关",
            20: "仅触及相关主题，但没有按用户要求的任务类型组织答案",
            40: "部分对齐任务类型，但核心动作明显缺失",
            60: "基本对齐任务类型，但结论形态或关键步骤仍不完整",
            80: "任务类型对齐良好，仅有轻微补充不足",
            100: "准确完成用户要求的任务类型，答案形态和判断标准完全匹配",
        },
    },
    {
        "key": "constraint_coverage",
        "label_zh": "约束覆盖",
        "description": "评估最终回答是否覆盖用户给出的时间、范围、对象、排除条件、格式或其他显式约束。",
        "six_level_anchors": {
            0: "完全无视关键约束或处理对象错误",
            20: "只覆盖少量约束，遗漏核心时间、范围或对象要求",
            40: "覆盖部分约束，但遗漏足以影响结论的关键限制",
            60: "多数约束被覆盖，但仍有明显遗漏或口径不清",
            80: "关键约束基本覆盖，仅有轻微边界说明不足",
            100: "逐项覆盖所有显式约束，时间、对象、范围和格式均清楚",
        },
    },
    {
        "key": "answer_focus",
        "label_zh": "答案焦点",
        "description": "评估最终回答是否围绕用户主问展开，而非数据堆砌、背景泛化或焦点漂移。",
        "six_level_anchors": {
            0: "最终回答焦点完全偏离主问",
            20: "主要篇幅偏离主问，只留下零散相关信息",
            40: "有相关内容，但主答案被背景、数据或模板话术淹没",
            60: "基本围绕主问，但结构和重点仍不够清楚",
            80: "焦点清楚，主答案突出，仅有少量冗余",
            100: "主问被直接、集中、清晰地回答，补充信息全部服务结论",
        },
    },
    {
        "key": "necessary_information_completeness",
        "label_zh": "必要信息完整度",
        "description": "评估最终回答是否具备完成主指令所必需的定义、原因、证据、标准或结论。",
        "six_level_anchors": {
            0: "缺少完成主指令所需的全部关键信息",
            20: "只有零散信息，无法支撑用户要的结论或动作",
            40: "有部分必要信息，但关键定义、原因、标准或依据缺失",
            60: "必要信息基本具备，但证据或判断标准仍不够充分",
            80: "必要信息完整，能较好支撑主指令，仅有轻微不足",
            100: "必要信息充分、准确、结构清楚，完全支撑用户所需结论",
        },
    },
]

# ── 权重规则 ────────────────────────────────────────────────────────────────

# 默认权重（总和 100），LLM 动态权重回退时使用。
DEFAULT_WEIGHTS = {
    "explicit_instruction_completion": 35,
    "task_type_alignment": 22,
    "constraint_coverage": 18,
    "answer_focus": 15,
    "necessary_information_completeness": 10,
}

# 按 skill_name 匹配的权重规则，按顺序匹配第一个命中。
WEIGHT_RULES: list[dict] = []

# ── 封顶标签（保留原类别标签语义，不直接修改分数）────────────────────────

CAP_RULES = [
    {
        "name": "primary_instruction_missing",
        "label_zh": "主指令未完成",
        "label_tag": "主指令未完成",
        "severity": "critical",
        "ceiling": 45,
        "score_effect": "tag_only",
        "description": "最终回答没有完成用户明确要求的核心动作，例如问原因但无原因。",
    },
    {
        "name": "wrong_task_type",
        "label_zh": "任务类型错误",
        "label_tag": "任务类型错误",
        "severity": "critical",
        "ceiling": 50,
        "score_effect": "tag_only",
        "description": "最终回答的任务类型错误，例如问定义却答指数查询，问比较却只分别介绍。",
    },
    {
        "name": "critical_constraint_ignored",
        "label_zh": "关键约束被忽略",
        "label_tag": "关键约束被忽略",
        "severity": "critical",
        "ceiling": 60,
        "score_effect": "tag_only",
        "description": "最终回答忽略关键时间、对象、范围、排除条件或格式约束。",
    },
    {
        "name": "data_dump_without_instruction_answer",
        "label_zh": "数据堆砌但未回答主问",
        "label_tag": "数据堆砌但未回答主问",
        "severity": "warning",
        "ceiling": 55,
        "score_effect": "tag_only",
        "description": "最终回答大量堆砌行情、表格、指标、新闻摘录或查询结果，但未转化为用户要求的答案。",
    },
    {
        "name": "answer_focus_drift",
        "label_zh": "答案焦点漂移",
        "label_tag": "答案焦点漂移",
        "severity": "warning",
        "ceiling": 65,
        "score_effect": "tag_only",
        "description": "最终回答包含部分相关内容，但重点明显偏离用户要求。",
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
