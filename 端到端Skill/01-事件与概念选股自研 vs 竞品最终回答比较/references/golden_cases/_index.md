# 专家案例基准

本文件沉淀专家文档中的高频评判锚点。评分时先判断用户问题是否与下列案例语义匹配；匹配时，将对应 hard checks 作为证据核验清单。不要因为答案表面流畅、篇幅很长或包装完整而放松这些检查。

## 使用规则

- 语义匹配即可使用，不要求用户问题逐字相同。
- hard checks 优先于泛化表述：如果答案违反 hard checks，应在相应维度扣分并按需触发封顶规则。
- 已给出明确日期、口径或公式的案例，必须据此核验；未给出最终数值的案例，重点核验事件抽象质量、产业链映射、排序逻辑和逻辑闭环。
- 专家评价中的核心失败模式（如"舍本逐末、只有数据罗列"、"逻辑描述不清晰"、"主观含糊"）应映射到对应维度扣分。

## Case 1: 算力涨价概念股

hard checks:
- 必须提取算力涨价背后的真正驱动因素（如 AI 训练需求激增、GPU 供给瓶颈、数据中心扩建周期），不能仅罗列算力概念股。
- 必须区分核心受益（GPU/芯片设计、先进封装）与边缘受益（PCB、连接器、散热），给出排序依据。
- 仅甩出一张代码+涨跌幅的冰冷表格，缺失个股与题材挂钩的逻辑，应扣 `intent_fulfillment` 和 `logic_closure`。

主要维度：`event_abstraction`, `ranking_judgment`, `logic_closure`

专家评价要点：问财"舍本逐末，缺少逻辑解读，只有数据罗列"，应扣 `logic_closure` 和 `credibility_expression`。

## Case 2: 先进封测产业链上游设备材料标的

hard checks:
- 必须映射产业链层级：设备（光刻、刻蚀、检测）→ 材料（光刻胶、靶材、CMP）→ 封装测试，不能仅给出封装测试公司。
- 必须区分"上游设备/材料"与"中游封装"，用户明确要求的是上游标的。
- 需要理清产业链的高价值点、高盈亏比点、高胜率点，结合行业逻辑、细分赛道逻辑、个股逻辑三者表述。

主要维度：`industry_mapping`, `logic_closure`, `intent_fulfillment`

专家评价要点：问财"分析结构对比豆包不够清晰"，隐藏需求是理清产业链高价值点，应扣 `industry_mapping`。

## Case 3: 原粮售卖最相关的股票

hard checks:
- 必须区分种植/销售粮食的公司 vs 粮食加工/研发型公司，用户明确"不要研发，而是种植粮食，销售粮食"。
- 不能仅做简单概念罗列，需结合个股主营产品和年报数据确认业务相关性。
- 行情数据与明细研报结合不深、只会念数据时，应扣 `logic_closure`。

主要维度：`intent_fulfillment`, `industry_mapping`, `logic_closure`

专家评价要点：问财"行情数据与明细研报、报告数据结合不深，只会念数据"，应扣 `logic_closure`。

## Case 4: 美军封锁伊朗港口——最利好哪些股并排序

hard checks:
- 必须提供完整的因果链：地缘冲突 → 油价/航运/军工/避险 → 具体行业 → 个股。
- 用户明确要求"从最利好到一般"排序，必须给出排序标准（如受益纯度、盈利弹性、确定性）。
- 个股逻辑描述不清晰、缺少推荐度排序、内容描述含糊且主观时，应触发 `missing_required_ranking` 或扣 `ranking_judgment`。

主要维度：`ranking_judgment`, `logic_closure`, `event_abstraction`

专家评价要点：问财"个股逻辑描述不清晰，板块内推荐个股时缺少推荐度排序，内容描述含糊且主观"。

## Case 5: 国民党主席访问大陆——海峡两岸概念股领涨

hard checks:
- 必须基于最新事件（4月7日访问）进行分析，不能引用过时的历史事件。
- 必须结合当前市场走势和两岸关系最新动态，时效性是关键。
- 同花顺产品矩阵间的逻辑没对齐（异动提醒与推荐个股逻辑矛盾）时，应扣 `credibility_expression`。

主要维度：`timeliness_fact_boundary`, `event_abstraction`, `ranking_judgment`

专家评价要点：问财"对个股的逻辑整理只会照本宣科"，产品矩阵逻辑不一致影响信任。

## Case 6: 美以伊战争——受影响优质科技股排序并说明核心理由

