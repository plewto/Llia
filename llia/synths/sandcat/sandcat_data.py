# llia.synths.Sandcat.Sandcat_data

from __future__ import print_function
from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance
from llia.synths.sandcat.sandcat_constants import *


prototype = {
    "amp" : 1.0,              # 0..2
    "vfreq" : 7.0,            # 0..100
    "vdelay" : 0.0,           # 0..2
    "vdepth" : 0.0,           # 0..1 (Programed)
    "vibrato" : 0.0,          # 0..1 (Manual)
    "vsens" : 0.1,            # 0..1
    "vxbus1" : 0.0,           # 0..1
    "lfo1_ratio" : 1.0,       # 0..4?
    "lfo1_freq_lfo2" : 0,     # 0..4? (potential feedback)
    "lfo2_ratio" : 1.0,       # 0..4?
    "lfo2_freq_lfo1" : 0,     # 0..4? (potential feedback)
    "clk1_ratio" : 1,         # 0..4?
    "clk2_ratio" : 1,         # 0..4?
    "env1_attack" : 0.01,     # 0..8
    "env1_decay" : 0.0,       # 0..8
    "env1_sustain" : 1.0,     # 0..1
    "env1_release" : 1.0,     # 0..8
    "env1_trig_src" : 0,      # 0,1,2,... (see constants)
    "env1_trig_mode" : 0,     # 0|1  0=gate, 1=trig
    "env2_attack" : 0.01,
    "env2_decay" : 0.0,
    "env2_sustain" : 1.0,
    "env2_release" : 1.0,
    "env2_trig_src" : 0,
    "env2_trig_mode" : 0,
    "env3_attack" : 0.01,
    "env3_decay" : 0.0,
    "env3_sustain" : 1.0,
    "env3_release" : 1.0,
    "env3_trig_src" : 0,
    "env3_trig_mode" : 0,
    "env4_attack" : 0.01,
    "env4_decay" : 0.0,
    "env4_sustain" : 1.0,
    "env4_release" : 1.0,
    "env4_trig_src" : 0,
    "env4_trig_mode" : 0,
    "ex1_harmonic" : 1,       # 1,2,3,...,8
    "ex1_lfo1" : 0,           # 1,2,3,...,8
    "ex1_env1" : 0,           # -8,-7.-6,...,6,7,8
    "ex1_pw" : 0.5,           # 0..1
    "ex1_pw_lfo1" : 0,        # 0..1
    "ex1_noise_select" : 0,   # 0|1  0=white, 1=pink
    "ex1_source_mix" : 0,     # -1..+1 -1=pulse +1=noise
    "ex2_harmonic" : 1,
    "ex2_lfo2" : 0,
    "ex2_env2" : 0,
    "ex2_pw" : 0.5,
    "ex2_pw_lfo2" : 0,
    "ex2_noise_select" : 0,
    "ex2_source_mix" : 0,
    "ks1_trig_src" : 0,       # 0,1,2,...
    "ks2_trig_src" : 0,       # 0,1,2,...
    "ks1_ratio" : 1,          # 0..16
    "ks1_decay" : 2,          # 0..8
    "ks1_coef" : 0.3,         # 0..1  KS feedback coeficient
    "ks1_velocity" : 0,       # 0..1
    "ks2_ratio" : 1,
    "ks2_decay" : 2,
    "ks2_coef" : 0.3,
    "ks2_velocity" : 0,
    "stack1_break_key" : 60,  # 0..127  MIDI key number
    "stack1_fb" : 0.0,        # 0..?
    "stack1_fb_lfo1" : 0.0,   # 0..1   LFO -> feedback 
    "mod1_ratio" : 1.0,       # 0..16  modulator freq ratio
    "mod1_bias" : 0.0,        # 0..1k
    "mod1_ks1" : 0.0,         # 0..?  ks1 -> FM mod depth
    "mod1_env1" : 1,          # 0..1  env1 -> mod amp
    "mod1_lag" : 0.0,         # 0..1  lag on env
    "mod1_lfo1" : 0.0,        # 0..1  LFO1 -> mod amp
    "mod1_velocity" : 0.0,    # 0..1  velocity -> mod amp
    "mod1_left_scale" : 0,    # key scales (see constants)
    "mod1_right_scale" : 0,   
    "car1_ratio" : 1.0,       # 0..16 carrier freq ratio
    "car1_bias" : 0.0,        # 0..1k
    "car1_mod1": 0.0,         # 0..?  mod1 -> car1
    "car1_ks1" : 0.0,         # 0..?  ks1  -> car1
    "car1_env_mode": 0,       # 0|1   0=env1, 1=gate
    "car1_lfo1":0,            # 0..1  lfo1 -> car1 amp
    "car1_velocity": 0,       # 0..1  velocity -> car1 amp
    "car1_left_scale":0,      # key scales (see constants)
    "car1_right_scale":0,
    "stack2_break_key" : 60,
    "stack2_fb" : 0.0,
    "stack2_fb_lfo2" : 0.0,
    "mod2_ratio" : 1.0,
    "mod2_bias" : 0.0,
    "mod2_ks2" : 0.0,
    "mod2_env2" : 1,
    "mod2_lag" : 0.0,
    "mod2_lfo2" : 0.0,
    "mod2_velocity" : 0.0,
    "mod2_left_scale" : 0,
    "mod2_right_scale" : 0,
    "car2_ratio" : 1.0,
    "car2_bias" : 0.0,
    "car2_mod1":0.0,          # 0..? mod1 -> car2
    "car2_mod2": 0.0,         # 0..? mod2 -> car2
    "car2_ks2" : 0.0,         # 0..? ks2 -> car2
    "car2_env_mode": 0,
    "car2_lfo2":0,
    "car2_velocity": 0,
    "car2_left_scale":0,
    "car2_right_scale":0,
    "ks1_amp" : 1.0,          # 0..2 ks1 linear amp
    "ks2_amp" : 1.0,          # 0..2 ks2 linear amp
    "stack1_amp" : 1.0,       # 0..2 stack 1 (mod1+car1) linear amp
    "stack2_amp" : 1.0,       # 0..2 stack 2 (mod2+car2) lineara amp
    "ks1_pan" : 0.0,          # -1..+1 pan (filter select)
    "ks2_pan" : 0.0,
    "stack1_pan" : 0.0,
    "stack2_pan" : 0.0,
    "f1_cutoff" : 16000,      # Filter cutoff in Hz.
    "f1_track" : 0.0,         # Filter key track -4..4
    "f1_env1" : 0,            # env1 -> filter in Hz
    "f1_env3" : 0,            # env3 -> filter in Hz
    "f1_lfo1" : 0,            # LFO1 -> filter in Hz
    "f1_lfov" : 0,            # LFOV (vibrato) -> filter in Hz
    "f1_velocity" : 0,        # velocity -> filter in Hz
    "f1_res" : 0,             # 0..1 filter resonance 
    "f1_pan" : 0,             # -1..+1 filter 1 output pan
    "f2_cutoff" : 16000,
    "f2_track" : 0,
    "f2_env4" : 0,
    "f2_lfo2" : 0,
    "f2_lfov" : 0,
    "f2_velocity" : 0,
    "f2_res" : 0,
    "f2_pan" : 0}


