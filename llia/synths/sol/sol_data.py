# llia.synths.Sol.Sol_data

from __future__ import print_function
from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance
from llia.synths.sol.sol_constants import *

prototype = {"port" : 0.0,                # Portamento time 0..1
             "amp" : 0.3,                 # Main output amp 0..2
             "timebase" : 7.00,           # Common LFO reference frequency 
             "vratio" : 1,                # Vibrato freq ratio.
             "vsens" : 0.1,               # Vibrato sensitivity 0..1
             "vdepth" : 0.0,              # Vibrato depth 0..1
             "vdelay" : 0.0,              # Vibrato onset delay in seconds
             "pitch_ctrlbus" : 0.0,       # Pitch mod by external control bus.
             "xlfo_ratio" : 1.0,          # XLFO freq ratio.
             "xlfo_wave" : 0.5,           # XLFO wave 0..1  saw/tri
             "xlfo_delay" : 0.0,          # XLFO onset delay in seconds
             "xenv_attack" : 0.0,         # XEnv ADSR
             "xenv_decay" : 0.0,          # 
             "xenv_sustain" : 0.0,        # 
             "xenv_release" : 0.0,        # 
             "xenv_lfo_trig" : 0,         # XEnv trig mode, 0=gate 1=XLFO
             "xpos" : 0.0,                # Initial x vector position (-1..+1)
             "xpos_xlfo" : 0.0,           # XLFO -> xvector (-1..+1)
             "xpos_xenv" : 0.0,           # XENV -> xvector (-1..+1)
             "xpos_vxbus" : 0.0,          # External x-bus -> xvector (-1..+1)
             "xamp" : 1.0,                # X Signal amp (0..2)
             "ylfo_ratio" : 1.0,          # Y vector parameters identical to X.
             "ylfo_wave" : 0.5,           # 
             "ylfo_delay" : 0.0,          # 
             "yenv_attack" : 0.0,         # 
             "yenv_decay" : 0.0,          # 
             "yenv_sustain" : 0.0,        # 
             "yenv_release" : 0.0,        # 
             "yenv_lfo_trig" : 0,         # 
             "ypos" : 0.0,                # 
             "ypos_ylfo" : 0.0,           # 
             "ypos_yenv" : 0.0,           # 
             "ypos_vybus": 0.0,           # 
             "yamp" : 1.0,                # 
             "alfo_ratio" : 1.0,          # ALFO freq ratio
             "alfo_delay" : 0.0,          # ALFO onset delay in seconds
             "blfo_ratio" : 1.0,          # BLFO freq ratio
             "blfo_delay" : 0.0,          # BLFO onset delay
             "aenv_attack" : 0.00,        # AENV ADSR
             "aenv_decay" : 0.00,         # 
             "aenv_sustain" : 1.00,       # 
             "aenv_release" : 0.00,       # 
             "aenv_lfo_trig" : 0,         # 0=gate 1=ALFO
             "benv_attack" : 0.00,        # BENV ADSR
             "benv_decay" : 0.00,         # 
             "benv_sustain" : 0.00,       # 
             "benv_release" : 0.00,       # 
             "benv_lfo_trig" : 0,         # 0=gate, 1=BLFO
             "cenv_attack" : 0.00,        # CEnv ADDSR (primary envelope)
             "cenv_decay1" : 0.00,        # 
             "cenv_decay2" : 0.00,        # 
             "cenv_release" : 0.00,       # 
             "cenv_breakpoint" : 1.0,     # 
             "cenv_sustain" : 1.0,        # 
             "cenv_trig_mode" : 0,        # 0=gate, 1=trig
             # OPA FM pair [mod]->[car] on x-xis
             "opa_mod_ratio" : 1.00,      # Modulator freq ratio
             "opa_mod_scale" : 1,         # Modulation depth scale.
             "opa_mod_depth" : 1.00,      # Modulation depth.
             "opa_mod_alfo" : 0.00,       # AENV -> mod depth
             "opa_mod_aenv" : 0.00,       # ALFO -> mod depth
             "opa_car_ratio" : 1.00,      # Carrier freq ratio
             "opa_car_bias" : 0.00,       # Carrier freq bias
             "opa_feedback" : 0.00,       # Feedback
             "opa_cross_feedback" : 0.00, # Feedback from OPB
             "opa_amp" : 1.0,             # OP amp
             # OPB FM pair [mod]->[car] on x-axis
             "opb_mod_ratio" : 1.00,      # OPB Parameters identical
             "opb_mod_scale" : 1,         # to OPA except BENV and 
             "opb_mod_depth" : 1.00,      # BLFO are used for modulation,
             "opb_mod_blfo" : 0.00,       # and cross-feedback is from 
             "opb_mod_benv" : 0.00,       # OPA
             "opb_car_ratio" : 1.00,
             "opb_car_bias" : 0.00,
             "opb_feedback" : 0.00,
             "opb_cross_feedback" : 0.00,
             "opb_amp" : 1.0,
             # OPC  Tri/Pulse/Saw/Noise source on y-axis
             "opc_saw_ratio" : 1.00,       # Saw(tri) freq ratio 
             "opc_pulse_ratio" : 0.50,     # Pulse freq ratio
             "opc_pulse_width" : 0.50,     # Initial pulse width
             "opc_pulse_width_alfo" : 0.0, # ALFO -> pulse width
             "opc_wave" : 0,               # Select wave 0..1 (tri,pulse,saw)
             "opc_wave_alfo" : 0.0,        # ALFO -> wave selection (-1..+1)
             "opc_wave_aenv" : 0.0,        # AENV -> wave selection (-1..+1)
             "opc_noise_amp" : 0.0,        # Noise amp
             "opc_filter_track" : 16,      # Filter track (relative to saw freq)
             "opc_filter_aenv" : 1,        # AENV -> filter track
             "opc_amp" : 1.0,              # OP amp
             # OPD Tri/Pulse/Saw/Noise  source on y-axis
             "opd_saw_ratio" : 1.00,       # OPD parameters identical to
             "opd_pulse_ratio" : 0.50,     # OPC except BLFO and BENV used
             "opd_pulse_width" : 0.50,     # for modulation sources.
             "opd_pulse_width_blfo" : 0.0,
             "opd_wave" : 0,
             "opd_wave_blfo" : 0.0,
             "opd_wave_benv" : 0.0,
             "opd_noise_amp" : 0.0,
             "opd_filter_track" : 16,
             "opd_filter_benv" : 1,
             "opd_amp" : 1.0,
             # x-axis filter (ops A & B)
             "xfilter_freq" : 16000,       # Initial cutoff in hz.
             "xfilter_track" : 0,          # key-number -> filter cutoff
             "xfilter_freq_aenv" : 0,      # AENV -> filter cutoff in hz
             "xfilter_freq_cenv" : 0,      # CENV -> filter cutoff 
             "xfilter_freq_alfo" : 0,      # ALFO -> filter cutoff
             "xfilter_freq_vlfo" : 0,      # VLFO -> filter cutoff (under vdepth control)
             "xfilter_res" : 0,            # Resonance (0..1)
             # y-axis filter (ops C & D)
             "yfilter_freq" : 16000,       # yfilter parameters identical
             "yfilter_track" : 0,          # to xfilter except BENV and 
             "yfilter_freq_benv" : 0,      # BLFO used for modulation sources.
             "yfilter_freq_cenv" : 0,
             "yfilter_freq_blfo" : 0,
             "yfilter_freq_vlfo" : 0,
             "yfilter_res" : 0}

