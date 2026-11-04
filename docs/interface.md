# PS PL接口定义

|通路|实际端口|协议与用途|
|---|---|---|
|PS配置|M_AXI_GP0 → ps7_0_axi_periph → DMA S_AXI_LITE / FIR s_axi_CTRL|AXI4-Lite寄存器控制；DMA基址0x40400000，FIR基址0x43C00000|
|DDR读|DMA M_AXI_MM2S → axi_smc/S00_AXI → M00_AXI → PS S_AXI_HP0|AXI存储映射；MM2S读取TxBuffer|
|输入流|DMA M_AXIS_MM2S → fir_0/in_r|32位AXI4-Stream；TDATA承载float32位模式|
|输出流|fir_0/out_r → DMA S_AXIS_S2MM|32位AXI4-Stream；S2MM写回RxBuffer|

HLS axis_t为ap_axiu<32,1,1,1>；TVAlID/TREADY握手控制流，TLAST标识最后样本。核心内部使用定点计算，不能把流上float32位模式等同于内部浮点计算。每次N=1000，缓冲区4000字节，TxBuffer/RxBuffer按64字节对齐。HLS每次调用清零history。

main.c的hw_fir_run(input)依次复制输入、清接收区、flush两区、设置N/禁用自动重启、先启动S2MM、启动FIR、启动MM2S、轮询双通道完成、invalidate接收缓存。TIMEOUT_LIMIT=100000000；接收启动失败返回-5，发送启动失败-6，超时-7。test_status记录失败；成功完成全部软硬件测试后为4。未实现中断驱动或自动重试。

FCLK_CLK0配置50 MHz，统一驱动DMA/FIR/互联；proc_sys_reset分发复位。运行期实测频率未独立测量。PS读取耗时用A9 Global Timer，不能据此反推PL频率。

依据：[main.c](../03_SDK_Software/fir_test/src/main.c)、[fir.cpp](../01_HLS_Accelerator/src/fir.cpp)、[BD脚本](../02_Vivado_Hardware/bd/fir_system_bd.tcl)。BIN为1000个小端IEEE-754 float32，见[测试输出](../04_Test_Evidence/output/)；SDK内存导出不属于FPGA端到端计时。
