# PS端与Python验证入口

本目录仅索引，不重复复制代码，不包含AI PC模型推理。

- [SDK应用](../03_SDK_Software/fir_test/)：src/main.c性能版；main_v1.0.c历史功能版，二者不能同时加入一个应用编译。
- [BSP配置](../03_SDK_Software/fir_test_bsp/system.mss)：由SDK 2019.1重新生成对应库。
- [硬件平台及xfir驱动](../03_SDK_Software/fir_system_wrapper_hw_platform_0/)：system.hdf、ps7_init与drivers/fir_v1_0。
- [标准库独立复算](../05_Docs/compare.py)：只读输入头、系数和现有BIN/dump，推荐首先运行。
- [队友Python验证](../04_Test_Evidence/python_verify/)：fir_hw_verify.py（Jupyter导出）、signal_generate.py（早期设计激励）及详细README。numpy/scipy/matplotlib版本未锁定。

fir_hw_verify.py全量执行依赖signal.npy/t.npy/clean.npy，并存在ref_sine.csv未自动生成的问题；部分计时常数来自历史批次，不应覆盖最终metrics。优先使用compare.py验证已有板测BIN。该脚本不计算RMSE或耗时比，且其quantize采用最近舍入近似，不能宣称位精确模拟所有ap_fixed/AP_TRN行为。两套Golden参考模型需分开解读。