class Sol(Program):

    def __init__(self,name):
        super(Sol,self).__init__(name,Sol,prototype)
        self.performance = performance()

program_bank = ProgramBank(Sol("Init"))
program_bank.enable_undo = False

def fval(f, mn=0,mx=1):
    return min(max(float(f),mn),mx)

def fill_list(src, template):
    acc = []
    for i,dflt in enumerate(template):
        try:
            val = float(src[i])
        except IndexError:
            val = float(dflt)
        acc.append(val)
    return acc

def vibrato(ratio=1.000,sens=0.01,depth=0.00,delay=0.00,extern=0.00):
    return {"vratio" : float(ratio),
            "vsens" : fval(sens),
            "vdepth" : fval(depth),
            "vdelay" : fval(delay,0,MAX_LFO_DELAY),
            "pitch_ctrlbus" : fval(extern)}

def vector(axis,pos=0.50,ratio=1.000,wave=0.50,delay=0.0,
           adsr = [0.000,0.000,1.000,0.000], trig=0,
           lfo_depth=0.00, env_depth=0.00,
           external = 0.00):
    a,d,s,r = fill_list(adsr,[0.0,0.0,1.0,0.0])
    return {"%slfo_ratio" % axis : float(ratio),
            "%slfo_wave" % axis : fval(wave),
            "%slfo_delay" % axis : fval(delay,0,MAX_LFO_DELAY),
            "%senv_attack" % axis : fval(a,0,MAX_ENV_SEGMENT_TIME),
            "%senv_decay" % axis : fval(d,0,MAX_ENV_SEGMENT_TIME),
            "%senv_sustain" % axis : fval(s),
            "%senv_release" % axis : fval(r,0,MAX_ENV_SEGMENT_TIME),
            "%senv_lfo_trig" % axis : int(trig),
            "%spos" % axis : fval(pos,-1,1),
            "%spos_%senv" % (axis,axis) : fval(env_depth,-1,1),
            "%spos_%slfo" % (axis,axis) : fval(lfo_depth,-1,1),
            "%spos_v%sbus" % (axis,axis) : fval(external,-1,1)}

