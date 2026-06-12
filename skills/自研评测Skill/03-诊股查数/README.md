# 03-诊股查数 Skill

> 自研模型「诊股查数」类问题的端到端评测协议，沉淀诊股、数据查询、对比分析与轻量诊断的评分细则与根因归因体系。

---

## 一、Skill 定位与目标

**核心使命**：用稳定协议评测自研模型在「诊股查数」场景下的**最终答案质量**和**完整链路质量**。

**关键定位**：

- **主锚点**：`text_answer`（最终答案）—— 盲评打分
- **辅助证据**：`chain`（完整规划链路）—— 工具评分、效率判断、根因归因
- **设计哲学**：「**查对一个字段不等于好答案**」—— 诊股查数类问题需要完成金融用户真正关心的**口径、对比、解释、可操作观察点**。

---

## 二、目录结构

```
03-诊股查数/
├── README.md                       # 本文件
├── SKILL_zh.md                     # 协议主文档（适用场景+执行步骤+保守评分原则）
├── scripts/
│   ├── __init__.py                 # 空文件
│   └── rule.py                     # Python 规则定义（10 维度 + 7 封顶 + 5 L1 根因）
└── references/
    ├── MANIFEST.md                 # 文件导航地图
    ├── output-schema_zh.md         # JSON 输出契约（v1）
    ├── output-schema_round1_zh.md  # Round 1 自然语言报告格式
    ├── rubric/                     # 评分细则（10 维度 + 7 封顶）
    │   ├── _index.md               # 维度列表+动态权重规则
    │   ├── raw-score-scale.md      # 六档分制 0/20/40/60/80/100
    │   ├── [10 个维度文件]
    │   └── cap_*.md                # 7 个封顶规则
    ├── golden_cases/               # 21 个专家案例 + 图片锚点
    │   ├── _index.md               # Case 1-21 + 跨案例判分锚点
    │   └── image_annotation_anchors.md
    ├── root-cause/                 # 根因归因体系（5 个 L1 阶段）
    │   ├── _index.md               # 阶段总览+证据规则+置信度
    │   ├── intent.md  evidence.md  tool.md  reasoning.md  composition.md
    └── tool_list/                  # 9 个工具的用法规范
```

---

## 三、5 步执行协议

| 步骤 | 动作 | 关键产出 |
|---|---|---|
| **步骤 0** | 分析题目 + 动态分配权重 | `weight_assignment`（总和=100）、命中 golden case |
| **步骤 1** | 盲评最终答案（不看链路） | 各维度 `raw_score` + `evidence`（不计算加权分） |
| **步骤 2** | 链路诊断 + 根因归因 | `tool_usage` 评分 + `root_causes` 列表 |
| **步骤 3** | 应用封顶规则 | `caps` 数组（限制最终分，不替代维度评分） |
| **步骤 4** | 序列化 JSON 输出 | 按 `output-schema_zh.md` 格式输出 |

---

## 四、10 个评分维度

| 维度 | 默认权重 | 适用性 | 核心关注 |
|---|---:|---|---|
| `intent_fulfillment` 意图满足度 | 12 | **始终 relevant** | 显性任务+隐含意图（主力/筹码/增长点/止盈位） |
| `data_accuracy_coverage` 数据准确与覆盖 | 18 | **始终 relevant** | 数据值、样本、标的、年份、字段是否正确完整 |
| `time_caliber_precision` 时间口径粒度 | 12 | relevant / supplementary | 交易日、复权、单位、汇率、分时、合约 |
| `calculation_comparison` 计算与对比 | 10 | relevant / supplementary / NA | 涨跌幅、差值、跑赢、比价、排序 |
| `analysis_framework_fit` 分析框架匹配 | 16 | relevant / supplementary / NA | **核心**：市场常用框架（主力双层、筹码五要素等） |
| `insight_extension` 延伸洞察 | 10 | relevant / supplementary / NA | 多周期、多维扩展、增量信息、可操作观察点 |
| `result_verifiability` 结果可验证性 | 8 | relevant / supplementary | 来源、明细、公式、证据类型 |
| `presentation_visualization` 呈现与可视化 | 5 | relevant / supplementary | 表格、图表、结论前置 |
| `tool_usage` 工具使用合理性 | 6 | **始终 relevant** | 工具选择、参数、约束处理（链路阶段评分） |
| `latency_efficiency` 响应耗时 | 3 | relevant / supplementary / NA | 无证据给中性分 60；简单题慢要扣分 |

