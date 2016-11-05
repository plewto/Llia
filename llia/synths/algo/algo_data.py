# llia.synths.algo.algo_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance

MOD_SCALE_COUNT = 6


prototype = {
    "amp" : 0.1,
    "port" : 0.0,
    "lfoA_delay" : 0.0,
    "lfoA_ratio" : 1.0,
    "lfoA_wave" : 0.5,
    "lfoB_delay" : 0.0,
    "lfoB_ratio" : 1.0,
    "lfoB_wave" : 0.5,
    "lfoC_delay" : 0.0,
    "lfoC_ratio" : 1.0,
    "lfoC_wave" : 0.5,
    "lfov_delay" : 0.0,
    "lfov_freq" : 7.0,
    "modDepth" : 1.0,
    "op1_amp" : 1.0,
    "op1_attack" : 0.0,
    "op1_bias" : 0.0,
    "op1_breakpoint" : 1.0,
    "op1_decay1" : 0.0,
    "op1_decay2" : 0.0,
    "op1_envmode" : 0,
    "op1_external" : 0.0,
    "op1_left_scale" : 0,
    "op1_lfo"  : 0.0,
    "op1_ratio" : 1.0,
    "op1_release" : 0.0,
    "op1_right_scale" : 0,
    "op1_sustain" : 1.0,
    "op1_velocity" : 0,
    "op2_amp" : 0.0,
    "op2_attack" : 0.0,
    "op2_bias" : 0.0,
    "op2_breakpoint" : 1.0,
    "op2_decay1" : 0.0,
    "op2_decay2" : 0.0,
    "op2_envmode" : 0,
    "op2_external" : 0,
    "op2_left_scale" : 0,
    "op2_lfo" : 0,
    "op2_mod_scale" : 1.0,
    "op2_ratio" : 1.0,
    "op2_release" : 0.0,
    "op2_right_scale" : 0,
    "op2_sustain" : 1.0,
    "op2_velocity" : 0,
    "op3_amp" : 0.0,
    "op3_attack" : 0.0,
    "op3_bias" : 0.0,
    "op3_breakpoint" : 1.0,
    "op3_decay1" : 0.0,
    "op3_decay2" : 0.0,
    "op3_envmode" : 0,
    "op3_external" : 0,
    "op3_left_scale" : 0,
    "op3_lfo" : 0,
    "op3_mod_scale" : 1.0,
    "op3_ratio" : 1.0,
    "op3_release" : 0.0,
    "op3_right_scale" : 0,
    "op3_sustain" : 1.0,
    "op3_velocity" : 0,
    "op4_amp" : 0.0,
    "op4_attack" : 0.0,
    "op4_bias" : 0.0,
    "op4_breakpoint" : 1.0,
    "op4_decay1" : 0.0,
    "op4_decay2" : 0.0,
    "op4_envmode" : 0,
    "op4_external" : 0,
    "op4_left_scale" : 0,
    "op4_lfo" : 0,
    "op4_mod_scale" : 1.0,
    "op4_ratio" : 1.0,
    "op4_release" : 0.0,
    "op4_right_scale" : 0,
    "op4_sustain" : 1.0,
    "op4_velocity" : 0,
    "op5_amp" : 1.0,
    "op5_attack" : 0.0,
    "op5_bias" : 0.0,
    "op5_breakpoint" : 1.0,
    "op5_decay1" : 0.0,
    "op5_decay2" : 0.0,
    "op5_envmode" : 0,
    "op5_external" : 0.0,
    "op5_left_scale" : 0,
    "op5_lfo" : 0.0,
    "op5_ratio" : 1.0,
    "op5_release" : 0.0,
    "op5_right_scale" : 0,
    "op5_sustain" : 1.0,
    "op5_velocity" : 0,
    "op6_amp" : 0.0,
    "op6_attack" : 0.0,
    "op6_bias" : 0.0,
    "op6_breakpoint" : 1.0,
    "op6_decay1" : 0.0,
    "op6_decay2" : 0.0,
    "op6_envmode" : 0,
    "op6_external" : 0,
    "op6_left_scale" : 0,
    "op6_lfo" : 0,
    "op6_mod_scale" : 1.0,
    "op6_ratio" : 1.0,
    "op6_release" : 0.0,
    "op6_right_scale" : 0,
    "op6_sustain" : 1.0,
    "op6_velocity" : 0,
    "op7_amp" : 1.0,
    "op7_attack" : 0.0,
    "op7_bias" : 0.0,
    "op7_breakpoint" : 1.0,
    "op7_decay1" : 0.0,
    "op7_decay2" : 0.0,
    "op7_envmode" : 0,
    "op7_external" : 0.0,
    "op7_left_scale" : 0,
    "op7_lfo" : 0.0,
    "op7_ratio" : 1.0,
    "op7_release" : 0.0,
    "op7_right_scale" : 0,
    "op7_sustain" : 1.0,
    "op7_velocity" : 0,
    "op8_amp" : 0.0,
    "op8_attack" : 0.0,
    "op8_bias" : 0.0,
    "op8_breakpoint" : 1.0,
    "op8_decay1" : 0.0,
    "op8_decay2" : 0.0,
    "op8_envmode" : 0,
    "op8_external" : 0,
    "op8_left_scale" : 0,
    "op8_lfo" : 0,
    "op8_mod_scale" : 1.0,
    "op8_ratio" : 1.0,
    "op8_release" : 0.0,
    "op8_right_scale" : 0,
    "op8_sustain" : 1.0,
    "op8_velocity" : 0,
    "stackA_enable" : 1,
    "stackA_env_feedback" : 0.0,
    "stackA_feedback" : 0.0,
    "stackA_key" : 60,
    "stackA_lfo_feedback" : 0.0,
    "stackB_enable" : 1,
    "stackB_env_feedback" : 0.0,
    "stackB_feedback" : 0.0,
    "stackB_key" : 60,
    "stackB_lfo_feedback" : 0.0,
    "stackC_enable" : 1,
    "stackC_env_feedback" : 0.0,
    "stackC_feedback" : 0.0,
    "stackC_key" : 60,
    "stackC_lfo_feedback" : 0.0,
    "vdepth" : 0.0,
    "vsens" : 0.1,
    "xmod" : 0.0,
    "xpitch" : 0.0,
    "xscale" : 1.0}

