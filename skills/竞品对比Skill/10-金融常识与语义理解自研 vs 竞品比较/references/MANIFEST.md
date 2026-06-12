# 参考文件索引

本文件是金融常识与语义理解自研 vs 竞品比较评测协议的导航地图。

- **绝对评分层**：rubric、golden cases、root cause、tool list 提供单模型绝对评分标准。
- **compare 专属层**：comparison protocol 与 whole-chain comparison 负责定义同题比较和整体链路差异解释。

## compare 专属参考

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [comparison_protocol.md](comparison_protocol.md) | 定义 pairwise 比较流程、先绝对后相对、我方优劣/竞品优点/shared failures 判定规则 | 步骤 3 比较前必读 |
| [whole_chain_comparison.md](whole_chain_comparison.md) | 说明真实输入结构、答案锚点、`chain[*].tools[*]` 读取路径和整体链路差异解释方法 | 步骤 2 链路诊断前必读 |

## 评分细则（rubric/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [rubric/_index.md](rubric/_index.md) | 维度列表、动态权重、适用性和关键扣分方向 | 步骤 0 |
| [rubric/raw-score-scale.md](rubric/raw-score-scale.md) | 六档原始分量表 | 步骤 1 |
| [rubric/cap_rules.md](rubric/cap_rules.md) | 封顶规则 | 步骤 3 封顶时 |

## 专家案例

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [golden_cases/_index.md](golden_cases/_index.md) | 专家文本案例 hard checks | 步骤 0 |
| [golden_cases/image_annotation_anchors.md](golden_cases/image_annotation_anchors.md) | docx 图片和截图中的补充锚点 | 步骤 0 |

## 根因与工具

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [root-cause/_index.md](root-cause/_index.md) | 根因选择规则 | 步骤 2 |
| [root-cause/intent.md](root-cause/intent.md) | 意图理解根因 | 按需 |
| [root-cause/evidence.md](root-cause/evidence.md) | 信息证据根因 | 按需 |
| [root-cause/tool.md](root-cause/tool.md) | 工具策略根因 | 按需 |
| [root-cause/reasoning.md](root-cause/reasoning.md) | 金融语义推理根因 | 按需 |
| [root-cause/composition.md](root-cause/composition.md) | 答案组织根因 | 按需 |
| [tool_list/_index.md](tool_list/_index.md) | 工具使用评分参考与工具详细规则入口 | 评分 `tool_usage` 前 |
| [tool_list/search.md](tool_list/search.md) | Search 搜索工具用法规则 | 按需 |
| [tool_list/finquery.md](tool_list/finquery.md) | FinQuery 金融查询工具用法规则 | 按需 |
| [tool_list/backtest.md](tool_list/backtest.md) | BackTest 回测工具用法规则 | 按需 |
| [tool_list/forecast.md](tool_list/forecast.md) | Forecast 预测工具用法规则 | 按需 |
| [tool_list/accessingfulltext.md](tool_list/accessingfulltext.md) | AccessingFullText 全文阅读工具用法规则 | 按需 |
| [tool_list/searchimage.md](tool_list/searchimage.md) | SearchImage 搜图工具用法规则 | 按需 |
| [tool_list/customerservicefaq.md](tool_list/customerservicefaq.md) | CustomerServiceFAQ 客服工具用法规则 | 按需 |
| [tool_list/saveuserprofile.md](tool_list/saveuserprofile.md) | SaveUserProfile 用户画像工具用法规则 | 按需 |
| [tool_list/codeinterpreter.md](tool_list/codeinterpreter.md) | CodeInterpreter 计算工具用法规则 | 按需 |

## 输出契约

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [output-schema_round1_zh.md](output-schema_round1_zh.md) | Round 1：同题校验、共享权重、两边证据摘要 | 步骤 0 后 |
| [output-schema_zh.md](output-schema_zh.md) | Pairwise JSON 输出契约、双边证据对象和比较结论格式 | 步骤 4 序列化时 |

## 关键依赖

- 步骤 0 题目分析 → 依赖 `rubric/_index.md` + `golden_cases/_index.md` + `golden_cases/image_annotation_anchors.md`
- `tool_usage` 维度评分 → 依赖 `whole_chain_comparison.md` + `tool_list/_index.md`；真实工具调用从 `chain[*].tools[*]` 读取
- 根因 L2 的选择 → 依赖 `root-cause/_index.md` 和对应 L1 文件
- 封顶规则触发 → 依赖 `rubric/cap_rules.md`

## 协议步骤到文件的映射

| 协议步骤 | 操作 | 读取文件 |
|---|---|---|
| 步骤 0：分析题目 | 适用性判断 + 动态权重 + 案例命中 | `rubric/_index.md` + `golden_cases/_index.md` + `golden_cases/image_annotation_anchors.md` |
| 步骤 1：分别做绝对评分 | 逐维度评分（仅活跃维度） | `rubric/_index.md` + `rubric/raw-score-scale.md` |
| 步骤 2：诊断整体链路 | tool_usage 评分 + 整体链路差异解释 + 根因选择 | `whole_chain_comparison.md` + `tool_list/_index.md` + `root-cause/_index.md` + 对应 L1 文件 |
| 步骤 3：封顶与逐维比较 | 封顶检查 + 先绝对后相对，输出我方优势/弱点、竞品优点、shared failures | `rubric/cap_rules.md` + `comparison_protocol.md` |
| 步骤 4：序列化输出 | 双边绝对评分 + 逐维比较 + 自然语言 | `output-schema_zh.md` |
