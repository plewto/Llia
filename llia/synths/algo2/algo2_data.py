# llia.synths.algo2.algo2_data


from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.util.lmath import clip, db_to_amp
from llia.performance_edit import performance
import llia.synths.algo2.algo2_constants as con

prototype = {
    "amp" : 0.2,              # Main linear amp 
    "port" : 0.00,            # portamento time (0..1)
    "x_pitch" : 0.00,         # external -> pitch (0..1)
    "x_scale" : 1.0,          # (-4..+4)
    "x_bias" : 0.0,           # (-4..+4)
    
    "lfo_freq": 1.00,         # (0.01 ... 100)
    "lfo_ratio" : 2.00,       # See constants
    "lfo_mix" : 1.00,         # (0..1)
    "lfo_delay" : 0.00,       # (0..4) seconds
    "lfo_depth" : 0.00,       # (0..1)
    "vsens" : 0.01,           # (0..1)
    "vdepth" : 0.00,          # (0..1) programmed vibrato
    
    "enva_attack" : 0.0,      # Envelope A 
    "enva_decay1" : 0.0,
    "enva_decay2" : 0.0,
    "enva_release" : 0.0,
    "enva_breakpoint" : 1.0,
    "enva_sustain" : 1.0,

    "envb_attack" : 0.0,      # Envelope B 
    "envb_decay1" : 0.0,
    "envb_decay2" : 0.0,
    "envb_release" : 0.0,
    "envb_breakpoint" : 1.0,
    "envb_sustain" : 1.0,
    "envc_attack" : 0.0,      # Envelope C 
    "envc_decay1" : 0.0,
    "envc_decay2" : 0.0,
    "envc_release" : 0.0,
    "envc_breakpoint" : 1.0,
    "envc_sustain" : 1.0,
    "envd_attack" : 0.0,      # Envelope D 
    "envd_decay1" : 0.0,
    "envd_decay2" : 0.0,
    "envd_release" : 0.0,
    "envd_breakpoint" : 1.0,
    "envd_sustain" : 1.0,
    
    "op1_ratio" : 1.0,        # OP1 (carrier)
    "op1_amp" : 1.00,         # linear amp
    "op1_enable" : 1.0,       # 0 -> disable  1-> enable
    "op1_x_amp" : 0.00,       # (0..1)
    "op1_break_key" : 60,     # MIDI key number
    "op1_left_scale" : 6,     # DB per octave (-12..+12)
    "op1_right_scale" : -3,   # DB per octave (-12..+12)
    "op1_lfo_amp" : 0.0,      # (0..1)
    "op1_env_select" : 0.0,   # (0..7)
                              #        0..3 --> A B C D gated
                              #        4..7 --> A B C D triggerd
                              # 
    "op4_ratio" : 1.00,       # OP4 (carrier)
    "op4_amp" : 1.00,
    "op4_enable" : 1,
    "op4_x_amp" : 0.00,
    "op4_break_key" : 60,
    "op4_left_scale" : 0,
    "op4_right_scale" : 0,
    "op4_lfo_amp" : 0.0,
    "op4_env_select" : 0.0,
    "op7_ratio" : 1.00,       # OP7 (carrier)
    "op7_amp" : 1.00,
    "op7_enable" : 1,
    "op7_x_amp" : 0.00,
    "op7_break_key" : 60,
    "op7_left_scale" : 0,
    "op7_right_scale" : 0,
    "op7_lfo_amp" : 0.0,
    "op7_env_select" : 0,

    "op2_ratio" : 1.00,       # OP2 (Modulator) [2]-->[1]
    "op2_bias" : 0.00,
    "op2_amp" : 1.00,
    "op2_enable" : 1,
    "op2_x_amp" : 0.00,
    "op2_break_key" : 60,
    "op2_left_scale" : 0,
    "op2_right_scale" : 0,
    "op2_lfo_amp" : 0.0,
    "op2_env_select" : 0.0,
    "op3_ratio" : 1.00,       # OP3 (Modulator) [3]-->[1]
    "op3_bias" : 0.00,        # (0..299) Hertz
    "op3_amp" : 1.00,
    "op3_enable" : 1,
    "op3_x_amp" : 0.00,
    "op3_break_key" : 60,
    "op3_left_scale" : 0,
    "op3_right_scale" : 0,
    "op3_lfo_amp" : 0.0,
    "op3_env_select" : 0,     # (0..15)
                              #         0..3   -> A B C D  gated
                              #         4..7   -> A B C D  triggerd
                              #         8..11  -> A B C D  gated inverted
                              #        12..15 -> A B C D  triggerd inverted

                              
    "op5_ratio" : 1.00,       # OP5 (Modulator) [5]-->[4]
    "op5_bias" : 0.00,
    "op5_amp" : 1.00,
    "op5_enable" : 1.0,
    "op5_x_amp" : 0.00,
    "op5_break_key" : 60,
    "op5_left_scale" : 0,
    "op5_right_scale" : 0,
    "op5_lfo_amp" : 0.0,
    "op5_env_select" : 0,
    "op6_ratio" : 1.00,       # OP6 (Modulator) [6]-->[4]
    "op6_bias" : 0.00,        
    "op6_amp" : 1.00,
    "op6_enable" : 1,
    "op6_x_amp" : 0.00,
    "op6_break_key" : 60,
    "op6_left_scale" : 0,
    "op6_right_scale" : 0,
    "op6_lfo_amp" : 0.0,
    "op6_feedback" : 0.0,     # (0..3)
    "op6_env_feedback" : 0.0, # (0..1)
    "op6_lfo_feedback" : 0.0, # (0..1)
    "op6_x_feedback" : 0.00,  # (0..1)
    "op6_env_select" : 0,
    "op8_ratio" : 1.00,       # OP8 (Modulator) [8]-->[7]
    "op8_bias" : 0.00,        # With feedback
    "op8_amp" : 1.00,
    "op8_enable" : 1,
    "op8_x_amp" : 0.00,
    "op8_break_key" : 60,
    "op8_left_scale" : 0,
    "op8_right_scale" : 0,
    "op8_lfo_amp" : 0.0,
    "op8_feedback" : 0.0,
    "op8_env_feedback" : 0.0,
    "op8_lfo_feedback" : 0.0,
    "op8_x_feedback" : 0.00,
    "op8_env_select" : 0}

