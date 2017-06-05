# llia.synths.sandcat.sandcat_random

from __future__ import print_function
from llia.util.lmath import (coin,rnd,pick)
from llia.synths.sandcat.sandcat_data import (sandcat,vibrato,lfo,clock,adsr,
                                              excite,pluck,stack,mod,car,
                                              mixer,panner)
from llia.synths.sandcat.sandcat_constants import *

SIMPLE_LFO_RATIOS = (1/16.0,
                     1/8.0,
                     1/3.0,
                     1/4.0,
                     1/2.0,
                     2/3.0,
                     3/4.0)

COMPLEX_LFO_RATIOS = SIMPLE_LFO_RATIOS + (3/8.0,
                                          5/8.0,
                                          7/8.0,
                                          1/5.0,
                                          2/5.0,
                                          3/5.0,
                                          4/5.0,
                                          1/6.0,
                                          5/6.0,
                                          1/9.0,
                                          2/9.0,
                                          4/9.0,
                                          5/9.0,
                                          7/9.0,
                                          8/9.0)
def pick_vibrato():
    freq = coin(0.75, 4+rnd(4), rnd(8))
    delay = coin(0.75, 0, rnd(2))
    sens = coin(0.75, rnd(0.1), rnd())
    depth = coin(0.75, 0, rnd())
    return vibrato(freq,delay,sens,depth)

def pick_excite(n):
    harm = coin(0.50, pick((1,2,3)), pick((3,4,5,6,7,8)))
    lfo = coin(0.75, 0, pick(EX_HARMONICS_MOD))
    env = coin(0.75, 0, pick(EX_HARMONICS_MOD))
    pw = coin(0.75, pick((0.4,0.5,0.6)), pick(EX_PW))
    pwm = coin(0.75, 0, pick(EX_PWM[1:]))
    pink = coin()
    mix = coin(0.5, coin(0.5, -1, 1), -1+rnd(2))
    return excite(n,harm,lfo,env,pw,pwm,pink,mix)

def pick_lfo_ratio(previous=None):
    def pick_r():
        return coin(0.75, pick(SIMPLE_LFO_RATIOS), 
                    coin(0.75, pick(COMPLEX_LFO_RATIOS), 0.1+rnd()))
    if not previous:
        r = pick_r()
    else:
        r = previous
        while r == previous:
            r = pick_r()
    return r

def pick_lfo(n,r):
    xmod = coin(0.75, 0.0, rnd(8))
    return lfo(n,r)


def pick_env_hint():
    t = coin(0.50, rnd(0.1),
             coin(0.75, rnd(),rnd(MAX_ENV_SEGMENT)))
    return t

def pick_adsr(n,hint):
    hint = coin(0.75, hint, pick_env_hint)
    def time():
        return rnd(hint)
    a,d,r = time(), time(), 2*time()
    s = coin(0.75, 0.5+rnd(), rnd())
    mode = coin(0.80, 0, 1)
    src = coin(0.75, 0, coin(0.75,
                             pick((1,2,3,4,7,8)),
                             pick((9,10,11,12,15,16))))
    return adsr(n,a,d,s,r,src,mode)
    
def pick_ks_ratio(harmonic_hint):
    if harmonic_hint:
        return coin(0.75, pick((0.5,1,2)), pick((0.25,0.75,1.5,3,4)))
    else:
        return coin(0.75, 0.5+rnd(2), coin(0.75, 0.25+rnd(2), coin(0.5, rnd(0.5), rnd(6))))

def pick_pluck(n, harmonic_hint):
    r = pick_ks_ratio(harmonic_hint)
    trig = coin(0.75, 0, coin(0.75, pick((1,2,3,4,7,8)), pick((9,10,11,12,15,16))))
    decay = coin(0.75, 4+rnd(4), rnd(8))
    coef = coin(0.75, rnd(0.333), rnd())
    vel = coin(0.50, 0, rnd())
    return pluck(n,r,decay,coef,trig,vel)

def pick_stack(n):
    fb = coin(0.75, 0, rnd(6))
    lfo = coin(0.75, 0, rnd())
    return stack(n,feedback=fb, feedback_lfo=lfo)

def pick_modulator_ratio(harmonic_hint):
    if harmonic_hint:
        return coin(0.75, pick((0.5, 1, 2, 3)), pick((0.5,0.75,1,1.5,2,3,4,5,6,8)))
    else:
        return coin(0.75, 0.5+rnd(3), coin(0.5, rnd(0.5), rnd(15)))

def pick_mod(n,harmonic_hint):
    r = pick_modulator_ratio(harmonic_hint)
    if coin(0.03): r = 0.001
    if r == 0.001:
        b = coin(0.9, rnd(0.1), rnd(300))
        ks = coin(0.75, rnd(10), rnd(5000))
    else:
        b = coin(0.75, 0.0, rnd(0.01))
        ks = coin(0.75, 0, rnd(4))
    env = coin(0.75, 1, rnd())
    lag = coin(0.5, 0, rnd())
    lfo = coin(0.75, 0, rnd())
    vel = coin(0.75, 0, rnd())
    return mod(n,r,b,ks,env,lag,lfo,vel)
    
