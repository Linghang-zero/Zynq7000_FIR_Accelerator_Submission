# 硬件搭建与环境

目标器件xc7z020clg400-2，Windows，Vivado/Vivado HLS/Xilinx SDK 2019.1。板卡精确商品型号、供电电压/电流、JTAG跳线及启动拨码尚无完整可核实清单，请按实物板厂家手册确认，不能直接套用其他Zynq板配置。

1. 断电核对板卡型号、极性、电源额定值和厂家建议，确认JTAG启动设置。
2. 连接合适的板卡电源、USB-JTAG与PC，安装Xilinx cable驱动。在Vivado Hardware Manager确认可识别目标xc7z020。
3. 使用独立工作目录操作，给目标下载[已有bitstream](../02_Vivado_Hardware/output/fir_system_wrapper.bit)，保留原文件。SDK导入包内硬件平台与BSP/应用，详情见[根README](../README.md)。
4. SDK连接Cortex-A9 #0，依硬件平台ps7_init.tcl完成PS初始化，再下载自行确认或重新编译的ELF。候选ELF未定版，不能仅按文件名认定。
5. 干净运行后暂停，查看test_status=4以及sw_sine_us/sw_mixed_us/hw_sine_us/hw_mixed_us。不要以“等待5秒”本身代替完成状态判断。

没有外接传感器、执行器或AI PC推理连接的已验证实现。本说明不新增此类接口。原始板测记录和截图见[测试证据](../04_Test_Evidence/)。没有本次新增板测，供电/启动设置与独立重建验证仍需团队完成。
