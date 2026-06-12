# data_logic：数据逻辑

用于解释时间、交易日、公式、分时、区间和不可用数据边界问题。

L2：
- `time_window_error`：日期、交易日、前 N 日、区间起止、分时 K 线时间点错误。
- `formula_error`：MACD、均线、回撤、涨跌幅、量价关系等公式或计算口径错误。
- `unavailable_data_forced`：数据不可用或低频更新时仍强行输出确定结果。

归因时说明正确口径和错误口径的差异。
