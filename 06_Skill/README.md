# Zynq-7000 FIR 验证与复现 Skill

入口：[SKILL.md](SKILL.md)。这是本地可交付技能包，未安装到全局技能目录；可整体复制，但须同时提供SKILL.md所列项目输入布局。

- [verify_fir.py](scripts/verify_fir.py)：严格离线验收入口。
- [compare.py](scripts/compare.py)：由原 `05_Docs/compare.py` 原样复制的参考实现；哈希见 [provenance.json](references/provenance.json)。
- [test_verify.py](scripts/test_verify.py)：真实归档数据回归及明确标记的临时破坏性负例（仅临时副本）。
- [TEST_RESULTS.md](TEST_RESULTS.md)：本次实际测试结果。
- [AI协作证据索引](references/ai_evidence.md)：真实案例与缺口。
- [DMA/格式排查](references/troubleshooting.md)、[人工复现边界](references/reproduction.md)。

从项目根运行 `python -B 06_Skill/scripts/verify_fir.py --project .`。不依赖numpy，不写入现有数据；默认只输出到终端。工程、BIN、性能数据与原脚本不修改。
