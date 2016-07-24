# llia.synths.klstr.klstr_gen

from __future__ import print_function
from random import randrange

from llia.synths.klstr.klstr_data import klstr
from llia.util.lmath import *


def pick_lfo():
    freq = coin(0.75, rnd()+0.001, coin(0.75, rnd(10), rnd(100)))
    ratio = float(coin(0.50, 1, pick([0.01, 0.1, 0.25, 0.333, 0.5, 0.667,
                                     0.75, 1.125, 1.25, 1.5, 1.75,
                                      2, 3, 4, 5, 8])))
    xmod = coin(0.75, 0, rnd(4))
    delay = coin(0.5, 0, rnd(4))
    depth = coin(0.5, 1, rnd())
    vibrato = coin(0.90, 0, rnd())
    rs =  {"freq" : freq,
           "ratio" : ratio,
           "xmod" : xmod,
           "delay" : delay,
           "depth" : depth,
           "vibrato" : vibrato}
    return rs

def pick_percussive_envelope():
    attack = coin(0.90, 0.00, rnd(0.05))
    decay = coin(0.50, rnd(0.1), rnd(1))
    release = coin(0.5, rnd(1), rnd(16))
    sustain = coin(0.5, 0.5+rnd(0.5), rnd())
    rs = {"gated" : True,
          "attack" : attack,
          "decay" : decay,
          "sustain" : sustain,
          "release" : release}
    return rs
                  

def pick_gated_env():
    erange = pick([0.1, 1.0, 2.0, 4.0])
    attack = float(coin(0.75, rnd(erange), rnd(8.0-erange)))
    decay = float(coin(0.75, rnd(erange), rnd(8.0-erange)))
    release = float(coin(0.75, rnd(erange), rnd(8.0-erange)))
    sustain = coin(0.75, 0.75+rnd(0.25), rnd())
    gatted = False
    rs =  {"gated" : gatted,
           "attack" : attack,
           "decay" : decay,
           "sustain" : sustain,
           "release" : release}
    return rs

def pick_env():
    return pick_percussive_envelope()

def pick_spread():
    depth = coin(0.5, rnd(0.01), rnd(4))
    lfo = coin(0.75, 0.0, rnd())
    env = coin(0.75, 0.0, rnd())
    rs = {"depth" : depth,
          "lfo" : lfo,
          "env" : env}
    return rs
          
def pick_cluster():
    depth = coin(0.75, rnd(), rnd(16))
    lfo = coin(0.5, 0, coin(0.75, rnd(), rnd(16)))
    env = coin(0.5, 0, coin(0.75, rnd(), rnd(16)))
    if depth >= 2:
        env = random_sign(0.5, env)
    lag = coin(0.50, 0, rnd())
    rs = {"depth" : depth,
          "lfo" : lfo,
          "env" : env,
          "lag" : lag}
    return rs

def pick_filter():
    freq = randrange(100, 9999)
    lfo = coin(0.5, 0, coin(0.5, rnd(1000), rnd(5000)))
    env = coin(0.5, 0, rnd(7000))
    if freq > 5000:
        env = random_sign(0.5, env)
    lag = coin(0.5, 0, rnd())
    res = coin(0.75, rnd(0.5), rnd)
    mix = coin(0.10, 0, coin(0.5, 1, 0.5+rnd(0.5)))
    rs = {"freq" : int(freq),
          "lfo" : int(lfo),
          "env" : int(env),
          "lag" : float(lag),
          "res" : float(res),
          "mix" : float(mix)}
    return rs
          
    


def gen_klstr_program(slot=127, *_):
    rs = klstr(slot, "Random", amp=-12,
               lfo = pick_lfo(),
               env = pick_env(),
               spread = pick_spread(),
               cluster = pick_cluster(),
               filter_ = pick_filter(),
               pw = coin(0.80, 0.5, rnd()),
               pwLfo = coin(0.75, 0, rnd()),
               noise = coin(0.80, -99, pick([0, -6, -9, -12])))
    return rs
        
