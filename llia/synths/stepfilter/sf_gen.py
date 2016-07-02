# llia.synths.stepfilter.sf_gen
# 2016.06.30

from __future__ import print_function
from random import randrange

from llia.synths.stepfilter.sf_data import sfilter
from llia.util.lmath import *


def gamut_1():
    return [0.5, 0.75, 1, 2, 3, 4, 5, 6]

def harmonic_gamut():
    return [1, 2, 3, 4, 5, 6, 7, 8]

def random_gamut():
    acc = []
    for i in range(8):
        acc.append(rnd(8))
    acc.sort()
    return acc

def arithmetic_gamut():
    acc = []
    delta = rnd()
    r = 1
    for i in range(8):
        acc.append(r)
        r += delta
    acc.sort()
    return acc

def geometric_gamut():
    acc = []
    ratio = 1 + rnd()
    r = 1
    for i in range(8):
        acc.append(r)
        r *= ratio
    acc.sort()
    return acc

def pick_gamut():
    acc = coin(0.8, coin(0.8, gamut_1, harmonic_gamut),
               pick([random_gamut(), arithmetic_gamut(), geometric_gamut()]))
    return acc

def pick_pulse_mix():
    acc = []
    less = coin(0.80)
    sum = 0
    if less:
        for i in range(8):
            v = coin(0.25, rnd(), 0)
            sum += v
            acc.append(v)
    else: # More
        for i in range(8):
            v = coin(0.75, rnd(), 0)
            sum += v
            acc.append(v)
    if not sum:
        i = pick([0,1,2,3,4,5,6,7])
        acc[i] = 1
    return acc
    

def gen_stepfilter_program(slot=127, *_):
    clk = rnd(3)
    amin = pick([50, 100, 100, 100, 200, 400])
    amax = pick([500, 800, 1600, 2000, 2000, 3000, 4000])
    bmin = pick([50, 100, 100, 100, 200, 400]),
    bmax = pick([500, 800, 1600, 2000, 2000, 3000, 4000])
    rs = sfilter(slot, "Random",
                 clockFreq = clk,
                 r = pick_gamut(),
                 a = pick_pulse_mix(),
                 b = pick_pulse_mix(),
                 alag = coin(0.75, rnd(0.2), coin(0.50, 0, rnd())),
                 arange = [amin, amax],
                 ares = rnd(),
                 blag = coin(0.75, rnd(0.2), coin(0.50, 0, rnd())),
                 brange = [bmin, bmax],
                 bres = rnd(),
                 lfofreq = clk * pick([0.1, 0.2, 0.25, 0.333, 0.5, 0.75, 1,
                                       1.5, 2, 3, 4, 5, 6, 8]),
                 apan = [random_sign(), coin(0.5, rnd(), 0)],
                 bpan = [random_sign(), coin(0.5, rnd(), 0), pick([0.25, 0.5, 1, 2, 3, 4])],
                 drypan = [random_sign(), coin(0.5, rnd(), 0)],
                 mix = [coin(0.50, 0, rnd()), 0.5+rnd(0.5), 0.5+rnd(0.5)],
                 amp = 1.0)
    print("DEBUG HERE")
    return rs
