#!/usr/bin/env python3
from __future__ import annotations

from amaranth import *

from amaranth_cocotb import run, get_current_module

import cocotb
from cocotb.triggers import ClockCycles, RisingEdge
from cocotb_test.simulator import Icarus

from uart import FancyUARTRx
from util import cocotb_header


async def collect_bus_data(dut, result: list[int]):
    while True:
        await RisingEdge(dut.clk)
        if dut.we.value:
            result.append(int(dut.data.value))


@cocotb.test()
async def stable8(dut):
    dut.in_.value = 1
    dut.frequency.value = round(300 / 12500 * 1024)
    dut.width.value = 8
    await cocotb_header(dut)

    result = []
    cocotb.start_soon(collect_bus_data(dut, result))
    bit_period = round(12500 / 300)

    for i in range(256):
        dut.in_.value = 0
        await ClockCycles(dut.clk, bit_period)
        for bit in range(8):
            dut.in_.value = (i & (1 << bit)) != 0
            await ClockCycles(dut.clk, bit_period)
        dut.in_.value = 1
        await ClockCycles(dut.clk, bit_period)

    assert result == list(range(256))


@cocotb.test()
async def stable5(dut):
    dut.in_.value = 1
    dut.frequency.value = round(300 / 12500 * 1024)
    dut.width.value = 5
    await cocotb_header(dut)

    result = []
    cocotb.start_soon(collect_bus_data(dut, result))
    bit_period = round(12500 / 300)

    for i in range(32):
        dut.in_.value = 0
        await ClockCycles(dut.clk, bit_period)
        for bit in range(5):
            dut.in_.value = (i & (1 << bit)) != 0
            await ClockCycles(dut.clk, bit_period)
        dut.in_.value = 1
        await ClockCycles(dut.clk, bit_period)

    assert all(result >> 3 == i for i, result in enumerate(result))


async def send_with_interferer(dut, bit):
    bit_period = round(12500 / 300)
    dut.in_.value = bit
    await ClockCycles(dut.clk, 2 * bit_period // 5)
    dut.in_.value = bit ^ 1
    await ClockCycles(dut.clk, bit_period // 5)
    dut.in_.value = bit
    await ClockCycles(dut.clk, bit_period - 3 * bit_period // 5)


@cocotb.test()
async def interferer(dut):
    dut.in_.value = 1
    dut.frequency.value = round(300 / 12500 * 1024)
    dut.width.value = 8
    await cocotb_header(dut)

    result = []
    cocotb.start_soon(collect_bus_data(dut, result))

    for i in range(256):
        await send_with_interferer(dut, 0)
        for bit in range(8):
            await send_with_interferer(dut, int((i & (1 << bit)) != 0))
        await send_with_interferer(dut, 1)

    print(result)
    assert result == list(range(256))


def test_uart():
    dut = FancyUARTRx()
    run(
        dut,
        get_current_module(),
        ports=dut.get_ports(),
        simulator=Icarus,
        vcd_file="test_uart.vcd",
    )
