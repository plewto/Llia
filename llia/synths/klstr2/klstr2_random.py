# llia.synths.klstr2.klstr2_random

from __future__ import print_function
from llia.util.lmath import (coin,rnd,pick,random_sign)
from llia.synths.klstr2.klstr2_data import klstr2
from llia.synths.klstr2.klstr2_constants import *


def env_time_hint():
    return pick(("slow","norm","norm","fast","fast"))

def pick_env_segment_time(hint, p_change=0.2):
    if coin(p_change):
        hint = env_time_hint()
    if hint == "slow":
        return coin(0.75, rnd(4),rnd(MAX_ENV_SEGMENT_TIME))
    elif hint == "norm":
        return coin(0.75, rnd(1), coin(0.75, rnd(2), rnd(4)))
    else:
        return coin(0.75, rnd(0.2), rnd())

def env_shape_hint():
    return pick(("gate","adsr","adsr","perc","perc"))

def pick_env_levels(hint, p_change=0.2):
    if coin(p_change):
        hint = env_shape_hint()
    if hint == "gate":
        bp = 1.0
        sus = 1.0
    elif hint == "adsr":
        bp = 0.75+rnd(0.25)
        sus = 0.75+rnd(0.25)
    else:
        #return coin(0.75, 0.5+rnd(0.5), rnd())
        bp = coin(0.75, 0.5+rnd(), rnd())
        sus = coin(0.75, rnd(25), 0.0)
    return bp,sus


def klstr2_random(slot,*_):
    return None
    
# def klstr2_random(slot,*_):

#     lfo = {"freq" : coin(0.75, rnd(1), coin(0.75, rnd(7),rnd(100))),
#            "ratio2" : pick(LFO_RATIOS),
#            "vibrato" : coin(0.75, 0, rnd(1))}

#     etime_hint = env_time_hint()
#     eshape_hint = env_shape_hint()
#     bp,sus = pick_env_levels(eshape_hint)
#     trig_mode = coin(0.1, 1, 0)
#     env1 = {"attack" : pick_env_segment_time(etime_hint),
#             "decay1" : pick_env_segment_time(etime_hint),
#             "decay2" : pick_env_segment_time(etime_hint),
#             "release" : pick_env_segment_time(etime_hint),
#             "breakpoint" : bp,
#             "sustain" : sus,
#             "mode": trig_mode}
#     bp,sus = pick_env_levels(eshape_hint)
#     env2 = {"attack" : pick_env_segment_time(etime_hint),
#             "decay1" : pick_env_segment_time(etime_hint),
#             "decay2" : pick_env_segment_time(etime_hint),
#             "release" : pick_env_segment_time(etime_hint),
#             "breakpoint" : bp,
#             "sustain" : sus,
#             "mode": trig_mode}

#     f1 = pick(FILTER_FREQUENCIES)
#     if f1 > 4000:
#         p_neg_f1_mod = 0.80
#     else:
#         p_neg_f1_mod = 0.05
#     f2 = pick(FILTER_FREQUENCIES)
#     if f2 > 4000:
#         p_neg_f2_mod = 0.80
#     else:
#         p_neg_f2_mod = 0.05
    
