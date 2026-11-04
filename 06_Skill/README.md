# Zynq-7000 FIR 验证与复现 Skill

入口：[SKILL.md](SKILL.md)。这是本地可交付技能包，未安装到全局技能目录；可整体复制，但须同时提供SKILL.md所列项目输入布局。

- [verify_fir.py](scripts/verify_fir.py)：严格离线验收入口。
- [compare.py](scripts/compare.py)：由原 `05_Docs/compare.py` 原样复制的参考实现；哈希见 [provenance.json](references/provenance.json)。
- [test_verify.py](scripts/test_verify.py)：真实归档数据回归及明确标记的临时破坏性负例（仅临时副本）。
- [TEST_RESULTS.md](TEST_RESULTS.md)：本次实际测试结果。
- [AI交互记录：五个案例、七项结构](AI_Interaction_Log.md)：区分原话选段、事后摘要和缺失历史。
- [AI协作证据索引](references/ai_evidence.md)：真实案例与缺口。
- [DMA/格式排查](references/troubleshooting.md)、[人工复现边界](references/reproduction.md)。

从项目根运行 `python -B 06_Skill/scripts/verify_fir.py --project .`。不依赖numpy，不写入现有数据；默认只输出到终端。工程、BIN、性能数据与原脚本不修改。

## 每项能力的适用范围与验证证据

|能力/输入|使用与输出|已验证效果及证据|失效条件/边界|
|---|---|---|---|
|BIN校验：固定51系数、输入头、5BIN/3dump|按SKILL.md运行verify_fir.py，输出JSON/返回码|5文件与3dump、8测试；见TEST_RESULTS及其原始日志|1000点/4000字节；系数/位宽/初态变化须重验；非位精确参考|
|DMA人工排查：匹配硬件产物、N、缓存及寄存器|按references/troubleshooting.md逐项核查，输出问题位置/停止条件|main.c及fir.cpp支持顺序和错误码；既有正常输出|未验证故障注入/自动恢复；旧ELF地址不得照用|
|HLS证据核查：源码和csim/csynth报告|人工比对pragma、achieved II和csim判据，输出证据位置|既有II=1、Failed checks=0；见AI_Interaction_Log案例一|未自动优化或新综合，无同条件优化前基线；II不代表端到端吞吐|
|工程复现准备：IP/BD/SDK与2019.1环境|按references/reproduction.md人工操作并保存新日志|仅完成静态准备，不是已验证自动化能力|路径、工具/IP、供电、依赖缺失时停止；完整重建待验|

经验提炼的失败/观察来源见[交互记录](AI_Interaction_Log.md)及[排查清单](references/troubleshooting.md)。技术实现证据与AI历史证据分开，不以结果反推模型对话。规范skill/目录入口见[skill/README.md](../skill/README.md)；是否接受索引布局待赛事确认。