class Sandcat(Program):

    def __init__(self,name):
        super(Sandcat,self).__init__(name,Sandcat,prototype)
        self.performance = performance()
program_bank = ProgramBank(Sandcat("Init"))


def fval(f):
    return round(float(f),4)

def vibrato(freq=7.0,delay=0.0,sens=0.1,depth=0.0,x1=0.0):
    return {"vfreq": fval(freq),
            "vdelay": fval(delay),
            "vsens": fval(sens),
            "vdepth": fval(depth),
            "vxbus1": fval(x1)}

def lfo(n,ratio=1.0,xmod=0.0):
    pratio = "lfo%d_ratio" % n
    if n==1:
        pxmod = "lfo1_freq_lfo2"
    else:
        pxmod = "lfo2_freq_lfo1"
    return {pratio : fval(ratio),
            pxmod : fval(xmod)}

def clock(n, ratio=0.1):
    param = "clk%d_ratio" % n
    return {param : float(ratio)}

def adsr(n,a,d,s,r,src=0,mode=0):
    def param(suffix):
        return "env%d_%s" % (n,suffix)
    return {param("attack") : fval(a),
            param("decay") : fval(d),
            param("sustain") : fval(s),
            param("release") : fval(r),
            param("trig_src") : int(src),
            param("trig_mode") : int(mode)}
                  
