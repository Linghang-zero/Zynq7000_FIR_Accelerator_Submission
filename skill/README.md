# 可复用开发经验

本文件记录工程经验，不是可自动执行或已验证的Codex Skill，不含SKILL.md或自动化能力承诺。

|主题|问题背景|解决方法|验证方式|适用边界|
|---|---|---|---|---|
|HLS II优化|逐样本FIR需提高吞吐|对称抽头配对、history完整分区、配对循环UNROLL、样本循环PIPELINE II=1|既有fir_csynth.rpt的achieved/target II=1及csim日志|HLS报告为模块阶段，不能用II推算PS端到端耗时；无优化前基线|
|AXI DMA调试|未先接收、TLAST/长度或缓存不一致会阻塞/读旧数据|按hw_fir_run先S2MM后FIR/MM2S；4000字节、flush/invalidate、轮询超时|已有test_status/完成样本、BIN与dump一致性|硬编码调试地址仅适配当时ELF，重新链接后必须重定位；未验证自动恢复|
|Vivado移植|归档布局不同于工程生成目录|保留原配置；在独立工作目录登记IP repo、从BD Tcl建立BD、核对wrapper和器件|本次只做路径静态检查；移植成功仍需重建验证|XPR的.srcs源文件缺失引用尚在，不能宣称原包一键复现|
|Python Golden|字节序、零初态、定点参考口径影响误差|按小端float32解析1000点；零填充因果FIR；固定输入/系数；区分浮点与量化模型|compare.py对4组BIN复算及dump逐字一致|compare.py非位精确ap_fixed仿真；不自动修复Notebook缺依赖|

依据：[HLS源码](../01_HLS_Accelerator/src/fir.cpp)、[SDK应用](../03_SDK_Software/fir_test/src/main.c)、[HLS报告](../01_HLS_Accelerator/report/fir_csynth.rpt)、[复算脚本](../05_Docs/compare.py)。未虚构AI辅助设计记录、自动优化搜索或优化前后收益。