class Algo2(Program):

    def __init__(self, name):
        super(Algo2, self).__init__(name, "Algo2", prototype)

program_bank = ProgramBank(Algo2("Init"))
program_bank.enable_undo = False



def _fill_external_params(d):
    acc = {}
    acc["x_pitch"] = float(d.get("pitch", 0))
    acc["x_scale"] = float(d.get("scale", 1))
    acc["x_bias"] = float(d.get( "bias", 0))
    return acc

def _fill_lfo_params(d):
    acc = {}
    acc["lfo_freq"] = float(d.get( "freq", 5.0))
    acc["lfo_ratio"] = float(d.get( "ratio", 2.0))
    acc["lfo_mix"] = float(d.get( "mix", 0.5))
    acc["lfo_delay"] = float(d.get( "delay", 0))
    acc["lfo_depth"] = float(d.get( "depth", 1))
    acc["vsens"] = float(d.get("vsens", 0.01))
    acc["vdepth"] = float(d.get( "vdepth", 0.0))
    return acc

def _fill_envelope(prefix, d):
    acc = {}
    def fval(key, dflt):
        v = max(0, float(d.get(key, dflt)))
        param = "env%s_%s" % (prefix, key)
        acc[param] = v
    fval("attack", 0)
    fval("decay1", 0)
    fval("decay2", 0)
    fval("release", 0)
    fval("brteakpoint", 1)
    fval("sustain", 1)
    return acc
    