def lfo(id,ratio=1.000,delay=0.000):
    return {"%slfo_ratio" % id : float(ratio),
            "%slfo_delay" % id : fval(delay,0,MAX_LFO_DELAY)}

def adsr(id, a=0.000, d=0.000, s=1.000, r=0.000, lfo_trig=0):
    return {"%senv_attack" % id : fval(a,0,MAX_ENV_SEGMENT_TIME),
            "%senv_decay" % id : fval(d,0,MAX_ENV_SEGMENT_TIME),
            "%senv_release" % id : fval(r,0,MAX_ENV_SEGMENT_TIME),
            "%senv_sustain" % id : fval(s),
            "%senv_lfo_trig" % id : int(lfo_trig)}

def addsr(a=0.000, d1=0.000, d2=0.000, r=0.000, bp=1.000, sus=1.000, trig=0):
    return {"cenv_attack" : fval(a,0,MAX_ENV_SEGMENT_TIME),
            "cenv_decay1" : fval(d1,0,MAX_ENV_SEGMENT_TIME),
            "cenv_decay2" : fval(d2,0,MAX_ENV_SEGMENT_TIME),
            "cenv_release" : fval(r,0,MAX_ENV_SEGMENT_TIME),
            "cenv_breakpoint" : fval(bp),
            "cenv_sustain" : fval(sus),
            "cenv_trig_mode" : int(trig)}

def fmop(op,mratio=1.0000,mscale=1,mdepth=0.000,lfo=0.000,env=0.000,
         cratio=1.000,cbias=0,feedback=0.000,cross_feedback=0.000,
         amp=1.000):
    return {"op%s_mod_ratio" % op : float(mratio),
            "op%s_mod_scale" % op : int(mscale),
            "op%s_mod_depth" % op : fval(mdepth),
            "op%s_mod_%slfo" % (op,op) : fval(lfo),
            "op%s_mod_%senv" % (op,op) : fval(env),
            "op%s_car_ratio" % op : float(cratio),
            "op%s_car_bias" % op : float(cbias),
            "op%s_feedback" % op : float(feedback),
            "op%s_cross_feedback" % op : float(cross_feedback),
            "op%s_amp" % op : fval(amp,0,2)}

def wvop(op,sratio=1.000,pratio=1.000,pw=0.50,pwm=0.00,
         wave=0.5, wave_lfo=0.00, wave_env=0.00,
         noise_amp = 0.00,
         filter_track=16, filter_env=0, amp=1.0):
    if op=="c":
        mod="a"
    else:
        mod="b"
    return {"op%s_saw_ratio" % op : float(sratio),
            "op%s_pulse_ratio" % op : float(pratio),
            "op%s_pulse_width" % op : fval(pw),
            "op%s_pulse_width_%slfo" % (op,mod) : fval(pwm),
            "op%s_wave" % op : fval(wave),
            "op%s_wave_%slfo" % (op,mod) : fval(wave_lfo,-1,1),
            "op%s_wave_%senv" % (op,mod) : fval(wave_env,-1,1),
            "op%s_noise_amp" % op : fval(noise_amp, 0, 2),
            "op%s_filter_track" % op : int(filter_track),
            "op%s_filter_%senv" % (op,mod) : int(filter_env),
            "op%s_amp" % op : fval(amp,0,2)}

