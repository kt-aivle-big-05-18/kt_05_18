import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import time
import winsound

fs = 44100  # Sample rate
seconds = 6  # 녹음 시간
n = 10 # 녹음 진행할 순서

def play_beep():
    duration = 700  # 삐 소리의 지속 시간(ms)
    frequency = 500  # 삐 소리의 주파수(Hz)
    winsound.Beep(frequency, duration)

for i in range(n): 
    print(f"Recording {i+553}...")

    # 삐 소리 재생
    play_beep()

    # 녹음 시작
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished

    # 녹음된 데이터를 int16 형태로 변환
    myrecording_int = np.int16(myrecording * 32767)

    # 변환된 데이터를 WAV 파일로 저장
    filename = f"test_{i+553}.wav" # 저장되는 경로 및 이름
    write(filename, fs, myrecording_int) 

    print(f"Recording {i+553} saved as {filename}\n")
    time.sleep(1)  # 1초 딜레이