def excite(n, harmonic=1, lfo=0, env=0, pw=0.5, pwm=0.0, noise=0, mix=0):
    def param(suffix):
        return "ex%d_%s" % (n,suffix)
    lfo_param = param("lfo%d" % n)
    env_param = param("env%d" % n)
    pwm_param = param("pw_lfo%d" % n)
    return {param("harmonic") : int(harmonic),
            lfo_param : int(lfo),
            env_param : int(env),
            param("pw") : float(pw),
            pwm_param : float(pwm),
            param("noise_select") : int(noise),
            param("source_mix") : fval(mix)}


def pluck(n, ratio=1.0, decay=3, coef=0.5, trig=0, velocity=0.0):
    def param(suffix):
        return "ks%d_%s" % (n,suffix)
    return {param("ratio") : fval(ratio),
            param("decay") : fval(decay),
            param("coef") : fval(coef),
            param("trig_src") : int(trig),
            param("velocity") : fval(velocity)}

def stack(n, break_key=60, feedback=0.0, feedback_lfo = 0.0):
    def param(suffix):
        return "stack%d_%s" % (n,suffix)
    lfo = param("fb_lfo%d" % n)
    return {param("break_key") : int(break_key),
            param("fb") : float(feedback),
            lfo : float(feedback_lfo)}
        
def mod(n, ratio=1.0, bias=0.0, ks=0.0, env=1.0, lag=0.0, lfo=0.0,
              velocity=0.0, left=0, right=0):
    def param(suffix):
        return "mod%d_%s" % (n,suffix)
    param_ks = param("ks%d" % n)
    param_env = param("env%d" % n)
    param_lfo = param("lfo%d" % n)
    return {param("ratio") : fval(ratio),
            param("bias") : fval(bias),
            param_ks : fval(ks),
            param_env : fval(env),
            param_lfo : fval(lfo),
            param("lag") : fval(lag),
            param("velocity") : fval(velocity),
            param("left_scale") : int(left),
            param("right_scale") : int(right)}

def car(n, ratio=1.0, bias=0.0, mod1=0.0, mod2=0.0, ks=0.0,
        env_mode=0, lfo=0.0, velocity=0.0, left=0, right=0):
    def param(suffix):
        return "car%d_%s" % (n,suffix)
    rs = {param("ratio") : fval(ratio),
          param("bias") : fval(bias),
          param("ks%d" % n) : fval(ks),
          param("env_mode") : int(env_mode),
          param("lfo%d" % n) : fval(lfo),
          param("velocity") : fval(velocity),
          param("left_scale") : int(left),
          param("right_scale") : int(right),
          param("mod1") : fval(mod1)}
    if n==2:
        rs.update({param("mod2") : fval(mod2)})
    return rs
   
def mixer(ks1=1.0, ks2=1.0, stack1=1.0, stack2=1.0):
    return {"ks1_amp" : fval(ks1),
            "ks2_amp" : fval(ks2),
            "stack1_amp" : fval(stack1),
            "stack2_amp" : fval(stack2)}

def panner(ks1=1.0, ks2=1.0, stack1=1.0, stack2=1.0):
    return {"ks1_pan" : fval(ks1),
            "ks2_pan" : fval(ks2),
            "stack1_pan" : fval(stack1),
            "stack2_pan" : fval(stack2)}