**权重关键规则**：

- 总和必须 = 100
- `not_applicable` 维度权重 = 0，评分阶段跳过
- `supplementary` 维度 ≤ 5
- 权重分配要附 `rationale`

**六档分制（raw-score-scale）**：

- `100` 完美满足；`80` 极轻微不足；`60` 基本满足；`40` 关键缺失；`20` 仅触及边角；`0` 完全未响应
- 加权公式：`加权分 = raw_score / 100 × dynamic_weight`

---

## 五、7 个封顶规则（cap rules）

| 规则 | 上限 | 触发场景 |
|---|---:|---|
| `hard_data_or_fact_error` 硬性数据错误 | **35** | 核心数据值/标的/客户/价格/宏观指标明显错误；空结果但实际有符合标的；编造 |
| `missing_required_data` 必要数据缺失 | **60** | 用户明确要求的关键数据未给出；样本明显不全；只答部分子任务 |
| `time_or_caliber_error` 时间/口径错误 | **45** | 交易日/自然日错；前 N 日、前 N 年锚点错；汇率/合约/复权/分红日类型错 |
| `intraday_precision_missing` 日内精度缺失 | **55** | 用户要求分时/分钟区间但用日线/全天成交额替代 |
| `wrong_analysis_framework` 分析框架错误 | **55** | 主力只看资金流；筹码只看集中度 90；止盈只给一个价；增长点答成存量业务 |
| `data_dump_without_insight` 数据堆砌无洞察 | **65** | 诊断题只堆数据无结论；图表多但没转译为判断 |
| `unverifiable_or_fabricated_result` 不可验证/编造 | **50** | 精确结论无任何可定位证据；工具输出空仍声称查到 |

**多个封顶同时触发取最低上限**。封顶不替代维度评分，更好的隐藏规划不豁免最终答案触发的封顶。

---

## 六、5 个 L1 根因归因体系

```
intent（理解问题）
├── surface-query-only          表层取数，未识别诊断语义
├── subtask-missed              遗漏子任务（只列数据不算差值）
├── scope-constraint-missed     忽略标的/时间/市场/条件约束
└── ambiguous-time-not-resolved 模糊时间未锚定

evidence（检索数据/证据）
├── wrong-data-value            数据值/字段/标的错误
├── data-depth-insufficient     历史深度不足
├── data-completeness-gap       覆盖不全
├── nonpublic-source-gap        非公开资料无补充
├── stale-evidence              使用过期数据
└── source-quality-weak         来源质量弱

tool（选择与执行工具）
├── wrong-tool-selection        用错工具
├── tool-input-error            参数/标的/口径错误
├── tool-limit-not-handled      上限未处理（如 500 根 K 线）
├── sql-condition-parse-error   SQL 条件解析错（如「一个月前上市」）
├── missing-cross-check         空结果未二次核验
└── inefficient-tool-strategy   反复无效查询

reasoning（计算与金融推理）
├── calculation-error           计算错误
├── time-caliber-reasoning-error 时间口径推理错
├── market-framework-mismatch   框架错位
├── incremental-vs-stock-confusion 存量当增长点
├── comparison-not-synthesized  对比未转化为差异
└── causal-chain-incomplete     缺少因果链

composition（组织答案）
├── detail-omission             缺少关键明细
├── process-hidden              过程隐藏
├── format-degradation          呈现差
├── chart-without-interpretation 有图无解释
└── overly-terse-answer         诊断题过短
```

**选择规则**：按 raw_score 升序 + 权重降序排序；最多 8 个根因；活跃维度 raw_score ≥ 60 且无封顶时允许空数组。每个根因必须绑定证据，置信度分 high/medium/low 三档。

---

## 七、21 个专家案例（golden cases）覆盖的题型