def _fill_carrier(prefix, d):
    acc = {}
    def fval(key, dflt):
        return float(d.get(key,dflt))
    def ival(key, dflt):
        return int(d.get(key,dflt))
    acc["op%s_ratio" % prefix] = fval("ratio", 1)
    acc["op%s_amp" % prefix] = float(db_to_amp(ival("amp", 0)))
    if ival("enable", 1):
        enable = 1
    else:
        enable = 0
    acc["op%s_enable" % prefix] = enable
    acc["op%s_x_amp" % prefix] = fval("x", 0)
    acc["op%s_lfo_amp" % prefix] = fval("lfo", 0)
    acc["op%s_break_key" % prefix] = clip(ival("break-key", 60), 0, 127)
    acc["op%s_left_scale" % prefix] = ival("left-scale", 0)
    acc["op%s_right_scale" % prefix] = ival("right-scale", 0)
    env = clip(ival("env", 0), 0, 3)
    acc["op%s_env_select"] = env
    return acc


def _fill_modulator(prefix, d):
    acc = {}
    def fval(key, dflt):
        return float(d.get(key,dflt))
    def ival(key, dflt):
        return int(d.get(key, dflt))
    acc["op%s_ratio" % prefix] = fval("ratio", 1)
    acc["op%s_amp" % prefix] = float(db_to_amp(ival("amp", 0)))
    if ival("enable", 1):
        enable = 1
    else:
        enable = 0
    acc["op%s_enable" % prefix] = enable
    acc["op%s_x_amp" % prefix] = fval("x", 0)
    acc["op%s_lfo_amp" % prefix] = fval("lfo", 0)
    acc["op%s_break_key" % prefix] = clip(ival("break-key", 60), 0, 127)
    acc["op%s_left_scale" % prefix] = ival("left-scale", 0)
    acc["op%s_right_scale" % prefix] = ival("right-scale", 0)
    env = clip(ival("env", 0), 0, 7)
    acc["op%s_env_select"] = env
    acc["op%s_bias" % prefix] = clip(fval("bias",0), 0, con.MAX_OSC_BIAS_FREQUENCY)
    if prefix == 6 or prefix == 8:
        acc["op%s_feedback" % prefix] = fval("feedback", 0)
        acc["op%s_env_feedback" % prefix] = fval("env->feedback", 0)
        acc["op%s_lfo_feedback" % prefix] = fval("lfo->feedback", 0)
        acc["op%s_x_feedback" % prefix] = fval("x->feedback", 0)
    return acc


                                 


