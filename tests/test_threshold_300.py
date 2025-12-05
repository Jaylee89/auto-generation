import sys
import time
import threading
from unittest.mock import patch
from edge_detector import EdgeDetector

def test_threshold():
    with patch.object(EdgeDetector, 'is_edge_foreground', return_value=True):
        detector = EdgeDetector(audio_threshold=300)
        print(f"Testing with threshold={detector.audio_threshold}")
        def monitor():
            detector.start_audio_monitoring()
            time.sleep(5)
            detector.stop()
        t = threading.Thread(target=monitor, daemon=True)
        t.start()
        t.join()
        print("Test completed.")

if __name__ == "__main__":
    test_threshold()