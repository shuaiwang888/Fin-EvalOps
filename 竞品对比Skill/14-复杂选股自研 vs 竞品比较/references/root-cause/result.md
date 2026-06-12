# result：结果覆盖

用于解释最终候选池、排序、字段和无结果说明的问题。

L2：
- `missing_candidates`：候选池不完整、无关或来自错误条件。
- `no_result_not_explained`：返回 0 结果但没有解释条件过严、解析失败、数据不可用或真实无结果。
- `ranking_or_field_missing`：排序、Top N、选一只或指定输出字段缺失。

证据应对照用户问题的输出要求和最终答案表格/列表。
