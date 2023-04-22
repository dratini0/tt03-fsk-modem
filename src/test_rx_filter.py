#!/usr/bin/env python3
import math
from random import randint

from amaranth import *

from amaranth_cocotb import run, get_current_module

import cocotb
from cocotb.triggers import ClockCycles, RisingEdge
from cocotb_test.simulator import Icarus

import numpy as np
from scipy.signal import lfilter

from rx import RxFilter
from util import cocotb_header


def wrap_int(val):
    val = int(val)
    return val - 64 if val > 32 else val


@cocotb.test()
async def impulse_response(dut):
    dut.in_.value = 0
    await cocotb_header(dut)
    result = []
    dut.in_.value = 1
    await RisingEdge(dut.clk)
    result.append(wrap_int(dut.out.value))
    dut.in_.value = 0
    for i in range(127):
        await RisingEdge(dut.clk)
        result.append(wrap_int(dut.out.value))


@cocotb.test()
async def step_response(dut):
    dut.in_.value = 0
    await cocotb_header(dut)
    result = []
    dut.in_.value = 1
    await RisingEdge(dut.clk)
    result.append(wrap_int(dut.out.value))
    for i in range(127):
        await RisingEdge(dut.clk)
        result.append(wrap_int(dut.out.value))

    assert all(i >= 0 for i in result)  # Check for no overflow


@cocotb.test()
async def frequency_response(dut):
    dut.in_.value = 0
    await cocotb_header(dut)
    phase = 0
    test_signal = []
    for frequency in range(100, 1001, 100):
        omega = frequency / 12500 * 2 * math.pi
        for i in range(1024):
            test_signal.append(int(math.sin(phase) >= 0))
            phase += omega

    result = []
    for sample in test_signal:
        dut.in_.value = sample
        await RisingEdge(dut.clk)
        result.append(wrap_int(dut.out.value))
    test_signal = np.array(test_signal)
    result = np.array(result)

    reference = lfilter(*RxFilter.get_iir(), test_signal)

    for i in range(0, 10 * 1024, 1024):
        print(i / 1024)
        result_power = np.sqrt(np.sum(result[i : i + 1024] * result[i : i + 1024]))
        reference_power = np.sqrt(
            np.sum(reference[i : i + 1024] * reference[i : i + 1024])
        )
        assert 0.9 < result_power / reference_power < 1.1


def test_wave_gen():
    dut = RxFilter()
    run(
        dut,
        get_current_module(),
        ports=dut.get_ports(),
        simulator=Icarus,
        vcd_file=f"{get_current_module()}.vcd",
    )