def filter(id,freq=16000,track=0,env=0,cenv=0,lfo=0,vlfo=0,res=0.5,amp=1.0):
    if id=="x":
        mod="a"
    else:
        mod="b"
    return {"%sfilter_freq" % id : int(freq),
            "%sfilter_track" % id : int(track),
            "%sfilter_freq_%senv" % (id,mod) : int(env),
            "%sfilter_freq_cenv" % id : int(cenv),
            "%sfilter_freq_%slfo" % (id,mod) : int(lfo),
            "%sfilter_freq_vlfo" % id  : int(vlfo),
            "%sfilter_res" % id : fval(res),
            "%samp" % id : fval(amp,0,2)}

def sol(slot, name, amp=0.3000,
        port = 0.0000,
        timebase = 7.0000,
        vibrato = vibrato(ratio=1.000,sens=0.01,depth=0.00,
                          delay=0.0,extern=0),
        x = vector("x",pos=0.00,ratio=0.125,wave=0.5,delay=0.0,
                   adsr = [0.000, 0.000, 1.000, 0.000],
                   lfo_depth = 0.75, env_depth = 0.00, external = 0.00),
        y = vector("y",pos=0.00,ratio=0.25,wave=0.5,delay=0.0,
                   adsr = [0.000, 0.000, 1.000, 0.000],
                   lfo_depth = 0.75, env_depth = 0.00, external = 0.00) ,
        alfo = lfo("a",ratio=1.000, delay=0.000),
        blfo = lfo("b",ratio=1.000, delay=0.000),
        aenv = adsr("a",a=0.000, d=0.000, s=1.000, r=0.000),
        benv = adsr("b",a=0.000, d=0.000, s=1.000, r=0.000),
        cenv = addsr(a=0.000, d1=0.000, d2=0.000, r=0.000, bp=1.00, 
                     sus=1.00, trig=0),
        opa = fmop("a",mratio=1.000,mscale=2,mdepth=0.000,lfo=0.00,env=0.00,
                   cratio=1.00,cbias=0.000,
                   feedback=0.000, cross_feedback=0.000, amp = 1.0),
        opb = fmop("b",mratio=2.000,mscale=2,mdepth=0.000,lfo=0.00,env=0.00,
                   cratio=1.00,cbias=0.000,
                   feedback=0.000, cross_feedback=0.000, amp = 1.0),
        opc = wvop("c",sratio=1.000,pratio=1.000,pw=0.5,pwm=0.000,
                   wave=0.5,wave_lfo=0.000,wave_env=0.000,
                   noise_amp=0.00,
                   filter_track=16,filter_env=0,amp=1.0),
        opd = wvop("d",sratio=1.500,pratio=1.000,pw=0.5,pwm=0.000,
                   wave=0.5,wave_lfo=0.000,wave_env=0.000,
                   noise_amp=0.00,
                   filter_track=16,filter_env=0,amp=1.0),
        xfilter = filter("x",freq=16000,track=0,
                         env=0,cenv=0,
                         lfo=0,vlfo=0,
                         res=0.50,amp=1.00),
        yfilter = filter("y",freq=16000,track=0,
                         env=0,cenv=0,
                         lfo=0,vlfo=0,
                         res=0.50,amp=1.00)):
    p = Sol(name)
    p["amp"] = fval(amp,0,2)
    p["port"] = fval(port)
    p["timebase"] = float(timebase)
    p.update(vibrato)
    p.update(x)
    p.update(y)
    p.update(alfo)
    p.update(blfo)
    p.update(aenv)
    p.update(benv)
    p.update(cenv)
    p.update(opa)
    p.update(opb)
    p.update(opc)
    p.update(opd)
    p.update(xfilter)
    p.update(yfilter)
    program_bank[slot] = p
    return p

sol(0,"Init")


