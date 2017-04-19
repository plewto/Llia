# llia.synths.Locus.Locus_data

from __future__ import print_function
from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance

prototype = {
    "amp" : 0.1,                  # main output amplitude
    "xamp" : 1.0,                 # x-axis amp (ops A and C)
    "yamp" : 1.0,                 # y-axis amp (ops B and D)
    "env1_attack" : 0.00,         # env1 ADDSR modulation source
    "env1_decay1" : 0.00,         # all env times (0..?)
    "env1_decay2" : 0.00,         #
    "env1_release" : 0.00,        #
    "env1_breakpoint" : 1.00,     # (0..1)
    "env1_sustain": 1.00,         # (0..1)
    "env2_attack" : 0.00,         # env2 primary envelope
    "env2_decay1" : 0.00,         #
    "env2_decay2" : 0.00,         #
    "env2_release" : 0.00,        #
    "env2_breakpoint" : 1.00,     # (0..1)
    "env2_sustain" : 1.00,        # (0..1)
    "vfreq" : 5.00,               # vlfo - primary LFO & vibrato (0..99)
    "vsens" : 0.1,                # vibrato sensitivity (0..1)
    "vdepth" : 0.0,               # vibrato depth (0..1)
    "vdelay" : 0.0,               # vibrato LFO onset delay (0..4)
    "lfox_ratio" : 1.0,           # x-axis LFO frequency relative to vlfo
    "lfox_delay" : 0.0,           # xlfo onset delay (0..4)
    "lfoy_ratio" : 0.5,           # y-axis LFO frequency relative to vlfo
    "lfoy_delay" : 0.0,           # ylfo onset delay (0..4)
    "xpos" : 0.0,                 # initial x-axis value (-1..+1)
    "xpos_lfo" : 0.0,             # lfox -> x position (-1..+1)
    "xpos_env1" : 0.0,            # env1 -> x position (-1..+1)
    "xpos_xbus" : 0.0,            # external bus x -> x position (-1..+1)
    "ypos" : 0.0,                 # initial y-axis value
    "ypos_lfo" : 0.0,             # lfoy -> y position
    "ypos_env1" : 0.0,            # env1 -> y position
    "ypos_ybus" : 0.0,            # external bus y -> y position
    "opa_lfo_ratio"  : 1.0,       # relative to vlfo
    "opa_lfo_wave"   : 0.5,       # (0..1) 0.5:tri
    "opa_mod_ratio"  : 1.0,       # modulator frequency ratio (0.125...16)
    "opa_mod_depth"  : 1.0,       # modulator output amp (0..1)
    "opa_mod_scale"  : 1.0,       # modulator output scale 
    "opa_mod_env1"   : 1.0,       # env1 to mod depth (0..1)
    "opa_mod_lfo"    : 0.0,       # lfo to mod depth (0..1)
    "opa_car_ratio"  : 1.0,       # carrier frequency ratio (0,0.125...16)
    "opa_car_bias"   : 0,         # carrier frequency bias (0...9999)
    "opa_env_delay"  : 0.0,       # (0..1)
    "opa_feedback"   : 0.0,       # (0..1)
    "opa_pitch_env1" : 0.0,       # (-1..+1)
    "opa_pitch_lfo"  : 0.0,       # (-1..+1)
    "opa_amp" : 1.0,              # (0..2)
    "opb_lfo_ratio"  : 1.0,       # relative to vlfo
    "opb_lfo_wave"   : 0.5,       # (0..1) 0.5:tri
    "opb_mod_ratio"  : 1.0,       # modulator frequency ratio (0.125...16)
    "opb_mod_depth"  : 1.0,       # modulator output amp (0..1)
    "opb_mod_scale"  : 1.0,       # modulator output scale 
    "opb_mod_env1"   : 1.0,       # env1 to mod depth (0..1)
    "opb_mod_lfo"    : 0.0,       # lfo to mod depth (0..1)
    "opb_car_ratio"  : 1.0,       # carrier frequency ratio (0,0.125...16)
    "opb_car_bias"   : 0,         # carrier frequency bias (0...9999)
    "opb_env_delay"  : 0.0,       # (0..1)
    "opb_feedback"   : 0.0,       # (0..1)
    "opb_pitch_env1" : 0.0,       # (-1..+1)
    "opb_pitch_lfo"  : 0.0,       # (-1..+1)
    "opb_amp" : 1.0,              # (0..2)

    "opc_lfo_ratio"  : 1.0,       # relative to vlfo
    "opc_lfo_wave"   : 0.5,       # (0..1) 0.5 : tri
    "opc_wave"       : 0.5,       # cross mix sine/pulse/saw/noise (0..1)
    "opc_wave_lfo"   : 0.0,       # lfo to wave mix (-1..+1)
    "opc_wave_env1"  : 0.0,       # env1 to wave mix (-1..+1)
    "opc_sine_ratio"   : 1.0,     # sine wave freq ratio (0.125..16)
    "opc_pulse_ratio" : 1.0,      # pulse wave freq ratio    (0.125..16)
    "opc_saw_ratio"   : 1.0,      # sawtooth wave freq ratio (0.125..16)
    "opc_pulse_width"     : 0.5,  # (0..1)
    "opc_pulse_width_lfo" : 0.0,  # (0..1)
    "opc_noise_amp"  : 0.0,       # (0..2)
    "opc_noise_lowpass" : 16000,  # (100..16k)
    "opc_noise_highpass" : 20,    # (20..8k)
    "opc_filter_freq" : 16000,    # (20..16k)
    "opc_filter_freq_lfo" : 0,    # (-12k..+12k)
    "opc_filter_freq_env1" : 0,   # (-12k..+12k)
    "opc_filter_res" : 0.0,       # (0..1)
    "opc_env_delay" : 0.0,        # (0..1)
    "opc_pitch_env1" : 0.0,       # (-1..+1)
    "opc_pitch_lfo" : 0.0,        # (-1..+1)
    "opc_amp" : 1.0,              # (0..2)
    "opd_lfo_ratio"  : 1.0,       # relative to vlfo
    "opd_lfo_wave"   : 0.5,       # (0..1) 0.5 : tri
    "opd_wave"       : 0.5,       # cross mix sine/pulse/saw/noise (0..1)
    "opd_wave_lfo"   : 0.0,       # lfo to wave mix (-1..+1)
    "opd_wave_env1"  : 0.0,       # env1 to wave mix (-1..+1)
    "opd_sine_ratio"   : 1.0,     # sine wave freq ratio (0.125..16)
    "opd_pulse_ratio" : 1.0,      # pulse wave freq ratio    (0.125..16)
    "opd_saw_ratio"   : 1.0,      # sawtooth wave freq ratio (0.125..16)
    "opd_pulse_width"     : 0.5,  # (0..1)
    "opd_pulse_width_lfo" : 0.0,  # (0..1)
    "opd_noise_amp"  : 0.0,       # (0..2)
    "opd_noise_lowpass" : 16000,  # (100..16k)
    "opd_noise_highpass" : 20,    # (20..8k)
    "opd_filter_freq" : 16000,    # (20..16k)
    "opd_filter_freq_lfo" : 0,    # (-12k..+12k)
    "opd_filter_freq_env1" : 0,   # (-12k..+12k)
    "opd_filter_res" : 0.0,       # (0..1)
    "opd_env_delay" : 0.0,        # (0..1)
    "opd_pitch_env1" : 0.0,       # (-1..+1)
    "opd_pitch_lfo" : 0.0,        # (-1..+1)
    "opd_amp" : 1.0,              # (0..2)
    "env1_mode" : 0,              # Dummy place holder parameters
    "env2_mode" : 0}

