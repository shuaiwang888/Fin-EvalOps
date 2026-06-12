"""
11-instruction-following-ability 评测规则定义 (v5)。

指令遵循能力类问题：评估模型是否准确完成用户的主指令、任务类型和约束条件。
"""

DIMENSIONS = [
    {
        "key": "explicit_instruction_completion", "label_zh": "显式指令完成",
        "description": "评估主指令是否被完整执行。始终考察。",
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
        "key": "task_type_alignment", "label_zh": "任务类型对齐",
        "description": "评估原因、定义、比较、排序、建议等任务类型是否对齐。始终考察。",
        "six_level_anchors": {
            0: "答案任务类型与用户要求完全相反",
            20: "任务类型根本错误，如问定义却答行情查询",
            40: "任务类型大致相关但输出形态与用户需求明显不匹配",
            60: "任务类型基本正确，但部分子任务执行有偏差",
            80: "任务类型对齐准确，输出形态匹配用户需求",
            100: "任务类型完美对齐，所有子任务和输出形态精确匹配",
        },
    },
    {
        "key": "constraint_coverage", "label_zh": "约束覆盖",
        "description": "评估时间、范围、对象、排除条件等约束是否被覆盖。",
        "six_level_anchors": {
            0: "完全忽略所有用户约束条件",
            20: "关键约束被忽略，导致答案严重偏离用户要求",
            40: "部分约束被覆盖但关键限制条件遗漏",
            60: "主要约束基本覆盖，但个别边界条件不够精确",
            80: "约束覆盖全面，所有显式条件均被处理",
            100: "所有显式和隐式约束完美覆盖，无任何遗漏",
        },
    },
    {
        "key": "answer_focus", "label_zh": "答案焦点",
        "description": "评估是否围绕主问展开，而非数据堆砌或跑题。始终考察。",
        "six_level_anchors": {
            0: "答案完全跑题，与用户主问无关",
            20: "重点明显偏离用户要求，大量无关内容",
            40: "有部分相关内容但焦点模糊，被次要信息稀释",
            60: "基本围绕主问，但部分内容不够聚焦",
            80: "焦点清晰，围绕主问展开，信息密度合理",
            100: "焦点完美，每个信息片段都服务主问，无任何偏离",
        },
    },
    {
        "key": "necessary_information_completeness", "label_zh": "必要信息完整度",
        "description": "评估必要证据和信息是否完整支撑答案。",
        "six_level_anchors": {
            0: "完全没有支撑答案的必要信息",
            20: "必要信息严重缺失，答案无法成立",
            40: "有部分证据但关键信息缺失，结论不牢靠",
            60: "必要信息基本齐全，但个别支撑点可补充",
            80: "必要信息完整，证据充分支撑结论",
            100: "信息完美完整，所有必要证据和细节均到位",
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
    "explicit_instruction_completion": 30,
    "task_type_alignment": 20,
    "constraint_coverage": 15,
    "answer_focus": 15,
    "necessary_information_completeness": 10,
    "tool_usage": 10,
}

WEIGHT_RULES: list[dict] = []

CAP_RULES = [
    {
        "name": "primary_instruction_missing", "label_zh": "主指令缺失",
        "label_tag": "主指令缺失", "severity": "critical", "ceiling": 45,
        "description": "用户主指令未完成，例如问原因但无原因。",
    },
    {
        "name": "wrong_task_type", "label_zh": "任务类型错误",
        "label_tag": "任务类型错误", "severity": "critical", "ceiling": 50,
        "description": "答案任务类型错误，例如问定义却答指数查询。",
    },
    {
        "name": "critical_constraint_ignored", "label_zh": "关键约束忽略",
        "label_tag": "关键约束忽略", "severity": "critical", "ceiling": 60,
        "description": "忽略关键时间、对象、范围或排除条件。",
    },
    {
        "name": "data_dump_without_instruction_answer", "label_zh": "数据堆砌未回答主问",
        "label_tag": "数据堆砌未回答主问", "severity": "warning", "ceiling": 55,
        "description": "大量数据堆砌但未回答主问。",
    },
    {
        "name": "answer_focus_drift", "label_zh": "答案焦点漂移",
        "label_tag": "答案焦点漂移", "severity": "warning", "ceiling": 65,
        "description": "有部分相关内容，但重点明显偏离用户要求。",
    },
]

ROOT_CAUSE_TAXONOMY = [
    {"l1": "intent", "l1_zh": "理解问题", "description": "是否准确解析用户主指令、任务类型和约束条件", "l2": ["primary_instruction_misread", "task_type_misidentified", "constraint_overlooked", "focus_target_misjudged"]},
    {"l1": "evidence", "l1_zh": "检索数据", "description": "获取的信息是否服务主指令", "l2": ["missing_required_evidence", "irrelevant_data_retrieved", "insufficient_data_depth"]},
    {"l1": "tool", "l1_zh": "选择与执行工具", "description": "是否选对工具、写对参数", "l2": ["wrong_tool_selection", "insufficient_tool_chain", "tool_param_error"]},
    {"l1": "reasoning", "l1_zh": "指令到答案转换", "description": "数据是否被正确转换为服务指令的答案", "l2": ["data_not_interpreted_for_instruction", "wrong_output_type", "missing_instruction_driven_synthesis"]},
    {"l1": "composition", "l1_zh": "组织答案", "description": "答案结构和焦点是否服务主指令", "l2": ["data_dump_without_focus", "unclear_answer_structure", "focus_drift_in_composition"]},
]

ROOT_CAUSE_DIM_MAP = {
    "explicit_instruction_completion": "intent",
    "task_type_alignment": "intent",
    "constraint_coverage": "intent",
    "answer_focus": "composition",
    "necessary_information_completeness": "evidence",
    "tool_usage": "tool",
}

CONFIDENCE_THRESHOLD = 3
