#!/usr/bin/env python3

from amaranth import *
from amaranth.back import verilog

from rx import Rx
from wave_gen import WaveGen
from spi import SPI


class Registers(Elaboratable):
    def __init__(self):
        self.data_in = Signal(8)
        self.we = Signal(8)

        self.wg1_freq_space = Signal(12, reset_less=True)
        self.wg1_freq_mark = Signal(12, reset_less=True)
        self.wg2_freq = Signal(12, reset_less=True)
        self.wg_mux_cfg = Signal(2, reset_less=True)

        self.mixer_freq = Signal(12, reset_less=True)
        self.frequency_invert = Signal(1, reset_less=True)
        self.enforce_validity = Signal(1, reset_less=True)

    def elaborate(self, platform):
        m = Module()

        address = self.data_in[4:8]
        data = self.data_in[0:4]
        with m.If(self.we):
            with m.Switch(self.data_in[4:8]):
                with m.Case(0):
                    m.d.sync += self.wg1_freq_space[0:4].eq(data)
                with m.Case(1):
                    m.d.sync += self.wg1_freq_space[4:8].eq(data)
                with m.Case(2):
                    m.d.sync += self.wg1_freq_space[8:12].eq(data)
                with m.Case(3):
                    m.d.sync += self.wg1_freq_mark[0:4].eq(data)
                with m.Case(4):
                    m.d.sync += self.wg1_freq_mark[4:8].eq(data)
                with m.Case(5):
                    m.d.sync += self.wg1_freq_mark[8:12].eq(data)
                with m.Case(6):
                    m.d.sync += self.wg2_freq[0:4].eq(data)
                with m.Case(7):
                    m.d.sync += self.wg2_freq[4:8].eq(data)
                with m.Case(8):
                    m.d.sync += self.wg2_freq[8:12].eq(data)
                with m.Case(9):
                    m.d.sync += self.wg_mux_cfg.eq(data[0:2])
                with m.Case(10):
                    m.d.sync += self.mixer_freq[0:4].eq(data)
                with m.Case(11):
                    m.d.sync += self.mixer_freq[4:8].eq(data)
                with m.Case(12):
                    m.d.sync += self.mixer_freq[8:12].eq(data)
                with m.Case(13):
                    m.d.sync += self.frequency_invert.eq(data[0])
                    m.d.sync += self.enforce_validity.eq(data[1])
        return m


class WaveGenMux(Elaboratable):
    def __init__(self, width):
        self.in1 = Signal(width)
        self.in2 = Signal(width)
        self.cfg = Signal(2)

        self.out = Signal(width)

    def elaborate(self, platform):
        m = Module()

        with m.Switch(self.cfg):
            with m.Case(0):
                m.d.comb += self.out[:-1].eq(0)
                m.d.comb += self.out[-1].eq(1)
            with m.Case(1):
                m.d.comb += self.out.eq(self.in1)
            with m.Case(2):
                m.d.comb += self.out.eq((self.in1 + self.in2) >> 1)

        return m


class FSKModem(Elaboratable):
    def __init__(self):
        self.cs_n = Signal()
        self.sck = Signal()
        self.mosi = Signal()
        self.data_in = Signal()
        self.samples_in = Signal()

        self.data_out = Signal()
        self.valid_out = Signal()
        self.samples_out = Signal(6)

        self._rx = Rx()
        self._wg1 = WaveGen(14)
        self._wg2 = WaveGen(14)
        self._wgmux = WaveGenMux(6)
        self._spi = SPI()
        self._registers = Registers()

    def elaborate(self, platform):
        m = Module()
        m.submodules.rx = self._rx
        m.submodules.wg1 = self._wg1
        m.submodules.wg2 = self._wg2
        m.submodules.wgmux = self._wgmux
        m.submodules.spi = self._spi
        m.submodules.registers = self._registers

        m.d.comb += [
            self._spi.cs_n.eq(self.cs_n),
            self._spi.sck.eq(self.sck),
            self._spi.mosi.eq(self.mosi),
            self._registers.data_in.eq(self._spi.data),
            self._registers.we.eq(self._spi.we),
        ]
        m.d.comb += [
            self._wg1.frequency.eq(
                Mux(
                    self.data_in,
                    self._registers.wg1_freq_mark,
                    self._registers.wg1_freq_space,
                )
            ),
            self._wg2.frequency.eq(self._registers.wg2_freq),
            self._wgmux.in1.eq(self._wg1.out[-6:]),
            self._wgmux.in2.eq(self._wg2.out[-6:]),
            self._wgmux.cfg.eq(self._registers.wg_mux_cfg),
            self.samples_out.eq(self._wgmux.out),
        ]
        m.d.comb += [
            self._rx.in_.eq(self.samples_in),
            self._rx.frequency.eq(self._registers.mixer_freq),
            self._rx.frequency_invert.eq(self._registers.frequency_invert),
            self.data_out.eq(
                self._rx.out | (self._registers.enforce_validity & ~self._rx.valid)
            ),
            self.valid_out.eq(self._rx.valid),
        ]
        return m

    def get_ports(self):
        return [
            self.cs_n,
            self.sck,
            self.mosi,
            self.data_in,
            self.samples_in,
            self.data_out,
            self.valid_out,
            self.samples_out,
        ]


class FSKModemTop(Elaboratable):
    """The top level, responsible for pinout definition"""

    def __init__(self):
        self.io_in = Signal(8)
        self.io_out = Signal(8)

        self._fsk_modem = FSKModem()

    def elaborate(self, platform):
        m = Module()

        clk_in = self.io_in[0]
        rst = self.io_in[1]
        cs_n = self.io_in[2]
        sck = self.io_in[3]
        mosi = self.io_in[4]
        data_in = self.io_in[5]
        samples_in = self.io_in[7]
        data_out = self.io_out[0]
        valid_out = self.io_out[1]
        samples_out = self.io_out[2:8]

        # Set up clock domain from io_in[0]
        cd_sync = ClockDomain("sync")
        m.d.comb += cd_sync.clk.eq(clk_in)
        m.d.comb += cd_sync.rst.eq(rst)
        m.domains += cd_sync

        m.submodules.fsk_modem = self._fsk_modem
        m.d.comb += [
            self._fsk_modem.cs_n.eq(cs_n),
            self._fsk_modem.sck.eq(sck),
            self._fsk_modem.mosi.eq(mosi),
            self._fsk_modem.data_in.eq(data_in),
            self._fsk_modem.samples_in.eq(samples_in),
            data_out.eq(self._fsk_modem.data_out),
            valid_out.eq(self._fsk_modem.valid_out),
            samples_out.eq(self._fsk_modem.samples_out),
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
