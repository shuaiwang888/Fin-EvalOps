"""
14-complex-stock-selection-self-vs-competitor 评测规则定义。

本比较 skill 的绝对评分层沿用第 14 类复杂选股 self_judge 的维度、权重、
封顶标签和根因体系；pairwise 比较字段由输出 schema 约束。
"""

DIMENSIONS = [
    {
        "key": "intent_condition_extraction",
        "label_zh": "意图与条件抽取",
        "description": "评估答案和链路是否完整抽取用户长问句中的显性条件、隐性条件、否定条件和输出要求。",
        "six_level_anchors": {
            0: "完全没有抽取用户核心条件，答案与选股需求基本无关",
            20: "只抽取少量表层条件，遗漏大部分关键约束",
            40: "抽取了部分核心条件，但遗漏或改写会显著改变候选池",
            60: "主要条件基本抽取完整，但存在少量次要遗漏、否定条件处理不足或输出要求遗漏",
            80: "显性和多数隐性条件抽取准确，否定条件、范围、排序和输出字段基本完整",
            100: "所有显性/隐性/否定/格式条件均准确抽取，未擅自增删或改写用户约束",
        },
    },
    {
        "key": "financial_semantics_and_caliber",
        "label_zh": "金融语义与口径",
        "description": "评估均线、MACD、KDJ、资金流、龙虎榜、北向、退市风险、主线题材等金融语义和数据口径是否正确。",
        "six_level_anchors": {
            0: "核心金融概念或数据口径完全误解，导致筛选方向错误",
            20: "多处金融语义错误，指标公式、时间口径或业务边界严重混乱",
            40: "存在关键语义或口径偏差，虽然部分条件正确但候选池会明显失真",
            60: "金融语义基本正确，但个别复杂指标、低频数据或业务边界解释不充分",
            80: "金融指标和业务口径理解准确，能识别数据不可用、低频更新和语义边界",
            100: "金融语义、指标公式、交易口径和业务边界全部准确，并能主动说明不可用或需确认的口径",
        },
    },
    {
        "key": "screening_plan_decomposition",
        "label_zh": "筛选规划拆解",
        "description": "评估是否把长问句拆成可执行的分层筛选、二次验证、交集/并集、先后关系和跨领域步骤。",
        "six_level_anchors": {
            0: "完全没有可执行筛选规划，将复杂任务当作单句查询或闲聊处理",
            20: "规划粗糙，未拆解长问句，条件顺序、层级或依赖关系大面积丢失",
            40: "有初步拆解但关键层级、先后关系或跨领域交集处理错误",
            60: "规划基本可执行，但对二次验证、前后依赖、近似条件或无数据兜底处理不足",
            80: "能分层筛选、保留先后关系，并把结构化条件与非标条件合理编排",
            100: "拆解完美，硬条件、软条件、二次验证、排序、兜底和用户交互边界全部清晰",
        },
    },
    {
        "key": "tool_usage",
        "label_zh": "工具与信源匹配",
        "description": "评估 FinQuery、Search、BackTest、CodeInterpreter 等工具选择、关键词聚焦、交叉验证和工具输出读取是否合理。",
        "six_level_anchors": {
            0: "应使用工具却完全未使用，或工具选择全部错误",
            20: "关键非标信息、行情数据或计算任务使用了明显错误的工具",
            40: "工具选择部分合理，但关键词不聚焦、参数错误或缺少必要交叉验证",
            60: "工具使用基本合理，但存在冗余调用、漏查信源或工具输出读取不充分",
            80: "结构化取数、搜索、计算和验证工具匹配良好，参数和关键词较准确",
            100: "工具编排精准高效，结构化与非标证据分工清楚，最小调用完成充分验证",
        },
    },
    {
        "key": "result_correctness_and_coverage",
        "label_zh": "结果正确性与覆盖",
        "description": "评估最终候选股、无结果解释、字段展示、条件覆盖和结果可核验性是否满足用户需求。",
        "six_level_anchors": {
            0: "没有给出可用结果，或结果与用户条件完全不符",
            20: "候选池严重错误，遗漏大量条件或输出明显无关标的",
            40: "结果覆盖部分条件，但关键条件缺失、结果字段错误或无结果解释不可信",
            60: "结果基本可用，但候选覆盖、字段完整性或无结果边界说明仍有明显不足",
            80: "结果较准确，覆盖主要条件，字段和无结果解释清晰，可供进一步复核",
            100: "结果完全贴合条件，候选池、字段、无结果说明和可核验证据都可靠完整",
        },
    },
    {
        "key": "ranking_and_decision_actionability",
        "label_zh": "排序与决策可执行性",
        "description": "评估是否按用户要求输出排序、Top N、选一只、候选池优先级和后续验证/使用方式。",
        "six_level_anchors": {
            0: "用户要求排序或决策输出但完全未提供",
            20: "仅罗列股票，没有排序标准、优先级或可执行结论",
            40: "有排序或候选池，但排序标准与用户要求不匹配或理由很弱",
            60: "排序和决策表达基本满足，但优先级理由、字段或后续验证点不足",
            80: "排序清晰，能解释主排序/次排序和候选池使用方式",
            100: "排序和决策输出完美，标准透明、字段完整、可复核且能直接用于筛选/交易准备",
        },
    },
    {
        "key": "data_logic_time_boundary",
        "label_zh": "数据逻辑与时间边界",
        "description": "评估交易日、日期区间、分时/K线时间点、指标公式、计算口径和不可用数据边界是否严谨。",
        "six_level_anchors": {
            0: "核心日期、交易日、公式或时间窗口错误，结论不可用",
            20: "多处时间/公式/口径错误，严重破坏筛选结果",
            40: "存在关键时间边界或计算口径偏差，部分结果可能失真",
            60: "数据逻辑基本正确，但边界条件、交易日处理或公式说明不够精确",
            80: "时间窗口、交易日、公式和数据边界清晰，仅有轻微可改进处",
            100: "所有时间、公式、交易日、分时边界和不可用数据说明都严谨准确",
        },
    },
    {
        "key": "composition_credibility",
        "label_zh": "表达可信度",
        "description": "评估表达是否清晰可信，是否避免数据堆砌、幻觉、过度承诺或用图表掩盖核心错误。",
        "six_level_anchors": {
            0: "表达严重误导，包含明显幻觉或与证据冲突的结论",
            20: "表达混乱、空泛或过度自信，可信度很低",
            40: "结构和表达有一定可读性，但存在主观断言、漂亮表格掩盖错误或证据弱",
            60: "表达基本清楚可信，但重点不够凝练或部分断言缺少证据边界",
            80: "结构清晰，证据与结论匹配，能说明限制和不确定性",
            100: "表达专业克制，结构服务决策，所有关键结论均有证据和边界",
        },
    },
]

