# llia.synths.klstr2.klstr2_random

from __future__ import print_function
from llia.util.lmath import (coin,rnd,pick,random_sign)
from llia.synths.klstr2.klstr2_data import klstr2
from llia.synths.klstr2.klstr2_constants import *

# Envelope time ranges
ULTRA_FAST = 1
FAST = 2
MEDIUM = 3
SLOW = 4
GLACIAL = 5
FULL = 6

# Envelope contours
PERCUSSIVE=0
ADSR = 1
ASR = 2
GATE = 3

verbose = False

def pick_env_time_hint(is_percussive=False):
    if is_percussive:
        h = coin(0.74, SLOW, coin(0.67, MEDIUM, GLACIAL))
    else:
        h = coin(0.75,
                 pick((ULTRA_FAST,FAST,FAST, MEDIUM)),
                 pick((FAST,MEDIUM,SLOW,GLACIAL,FULL)))
    return h

def pick_env_segment_time(hint=FULL, p_changeup=0.1):
    hint = coin(p_changeup, pick_env_time_hint(),hint)
    mn,mx = 0, MAX_ENV_SEGMENT_TIME
    try:
        mn,mx = {ULTRA_FAST : (0.00, 0.05),
                 FAST : (0.00, 0.20),
                 MEDIUM : (0.10, 1.00),
                 SLOW : (1.0, 4.0),
                 GLACIAL : (4.0, MAX_ENV_SEGMENT_TIME)}[hint]
    except KeyError:
        pass
    return mn+rnd(mx-mn)

def pick_env_times(hint=None,p_changeup=0.1):
    hint = hint or pick_env_time_hint()
    acc = []
    for i in range(4):
        t = pick_env_segment_time(hint,p_changeup)
        acc.append(t)
    return tuple(acc)

def pick_env_type_hint(hint=None, p_changeup=1.0):
    hint = hint or coin(0.8,
                        coin(0.25, PERCUSSIVE,ADSR),
                        coin(0.67, ASR, GATE))
    if coin(p_changeup):
        return pick_env_type_hint(hint,0)
    return hint
        
def round_env_values(envlist):
    head = map(lambda x: round(x,4), envlist[:-1])
    head.append(envlist[-1])
    return head
    
def gate_envelope(*_):
    return [0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0]

def asr_envelope(time_hint):
    att,dcy1,dcy2,rel = pick_env_times(time_hint,0.0)
    bp = sus = 1.0
    return round_env_values([att,dcy1,dcy2,rel,bp,sus,0])

def adsr_envelope(time_hint):
    att,dcy1,dcy2,rel = pick_env_times(time_hint,0.0)
    sus = coin(0.75, 0.5+rnd(0.5),rnd())
    bp = coin(0.50, sus, sus+rnd(1-sus))
    return round_env_values([att,dcy1,dcy2,rel,bp,sus,0])

def percussive_envelope(time_hint):
    if time_hint < MEDIUM:
        time_hint = pick_env_time_hint(True)
    junk,dcy1,dcy2,rel = pick_env_times(time_hint,0.0)
    att = coin(0.80, 0.00, rnd(0.01))
    dcy1,dcy2 = min(dcy1,dcy2),max(dcy1,dcy2)
    while dcy1 > 1:
        dcy1 = dcy1-1
    if dcy2 < 0.5:
        dcy2 = coin(0.25, dcy2, pick([dcy1*2,dcy1*3,dcy1*4]))
    bp = coin(0.50,rnd(0.75),0.75)
    sus = coin(0.90,0.0,rnd(0.12))
    return round_env_values([att,dcy1,dcy2,rel,bp,sus,0])

def pick_envelope(time_hint, mode_hint, p_changeup=0.1):
    mode_hint = coin(p_changeup, pick_env_type_hint(mode_hint,p_changeup))
    if mode_hint == PERCUSSIVE:
        elst = percussive_envelope(time_hint)
    elif mode_hint == ASR:
        elst = asr_envelope(time_hint)
    elif mode_hint == GATE:
        elst = gate_envelope()
    else:
        elst = adsr_envelope(time_hint)
    return {"attack" : elst[0],
            "decay1" : elst[1],
            "decay2" : elst[2],
            "release" : elst[3],
            "breakpoint" : elst[4],
            "sustain" : elst[5],
            "mode" : 0}
        
def pick_lfo_freq():
    return coin(0.75, rnd(), coin(0.90, rnd(7), rnd(99)))

def pick_lfo_ratio(freq):
    if freq <= 1:
        return pick(LFO_RATIOS)
    else:
        return coin(0.90, pick(LFO_RATIOS[:16]), pick(LFO_RATIOS))
                    
