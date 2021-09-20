#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 18:12:04 2021

@author: omidsh
"""
# Using https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.remez.html

import scipy.io
from scipy import signal
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

def plot_response(fs, w, h, title):
    "Utility function to plot response functions"
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(0.5*fs*w/np.pi, 20*np.log10(np.abs(h)))
    ax.set_ylim(-40, 5)
    ax.set_xlim(0, 0.5*fs)
    ax.grid(True)
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Gain (dB)')
    ax.set_title(title)
    
flt = np.zeros([8, 400])

Sensitivity = 40
"""
mat1 = scipy.io.loadmat('filter1.mat')
flt[0][:] = mat1['filter1'];

mat2 = scipy.io.loadmat('filter2.mat')
flt[1][:] = mat2['filter2'];

mat3 = scipy.io.loadmat('filter3.mat')
flt[2][:] = mat3['filter3'];

mat4 = scipy.io.loadmat('filter4.mat')
flt[3][:] = mat4['filter4'];

mat5 = scipy.io.loadmat('filter5.mat')
flt[4][:] = mat5['filter5'];

mat6 = scipy.io.loadmat('filter6.mat')
flt[5][:] = mat6['filter6'];

mat7 = scipy.io.loadmat('filter7.mat')
flt[6][:] = mat7['filter7'];

mat8 = scipy.io.loadmat('filter8.mat')
flt[7][:] = mat8['filter8'];

"""

fs = 8192.0         # Sample rate, Hz
bands = [[670, 710], [750, 790], [830, 870], [920, 960],
         [1190, 1230], [1320, 1360], [1460, 1500], [1610, 1650]]  # Desired pass band, Hz
trans_width = 40    # Width of transition from pass band to stop band, Hz
numtaps = 400        # Size of the FIR filter.

for i in range(8):
    band = bands[i][:]
    edges = [0, band[0] - trans_width, band[0], band[1],
             band[1] + trans_width, 0.5*fs]
    taps = signal.remez(numtaps, edges, [0, 1, 0], Hz=fs)
    w, h = signal.freqz(taps, [1], worN=2000)
    flt[i][:] = taps
    
    # plot_response(fs, w, h, "Band-pass Filter")


fs, sgl = wavfile.read('./Wav_Files/DialedSequence_SNR30dB.wav')


signal_flt = np.zeros([8, len(sgl)])

for i in range(8):
    signal_flt[i][:] = signal.convolve(sgl, flt[i][:], mode='same') / sum(flt[i][:])
 
out = ""
cnt_z = 0
start = False
code = 0
cnt_s = 0
code_l = 0
code_r = 0
maxl = 0
maxr = 0
energy = np.zeros(8)

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

MAXX = np.amax(sgl)

for t in range(len(sgl)) :
           
    if (start):
        if(cnt_s > 1800):
            for i in range(8):
                if (i<4 and energy[i] > maxl): 
                    maxl = energy[i]
                    code_l = i
                elif (i>=4 and energy[i] > maxr): 
                    maxr = energy[i]
                    code_r = i
                energy[i] = 0
            
            code = code_l*4 + (code_r-4)
            print(code)
            out += switcher[code]
            cnt_s = 0
            code_l = 0
            code_r = 0
            maxl = 0
            maxr = 0
            start = False
        else:
            for i in range(8):
                energy[i] += signal_flt[i][t] ** 2
            cnt_s += 1
    else:
        for i in range(8):
            if (signal_flt[i][t] > 5*10**5):#Sensitivity * MAXX):              
                if (cnt_z > 800):
                    start = True
                    cnt_z = 0
                else:
                    cnt_z = 0
            else :
                cnt_z += 1
    
print(out) 
   

plt.figure()
plt.title("DialedSequence_SNR00dB")
plt.plot(signal_flt[0][:])
plt.plot(signal_flt[1][:])
plt.plot(signal_flt[2][:])
plt.plot(signal_flt[3][:])

plt.legend(['697 Hz', '770 Hz', '852 Hz', '941 Hz'])
plt.show()  


plt.figure()
plt.title("DialedSequence_SNR00dB")
plt.plot(signal_flt[4][:])
plt.plot(signal_flt[5][:])
plt.plot(signal_flt[6][:])
plt.plot(signal_flt[7][:])

plt.legend(['1209 Hz', '1336 Hz', '1477 Hz', '1633 Hz'])
plt.show()  