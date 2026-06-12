"""
11-instruction-following-ability-self-vs-competitor 评测规则定义。

该比较 skill 沿用第 11 类指令遵循能力的绝对评分维度、默认权重、
封顶规则和根因体系；pairwise 比较字段由输出 schema 约束。
"""

# 维度定义

DIMENSIONS = [
    {
        "key": "explicit_instruction_completion",
        "label_zh": "显式指令完成",
        "description": "评估答案是否完成用户明确提出的主指令。",
        "six_level_anchors": {
            0: "完全没有回应主指令或对象错误",
            20: "大部分答非所问，仅有零散相关数据",
            40: "只完成相关任务，未真正完成用户要求的任务类型",
            60: "大方向相关，但主指令执行不完整，用户仍需追问",
            80: "主指令完成，少量约束或证据补充不充分",
            100: "完整执行主指令和关键约束，答案类型、焦点、证据均匹配",
        },
    },
    {
        "key": "task_type_alignment",
        "label_zh": "任务类型对齐",
        "description": "评估答案是否对齐原因、定义、比较、排序、建议等用户要求的任务类型。",
        "six_level_anchors": {
            0: "完全没有回应主指令或对象错误",
            20: "大部分答非所问，仅有零散相关数据",
            40: "只完成相关任务，未真正完成用户要求的任务类型",
            60: "大方向相关，但主指令执行不完整，用户仍需追问",
            80: "主指令完成，少量约束或证据补充不充分",
            100: "完整执行主指令和关键约束，答案类型、焦点、证据均匹配",
        },
    },
    {
        "key": "constraint_coverage",
        "label_zh": "约束覆盖",
        "description": "评估答案是否覆盖用户给出的时间、范围、对象、排除条件和格式约束。",
        "six_level_anchors": {
            0: "完全没有回应主指令或对象错误",
            20: "大部分答非所问，仅有零散相关数据",
            40: "只完成相关任务，未真正完成用户要求的任务类型",
            60: "大方向相关，但主指令执行不完整，用户仍需追问",
            80: "主指令完成，少量约束或证据补充不充分",
            100: "完整执行主指令和关键约束，答案类型、焦点、证据均匹配",
        },
    },
    {
        "key": "answer_focus",
        "label_zh": "答案焦点",
        "description": "评估答案是否围绕用户主问展开，而非数据堆砌、背景泛化或焦点漂移。",
        "six_level_anchors": {
            0: "完全没有回应主指令或对象错误",
            20: "大部分答非所问，仅有零散相关数据",
            40: "只完成相关任务，未真正完成用户要求的任务类型",
            60: "大方向相关，但主指令执行不完整，用户仍需追问",
            80: "主指令完成，少量约束或证据补充不充分",
            100: "完整执行主指令和关键约束，答案类型、焦点、证据均匹配",
        },
    },
    {
        "key": "necessary_information_completeness",
        "label_zh": "必要信息完整度",
        "description": "评估答案是否具备完成主指令所必需的定义、原因、证据、标准或结论。",
        "six_level_anchors": {
            0: "完全没有回应主指令或对象错误",
            20: "大部分答非所问，仅有零散相关数据",
            40: "只完成相关任务，未真正完成用户要求的任务类型",
            60: "大方向相关，但主指令执行不完整，用户仍需追问",
            80: "主指令完成，少量约束或证据补充不充分",
            100: "完整执行主指令和关键约束，答案类型、焦点、证据均匹配",
        },
    },
    {
        "key": "tool_usage",
        "label_zh": "工具使用合理性",
        "description": "评估工具选择、查询设计和工具结果转化是否服务用户主指令。",
        "six_level_anchors": {
            0: "完全没有回应主指令或对象错误",
            20: "大部分答非所问，仅有零散相关数据",
            40: "只完成相关任务，未真正完成用户要求的任务类型",
            60: "大方向相关，但主指令执行不完整，用户仍需追问",
            80: "主指令完成，少量约束或证据补充不充分",
            100: "完整执行主指令和关键约束，答案类型、焦点、证据均匹配",
        },
    },
]

# 默认权重与自研 skill 的建议权重保持一致，sum=100。

DEFAULT_WEIGHTS = {
    "explicit_instruction_completion": 30,
    "task_type_alignment": 20,
    "constraint_coverage": 15,
    "answer_focus": 15,
    "necessary_information_completeness": 10,
    "tool_usage": 10,
}

CAP_RULES = [
    {
        "name": "primary_instruction_missing",
        "label_zh": "主指令未完成",
        "severity": "critical",
        "ceiling": 45,
        "description": "用户主指令未完成，例如问原因但无原因。",
    },
    {
        "name": "wrong_task_type",
        "label_zh": "任务类型错误",
        "severity": "critical",
        "ceiling": 50,
        "description": "答案任务类型错误，例如问定义却答指数查询。",
    },
    {
        "name": "critical_constraint_ignored",
        "label_zh": "关键约束被忽略",
        "severity": "critical",
        "ceiling": 60,
        "description": "忽略关键时间、对象、范围或排除条件。",
    },
    {
        "name": "data_dump_without_instruction_answer",
        "label_zh": "数据堆砌但未回答主问",
        "severity": "warning",
        "ceiling": 55,
        "description": "大量数据堆砌但未回答主问。",
    },
    {
        "name": "answer_focus_drift",
        "label_zh": "答案焦点漂移",
        "severity": "warning",
        "ceiling": 65,
        "description": "有部分相关内容，但重点明显偏离用户要求。",
    },
]

ROOT_CAUSE_TAXONOMY = [
    {
        "l1": "intent",
        "l1_zh": "指令识别",
        "description": "是否抽取出用户主指令和约束。",
        "l2": [
            "primary-instruction-missed",
            "task-type-misread",
            "constraint-missed",
            "secondary-info-overweighted",
        ],
    },
    {
        "l1": "evidence",
        "l1_zh": "证据收集",
        "description": "证据是否服务主指令。",
        "l2": [
            "evidence-not-causal",
            "definition-evidence-missing",
            "constraint-evidence-missing",
            "irrelevant-evidence-dominates",
        ],
    },
    {
        "l1": "tool",
        "l1_zh": "工具执行",
        "description": "工具是否为完成指令而用。",
        "l2": [
            "tool-query-not-aligned",
            "tool-result-not-transformed",
            "missing-required-tool-check",
            "over-fetching",
        ],
    },
    {
        "l1": "reasoning",
        "l1_zh": "指令转换",
        "description": "是否把数据转成用户要求的答案类型。",
        "l2": [
            "phenomenon-not-cause",
            "query-result-not-definition",
            "comparison-not-contrasted",
            "decision-criterion-missing",
        ],
    },
    {
        "l1": "composition",
        "l1_zh": "答案呈现",
        "description": "主答案是否放在前面且聚焦。",
        "l2": [
            "answer-buried",
            "no-direct-answer",
            "constraints-not-enumerated",
            "generic-template",
        ],
    },
]

ROOT_CAUSE_DIM_MAP = {
    "explicit_instruction_completion": "intent",
    "task_type_alignment": "intent",
    "constraint_coverage": "intent",
    "answer_focus": "composition",
    "necessary_information_completeness": "evidence",
    "tool_usage": "tool",
}
