# llia.synths.lfo3.lfo3_random

from __future__ import print_function

from llia.util.lmath import *
from llia.synths.lfo3.lfo3_data import lfo3

def pick_common_frequency():
    slow = rnd()
    med = 1 + rnd(9)
    fast = rnd(100)
    return coin(0.75, med,
                coin(0.75, slow, fast))

def select_frequency_ratios():
    simple = (0.25, 0.333, 0.5, 0.667, 0.75,
              1.0, 1.5, 2.0, 3, 4)
    slow = (0.25, 0.125, 0.1, 0.0625, 0.03125)
    fast = (5,6,8,9,10,12,16)
    a = 1
    b = coin(0.75, pick(simple),
             coin(0.75, coin(0.75, pick(slow), pick(fast)),
                  0.01 + rnd(16)))
    c = coin(0.75, pick(simple),
             coin(0.75, coin(0.75, pick(slow), pick(fast)),
                  0.01 + rnd(16)))
    return a,b,c
    
def select_phases():
    s1 = (0.000, 0.333, 0.667)
    s2 = (0.000, 0.000, 0.000)
    s3 = (0.000, 0.111, 0.222)
    s4 = (0.000, rnd(), rnd())
    rs = coin(0.75, s1,
              coin(0.75, s2,
                   coin(0.5, s3, s4)))
    return rs

def select_envelope_bleeds():
    a = coin(0.75, 1.0, coin(0.75, 0.0, rnd()))
    b = coin(0.75, 1.0, coin(0.75, 0.0, rnd()))
    c = coin(0.75, 1.0, coin(0.75, 0.0, rnd()))
    return a,b,c

def select_envelope():
    dly = coin(0.75, 0.0, rnd(4))
    att = coin(0.75, dly, rnd(4))
    hld = coin(0.80, 1, rnd())
    rel = coin(0.75, hld, rnd(4))
    return dly, att, hld, rel

def random_lfo3_avoid_feedback(slot):
    freq = pick_common_frequency()
    ratios = select_frequency_ratios()
    phases = select_phases()
    bleeds = select_envelope_bleeds()
    env = select_envelope()
    p = lfo3(slot, "Random - no feedback",
             freq = freq,
             a = {"ratio" : ratios[0],
                  "phase" : phases[0],
                  "bleed" : bleeds[0],
                  "scale" : 1.0,
                  "bias"  : 0.0,
                  "bFreqMod" : 0.0},
             b = {"ratio" : ratios[1],
                  "phase" : phases[1],
                  "bleed" : bleeds[1],
                  "scale" : 1.0,
                  "bias"  : 0.0,
                  "envFreqMod" : coin(0.75, 0.0, rnd(2)),
                  "aFreqMod" : coin(0.75, 0.0, rnd(2)),
                  "cAmpMod" : 0.0},
             c = {"ratio" : ratios[2],
                  "phase" : phases[2],
                  "bleed" : bleeds[2],
                  "scale" : 1.0,
                  "bias"  : 0.0,
                  "bAmpMod" : coin(0.75, 0.0, rnd())},
             env = {"delay" : env[0],
                    "attack" : env[1],
                    "hold" : env[2],
                    "release" : env[3]})
    return p

def random_lfo3_allow_feedback(slot):
    freq = pick_common_frequency()
    ratios = select_frequency_ratios()
    phases = select_phases()
    bleeds = select_envelope_bleeds()
    env = select_envelope()
    p = lfo3(slot, "Random - (possible feedback)",
             freq = freq,
             a = {"ratio" : ratios[0],
                  "phase" : phases[0],
                  "bleed" : bleeds[0],
                  "scale" : 1.0,
                  "bias"  : 0.0,
                  "bFreqMod" : coin(0.50, 0.0, rnd(2))},
             
             b = {"ratio" : ratios[1],
                  "phase" : phases[1],
                  "bleed" : bleeds[1],
                  "scale" : 1.0,
                  "bias"  : 0.0,
                  "envFreqMod" : coin(0.75, 0.0, rnd(2)),
                  "aFreqMod" : coin(0.75, 0.0, rnd(2)),
                  "cAmpMod" : coin(0.5, 0.0, rnd())},
             
             c = {"ratio" : ratios[2],
                  "phase" : phases[2],
                  "bleed" : bleeds[2],
                  "scale" : 1.0,
                  "bias"  : 0.0,
                  "bAmpMod" : coin(0.75, 0.0, rnd())},
             env = {"delay" : env[0],
                    "attack" : env[1],
                    "hold" : env[2],
                    "release" : env[3]})
    return p

def random_lfo3(slot, *_):
    allow_feedback = coin(0.25)
    if allow_feedback:
        p = random_lfo3_allow_feedback(slot)
    else:
        p = random_lfo3_avoid_feedback(slot)
    return p
    
             
                  
