import cv2 as cv
import numpy as np
from math import ceil

def draw_mod(frame, signal, width, height):
    width_scaled_signal = np.array_split(signal, width)
    width_scaled_signal = np.array([ np.mean(interval) for interval in width_scaled_signal ])

    #frame = cv.line(frame, (0, height), (0, height), (102, 0, 255), 1)

    for idx, sample in enumerate(width_scaled_signal[1:]):
        frame = cv.line(frame, (idx, height), (idx, height - ceil(sample)), (0, 255, 0), 1)
    return frame

def min_max_scaler(signal, max_val):
    return max_val*((signal - np.min(signal)) / (np.max(signal) - np.min(signal)))