def pick_harmonic_envmod(n):
    if coin(0.60):
        return 0
    else:
        if n > 12:
            psign = 0.75
        else:
            psign = 0.25
    return random_sign(psign)*pick(HARMONICS)

def pick_harmonic_lfomod(n):
    if coin(0.60):
        return 0
    else:
        return pick(HARMONICS)

def pick_noise_mod(nfreq):
    if coin(0.25):
        if nfreq > 4000:
            psign = 0.75
        else:
            psign = 0.25
        return random_sign(psign)*pick(FILTER_FREQUENCIES)
    else:
        return 0

def pick_filter_mod(ff):
    if coin(0.25):
        if ff > 4000:
            psign = 0.75
        else:
            psign = 0.25
        return random_sign(psign)*pick(FILTER_FREQUENCIES)
    else:
        return 0
    
    
def klstr2_random(slot, *_):
    em_hint = pick_env_type_hint()
    et_hint = pick_env_time_hint(em_hint==PERCUSSIVE)
    lfo_freq = pick_lfo_freq()
    pw = coin(0.75, 0.5, rnd())
    h1 = pick(HARMONICS)
    h2 = pick(HARMONICS)
    noise_lowpass = pick(FILTER_FREQUENCIES)
    f1 = pick(FILTER_FREQUENCIES)
    f2 = pick(FILTER_FREQUENCIES)
    p = klstr2(slot,"Random",amp=0.2,
               lfo = {"freq" : lfo_freq,
                      "ratio2" : pick_lfo_ratio(lfo_freq),
                      "vibrtao" : coin(0.75, 0, coin(0.90, rnd(0.1), rnd()))},
               env1 = pick_envelope(et_hint,em_hint),
               env2 = pick_envelope(et_hint,em_hint),
               spread = {"n" : coin(0.60, rnd(0.1), rnd()),
                         "env1" : coin(0.05, rnd(), 0),
                         "lfo1" : coin(0.05, rnd(), 0),
                         "external" : 0},
               cluster = {"n" :rnd(),
                          "env1" : coin(0.50, rnd(), 0.0),
                          "lfo1" : coin(0.08, rnd(), 0.0),
                          "lfo2" : coin(0.08, rnd(), 0.0),
                          "external" : 0},
               pw = {"pw" : coin(0.75, 0.5, rnd()),
                     "env1" : coin(0.20, rnd(), 0.0),
                     "lfo1" : coin(0.20, rnd(), 0.0)},
               harm1 = {"n" : h1,
                        "env1" : pick_harmonic_envmod(h1),
                        "env2" : pick_harmonic_envmod(h1),
                        "lfo1" : pick_harmonic_lfomod(h1),
                        "lfo2" : pick_harmonic_lfomod(h1)},
               harm2 = {"n" : h2,
                        "env1" : pick_harmonic_envmod(h2),
                        "lfo1" : pick_harmonic_lfomod(h2),
                        "external" : 0,
                        "lag" : coin(0.25, rnd(), 0.0)},
               noise_filter = {"highpass" : coin(0.75,
                                                 FILTER_FREQUENCIES[0],
                                                 pick(FILTER_FREQUENCIES)),
                               "lowpass" : noise_lowpass,
                               "env1" : pick_noise_mod(noise_lowpass),
                               "lfo1" : pick_noise_mod(noise_lowpass)},
               mixer = {"noise" : coin(0.20, rnd(2), 0.0),
                        "balnace_a" : random_sign()*rnd(),
                        "balance_b" : random_sign()*rnd(),
                        "balnce_noise" : random_sign()*rnd(),
                        "out2_lag" : coin(0.01, 0, rnd())},
               filter_1 = {"freq" : f1,
                           "env1" : pick_filter_mod(f1),
                           "lfo1" : pick_filter_mod(f1),
                           "lfo2" : pick_filter_mod(f1),
                           "external" : 0,
                           "res" : coin(0.75, rnd(0.5), rnd()),
                           "mix" : coin(0.75, 0.5+rnd(1.5), rnd()),
                           "pan" : -0.75},
               filter_2 = {"freq" : f2,
                           "env1" : pick_filter_mod(f2),
                           "env2" : pick_filter_mod(f2),
                           "lfo1" : pick_filter_mod(f2),
                           "lag"  : coin(0.25, rnd(), 0.0),
                           "res" : coin(0.75, rnd(0.5), rnd()),
                           "mix" : coin(0.75, 0.5+rnd(1.5), rnd()),
                           "pan" : 0.75})
    return p
                               
                               
                                                 
               
                          
               
    
    
