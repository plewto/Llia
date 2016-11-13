# llia.synths.corvus.rndgen.corvus_gen
# Top level random program generator
#


from __future__ import print_function
from llia.util.lmath import (rnd,coin,random_sign,approx,pick)
from llia.synths.corvus.rndgen.basic import basic_generator
#from llia.synths.corvus.corvusgen.chorusgen import chorus_generator
from llia.synths.corvus.corvus_constants import *


gen_config = {"p-harmonic"  : 0.6,           # probability harmonic frequency
              "p-bias"      : 0.3,
              "p-deep-modulation" : 0.1,     # 
              "p-pitch-env" : 0.02,          #
              "p-vibrato" : 0.30,
              "p-velocity" : 0.40,
              "p-lfo" : 0.1,                 # p of LFO -> mod depth
              "p-noise" : 0.4,               # p of OP3 noise
              "p-buzz" : 0.4,                # p of OP4 buzz
              "env-hint" : ADSR,             # see constants
              "env-time-hint" : None,
              "p-env-changeup" : 0.3,
              "engine" : None}


def corvusgen(slot=127, *_):
    return basic_generator(slot, gen_config)

