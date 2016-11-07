# llia.synths.algo.algogen.chorusgen
#
# Specilized algo patch generator uses at least one
# carrier with fixed frequency for corusing effect.

from __future__ import print_function
from llia.synths.algo.algo_constants import *
from llia.util.lmath import (rnd,coin,pick)
from llia.synths.algo.algo_data import (vibrato,stack,env,op,algo)
from llia.synths.algo.algogen.envgen import pick_envelopes
from llia.synths.algo.algogen.freqgen import pick_frequencies
from llia.synths.algo.algogen.ampgen import operator_amps,modulation_scales
from llia.synths.algo.algogen.basicgen import (pick_velocity,
                                               pick_op_lfo,
                                               pick_stack_feedback,
                                               pick_vibrato,
                                               pick_stack_lfo)

def _round(n):
    return round(n,4)

def chorus_generator(slot=127,genconfig={}):
    print("# Using chorus_generator")
    def get_config(key,dflt):
        return genconfig.get(key,dflt)
    ratios,biases = pick_frequencies(get_config("p-harmonic", 0.8))
    op_amps = operator_amps()
    mod_scales = modulation_scales(0)
    ratios,biases,mod_scales = list(ratios),list(biases),list(mod_scales)
    for stk in "ABC":
        use_chorus = coin(0.6)
        if use_chorus:
            cop = {"A":1,"B":5,"C":7}[stk]
            mod1 = {"A":2,"B":4,"C":8}[stk]
            mod2 = {"A":3,"B":6,"C":None}[stk]
            ratios[cop-1] = 0
            biases[cop-1] = coin(0.75, _round(rnd(2)), _round(rnd(7)))
            mod_scales[mod1-1] = pick((100,100,1000,1000,10000))
            if (mod2 == 6 and coin(0.20)):
                mod_scales[mod2-1] = pick((100,100,1000,1000,10000))
    envelopes = pick_envelopes(get_config("env-type-hint",ADSR),
                               get_config("env-time-hint",ADSR),
                               get_config("p-env-changeup",MEDIUM),
                               get_config("p-env-changeup",MEDIUM),
                               p_duplicate_carrier = 0.35)
    env1, env2, env3, env4, env5, env6, env7, env8 = envelopes
    vf,vdly,vsens,vdepth = pick_vibrato()
    pfb = get_config("p-feedback",0.1)
    afb = pick_stack_feedback(pfb)
    bfb = pick_stack_feedback(pfb)
    cfb = pick_stack_feedback(pfb)
    alfo = pick_stack_lfo()
    blfo = pick_stack_lfo()
    clfo = pick_stack_lfo()
    def openv(op,value):
        return env(op,value[0],value[1],value[2],value[3],
                   value[4],value[5],value[6])
    def opp(n):
        index = n-1
        return op(n,
                  ratios[index],
                  biases[index],
                  op_amps[index],
                  mod_scales[index],
                  0,0,
                  pick_velocity(),
                  pick_op_lfo(),
                  0)
    p = algo(slot,"Random",
             amp = 0.5,
             modDepth = _round(coin(0.75, 1.0, 0.5+rnd(0.5))),
             external = [0.0, 0.0, 1.0], # [mod,pitch,scale]
             vibrato = vibrato(vf,vdly,vsens,vdepth),
             stackA = stack("A",
                            True,
                            op_amps[0],
                            60,
                            feedback=afb[0],
                            fb_env=afb[1],
                            fb_lfo=afb[2],
                            lfo_ratio=alfo[0],
                            lfo_delay=alfo[1],
                            lfo_wave=alfo[2]),
             stackB = stack("B",True,op_amps[4],60,
                            feedback=bfb[0],
                            fb_env=bfb[1],
                            fb_lfo=bfb[2],
                            lfo_ratio=blfo[0],
                            lfo_delay=blfo[1],
                            lfo_wave=blfo[2]),
              stackC = stack("C",True,op_amps[6],60,
                            feedback=cfb[0],
                            fb_env=cfb[1],
                            fb_lfo=cfb[2],
                            lfo_ratio=clfo[0],
                            lfo_delay=clfo[1],
                            lfo_wave=clfo[2]),
             env1 = openv(1,env1),
             env2 = openv(2,env2),
             env3 = openv(3,env3),
             env4 = openv(4,env4),
             env5 = openv(5,env5),
             env6 = openv(6,env6),
             env7 = openv(7,env7),
             env8 = openv(8,env8),
             op1 = opp(1),
             op2 = opp(2),
             op3 = opp(3),
             op4 = opp(4),
             op5 = opp(5),
             op6 = opp(6),
             op7 = opp(7),
             op8 = opp(8))
    return p