hard checks:
- 必须按可投资价值排序，每个股票需逐个说明核心理由。
- 需分析战争影响程度（局部冲突 vs 全面升级），不同情景下的受益逻辑不同。
- 前半段分析惊艳但后续数据佐证逻辑敷衍（虎头蛇尾），应扣 `logic_closure`。

主要维度：`ranking_judgment`, `logic_closure`, `event_abstraction`

专家评价要点：问财"结合行情数据效果前半段够惊艳，后续数据分析佐证逻辑敷衍，总体虎头蛇尾"。

## Case 7: 最近一两天有哪些新闻导致A股潜在爆发

hard checks:
- 必须使用实时新闻数据，不能引用过时资讯或调研报告。用户明确要求"最近一两天"的"新闻或事件"。
- 必须按事件重大程度和个股可能爆发幅度双维度排序。
- 用研报冒充新闻、用通用概念材料替代事件证据时，应触发 `wrong_evidence_type` 封顶规则。

主要维度：`timeliness_fact_boundary`, `credibility_expression`, `ranking_judgment`

专家评价要点：问财"过度主观表述，资讯内容以次充好"，"用户明确要求新闻、事件，引用的内容又是调研报告"，应触发 `wrong_evidence_type`。

## Case 8: 中美产业链博弈——受益上市公司

hard checks:
- 必须识别具体的受限领域（芯片、AI、量子、先进制造）和对应国产替代方向。
- 需完整因果链：美国限制措施 → 受影响产业链环节 → 中国应对政策 → 受益上市公司。
- 行文描述说一半藏一半、没有可信度时，应扣 `credibility_expression`。

主要维度：`event_abstraction`, `industry_mapping`, `logic_closure`

专家评价要点：问财"行文描述说一半藏一半，没有可信度，哪些市场研究？强调的逻辑是什么？都没有说明"。

## Case 9: 蓝箭航天上市——关联公司受益排序

hard checks:
- 必须按受益强度排序关联公司，区分直接参股、供应链合作、概念关联。
- 应分析股价上市前后的表现趋势。
- 只有数据罗列而缺少逻辑解读时，应扣 `logic_closure`。

主要维度：`ranking_judgment`, `intent_fulfillment`, `logic_closure`

专家评价要点：问财"舍本逐末，缺少逻辑解读，只有数据罗列"。

## Case 10: 国资委国有资本投向方向

hard checks:
- 必须超越简单名单罗列，解释国有资本的政策方向、重点领域和投资逻辑。
- 需从政策文件 → 投向方向 → 行业 → 个股的完整逻辑链。
- 问财胜出场景：结合结构化取数给出全市场明细数据、由点及面时效果好。应确认是否发挥了此优势。

主要维度：`logic_closure`, `intent_fulfillment`, `industry_mapping`

专家评价要点：问财唯一胜出场景——"结合结构化取数给出全市场明细数据，由点及面效果更好"。

## Case 11: 纤维素醚用途与产能最高公司

hard checks:
- 必须先拆解纤维素醚下游应用与行业格局，再落到公司；行业总产值、全球/国内产能格局应先于单一公司结论。
- 产能最高不能只看 A 股单一标的；需要国内外产能对比、市场地位和公司口径。
- 只给山东赫达等单一标的而缺少全球/国内对照，不能满足"产能最高的公司有哪些"。

主要维度：`industry_mapping`, `logic_closure`, `intent_fulfillment`

## Case 12: 石墨负极材料多条件筛选

hard checks:
- 对订单多、耐用、安全、成本低、技术强、现金流强、市占率高等条件，必须用外部资料与基本面数据交叉支撑。
- 经营现金流、毛利率、研发费率只能覆盖部分条件；若忽略订单、产品质量和市占率，应扣分。
- 需要结构化对比各标的的市占率、订单、技术、成本、现金流，而非只给概念股名单。

主要维度：`intent_fulfillment`, `logic_closure`, `credibility_expression`

## Case 13: 航天工程碳纤维材料股票

hard checks:
- 必须聚焦航天工程用碳纤维材料，按产业链环节和航天应用场景分组。
- 个股描述需要市占率、产能、核心技术、航天应用场景或市场地位等硬证据。
- 只做概念性表述、缺少优先级区分，应扣 `ranking_judgment` 和 `credibility_expression`。

主要维度：`industry_mapping`, `logic_closure`, `ranking_judgment`

## Case 14: 光纤板块给谷歌供货个股

hard checks:
- 必须区分直接供货、间接供货、供应链相关和概念相关。
- 需要说明供货产品、客户关系、市场份额或业务占比；仅模糊说"相关"不够。
- 对供货关系不能只靠概念标签或行情表现证明。

