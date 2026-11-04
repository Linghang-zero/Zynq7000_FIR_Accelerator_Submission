# FPGA与HLS工程索引

这是规范目录索引，不移动或复制真实工程。

|内容|原位入口|
|---|---|
|HLS算法、系数、testbench|[01_HLS_Accelerator/src](../01_HLS_Accelerator/src/)|
|HLS GUI配置与历史构建脚本|[project](../01_HLS_Accelerator/project/)、[script](../01_HLS_Accelerator/script/)|
|导出IP及驱动|[ip_export](../01_HLS_Accelerator/ip_export/)|
|Vivado XPR|[fir_zynq_system.xpr](../02_Vivado_Hardware/prj/fir_zynq_system.xpr)|
|BD、wrapper及重建Tcl|[bd](../02_Vivado_Hardware/bd/)|
|8个XCI|[ip_config](../02_Vivado_Hardware/ip_config/)|
|bitstream / HDF|[output](../02_Vivado_Hardware/output/)|
|HLS与硬件报告|[HLS report](../01_HLS_Accelerator/report/)、[Vivado report](../02_Vivado_Hardware/report/)|

不新建空的src/build/report伪工程。XPR仍引用未随包保留的.srcs树；HLS历史script.tcl的add_files同样不匹配当前归档布局。IP Repository相对路径存在。配置未改，本副本不宣称可原样一键打开重建；请按根README在包外独立工作目录建工程并重指真实源码。
