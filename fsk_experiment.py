#!/usr/bin/env python3

from math import floor
import wave

import numpy as np
from numpy.fft import rfft
import matplotlib.pyplot as plt
from scipy.signal import lfilter, firwin

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
F_C = 1750.0
# Ch 1 of ITU V.21
# F_C = 1080.0

F = [F_C + 100.0, F_C - 100.0]

BAUD = 300.0

phase_per_sample = [f / F_S * np.pi * 2 for f in F]
samples_per_bit = F_S / BAUD

waveform = np.zeros(floor(10 * F_S))
ref_waveform = np.zeros(floor(10 * F_S))

phase = 0.0
for i in range(len(waveform)):
    waveform[i] = np.sin(phase)
    phase += phase_per_sample[prbs9[floor(i / samples_per_bit) % len(prbs9)]]
    ref_waveform[i] = prbs9[floor(i / samples_per_bit) % len(prbs9)]

quantized = np.round(waveform * 1) / 1  # 4 bits

i_square = np.float64((np.arange(len(waveform)) * (F_C / F_S)) % 1 >= 0.5) * 2 - 1
q_square = (
    np.float64((np.arange(len(waveform)) * (F_C / F_S) + 0.25) % 1 >= 0.5) * 2 - 1
)

# filter_ba = butter(2, BAUD, fs=F_S)
filter_ = firwin(15, 100, fs=12500)
filter_approximate = np.exp2(np.round(np.log2(filter_/filter_[0])))
print(f"Gain: {sum(filter_approximate)}")
filter_ba = [filter_approximate, [1] + [0] * 14]
# filter_ba = [[1/16, 0], [1.0, -15/16]]
i = lfilter(*filter_ba, i_square * quantized)
q = lfilter(*filter_ba, q_square * quantized)
# i = lfilter(*filter_ba, i)
# q = lfilter(*filter_ba, q)
angle = np.unwrap(np.arctan2(q, i))
angle_rounded =  np.round(angle / (2 * np.pi) * 8)

_, ((constellation_plot, iq_plot, _), (angle_plot, angle_rounded_plot, ref_waveform_plot)) = plt.subplots(2, 3)
constellation_plot.plot(i[1000:4000], q[1000:4000])
iq_plot.plot(i[1000:4000])
iq_plot.plot(q[1000:4000])
angle_plot.plot(angle[1000:4000])
angle_rounded_plot.plot(angle_rounded[1000:4000])
ref_waveform_plot.plot(ref_waveform[1000:4000])
plt.show()
