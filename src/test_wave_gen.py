#!/usr/bin/env python3
from amaranth import *

from amaranth_cocotb import run, get_current_module

import cocotb
from cocotb.triggers import ClockCycles, RisingEdge
from cocotb_test.simulator import Icarus

import numpy as np
from numpy.fft import rfft

from util import cocotb_header
from wave_gen import WaveGen


@cocotb.test()
async def bench(dut):
    dut.frequency.value = 0
    await cocotb_header(dut)
    for frequency in [1, 2, 3] + list(range(10, 201, 10)):
        dut.frequency.value = frequency
        await ClockCycles(dut.clk, 74)
        sample = []
        for _ in range(1024):
            await RisingEdge(dut.clk)
            sample.append(int(dut.out))
        await ClockCycles(dut.clk, 101)
        fft = np.abs(rfft(sample))
        total_power = np.sum(fft[1:] * fft[1:])
        fundamental_power = fft[frequency] * fft[frequency]
        thd = np.sqrt((total_power - fundamental_power) / fundamental_power)
        assert thd < 0.2


def test_wave_gen():
    dut = WaveGen()
    run(
        dut,
        get_current_module(),
        ports=dut.get_ports(),
        simulator=Icarus,
        vcd_file=f"{get_current_module()}.vcd",
    )
