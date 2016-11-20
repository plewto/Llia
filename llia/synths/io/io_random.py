# llia.synths.io.io_random

from __future__ import print_function
from llia.util.lmath import (coin,rnd,pick)
from llia.synths.io.io_data import (io,vibrato,blip,noise,chiff,
                                    modulator,carrier)
from llia.synths.io.io_constants import *


def env_hint():
    typ = pick(["adsr","asr","perc"])
    tm = pick(["fast","medium","slow"])
    return typ,tm

p_env_changeup = 0.2

def envelopes():
    type_hint, time_hint = env_hint()
    acc = []
    def pick_time(hint):
        if hint == "fast":
            return rnd(0.1)
        elif hint == "medium":
            return coin(0.75, rnd(0.2), rnd(0.5))
        else:
            return 0.5+coin(0.75, rnd(2), rnd(6))
    for op in (1,2,3):
        typ = coin(p_env_changeup, pick(["adsr","asr","perc"]), type_hint)
        tm = coin(p_env_changeup, pick(["fast","medium","slow"]), time_hint)
        
        att = pick_time(tm)
        dcy = pick_time(tm)
        rel = pick_time(tm)
        sus = coin(0.5, 0.5+rnd(0.5), rnd())
        if typ == "asr":
            sus = 1.0
        elif typ == "perc":
            sus = coin(0.75, 0.0, rnd(0.1))
            dcy /= 2
            rel *= 2
        acc.append((att,dcy,sus,rel))
    return acc


def trem_ratio():
    r = coin(0.75, (1.0, ""), pick(TREMOLO_RATIOS))
    return r[0]

def cformants():
    f1 = int(100+rnd(500))
    f2 = int(f1+100+rnd(500))
    f3 = int(f2+100+rnd(1500))
    return f1,f2,f3

def cratios():
    harmonic = (1,1,1,1,1,1,1,1,
                2,2,2,2,2,2,2,2,
                3,3,3,4,4,5,6,8)
    acc = []
    for i in range(3):
        acc.append(coin(0.80, pick(harmonic), rnd(8)))
    return tuple(acc)


def car(op, ff, ratios, envs, amp):
    env = envs[op-1]
    mode = coin(0.50, 0, 1)
    modDepth = coin(0.75, rnd(4), rnd(8))
    if mode: modDepth /= 2.0
    rs = carrier(op,
                   formant =  ff[op-1],
                   ratio = ratios[op-1],
                   mode = mode,
                   velocity = coin(0.75, rnd(), 0),
                   tremolo = coin(0.75, 0, coin(0.75, rnd(0.3), rnd())),
                   modDepth = modDepth,
                   attack = env[0],
                   decay = env[1],
                   sustain = env[2],
                   release = env[3],
                   lag = coin(0.5, 0, rnd()),
                   key = 60,
                   leftScale = 0,
                   rightScale = 0,
                   x = 0.0,
                   amp = amp)
    return rs
            
def io_random(slot, *_):
    envs = envelopes()
    amps = []
    for i in (1,2,3):
        amps.append(coin(0.75, 0.5+rnd(),rnd()))
    amps[pick((0,1,2))] = 1.0
    ff = cformants()
    rr = cratios()
    p = io(slot,"Random",
           amp = 0.1,
           vibrato = vibrato(freq = coin(0.75,4+rnd(4),rnd(16)),
                             lock = coin(0.75, 1, 0),
                             noise = coin(0.5, 0.0, rnd()),
                             sens = coin(0.80, rnd(0.1),rnd()),
                             depth = coin(0.25, 0, coin(0.75, rnd(0.3), rnd())),
                             x = 0.0,
                             tremRatio = trem_ratio()),
           blip = blip(attack = coin(0.75, rnd(0.1),rnd(MAX_BLIP_SEGMENT_TIME)),
                       decay = coin(0.75, 0.1+rnd(0.2), rnd(MAX_BLIP_SEGMENT_TIME)),
                       depth = coin(0.75, 0.0, coin(0.75, rnd(0.2), rnd()))),
           noise = noise(ratio = coin(0.75, 1.0, pick(NOISE_RATIOS)),
                         amp = coin(0.75, rnd(0.4), rnd())),
           modulator = modulator(ratio = pick((1,1,1,1,2,2,2,2,3,4)),
                                 feedback = coin(0.5, 0.0, coin(0.75, rnd(2), rnd(4))),
                                 lfo = coin(0.75, 0.0, coin(0.75, rnd(0.2), rnd()))),
           op1 = car(1,ff,rr,envs,amps[0]),
           op2 = car(2,ff,rr,envs,amps[1]),
           op3 = car(3,ff,rr,envs,amps[2]))
    return p
    
