# 参考文件索引

## 评分细则

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [rubric/_index.md](rubric/_index.md) | 维度列表、动态权重、适用性 | 步骤 0 |
| [rubric/raw-score-scale.md](rubric/raw-score-scale.md) | 六档分制定义（0/20/40/60/80/100） | 步骤 1 |
| [rubric/explicit_instruction_completion.md](rubric/explicit_instruction_completion.md) | 显式指令完成维度评分细则 | 步骤 1 |
| [rubric/task_type_alignment.md](rubric/task_type_alignment.md) | 任务类型对齐维度评分细则 | 步骤 1 |
| [rubric/constraint_coverage.md](rubric/constraint_coverage.md) | 约束覆盖维度评分细则 | 步骤 1 |
| [rubric/answer_focus.md](rubric/answer_focus.md) | 答案焦点维度评分细则 | 步骤 1 |
| [rubric/necessary_information_completeness.md](rubric/necessary_information_completeness.md) | 必要信息完整度维度评分细则 | 步骤 1 |
| [rubric/tool_usage.md](rubric/tool_usage.md) | 工具使用合理性维度评分细则 | 步骤 2 |
| [rubric/cap_primary_instruction_missing.md](rubric/cap_primary_instruction_missing.md) | 主指令缺失封顶规则 | 步骤 3 |
| [rubric/cap_wrong_task_type.md](rubric/cap_wrong_task_type.md) | 任务类型错误封顶规则 | 步骤 3 |
| [rubric/cap_critical_constraint_ignored.md](rubric/cap_critical_constraint_ignored.md) | 关键约束忽略封顶规则 | 步骤 3 |
| [rubric/cap_data_dump_without_instruction_answer.md](rubric/cap_data_dump_without_instruction_answer.md) | 数据堆砌未回答主问封顶规则 | 步骤 3 |
| [rubric/cap_answer_focus_drift.md](rubric/cap_answer_focus_drift.md) | 答案焦点漂移封顶规则 | 步骤 3 |

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
| [root-cause/reasoning.md](root-cause/reasoning.md) | 指令到答案转换根因 | 按需 |
| [root-cause/composition.md](root-cause/composition.md) | 答案组织根因 | 按需 |
| [tool_list/_index.md](tool_list/_index.md) | 工具使用评分参考 | 评分 `tool_usage` 前 |

## 输出契约

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [output-schema_zh.md](output-schema_zh.md) | JSON 输出格式 | 步骤 4 |
| [output-schema_round1_zh.md](output-schema_round1_zh.md) | Round 1 分析输出格式 | 步骤 0-1 |
