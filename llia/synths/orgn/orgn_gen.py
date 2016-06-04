# llia.synths.organ.orgn_gen
# 2016.06.04

from __future__ import print_function
from random import randrange


from llia.synths.orgn.orgn_data import orgn
from llia.util.lmath import *

def pick_lfo_frequency():
    return float(coin(0.75, randrange(5,8), randrange(1,11)))

def pick_lfo_delay():
    return float(coin(0.75, rnd(3.0), 0.0))

def pick_vibrato_sensitivity():
    return float(coin(0.90, rnd(0.3), rnd()))

def pick_vibrato_depth():
    return float(coin(0.5, rnd(), 0))

def pick_chorus_depth():
    return float(coin(0.5, rnd(), 0))

def pick_chorus_delay():
    return float(coin(0.5, rnd(4), 0))

def pick_stack_amps():
    a = randrange(-36, 0, 3)
    b = randrange(-36, 0, 3)
    mx = max(a,b)
    scale = abs(mx)
    a += scale
    b += scale
    c = coin(0.5, randrange(-36, -6, 3), randrange(-18, -6, 3))
    return (a,b,c)

def pick_stack_a(amp, *_):
    c = 0.5
    m = coin(0.75, 0.5, pick([0.25, 1.0]))
    depth = rnd()
    return [c, m, depth, amp]

def pick_stack_b(amp, dt_range):
    c = approx(coin(0.75, 1.0, 2.0), dt_range)
    m = approx(coin(0.75, 1.0, pick([0.5, 2.0])), dt_range)
    depth = rnd()
    return [c, m, depth, amp]
             
def pick_stack_c(amp, dt_range):
    c = approx(coin(0.75, 3.0, pick([1.5, 2.0])), dt_range)
    m = approx(pick([1.0, 1.5, 2.0, 3.0]), dt_range)
    depth = rnd()
    return [c, m, depth, amp]

def pick_adsr():
    return coin(0.50,
                [0.0, 1.0, 1.0, 0.0],
                coin(0.75,
                     [0.0, rnd(), rnd(), rnd()],
                     [rnd(2.0), rnd(2.0), rnd(), rnd(2.0)]))
                     
def pick_brightness():
    return coin(0.9, 1.0, rnd())

def gen_orgn_program(slot=127, *_):
    aamp, bamp, camp = pick_stack_amps()
    dt_range = coin(0.75, 0.0, coin(0.75, 0.01, 0.1))
    rs = orgn(slot, "Random", amp=-18,
              vfreq = pick_lfo_frequency(),
              vdelay = pick_lfo_delay(),
              vsens = pick_vibrato_sensitivity(),
              vdepth = pick_vibrato_depth(),
              chorus = [pick_chorus_depth(), pick_chorus_delay()],
              a = pick_stack_a(aamp),
              b = pick_stack_b(bamp, dt_range),
              c = pick_stack_c(camp, dt_range),
              adsr = pick_adsr(),
              brightness = pick_brightness())
    return rs
         
         
         
         
