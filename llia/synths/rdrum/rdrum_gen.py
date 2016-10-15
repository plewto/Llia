# llia.synths.rdrum.rdrum_gen

from __future__ import print_function
from random import randrange

from llia.synths.rdrum.rdrum_data import rdrum
from llia.util.lmath import *

def pick_ratios():
    a = pick([0.5, 0.5, 1.0, 1.0, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0])
    b = pick([1.0, 1.0, 1.0, 2.0, 3.0, 4.0, 6.0])
    nse = float(coin(0.75, pick([1, 2, 3, 4, 4, 5, 6, 6, 8]), 0))
    if nse:
        nsebias = 0
    else:
        nsebias = 100+rnd(9100)
    return (a,b,nse,int(nsebias))

def pick_attacks():
    a = coin(0.80, rnd(0.01), rnd(6))
    b = coin(0.80, rnd(0.01), rnd(6))
    nse = coin(0.70, rnd(0.1), rnd(6))
    return (a,b,nse)

pick_decays = pick_attacks

def pick_mix():
    a = coin(0.75, 0, pick([-3, -6, -9]))
    b = coin(0.75, pick([-3, -3, -6, -9]), 0)
    nse = coin(0.5, -99, pick([9, -3, -6, -9, -12, -15, -18]))
    return (a,b,nse)

def pick_bend():
    a = coin(0.85, 0, random_sign())
    b = coin(0.85, a, random_sign())
    nse = coin(0.85, 1, random_sign())
    return (a,b,nse)

def pick_velocity():
    return coin(0.75, (0,0, 0,0, 0,0), (rnd(),rnd(),rnd()))

def gen_rdrum_program(slot=127, *_):
    ar, br, nr, nbias  = pick_ratios()
    aa, ba, na = pick_attacks()
    ad, bd, nd = pick_decays()
    abnd, bbnd, nbnd = pick_bend()
    avel, bvel, nvel = pick_velocity()
    aamp, bamp, namp = pick_mix()
    
    rs = rdrum(slot, "Random", amp=-3,
               a = {"ratio" : ar,
                    "attack" : aa,
                    "decay" : ad,
                    "bend" : abnd,
                    "amp" : aamp,
                    "tone" : coin(0.5, 0, rnd())},
                b = {"ratio" : br,
                     "attack" : ba,
                     "decay" : bd,
                     "bend" : bbnd,
                     "amp" : bamp,
                     "tune" : coin(0.75, 0, rnd(4))},
               noise = {"ratio" : nr,
                        "bias" : nbias,
                        "attack" : na,
                        "decay" : nd,
                        "bend" : nbnd,
                        "amp" : namp,
                        "res" : rnd()})
    return rs

               
               
    
