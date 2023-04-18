#!/usr/bin/env python3

from amaranth import *

from util import main


class WaveLUT(Elaboratable):
    def __init__(self, width=10):
        self.in_ = Signal(width)
        self.out = Signal(width)

    def elaborate(self, platform):
        m = Module()
        with m.If(~self.in_[-1]):
            m.d.comb += self.out.eq(self.in_[:-1] << 1)
        with m.Else():
            m.d.comb += self.out.eq(~(self.in_[:-1] << 1))

        return m

    def get_ports(self):
        return [self.in_, self.out]


class WaveGen(Elaboratable):
    def __init__(self, width=10):
        self.frequency = Signal(width)
        self.out = Signal(width)

        self._state = Signal(width, reset_less=True)
        self._lut = WaveLUT(width)

    def elaborate(self, platform):
        m = Module()

        m.submodules.lut = self._lut
        m.d.comb += [
            self._lut.in_.eq(self._state),
            self.out.eq(self._lut.out),
        ]

        m.d.sync += self._state.eq(self._state + self.frequency)

        return m

    def get_ports(self):
        return [self.frequency, self.out]


if __name__ == "__main__":
    main(WaveGen(10))