| 类别 | 典型案例 |
|---|---|
| **分红类** | Case 1 上市以来每年分红；Case 2 同花顺/东财分红总额对比；Case 5 兴业银行什么时候分红 |
| **行情/涨跌幅** | Case 3 过去 5 年每年涨跌幅对比 |
| **资金/主力** | Case 7 新奥股份 4 月 10 日主力 |
| **筹码** | Case 8 春秋电子筹码集中度 |
| **增长点** | Case 9 英威腾未来增长点 |
| **技术指标** | Case 10 分钟区间买卖金额；Case 11 粤传媒乖离率 |
| **商品/期货** | Case 6 内外盘原油比价；Case 12 黄金价格 |
| **宏观** | Case 13 A 股开户数；Case 14 新能源车渗透率 |
| **行业** | Case 15 2026 年 3 月跑赢沪深 300 的行业板块 |
| **止盈位** | Case 16 瑞尔特止盈位 |
| **概念/热词** | Case 17 张雪机车 |
| **全市场条件** | Case 18 一个月前上市今日涨 7% 非 ST 非科创；Case 19 连续 500 根 K 线收盘>10 元；Case 20 长江电力连续 5 年蓄能电量；Case 21 5 月 6 日前 5 日累计涨幅>10% |

**跨案例判分锚点（7 条共识）**：

1. 数据正确只是及格线
2. 简单题：准确 + 完整 + 快
3. 对比题：必须给差异 / 排序 / 强弱 / 口径
4. 诊断题：必须把字段转译为市场判断
5. 非结构化资料题：不能只依赖结构化库
6. SQL/工具问题：条件解析、时间推移、上限兜底、空结果不复核是主要硬伤
7. 模糊问句：应合理推断并说明假设

---

## 八、关键评分原则（保守评分）

SKILL_zh.md 中明确列出的「保守评分」原则，是这个 skill 的**灵魂**：

1. **不是查到一个字段就结束** —— 必须完成显性任务 + 补足金融用户真正关心的口径、对比、解释、可操作观察点
2. **数据准确优先于表达** —— 客观数据题：数据准确/时间口径/样本完整性 > 表达；图表和延伸分析只能加分，不能覆盖核心错误
3. **诊断题必须用市场常用框架** —— 例如筹码集中度看**股东户数变化 + 大股东持股 + 机构持仓 + 筹码分布**，不是孤立搬冷门字段
4. **"主力"等多义词必须覆盖真实语义** —— 大资金 + 龙虎榜/知名席位
5. **"增长点"要关注增量变化** —— 客户突破/市占率/新订单/新业务边际改善/调研纪要；只说原有业务优秀是**存量信息**
6. **"止盈位"不能只给一个价格** —— 至少说明技术位 + 基本面/消息面 + 风险收益比 + 仓位或持仓目标 + 必要时追问成本和周期
7. **跨市场品种必须讲清口径** —— 价格/单位/汇率/内外盘价差/基差/合约差异；用经验汇率或模糊规则应扣分
8. **全市场条件查询要严肃检查 SQL** —— 上市时间/连续 K 线/节假日前 N 个交易日/「一共涨幅」易被错解
9. **数据缺口要诚实** —— 主动用搜索/公告/研报/调研纪要补充；仍无法取得时明确局限，不得编造

---

## 九、9 个工具的定位与使用规则

| 工具 | 核心用途 | 关键规范 |
|---|---|---|
| **FinQuery** | 金融数据查询（核心） | 条件选股须原句输入；>5 指标需拆分并行；支持明确时间范围；**不支持抽象时间** |
| **Search** | 搜索非结构化数据 | 关键词 ≤ 5 个；可分多次 |
| **BackTest** | 事件/策略回测 | 自然语言输入；无结果时策略类终止、事件类可换工具 |
| **Forecast** | 个股未来表现预测 | **仅支持单只股票** |
| **AccessingFullText** | 深度阅读网页 | 输入为 url 列表 |
| **SearchImage** | 搜图 | 关键词 ≤ 5 个；图片直接展示 |
| **CustomerServiceFAQ** | 同花顺 APP 使用问题 | **仅** 客服问题；条件选股/诊股/评价类不可用 |
| **SaveUserProfile** | 保存用户画像 | 仅用户主动披露偏好/财务背景时使用 |
| **CodeInterpreter** | Python 沙箱计算/可视化 | 30 秒时限；保留运行状态 |

