---
name: zynq7000-fir-verify
description: 验证 Zynq-7000 固定 51 抽头 FIR 的小端 float32 BIN，复用项目量化参考程序进行严格长度和逐点误差验收，并提供人工 DMA 排查流程。用于离线验证和复现准备，不执行硬件构建、下载或自动恢复。
---

# Zynq-7000 FIR 验证与复现 Skill

## 输入与适用范围

Python 3.9+（标准库），Windows 工程基准为 Vivado/Vivado HLS/SDK 2019.1、Zynq-7020、AXI DMA Simple MM2S/S2MM。项目或独立数据根须保留以下相对布局：
- `01_HLS_Accelerator/src/fir.cpp`：本项目51个固定对称系数；data_t=ap_fixed<24,4>，coeff_t=ap_fixed<24,2>。
- `03_SDK_Software/fir_test/src/fir_test_inputs.h`：SineInput/MixedInput，各1000点。
- 默认批量验收还需要 `04_Test_Evidence/output/` 五个BIN与 `dumps/` 三个dump。
- 新BIN可用 `--bin` 和 `--signal` 单独检查；必须与上述输入及系数一一匹配，不支持任意波形自动识别。

## 使用方法

在项目根执行（也可从其他目录用绝对路径调用脚本并显式传 `--project`）：

```powershell
python -B 06_Skill/scripts/verify_fir.py --project .
python -B 06_Skill/scripts/verify_fir.py --project . --bin 04_Test_Evidence/output/fir_sine_fpga_perf_1000.bin --signal sine
python -B 06_Skill/scripts/test_verify.py
```

预期批量输出：`result: PASS`，cases共5项；各1000点/4000字节，3组 `dump_equal: true`。未指定dump的项为null，不冒充已检查。进程返回0为通过，1为数值失败/输入错误，2为命令用法错误。需要保存时加 `--output <不存在的新JSON路径>`；已有文件不覆盖。

## 执行与验收

1. 核输入、系数、位宽、有限数值和模型哈希；缺失任一必需文件立即失败，不跳过缺组。
2. 强制4000字节、小端float32、1000点。按原 compare.py 的 parse_inputs/parse_coeffs/read_bin/reference_fir 计算，禁止改原脚本。
3. 每点比较，输出最大绝对误差、RMSE、>0.001点数及文件SHA-256。阈值为最大绝对误差≤3.0e-6、>0.001点数为0；有dump时必须1000字且逐字一致。
4. 批量五组全过才返回PASS。RMSE为本Skill离线量化参考新增诊断量，不替换报告/Jupyter原批次RMSE或性能数据。
5. 若失败，阅读 [DMA与格式排查](references/troubleshooting.md)。脚本不诊断唯一硬件根因，不自动改变字节序、不截断、不修复数据。

## 验证边界

验收记录见 [TEST_RESULTS.md](TEST_RESULTS.md)；原compare.py及输入来源见 [provenance.json](references/provenance.json)。该参考采用近似定点量化、float64累加、float32输出，不是位精确ap_fixed仿真。新输入限制abs(x)<4仅为保守范围，不证明任意输入或所有溢出情形正确。BIN没有字节序元信息；反字节序负例可被拒绝，但不能据此声称能可靠识别所有字节序错误。

系数或位宽变更、不同初态/样本数、工具/IP版本不匹配、旧ELF调试地址、工程依赖缺失使原验收前提失效。输入头变化须人工确认与BIN同批。HLS II、Vivado移植、SDK完整重建仍按 [复现与证据边界](references/reproduction.md) 人工执行；没有自动综合、实现、下载、测频或故障恢复功能。

## 协作来源和提炼记录

见[AI_Interaction_Log.md](AI_Interaction_Log.md)中五个案例的七项结构和真实性分级。只有离线校验是已实际运行的自动化能力；DMA/HLS核查与移植准备分别受人工操作和静态检查边界限制。逐项输入/输出、操作及证据汇总见[README](README.md)。不能把历史实现反推为AI建议，也不能把本包当作已验证的通用PYNQ技能。