sol(1,"Brush Organ",amp=0.300,
    port=0.000,
    timebase=6.4663,
    vibrato = vibrato(ratio=0.03125,sens=0.100,depth=0.000,
                      delay=2.054,extern=0.000),
    alfo = lfo("a",ratio=5.00000,delay=0.0000),
    aenv = adsr("a",a=0.000,d=0.000,s=0.464,r=0.000,lfo_trig=1),
    blfo = lfo("b",ratio=0.05000,delay=0.0000),
    benv = adsr("b",a=0.000,d=0.011,s=0.690,r=0.000,lfo_trig=0),
    cenv=addsr(a=0.000,d1=0.000,d2=0.000,r=0.000,bp=0.949,sus=0.432,trig=0),
    opa = fmop("a",mratio=2.0000,mscale=1,mdepth=0.055,lfo=0.499,env=0.999,
               cratio=1.0000,cbias=0.0000,
               feedback=0.0000,cross_feedback=0.0000,amp=1.000),
    opb = fmop("b",mratio=2.0000,mscale=3,mdepth=0.698,lfo=0.000,env=0.687,
               cratio=8.0000,cbias=0.0000,
               feedback=2.6103,cross_feedback=0.0000,amp=0.784),
    opc = wvop("c",sratio=4.0000,pratio=2.0000,pw=0.905,pwm=0.006,
               wave=0.500,wave_lfo=0.000,wave_env=0.000,
               noise_amp=0.000,filter_track=16,filter_env=0,amp=0.303),
    opd = wvop("d",sratio=3.0000,pratio=5.0000,pw=0.500,pwm=0.150,
               wave=0.500,wave_lfo=0.000,wave_env=0.000,
               noise_amp=0.000,filter_track=16,filter_env=3,amp=1.000),
    x = vector("x",pos=0.000,ratio=0.37500,wave=0.500,delay=0.000,
               adsr=[0.000,0.002,0.973,2.733],trig=1,
               lfo_depth=0.474, env_depth=0.000,external=0.000),
    xfilter = filter("x",freq=11406,track=2,
                     env=0,cenv=0,lfo=4594,vlfo=0,res=0.193,amp=1.000),
    y = vector("y",pos=0.000,ratio=2.25000,wave=0.500,delay=0.000,
               adsr=[0.000,4.325,0.522,0.000],trig=0,
               lfo_depth=-0.026, env_depth=0.000,external=0.000),
    yfilter = filter("y",freq=15902,track=0,
                     env=-1,cenv=-89,lfo=0,vlfo=0,res=0.275,amp=1.000))
sol(2,"Cashew",amp=0.300,
    port=0.000,
    timebase=7.8491,
    vibrato = vibrato(ratio=1.00000,sens=0.100,depth=0.232,
                      delay=3.266,extern=0.000),
    alfo = lfo("a",ratio=0.06250,delay=2.9002),
    aenv = adsr("a",a=0.577,d=0.520,s=0.355,r=0.461,lfo_trig=0),
    blfo = lfo("b",ratio=0.50000,delay=0.0000),
    benv = adsr("b",a=0.577,d=13.115,s=0.932,r=0.414,lfo_trig=0),
    cenv=addsr(a=0.000,d1=3.851,d2=0.437,r=0.351,bp=0.899,sus=0.400,trig=0),
    opa = fmop("a",mratio=2.0000,mscale=3,mdepth=0.546,lfo=0.000,env=0.659,
               cratio=2.0000,cbias=0.0000,
               feedback=0.0000,cross_feedback=0.0000,amp=1.000),
    opb = fmop("b",mratio=1.0000,mscale=2,mdepth=0.014,lfo=0.000,env=0.313,
               cratio=0.9957,cbias=0.8926,
               feedback=0.0000,cross_feedback=0.0000,amp=0.061),
    opc = wvop("c",sratio=4.0000,pratio=2.0000,pw=0.009,pwm=0.000,
               wave=0.500,wave_lfo=0.000,wave_env=0.000,
               noise_amp=0.000,filter_track=6,filter_env=0,amp=1.000),
    opd = wvop("d",sratio=3.0000,pratio=8.0000,pw=0.500,pwm=0.730,
               wave=0.500,wave_lfo=0.000,wave_env=0.000,
               noise_amp=0.000,filter_track=16,filter_env=5,amp=1.000),
    x = vector("x",pos=0.000,ratio=0.75000,wave=0.500,delay=0.000,
               adsr=[0.592,0.130,0.722,0.312],trig=0,
               lfo_depth=0.584, env_depth=0.000,external=0.000),
    xfilter = filter("x",freq=2073,track=0,
                     env=0,cenv=10650,lfo=0,vlfo=0,res=0.010,amp=1.000),
    y = vector("y",pos=0.000,ratio=0.50000,wave=0.500,delay=0.000,
               adsr=[0.575,0.500,0.604,0.286],trig=0,
               lfo_depth=-0.851, env_depth=0.000,external=0.000),
    yfilter = filter("y",freq=10765,track=0,
                     env=0,cenv=-3210,lfo=0,vlfo=0,res=0.470,amp=1.000))
