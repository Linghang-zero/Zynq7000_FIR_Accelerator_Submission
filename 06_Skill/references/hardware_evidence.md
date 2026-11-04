# 公开硬件证据与原审计结论的边界

本文件是索引说明，不是新的综合报告或板测结果。原VIVADO_AUDIT及历史修改记录为内部工作资料，不纳入公开包；这里保留报告所需的核查结论和可公开复查的实际文件。

## DSP与BRAM

- [fir.cpp](../../01_HLS_Accelerator/src/fir.cpp)：51抽头、25组对称配对及中心抽头，共26个乘法表达式；h[0]=0，第0对乘法恒零。
- [导出RTL](../../01_HLS_Accelerator/ip_export/hdl/verilog/fir.v)：保留25个乘法器，原审计以位宽分布核对24组非零对称乘法和中心抽头。中心抽头占1个DSP的解释来自这条静态证据链，未在本次重新综合。
- [全系统Fully Placed资源报告](../../02_Vivado_Hardware/report/fir_system_wrapper_utilization_placed.rpt)：7084 LUT、8010寄存器、2个Block RAM、25个DSP。
- FIR IP OOC的3053 LUT、25 DSP、0 BRAM来自原工程的独立综合报告。该原报告未随包，公开包无法独立复核全部OOC数字；本说明不冒充原始OOC报告。
- 原审计记录2个BRAM属于DMA MM2S/S2MM数据FIFO，FIR历史存储映射LUTRAM；相应详细实现日志在原工程，不以系统总资源表单独证明归属。

## 时序与时钟

[布线时序报告](../../02_Vivado_Hardware/report/fir_system_wrapper_timing_summary_routed.rpt)保留WNS=8.855 ns、WHS=0.036 ns、TNS/THS=0，20 ns时钟约束；[BD Tcl](../../02_Vivado_Hardware/bd/fir_system_bd.tcl)和[时钟报告](../../02_Vivado_Hardware/report/fir_system_wrapper_clock_utilization_routed.rpt)支持50 MHz配置。HLS的10 ns为综合目标，不是板上独立测频。

## AI协作材料

旧稿曾写“现有资源统计不能单独确定中心抽头的具体硬件映射”，后按用户提供审计修正。这是后期协作摘要，不是完整AI原始回答。提示选段及缺失材料见[AI索引](ai_evidence.md)；采用结果见[正式报告](../../report/README.md)。
