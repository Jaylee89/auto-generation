import sys
import time
import numpy as np
import pyaudio

CHUNK = 1024
RATE = 16000
THRESHOLD = 500

audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

print("Recording audio for 5 seconds...")
start = time.time()
while time.time() - start < 5:
    data = stream.read(CHUNK)
    arr = np.frombuffer(data, dtype=np.int16)
    energy = np.sqrt(np.mean(arr**2))
    print(f"Energy: {energy:.2f}, threshold: {THRESHOLD}, above? {energy > THRESHOLD}")

stream.stop_stream()
stream.close()
audio.terminate()