sol(3,"Whale Call",amp=0.300,
    port=0.503,
    timebase=7.2694,
    vibrato = vibrato(ratio=1.00000,sens=0.000,depth=0.000,
                      delay=3.114,extern=0.000),
    alfo = lfo("a",ratio=6.00000,delay=3.6653),
    aenv = adsr("a",a=0.589,d=0.042,s=0.054,r=0.364,lfo_trig=0),
    blfo = lfo("b",ratio=0.00391,delay=1.6809),
    benv = adsr("b",a=0.252,d=0.271,s=0.425,r=0.440,lfo_trig=0),
    cenv=addsr(a=0.407,d1=2.979,d2=0.171,r=3.996,bp=0.994,sus=0.133,trig=0),
    opa = fmop("a",mratio=5.0936,mscale=3,mdepth=0.160,lfo=0.000,env=0.052,
               cratio=5.0617,cbias=0.0000,
               feedback=0.0000,cross_feedback=0.0000,amp=1.000),
    opb = fmop("b",mratio=5.2440,mscale=2,mdepth=0.692,lfo=0.000,env=0.855,
               cratio=2.7592,cbias=0.3172,
               feedback=1.6330,cross_feedback=0.0000,amp=0.301),
    opc = wvop("c",sratio=7.6778,pratio=1.9939,pw=0.717,pwm=0.000,
               wave=0.500,wave_lfo=0.000,wave_env=0.000,
               noise_amp=0.000,filter_track=3,filter_env=0,amp=1.000),
    opd = wvop("d",sratio=3.9350,pratio=2.5107,pw=0.424,pwm=0.000,
               wave=0.500,wave_lfo=0.000,wave_env=-0.095,
               noise_amp=0.000,filter_track=16,filter_env=0,amp=1.000),
    x = vector("x",pos=0.000,ratio=0.01042,wave=0.500,delay=0.000,
               adsr=[0.184,0.264,0.915,0.582],trig=0,
               lfo_depth=-0.577, env_depth=0.000,external=0.000),
    xfilter = filter("x",freq=6839,track=0,
                     env=0,cenv=3556,lfo=0,vlfo=0,res=0.744,amp=1.000),
    y = vector("y",pos=0.000,ratio=1.00000,wave=0.500,delay=0.000,
               adsr=[0.356,0.242,0.689,0.143],trig=0,
               lfo_depth=0.121, env_depth=-0.873,external=0.000),
    yfilter = filter("y",freq=3242,track=0,
                     env=0,cenv=0,lfo=12758,vlfo=0,res=0.979,amp=1.000))
sol(4,"Cephalopod",amp=0.300,
    port=0.000,
    timebase=7.9858,
    vibrato = vibrato(ratio=1.00000,sens=0.000,depth=0.000,
                      delay=3.693,extern=0.000),
    alfo = lfo("a",ratio=8.00000,delay=0.7284),
    aenv = adsr("a",a=15.449,d=15.073,s=0.804,r=7.886,lfo_trig=0),
    blfo = lfo("b",ratio=0.00391,delay=0.0000),
    benv = adsr("b",a=12.500,d=0.002,s=0.912,r=10.030,lfo_trig=0),
    cenv=addsr(a=0.000,d1=12.317,d2=13.394,r=6.671,bp=0.991,sus=0.635,trig=0),
    opa = fmop("a",mratio=1.0000,mscale=2,mdepth=0.388,lfo=0.000,env=0.154,
               cratio=7.9668,cbias=0.0000,
               feedback=0.0000,cross_feedback=0.0000,amp=1.000),
    opb = fmop("b",mratio=3.0000,mscale=3,mdepth=0.446,lfo=0.000,env=0.000,
               cratio=3.9974,cbias=1.3229,
               feedback=0.0000,cross_feedback=0.0000,amp=1.000),
    opc = wvop("c",sratio=6.0000,pratio=2.0000,pw=0.500,pwm=0.000,
               wave=0.500,wave_lfo=0.000,wave_env=0.000,
               noise_amp=0.000,filter_track=7,filter_env=1,amp=0.790),
    opd = wvop("d",sratio=1.0000,pratio=2.0000,pw=0.500,pwm=0.000,
               wave=0.500,wave_lfo=0.000,wave_env=0.000,
               noise_amp=0.000,filter_track=16,filter_env=2,amp=1.000),
    x = vector("x",pos=-0.803,ratio=0.02083,wave=0.500,delay=0.815,
               adsr=[12.650,5.135,0.918,13.329],trig=0,
               lfo_depth=-0.938, env_depth=0.000,external=0.000),
    xfilter = filter("x",freq=333,track=0,
                     env=13699,cenv=0,lfo=0,vlfo=0,res=0.544,amp=1.000),
    y = vector("y",pos=0.000,ratio=0.05000,wave=0.500,delay=0.000,
               adsr=[5.299,8.680,0.117,12.080],trig=0,
               lfo_depth=-0.175, env_depth=0.000,external=0.000),
    yfilter = filter("y",freq=12561,track=0,
                     env=1831,cenv=0,lfo=0,vlfo=0,res=0.880,amp=1.000))

