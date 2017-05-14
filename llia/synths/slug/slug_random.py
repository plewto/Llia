# llia.synths.slug.slug_random

from __future__ import print_function
from llia.util.lmath import (coin,rnd,pick,approx,random_sign)
from llia.synths.slug.slug_data import (slug,lfo,adsr,pulse,pulse_filter,
                                        pluck,carrier,modulator)
from llia.synths.slug.slug_constants import *

def rsign(n=1):
    return random_sign(0.5,n)

def pick_env_time_hint():
    return coin(0.75,
                pick([ULTRA_FAST, FAST, MEDIUM]),
                pick([SLOW, SLOW, VERY_SLOW]))

def pick_env_segment_time(hint):
    hint = coin(0.75, hint, pick_env_time_hint())
    if hint == ULTRA_FAST:
        rs = rnd(0.05)
    elif hint == FAST:
        rs = rnd(0.1)
    elif hint == MEDIUM:
        rs = 0.1+rnd()
    elif hint == SLOW:
        rs = 1 + rnd(4)
    else:
        rs = 3+rnd(5)
    return rs

def pick_fratio(is_harmonic):
    if is_harmonic:
        rs = coin(0.75,
                  pick([0.5,1,1,1,2,2,2,3,3,4]),
                  coin(0.75,
                       pick([0.25,5,6,7,8]),
                       pick([0.75, 1.333, 1.5])))
    else:
        rs = 0.25+rnd(8)
    if coin(0.25):
        rs = approx(rs, 0.01)
    return rs

def pick_pluck_mod():
    rs = coin(0.25, 0, coin(0.75, rnd(4), rnd(MAX_PLUCK_MOD)))
    return rs


def slug_random(slot,*_):
    etime_hint = pick_env_time_hint()
    a1 = pick_env_segment_time(etime_hint)
    d1 = pick_env_segment_time(etime_hint)
    s1 = rnd()
    r1 = 2*pick_env_segment_time(etime_hint)
    p1 = 2*pick_env_segment_time(etime_hint)
    a2 = pick_env_segment_time(etime_hint)
    d2 = pick_env_segment_time(etime_hint)
    s2 = rnd()
    r2 = 2*pick_env_segment_time(etime_hint)
    p2 = 2*pick_env_segment_time(etime_hint)

    is_harmonic = coin(0.75, True, False)
    ffreq = pick([100,200,400,800,1600,3200,
                  6400,8000,10000,12000,16000])
    ffenv = rsign(coin(0.25, 0, pick([800,1600,3200,6400,8000,
                                      10000,12000,16000])))
    ffpenv = rsign(coin(0.25, 0, pick([800,1600,3200,6400,8000,
                                       10000,12000,16000])))
    fflfo = coin(0.75, 0, pick([100,200,400,800,1600,3200]))
    ffvel = coin(0.75, 0, pick([1000, 2000, 4000, 8000, 1600,
                                3200, 6400, 12000]))
    prog = slug(slot, "Random",amp=0.1,
                break_key=60,
                env_mode = coin(0.90, 0, 1),
                port = coin(0.90, 0, rnd()),
                port_velocity = coin(0.75, 0, rnd()),
                lfo = lfo(freq=coin(0.75, 3+rnd(5), rnd(8)),
                          delay=coin(0.5, 0, rnd(2)),
                          vsens = coin(0.9, 0.1, rnd()),
                          depth = coin(0.75, 0, rnd()),
                          noise = coin(0.75, 0, rnd()),
                          x=0.0),
                env1 = adsr(1,a1,d1,s1,r1,
                            velocity = coin(0.75, 0, rnd()),
                            key_scale = coin(0.75, 0, rnd())),
                env2 = adsr(2,a2,d2,s2,r2,
                            velocity = coin(0.75, 0, rnd()),
                            key_scale = coin(0.75, 0, rnd())),
                pdecay1 = p1,
                pdecay2 = p2,
                pulse = pulse(enable=coin(0.75, 1, 0),
                              amp = coin(0.50, 1.0, rnd()),
                              tune = pick_fratio(is_harmonic),
                              width = coin(0.75, 0.25+rnd(0.5), rnd()),
                              width_env1 = coin(0.25, rnd(), 0),
                              width_lfo = coin(0.25, rnd(0.5), 0),
                              env=rnd()),
                pulse_filter = pulse_filter(res=rnd(),
                                            cutoff=ffreq,
                                            env1=ffenv,
                                            penv1=ffpenv,
                                            lfo=fflfo,
                                            x=0,
                                            velocity=ffvel,
                                            left_track=0,
                                            right_track=0),
                pluck = pluck(enable=coin(0.75, 1, 0),
                              amp = coin(0.50, 1.0, rnd()),
                              tune = pick_fratio(is_harmonic),
                              decay = coin(0.5, 2*rnd(), rnd(MAX_PLUCK_DECAY)),
                              width = coin(0.5, 1, 0),
                              harmonic = coin(0.75,
                                              pick([1,2,3]),
                                              pick([4,5,6,7,8])),
                              damp = coin(0.75, rnd(0.5), 0.5+rnd(0.5)),
                              noise = rnd(),
                              velocity = coin(0.75, 0, rnd()),
                              left_scale = coin(0.75, 0, rsign(pick([3,6,9]))),
                              right_scale = coin(0.75, 0, rsign(pick([3,6,9])))),
                car1 = carrier(1, enable=coin(0.75, 1, 0),
                               amp = coin(0.50, 0.5+rnd(), rnd()),
                               tune = pick_fratio(is_harmonic),
                               bias = coin(0.75, coin(0.90, rnd(2), rnd(999))),
                               velocity = coin(0.75, 0, rnd()),
                               left_scale=0, right_scale=0, env=rnd(),
                               mod_scale = coin(0.75, 1+rnd(4),
                                                coin(0.80, 1+rnd(12), rnd(MAX_MOD_SCALE))),
                               xmod=0.0,
                               fm=coin(0.75, rnd(), 0),
                               pluck=pick_pluck_mod()),
                car2 = carrier(2, enable=coin(0.75, 1, 0),
                               amp = coin(0.50, 0.5+rnd(), rnd()),
                               tune = pick_fratio(is_harmonic),
                               bias = coin(0.75, coin(0.90, rnd(2), rnd(999))),
                               velocity = coin(0.75, 0, rnd()),
                               left_scale=0, right_scale=0, env=rnd(),
                               mod_scale = coin(0.75, 1+rnd(4),
                                                coin(0.80, 1+rnd(12), rnd(MAX_MOD_SCALE))),
                               xmod=0.0,
                               fm=coin(0.75, rnd(), 0),
                               pluck=pick_pluck_mod()),
                mod1 = modulator(1, enable=coin(0.75, 1, 0),
                                 tune=pick_fratio(is_harmonic),
                                 pluck=pick_pluck_mod(),
                                 velocity=coin(0.75, 0, rnd()),
                                 left_scale=0, right_scale=0,
                                 env=rnd()),
                mod2 = modulator(2, enable=coin(0.75, 1, 0),
                                 tune=pick_fratio(is_harmonic),
                                 pluck=pick_pluck_mod(),
                                 velocity=coin(0.75, 0, rnd()),
                                 left_scale=0, right_scale=0,
                                 env=rnd()))
    return prog
