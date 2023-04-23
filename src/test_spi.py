#!/usr/bin/env python3
from __future__ import annotations

from amaranth import *

from amaranth_cocotb import run, get_current_module

import cocotb
from cocotb.triggers import ClockCycles, RisingEdge
from cocotb_test.simulator import Icarus

from spi import SPI
from util import bytes_to_bitstream, cocotb_header, send_bitstream


async def collect_bus_data(dut, result: list[int]):
    while True:
        await RisingEdge(dut.clk)
        if dut.we.value:
            result.append(int(dut.data.value))


async def cocotb_header_module(dut):
    dut.cs_n.value = 1
    dut.sck.value = 0
    dut.mosi.value = 0
    result = []
    cocotb.start_soon(collect_bus_data(dut, result))
    await cocotb_header(dut)
    return result


@cocotb.test()
async def unstable_clock(dut):
    result = await cocotb_header_module(dut)

    await ClockCycles(dut.clk, 5)
    dut.cs_n.value = 0
    await ClockCycles(dut.clk, 1)
    dut.mosi.value = 1
    await ClockCycles(dut.clk, 1)
    dut.sck.value = 1
    await ClockCycles(dut.clk, 3)
    dut.mosi.value = 0
    await ClockCycles(dut.clk, 4)
    dut.sck.value = 0
    await ClockCycles(dut.clk, 5)
    dut.sck.value = 1
    await ClockCycles(dut.clk, 6)
    dut.sck.value = 0
    await ClockCycles(dut.clk, 7)
    dut.mosi.value = 1
    await ClockCycles(dut.clk, 8)
    dut.sck.value = 1
    await ClockCycles(dut.clk, 9)
    dut.sck.value = 0
    dut.mosi.value = 0
    await ClockCycles(dut.clk, 10)
    dut.sck.value = 1
    await ClockCycles(dut.clk, 11)
    dut.sck.value = 0
    dut.mosi.value = 1
    await ClockCycles(dut.clk, 12)
    dut.sck.value = 1
    await ClockCycles(dut.clk, 13)
    dut.sck.value = 0
    dut.mosi.value = 0
    await ClockCycles(dut.clk, 14)
    dut.sck.value = 1
    await ClockCycles(dut.clk, 15)
    dut.sck.value = 0
    dut.mosi.value = 1
    await ClockCycles(dut.clk, 16)
    dut.sck.value = 1
    await ClockCycles(dut.clk, 17)
    dut.sck.value = 0
    dut.mosi.value = 0
    await ClockCycles(dut.clk, 18)
    dut.sck.value = 1
    await ClockCycles(dut.clk, 19)
    dut.sck.value = 0
    await ClockCycles(dut.clk, 20)
    dut.cs_n.value = 1
    await ClockCycles(dut.clk, 2)

    assert result == [0xAA]


@cocotb.test()
async def lots_of_data(dut):
    result = await cocotb_header_module(dut)

    await send_bitstream(dut, bytes_to_bitstream(range(128)))
    await send_bitstream(dut, bytes_to_bitstream(range(128, 256)))
    await ClockCycles(dut.clk, 2)
    assert result == list(range(256))


@cocotb.test()
async def ignore_when_cs_high(dut):
    result = await cocotb_header_module(dut)

    await send_bitstream(dut, bytes_to_bitstream([0xF0]))

    dut.sck.value = 1
    await RisingEdge(dut.clk)
    dut.sck.value = 0
    dut.mosi.value = 1
    await RisingEdge(dut.clk)
    dut.sck.value = 1
    await RisingEdge(dut.clk)
    dut.sck.value = 0
    dut.mosi.value = 1
    await RisingEdge(dut.clk)

    await send_bitstream(dut, bytes_to_bitstream([0xF0]))

    await ClockCycles(dut.clk, 2)
    assert result == [0xF0, 0xF0]


@cocotb.test()
async def partial_byte_recovery(dut):
    result = await cocotb_header_module(dut)

    await send_bitstream(dut, [0, 0, 0, 0])
    await send_bitstream(dut, bytes_to_bitstream([0xF0]))

    await ClockCycles(dut.clk, 2)
    assert result == [0xF0]


def test_one_shot():
    spi = SPI()
    run(
        spi,
        get_current_module(),
        ports=spi.get_ports(),
        simulator=Icarus,
        vcd_file="test_spi.vcd",
    )