主要维度：`industry_mapping`, `credibility_expression`, `logic_closure`

## Case 15: 机器人用空心杯电机设计制造龙头

hard checks:
- 必须正确理解"机器人用空心杯电机"，不能泛化成机器人整机或普通电机。
- 需要国内/全球龙头、量产规格、市占率、客户、应用场景等对比。
- 误解"机器人"实体边界时，应考虑 `forced_mapping_or_entity_boundary_error`。

主要维度：`intent_fulfillment`, `industry_mapping`, `credibility_expression`

## Case 16: HBM 存储芯片业绩弹性最大

hard checks:
- 必须围绕 HBM 的需求爆发、技术升级、供给瓶颈、价格/市场规模/巨头市占率拆解投资逻辑。
- A 股产业链要按材料、设备、封装、测试、存储配套等环节说明业绩弹性。
- 只停留在概念介绍、缺少 2026 年市场规模/价格/市占率等关键量化证据，应明显扣分。

主要维度：`event_abstraction`, `industry_mapping`, `ranking_judgment`, `logic_closure`

## Case 17: 华为昇腾产业链核心标的

hard checks:
- 必须清晰梳理昇腾产业链环节，并区分板块中军、弹性小票、核心供应商和弱关联公司。
- 不能把指数权重与市值分布伪装成两个实质不同的逻辑。
- 个股逻辑应有业务链路或数据支撑，不能仅列概念。

主要维度：`industry_mapping`, `ranking_judgment`, `logic_closure`

## Case 18: 钯金上涨利好上市公司

hard checks:
- 必须说明钯金价格上涨对上游资源、中游加工、回收、下游催化剂等环节的不同影响。
- 不能只给回收端逻辑；需梳理上下游产业结论。
- 个股需要受益方向、资源/业务暴露和弹性差异。

主要维度：`industry_mapping`, `event_abstraction`, `ranking_judgment`

## Case 19: 光模块上游材料成本占比与国产替代

hard checks:
- "上游材料"应按整个上游产业链产品理解，不能狭义化为单一材料。
- 必须列明各层级成本占比、技术壁垒、国产化率和主要上市公司。
- 云南锗业等个股若被提及，应说明良率、客户、产品环节等具体证据。

主要维度：`industry_mapping`, `logic_closure`, `credibility_expression`

## Case 20: 氨纶涨价最受益公司

hard checks:
- 核心判断标准应是涨价对利润弹性的传导：产能、自产原料、价差、成本结构和业务占比。
- 不能只聚焦少数龙头而遗漏二三线弹性标的对比。
- 需要实际氨纶价格波动或价差数据支撑；主观数据幻觉也要扣分。

主要维度：`event_abstraction`, `ranking_judgment`, `logic_closure`

## Case 21: 国家重点六张网建设受惠主板公司

hard checks:
- 必须遵守用户"主板"约束，不能多余补充创业板并混入核心表格。
- 行业壁垒和核心竞争力需要用量化或业务证据定义，不能只贴标签。
- 开放题允许多路径答案，但表格逻辑必须自洽，不得误导。

主要维度：`intent_fulfillment`, `industry_mapping`, `credibility_expression`

## Case 22: 历届世界杯概念最强三只股票及表现

hard checks:
- 必须先确定历届世界杯时间窗口，再核验对应区间涨跌幅；错误涨幅属于硬事实错误。
- 不能只查体育产业概念成分股；应结合搜索识别当时被市场热炒的世界杯概念股。
- 推理链应是事件窗口 → 热炒题材范围 → 区间表现 → 前三标的。

主要维度：`timeliness_fact_boundary`, `credibility_expression`, `logic_closure`

## Case 23: 电影《寒战1994》出品上市公司

hard checks:
- 必须给出核心答案，同时区分第一出品方、主控方、联合出品方及其上市公司关系。
- 不能只给一个简单结论而遗漏事件涉及的公司关系。
- 结论排版应清晰，避免字多但核心事件信息不足。

主要维度：`intent_fulfillment`, `industry_mapping`, `credibility_expression`

## Case 24: 三星罢工事件利好国产芯片

hard checks:
- 必须说明事件背景、影响程度和发酵阶段，判断是短期扰动还是长期供需变化。
- 需要从三星受影响环节推到国产替代或供应链受益环节，再到个股。
- 缺少事件影响程度分析会降低后续个股定位可信度。

主要维度：`event_abstraction`, `industry_mapping`, `logic_closure`

## Case 25: 华为 AI 芯片销量激增、英伟达在华业务遇阻

