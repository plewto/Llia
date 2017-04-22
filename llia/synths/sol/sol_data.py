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

sol(  1,"Test",amp=0.300,
    port=0.000,
    timebase=7.0000,
    vibrato = vibrato(ratio=1.00000,sens=0.100,depth=0.000,
                      delay=0.000,extern=0.000),
    alfo = lfo("a",ratio=1.00000,delay=0.0000),
    aenv = adsr("a",a=0.000,d=0.000,s=1.000,r=0.000,lfo_trig=0),
    blfo = lfo("b",ratio=1.00000,delay=0.0000),
    benv = adsr("b",a=0.000,d=0.000,s=0.000,r=0.000,lfo_trig=0),
    cenv=addsr(a=0.000,d1=0.000,d2=0.000,r=0.000,bp=1.000,sus=1.000,trig=0),
    opa = fmop("a",mratio=1.0000,mscale=1,mdepth=1.000,lfo=0.000,env=0.000,
               cratio=1.0000,cbias=0.0000,
               feedback=0.0000,cross_feedback=0.0000,amp=1.000),
    opb = fmop("b",mratio=1.0000,mscale=1,mdepth=1.000,lfo=0.000,env=0.000,
               cratio=1.0000,cbias=0.0000,
               feedback=0.0000,cross_feedback=0.0000,amp=1.000),
    opc = wvop("c",sratio=1.0000,pratio=0.5000,pw=0.500,pwm=0.000,
               wave=0.000,wave_lfo=0.000,wave_env=0.000,
               noise_amp=0.000,filter_track=16,filter_env=1,amp=1.000),
    opd = wvop("d",sratio=1.0000,pratio=0.5000,pw=0.500,pwm=0.000,
               wave=0.000,wave_lfo=0.000,wave_env=0.000,
               noise_amp=0.000,filter_track=16,filter_env=1,amp=1.000),
    x = vector("x",pos=0.000,ratio=1.00000,wave=0.500,delay=0.000,
               adsr=[0.000,0.000,0.000,0.000],trig=0,
               lfo_depth=0.000, env_depth=0.000,external=0.000),
    xfilter = filter("x",freq=16000,track=0,
                     env=0,cenv=0,lfo=0,vlfo=0,res=0.000,amp=1.000),
    y = vector("y",pos=0.000,ratio=1.00000,wave=0.500,delay=0.000,
               adsr=[0.000,0.000,0.000,0.000],trig=0,
               lfo_depth=0.000, env_depth=0.000,external=0.000),
    yfilter = filter("y",freq=16000,track=0,
                     env=0,cenv=0,lfo=0,vlfo=0,res=0.000,amp=1.000))
