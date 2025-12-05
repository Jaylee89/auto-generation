import subprocess
import time
import sys
import os

# 在后台启动检测器
proc = subprocess.Popen([sys.executable, 'edge_detector.py'], 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.STDOUT,
                        text=True)

# 等待5秒
time.sleep(5)

# 终止进程
proc.terminate()
try:
    outs, errs = proc.communicate(timeout=2)
    print("输出:")
    print(outs)
except subprocess.TimeoutExpired:
    proc.kill()
    outs, errs = proc.communicate()
    print("进程被终止")