hard checks:
- 必须拆解两个驱动：华为昇腾/国产 AI 芯片需求上行，以及英伟达在华供给/政策受限。
- 个股逻辑需要详实数据或业务证据，不能只说一半或含糊带过。
- 应区分芯片设计、算力服务器、整机、生态软件、封测、供应链等受益层级。

主要维度：`event_abstraction`, `industry_mapping`, `logic_closure`

## Case 26: 算电协同绿电直供项目投运

hard checks:
- 必须围绕新闻中的风光储同源、绿电直供、算力园区降本和电网稳定性推导。
- 相关股票应优先映射绿电供给侧、储能、电力设备、园区能源管理等直接环节；直接跳到算力硬件通常链条过远。
- 事件后续发酵链路若像硬凑，应扣 `event_abstraction` 和 `logic_closure`。

主要维度：`event_abstraction`, `industry_mapping`, `logic_closure`

## Case 27: 长征十号乙首飞利好商业航天

hard checks:
- 必须先看事件相关度和受益纯度，再看资金流、弹性、换手等行情辅助指标。
- 过度依赖行情片面指标来选事件标的，是本末倒置。
- 应说明首飞事件对应火箭制造、发动机、测控、材料、卫星互联网或发射服务等链条。

主要维度：`event_abstraction`, `ranking_judgment`, `industry_mapping`

## Case 28: 谷歌/亚马逊自研 AI 芯片利好 A 股

hard checks:
- 必须拆解海外事件的核心逻辑：自研 TPU/Trainium、AI 芯片订单、云资本开支、光模块/PCB/先进封装/服务器链条。
- 核心个股不能只粗略列出；每个股票应说明对应环节、影响程度和量化支撑。
- 如果前半段框架好但个股理由粗糙，扣 `logic_closure`。

主要维度：`event_abstraction`, `industry_mapping`, `logic_closure`

## Case 29: A 股商业航天最像 SpaceX/马斯克

hard checks:
- 必须先说明 SpaceX 的业务范围和护城河，再比较 A 股公司的业务范围、订单、发射/火箭/卫星能力。
- 需要给出 2026 年可确定订单或明确无法确认的口径。
- 只给对标结论但缺少详细理由，答案立不住。

主要维度：`industry_mapping`, `logic_closure`, `credibility_expression`

## Case 30: 复制山东墨龙式中东战争炒作

hard checks:
- 用户核心不是找油气板块本身，而是找山东墨龙式的地缘冲突赚钱效应复制。
- 必须说明山东墨龙及港股在事件中的涨幅、发酵路径、市场记忆和可复制条件。
- 股票过多、环节发酵程度不排序、个股逻辑含糊，应扣 `ranking_judgment`。

主要维度：`intent_fulfillment`, `event_abstraction`, `ranking_judgment`

## Case 31: 中国股票媲美美股七朵金花

hard checks:
- 必须给出 A 股/港股与美股核心科技股的精确对标表，并解释中美产业结构差异。
- 多套版本可以作为辅助，但必须收敛成可执行主表和权重/理由。
- 分类混乱、宽泛推演、碎片化，会降低实操价值。

主要维度：`industry_mapping`, `logic_closure`, `credibility_expression`

## Case 32: 国内是否有谷歌可比公司

hard checks:
- 合格答案应先指出没有一家中国公司能 100% 复制谷歌全貌，再拆解搜索广告、云、AI、安卓/生态、视频等维度对标。
- 个股总结不能只谈对标点，必须细化强弱差距和量化支撑。
- 明确差异不是扣分点；不说明差异或强行完全对标才扣分。

主要维度：`industry_mapping`, `logic_closure`, `credibility_expression`

## Case 33: 储能+锂电+AI 基建与德业股份关系

hard checks:
- 必须用德业股份业务板块、逆变器/储能收入、毛利率、行业对比、市值、催化和股价表现说明关系。
- 回测德业股价与储能指数只能解释走势共振，不能替代基本面链条。
- 应回答"和德业股份有关系吗"的直接关系强弱，而非泛谈板块轮动。

主要维度：`intent_fulfillment`, `logic_closure`, `credibility_expression`

## Case 34: Anthropic 与中国哪家大模型公司更像

hard checks:
- 不能只按"安全"单一维度比较；需比较定位、模型能力、商业化、客户结构、生态、融资/估值、产品形态。
- 必须覆盖市场主流候选，而非只列一个预设对象。
- 为契合预设结论强行解释不匹配证据，应扣 `credibility_expression` 和 `forced-analogy`。

主要维度：`intent_fulfillment`, `industry_mapping`, `credibility_expression`

