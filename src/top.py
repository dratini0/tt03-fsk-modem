#!/usr/bin/env python3

from amaranth import *
from amaranth.back import verilog


class FSKModemTop(Elaboratable):
    """The top level, responsible for pinout definition"""

    def __init__(self):
        self.io_in = Signal(8)
        self.io_out = Signal(8)

        self._counter1 = Signal(signed(8))
        self._counter2 = Signal(signed(8))
        self._counter3 = Signal(signed(8))
        self._counter4 = Signal(signed(8))

    def elaborate(self, platform):
        m = Module()

        clk_in = self.io_in[0]
        rst = self.io_in[1]

        # Set up clock domain from io_in[0]
        cd_sync = ClockDomain("sync")
        m.d.comb += cd_sync.clk.eq(clk_in)
        m.d.comb += cd_sync.rst.eq(rst)
        m.domains += cd_sync

        m.d.sync += [
            self._counter1.eq(self._counter1 + 7),
            self._counter2.eq(self._counter2 + 11),
            self._counter3.eq(self._counter3 + 13),
            self._counter4.eq(self._counter4 + 17),
        ]
        m.d.comb += self.io_out[0].eq((self._counter1 * self._counter2 >> 7) > (self._counter3 * self._counter4 >> 7))

        return m

    def get_ports(self):
        return [self.io_in, self.io_out]


if __name__ == "__main__":
    top = FSKModemTop()
    print(
        verilog.convert(
            top,
            ports=top.get_ports(),
            name="dratini0_fsk_modem_top",
            emit_src=False,
            strip_internal_attrs=True,
        )
    )