class Locus(Program):

    def __init__(self,name):
        super(Locus,self).__init__(name,Locus,prototype)
        self.performance = performance()

program_bank = ProgramBank(Locus("Init"))
program_bank.enable_undo = False


def _env(index, att, dcy1, dcy2, rel, bp, sus):
    return {"env%d_attack" % index : float(att),
            "env%d_decay1" % index : float(dcy1),
            "env%d_decay2" % index : float(dcy2),
            "env%d_release" % index : float(rel),
            "env%d_breakpoint" % index : float(bp),
            "env%d_sustain" % index : float(sus)}

def env1(a=0.00, d1=0.00, d2=0.00, r=0.00, bp=1.0, s=1.0):
    return _env(1,a,d1,d2,r,bp,s)

def env2(a=0.00, d1=0.00, d2=0.00, r=0.00, bp=1.0, s=1.0):
    return _env(2,a,d1,d2,r,bp,s)

def vibrato(freq=5.0, sens=0.1, depth=0, delay=0.0):
    return {"vfreq" : float(freq),
            "vsens" : float(sens),
            "vdepth" : float(depth),
            "vdelay" : float(delay)}

def _vector(index, pos, lfo, env1, external):
    return {"%spos" % index : float(pos),
            "%spos_lfo" % index : float(lfo),
            "%spos_env1" % index : float(env1),
            "%spos_%sbus" % (index, index) : float(external)}

