# 基于Zynq-7000的51抽头FIR软硬件协同设计

ARM Cortex-A9负责控制与软件FIR基准，Zynq-7020 PL执行HLS FIR加速，AXI DMA搬运DDR与FIR之间的数据。PC端只做Python离线验证；本项目没有AI PC模型推理端。

## 架构与核心技术

DDR → SmartConnect/PS HP0 → DMA MM2S → FIR AXI4-Stream → DMA S2MM → SmartConnect/PS HP0 → DDR。PS通过GP0及AXI-Lite配置DMA和FIR。DMA/FIR位于PL；PS仍参与缓冲准备、缓存维护和等待。

51抽头对称低通；内部定点计算，AXI4-Stream承载float32位模式；HLS样本循环II=1。26个乘法表达式中h[0]=0的一组被消除，剩余24组配对及中心抽头对应25个DSP48E1，中心抽头占1个DSP。系统2个BRAM属于DMA FIFO，FIR无BRAM。PL为50 MHz/20 ns，HLS目标100 MHz/10 ns，不混用阶段。

## 目录索引

|规范入口|说明与真实文件位置|
|---|---|
|[docs](docs/architecture.md)|架构、接口与硬件搭建说明|
|[fpga](fpga/README.md)|索引01_HLS_Accelerator与02_Vivado_Hardware，不移动工程|
|[host](host/README.md)|索引03_SDK_Software、04_Test_Evidence/python_verify及05_Docs/compare.py|
|[metrics](metrics/README.md)|指标CSV及原始证据索引|
|[06_Skill](06_Skill/README.md)|可交付离线验证Skill：5组BIN/3个dump与8项回归；硬件步骤仍需人工|
|[skill](skill/README.md)|历史工程经验清单，保留其原验证边界|
|[report](report/README.md)|正式设计报告定版 DOCX/PDF、版本与改动范围|

原有01_HLS_Accelerator、02_Vivado_Hardware、03_SDK_Software、04_Test_Evidence、05_Docs全部原位保留。_PENDING为本机候选材料，仍受现有.gitignore排除。旧报告及过期记录已移至项目外备份，内部审计不纳入公开文件；报告相关的未闭环事项见[report/README.md](report/README.md)。

## 性能与资源

测试1000点、ARM Cortex-A9单核-O0；最终计时批次为图12对应的SDK Expressions截图。

|指标|正弦|混频|
|---|---:|---:|
|ARM纯计算耗时|2469.3239 μs|2468.7209 μs|
|FPGA+DMA端到端耗时|96.2880 μs|95.5110 μs|
|耗时对照比|约25.65倍|约25.85倍|
|最大绝对误差（compare.py参考模型）|2.194196×10⁻⁶|2.980232×10⁻⁶|

最大绝对误差统一不超过3.0×10⁻⁶，误差>0.001点数均0。两端计时口径不同，不是严格同口径加速比。HLS/浮点Golden/量化Golden误差不可混用。全系统实现阶段：7084 Slice LUTs、8010 Slice Registers、2 Block RAM、25 DSP；WNS=8.855 ns、WHS=0.036 ns、TNS=THS=0，保持余量较小。数据与阶段见[metrics.csv](metrics/metrics.csv)，证据见[metrics说明](metrics/README.md)。

## 环境依赖

Windows，Vivado 2019.1、Vivado HLS 2019.1、Xilinx SDK 2019.1；器件xc7z020clg400-2；Xilinx JTAG驱动。compare.py仅需Python3标准库。队友验证脚本需要numpy/scipy/matplotlib，版本未锁定，完整运行还缺中间输入。开发板供电和启动设置见[hardware_setup](docs/hardware_setup.md)，精确板型与跳线需人工确认。

## 从零复现流程与验证边界

下列是按已有代码编写的操作步骤，未在本归档副本完成独立全流程重建；路径静态检查不等于构建成功。本次整理没有运行Xilinx工具或板卡。所有会产生文件的步骤应在包外新建工作目录执行，不能覆盖本归档。

