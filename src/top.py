#!/usr/bin/env python3

from amaranth import *
from amaranth.back import verilog

from rx import Rx
from wave_gen import WaveGen


class FSKModemTop(Elaboratable):
    """The top level, responsible for pinout definition"""

    def __init__(self):
        self.io_in = Signal(8)
        self.io_out = Signal(8)

        self._rx = Rx()
        self._wg1 = WaveGen()
        self._wg2 = WaveGen()

    def elaborate(self, platform):
        m = Module()

        clk_in = self.io_in[0]
        rst = self.io_in[1]
        control_in = self.io_in[2]
        samples_in = self.io_in[3:8]
        data_out = self.io_out[0]
        valid_out = self.io_out[1]
        samples_out = self.io_out[3:8]

        # Set up clock domain from io_in[0]
        cd_sync = ClockDomain("sync")
        m.d.comb += cd_sync.clk.eq(clk_in)
        m.d.comb += cd_sync.rst.eq(rst)
        m.domains += cd_sync

        m.submodules.rx = self._rx
        m.submodules.wg1 = self._wg1
        m.submodules.wg2 = self._wg2

        m.d.comb += [
            self._rx.frequency.eq(round(1750 / 12500 * 1024)),
            self._wg1.frequency.eq(round(770 / 12500 * 1024)),
            self._wg2.frequency.eq(round(1336 / 12500 * 1024)),
            self._rx.frequency_invert.eq(0),
            self._rx.in_.eq(samples_in),
            data_out.eq(self._rx.out),
            valid_out.eq(self._rx.valid),
            samples_out.eq((self._wg1.out[-5:] + self._wg2.out[-5:])[1:]),
        ]

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
