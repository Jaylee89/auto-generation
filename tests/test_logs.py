import sys
import time
import threading
from edge_detector import EdgeDetector

def run_test():
    detector = EdgeDetector()
    print("启动检测器（2秒）...")
    # 在后台线程中运行detector.run
    t = threading.Thread(target=detector.run)
    t.daemon = True
    t.start()
    time.sleep(2)
    print("正在停止检测器...")
    detector.stop()
    print("测试完成。")

if __name__ == "__main__":
    run_test()