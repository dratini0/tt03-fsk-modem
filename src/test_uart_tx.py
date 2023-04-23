#!/usr/bin/env python3
from __future__ import annotations

from amaranth import *

from amaranth_cocotb import run, get_current_module

import cocotb
from cocotb.triggers import ClockCycles, RisingEdge
from cocotb_test.simulator import Icarus

from uart import UARTTx
from util import cocotb_header


@cocotb.test()
async def bench(dut):
    dut.data.value = 0
    dut.we.value = 0
    dut.frequency.value = round(1200 / 12500 * 1024)

    await cocotb_header(dut)

    for i in range(256):
        dut.data.value = i
        dut.we.value = 1
        await RisingEdge(dut.clk)
        dut.data.value = 0
        dut.we.value = 0
        await ClockCycles(dut.clk, round(12500 / 1200 * 20))


def test_uart_tx():
    dut = UARTTx()
    run(
        dut,
        get_current_module(),
        ports=dut.get_ports(),
        simulator=Icarus,
        vcd_file="test_uart_tx.vcd",
    )
