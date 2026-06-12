# 复合意图类问题自研 vs 竞品比较评测协议

本协议用于比较**同一 `case_id`（同题配对键）下**自研模型与一个竞品模型在复合意图类金融问题上的**整体链路 + 最终回答**。它保留 `06-compound-intent` 的绝对评分体系（rubric、golden cases、root cause、tool list、cap rules），只增加 pairwise 比较协议和链路差异解释方法。

## 协议边界

- **绝对评分**：判断单个模型是否正确拆解复合意图、覆盖关键子任务、整合多源证据并形成可执行结论。
- **横向比较**：
  1. 对同题两边分别做绝对评分；
  2. 再比较自研强项、自研弱项和竞品强项；
  3. 最后用两边完整链路解释这些答案差异是怎么产生的。
- 比较对象不是“两个最终答案”这么窄，而是：
  - 同一用户问题；
  - 两边最终回答；
  - 两边可见整体链路，包括 `chain[*].plan`、`chain[*].tools[*]`、工具输入和工具输出；
  - 可用的截图 OCR、人工批注和线上维度信号。
- 链路的价值在于解释答案差异，不是脱离答案单独评判“工程美学”。

## 适用范围

仅在以下条件同时满足时使用本协议：
- 题目属于复合意图或复杂投研推理任务；
- 输入中存在同一 `case_id` 对应的两份记录；
- 两份记录分别代表自研模型与**一个**竞品模型；
- 当前任务目标是回答：
  - 自研模型相比竞品好在哪里；
  - 自研模型相比竞品差在哪里；
  - 竞品模型哪里值得学习。

复合意图类问题包括：
- 一句话包含多个子任务、多个时间窗口、多个资产/公司/行业或多个输出要求；
- 复杂问句，尤其是字数较长、包含“现状/未来/影响/传导/策略/标的/估值/利润/案例/怎么做”等多层要求；
- 深度调研、行业竞争格局、产业链映射、事件影响评估、热点板块归纳、复杂交易方案；
- 需要把行情、新闻、公告、产业、政策、财务、资金、舆情等多源信息串成统一投资结论。

不适用于：
- 普通单模型质检；
- 不同问题之间的横向比较；
- 一次同时比较多个竞品模型；
- 纯单一意图的行情查询、单步取数计算、普通 KYC 推荐、简单事件概念选股或客服问题；
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
- 竞品记录可能只有一个 `chain` step，`plan` 为空，但 `chain[0].tools` 仍包含可用的工具调用证据；

详细规则见：
- [references/comparison_protocol.md](references/comparison_protocol.md)
- [references/whole_chain_comparison.md](references/whole_chain_comparison.md)

## 执行协议

0. **先分析题目，建立共享评测框架**
   阅读 [references/rubric/_index.md](references/rubric/_index.md)，仅依据用户问题、必要 `context` 和已提供的线上维度信号判断维度适用性并分配动态权重。
   同一题下，自研与竞品必须使用**同一套**适用性和权重，避免把权重差异误当成模型差异。
   同时阅读 [references/golden_cases/_index.md](references/golden_cases/_index.md) 与 [references/golden_cases/image_output_anchors.md](references/golden_cases/image_output_anchors.md)，命中专家案例、截图 OCR、人工批注或竞品对比摘要时使用对应 hard checks。

1. **先分别做绝对评分**
   对自研与竞品分别按本 skill 定义的 8 个维度评分：
   - `intent_decomposition`
   - `task_coverage_priority`
   - `multi_source_evidence_integration`
   - `analysis_chain_closure`
   - `data_logic_rigor`
   - `decision_actionability`
   - `composition_readability`
   - `tool_usage`

   除 `tool_usage` 外，先只依据用户问题、必要 `context`、各自最终答案评分；不得因为另一方更差，就抬高本方绝对分。每个活跃维度的 `raw_score` 必须取六档值：0/20/40/60/80/100。

2. **再分别诊断两边整体链路**
   阅读 [references/root-cause/_index.md](references/root-cause/_index.md)、[references/tool_list/_index.md](references/tool_list/_index.md) 和 [references/whole_chain_comparison.md](references/whole_chain_comparison.md)。
   对两边分别检查：
   - 是否正确拆解复合子任务；
   - 子任务覆盖是否完整、主次是否合理；
   - 工具选择是否正确；
   - 查询输入是否贴合任务；
   - 证据是否覆盖了题目真正需要的行情、新闻、公告、产业、政策、财务、资金或案例信息；
   - 是否处理时间窗口、数据口径、案例真实性和冲突证据；
   - 工具结果是否真正转化成了更完整、更严谨、更可执行的最终答案；

   当 `plan` 存在时，可结合其判断意图拆解、任务排序和推理闭环；当 `plan` 为空时，不强行编造“推理文本”归因，优先依据工具行为、证据流和最终答案做判断。

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
- 若双方都没有真正完成用户任务，必须明确输出共同不足，不能把“谁稍微好一点”写成高质量答案；
- 若一方覆盖了更多子任务但主任务判断错误，不能只按覆盖面判胜；

## 安全护栏

本 skill 的评分安全护栏，尤其包括：
- 先拆复合任务，不先套固定题型；
- 严惩漏答关键子任务、主次关系错位和把次要信息写成主结论；
- 严惩资料拼盘替代综合结论；
- 严肃对待时间窗口、数据口径、计算逻辑、案例真实性和事实边界；
- 要求多源证据真正整合，而不是并排罗列；
- 用户要求影响、传导、策略、怎么做、哪个最好时，必须形成事实、影响、传导和决策闭环；
- 截图型或 OCR 型输入中若出现人工批注，必须作为高优先级专家信号处理。

## 参考索引

通过 [references/MANIFEST.md](references/MANIFEST.md) 按需读取子文件。
