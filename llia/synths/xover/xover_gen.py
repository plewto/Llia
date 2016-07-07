# llia.synths.xover.xover_gen

from __future__ import print_function
from random import randrange
from llia.synths.xover.xover_data import xover
from llia.util.lmath import *

def pick_lfo_frequency():
    rng = coin(0.90, coin(0.75, 'slow', 'medium'), 'fast')
    print("# xover LFO range: %s" % rng)
    if rng == 'slow':
        return rnd()
    elif rng == 'medium':
        return 1 + rnd(6)
    else:
        return coin(0.75, rnd(30), rnd(400))

def pick_crossover():
    return pick([100, 200, 400, 800, 1600, 4000, 8000, 12500])

def pick_lfo_crossover():
    return coin(0.50, 0, rnd())

def pick_lfo_crossover_ratio():
    return coin(0.50, 1, pick([0.25, 0.5, 0.75, 1.333, 1.5, 2, 3, 4, 5]))

def pick_res():
    return rnd()

def pick_lp_mode():
    return coin(0.75, 1.0, rnd())

def pick_lp_mod():
    return coin(0.75, 1.0, rnd())

def pick_lp_amp():
    return coin(0.80, 0, pick([-6, -12, -18, -36, -99]))

def pick_hp_mode():
    return coin(0.75, 1.0, rnd())

def pick_hp_mod():
    return coin(0.75, 1.0, rnd())

def pick_hp_amp():
    return coin(0.80, 0, pick([-6, -12, -18, -36, -99]))

def pick_spread():
    return coin(0.5, 0, random_sign())

def pick_pan_mod():
    return coin(0.50, 0, rnd())

def pick_pan_mod_ratio():
    return coin(0.5, 1, pick([0.25, 0.5, 0.75, 1.333, 1.5, 2, 3, 4, 5]))

def pick_dry_amp():
    return coin(0.75, -99, pick([-36, -18, -9, -6, 0]))


def gen_xover_program(slot=127, *_):
    rs = xover(slot, "Random",
               lfoFreq = pick_lfo_frequency(),
               crossover = pick_crossover(),
               res = pick_res(),
               lfoCrossover = pick_lfo_crossover(),
               lfoCrossoverRatio = pick_lfo_crossover_ratio(),
               lpMode = pick_lp_mode(),
               lpMod = pick_lp_mod(),
               lpAmp = pick_lp_amp(),
               hpMode = pick_hp_mode(),
               hpMod = pick_hp_mod(),
               hpAmp = pick_hp_amp(),
               spread = pick_spread(),
               lfoPanMod = pick_pan_mod(),
               lfoPanRatio = pick_pan_mod_ratio(),
               dryAmp = pick_dry_amp(),
               dryPan = 0,
               amp = 0)
    return rs
        
    

    