class Algo(Program):

    def __init__(self,name):
        super(Algo,self).__init__(name,Algo,prototype)
        self.performance = performance()

program_bank = ProgramBank(Algo("Init"))
program_bank.enable_undo = False


def vibrato(freq=5.0,
            delay=0.0,
            sens = 0.1,
            depth = 0.0):
    return {"lfov_freq" : float(freq),
            "lfov_delay" : float(delay),
            "vsens" : float(sens),
            "vdepth" : float(depth)}
            


def stack(id_,
          enable=True,          # stackX_enable
          amp = 1.0,            # op[1,5,7]_amp
          break_key = 60,       # stackX_key
          feedback = 0.0,       # stackX_feedback
          fb_env = 0.0,         # stackX_env_feedback
          fb_lfo = 0.0,         # stackX_lfo_feedback
          lfo_ratio = 1.0,      # lfoX_ratio
          lfo_delay = 0.0,      # lfoX_delay
          lfo_wave = 0.5):      # lfoX_wave
    id_ = str(id_).upper()
    carrier = {"A":1,"B":5,"C":7}[id_]
    def lfo(q):
        return "lfo%s_%s" % (id_,q)
    def param(q):
        return "stack%s_%s" % (id_,q)
    if enable:
        flag = 1
    else:
        flag = 0
    d = {param("enable") : float(flag),
         "op%s_amp" % carrier : float(amp),
         param("key") : int(break_key),
         param("feedback") : float(feedback),
         param("env_feedback") : float(fb_env),
         param("lfo_feedback") : float(fb_lfo),
         lfo("ratio") : float(lfo_ratio),
         lfo("delay") : float(lfo_delay),
         lfo("wave") : float(lfo_wave)}
    return d

