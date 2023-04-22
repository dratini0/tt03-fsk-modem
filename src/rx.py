#!/usr/bin/env python3

from functools import reduce
from operator import __add__

from amaranth import *

import numpy as np
from scipy.signal import firwin

from util import main


class RxFilter(Elaboratable):
    def __init__(self, filter_size=31):
        # Now do this with Verilog.
        filter_designed = firwin(filter_size, 300, fs=12500)
        self._filter_exponents = np.int32(
            np.round(np.log(filter_designed / filter_designed[0]) / np.log(2))
        )
        self._filter = np.int32(np.exp2(self._filter_exponents))

        self.in_ = Signal(1)
        self.out = Signal(range(sum(self._filter) + 1))

        self._x = Signal(filter_size - 1, reset_less=True)

    def elaborate(self, platform):
        m = Module()

        m.d.sync += [self._x[0].eq(self.in_), self._x[1:].eq(self._x[:-1])]

        result = reduce(
            __add__,
            (x << int(e) for (x, e) in zip(self._x, self._filter_exponents[1:])),
            self.in_,
        )

        m.d.comb += [
            self.out.eq(result),
        ]

        return m

    def get_ports(self):
        return [self.in_, self.out]

    def get_filter(self):
        return [
            self._filter,
            [1.0] + [0.0] * 14,
        ]

    def get_gain(self):
        return int(np.sum(self._filter))


class IQMixer(Elaboratable):
    def __init__(self, width):
        self.in_ = Signal(signed(width))
        self.frequency = Signal(10)

        self.i = Signal(signed(width))
        self.q = Signal(signed(width))

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


class PhaseDifferentiator(Elaboratable):
    def __init__(self):
        self.phase = Signal(3)

        self.out = Signal(reset_less=True)
        self.valid = Signal()

        self._last_phase = Signal(3, reset_less=True)
        self._valid_counter_reset = Signal(1)
        self._valid_counter = Signal(10, reset_less=True)

    def elaborate(self, platform):
        m = Module()

        m.d.comb += self.valid.eq(self._valid_counter == 0x3FF)
        m.d.sync += self._last_phase.eq(self.phase)

        with m.Switch((self.phase - self._last_phase)[:3]):
            with m.Case(0):
                m.d.comb += self._valid_counter_reset.eq(0)
            with m.Case(-1):
                m.d.sync += self.out.eq(1)
                m.d.comb += self._valid_counter_reset.eq(0)
            with m.Case(1):
                m.d.sync += self.out.eq(0)
                m.d.comb += self._valid_counter_reset.eq(0)
            with m.Default():
                m.d.comb += self._valid_counter_reset.eq(1)

        with m.If(self._valid_counter_reset):
            m.d.sync += self._valid_counter.eq(0)
        with m.Else():
            m.d.sync += self._valid_counter.eq(self._valid_counter + ~self.valid)

        return m

    def get_ports(self):
        return [self.phase, self.out, self.valid]


class GlitchFilter(Elaboratable):
    def __init__(self, threshold=3):
        self.in_ = Signal()
        self.out = Signal(reset_less=True)

        self._threshold = threshold
        self._count = Signal(range(threshold + 1), reset_less=True)

    def elaborate(self, platform):
        m = Module()

        with m.If(self.in_ == self.out):
            m.d.sync += self._count.eq(0)
        with m.Elif(self._count == self._threshold):
            m.d.sync += [
                self._count.eq(0),
                self.out.eq(self.in_),
            ]
        with m.Else():
            m.d.sync += self._count.eq(self._count + 1)

        return m

    def get_ports(self):
        return [self.in_, self.out]


class Rx(Elaboratable):
    def __init__(self):
        self.in_ = Signal(1)
        self.frequency = Signal(10)
        self.frequency_invert = Signal()

        self.out = Signal()
        self.valid = Signal()

        self._mixer = IQMixer(1)
        self._i_filter = RxFilter()
        self._q_filter = RxFilter()
        self._phase_detector = PhaseDetector(10)
        self._phase_differentiator = PhaseDifferentiator()
        self._glitch_filter = GlitchFilter(3)

    def elaborate(self, platform):
        m = Module()

        m.submodules.mixer = self._mixer
        m.submodules.i_filter = self._i_filter
        m.submodules.q_filter = self._q_filter
        m.submodules.phase_detector = self._phase_detector
        m.submodules.phase_differentiator = self._phase_differentiator
        m.submodules.glitch_filter = self._glitch_filter

        m.d.comb += [
            self._mixer.in_.eq(self.in_),
            self._mixer.frequency.eq(self.frequency),
            self._i_filter.in_.eq(self._mixer.i),
            self._q_filter.in_.eq(self._mixer.q),
            self._phase_detector.i.eq(
                self._i_filter.out - self._i_filter.get_gain() // 2
            ),
            self._phase_detector.q.eq(
                self._q_filter.out - self._q_filter.get_gain() // 2
            ),
            self._phase_differentiator.phase.eq(self._phase_detector.phase),
            self._glitch_filter.in_.eq(self._phase_differentiator.out),
            self.out.eq(self._glitch_filter.out ^ self.frequency_invert),
            self.valid.eq(self._phase_differentiator.valid),
        ]

        return m

    def get_ports(self):
        return [self.in_, self.frequency, self.frequency_invert, self.out, self.valid]


if __name__ == "__main__":
    main(Rx())