def sandcat(slot, name, amp=0.1,
            vibrato=vibrato(freq=7.0,delay=0.0,sens=0.1,depth=0.0, x1=0.0),
            lfo1 = lfo(1, ratio=0.1, xmod=0.0),
            lfo2 = lfo(2, ratio=0.2, xmod=0.0),
            clk1 = clock(1, ratio=0.3),
            clk2 = clock(2, ratio=0.4),
            env1 = adsr(1, 0.01, 0.10, 1.00, 1.00, src=0, mode=0),
            env2 = adsr(2, 0.01, 0.10, 1.00, 1.00, src=0, mode=0),
            env3 = adsr(3, 0.01, 0.10, 1.00, 1.00, src=0, mode=0),
            env4 = adsr(4, 0.01, 0.10, 1.00, 1.00, src=0, mode=0),
            ex1 = excite(1, harmonic=1, lfo=0, env=0, pw=0.5, pwm=0.0,
                         noise=0, mix=0.0),
            ex2 = excite(2, harmonic=1, lfo=0, env=0, pw=0.5, pwm=0.0,
                         noise=0, mix=0.0),
            ks1 = pluck(1,ratio=1.0, decay=3.0, coef=0.5, trig=0, velocity=0.0),
            ks2 = pluck(2,ratio=2.0, decay=3.0, coef=0.5, trig=0, velocity=0.0),
            stack1 = stack(1, break_key=60, feedback=0.0, feedback_lfo=0.0),
            stack2 = stack(2, break_key=60, feedback=0.0, feedback_lfo=0.0),
            mod1 = mod(1, ratio=1.0, bias=0.0, ks=0.0, env=1.0, lag=0.0,
                       lfo=0.0, velocity=0.0, left=0, right=0),
            mod2 = mod(2, ratio=1.0, bias=0.0, ks=0.0, env=1.0, lag=0.0,
                       lfo=0.0, velocity=0.0, left=0, right=0),
            car1 = car(1, ratio=1.0, bias=0.0, mod1=1.0, ks=0.0,
                       env_mode=0, lfo=0.0, velocity=0.0, left=0, right=0),
            car2 = car(2, ratio=2.0, bias=0.0, mod1=0.0, mod2=1.0, ks=0.0,
                       env_mode=0, lfo=0.0, velocity=0.0, left=0, right=0),

            f1_cutoff=16000, f1_track=0.0, f1_env3=0,
            f1_lfo1=0, f1_lfov=0, f1_velocity=0, f1_res=0.0,f1_pan=0.0,

            f2_cutoff=16000, f2_track=0.0, f2_env4=0,
            f2_lfo2=0, f2_lfov=0, f2_velocity=0, f2_res=0.0,f2_pan=0.0,
            mixer = mixer(),
            panner = panner()):
    p = Sandcat(name)
    p["amp"] = fval(amp)
    p["f1_cutoff"] = int(f1_cutoff)
    p["f1_track"] = int(f1_track)
    p["f1_env3"] = int(f1_env3)
    p["f1_lfo1"] = int(f1_lfo1)
    p["f1_lfov"] = int(f1_lfov)
    p["f1_velocity"] = int(f1_velocity)
    p["f1_res"] = int(f1_res)
    p["f1_pan"] = int(f1_pan)

    p["f2_cutoff"] = int(f2_cutoff)
    p["f2_track"] = int(f2_track)
    p["f2_env4"] = int(f2_env4)
    p["f2_lfo2"] = int(f2_lfo2)
    p["f2_lfov"] = int(f2_lfov)
    p["f2_velocity"] = int(f2_velocity)
    p["f2_res"] = int(f2_res)
    p["f2_pan"] = int(f2_pan)
    p.update(vibrato)
    p.update(lfo1)
    p.update(lfo2)
    p.update(clk1)
    p.update(clk2)
    p.update(env1)
    p.update(env2)
    p.update(env3)
    p.update(env4)
    p.update(ex1)
    p.update(ex2)
    p.update(ks1)
    p.update(ks2)
    p.update(stack1)
    p.update(stack2)
    p.update(mod1)
    p.update(mod2)
    p.update(car1)
    p.update(car2)
    p.update(mixer)
    p.update(panner)
    program_bank[slot] = p
    return p

sandcat(0,"Init")



