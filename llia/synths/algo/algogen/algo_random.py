# llia.synths.algo.algogen.algo_random
# Top level random program generator
# 

from __future__ import print_function
from llia.util.lmath import (rnd,coin,random_sign,approx,pick)
from llia.synths.algo.algogen.basicgen import basic_generator
from llia.synths.algo.algogen.chorusgen import chorus_generator
from llia.synths.algo.algo_constants import *

gen_config = {"p-harmonic" : 0.8,
              "p-deep-modulation" : 0.10,
              "env-type-hint" : ADSR,
              "env-time-hint" : MEDIUM,
              "p-env-changeup" : 0.10,
              "p-feedback" : 0.1,
              "engion" : None}
              

def _random_engion(slot,gconfig):
    fn = pick((basic_generator,chorus_generator))
    return fn(slot,gconfig)

def set_engion(name):
    name = name.lower()
    fn = {"random":_random_engion,
          "basic":basic_generator,
          "chorus":chorus_generator}[name]
    gen_config["engion"] = fn



    
set_engion("random")
    
def algogen(slot=127,*_):
    print("DEBUG time hint is ", gen_config["env-time-hint"])
    eng = gen_config["engion"]
    prog = eng(slot,gen_config)
    return prog
