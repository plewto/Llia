# llia.synths.lfo2.lfo2_random

from __future__ import print_function

from llia.util.lmath import *
from llia.synths.lfo2.lfo2_data import lfo2



def pick_clock_frequency():
    f = coin(0.75, 0.5+rnd(3),
             coin(0.50, rnd(0.5), rnd(8)))
    return f

def pick_frequency_ratios(clkfreq):
    low_ratios = [0.5, 1, 1.5, 2, 2.5]
    high_ratios = [1,2,2,3,3,3,4,4,4,4,5,6,6,7,8,9,12]
    if clkfreq >= 5:
        saw = coin(0.80, pick(low_ratios), rnd(8))
        pls = coin(0.80, pick(low_ratios), rnd(8))
    else:
        saw = coin(0.8, pick(high_ratios), rnd(8))
        pls = coin(0.8, pick(high_ratios), rnd(8))
    return saw,pls


def random_lfo2(slot=127, *_):
    clk_freq = pick_clock_frequency()
    clk_pw = coin(0.80, 0.5, 0.1 * rnd(0.8))
    clk_amp = 0.0
    saw_ratio, pulse_ratio = pick_frequency_ratios(clk_freq)
    saw_shape = pick([0.0, 0.5, 0.5, 1.0, rnd()])
    saw_amp = 1.0
    saw_bleed = coin(0.75, 0, coin(0.5, 1, rnd()))
    pulse_width = coin(0.80, 0.5, rnd())
    pulse_amp = 1.0
    pulse_bleed = coin(0.75, 0, coin(0.5, 1, rnd()))
    lag = coin(0.80, 0.0, rnd())
    p = lfo2(slot,"Random",
             clock = [clk_freq, clk_pw, clk_amp],
             saw = [saw_ratio, saw_shape, saw_amp, saw_bleed],
             pulse = [pulse_ratio, pulse_width, pulse_amp, pulse_bleed],
             bias = [0.0, 0.0],
             lag = lag)
    return p
