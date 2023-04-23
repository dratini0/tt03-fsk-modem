#!/usr/bin/env python3
from amaranth import *
from amaranth.cli import main
from amaranth.lib.enum import Enum

from util import main, OneShot


class UARTState(Enum):
    READY = 0
    START = 1
    DATA = 2
    STOP = 3


class FancyUARTRx(Elaboratable):
    def __init__(self):
        self.in_ = Signal()
        self.width = Signal(range(9))
        self.frequency = Signal(10)

        self.data = Signal(8, reset_less=True)
        self.we = Signal(reset_less=True)

        self._state = Signal(UARTState, reset=UARTState.READY)
        self._bit_index = Signal(3, reset_less=True)
        self._vote = Signal(signed(9), reset_less=True)
        self._clock = Signal(10, reset_less=True)
        self._clock_overflow = Signal()

        self._edge = OneShot()

    def elaborate(self, platform):
        m = Module()

        m.submodules.edge = self._edge
        m.d.comb += self._edge.in_.eq(~self.in_)

        m.d.comb += self._clock_overflow.eq((self._clock + self.frequency)[10])

        m.d.sync += [
            self._clock.eq(self._clock + self.frequency),
            self._vote.eq(self._vote + Mux(self.in_, 1, -1)),
            self.we.eq(0),
        ]

        with m.If(self._clock_overflow):
            m.d.sync += [
                self._vote.eq(0),
                self.data.eq(Cat(self.data[1:], self._vote >= 0)),
                self._bit_index.eq(self._bit_index + 1),
            ]

        with m.Switch(self._state):
            with m.Case(UARTState.READY):
                with m.If(self._edge.out):
                    m.d.sync += [
                        self._state.eq(UARTState.START),
                        self._vote.eq(0),
                        self._clock.eq(0),
                    ]
            with m.Case(UARTState.START):
                with m.If(self._clock_overflow):
                    with m.If(self._vote < 0):
                        m.d.sync += [
                            self._state.eq(UARTState.DATA),
                            self._bit_index.eq(0),
                        ]
                    with m.Else():
                        m.d.sync += self._state.eq(UARTState.READY)
            with m.Case(UARTState.DATA):
                with m.If(self._clock_overflow):
                    with m.If(self._bit_index + 1 == self.width):
                        m.d.sync += [
                            self.we.eq(1),
                            self._state.eq(UARTState.STOP),
                            self._clock.eq(self._clock + self.frequency + (1 << 8))
                        ]
            with m.Case(UARTState.STOP):
                with m.If(self._clock_overflow):
                    m.d.sync += self._state.eq(UARTState.READY)

        return m

    def get_ports(self):
        return [self.in_, self.width, self.frequency, self.data, self.we]


class UARTTx(Elaboratable):
    def __init__(self):
        self.data = Signal(8)
        self.we = Signal()
        self.frequency = Signal(10)

        self.out = Signal()

        self._state = Signal(UARTState, reset=UARTState.READY)
        self._bit_index = Signal(3, reset_less=True)
        self._clock = Signal(10, reset_less=True)
        self._clock_overflow = Signal()
        self._data = Signal(8, reset_less=True)

    def elaborate(self, platform):
        m = Module()

        m.d.comb += self._clock_overflow.eq((self._clock + self.frequency)[10])

        m.d.sync += [
            self._clock.eq(self._clock + self.frequency),
        ]

        with m.If(self._clock_overflow):
            m.d.sync += [
                self._bit_index.eq(self._bit_index + 1),
            ]

        with m.Switch(self._state):
            with m.Case(UARTState.READY):
                m.d.comb += self.out.eq(1)
            with m.Case(UARTState.START):
                m.d.comb += self.out.eq(0)
                with m.If(self._clock_overflow):
                    m.d.sync += self._state.eq(UARTState.DATA),
            with m.Case(UARTState.DATA):
                m.d.comb += self.out.eq(self._data[0])
                with m.If(self._clock_overflow):
                    m.d.sync += self._data.eq(self._data[1:])
                    with m.If(self._bit_index == 0):
                        m.d.sync += self._state.eq(UARTState.READY)

        with m.If(self.we):
            m.d.sync += [
                self._data.eq(self.data),
                self._bit_index.eq(0),
                self._state.eq(UARTState.START),
                self._clock.eq(0),
            ]

        return m

    def get_ports(self):
        return [self.data, self.we, self.frequency, self.out]


if __name__ == "__main__":
    main(FancyUARTRx())
