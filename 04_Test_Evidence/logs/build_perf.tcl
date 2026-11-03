# 工作目录参数化：默认取当前目录，可用环境变量 FIR_WORK_DIR 覆盖
if {[info exists ::env(FIR_WORK_DIR)]} {
    set WORK_DIR $::env(FIR_WORK_DIR)
} else {
    set WORK_DIR [pwd]
}
setws $WORK_DIR/ws
importprojects $WORK_DIR/fir_test_perf_bsp
importprojects $WORK_DIR/fir_test_perf
puts "=== PROJECTS ==="
projects
puts "=== BUILD ==="
projects -build -name fir_test -type app
puts "=== BUILD DONE ==="
exit