DEFAULT_WEIGHTS = {
    "intent_condition_extraction": 18,
    "financial_semantics_and_caliber": 14,
    "screening_plan_decomposition": 14,
    "tool_usage": 12,
    "result_correctness_and_coverage": 16,
    "ranking_and_decision_actionability": 10,
    "data_logic_time_boundary": 10,
    "composition_credibility": 6,
}

WEIGHT_RULES = []

CAP_RULES = [
    {
        "name": "core_condition_omitted_or_rewritten",
        "label_zh": "核心条件遗漏或改写",
        "label_tag": "核心条件遗漏/改写",
        "severity": "critical",
        "ceiling": 45,
        "description": "遗漏或擅自改写用户的核心筛选条件，导致候选池实质改变。",
    },
    {
        "name": "hard_financial_semantics_or_caliber_error",
        "label_zh": "硬性金融语义或口径错误",
        "label_tag": "金融语义/口径硬错",
        "severity": "critical",
        "ceiling": 45,
        "description": "关键金融指标、交易口径、业务语义或数据可用性判断错误。",
    },
    {
        "name": "unsupported_data_forced_output",
        "label_zh": "不支持数据却强行输出",
        "label_tag": "无数据强行输出",
        "severity": "critical",
        "ceiling": 50,
        "description": "数据不可得、已停更或工具不支持时未说明边界，仍强行给确定结果。",
    },
    {
        "name": "wrong_tool_strategy",
        "label_zh": "错误工具策略",
        "label_tag": "工具策略错误",
        "severity": "critical",
        "ceiling": 55,
        "description": "非标产业/事件/合作关系应搜索却只做结构化查询，或结构化行情条件未用取数工具。",
    },
    {
        "name": "layered_or_temporal_screening_failure",
        "label_zh": "分层或先后筛选失败",
        "label_tag": "分层/先后筛选失败",
        "severity": "critical",
        "ceiling": 55,
        "description": "多阶段筛选、跨领域交集、横盘后突破、前一日/后一日等时序依赖处理失败。",
    },
    {
        "name": "missing_required_ranking_or_fields",
        "label_zh": "遗漏必要排序或字段",
        "label_tag": "遗漏排序/字段",
        "severity": "critical",
        "ceiling": 60,
        "description": "用户明确要求排序、Top N、选一只或指定输出字段，但最终答案未满足。",
    },
    {
        "name": "unverifiable_result_or_data_hallucination",
        "label_zh": "结果不可验证或数据幻觉",
        "label_tag": "结果不可验证/数据幻觉",
        "severity": "critical",
        "ceiling": 50,
        "description": "输出候选股、数值、公式或事实无法从链路证据验证，或与工具结果明显冲突。",
    },
    {
        "name": "chart_or_table_without_decision_value",
        "label_zh": "图表表格无决策价值",
        "label_tag": "图表/表格无决策价值",
        "severity": "warning",
        "ceiling": 65,
        "description": "大量表格、图表或过程说明没有帮助用户判断谁符合条件、为什么排序、下一步怎么用。",
    },
]

