# llia.synths.stepfilter.sf_gen
# 2016.06.30

from __future__ import print_function
from random import randrange

import llia.synths.stepfilter.sf_constants as sfcon
from llia.synths.stepfilter.sf_data import sfilter
from llia.util.lmath import *

def pick_gamut():
    k = pick(["default", "harmonic", "odd", "cluster"])
    g = {"default" : sfcon.DEFAULT_GAMUT,
         "harmonic" : sfcon.HARMONIC_GAMUT,
         "odd" : sfcon.ODD_GAMUT,
         "cluster" : sfcon.CLUSTER_GAMUT}[k]
    print("# ", k, g)
    return g

def pick_pulse_mix():
    amp = 0
    acc = []
    p = coin(0.5, 0.25, 0.75)
    for i in range(8):
        if coin(p):
            q = int(rnd()*100)/100.0
            amp += q
            acc.append(q)
    if not amp:
        return pick_pulse_mix()
    return acc

def pick_filter_freq():
    if coin(0.25):
        return pick(sfcon.FILTER_FREQUENCIES)
    else:
        return pick(sfcon.FILTER_FREQUENCIES[:-4])

def pick_filter_frequencies():
    a, b = pick_filter_freq(), pick_filter_freq()
    if a == b:
        return pick_filter_frequencies()
    a, b = min(a,b), max(a,b)
    return a,b

def pick_clocks():
    clk = rnd(3)
    lfo = clk * pick(sfcon.LFO_FREQUENCIES)
    blfo = pick(sfcon.BLFO_RATIOS)
    return (clk, lfo, blfo)

def pick_lag():
    rs = coin(0.75, rnd(0.2), rnd())
    return rs

def pick_res():
    rs = rnd()
    return rs

def gen_stepfilter_program(slot=127, *_):
    clk, lfo, blfo = pick_clocks()
    rs = sfilter(slot, "Random",
                 clockFreq = clk,
                 r = pick_gamut(),
                 a = pick_pulse_mix(),
                 b = pick_pulse_mix(),
                 alag = pick_lag(),
                 arange = pick_filter_frequencies(),
                 ares = pick_res(),
                 blag = pick_lag(),
                 brange = pick_filter_frequencies(),
                 bres = pick_lag(),
                 lfofreq = lfo,
                 apan = [random_sign(), coin(0.5, rnd(), 0)],
                 bpan = [random_sign(), coin(0.5, rnd(), 0),
                         pick(sfcon.BLFO_RATIOS)],
                 drypan = [random_sign(), coin(0.5, rnd(), 0)],
                 mix = [coin(0.5, 0, rnd()), 0.5+rnd(0.5), 0.5+rnd(0.5)],
                 amp = 1.0)
    return rs
                 
    
