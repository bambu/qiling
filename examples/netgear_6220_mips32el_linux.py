#!/usr/bin/env python3
# 
# Cross Platform and Multi Architecture Advanced Binary Emulation Framework
# Built on top of Unicorn emulator (www.unicorn-engine.org) 

# After mapping /proc there will be a /dev/mtdblock11 missing and crash
# To fix this,
#   - cd $yourfirmware_rootfs/dev
#   - dd if=/dev/zero of=mtdblock11 bs=1 size=12345
#   - mkfs.ext4 mtdblock11
# 
# This firmware will more or less alive now.


import sys
sys.path.append("..")
from qiling import *

# due to mtdblock11 causing llseek to crash. we implement our own llseek
def my_syscall__llseek(ql, fd, offset_high, offset_low, result, whence, null0):
    regreturn = 0 
    ql.nprint("_llseek(%d, 0x%x, 0x%x, 0x%x = %d)" % (fd, offset_high, offset_low, result, regreturn))
    ql_definesyscall_return(ql, regreturn)

def my_netgear(path, rootfs):
    ql = Qiling(
                path, 
                rootfs, 
                output      = "debug", 
                log_file    = 'logfile', 
                log_split   = True, 
                log_console = True, 
                mmap_start  = 0x7ffef000 - 0x800000
                )
    ql.root = False
    ql.add_fs_mapper('/proc', '/proc')
    ql.set_syscall(4140, my_syscall__llseek)
    ql.run()


if __name__ == "__main__":
    my_netgear(["rootfs/netgear_r6220/bin/mini_httpd",
                "-d","/www",
                "-r","NETGEAR R6220",
                "-c","**.cgi",
                "-t","300"], 
                "rootfs/netgear_r6220")
