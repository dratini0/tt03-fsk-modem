#!/usr/bin/env python3
import itertools
from random import randint

from amaranth import *

from amaranth_cocotb import run, get_current_module

import cocotb
from cocotb.triggers import ClockCycles, RisingEdge, Timer
from cocotb_test.simulator import Icarus, run as cocotb_run

import numpy as np

from top import FSKModem
from util import (
    bytes_to_bitstream,
    cocotb_header,
    send_bitstream,
)

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
async def modem_mode(dut):
    test_data = [1] * 100 + [0, 1] * 10 + prbs9 * 2

    phase_per_sample = [f / F_S * np.pi * 2 for f in F]
    samples_per_bit = F_S / BAUD

    waveform_rx = np.zeros(int(len(test_data) * samples_per_bit), dtype=np.int32)
    waveform_tx = np.zeros(int(len(test_data) * samples_per_bit), dtype=np.int32)
    phase = 0.0
    for i in range(len(waveform_rx)):
        waveform_rx[i] = int(np.sin(phase) >= 0)
        phase += phase_per_sample[test_data[int(i / samples_per_bit)]]
        waveform_tx[i] = test_data[int(i / samples_per_bit)]

    waveform_rx = waveform_rx.tolist()
    waveform_tx = waveform_tx.tolist()

    dut.cs_n.value = 1
    dut.sck.value = 0
    dut.mosi.value = 0
    dut.data_in.value = 1
    dut.samples_in.value = 0

    await cocotb_header(dut)

    f_c = round(F_C / F_S * 1024)
    f_0 = round(F[0] / F_S * 1024)
    f_1 = round(F[1] / F_S * 1024)
    program = [
        0x00 | (f_0 & 0x0F),
        0x10 | ((f_0 >> 4) & 0x0F),
        0x20 | (f_1 & 0x0F),
        0x30 | ((f_1 >> 4) & 0x0F),
        0x61,
        0x70 | (f_c & 0x0F),
        0x80 | ((f_c >> 4) & 0x0F),
        0x92,
    ]

    await send_bitstream(dut, bytes_to_bitstream(program))

    for sample_rx, sample_tx in zip(waveform_rx, waveform_tx):
        dut.samples_in.value = sample_rx
        dut.data_in.value = sample_tx
        await RisingEdge(dut.clk)


@cocotb.test()
async def dtmf_mode(dut):
    F_R = [697, 770, 852, 941]
    F_C = [1209, 1336, 1477, 1633]

    dut.cs_n.value = 1
    dut.sck.value = 0
    dut.mosi.value = 0
    dut.data_in.value = 1
    dut.samples_in.value = 0

    await cocotb_header(dut)

    # mute
    await send_bitstream(dut, bytes_to_bitstream([0x60]))

    await Timer(50, "ms")

    for f_row in F_R:
        for f_col in F_C:
            f_row_reg = round(f_row / F_S * 1024)
            f_col_reg = round(f_col / F_S * 1024)
            program = [
                0x20 | (f_row_reg & 0x0F),
                0x30 | ((f_row_reg >> 4) & 0x0F),
                0x40 | (f_col_reg & 0x0F),
                0x50 | ((f_col_reg >> 4) & 0x0F),
                0x62,
            ]
            await send_bitstream(dut, bytes_to_bitstream(program))
            await Timer(100, "ms")
            await send_bitstream(dut, bytes_to_bitstream([0x60]))
            await Timer(50, "ms")


def test_fsk_modem():
    top = FSKModem()
    run(
        top,
        get_current_module(),
        ports=top.get_ports(),
        simulator=Icarus,
        vcd_file="test_fsk_modem.vcd",
    )
