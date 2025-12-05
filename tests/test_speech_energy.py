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

print("Please speak for 3 seconds...")
start = time.time()
max_energy = 0
while time.time() - start < 3:
    data = stream.read(CHUNK)
    arr = np.frombuffer(data, dtype=np.int16)
    energy = np.sqrt(np.mean(arr**2))
    if energy > max_energy:
        max_energy = energy
    print(f"Energy: {energy:.2f}")

stream.stop_stream()
stream.close()
audio.terminate()
print(f"Max energy observed: {max_energy:.2f}")
print(f"Threshold: {THRESHOLD}")