# L1：承接上下文

用于解释多轮对话中没有使用用户补充信息或前轮承诺。

L2：
- `prior_turn_ignored`：历史轮次被忽略。
- `clarification_not_followed`：首轮澄清建立的变量或框架没有在后续使用。
- `user_variables_dropped`：用户补充的成本、仓位、目标价、股票或时间窗被遗漏。
- `context_state_conflict`：答案与上下文已有信息冲突。

证据常来自 `context[N].question`、`context[N].answer`、`text_answer`。
