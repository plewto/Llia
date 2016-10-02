# llia.synths.chronos.chronos_random

from llia.util.lmath import *
from llia.synths.chronos.chronos_data import chronos


def random_program(slot=127, *_):
    p = chronos(slot, "Random",
                lfoCommonFreq = coin(0.75, rnd(3),rnd(10)),
                d1Dry1In = 1.0,
                d1Dry2In = 0.0,
                d1DelayTime = coin(0.5, rnd(2), coin(0.5, rnd(0.2), rnd(0.01))),
                d1LfoRatio = pick([0.125,0.25,0.5,0.75,1.0,1.5,2,3,4,5,6,8]),
                d1ExternalModDepth = 0.0,
                d1Lowpass = coin(0.75, 20000, pick([1000,2000,4000,8000])),
                d1Highpass = coin(0.75, 40, pick([200,400,800,1600,3200])),
                d1Feedback = coin(0.75, rnd(0.75), rnd()),
                d2Dry1In = 0.0,
                d2Dry2In = 1.0,
                d2Delay1In = coin(0.75, 0.0, 1.0),
                d2DelayTime = coin(0.5, rnd(2), coin(0.5, rnd(0.2), rnd(0.01))),
                d2LfoRatio = pick([0.125,0.25,0.5,0.75,1.0,1.5,2,3,4,5,6,8]),
                d2ExternalModDepth = 0.0,
                d2Lowpass = coin(0.75, 20000, pick([1000,2000,4000,8000])),
                d2Highpass = coin(0.75, 40, pick([200,400,800,1600,3200])),
                d2Feedback = coin(0.75, rnd(0.75), rnd()),
                dry1Amp = 1.0,
                dry2Amp = 1.0,
                d1Amp = coin(0.75, 1, 0.5 + rnd(0.5)),
                d2Amp = coin(0.75, 1, 0.5 + rnd(0.5)),
                dry1Pan = 0.75,
                dry2Pan = -0.75,
                d1Pan = -0.75,
                d2Pan = 0.75)
    return p