1. **准备与基线**：保存项目副本，确认五个原工程目录完整；核对[主应用](03_SDK_Software/fir_test/src/main.c)、[输入数组](03_SDK_Software/fir_test/src/fir_test_inputs.h)、[HLS系数](01_HLS_Accelerator/src/fir.cpp)、5个BIN。板卡供电/JTAG按厂家手册搭建。
2. **先验证已有数据**：推荐运行 `python -B 06_Skill/scripts/verify_fir.py --project .`，严格检查5组BIN、3个dump及返回码；用法和实测记录见[Skill入口](06_Skill/SKILL.md)与[测试结果](06_Skill/TEST_RESULTS.md)。也可在项目根目录运行 `python 05_Docs/compare.py`。应比较正弦/混频的V1.0及性能版各1000点，最大误差约2.194196e-6/2.980232e-6，超0.001为0；提供dump的组应逐字一致。该脚本不重跑板卡，输出末尾“约2×10⁻⁶”是历史措辞，以实际数值和本README上界为准。
3. **HLS重建**：在Vivado HLS 2019.1 GUI新建包外工程，顶层fir，器件xc7z020clg400-2，添加原src/fir.cpp为设计、src/fir_test.cpp为testbench；testbench以`__FILE__`定位`../data/`下的`input_signal.txt`/`expected_output.txt`，保持src与data同级即可，无需改任何路径（另备`../data/`、`../../data/`、`data/`三个工作目录相对候选），设置目标10 ns、uncertainty 12.5%，运行C Simulation、C Synthesis，再按需C/RTL Co-simulation及IP Catalog导出。源码中的pragma保持不变。历史script.tcl使用fir_hls/fir.cpp旧布局，不能在现目录直接无修改执行；本次未修改脚本或生成替代构建文件。新导出只放包外，原ip_export继续保留。
4. **Vivado重建**：在Vivado 2019.1新建包外RTL工程，器件xc7z020clg400-2，IP Repository添加原01_HLS_Accelerator/ip_export。在新工程Tcl Console执行 `source {<项目>/02_Vivado_Hardware/bd/fir_system_bd.tcl}`，执行validate_bd_design，Generate Output Products，生成HDL wrapper并设fir_system_wrapper为top；核对PS FCLK0=50 MHz、HP0、DMA Simple双通道、MM2S/S2MM与FIR连接。不要把独立fir_0/fir_1候选混入BD。运行综合、实现、时序/DRC检查，通过后仅在新工作区生成bitstream并Export Hardware（SDK2019.1用HDF，不是XSA）。原XPR仍依赖缺失的.srcs布局，不作为已验证的一键入口；若BD Tcl重建失败，记录报错由团队确认，不改原归档。
5. **SDK编译**：新建包外workspace，导入原硬件平台、fir_test_bsp及fir_test三工程，或用新导出HDF创建硬件平台，保持工程名与BSP依赖一致。确认自定义drivers/fir_v1_0注册，按system.mss重新生成standalone BSP，核对DMA/FIR设备ID。只编译main.c，排除main_v1.0.c，否则重复main；选择-O0并检查lscript.ld的DDR布局。构建ELF保存到工作区，候选ELF不默认为正式版。上述编译步骤尚未独立验证。
6. **下载运行**：Hardware Manager下载已有或新工作区确认过的bitstream；SDK系统调试执行PS初始化并下载匹配HDF/bitstream的ELF，选择Cortex-A9 #0。干净运行至test_status=4，再暂停读取sw_sine_us/sw_mixed_us/hw_sine_us/hw_mixed_us；不要混配不同运行。性能窗口见main.c；导出BIN不计入计时。
7. **导出与对比**：使用SDK符号定位RxBuffer，从Memory视图导出4000字节小端数据。当前main.c第二次硬件测试会覆盖第一次RxBuffer；正弦结果应在第二次调用前暂停导出，混频在第二次结束导出，不能把同一RxBuffer当成两组数据。板测Tcl中的硬编码地址仅对当时ELF有效，新链接必须按符号重查。保存新结果到包外，再按compare.py同口径比对。原5个BIN和截图不得覆盖。
8. **Python波形链路**：先读[python_verify/README](04_Test_Evidence/python_verify/README.md)。完整脚本不能直接当成已验证的一键命令：signal.npy/t.npy/clean.npy缺失，ref_sine.csv未在脚本生成，部分性能常数为旧批次。可在包外补齐后按Cell顺序运行并核对模型；本次不生成或猜造缺失输入。

## 已知限制与竞赛适配

- XPR/HLS历史脚本路径与归档布局不完全匹配；原配置保持，独立重建仍待验证。
- 唯一正式报告：[Word](report/FIR技术报告_最终版.docx)、[PDF](report/FIR技术报告_最终版.pdf)，版本与用途见[报告说明](report/README.md)。
- 旧报告及历史清单已移至项目外备份。公开证据边界见[硬件证据说明](06_Skill/references/hardware_evidence.md)，不将历史审计当作新的实验。
- 已整理后期AI核查摘要与真实用户问题选段，见[AI证据索引](06_Skill/references/ai_evidence.md)；仍缺完整原始会话和早期开发记录。没有严格同口径性能对比或优化前指标，不得推断。
- 图片中“AI PC模型推理”相关条款与本项目现有能力不匹配，须向赛事确认适用性，不能虚构AI PC端。失败分析、前人工作关联及供电启动细节仍需补证。
- 文档属性中作者/最后修改者为网络昵称；本机审计与Git历史仍可能含路径线索，本次未清理历史、未公开发布。