def algo2(slot, name, amp=-12, port = 0.00,
          external = {
              "pitch" : 0.0,
              "scale" : 1.0,
              "bias" : 0.0},
          lfo = {
              "freq" : 1.0,
              "ratio" : 2.0,
              "mix" : 0.0,
              "delay" : 0.0,
              "depth" : 1.0,
              "vsens" : 0.01,
              "vdepth" : 0.0},
          enva = {
              "attack" : 0.0,
              "decay1" : 0.0,
              "decay2" : 0.0,
              "release" : 0.0,
              "breakpoint" : 1.0,
              "sustain" : 1.0},
          envb = {
              "attack" : 0.0,
              "decay1" : 0.0,
              "decay2" : 0.0,
              "release" : 0.0,
              "breakpoint" : 1.0,
              "sustain" : 1.0},
          envc = {
              "attack" : 0.0,
              "decay1" : 0.0,
              "decay2" : 0.0,
              "release" : 0.0,
              "breakpoint" : 1.0,
              "sustain" : 1.0},
          envd = {
              "attack" : 0.0,
              "decay1" : 0.0,
              "decay2" : 0.0,
              "release" : 0.0,
              "breakpoint" : 1.0,
              "sustain" : 1.0},
          op1 = {
              "ratio" : 1.0,
              "amp" : 0,
              "enable" : 1,
              "x" : 0.0,
              "lfo" : 0.0,
              "break-key" : 60,
              "left-scale" : 0,
              "right-scale" : 0,
              "env" : 0},
          op4 = {
              "ratio" : 1.0,
              "amp" : 0,
              "enable" : 1,
              "x" : 0.0,
              "lfo" : 0.0,
              "break-key" : 60,
              "left-scale" : 0,
              "right-scale" : 0,
              "env" : 0},
          op7 = {
              "ratio" : 1.0,
              "amp" : 0,
              "enable" : 1,
              "x" : 0.0,
              "lfo" : 0.0,
              "break-key" : 60,
              "left-scale" : 0,
              "right-scale" : 0,
              "env" : 0},
          op3 = {
              "ratio" : 1.0,
              "bias" : 0,
              "amp" : 0.0,
              "enable" : 1,
              "x" : 0.0,
              "lfo" : 0.0,
              "break-key" : 60,
              "left-scale" : 0,
              "right-scale" : 0,
              "env" :0},
          op2 = {
              "ratio" : 1.0,
              "bias" : 0,
              "amp" : 0.0,
              "enable" : 1,
              "x" : 0.0,
              "lfo" : 0.0,
              "break-key" : 60,
              "left-scale" : 0,
              "right-scale" : 0,
              "env" :0},
          op5 = {
              "ratio" : 1.0,
              "bias" : 0,
              "amp" : 0.0,
              "enable" : 1,
              "x" : 0.0,
              "lfo" : 0.0,
              "break-key" : 60,
              "left-scale" : 0,
              "right-scale" : 0,
              "env" :0},
          op6 = {
              "ratio" : 1.0,
              "bias" : 0,
              "amp" : 0.0,
              "enable" : 1,
              "x" : 0.0,
              "lfo" : 0.0,
              "break-key" : 60,
              "left-scale" : 0,
              "right-scale" : 0,
              "env" : 0,
              "feedback" : 0.0,
              "env->feedbac" : 0.0,
              "lfo->feedback" : 0.0,
              "x->feedback" : 0.0},
          op8 = {
              "ratio" : 1.0,
              "bias" : 0,
              "amp" : 0.0,
              "enable" : 1,
              "x" : 0.0,
              "lfo" : 0.0,
              "break-key" : 60,
              "left-scale" : 0,
              "right-scale" : 0,
              "env" : 0,
              "feedback" : 0.0,
              "env->feedbac" : 0.0,
              "lfo->feedback" : 0.0,
              "x->feedback" : 0.0}):
    acc = _fill_external_params(external)
    acc.update(_fill_lfo_params(lfo))
    acc.update(_fill_envelope("a", enva))
    acc.update(_fill_envelope("b", envb))
    acc.update(_fill_envelope("c", envc))
    acc.update(_fill_envelope("d", envd))
    acc.update(_fill_carrier(1, op1))
    acc.update(_fill_carrier(4, op4))
    acc.update(_fill_carrier(7, op7))
    acc.update(_fill_modulator(3, op3))
    acc.update(_fill_modulator(2, op2))
    acc.update(_fill_modulator(5, op5))
    acc.update(_fill_modulator(6, op6))
    acc.update(_fill_modulator(8, op8))
    acc["amp"] = float(db_to_amp(amp))
    acc["port"] = float(port)
    p = Algo2(name)
    for param,value in acc.items():
        p[param] = value
    program_bank[slot] = p
    return p
   
 

