import pyaudio
import numpy as np
import wave
import time
import threading
import queue
import sys
import os

class AudioRecorder:
    def __init__(self, rate=16000, chunk=1024, channels=1, threshold=500, silence_limit=2.0):
        """
        初始化录音机。
        :param rate: 采样率
        :param chunk: 每次读取的帧数
        :param channels: 声道数
        :param threshold: 语音活动检测的能量阈值
        :param silence_limit: 无声持续时间（秒）后停止录音
        """
        self.rate = rate
        self.chunk = chunk
        self.channels = channels
        self.threshold = threshold
        self.silence_limit = silence_limit
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.recording = False
        self.silence_start = None
        self.output_dir = "recordings"
        os.makedirs(self.output_dir, exist_ok=True)

    def start(self):
        """开始监听并录音"""
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk,
            stream_callback=self.callback
        )
        self.stream.start_stream()
        print("开始监听... 等待语音活动。")
        try:
            while self.stream.is_active():
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.stop()

    def callback(self, in_data, frame_count, time_info, status):
        """音频流回调函数"""
        data = np.frombuffer(in_data, dtype=np.int16)
        energy = np.sqrt(np.mean(data**2))
        
        if energy > self.threshold:
            if not self.recording:
                print(f"检测到语音（能量={energy:.2f}），开始录音。")
                self.recording = True
                self.frames = []
                self.silence_start = None
            self.frames.append(in_data)
        else:
            if self.recording:
                # 无声
                if self.silence_start is None:
                    self.silence_start = time.time()
                elif time.time() - self.silence_start > self.silence_limit:
                    print(f"无声超过{self.silence_limit}秒，停止录音。")
                    self.save_recording()
                    self.recording = False
                    self.silence_start = None
                else:
                    self.frames.append(in_data)
            else:
                pass  # 持续无声
        return (in_data, pyaudio.paContinue)

    def save_recording(self):
        """保存录音到WAV文件"""
        if not self.frames:
            return
        filename = os.path.join(self.output_dir, f"recording_{int(time.time())}.wav")
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        print(f"录音已保存: {filename}")
        self.frames = []

    def stop(self):
        """停止录音并清理"""
        if self.recording:
            self.save_recording()
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.audio.terminate()
        print("录音机已停止。")

def main():
    recorder = AudioRecorder(threshold=500, silence_limit=2.0)
    try:
        recorder.start()
    except KeyboardInterrupt:
        recorder.stop()
        print("程序退出。")

if __name__ == "__main__":
    main()