ROOT_CAUSE_TAXONOMY = [
    {
        "l1": "intent",
        "l1_zh": "意图理解",
        "description": "是否完整理解长问句条件、否定条件、隐性指令和输出要求。",
        "l2": ["long_query_missed_condition", "hidden_instruction_ignored", "output_requirement_missed"],
    },
    {
        "l1": "semantics",
        "l1_zh": "金融语义",
        "description": "是否正确理解指标、行情、交易、业务和数据口径。",
        "l2": ["metric_caliber_error", "business_rule_misread", "unsupported_data_boundary_missed"],
    },
    {
        "l1": "planning",
        "l1_zh": "筛选规划",
        "description": "是否正确拆解多条件、多阶段、跨领域和先后依赖筛选。",
        "l2": ["no_decomposition", "condition_order_lost", "layered_screening_not_handled"],
    },
    {
        "l1": "tool",
        "l1_zh": "工具信源",
        "description": "是否选对工具、写对输入、读对输出并做必要验证。",
        "l2": ["wrong_tool_selection", "poor_search_keywording", "missing_cross_validation", "tool_output_misread"],
    },
    {
        "l1": "data_logic",
        "l1_zh": "数据逻辑",
        "description": "是否正确处理时间窗口、交易日、公式、分时点位和不可用数据。",
        "l2": ["time_window_error", "formula_error", "unavailable_data_forced"],
    },
    {
        "l1": "result",
        "l1_zh": "结果覆盖",
        "description": "最终候选池、排序、字段、无结果说明是否满足用户要求。",
        "l2": ["missing_candidates", "no_result_not_explained", "ranking_or_field_missing"],
    },
    {
        "l1": "composition",
        "l1_zh": "答案组织",
        "description": "答案是否把过程和数据组织成可信、清楚、可执行的判断。",
        "l2": ["data_dump_no_decision", "overconfident_or_unclear", "chart_without_explanation"],
    },
]

ROOT_CAUSE_DIM_MAP = {
    "intent_condition_extraction": "intent",
    "financial_semantics_and_caliber": "semantics",
    "screening_plan_decomposition": "planning",
    "tool_usage": "tool",
    "result_correctness_and_coverage": "result",
    "ranking_and_decision_actionability": "result",
    "data_logic_time_boundary": "data_logic",
    "composition_credibility": "composition",
}
