#!/usr/bin/env python3

import matplotlib.pyplot as plt

import numpy as np
from numpy.fft import rfft

wave_orig = np.abs(np.linspace(0, 4, 1025)[:1024] - 2) - 1

clamp_level = np.linspace(0, 1, 257)[1:]
thd = np.zeros_like(clamp_level)

for i, i_clamp_level in enumerate(clamp_level):
    wave_clamped = wave_orig.copy()
    wave_clamped[wave_clamped > i_clamp_level] = i_clamp_level
    wave_clamped[wave_clamped < -i_clamp_level] = -i_clamp_level
    fft = np.abs(rfft(wave_clamped))
    total_power = np.sum(fft * fft)
    fundamental_power = fft[1] * fft[1]
    thd[i] = np.log10((total_power - fundamental_power) / (fundamental_power)) * 10

print(thd)
plt.plot(clamp_level, thd)
plt.show()
