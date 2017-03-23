# llia.synths.scanner.scanner_random

from __future__ import print_function
from llia.util.lmath import (coin,rnd,pick,random_sign)
from llia.synths.scanner.scanner_data import scanner
#from llia.synths.scanner.scanner_constants import *

def scanner_random(slot,*_):
    srate = coin(0.50, rnd(7),coin(0.90, rnd(), rnd(100)))
    wave = coin(0.70, 0.5, rnd())
    delay = rnd(0.05)
    depth = rnd()
    feedback = random_sign(0.5, coin(0.75, 0.5+rnd(0.49), rnd(0.75)))
    if abs(feedback) > 0.75:
        lowpass = pick((16000, 12000, 8000, 8000, 8000, 4000, 4000, 2000))
    else:
        lowpass = 16000
    dry = 0.5
    wet = 0.5

    return scanner(slot, "Random",
                   srate, wave, delay, depth,
                   feedback,lowpass, dry, wet, wet, 0.0)