def env(op,
        attack = 0.0,
        decay1 = 0.0,
        decay2 = 0.0,
        release = 0.0,
        breakpoint = 1.0,
        sustain = 1.0,
        mode = 0):
    def param(key):
        return "op%d_%s" % (op,key)
    d = {param("attack") : float(attack),
         param("decay1") : float(decay1),
         param("decay2") : float(decay2),
         param("release") : float(release),
         param("breakpoint") : float(breakpoint),
         param("sustain") : float(sustain),
         param("mode") : int(mode)}
    return d

def _carrier(op,
             ratio = 1.0,
             bias = 0.0,
             left = 0,
             right = 0,
             velocity = 0.0,
             lfo = 0.0,
             external = 0.0):
    def param(key):
        return "op%d_%s" % (op,key)
    d ={param("ratio") : float(ratio),
        param("bias") : float(bias),
        param("left_scale") : int(left),
        param("right_scale") : int(right),
        param("lfo") : float(lfo),
        param("external") : float(external)}
    return d

def _modulator(op,
       	       ratio = 1.0,
	       bias = 0.0,
	       amp = 0.0,
	       mod_scale = 1.0,
	       left = 0,
	       right = 0,
	       velocity = 0.0,
	       lfo = 0.0,
	       external = 0.0):
    def param(key):
        return "op%d_%s" % (op,key)
    d = {param("ratio") : float(ratio),
         param("bias") : float(bias),
         param("amp") : float(amp),
         param("mod_scale") : float(mod_scale),
         param("left_scale") : int(left),
         param("right_scale") : int(right),
         param("velocity") : float(velocity),
         param("lfo") : float(lfo),
         param("external") : float(external)}
    return d

def is_carrier(n):
    return n==1 or n==5 or n==7

def op(n,
       ratio = 1.0,
       bias = 0.0,
       amp = 0.0,
       mod_scale = 1.0,
       left = 0,
       right = 0,
       velocity = 0.0,
       lfo = 0.0,
       external = 0.0):
    if is_carrier(n):
        return _carrier(n,ratio,bias,left,right,velocity,lfo,external)
    else:
        return _modulator(n,ratio,bias,amp,mod_scale,left,right,velocity,lfo,external)

def _fill(lst, template):
    acc = []
    for i,dflt in enumerate(template):
        try:
            val = float(lst[i])
            acc.append(val)
        except IndexError:
            acc.append(dflt)
    return acc
    
def algo(slot, name,
         amp = 1.0,
         modDepth = 1.0,
         port = 0.0,
         external = [0.0, 0.0, 1.0], # [mod,pitch,scale]
         vibrato = vibrato(),
         stackA = stack("A"),
         stackB = stack("B"),
         stackC = stack("C"),
         env1 = env(1),
         env2 = env(2),
         env3 = env(3),
         env4 = env(4),
         env5 = env(5),
         env6 = env(6),
         env7 = env(7),
         env8 = env(8),
         op1 = op(1),
         op2 = op(2),
         op3 = op(3),
         op4 = op(4),
         op5 = op(5),
         op6 = op(6),
         op7 = op(7),
         op8 = op(8)):
    p = Algo(name)
    p["amp"] = float(amp)
    p["modDepth"] = float(modDepth)
    p["port"] = float(port)
    x = _fill(external, [0.0,0.0,1.0])
    p["xmod"] = float(x[0])
    p["xpitch"] = float(x[1])
    p["xscale"] =float(x[2])
    for d in (stackA,stackB,stackC):
        for k,v in d.items():
            p[k] = v
    for d in (vibrato,
              env1,env2,env3,env4,env5,env6,env7,env8,
              op1,op2,op3,op4,op5,op6,op7,op8):
        for k,v in d.items():
            p[k] = v
    program_bank[slot] = p
    return p


