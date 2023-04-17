#!/usr/bin/env python3
from itertools import chain

from amaranth import *
import amaranth.cli

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge, Timer


class OneShot(Elaboratable):
    def __init__(self, reset_less=True):
        self.in_ = Signal()
        self.last_in = Signal(reset_less=reset_less)
        self.out = Signal()

    def elaborate(self, platform):
        m = Module()
        m.d.sync += self.last_in.eq(self.in_)
        m.d.comb += self.out.eq(self.in_ & ~self.last_in)
        return m

    def get_ports(self):
        return [self.in_, self.out]


def main(fragment):
    amaranth.cli.main(fragment, ports=fragment.get_ports())


async def cocotb_header(dut):
    dut.clk.value = 0
    dut.rst.value = 0
    await Timer(80, "us")
    cocotb.start_soon(Clock(dut.clk, 80, units="us").start())
    dut.rst.value = 1
    await ClockCycles(dut.clk, 5)
    dut.rst.value = 0
    await ClockCycles(dut.clk, 5)


async def divided_clock(dut, period):
    while True:
        dut.hall_in.value = 1
        await ClockCycles(dut.clk, period // 2)
        dut.hall_in.value = 0
        await ClockCycles(dut.clk, period - period // 2)


async def counter_coro(dut, signal, counter):
    while True:
        await RisingEdge(dut.clk)
        counter[0] += int(signal.value)


async def send_bitstream(dut, bitsream):
    await RisingEdge(dut.clk)
    dut.cs_n.value = 0
    for bit in bitsream:
        dut.sck.value = 0
        dut.mosi.value = bit
        await RisingEdge(dut.clk)
        dut.sck.value = 1
        await RisingEdge(dut.clk)
    dut.cs_n.value = 1
    dut.sck.value = 0
    dut.mosi.value = 0
    await RisingEdge(dut.clk)


def bytes_to_bitstream(data):
    return list(
        chain.from_iterable(
            [byte & (1 << bit) != 0 for bit in range(7, -1, -1)] for byte in data
        )
    )