def xvector(pos=0.0, lfo=0.0, env=0.0, external=0.0):
    return _vector("x",pos,lfo,env,external)

def xlfo(ratio=2, delay=0):
    return {"lfox_ratio" : float(ratio),
            "lfox_delay" : float(delay)}

def yvector(pos=0.0, lfo=0.0, env=0.0, external=0.0):
    return _vector("y",pos,lfo,env,external)

def ylfo(ratio=2, delay=0):
    return {"lfoy_ratio" : float(ratio),
            "lfoy_delay" : float(delay)}

def _opmodulator(op,ratio,depth,scale,env1,lfo):
    return {"op%s_mod_ratio" % op : float(ratio),
            "op%s_mod_depth" % op : float(depth),
            "op%s_mod_scale" % op : float(scale),
            "op%s_mod_env1"  % op : float(env1),
            "op%s_mod_lfo"   % op : float(lfo)}

def amod(ratio=1.00,depth=1.00,scale=1.0,env1=0.0,lfo=0.0):
    return _opmodulator("a",ratio,depth,scale,env1,lfo)

def bmod(ratio=1.00,depth=1.00,scale=1.0,env1=0.0,lfo=0.0):
    return _opmodulator("b",ratio,depth,scale,env1,lfo)

def _opcarrier(op,ratio,bias,feedback):
    return {"op%s_car_ratio" % op : float(ratio),
            "op%s_car_bias" % op : float(bias),
            "op%s_feedback" % op : float(feedback)}

def acar(ratio=1.000,bias=0.000,feedback=0.00):
    return _opcarrier("a",ratio,bias,feedback)

def bcar(ratio=1.000,bias=0.000,feedback=0.00):
    return _opcarrier("b",ratio,bias,feedback)

def _oplfo(op,ratio,wave):
    return {"op%s_lfo_ratio" % op : float(ratio),
            "op%s_lfo_wave" % op : float(wave)}

def alfo(ratio=1.000, wave=0.5):
    return _oplfo("a",ratio,wave)

def blfo(ratio=1.000, wave=0.5):
    return _oplfo("b",ratio,wave)

def clfo(ratio=1.000, wave=0.5):
    return _oplfo("c",ratio,wave)

def dlfo(ratio=1.000, wave=0.5):
    return _oplfo("d",ratio,wave)

def _op(op,plfo,penv1,delay,amp):
    return {"op%s_pitch_env1" % op : float(penv1),
            "op%s_pitch_lfo" % op : float(plfo),
            "op%s_env_delay" % op : float(delay),
            "op%s_amp" % op : float(amp)}

def opa(plfo=0.000,penv1=0.000,delay=0.00,amp=1.00):
    return _op("a",plfo,penv1,delay,amp)

def opb(plfo=0.000,penv1=0.000,delay=0.00,amp=1.00):
    return _op("b",plfo,penv1,delay,amp)

def opc(plfo=0.000,penv1=0.000,delay=0.00,amp=1.00):
    return _op("c",plfo,penv1,delay,amp)

def opd(plfo=0.000,penv1=0.000,delay=0.00,amp=1.00):
    return _op("d",plfo,penv1,delay,amp)

def _opwave(op,wave,lfo,env1):
    return {"op%s_wave" % op : float(wave),
            "op%s_wave_lfo" % op : float(lfo),
            "op%s_wave_env1" % op : float(env1)}

def cwave(wave=0.500,lfo=0.00,env1=0.00):
    return _opwave("c",wave,lfo,env1)

def dwave(wave=0.500,lfo=0.00,env1=0.00):
    return _opwave("d",wave,lfo,env1)

def _optune(op,sine,pulse,saw):
    return {"op%s_sine_ratio" % op : float(sine),
            "op%s_pulse_ratio" % op : float(pulse),
            "op%s_saw_ratio" % op : float(saw)}

def ctune(sine=1.000,pulse=1.000,saw=1.000):
    return _optune("c",sine,pulse,saw)

def dtune(sine=1.000,pulse=1.000,saw=1.000):
    return _optune("d",sine,pulse,saw)

def _oppulse(op,width,lfo):
    return {"op%s_pulse_width" % op : float(width),
            "op%s_pulse_width_lfo" % op : float(lfo)}

def cpulse(width=0.500, lfo=0.00):
    return _oppulse("c",width,lfo)

def dpulse(width=0.500, lfo=0.00):
    return _oppulse("d",width,lfo)

