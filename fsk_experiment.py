#!/usr/bin/env python3

from math import floor
import wave

import numpy as np
from numpy.fft import rfft
import matplotlib.pyplot as plt
from scipy.signal import lfilter, butter

prbs9 = list(
    map(
        int,
        (
            "00010001100001001110010101011000011011110100110111"
            "00100010100001010110100111111011001001001011011111"
            "10010011010100110011000000011000110010100011010010"
            "11111110100010110001110101100101100111100011111011"
            "10100000110101101101110110000010110101111101010101"
            "00000010100101011110010111011100000011100111010010"
            "01111010111010100010010000110011100001011110110110"
            "01101000011101111000011111111100000111101111100010"
            "11100110010000010010100111011010001111001111100110"
            "11000101010010001110001101101010111000100110001000"
            "10000000010"
        ),
    )
)

F_S = 12500.0

# Ch 2 of ITU V.21
F = [1850.0, 1650.0]

BAUD = 300.0

phase_per_sample = [f / F_S * np.pi * 2 for f in F]
samples_per_bit = F_S / BAUD

waveform = np.zeros(floor(10 * F_S))

phase = 0.0
for i in range(len(waveform)):
    waveform[i] = np.sin(phase)
    phase += phase_per_sample[prbs9[floor(i / samples_per_bit) % len(prbs9)]]

quantized = np.round(waveform * 7) / 7  # 4 bits

F_C = 1750.0
i_square = np.float64((np.arange(len(waveform)) * (F_C / F_S)) % 1 >= 0.5) * 2 - 1
q_square = (
    np.float64((np.arange(len(waveform)) * (F_C / F_S) + 0.25) % 1 >= 0.5) * 2 - 1
)

# filter_ba = butter(2, BAUD, fs=F_S)
#filter_ba = [[0.5, 1, 0.5], [ 1.        , round(-1.78743252 * 32) / 32,  round(0.80794959 * 32) / 32]]
filter_ba = [[1/16, 1/16], [1.0, -15/16]]
i = lfilter(*filter_ba, i_square * quantized)
q = lfilter(*filter_ba, q_square * quantized)
i = lfilter(*filter_ba, i)
q = lfilter(*filter_ba, q)
i_ = i[2:] - i[:-2]
q_ = q[2:] - q[:-2]
i, q = i[2:], q[2:]
cross = i * q_ - q * i_

plt.plot(i[1000:4000], q[1000:4000])
plt.show()
plt.plot(i[1000:4000])
plt.plot(q[1000:4000])
plt.show()
plt.plot(cross[1000:4000])
plt.show()
