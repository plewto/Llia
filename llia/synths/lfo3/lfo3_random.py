# llia.synths.lfo3.lfo3_random

from __future__ import print_function

from llia.util.lmath import *
from llia.synths.lfo3.lfo3_data import lfo3, HARMONICS

def pick_freq():
    f = coin(0.75, rnd(1),
             coin(0.75, rnd(0.1), rnd(10)))
    return f

def pick_mod_freq(f):
    if coin(0.75):
        if coin(0.75):
            r = pick([0.125,0.25,0.333,0.375,0.5,0.667,0.675,0.75,0.875])
        else:
            r = pick(HARMONICS)
    else:
        r = rnd()
    return f*r

def pick_ratios():
    acc = []
    for i in range(3):
        r = pick(HARMONICS)
        acc.append(r)
    return acc

def pick_amps():
    acc = [1]
    for i in range(2):
        a = coin(0.75, 1, rnd())
        acc.append(a)
    return acc

def pick_envelope():
    delay = coin(0.75, rnd(1), rnd(8))
    attack = coin(0.75, delay, rnd(8))
    hold = coin(0.50, 0, rnd(1))
    release = coin(0.75, hold, rnd(3))
    return [delay,attack,hold,release]

def pick_fm():
    e = coin(0.90, 0.0, rnd(4))
    m = coin(0.90, 0.0, rnd(4))
    return [e,m]

def pick_am():
    bleed = coin(0.75, 1.0, 0.0)
    am = coin(0.90, 0.0, rnd())
    return [bleed,am]


def random_lfo3(slot, *_):
    freq = pick_freq()
    mod_freq = pick_mod_freq(freq)
    p = lfo3(slot, "Random",
             freq = freq,
             ratios = pick_ratios(),
             amps = pick_amps(),
             am = pick_am(),
             fm = pick_fm(),
             mod_freq = mod_freq,
             scale = 1.0,
             bias = 0)
    return p
    
             
                  