sol(5,"SETI",amp=0.300,
    port=0.000,
    timebase=7.0818,
    vibrato = vibrato(ratio=1.00000,sens=0.000,depth=0.078,
                      delay=0.505,extern=0.000),
    alfo = lfo("a",ratio=0.02500,delay=0.0000),
    aenv = adsr("a",a=0.784,d=1.616,s=0.619,r=0.000,lfo_trig=0),
    blfo = lfo("b",ratio=0.87500,delay=0.0000),
    benv = adsr("b",a=4.779,d=1.711,s=0.917,r=5.976,lfo_trig=0),
    cenv=addsr(a=4.335,d1=0.773,d2=3.782,r=5.241,bp=0.982,sus=0.079,trig=0),
    opa = fmop("a",mratio=2.5248,mscale=2,mdepth=0.728,lfo=0.000,env=0.795,
               cratio=2.6360,cbias=1.0608,
               feedback=0.5533,cross_feedback=0.0000,amp=1.000),
    opb = fmop("b",mratio=5.2300,mscale=3,mdepth=0.600,lfo=0.000,env=0.000,
               cratio=1.3259,cbias=0.0000,
               feedback=0.9466,cross_feedback=0.0000,amp=0.821),
    opc = wvop("c",sratio=6.4579,pratio=2.3779,pw=0.021,pwm=0.000,
               wave=0.500,wave_lfo=0.000,wave_env=0.000,
               noise_amp=0.000,filter_track=16,filter_env=0,amp=1.000),
    opd = wvop("d",sratio=6.3031,pratio=6.8911,pw=0.500,pwm=0.437,
               wave=0.500,wave_lfo=0.000,wave_env=0.000,
               noise_amp=0.000,filter_track=16,filter_env=0,amp=1.000),
    x = vector("x",pos=0.000,ratio=0.08333,wave=0.500,delay=0.000,
               adsr=[0.000,5.504,0.344,2.900],trig=1,
               lfo_depth=0.882, env_depth=0.000,external=0.000),
    xfilter = filter("x",freq=9352,track=1,
                     env=201,cenv=-6058,lfo=0,vlfo=0,res=0.218,amp=1.000),
    y = vector("y",pos=0.000,ratio=0.66667,wave=0.500,delay=0.000,
               adsr=[3.343,6.033,0.954,0.075],trig=0,
               lfo_depth=0.253, env_depth=0.000,external=0.000),
    yfilter = filter("y",freq=6565,track=0,
                     env=-8560,cenv=0,lfo=9435,vlfo=0,res=0.460,amp=1.000))

