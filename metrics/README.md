# 指标与证据索引

[metrics.csv](metrics.csv)为本次整理的定版指标表。耗时采用报告图12的SDK Expressions同屏批次，不重新计算或混配其他运行。performance_ratio是耗时对照比，不是严格同口径加速比：ARM只计-O0纯FIR计算，FPGA计输入准备、缓存维护、DMA、FIR与完成等待。

资源区分全系统Fully Placed、FIR IP OOC与HLS估算；没有优化前资源基线。FIR OOC原始报告位于原工程、未纳入提交包，因此 3053 LUT / 25 DSP / 0 BRAM 一行在包内无法独立复核，不另造替代报告。

- [最终性能截图](../04_Test_Evidence/screenshots/性能测试_SDK_Expressions_20261024.png)
- [原始日志](../04_Test_Evidence/logs/)、[5个BIN](../04_Test_Evidence/output/)、[dump](../04_Test_Evidence/dumps/)、[截图](../04_Test_Evidence/screenshots/)
- [资源报告](../02_Vivado_Hardware/report/fir_system_wrapper_utilization_placed.rpt)、[时序报告](../02_Vivado_Hardware/report/fir_system_wrapper_timing_summary_routed.rpt)
- [复算脚本](../05_Docs/compare.py)、[历史验证程序](../04_Test_Evidence/python_verify/)

不复制logs/scripts/evidence，避免证据重复及分叉。数值误差行采用compare.py参考模型的已有复算，不等于位精确HLS模拟；其他Python浮点Golden会产生不同误差，应保留模型说明。
