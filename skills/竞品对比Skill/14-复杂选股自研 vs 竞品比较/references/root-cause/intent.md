# intent：意图理解

用于解释条件抽取和用户目标理解失败。

L2：
- `long_query_missed_condition`：长问句中遗漏核心硬条件或否定条件。
- `hidden_instruction_ignored`：忽略“尽可能满足”“没有就按最接近选”“剔除泛概念”等隐性执行指令。
- `output_requirement_missed`：遗漏排序、Top N、选一只、完整名单或指定输出字段。

归因时说明被遗漏的原始条件，以及遗漏如何改变候选池或最终可用性。
