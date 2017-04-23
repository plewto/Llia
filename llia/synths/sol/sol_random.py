# llia.synths.sol.sol_random

from __future__ import print_function
from llia.util.lmath import (coin,rnd,pick,approx,random_sign)
from llia.synths.sol.sol_data import (sol,vibrato,vector,lfo,adsr,addsr,
                                      fmop,wvop,filter)
from llia.synths.sol.sol_constants import *

def rsign(n):
    return random_sign(0.5,n)

ULTRA_FAST = 0
FAST = 1
MEDIUM = 2
SLOW = 3
GLACIAL = 4

def pick_env_time_hint():
    return coin(0.75,
                pick([ULTRA_FAST,FAST,MEDIUM]),
                coin(0.75,SLOW,GLACIAL))

def pick_env_segment_time(time_hint):
    if time_hint == ULTRA_FAST:
        rs = coin(0.75, 0.0, rnd(0.03))
    elif time_hint == FAST:
        rs = rnd(0.1)
    elif time_hint == MEDIUM:
        rs = 0.1+rnd(0.5)
    elif time_hint == SLOW:
        rs = 0.5+rnd(6)
    else:
        rs = 4+rnd(MAX_ENV_SEGMENT_TIME-4)
    if coin(0.1):
        rs = pick_env_segment_time(pick_env_time_hint())
    return rs

def adsr_list(time_hint):
    return [pick_env_segment_time(time_hint),
            pick_env_segment_time(time_hint),
            coin(0.75, 0.3+rnd(0.7), rnd()),
            pick_env_segment_time(time_hint)]

HARMONICS = (1,1,2,2,3,4)
HARMONICS2 = (0.5,1.5,5,6,8)

def pick_fm_modulation_ratio(is_harmonic):
    if is_harmonic:
        rs = coin(0.75,
                  pick(HARMONICS),
                  pick(HARMONICS2))
    else:
        rs = coin(0.75, 0.5+rnd(5), rnd(12))
    return rs

# def pick_fm_carrier(is_harmonic,is_lowfreq):
#     if is_lowfreq:
#         r = 0.001
#         b = pick([0.1,0.01])
#     else:
#         if is_harmonic:
#             r = coin(0.75,
#                      pick(HARMONICS),
#                      pick(HARMONICS2)),
#             b = coin(0.75, 0, rnd(2))    # Random chorus
#         else:
#             r = 0.5+rnd(8)
#             b = coin(0.75, 0, rnd(100))
#     return r,b

def pick_fm_carrier_ratio(is_harmonic):
    r = pick_fm_modulation_ratio(is_harmonic)
    return coin(0.75,r, approx(r, 0.005))

def pick_saw_ratio(is_harmonic):
    if is_harmonic:
        rs = coin(0.75,pick(HARMONICS),pick(HARMONICS2))
    else:
        rs = 0.5+rnd(8)
    return rs


pick_pulse_ratio = pick_saw_ratio

def pick_lfo_ratio():
    return float(pick(LFO_RATIOS))

def pick_filter(id):
    floor,ceiling = 100,16000
    ff = int(floor+rnd(ceiling-floor))
    trk = coin(0.75,0,pick((0.5,1,2)))
    head = ceiling-ff
    r = rnd()
    if r<0.25:
        env = cenv = 0
    elif r<0.50:
        env = int(rnd(head))
        cenv = 0
    elif r<0.75:
        cenv=int(rnd(head))
        env=int(rnd(head-cenv))
    else:
        env=0
        cenv=int(rnd(head))
    if ff > 6000:
        env = coin(0.8,-1,1)*env
        cenv = coin(0.8,-1,1)*cenv
    if cenv==0 and env==0:
        plfo = 0.5
    else:
        plfo = 0.1
    lfo = coin(plfo, int(head), 0)
    vlfo = coin(0.05,int(head),0)
    return filter(id,freq=ff,track=trk,
                  env=env,cenv=cenv,lfo=lfo,vlfo=vlfo,
                  res=rnd())
    
    

