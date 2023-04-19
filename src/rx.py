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
            self.out.eq((self._v[0] >> 2) + (self._v[1] >> 1) + (self._v[2] >> 2)),
            self._v[0].eq(
                self.in_
                + (self.in_ >> 1)
                + (57 * self._v[1] >> 5)
                - (26 * self._v[2] >> 5)
            ),
        ]

        return m

    def get_ports(self):
        return [self.in_, self.out]

    @staticmethod
    def get_iir():
        return [[1.5 / 4, 1.5 / 2, 1.5 / 4], [1.0, -57 / 32, 26 / 32]]


if __name__ == "__main__":
    main(WaveGen(10))
