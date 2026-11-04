# 系统架构与数据流

本项目为ARM Cortex-A9与Zynq PL的51抽头FIR软硬件协同实现，PC仅用于离线Python验证，不包含AI PC模型推理端。

```text
PS DDR → HP0 / SmartConnect → DMA MM2S → FIR in_r
                                            ↓
PS DDR ← HP0 / SmartConnect ← DMA S2MM ← FIR out_r
PS M_AXI_GP0 → ps7_0_axi_periph → DMA S_AXI_LITE / FIR s_axi_CTRL
```

DMA、FIR、SmartConnect均位于PL。DDR访问使用AXI存储映射，DMA与FIR之间使用32位AXI4-Stream。PS准备缓冲区、配置与等待DMA；DMA承担批量数据搬运，不能将整个端到端通路描述为无CPU参与。

FIR为51抽头对称低通，25组配对加中心抽头共26个乘法表达式；h[0]=0的一组被消除，24组配对加中心抽头映射25个DSP48E1。FIR无BRAM，历史数据使用LUTRAM；系统2个BRAM归DMA的两通道FIFO。PL配置50 MHz/20 ns，HLS目标100 MHz/10 ns，二者阶段不同。

源码与证据：[HLS算法](../01_HLS_Accelerator/src/fir.cpp)、[BD连接Tcl](../02_Vivado_Hardware/bd/fir_system_bd.tcl)、[资源报告](../02_Vivado_Hardware/report/fir_system_wrapper_utilization_placed.rpt)、[时序报告](../02_Vivado_Hardware/report/fir_system_wrapper_timing_summary_routed.rpt)、[指标说明](../metrics/README.md)、[正式报告](../report/README.md)。其中 FIR IP 独立综合（OOC）的 3053 LUT / 25 DSP / 0 BRAM 来自原工程 OOC 报告，该报告未随包，包内无法独立复核。