def sol_random(slot,*_):
    is_harmonic = coin(0.75)
    env_time_hint = pick_env_time_hint()

    p = sol(slot,"Random",amp=0.3,
            port=coin(0.80, 0, rnd()),
            timebase=4+rnd(4),
            vibrato=vibrato(ratio=coin(0.75,1,pick_lfo_ratio()),
                            sens=coin(0.75, 0.1, coin(0.75, 0, rnd())),
                            depth=coin(0.75,0,rnd()),
                            delay=rnd(MAX_LFO_DELAY),
                            extern=0),
            x=vector("x",pos=coin(0.75,0,rsign(rnd())),
                     ratio=pick_lfo_ratio(),
                     wave=coin(0.75, 0.5, rnd()),
                     delay=coin(0.75, 0, rnd(MAX_LFO_DELAY)),
                     adsr=adsr_list(env_time_hint),
                     trig=coin(0.2),
                     lfo_depth=coin(0.75,rsign(rnd()),0),
                     env_depth=coin(0.25,rsign(rnd()),0),
                     external=0),
            y=vector("y",pos=coin(0.75,0,rsign(rnd())),
                     ratio=pick_lfo_ratio(),
                     wave=coin(0.75, 0.5, rnd()),
                     delay=coin(0.75, 0, rnd(MAX_LFO_DELAY)),
                     adsr=adsr_list(env_time_hint),
                     trig=coin(0.2),
                     lfo_depth=coin(0.75,rsign(rnd()),0),
                     env_depth=coin(0.25,rsign(rnd()),0),
                     external=0),
            alfo=lfo("a",pick_lfo_ratio(),coin(0.5,0,rnd(MAX_LFO_DELAY))),
            blfo=lfo("b",pick_lfo_ratio(),coin(0.5,0,rnd(MAX_LFO_DELAY))),
            aenv=adsr("a",
                      a=pick_env_segment_time(env_time_hint),
                      d=pick_env_segment_time(env_time_hint),
                      s=coin(0.75,0.3+rnd(0.7),rnd()),
                      r=pick_env_segment_time(env_time_hint),
                      lfo_trig=coin(0.1,1,0)),
            benv=adsr("b",
                      a=pick_env_segment_time(env_time_hint),
                      d=pick_env_segment_time(env_time_hint),
                      s=coin(0.75,0.3+rnd(0.7),rnd()),
                      r=pick_env_segment_time(env_time_hint),
                      lfo_trig=coin(0.1,1,0)),
            cenv=addsr(a=coin(0.50, pick_env_segment_time(ULTRA_FAST),
                              pick_env_segment_time(env_time_hint)),
                       d1=pick_env_segment_time(env_time_hint),
                       d2=pick_env_segment_time(env_time_hint),
                       r=pick_env_segment_time(env_time_hint),
                       bp=coin(0.75, 0.7+rnd(0.3), rnd()),
                       sus=rnd(),
                       trig=coin(0.1,1,0)),
            opa=fmop("a",mratio=pick_fm_modulation_ratio(is_harmonic),
                     mscale = coin(0.75, pick((2,3)), pick(MOD_SCALES[:4])),
                     mdepth = rnd(),
                     lfo = coin(0.1, rnd(), 0),
                     env = coin(0.5, rnd(), 0),
                     cratio = pick_fm_carrier_ratio(is_harmonic),
                     cbias = coin(0.75, 0, coin(0.75, rnd(2), rnd(99))),
                     feedback = coin(0.80, 0, rnd(3)),
                     cross_feedback = coin(0.9, 0, rnd(3)),
                     amp = coin(0.75, 1, rnd())),
            opb=fmop("b",mratio=pick_fm_modulation_ratio(is_harmonic),
                     mscale = coin(0.75, pick((2,3)), pick(MOD_SCALES[:4])),
                     mdepth = rnd(),
                     lfo = coin(0.1, rnd(), 0),
                     env = coin(0.5, rnd(), 0),
                     cratio = pick_fm_carrier_ratio(is_harmonic),
                     cbias = coin(0.75, 0, coin(0.75, rnd(2), rnd(99))),
                     feedback = coin(0.80, 0, rnd(3)),
                     cross_feedback = coin(0.9, 0, rnd(3)),
                     amp = coin(0.75, 1, rnd())),
            opc=wvop('c',sratio=pick_saw_ratio(is_harmonic),
                     pratio=pick_pulse_ratio(is_harmonic),
                     pw=coin(0.75, 0.5, rnd()),pwm=coin(0.5,0,rnd()),
                     wave=coin(0.75, 0.5, rnd()),
                     wave_lfo=coin(0.75,0,rsign(rnd())),
                     wave_env=coin(0.75,0,rsign(rnd())),
                     noise_amp=coin(0.90, 0, rnd()),
                     filter_track=coin(0.75,16,pick([1,2,3,4,5,6,7,8,9,12])),
                     filter_env=coin(0.75,0, pick([1,2,3,4,5,6,7,8,9,12])),
                     amp = coin(0.75, 1, rnd())),
            opd=wvop('d',sratio=pick_saw_ratio(is_harmonic),
                     pratio=pick_pulse_ratio(is_harmonic),
                     pw=coin(0.75, 0.5, rnd()),pwm=coin(0.5,0,rnd()),
                     wave=coin(0.75, 0.5, rnd()),
                     wave_lfo=coin(0.75,0,rsign(rnd())),
                     wave_env=coin(0.75,0,rsign(rnd())),
                     noise_amp=coin(0.90, 0, rnd()),
                     filter_track=coin(0.75,16,pick([1,2,3,4,5,6,7,8,9,12])),
                     filter_env=coin(0.75,0, pick([1,2,3,4,5,6,7,8,9,12])),
                     amp = coin(0.75, 1, rnd())),
            xfilter = pick_filter('x'),
            yfilter = pick_filter('y'))
    return p