algo2(0, "Random0", amp=-12, port=0.000,
      external = {
          "pitch" : 0.000,
          "scale" : 1.000,
          "bias"  : 0.000},
      lfo = {
          "freq"   : 2.019,
          "ratio"  : 1.000,
          "mix"    : 0.000,
          "delay"  : 1.622,
          "depth"  : 0.795,
          "vsens"  : 0.003,
          "vdepth" : 0.171},
      enva = {
          "attack"     : 0.012,
          "decay1"     : 0.889,
          "decay2"     : 6.994,
          "release"    : 0.233,
          "breakpoint" : 1.000,
          "sustain"    : 0.540},
      envb = {
          "attack"     : 0.423,
          "decay1"     : 0.604,
          "decay2"     : 0.065,
          "release"    : 0.479,
          "breakpoint" : 1.000,
          "sustain"    : 0.582},
      envc = {
          "attack"     : 0.911,
          "decay1"     : 0.400,
          "decay2"     : 0.630,
          "release"    : 0.108,
          "breakpoint" : 1.000,
          "sustain"    : 0.691},
      envd = {
          "attack"     : 0.070,
          "decay1"     : 0.850,
          "decay2"     : 0.581,
          "release"    : 0.863,
          "breakpoint" : 1.000,
          "sustain"    : 0.967},
      op1 = {
          "ratio"  : 35.9863,
          "amp"    : -6,
          "enable" : 1,
          "x"      : 0.000,
          "lfo"    : 0.000,
          "break-key"   : 60,
          "left-scale"  : -99,
          "right-scale" : 9,
          "env"         : 0},
      op4 = {
          "ratio"  : 0.2500,
          "amp"    : 0,
          "enable" : 1,
          "x"      : 0.000,
          "lfo"    : 0.000,
          "break-key"   : 60,
          "left-scale"  : -99,
          "right-scale" : 9,
          "env"         : 0},
      op7 = {
          "ratio"  : 1.0000,
          "amp"    : 0,
          "enable" : 1,
          "x"      : 0.000,
          "lfo"    : 0.000,
          "break-key"   : 60,
          "left-scale"  : -99,
          "right-scale" : 9,
          "env"         : 0},
      op3 = {
          "ratio"  : 1.0000,
          "bias"   : 0,
          "amp"    : 1,
          "enable" : 1,
          "x"      : 0.000,
          "lfo"    : 0.000,
          "break-key"   : 60,
          "left-scale"  : -99,
          "right-scale" : 9,
          "env"         : 0},
      op2 = {
          "ratio"  : 0.5625,
          "bias"   : 0,
          "amp"    : 1,
          "enable" : 1,
          "x"      : 0.000,
          "lfo"    : 0.135,
          "break-key"   : 60,
          "left-scale"  : -99,
          "right-scale" : 9,
          "env"         : 0},
      op5 = {
          "ratio"  : 8.9697,
          "bias"   : 0,
          "amp"    : 1,
          "enable" : 1,
          "x"      : 0.000,
          "lfo"    : 0.000,
          "break-key"   : 60,
          "left-scale"  : -99,
          "right-scale" : 9,
          "env"         : 0},
      op6 = {
          "ratio"  : 64.0000,
          "bias"   : 2,
          "amp"    : 1,
          "enable" : 1,
          "x"      : 0.000,
          "lfo"    : 0.000,
          "break-key"   : 60,
          "left-scale"  : -99,
          "right-scale" : 9,
          "env"         : 0,
          "feedback"       : 0.000,
          "env->feedback" : 0.000,
          "lfo->feedback" : 0.000,
          "x->feedback"   : 0.000},
      op8 = {
          "ratio"  : 64.0000,
          "bias"   : 0,
          "amp"    : 1,
          "enable" : 1,
          "x"      : 0.000,
          "lfo"    : 0.000,
          "break-key"   : 60,
          "left-scale"  : -99,
          "right-scale" : 9,
          "env"         : 0,
          "feedback"      : 0.000,
          "env->feedback" : 0.000,
          "lfo->feedback" : 0.000,
          "x->feedback"   : 0.000})

