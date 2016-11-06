# llia.synths.algo.algogen.algo_random

from __future__ import print_function
from llia.util.lmath import (rnd,coin,random_sign,approx,pick)
from llia.synths.algo.algogen.basicgen import basic_generator

p_harmonic = 0.8
p_deep_modulation = 0.10
env_type_hint = None
env_time_hint = None
p_env_changeup = 0.10






def algogen(slot=127,*_):
    basic_generator()
    prog = basic_generator(slot,
                           p_harmonic = p_harmonic,
                           p_deep_modulation = p_deep_modulation,
                           env_type_hint = env_type_hint,
                           env_time_hint = env_time_hint,
                           p_env_changeup = p_env_changeup)
    return prog
