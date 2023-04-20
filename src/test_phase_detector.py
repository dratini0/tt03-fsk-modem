#!/usr/bin/env python3
import math
from random import randint

from amaranth import *

from amaranth_cocotb import run, get_current_module

import cocotb
from cocotb.triggers import Timer
from cocotb_test.simulator import Icarus

from rx import PhaseDetector


@cocotb.test()
async def bench(dut):
    cases = {
        (1, 0): 0,
        (0, 1): 1,
        (-1, 1): 2,
        (-2, 0): 3,
        (-2, -1): 4,
        (-1, -2): 5,
        (0, -2): 6,
        (1, -1): 7,
    }

    for (i, q), phase in cases.items():
        dut.i.value = i
        dut.q.value = q
        await Timer(1, "ms")
        assert dut.phase == phase


def test_wave_gen():
    dut = PhaseDetector(11)
    run(
        dut,
        get_current_module(),
        ports=dut.get_ports(),
        simulator=Icarus,
        vcd_file=f"{get_current_module()}.vcd",
    )