#     p = klstr2(slot, "Random", amp=0.1,
#                lfo = lfo,
#                env1 = env1,
#                env2 = env2,
#                spread = {"n" : coin(0.50, rnd(0.1), rnd()),
#                          "env1" : coin(0.05, rnd(), 0.0),
#                          "lfo1" : coin(0.05, rnd(), 0.0),
#                          "external" : 0.0},
#                cluster = {"n" : rnd(),
#                           "env1" : coin(0.2, rnd(), 0.0),
#                           "lfo1" : coin(0.05, rnd(), 0.0),
#                           "lfo2" : coin(0.05, rnd(), 0.0),
#                           "external" : 0.0},
#                pw = {"pw" : coin(0.5, 0.5, rnd()),
#                      "lfo1" : coin(0.15, rnd(), 0.0),
#                      "env1" : coin(0.15, rnd(), 0.0)},
#                # harm1 = {"n" : pick(HARMONICS),
#                #          "env1" : coin(0.07, pick(range(-24,24)), 0),
#                #          "env2" : coin(0.07, pick(range(-24,24)), 0),
#                #          "lfo1" : coin(0.03, pick(range(1,24)), 0),
#                #          "lfo2" : coin(0.03, pick(range(1,24)), 0)},
#                # harm2 = {"n" : pick(HARMONICS),
#                #          "env1" : coin(0.07, pick(range(-24,24)), 0),
#                #          "lfo1" : coin(0.03, pick(range(1,24)), 0),
#                #          "external" : 0,
#                #          "lag" : coin(0.5, rnd(), 0.0)},

#                harm1 = {"n" : pick(HARMONICS),
#                         "env1" : coin(0.75, 0, pick(POLAR_HARMONIC_MOD_RANGE)),
#                         "env2" : coin(0.75, 0, pick(POLAR_HARMONIC_MOD_RANGE)),
#                         "lfo1" : coin(0.75, 0, pick(HARMONIC_MOD_RANGE)),
#                         "lfo2" : coin(0.75, 0, pick(HARMONIC_MOD_RANGE))},

#                harm2 = {"n" : pick(HARMONICS),
#                         "env1" : coin(0.75, 0, pick(POLAR_HARMONIC_MOD_RANGE)),
#                         "lfo1" : coin(0.75, 0, pick(HARMONIC_MOD_RANGE)),
#                         "external" : 0,
#                         "lag" : coin(0.5, rnd(), 0.0)},
               
#                noise_filter = {"lowpass" : pick(NOISE_LOWPASS_FREQUENCIES),
#                                "env1" : random_sign()*coin(0.75, 0.0,pick(NOISE_LOWPASS_FREQUENCIES)),
#                                "lfo1" : coin(0.75, 0.0,pick(NOISE_LOWPASS_FREQUENCIES)),
#                                "highpass" : coin(0.75, 67, pick(NOISE_HIGHPASS_FREQUENCIES))},
#                mixer = {"noise" : coin(0.80, 0.0, rnd(2)),
#                         "balance_a" : random_sign(0.75)*rnd(),
#                         "balance_b" : random_sign(0.25)*rnd(),
#                         "balnace_noise" : random_sign()*rnd()},
#                filter_1 = {"freq" : f1,
#                            "env1" : random_sign(1-p_neg_f1_mod)*coin(0.75, pick(FILTER_FREQUENCIES), 0),
#                            "lfo1" : coin(0.07, pick(FILTER_FREQUENCIES)),
#                            "lfo2" : coin(0.07, pick(FILTER_FREQUENCIES)),
#                            "external" : 0,
#                            "res" : coin(0.5, rnd(0.5), coin(0.75, 0.5+rnd(0.3), 0.8+rnd(0.2))),
#                            "mix" : coin(0.75, 1.0, rnd()),
#                            "pan" : coin(0.75, 0.75, random_sign()*rnd())},
#                filter_2 = {"freq" : f2,
#                            "env1" : random_sign(1-p_neg_f2_mod)*coin(0.75, pick(FILTER_FREQUENCIES), 0),
#                            "lfo1" : coin(0.07, pick(FILTER_FREQUENCIES)),
#                            "lfo2" : coin(0.07, pick(FILTER_FREQUENCIES)),
#                            "lag"  : coin(0.5, 0.0, rnd()),
#                            "res" : coin(0.5, rnd(0.5), coin(0.75, 0.5+rnd(0.3), 0.8+rnd(0.2))),
#                            "mix" : coin(0.75, 1.0, rnd()),
#                            "pan" : coin(0.75, 0.75, random_sign()*rnd())})
#     return p
