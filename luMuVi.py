import pyaudio
import wave
import scipy
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

from sklearn.preprocessing import MinMaxScaler
from math import ceil
from time import sleep
from draw_mod import draw_mod, min_max_scaler


CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
WAVE_OUTPUT_FILENAME = "output.wav"

WIDTH = 1600 // 2
HEIGHT = 900

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("start!")

while(1):
    stream.start_stream()
    data = np.fromstring(stream.read(CHUNK), dtype=np.uint16)
    stream.stop_stream()
    if np.max(data) == 0:
        continue
    else:
        fft = np.abs(scipy.fft.fft(data))
    """
    vamos pegar o maximo valor, pra setar a altura da figura
    na vdd vamos ter q normalizar pra uma certa altura

    primeiro vamos fazer o frame de [0, RATE] e dps espelhamos ele
    acho q assim diminui a complexidade
    """

    height_scaled_fft = np.floor(min_max_scaler(fft[0: CHUNK//2], 1.6*HEIGHT))

    frame = np.zeros((HEIGHT, WIDTH, 3))
    
    frame = draw_mod(frame, height_scaled_fft, WIDTH, HEIGHT)

    mirrored_frame = np.concatenate((np.flip(frame, axis=1), frame), axis=1)
    cv.imshow("luMuVi", mirrored_frame)
    c = cv.waitKey(1)
    if c == 27:
        break

stream.stop_stream()
stream.close()
p.terminate()

wf.close()