def _opnoise(op,lowpass,highpass,amp):
    return {"op%s_noise_lowpass" % op : int(lowpass),
            "op%s_noise_highpass" % op : int(highpass),
            "op%s_noise_amp" % op : float(amp)}

def cnoise(lowpass=16000,highpass=20,amp=0.00):
    return _opnoise("c",lowpass,highpass,amp)

def dnoise(lowpass=16000,highpass=20,amp=0.00):
    return _opnoise("d",lowpass,highpass,amp)

def _opfilter(op,freq,lfo,env1,res):
    return {"op%s_filter_freq" % op : int(freq),
            "op%s_filter_freq_lfo" % op : int(lfo),
            "op%s_filter_freq_env1" % op : int(env1),
            "op%s_filter_res" % op : float(res)}

def cfilter(freq=16000,lfo=0,env1=0,res=0.00):
    return _opfilter("c",freq,lfo,env1,res)

def dfilter(freq=16000,lfo=0,env1=0,res=0.00):
    return _opfilter("d",freq,lfo,env1,res)

def locus(slot, name, amp=0.1,
          xamp=1.000,yamp=1.000,
          env1=env1(a=0.000,d1=0.000,d2=0.000,r=0.000,bp=1.00,s=1.00),
          env2=env2(a=0.000,d1=0.000,d2=0.000,r=0.000,bp=1.00,s=1.00),
          vibrato=vibrato(freq=5.000,sens=0.01,depth=0.00,delay=0.00),
          xvector=xvector(pos=0.00,lfo=0.00,env=0.00,external=0.00),
          yvector=yvector(pos=0.00,lfo=0.00,env=0.00,external=0.00),
          xlfo=xlfo(ratio=0.50,delay=0.00),
          ylfo=ylfo(ratio=1.75,delay=0.00),
          
          amod=amod(ratio=1.000,depth=1.000,scale=1.000,env1=0.000,lfo=0.000),
          acar=acar(ratio=1.000,bias=0.000,feedback=0.000),
          alfo=alfo(ratio=1.00,wave=0.5),
          opa=opa(plfo=0.000,penv1=0.000,delay=0.00,amp=1.0),

          
          bmod=bmod(ratio=1.000,depth=1.000,scale=1.000,env1=0.000,lfo=0.000),
          bcar=bcar(ratio=1.000,bias=0.000,feedback=0.000),
          blfo=blfo(ratio=1.00,wave=0.5),
          opb=opb(plfo=0.000,penv1=0.000,delay=0.00,amp=1.0),
          clfo=clfo(ratio=1.00,wave=0.5),
          
          cwave=cwave(wave=0.500,lfo=0.000,env1=0.00),
          ctune=ctune(sine=1.000,pulse=1.000,saw=1.000),
          cpulse=cpulse(width=0.500,lfo=0.00),
          cnoise=cnoise(lowpass=16000,highpass=20,amp=0.000),

          cfilter=cfilter(freq=16000,lfo=0,env1=0,res=0.000),


          opc=opc(plfo=0.000,penv1=0.000,delay=0.00,amp=1.0),
          dlfo=dlfo(ratio=1.00,wave=0.5),

          dwave=dwave(wave=0.500,lfo=0.000,env1=0.00),
          dtune=dtune(sine=1.000,pulse=1.000,saw=1.000),
          dpulse=dpulse(width=0.500,lfo=0.00),
          dnoise=dnoise(lowpass=16000,highpass=20,amp=0.000),
          dfilter=dfilter(freq=16000,lfo=0,env1=0,res=0.000),
          
          opd=opd(plfo=0.000,penv1=0.000,delay=0.00,amp=1.0)):
    p = Locus(name)
    p["amp"] = float(amp)
    p["xamp"] = float(xamp)
    p["yamp"] = float(yamp)
    p.update(env1)
    p.update(env2)
    p.update(vibrato)
    p.update(xvector)
    p.update(yvector)
    p.update(xlfo)
    p.update(ylfo)
    p.update(amod)
    p.update(acar)
    p.update(alfo)
    p.update(opa)
    p.update(bmod)
    p.update(bcar)
    p.update(blfo)
    p.update(opb)
    p.update(clfo)
    p.update(cwave)
    p.update(ctune)
    p.update(cpulse)
    p.update(cnoise)
    p.update(cfilter)
    p.update(opc)
    p.update(dlfo)
    p.update(dwave)
    p.update(dtune)
    p.update(dpulse)
    p.update(dnoise)
    p.update(dfilter)
    p.update(opd)
    program_bank[slot] = p
    return p

locus(0,"Init")