**工具失败归因映射**（来自 `image_annotation_anchors.md`）：

- SQL/条件解析错误 → `tool/sql-condition-parse-error`
- 取数上限或接口缺失 → `tool/tool-limit-not-handled` 或 `evidence/data-completeness-gap`
- linking 错误 → `tool/tool-input-error` 或 `evidence/wrong-data-value`
- 指标配置/覆盖问题 → `evidence/data-completeness-gap` 或 `tool/wrong-tool-selection`
- 长问句拆解失败 → `intent/subtask-missed` 或 `reasoning/comparison-not-synthesized`

---

## 十、JSON 输出契约

**schema_version** = `stock-diagnosis-data-lookup/v1`

**核心字段**：

- `weight_assignment`：所有 10 维度的适用性 + 动态权重 + 理由（总和=100）
- `skipped_dimensions`：not_applicable 列表
- `matched_golden_cases`：命中的 case + 使用的 hard checks
- `dimension_scores`：仅含活跃维度的 raw_score（0/20/40/60/80/100）+ evidence
- `caps`：触发的封顶 + 重要未触发的封顶
- `root_causes`：有序数组（L1 + L2 + dimension + confidence + summary + evidence）
- `narrative_review`：简短可执行（summary / strengths / weaknesses / next_actions）

**不输出**：`weighted_points`、`absolute_score_pre_cap`、`final_score`（由调用方计算）

**证据对象**：`{source, pointer, summary}` 三元组；`source` 限定 8 种类型（question / final_answer / context / reasoning / function_call / function_call_output / timing / online_signal）。

---

## 十一、与代码实现的对接（scripts/rule.py）

`rule.py` 提供了与 JSON 输出完全对齐的 Python 数据结构：

- `DIMENSIONS`：10 个维度的 `key`、`label_zh`、`description`、`six_level_anchors`（六档制描述）
- `DEFAULT_WEIGHTS`：默认权重（与 `rubric/_index.md` 一致）
- `CAP_RULES`：7 个封顶的 name / label_zh / severity / ceiling / description
- `ROOT_CAUSE_TAXONOMY`：5 个 L1（简版，l2 较精简版）
- `ROOT_CAUSE_DIM_MAP`：10 维度 → 5 L1 的映射
  - `intent_fulfillment → intent`
  - `data_accuracy_coverage / time_caliber_precision → evidence`
  - `calculation_comparison / analysis_framework_fit / insight_extension → reasoning`
  - `result_verifiability / presentation_visualization → composition`
  - `tool_usage / latency_efficiency → tool`

**`CONFIDENCE_THRESHOLD = 3`**：根因置信度阈值。

---

## 十二、与其他 skill 的边界

- ❌ **不适用**：事件/概念驱动选股、重度投顾推荐、KYC 适配、纯财报归因、复杂策略回测、客服问答
- ✅ **重计算回测收益类问题**：优先用「回测取数计算」skill
- 与 01-选股类、02-回测类等 skill 形成互补：本 skill 偏**诊股 + 查数 + 轻量诊断**

---

## 快速上手 Checklist

1. 评测时**先看 SKILL_zh.md 的「保守评分」9 条** —— 评分哲学的总纲
2. **步骤 0** 必读 `rubric/_index.md` + `golden_cases/_index.md` 确定权重和案例命中
3. **步骤 1** 用「六档制 + 证据绑定」盲评最终答案
4. **步骤 2** 必须阅读 `chain`，定位根因到 5 个 L1 之一
5. **步骤 3** 检查 7 个封顶，取最低上限
6. **步骤 4** 按 `output-schema_zh.md` 输出 JSON，可选附简短自然语言评审

**核心方法论**：「数据准确只是及格线，**框架匹配 + 多周期连续 + 增量洞察**才是好答案」。
