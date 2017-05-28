# llia.synths.siris.siris_random

from __future__ import print_function
from llia.util.lmath import (coin,rnd,pick)
from llia.synths.siris.siris_data import (siris,vibrato,adsr,excite,ks_excite,ks,
                                          clip,ks_trig,noise,filter)
from llia.synths.siris.siris_constants import *

def pick_max_env_segment():
    a = MAX_ENV_SEGMENT
    b,c,d = a/2,a/4,a/8
    return pick([a,b,c,d])

def pick_env_segment_time(max_time):
    max_time = coin(0.80, max_time, pick_max_env_segment)
    return rnd(max_time)

def pick_attack(max_time,p=0.8):
    t = rnd(coin(p, 0.005, max_time))
    return t

def pick_vibrato():
    timebase = 3+rnd(5)
    vratio = 1.0
    vsens = coin(0.50, 0, coin(0.75, 0.1, rnd()))
    vdepth = coin(0.50, 0, coin(0.75, rnd(0.3),rnd()))
    vdelay = coin(0.5, 0, rnd(2))
    return vibrato(timebase,vratio,vsens,vdepth,vdelay)

def pick_adsr(mx_time):
    return adsr(pick_attack(mx_time),
                pick_env_segment_time(max_time),
                coin(0.75, rnd(0.5), rnd()),
                pick_env_segment_time(max_time),
                mode = coin(0.8, 0, 1))

def pick_excite(n):
    harm = coin(0.80, pick([1,2,3,4]),pick([5,6,7,8]))
    hlfo = coin(0.5,-1,1) * coin(0.75, 0, int(rnd(harm)))
    henv = coin(0.5,-1,1) * coin(0.75, 0, int(rnd(harm)))
    pw = coin(0.8, pick([0.4,0.5,0.6]),pick([0.1,0.2,0.3,0.7,0.8,0.9]))
    pwlfo = coin(0.75, 0, coin(0.75, pick([0.1,0.2]), pick([0.1,0.2,0.3,0.4])))
    pwenv = coin(0.75, 0, pick([0.1,0.2,0.3,0.4,0.5]))
    return excite(n,harm,hlfo,henv,pw,pwlfo,pwenv)

def pick_excite_source(n):
    ex1 = coin(0.75, 1, 0)
    ex2 = coin(0.75, 0, 0.5+rnd())
    nse = coin(0.33, rnd(), 0)
    if n == 2:
        ex1,ex2 = ex2,ex1
    return ks_excite(n,ex1,ex2,nse,coin(0.80))

def pick_trig(n):
    mode = pick([0,1,2])
    ratio = coin(0.75,
                 pick([0.5,1,2,3,4,5,6]),
                 pick([8,9,10,12,15,16]))
    return ks_trig(n,mode,ratio)

def pick_clip(n):
    return clip(n,coin(0.20),coin(0.75,1,rnd(4)),coin(0.75,1,rnd()))

def pick_ks(n,mx_time):
    ratio = coin(0.75,
                 pick([0.5,1,1.5,2,3,4]),
                 coin(0.75, pick([0.25,0.75,5,6,8]), rnd(8)))
    att = pick_attack(mx_time)
    decay = pick_env_segment_time(mx_time)
    coef = coin(0.75, rnd(0.5), rnd())
    velocity = coin(0.75, 0, rnd())
    amp = coin(0.75, 1, rnd())
    delay = coin(0.75, 0, rnd(0.1))
    return ks(n,ratio,att,decay,coef,velocity,amp,delay)

def pick_noise(mx_time):
    att = pick_attack(mx_time)
    decay = pick_env_segment_time(mx_time)
    lowpass = coin(0.75, 16000, pick([12000,8000,6000,4000,3000]))
    highpass = coin(0.75, 100, pick([1000,2000,3000,4000,6000,8000]))
    return noise(att,decay,lowpass,highpass,
                 ex1_amp = coin(0.90,0, rnd()),
                 ex2_amp = coin(0.90,0, rnd()),
                 velocity = rnd(),
                 amp = coin(0.90, 0, rnd()))

def pick_filter():
    freq = coin(0.50,
                pick([100,200,300,400,600,800,1200]),
                1000*pick([2,3,4,6,8,10,16]))
    track = coin(0.75, 0, pick([0.5,1,1.5]))
    if freq > 6000:
        esign = -1
    elif freq > 2000:
        esign = coin(0.5, -1, 1)
    else:
        esign = 1
    env = esign*(coin(0.75, 0, rnd(16000)))
    lfo = coin(0.80,0, rnd(500))
    vel = coin(0.80, 0, rnd(8000))
    res = coin(0.75, rnd(0.6), rnd())
    return filter(freq,track,env,lfo,vel,res)

def siris_random(slot,*_):
    mx_env = pick_max_env_segment()
    rs = siris(slot,"Random",amp=0.1,
               port = coin(0.80, 0, coin(0.75, rnd(0.3), rnd())),
               vibrato = pick_vibrato(),
               adsr=adsr(mx_env),
               ex_lfo = 1.0/pick([1,2,2,3,3,3,4,4,4,4,5,5,5,5,5,6,7,8,
                                  9,10,11,12,13,14,15,16]),
               ex_attack = pick_attack(mx_env,p=0.5),
               ex_decay = pick_env_segment_time(mx_env),
               excite1 = pick_excite(1),
               excite2 = pick_excite(2),
               ks1_excite = pick_excite_source(1),
               ks2_excite = pick_excite_source(2),
               ks1_trig = pick_trig(1),
               ks2_trig = pick_trig(2),
               clip1 = pick_clip(1),
               clip2 = pick_clip(2),
               ks1 = pick_ks(1,mx_env),
               ks2 = pick_ks(2,mx_env),
               noise= pick_noise(mx_env),
               filter=pick_filter())
    return rs
