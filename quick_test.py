import sys
import time
import threading
from edge_detector import EdgeDetector

def run():
    detector = EdgeDetector()
    print("启动检测器（运行3秒）...")
    # 在一个线程中启动音频监控
    import threading
    def target():
        detector.start_audio_monitoring()
        while True:
            time.sleep(0.1)
    t = threading.Thread(target=target, daemon=True)
    t.start()
    time.sleep(3)
    detector.stop()
    print("测试完成")

if __name__ == "__main__":
    run()