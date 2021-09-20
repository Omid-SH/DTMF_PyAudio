#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 18:18:53 2021

@author: omidsh
"""

import pyaudio
import numpy as np

import scipy.io
from scipy import signal
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

# Filter Design
fs = 44100.0         # Sample rate, Hz
bands = [[670, 710], [750, 790], [830, 870], [920, 960],
         [1190, 1230], [1320, 1360], [1460, 1500], [1610, 1650]]  # Desired pass band, Hz
trans_width = 40    # Width of transition from pass band to stop band, Hz
numtaps = 400        # Size of the FIR filter.

flt = np.zeros([8, 400])

for i in range(8):
    band = bands[i][:]
    edges = [0, band[0] - trans_width, band[0], band[1],
             band[1] + trans_width, 0.5*fs]
    taps = signal.remez(numtaps, edges, [0, 1, 0], Hz=fs)
    w, h = signal.freqz(taps, [1], worN=2000)
    flt[i][:] = taps
        
    
switcher = {
        0: "1",
        1: "2",
        2: "3",
        3: "A",
        4: "4",
        5: "5",
        6: "6",
        7: "B",
        8: "7",
        9: "8",
        10: "9",
        11: "C",
        12: "*",
        13: "0",
        14: "#",
        15: "D"
    }

CHUNK = 4098
signal_flt = np.zeros([8, 2*CHUNK])

WIDTH = 2
CHANNELS = 1 # Mono Signal
RATE = 44100
# RECORD_SECONDS = 5

Data = np.zeros(2*CHUNK)
Sensitivity = 1.05

def signal_processing (x):
    Data[0:CHUNK] = Data[CHUNK:2*CHUNK]
    Data[CHUNK:2*CHUNK] = x
    

    for i in range(8):
        signal_flt[i][:] = signal.convolve(Data, flt[i][:], mode='same') / sum(flt[i][:])
    
    code = 0
    start = False

    for i in range(8):
        if (np.max(signal_flt[i][CHUNK:2*CHUNK]) > Sensitivity * np.amax(Data)):
            if(i < 4):
                code += 4*i
            else:
                code += (i-4)
            start = True
            
    if (start):
        if (code < 16 ):
            print(switcher[code])
        return signal_flt
        

    
    print('...')
    return signal_flt

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)

print("Code Is Running ... ")

try:
    while 1:
        data = stream.read(CHUNK)
        x = np.frombuffer(data, dtype=np.int16)
        signal_flt = signal_processing(x)
        

        #print(x.type())
        #out = np.ndarray.tobytes(y)
        #stream.write(out, CHUNK)
        
except KeyboardInterrupt:

    stream.stop_stream()
    stream.close()

    p.terminate()
    print("Done")

