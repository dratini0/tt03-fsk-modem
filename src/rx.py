#!/usr/bin/env python3

from amaranth import *

from util import main


class RxFilter(Elaboratable):
    def __init__(self):
        self.in_ = Signal(signed(5))
        self.out = Signal(signed(11))

        self._v = [Signal(signed(11), name=f"v_{i}") for i in range(3)]

    def elaborate(self, platform):
        m = Module()

        m.d.sync += [
            self._v[1].eq(self._v[0]),
            self._v[2].eq(self._v[1]),
        ]

        m.d.comb += [
            self.out.eq(((self._v[0]) + (self._v[1] << 1) + (self._v[2]) + 1) >> 2),
            self._v[0].eq(
                (
                    (self.in_ << 3)
                    + (self.in_ << 2)
                    + (57 * self._v[1] >> 2)
                    - (26 * self._v[2] >> 2)
                    + (1 << 2)
                )
                >> 3
            ),
        ]

        return m

    def get_ports(self):
        return [self.in_, self.out]

    @staticmethod
    def get_iir():
        return [[1.5 / 4, 1.5 / 2, 1.5 / 4], [1.0, -57 / 32, 26 / 32]]


class IQMixer(Elaboratable):
    def __init__(self):
        self.in_ = Signal(signed(5))
        self.frequency = Signal(10)

        self.i = Signal(signed(5))
        self.q = Signal(signed(5))

        self._phase = Signal(10, reset_less=True)

    def elaborate(self, platform):
        m = Module()

        m.d.sync += self._phase.eq(self._phase + self.frequency)

        with m.Switch(self._phase[-2:]):
            with m.Case(0):
                m.d.comb += [
                    self.i.eq(self.in_),
                    self.q.eq(self.in_),
                ]
            with m.Case(1):
                m.d.comb += [
                    self.i.eq(self.in_),
                    self.q.eq(~self.in_),
                ]
            with m.Case(2):
                m.d.comb += [
                    self.i.eq(~self.in_),
                    self.q.eq(~self.in_),
                ]
            with m.Case(3):
                m.d.comb += [
                    self.i.eq(~self.in_),
                    self.q.eq(self.in_),
                ]

        return m

    def get_ports(self):
        return [self.in_, self.frequency, self.i, self.q]


class PhaseDetector(Elaboratable):
    def __init__(self, width):
        self.i = Signal(signed(width))
        self.q = Signal(signed(width))

        self.phase = Signal(3)

    def _abs(self, signal):
        return Mux(signal >= 0, signal, ~signal)

    def elaborate(self, platform):
        m = Module()

        with m.Switch(
            Cat(self._abs(self.i) > self._abs(self.q), self.i >= 0, self.q >= 0)
        ):
            with m.Case(0b111):
                m.d.comb += self.phase.eq(0)
            with m.Case(0b110):
                m.d.comb += self.phase.eq(1)
            with m.Case(0b100):
                m.d.comb += self.phase.eq(2)
            with m.Case(0b101):
                m.d.comb += self.phase.eq(3)
            with m.Case(0b001):
                m.d.comb += self.phase.eq(4)
            with m.Case(0b000):
                m.d.comb += self.phase.eq(5)
            with m.Case(0b010):
                m.d.comb += self.phase.eq(6)
            with m.Case(0b011):
                m.d.comb += self.phase.eq(7)
        return m

    def get_ports(self):
        return [self.i, self.q, self.phase]


if __name__ == "__main__":
    main(WaveGen(10))
