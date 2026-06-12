# 事件与概念选股自研 vs 竞品比较评测协议

本协议用于比较**同一 `case_id`（同题配对键）下**自研模型与一个竞品模型的**整体链路 + 最终回答**。它定义了事件/概念选股领域的绝对评分体系（由 rubric、golden cases、root cause 构成），以及 pairwise 比较协议与链路差异解释方法。

## 协议边界

- **绝对评分**：判断单个模型在事件/概念选股任务上答得好不好。
- **横向比较**：
  1. 对同题两边分别做绝对评分；
  2. 再比较自研强项、自研弱项和竞品强项；
  3. 最后用两边完整链路解释这些答案差异是怎么产生的。
- 比较对象不是“两个最终答案”这么窄，而是：
  - 同一用户问题；
  - 两边最终回答；
  - 两边可见整体链路，包括 `chain[*].plan`、`chain[*].tools[*]`、工具输入和工具输出。
- 链路的价值在于解释答案差异，不是脱离答案单独评判“工程美学”。

## 适用范围

仅在以下条件同时满足时使用本协议：
- 题目属于事件/概念驱动的选股、排序、产业映射或受益标的判断任务；
- 输入中存在同一 `case_id` 对应的两份记录；
- 两份记录分别代表自研模型与**一个**竞品模型；
- 当前任务目标是回答：
  - 自研模型相比竞品好在哪里；
  - 自研模型相比竞品差在哪里；
  - 竞品模型哪里值得学习。

不适用于：
- 普通单模型质检；
- 不同问题之间的横向比较；
- 一次同时比较多个竞品模型；
- 只看最终答案、完全不需要链路归因的轻量 benchmark。

## 输入语义

每次评测至少读取：
- `case_id`：同题配对键（自研与竞品共享）；
- 用户问题；
- 自研模型完整记录；
- 竞品模型完整记录。

### 最终答案锚点

- 自研模型：优先使用 `text_answer` 作为最终答案主锚点；
- 竞品模型：若 `text_answer` 为空，则使用 `answer` 作为最终答案主锚点；
- 若编排层已提前生成统一字段，可直接读取归一化后的最终答案，但不得因此改变原始证据指针。

### 真实链路结构

- `tool_usage` 是**评测维度名**，不是输入 JSON 的字段名；
- 真实工具调用从 `chain[N].tools[M]` 读取；
- 顶层 `tools` 字段即便存在，也可能为空，不能把它当成主要链路来源；
- 自研记录通常是多步 `chain`，`plan` 较完整；
- 竞品记录可能只有一个 `chain` step，`plan` 为空，但 `chain[0].tools` 仍包含可用的工具调用证据。

详细规则见：
- [references/comparison_protocol.md](references/comparison_protocol.md)
- [references/whole_chain_comparison.md](references/whole_chain_comparison.md)

## 执行协议

0. **先分析题目，建立共享评测框架**
   阅读 [references/rubric/_index.md](references/rubric/_index.md)，仅依据用户问题判断维度适用性并分配动态权重。
   同一题下，自研与竞品必须使用**同一套**适用性和权重，避免把权重差异误当成模型差异。
   同时阅读 [references/golden_cases/_index.md](references/golden_cases/_index.md) 与 [references/golden_cases/image_annotation_anchors.md](references/golden_cases/image_annotation_anchors.md)，命中专家案例时使用对应 hard checks。

1. **先分别做绝对评分**
   对自研与竞品分别按本 skill 定义的 8 个维度评分：
   - `intent_fulfillment`
   - `event_abstraction`
   - `industry_mapping`
   - `ranking_judgment`
   - `logic_closure`
   - `timeliness_fact_boundary`
   - `credibility_expression`
   - `tool_usage`

   除 `tool_usage` 外，先只依据用户问题和各自最终答案评分；不得因为另一方更差，就抬高本方绝对分。

2. **再分别诊断两边整体链路**
   阅读 [references/root-cause/_index.md](references/root-cause/_index.md)、[references/tool_list/_index.md](references/tool_list/_index.md) 和 [references/whole_chain_comparison.md](references/whole_chain_comparison.md)。
   对两边分别检查：
   - 工具选择是否正确；
   - 查询输入是否贴合任务；
   - 证据是否覆盖了题目真正需要的维度；
   - 是否有交叉验证；
   - 工具结果是否真正转化成了更好的最终答案。

   当 `plan` 存在时，可结合其判断意图和推理；当 `plan` 为空时，不强行编造“推理文本”归因，优先依据工具行为、证据流和最终答案做判断。

3. **最后做 pairwise 比较**
   阅读 [references/comparison_protocol.md](references/comparison_protocol.md)。
   在双方绝对评分完成后，逐维比较：
   - 自研真正做得好的地方；
   - 自研真正落后的地方；
   - 竞品真正值得学习的地方；
   - 双方共同失败点；
   - 哪些链路差异导致了最终答案差异。

   比较时必须坚持：
   - **先绝对、后相对**：双方都差时，先写共同短板，再写谁相对更好；
   - **答案与链路合看**：答案决定质量，链路解释质量是怎么形成的；
   - **证据优先**：每条优势、弱点和学习点都要绑定最终答案或链路证据；
   - **不做多模型聚合**：本协议一次只比较一个竞品，跨竞品总结由后续汇总层完成。

4. **序列化输出**
   阅读 [references/output-schema_zh.md](references/output-schema_zh.md)。
   先输出结构化 JSON，再附简短自然语言评审。

## 保守评分

- 自研与竞品使用同一维度、同一权重、同一 hard checks；
- 不因为相对胜负而改变绝对评分；
- 不因为链路看起来繁复就自动加分；
- 若链路更好但最终答案没有兑现，优点只能记为链路信号，不能替代答案质量；
- 若双方都没有真正完成用户任务，必须明确输出共同不足，不能把“谁稍微好一点”写成高质量答案。

## 安全护栏

本 skill 的评分安全护栏，尤其包括：
- 严肃对待“最受益”“领涨”“排序”“核心标的”等隐含优先级任务；
- 严肃对待最新、最近、截至某日等时间边界；
- 惩罚数据堆砌、概念罗列和只会取数；
- 要求硬证据支撑产能、订单、市占率、客户供货、成本、技术壁垒等断言；
- 区分主营/副业、直接/间接、核心/边缘、品牌/代工、上游/下游等实体边界；
- 对 A 股映射海外标杆保持克制，不能强行凑相似；
- 事件题先看事件贴合度和受益纯度，再看行情热度。

## 参考索引

通过 [references/MANIFEST.md](references/MANIFEST.md) 按需读取子文件。