def pick_cutoff():
    return coin(0.50, 4000+rnd(12000), rnd(4000))

def pick_track():
    return coin(0.8, 0, pick([0.5,1,1.5,2]))

def pick_filter_env(freq,track):
    if freq>4000 or track>=1:
        pneg = 0.33
    else:
        pneg = 0.05
    sign = coin(pneg, -1, 1)
    mag = coin(0.75, rnd(4000), rnd(8000))
    return sign*mag

def pick_filter_lfo():
    return coin(0.80, 0, coin(0.75, rnd(500), rnd(4000)))

def pick_filter_velocity():
    return coin(0.75, 0, coin(0.75, rnd(4000), rnd(8000)))

def pick_filter_res():
    return coin(0.5, rnd(0.5), 0.5+rnd(0.5))

def pick_carrier_ratio(harmonic_hint):
    return pick_modulator_ratio(harmonic_hint)

def pick_car(n,harmonic_hint):
    r = pick_carrier_ratio(harmonic_hint)
    if coin(0.03): r = 0.001
    if r == 0.001:
        b = coin(0.9, rnd(0.1), rnd(300))
        mx = 5000
    else:
        b = coin(0.75,0.0,rnd())
        mx = 8
    ks = mx*coin(0.75, 0.0, rnd())
    if not ks:
        mod = rnd()
    else:
        mod = mx*coin(0.75,0.0,rnd())
    if n == 1:
        mod1 = mod
        mod2 = 0
    else:
        mod1 = coin(0.75, 0, mod)
        if not mod1:
            mod2 = rnd()
        else:
            mod2 = coin(0.75, 0, rnd)
        mod2 = mx*mod2
    gate = coin(0.80, 1, 0)
    lfo = coin(0.75, 0, rnd())
    vel = coin(0.75, 0, rnd())
    return car(n,r,b,mod1,mod2,ks,gate,lfo,vel)

def pick_mixer():
    p1 = coin(0.667, 0.333+rnd(0.667), 0)
    s1 = coin(0.667, 0.333+rnd(0.667), 0)
    p2 = coin(0.667, 0.333+rnd(0.667), 0)
    s2 = coin(0.667, 0.333+rnd(0.667), 0)
    return mixer(ks1=p1, ks2=p2, stack1=s1, stack2=s2)

def pick_panner():
    p1 = coin(0.75, coin(0.75, 1, 0.5+rnd(0.5)), -1*rnd(2))
    s1 = coin(0.75, coin(0.75, 1, 0.5+rnd(0.5)), -1*rnd(2))
    p2 = coin(0.75, coin(0.75, -1, -1+rnd(0.5)), -1*rnd(2))
    s2 = coin(0.75, coin(0.75, -1, -1+rnd(0.5)), -1*rnd(2))
    return panner(p1,p2,s1,s2)
    
    
def sandcat_random(slot,*_):
    harmonic_hint = coin(0.75)
    lfr1 = pick_lfo_ratio()
    clk1 = pick_lfo_ratio(lfr1)
    lfr2 = pick_lfo_ratio()
    clk2 = pick_lfo_ratio(lfr2)
    env_hint = pick_env_hint()
    f1 = pick_cutoff()
    f1_trk = pick_track()
    f1_env = pick_filter_env(f1,f1_trk)
    f2 = pick_cutoff()
    f2_trk = pick_track()
    f2_env = pick_filter_env(f2,f2_trk)
    p = sandcat(slot, "Random", amp=0.1,
                vibrato=pick_vibrato(),
                lfo1 = pick_lfo(1,lfr1),
                lfo2 = pick_lfo(2,lfr2),
                clk1 = clock(1, clk1),
                clk2 = clock(2, clk2),
                env1 = pick_adsr(1,env_hint),
                env2 = pick_adsr(2,env_hint),
                env3 = pick_adsr(3,env_hint),
                env4 = pick_adsr(4,env_hint),
                ex1 = pick_excite(1),
                ex2 = pick_excite(2),
                ks1 = pick_pluck(1, harmonic_hint),
                ks2 = pick_pluck(2, harmonic_hint),
                stack1 = stack(1),
                stack2 = stack(2),
                mod1 = pick_mod(1,harmonic_hint),
                mod2 = pick_mod(2,harmonic_hint),
                car1 = pick_car(1,harmonic_hint),
                car2 = pick_car(2,harmonic_hint),

                f1_cutoff = f1, f1_track = f1_trk, f1_env3 = f1_env,
                f1_lfo1 = pick_filter_lfo(), f1_lfov = pick_filter_lfo(),
                f1_res = pick_filter_res(), f1_velocity = pick_filter_velocity(),

                f2_cutoff = f2, f2_track = f2_trk, f2_env4 = f2_env,
                f2_lfo2 = pick_filter_lfo(), f2_lfov = pick_filter_lfo(),
                f2_res = pick_filter_res(), f2_velocity = pick_filter_velocity(),

                mixer = pick_mixer(),
                panner = pick_panner(),
                f1_pan = 0.5,
                f2_pan = -0.5)
    return p