algo2(1, "Random1", amp=-12, port=0.000,
      external = {
          "pitch" : 0.000,
          "scale" : 1.000,
          "bias"  : 0.000},
      lfo = {
          "freq"   : 6.499,
          "ratio"  : 3.000,
          "mix"    : 0.000,
          "delay"  : 3.090,
          "depth"  : 0.615,
          "vsens"  : 0.006,
          "vdepth" : 0.094},
      enva = {
          "attack"     : 0.002,
          "decay1"     : 0.231,
          "decay2"     : 0.407,
          "release"    : 0.141,
          "breakpoint" : 1.000,
          "sustain"    : 0.769},
      envb = {
          "attack"     : 0.689,
          "decay1"     : 0.821,
          "decay2"     : 0.473,
          "release"    : 0.119,
          "breakpoint" : 1.000,
          "sustain"    : 0.670},
      envc = {
          "attack"     : 0.713,
          "decay1"     : 0.406,
          "decay2"     : 0.974,
          "release"    : 4.574,
          "breakpoint" : 1.000,
          "sustain"    : 0.993},
      envd = {
          "attack"     : 0.347,
          "decay1"     : 1.887,
          "decay2"     : 0.019,
          "release"    : 0.528,
          "breakpoint" : 1.000,
          "sustain"    : 0.513},
      op1 = {
          "ratio"  : 15.9912,
          "amp"    : 0,
          "enable" : 1,
          "x"      : 0.000,
          "lfo"    : 0.000,
          "break-key"   : 60,
          "left-scale"  : -99,
          "right-scale" : 9,
          "env"         : 0},
      op4 = {
          "ratio"  : 24.9192,
          "amp"    : 0,
          "enable" : 1,
          "x"      : 0.000,
          "lfo"    : 0.000,
          "break-key"   : 60,
          "left-scale"  : -99,
          "right-scale" : 9,
          "env"         : 0},
      op7 = {
          "ratio"  : 3.9870,
          "amp"    : 0,
          "enable" : 1,
          "x"      : 0.000,
          "lfo"    : 0.000,
          "break-key"   : 60,
          "left-scale"  : -99,
          "right-scale" : 9,
          "env"         : 0},
      op3 = {
          "ratio"  : 4.0000,
          "bias"   : 0,
          "amp"    : 1,
          "enable" : 1,
          "x"      : 0.000,
          "lfo"    : 0.933,
          "break-key"   : 60,
          "left-scale"  : -99,
          "right-scale" : 9,
          "env"         : 0},
      op2 = {
          "ratio"  : 64.0000,
          "bias"   : 0,
          "amp"    : 1,
          "enable" : 0,
          "x"      : 0.000,
          "lfo"    : 0.000,
          "break-key"   : 60,
          "left-scale"  : -99,
          "right-scale" : 9,
          "env"         : 0},
      op5 = {
          "ratio"  : 1.0000,
          "bias"   : 0,
          "amp"    : 1,
          "enable" : 1,
          "x"      : 0.000,
          "lfo"    : 0.000,
          "break-key"   : 60,
          "left-scale"  : -99,
          "right-scale" : 9,
          "env"         : 0},
      op6 = {
          "ratio"  : 0.9979,
          "bias"   : 0,
          "amp"    : 1,
          "enable" : 1,
          "x"      : 0.000,
          "lfo"    : 0.000,
          "break-key"   : 60,
          "left-scale"  : -99,
          "right-scale" : 9,
          "env"         : 0,
          "feedback"      : 0.000,
          "env->feedback" : 0.000,
          "lfo->feedback" : 0.000,
          "x->feedback"   : 0.000},
      op8 = {
          "ratio"  : 0.2500,
          "bias"   : 0,
          "amp"    : 1,
          "enable" : 1,
          "x"      : 0.000,
          "lfo"    : 0.963,
          "break-key"   : 60,
          "left-scale"  : -99,
          "right-scale" : 9,
          "env"         : 0,
          "feedback"      : 0.000,
          "env->feedback" : 0.723,
          "lfo->feedback" : 0.000,
          "x->feedback"   : 0.000})

