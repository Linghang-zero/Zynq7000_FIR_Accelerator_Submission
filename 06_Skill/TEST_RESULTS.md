# Skill实际测试结果

日期：2026-11-04。运行环境：Windows，Python 3.12.14，标准库；未运行Vivado/HLS/SDK或板卡实验。

## 已执行命令

从项目根运行：

```powershell
python -B 06_Skill/scripts/verify_fir.py --project .
python -B 06_Skill/scripts/test_verify.py
```

批量验收返回0、PASS；回归共8项全部通过。原compare.py未修改，副本SHA-256与原文件一致；其函数及main入口在测试中以显式输入路径运行。verify_fir.py是正式CLI，compare.py副本作为参考库使用，不单独按其原默认路径运行。

|文件|点数/字节|最大绝对误差|RMSE（本次量化参考）|dump|结果|
|---|---|---|---|---|---|
|fir_sine_fpga_1000.bin|1000/4000|2.194195986e-06|1.317685639e-06|一致|PASS|
|fir_mixed_fpga_1000.bin|1000/4000|2.980232239e-06|1.701938833e-06|一致|PASS|
|fir_sine_fpga_perf_1000.bin|1000/4000|2.194195986e-06|1.317685639e-06|未指定，不作断言|PASS|
|fir_mixed_fpga_perf_1000.bin|1000/4000|2.980232239e-06|1.701938833e-06|一致|PASS|
|fir_impulse_fpga_1000.bin|1000/4000|2.384185791e-07|3.455013453e-08|未指定，不作断言|PASS|

五组>0.001点数均为0。正弦与混频两版BIN分别字节相同，因此不是4次独立数值实验；本次是对归档5个文件的重新离线验收。冲激的本次误差参考为量化Golden，不替换原冲激日志的浮点系数比较结果。RMSE不是新增板测性能数据，不写回metrics.csv。

## 回归测试覆盖

1. 真实5组BIN及3个dump全量验收。
2. CLI成功返回码、JSON输出和拒绝覆盖已有输出。
3. 系数/数据位宽变化拒绝。
4. 输入999点及超出保守幅度范围拒绝。
5. 缺文件拒绝。
6. 原参考程序函数和main入口实际运行。
7. 空BIN、截短、增长、NaN拒绝。
8. 临时反字节序、错信号、错误dump拒绝。

负例只在临时目录生成，明确为人为破坏副本；不是历史故障或板级注入实验。原始数据未改变。

原始回归输出见[regression_log.txt](references/regression_log.txt)，逐组结构化结果见[verification_results.json](references/verification_results.json)。

## 格式与复用边界

SKILL.md前置字段、命名、内部链接完成轻量静态检查。官方quick_validate.py因本机运行时缺PyYAML未成功运行，未伪称其通过；离线验证脚本不依赖PyYAML。未安装全局Skill，未通过另一智能体或另一工程的行为验证。

已验证：本归档数据和列出的离线拒绝路径。仅静态核对：DMA顺序、TLAST、缓存、HLS II证据、工程依赖。未验证：新综合、完整重建、新上板、故障注入/恢复及跨工程迁移。

## 脚本SHA-256

- `compare.py`：`D7201B12067135A0FA1AB86B69218CA05E1604ECD960F903F6062727764EFC31`
- `test_verify.py`：`AC9638A004F49F0F86E0C79C5C54079CD0F08D6F040E07ED92187A91DFE1B950`
- `verify_fir.py`：`8B589C45BB8F73E3EE63221724E39B9A4707EA9DD4DEAE7DA46752B8CE77E196`
