#!/usr/bin/env python3
import time
import subprocess
import sys

print("等待服务器启动...")
time.sleep(5)

print("开始运行测试...")
result = subprocess.run([sys.executable, "simple_docs_test.py"], 
                       capture_output=False, text=True)
sys.exit(result.returncode)