## Case 35: A 股映射美股 CPU 巨头英特尔

hard checks:
- 必须拆解英特尔产业链地位、CPU/晶圆制造/封装/服务器生态，并判断 A 股公司是产业链同位、供应链绑定还是业绩共振。
- 最终回答不能只给泛泛资料；应体现基本面、业务占比、客户/合作关系等可核验依据。
- 缺少硬数据支撑或核心标的壁垒分析，应扣 `credibility_expression` 与 `logic_closure`。

主要维度：`industry_mapping`, `credibility_expression`, `logic_closure`

## Case 36: 今年4月美股 AI 硬件核心票涨幅最大及 A 股映射

hard checks:
- 必须正确识别当月美股 AI 硬件涨幅最大的核心票，并处理"今年4月"时间窗口。
- A 股映射不仅是同产业链地位，也包括合作关系和业绩增长共振。
- 从 AI 硬件/数据中心泛化理解，未定位具体映射逻辑，应扣 `intent_fulfillment`。

主要维度：`timeliness_fact_boundary`, `industry_mapping`, `logic_closure`

## Case 37: 映射谷歌财报逻辑的国内公司

hard checks:
- 必须提取题干核心逻辑：AI 落地、云增长、利润率稳定、资本开支可控、回购/股息或基本盘稳健。
- 可按三个或更多指标拆解国内公司，且要说明每家公司对应哪条逻辑。
- 对主观词过度编造结果会降低可信度；表格更丰富不代表自动高分。

主要维度：`event_abstraction`, `industry_mapping`, `credibility_expression`

## Case 38: 国内对标闪迪、美光、西部数据

hard checks:
- 必须先说明 A 股没有完全对标这些海外存储品牌厂的公司，再分维度给出可比公司。
- 不能把代工厂当作西部数据这类品牌/技术壁垒公司对标；商业模式差异是关键。
- 概念纠偏和边界说明应加分。

主要维度：`industry_mapping`, `credibility_expression`, `intent_fulfillment`

## Case 39: 根据描述识别覆铜板公司

hard checks:
- 必须识别公司并用搜索/资料补充证明其符合描述，如全球市占率、M8/M9、高频高速材料、英伟达认证、800G/1.6T、泰国基地等。
- 只给结论不给论据，或话只说一半，应扣 `credibility_expression`。
- 若题干描述指向生益科技，应围绕各条件逐条核验。

主要维度：`intent_fulfillment`, `credibility_expression`, `logic_closure`

## Case 40: 一品红与美国关联股票代码

hard checks:
- 必须直接给出正确股票代码，并解释"与美国有关联"所指事件或公司关系。
- 字数更多但核心事件描述只有一句，不算高质量。
- 简单事实题也要结构清晰：结论、依据、相关公司/代码。

主要维度：`intent_fulfillment`, `credibility_expression`, `logic_closure`

## 跨案例判分锚点

当用户问题未命中具体案例时，仍按以下锚点评估：

- **结构化取数是优势，不是答案本身**：全市场扫描、概念成分、行情和财务数据可作为第一轮筛选，但必须转译成题材逻辑、个股理由和主次排序。
- **概念脱水与梯队划分是核心**：好答案要主动梳理题材分支，区分纯正主营、核心供应、边缘副产、概念蹭边，并帮助用户锁定龙头、中军、弹性票。
- **非标产业事实必须可验证**：主营产品、产业链、事件新闻、消息、客户供货、认证、订单、产能等强时效或非结构化信息，最终回答必须给出足够清楚的证据口径。
- **量化证据要贴着结论**：市场规模、价格涨幅、产能、市占率、订单、成本、现金流、良率、客户、股价事件窗口表现等数据，必须解释其如何支撑排序或投资逻辑。
- **事件相关度优先于行情热度**：事件炒作先看事件贴合度、受益纯度和赚钱效应复制，再看涨幅、成交、资金流、换手和弹性。
- **实体边界错是高危问题**：NER/Linking、主营/副业、直接/间接、品牌/代工、上游/下游、国内/全球口径错，会直接破坏答案可信度。
- **克制比迎合更可信**：对海外巨头映射、"最像谁"、"最高/最大/最强"等问题，明确没有完全对标并分维度比较，通常优于强行给一个看似漂亮但错误的结论。
- **图片人工批注补充**：若题目涉及特高压+柔直、两会、溴素、铜、SOFC、美股机器人，或答案存在复杂图表、交易性价比、非标产业事实、实体链接边界等问题，继续读取 [image_annotation_anchors.md](image_annotation_anchors.md) 使用补充 hard checks。
