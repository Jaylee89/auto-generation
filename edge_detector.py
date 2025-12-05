import subprocess
import time
import psutil
import numpy as np
import pyaudio
import wave
import os
import threading
from queue import Queue

class EdgeDetector:
    def __init__(self, audio_threshold=500, silence_limit=2.0, rate=16000, chunk=1024):
        self.audio_threshold = audio_threshold
        self.silence_limit = silence_limit
        self.rate = rate
        self.chunk = chunk
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.recording = False
        self.frames = []
        self.silence_start = None
        self.output_dir = "edge_recordings"
        os.makedirs(self.output_dir, exist_ok=True)
        self.edge_pid = None
        self.callback_count = 0
        self.update_edge_pid()
        print(f"EdgeDetector初始化完成: threshold={self.audio_threshold}, silence_limit={self.silence_limit}, rate={self.rate}, chunk={self.chunk}")
        print(f"输出目录: {self.output_dir}, Edge PID: {self.edge_pid}")

    def update_edge_pid(self):
        """获取Microsoft Edge的进程ID"""
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] and 'Microsoft Edge' in proc.info['name']:
                self.edge_pid = proc.info['pid']
                print(f"找到Edge进程 PID: {self.edge_pid}")
                return
        self.edge_pid = None
        print("未找到Edge进程")

    def is_edge_foreground(self):
        """使用AppleScript检查Edge是否为前台应用程序"""
        script = '''
        tell application "System Events"
            set frontApp to name of first application process whose frontmost is true
        end tell
        return frontApp
        '''
        try:
            result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, timeout=2)
            app_name = result.stdout.strip()
            is_edge = 'Microsoft Edge' in app_name
            print(f"前台应用检测: '{app_name}', Edge在前台: {is_edge}")
            return is_edge
        except Exception as e:
            print(f"前台应用检测失败: {e}")
            return False

    def start_audio_monitoring(self):
        """开始音频监控"""
        print(f"启动音频监控: rate={self.rate}, chunk={self.chunk}, threshold={self.audio_threshold}")
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk,
            stream_callback=self.audio_callback
        )
        self.stream.start_stream()
        print("音频流已启动")

    def audio_callback(self, in_data, frame_count, time_info, status):
        """音频流回调"""
        data = np.frombuffer(in_data, dtype=np.int16)
        energy = np.sqrt(np.mean(data**2))

        # 每50个chunk打印一次能量（调试用）
        self.callback_count += 1
        if self.callback_count % 50 == 0:
            print(f"音频能量 (chunk {self.callback_count}): {energy:.2f}")

        # print(f"energy is {energy}")
        # print(f"audio_threshold is {self.audio_threshold}")
        if True or energy > self.audio_threshold:
            if not self.recording and self.is_edge_foreground():
                print(f"检测到语音且Edge在前台，开始录音（能量={energy:.2f}）")
                self.recording = True
                self.frames = []
                self.silence_start = None
            elif not self.recording:
                # 能量超过阈值但Edge不在前台
                print(f"检测到语音但Edge不在前台，跳过录音（能量={energy:.2f}）")
            if self.recording:
                self.frames.append(in_data)
        else:
            if self.recording:
                if self.silence_start is None:
                    self.silence_start = time.time()
                elif time.time() - self.silence_start > self.silence_limit:
                    print(f"无声超过{self.silence_limit}秒，停止录音。")
                    self.save_recording()
                    self.recording = False
                    self.silence_start = None
                else:
                    self.frames.append(in_data)
        return (in_data, pyaudio.paContinue)

    def save_recording(self):
        """保存录音"""
        if not self.frames:
            return
        filename = os.path.join(self.output_dir, f"edge_recording_{int(time.time())}.wav")
        wf = wave.open(filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        print(f"录音已保存: {filename}")
        self.frames = []

    def run(self):
        """主循环"""
        print("启动Edge朗读检测器...")
        self.start_audio_monitoring()
        last_status_time = time.time()
        status_interval = 10.0  # 秒
        try:
            while True:
                time.sleep(0.5)
                # 定期更新Edge PID
                self.update_edge_pid()
                # 定期打印状态
                current_time = time.time()
                if current_time - last_status_time >= status_interval:
                    print(f"状态更新: recording={self.recording}, edge_pid={self.edge_pid}, callback_count={self.callback_count}")
                    last_status_time = current_time
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """停止"""
        print("正在停止检测器...")
        if self.recording:
            print("正在保存最终录音...")
            self.save_recording()
        if self.stream:
            print("正在停止音频流...")
            self.stream.stop_stream()
            self.stream.close()
        self.audio.terminate()
        print("检测器已停止。")

if __name__ == "__main__":
    detector = EdgeDetector()
    detector.run()