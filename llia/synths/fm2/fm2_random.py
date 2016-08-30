# llia.synths.fm2.fm2_random

from __future__ import print_function

from llia.synths.fm2.fm2_data import fm2
from llia.util.lmath import *

def get_env_hint():
    return pick(["PERCUSSION", "ADDSR"])

def get_envtime_hint():
    return pick([0.25, 1, 1, 1, 1, 1, 4, 8])

def env_segment_time(hint):
    hint = coin(0.75, hint, get_envtime_hint())
    return rnd(hint)

def percussion_envelope(time_hint):
    a = env_segment_time(0.05)
    d1 = env_segment_time(time_hint*0.5)
    d2 = env_segment_time(time_hint)
    r = env_segment_time(time_hint)
    bp = coin(0.75, 0.9+rnd(0.1), 0.5+rnd(0.5))
    s = coin(0.75, min(0.5+rnd(0.5), bp), rnd(0.25))
    hold = True
    return a,d1,d2,r,bp,s,hold

def addsr_envelope(time_hint):
    a = env_segment_time(time_hint)
    d1 = env_segment_time(time_hint)
    d2 = env_segment_time(time_hint)
    r = env_segment_time(time_hint)
    bp = coin(0.75, 0.9+rnd(0.1), 0.5+rnd(0.5))
    s = coin(0.50, rnd(bp), rnd())
    hold = False  # coin(0.75, False, True)
    return a,d1,d2,r,bp,s,hold

# def get_envelope(time_hint, shape_hint):
#     if shape_hint == "PERCUSION":
#         p = 0.75
#     else:
#         p = 0.25
#     e = coin(p, percussion_envelope(time_hint), addsr_envelope(time_hint))
#     return e


def get_envelope(time_hint, shape_hint):
    return addsr_envelope(time_hint)


def fm2_random(slot=127, *_):
    time_hint = get_envtime_hint()
    env_hint = get_env_hint()
    env1 = get_envelope(time_hint, env_hint)
    env2 = get_envelope(time_hint, env_hint)
    op1_chorus = coin(1)
    op1_ratio = float(pick([0.5, 0.5, 0.75,
                           1,1,1,1,1.5,
                           2,2,2,2,2.25,
                           3,3,3,4,4,4,5,5,
                           6,6,7,8,9,10,12,16]))
    op2_ratio = coin(0.75, pick([0.5,0.5,0.75,
                                 1,1,1,1,1,1.5,
                                 2,2,2,2,2,2.25,
                                 3,3,3,4,4,4,5,
                                 6,6,7,8,9,10,12,16]),
                     coin(0.75, 1+rnd(4), rnd(8)))
    op2_bias = coin(0.50, 0, coin(0.75, rnd(3), rnd(100)))
    if op2_bias == 0:
        if coin(0.5):
            op2_ratio = approx(op2_ratio)
    op2_amp = coin(10)
    op2_amp_range = coin(0.8, 1, pick([10,10,10,100,1000]))
    if op1_chorus:
        op1_ratio = 0
        op1_bias = rnd(3)
        op2_amp = 0.5 * rnd(0.5)
        op2_amp_range = pick([1000,10000])
    else:
        op1_bias = 0

    
    p = fm2(slot, "Random", amp=-12,
            port = coin(0.75, 0.0, rnd()),
            external = {"scale" : 1, "bias" : 0, "pitch" : 0, "mod" : 0},
            lfo = {"freq" : coin(0.75, 4+rnd(3),
                                 coin(0.5, rnd(), rnd(100))),
                   "delay" : rnd(4),
                   "vsens" : coin(0.80, 0.1, rnd()),
                   "vdepth" : coin(0.30, 0, coin(0.75, rnd(0.4), rnd()))},
            op1 = {"enable" : True,
                   "ratio" : op1_ratio,
                   "bias" : op1_bias,
                   "amp" : 0,
                   "attack" : env1[0],
                   "decay1" : env1[1],
                   "decay2" : env1[2],
                   "release" : env1[3],
                   "breakpoint" : env1[4],
                   "sustain" : env1[5],
                   "env-cycle" : env1[6],
                   "velocity" : coin(0.75, 0, rnd()),
                   "lfo" : coin(0.75, 0, rnd())
                   },
            op2 = {"enable" : True,
                   "ratio" : op2_ratio,
                   "bias" : op2_bias,
                   "amp" : 5, # op2_amp,
                   "modRange" : op2_amp_range,
                   "attack" : env2[0],
                   "decay1" : env2[1],
                   "decay2" : env2[2],
                   "release" : env2[3],
                   "breakpoint" : env2[4],
                   "sustain" : env2[5],
                   "env-cycle" : env2[6],
                   "velocity" : coin(0.75, 0, rnd()),
                   "lfo" : coin(0.75, 0, rnd()),
                   "feedback" : coin(0.50, 0, coin(0.75, rnd(2), rnd(4)))
                   })
    return p
            
            
        
