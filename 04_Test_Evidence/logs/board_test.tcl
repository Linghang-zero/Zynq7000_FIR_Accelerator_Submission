# 工作目录参数化：默认取当前目录，可用环境变量 FIR_WORK_DIR 覆盖
if {[info exists ::env(FIR_WORK_DIR)]} {
    set WORK_DIR $::env(FIR_WORK_DIR)
} else {
    set WORK_DIR [pwd]
}
connect
targets -set -filter {name =~ "ARM Cortex-A9 MPCore #0"}
puts "=== TARGET STATE ==="
puts [state]
puts "=== DOWNLOAD ELF ==="
dow $WORK_DIR/fir_test.elf
puts "=== RUN ==="
con
after 5000
puts "=== STATE AFTER 5s ==="
puts [state]
stop
after 500
puts "=== STOPPED STATE ==="
puts [state]
puts "=== READ VARIABLES ==="
puts "test_status      : [mrd 0x00112760 1]"
puts "completed_samples: [mrd 0x00112764 1]"
puts "sw_sine_cycles   : [mrd 0x001146b8 2]"
puts "sw_mixed_cycles  : [mrd 0x001146c0 2]"
puts "sw_sine_us       : [mrd 0x001146c8 2]"
puts "sw_mixed_us      : [mrd 0x001146d0 2]"
puts "sw_sine_checksum : [mrd 0x001146d8 1]"
puts "sw_mixed_checksum: [mrd 0x001146dc 1]"
puts "sw_sine_out0     : [mrd 0x001146e0 1]"
puts "sw_mixed_out0    : [mrd 0x001146e4 1]"
puts "=== DONE ==="
exit
