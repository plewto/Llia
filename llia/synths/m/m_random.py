# llia.synths.m.m_random

from llia.synths.m.m_constants import *
from llia.synths.m.m_data import (m,lfo,env,toneA,toneB,toneC,
                                  noise,mixer,filter_)
from llia.util.lmath import coin,rnd,pick

def r (value):
    return round(float(value), 4)

def sign(p=0.5):
    return coin(0.5, 1, -1)

def _lfo_ratio():
    low = LFO_RATIOS[:11]
    full = LFO_RATIOS
    return coin(0.75, pick(low), pick(full))

def _env_time(hint):
    hnt = coin(0.8, hint, pick(['FAST','MEDIUM','SLOW','GLACIAL']))
    if hnt == 'FAST':
        return r(rnd(0.1))
    elif hnt == 'MEDIUM':
        return r(0.1 + rnd(2))
    elif hnt == 'SLOW':
        return r(0.5 + rnd(4))
    else:
        return r(3+rnd(9))

def _env(n, time_hint, mode):
    times = []
    for i in range(4):
        times.append(_env_time(time_hint))
    bp = r(coin(0.75, 0.5+rnd(0.5), rnd()))
    sus = r(coin(0.75, 0.5+rnd(0.5), rnd()))
    mode = coin(0.90, mode, coin(0.50, 0, 1))
    return env(n,times,[bp,sus],mode)
                 
def _tune():
    harm = pick([0.125,0.25,0.50,0.75,1.0,1.333,1.5,2,3,4,5,6,8,12,16])
    return r(coin(0.75, harm, 0.1+rnd(16)))

def _ctune():
    harm = pick([1,1.333,1.5,2,3,4,5,6,7,8])
    return r(coin(0.75, harm, 1+rnd(8)))

def m_random(slot=127,*_):
    time_hint = pick(('FAST','MEDIUM','SLOW','GLACIAL'))
    env_mode = coin(0.80, 0, 1)
    rb1 = _tune()
    rb2 = coin(0.50, rb1+(coin(0.50, rnd(0.01), 0)), _tune())
    amps = []
    for i in range(3):
        amps.append(coin(0.75, 0.333+rnd(0.667), 0))
    amps.append(coin(0.75, 0, rnd()))
    amps[pick([0,1,2])]=1.0
    p = m(slot,"Random",
          port = coin(0.1, rnd(), 0),
          amp = 0.1,
          lfo =  lfo(vFreq = r(coin(0.75, 4+rnd(4), coin(0.75,
                                                         1+rnd(9),rnd(99)))),
                     vSens = r(coin(0.75, 0.1, rnd())),
                     vDepth = r(coin(0.75, 0.0, rnd())),
                     xPitch = 0.0,
                     aRatio = _lfo_ratio(),
                     bRatio = _lfo_ratio(),
                     cRatio = _lfo_ratio(),
                     aDelay = pick(LFO_DELAYS),
                     bDelay = pick(LFO_DELAYS),
                     cDelay = pick(LFO_DELAYS),
                     tLag = r(coin(0.50, 0, rnd()))),
          enva = _env('a',time_hint,env_mode),
          envb = _env('b',time_hint,env_mode),
          envc = _env('c',time_hint,env_mode),
          a = toneA(ratio = min(_tune()*pick([1,2,2,3,3,3,4,4,4,4,6,8,12,16,24,32]),99),
                    keyscale = [60,0,0],
                    quotient = [pick([1,2,3,4,5,6,7,8,9,10,11,12]),
                                coin(0.75, 0, pick(range(8))),
                                coin(0.75, 0, pick(range(8))),
                                0],
                    pulse = [r(coin(0.5, 0.5, rnd())),
                             r(coin(0.75, 0.0, rnd())),
                             r(coin(0.75, 0.0, rnd())),
                             0.0],
                    clkmix = coin(0.75, 0.0, rnd()),
                    envpitch = coin(0.90, 0.0, sign()*rnd()),
                    tremolo = coin(0.75, 0, rnd())),
          b = toneB(ratio1 = rb1, ratio2 = rb2,
                    keyscale = [60,0,0],
                    n1 = [pick(range(32)),
                          coin(0.75, 0.0, pick(range(32))),
                          coin(0.75, 0.0, pick(range(32))),
                          0.0],
                    n2 = [pick(range(32)),
                          coin(0.50, 0.0, rnd()),
                          coin(0.75, -1, coin(0.75, 1, 0))],
                    envpitch = coin(0.90, 0.0, sign()*rnd()),
                    tremolo = coin(0.75, 0, rnd())),
          c = toneC(ratio = _ctune(),
                    keyscale = [60,0,0],
                    pulseFreq = [_ctune(),
                                 coin(0.75, 0, pick(range(4))),
                                 coin(0.75, 0, pick(range(4))),
                                 0.0],
                    pwm = [coin(0.5, 0.5, rnd()),
                           coin(0.5, 0.0, rnd()),
                           coin(0.75, 0.0, rnd()),
                           0.0],
                    inciteSelect = coin(0.50, 0.0, rnd()),
                    envpitch = coin(0.90, 0, sign()*rnd()),
                    tremolo = coin(0.75,0, rnd())),
          noise = noise(lp = coin(0.75, 20000, 500+coin(5000)),
                        hp = coin(0.75, 10, 500+coin(5000)),
                        lag = coin(0.5, 0.0, rnd()),
                        tremolo = coin(0.75, 0, rnd())),
          mix = mixer(mix = amps,
                      pan = [sign()*rnd(),sign()*rnd(),sign()*rnd(),sign()*rnd()]),
          f1 = filter_(1,
                       freq = r(coin(0.75, rnd(5000), rnd(20000))),
                       track = r(pick([0,0,0,1])),
                       res = coin(0.75, rnd(0.5), rnd()),
                       lfo = [coin(0.75, 0.0, rnd(5000)),
                              coin(0.75, 0.0, rnd(5000))],
                       env = [coin(0.25, 0, coin(0.75, rnd(10000), -rnd(10000))),
                              coin(0.25, 0, coin(0.75, rnd(10000), -rnd(10000)))],
                       pan = 0.0),
          f2 = filter_(2,
                       freq = r(coin(0.75, rnd(5000), rnd(20000))),
                       track = r(pick([0,0,0,1])),
                       res = coin(0.75, rnd(0.5), rnd()),
                       lfo = [coin(0.75, 0.0, rnd(5000)),
                              coin(0.75, 0.0, rnd(5000))],
                       env = [coin(0.25, 0, coin(0.75, rnd(10000), -rnd(10000))),
                              coin(0.25, 0, coin(0.75, rnd(10000), -rnd(10000)))],
                       pan = 0.0))
    return p