sol(6,"Easy Financing",amp=0.300,
    port=0.000,
    timebase=7.9411,
    vibrato = vibrato(ratio=1.00000,sens=0.100,depth=0.576,
                      delay=2.060,extern=0.000),
    alfo = lfo("a",ratio=0.16667,delay=0.0000),
    aenv = adsr("a",a=0.074,d=0.574,s=0.894,r=0.435,lfo_trig=0),
    blfo = lfo("b",ratio=0.01042,delay=0.0000),
    benv = adsr("b",a=0.335,d=0.244,s=0.792,r=0.279,lfo_trig=1),
    cenv=addsr(a=0.000,d1=0.270,d2=0.194,r=0.343,bp=0.473,sus=0.400,trig=0),
    opa = fmop("a",mratio=1.5000,mscale=3,mdepth=0.279,lfo=0.635,env=0.000,
               cratio=2.0000,cbias=0.0000,
               feedback=0.0000,cross_feedback=0.0000,amp=1.000),
    opb = fmop("b",mratio=1.0000,mscale=2,mdepth=0.657,lfo=0.460,env=0.150,
               cratio=1.0022,cbias=0.1346,
               feedback=0.0000,cross_feedback=0.0000,amp=0.988),
    opc = wvop("c",sratio=1.0000,pratio=3.0000,pw=0.825,pwm=0.000,
               wave=0.500,wave_lfo=0.000,wave_env=0.000,
               noise_amp=0.000,filter_track=16,filter_env=0,amp=1.000),
    opd = wvop("d",sratio=0.5000,pratio=2.0000,pw=0.500,pwm=0.739,
               wave=0.633,wave_lfo=0.000,wave_env=0.000,
               noise_amp=0.000,filter_track=4,filter_env=0,amp=1.000),
    x = vector("x",pos=-0.084,ratio=16.00000,wave=0.098,delay=3.358,
               adsr=[0.225,0.391,0.923,0.307],trig=0,
               lfo_depth=-0.216, env_depth=0.000,external=0.000),
    xfilter = filter("x",freq=8082,track=1,
                     env=0,cenv=5192,lfo=0,vlfo=0,res=0.193,amp=1.000),
    y = vector("y",pos=0.000,ratio=0.16667,wave=0.567,delay=0.000,
               adsr=[0.134,0.459,0.694,4.875],trig=0,
               lfo_depth=-0.007, env_depth=-0.273,external=0.000),
    yfilter = filter("y",freq=2859,track=0,
                     env=7700,cenv=0,lfo=0,vlfo=0,res=0.081,amp=1.000))

sol(7,"Mountaintop Removal",amp=0.300,
    port=0.000,
    timebase=5.3997,
    vibrato = vibrato(ratio=0.66667,sens=0.100,depth=0.000,
                      delay=3.012,extern=0.000),
    alfo = lfo("a",ratio=0.01563,delay=0.0000),
    aenv = adsr("a",a=1.523,d=3.350,s=0.361,r=0.510,lfo_trig=0),
    blfo = lfo("b",ratio=0.66667,delay=2.7968),
    benv = adsr("b",a=1.673,d=3.231,s=0.815,r=2.371,lfo_trig=0),
    cenv=addsr(a=4.615,d1=6.027,d2=2.793,r=5.697,bp=0.851,sus=0.118,trig=0),
    opa = fmop("a",mratio=0.8932,mscale=2,mdepth=0.385,lfo=0.000,env=0.347,
               cratio=1.3835,cbias=0.0000,
               feedback=2.7715,cross_feedback=0.0000,amp=1.000),
    opb = fmop("b",mratio=4.0124,mscale=3,mdepth=0.533,lfo=0.000,env=0.930,
               cratio=11.8396,cbias=0.0000,
               feedback=0.0000,cross_feedback=0.0000,amp=0.973),
    opc = wvop("c",sratio=6.1170,pratio=3.2225,pw=0.500,pwm=0.000,
               wave=0.500,wave_lfo=-0.808,wave_env=0.000,
               noise_amp=0.000,filter_track=16,filter_env=9,amp=1.000),
    opd = wvop("d",sratio=7.8460,pratio=2.3170,pw=0.500,pwm=0.000,
               wave=0.531,wave_lfo=0.000,wave_env=0.000,
               noise_amp=0.000,filter_track=16,filter_env=3,amp=0.790),
    x = vector("x",pos=0.792,ratio=0.02083,wave=0.500,delay=0.000,
               adsr=[6.270,5.902,0.133,2.680],trig=0,
               lfo_depth=-0.964, env_depth=0.000,external=0.000),
    xfilter = filter("x",freq=13835,track=0,
                     env=0,cenv=-732,lfo=0,vlfo=0,res=0.324,amp=1.000),
    y = vector("y",pos=0.000,ratio=0.03125,wave=0.500,delay=3.659,
               adsr=[1.225,3.385,0.839,2.974],trig=0,
               lfo_depth=0.880, env_depth=0.000,external=0.000),
    yfilter = filter("y",freq=12044,track=0,
                     env=0,cenv=0,lfo=3956,vlfo=0,res=0.948,amp=1.000))