algo(0,"Test",
     amp = 0.200,
     modDepth = 1.000,
     port = 1.000,
     vibrato = vibrato(freq = 5.000,
                       delay = 0.000,
                       sens = 0.100,
                       depth = 0.000),
     stackA = stack("A", enable = True, amp = 1.000,
                    break_key = 60,
                    feedback = 0.000,
                    fb_env = 0.000,
                    fb_lfo = 0.000,
                    lfo_ratio = 1.000,
                    lfo_delay = 0.000,
                    lfo_wave = 0.500),
     stackB = stack("B", enable = True, amp = 1.000,
                    break_key = 60,
                    feedback = 0.000,
                    fb_env = 0.000,
                    fb_lfo = 0.000,
                    lfo_ratio = 1.000,
                    lfo_delay = 0.000,
                    lfo_wave = 0.500),
     stackC = stack("C", enable = True, amp = 1.000,
                    break_key = 60,
                    feedback = 0.000,
                    fb_env = 0.000,
                    fb_lfo = 0.000,
                    lfo_ratio = 1.000,
                    lfo_delay = 0.000,
                    lfo_wave = 0.500),
     env1 = env(1, 1.0000, 0.000, 0.000, 1.000,
                breakpoint = 1.000, sustain = 1.000, mode = 0),
     env2 = env(2, 0.0000, 0.000, 0.000, 0.000,
                breakpoint = 1.000, sustain = 1.000, mode = 0),
     env3 = env(3, 0.0000, 0.000, 0.000, 0.000,
                breakpoint = 1.000, sustain = 1.000, mode = 0),
     env4 = env(4, 0.0000, 0.000, 0.000, 0.000,
                breakpoint = 1.000, sustain = 1.000, mode = 0),
     env5 = env(5, 0.0000, 0.000, 0.000, 0.000,
                breakpoint = 1.000, sustain = 1.000, mode = 0),
     env6 = env(6, 0.0000, 0.000, 0.000, 0.000,
                breakpoint = 1.000, sustain = 1.000, mode = 0),
     env7 = env(7, 0.0000, 0.000, 0.000, 0.000,
                breakpoint = 1.000, sustain = 1.000, mode = 0),
     env8 = env(8, 0.0000, 0.000, 0.000, 0.000,
                breakpoint = 1.000, sustain = 1.000, mode = 0),
     op1 = op(1, ratio = 1.000, bias = 0.000,
              left = 0, right = 0,
              velocity = 0.000, lfo = 0.000, external = 0.000),
     op2 = op(2, ratio = 1.000, bias = 0.000, amp = 1.000, mod_scale = 1,
              left = 0, right = 0,
              velocity = 0.000, lfo = 0.000, external = 0.000),
     op3 = op(3, ratio = 1.000, bias = 0.000, amp = 1.000, mod_scale = 1,
              left = 0, right = 0,
              velocity = 0.000, lfo = 0.000, external = 0.000),
     op4 = op(4, ratio = 1.000, bias = 0.000, amp = 1.000, mod_scale = 1,
              left = 0, right = 0,
              velocity = 0.000, lfo = 0.000, external = 0.000),
     op5 = op(5, ratio = 1.000, bias = 0.000,
              left = 0, right = 0,
              velocity = 0.000, lfo = 0.000, external = 0.000),
     op6 = op(6, ratio = 1.000, bias = 0.000, amp = 1.000, mod_scale = 1,
              left = 0, right = 0,
              velocity = 0.000, lfo = 0.000, external = 0.000),
     op7 = op(7, ratio = 1.000, bias = 0.000,
              left = 0, right = 0,
              velocity = 0.000, lfo = 0.000, external = 0.000),
     op8 = op(8, ratio = 1.000, bias = 0.000, amp = 1.000, mod_scale = 1,
              left = 0, right = 0,
              velocity = 0.000, lfo = 0.000, external = 0.000))
   

    
