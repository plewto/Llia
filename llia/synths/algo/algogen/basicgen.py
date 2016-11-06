# llia.synths.algo.algogen.basicgen
#
# Basic patch generator


from llia.synths.algo.algo_constants import *
from llia.util.lmath import (rnd,coin,pick)
from llia.synths.algo.algo_data import (vibrato,stack,env,op,algo)
from llia.synths.algo.algogen.envgen import pick_envelopes
from llia.synths.algo.algogen.freqgen import pick_frequencies
from llia.synths.algo.algogen.ampgen import operator_amps,modulation_scales


def _round(n):
    return round(n,3)

def pick_velocity():
    return coin(0.5, 0, _round(rnd()))

def pick_op_lfo():
    return coin(0.2 ,_round(rnd()), 0)

# p_feedback  - probabbilty there is feedback
# Returns tuple (fb,env,lfo)
#
def pick_stack_feedback(p_feedback):
    fb = env = lfo = 0.0
    if coin(p_feedback):
        fb,env,lfo = coin(0.75,      # p "simple" feedback w/o modulation
                          (rnd(2),0.0,0.0),
                          (coin(0.33, rnd(), 0),
                           coin(0.33, rnd(), 0),
                           coin(0.33, rnd(), 0)))
    fb = _round(fb)
    env = _round(env)
    lfo = _round(lfo)
    return fb,env,lfo

# pick vibrato parameters
# Returns tuple (frequency, delay, sensitivity, depth)
#
def pick_vibrato():
    freq = _round(coin(0.75,2+rnd(5),coin(0.80, rnd(10),rnd(99))))
    dly = _round(rnd(4))
    sens = _round(coin(0.90, rnd(0.2),rnd()))
    depth = _round(coin(0.75, rnd(0.5), 0))
    return freq,dly,sens,depth
    
    
# Returns tuple (ratio,delay,wave)
#
def pick_stack_lfo():
    r = coin(0.75, pick(LFO_RATIOS[:14]), pick(LFO_RATIOS))[0]
    dly = _round(rnd(4))
    wv = _round(rnd())
    return r,dly,wv



def basic_generator(slot=127,
                    p_harmonic=0.80,
                    p_deep_modulation = 0.10,
                    env_type_hint = None,
                    env_time_hint = None,
                    p_env_changeup = 0.10,
                    p_feedback = 0.1):
    ratios,biases =pick_frequencies(p_harmonic)
    op_amps = operator_amps()
    mod_scales = modulation_scales(p_deep_modulation)
    envelopes = pick_envelopes(env_type_hint,
                               env_time_hint,
                               p_env_changeup,
                               p_env_changeup,
                               p_duplicate_carrier = 0.35)
    env1, env2, env3, env4, env5, env6, env7, env8 = envelopes
    vf,vdly,vsens,vdepth = pick_vibrato()
    afb = pick_stack_feedback(p_feedback)
    bfb = pick_stack_feedback(p_feedback)
    cfb = pick_stack_feedback(p_feedback)
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
             stackA = stack("A",True,op_amps[0],60,
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
             
