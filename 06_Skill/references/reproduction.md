# 人工复现与失效条件

本包自动化只覆盖已有或同口径BIN离线验证。四类经验的交付状态：

|经验|输入/使用|验收|失效条件/状态|
|---|---|---|---|
|BIN Golden|源输入、51系数、5BIN/3dump，运行verify_fir.py|全组长度、误差、dump及返回码|量化近似，非位精确；已有数据自动化回归见TEST_RESULTS|
|AXI DMA|匹配bit/HDF/ELF、N、缓冲、寄存器；按troubleshooting.md人工排查|正常状态与同批导出，错误码停止|缓存/TLAST/超时故障注入、自动恢复未验证|
|HLS II|2019.1、原源码；人工查完整分区/UNROLL/PIPELINE与fir_csynth.rpt|既有II=1及csim记录，不能推导端到端时延|新综合、优化前同条件收益未测试|
|工程移植|工具、IP、BD Tcl、SDK/BSP；独立工作区重建|新日志、bit/HDF/ELF配对、上板与Golden|旧.srcs/HLS路径、Python中间输入、板卡供电/拨码待核；完整重建未执行|

板卡供电、JTAG和启动配置必须依据实际厂家手册人工确认；本包不提供未经核实的电压或接线指令。环境与人工操作索引见[根README](../../README.md)和[硬件说明](../../docs/hardware_setup.md)。操作前保护原工程和数据；不自动调用Vivado/HLS/SDK/XSCT。不宣称L2完整重建或L3新上板已通过。
