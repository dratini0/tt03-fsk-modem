#!/usr/bin/env python3
import math
from random import randint

from amaranth import *

from amaranth_cocotb import run, get_current_module

import cocotb
from cocotb.triggers import RisingEdge
from cocotb_test.simulator import Icarus

import numpy as np

from rx import Rx
from util import cocotb_header

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


@cocotb.test()
async def prbs9_demod(dut):
    test_data = [1] * 100 + [0, 1] * 10 + prbs9 * 2

    phase_per_sample = [f / F_S * np.pi * 2 for f in F]
    samples_per_bit = F_S / BAUD

    waveform = np.zeros(int(len(test_data) * samples_per_bit), dtype=np.int32)
    phase = 0.0
    for i in range(len(waveform)):
        waveform[i] = int(np.sin(phase) >= 0)
        phase += phase_per_sample[test_data[int(i / samples_per_bit)]]

    waveform = waveform.tolist()

    dut.in_.value = 0
    dut.frequency.value = round(F_C / F_S * 1024)
    dut.frequency_invert.value = 0

    await cocotb_header(dut)
    result = []
    result_valid = []

    for sample in waveform:
        dut.in_.value = sample
        await RisingEdge(dut.clk)
        result.append(int(dut.out))
        result_valid.append(int(dut.valid))

    valid_start = result_valid.index(1)
    assert all(result_valid[valid_start:])
    signal_start = valid_start + result[valid_start:].index(0)
    for i, bit in enumerate(test_data[100:]):
        assert result[signal_start + round((i + 0.5) * samples_per_bit)] == bit


@cocotb.test()
async def random_validity(dut):
    dut.in_.value = 0
    dut.frequency.value = round(F_C / F_S * 1024)
    dut.frequency_invert.value = 0

    await cocotb_header(dut)
    result = []
    result_valid = []
    for sample in range(1000):
        dut.in_.value = randint(0, 1)
        await RisingEdge(dut.clk)
        result.append(int(dut.out))
        result_valid.append(int(dut.valid))



def test_wave_gen():
    dut = Rx()
    run(
        dut,
        get_current_module(),
        ports=dut.get_ports(),
        simulator=Icarus,
        vcd_file=f"{get_current_module()}.vcd",
    )
