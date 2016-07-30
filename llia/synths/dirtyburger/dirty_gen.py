# llia/synths/dirtyburger/dirty_gen

from __future__ import print_function
from random import randrange

from llia.util.lmath import *
from llia.synths.dirtyburger.dirty_data import dirty


def dirty_gen(slot=127, *_):
    dtime = coin(0.75, rnd(0.5), 0.5+rnd())
    fb = coin(0.75,
              [[coin(0.5, rnd(0.5), 0.5+rnd(0.4))],1.0, 1.0],
              [rnd(0.75), coin(0.75, 1 + rnd(0.2)), 0.125+rnd(0.75)])
    lp = coin(0.75, 2000 + rnd(8000), 100+rnd(8000))
    hp = coin(0.75, 100, 100+rnd(2000))
    wow = [coin(0.75, 0, coin(0.25, rnd(), rnd(0.1))),
           coin(0.80, 0, coin(0.25, rnd(), rnd(0.1)))]
    p = dirty(slot, "Random",
              delayTime = dtime,
              feedback = fb,
              eq = [lp, hp],
              dry = [0, -0.5],
              wet = [pick((0, -3, -6, -9)), 0.5])
    return p
              
