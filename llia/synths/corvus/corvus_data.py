# llia.synths.corvus.corvus_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance

prototype = {
    "port" : 0.00,        # norm 
    "amp" : 0.1,          # volume
    "vfreq" : 7.0,        # tumbler
    "vdelay" : 0.0,       # linear
    "vsens" : 0.0,        # norm
    "vdepth" : 0.0,       # norm
    "xpitch" : 0.0,       # norm
    "lfo1_ratio" : 1.0,   # msb
    "lfo1_delay" : 0.0,   # linear
    "lfo2_ratio" : 0.5,   # msb
    "lfo2_delay" : 0.0    # linear
}

for op in (1,2,3,4):
    for p,dflt in (("op%d_enable" , 1),       # toggle
                   ("op%d_ratio" , 1.0),      # tumbler
                   ("op%d_bias" , 0.0),       # tuimbler
                   ("op%d_amp" , 1.0),        # volume
                   ("op%d_velocity" , 0.0),   # norm
                   ("op%d_lfo1" , 0.0),       # norm
                   ("op%d_lfo2" , 0.0),       # norm
                   ("op%d_external" , 0.0),   # norm
                   ("op%d_left" , 0),         # msb
                   ("op%d_right" , 0),        # msb
                   ("op%d_key" , 60),         # msb
                   ("op%d_attack" , 0.00),    
                   ("op%d_decay1" , 0.00),
                   ("op%d_decay2" , 0.00),
                   ("op%d_release" , 0.00),
                   ("op%d_breakpoint" , 1.0), 
                   ("op%d_sustain" , 1.0),
                   ("op%d_env_mode" , 0),
                   ("fm%d_ratio" , 1.00),     # tumbler
                   ("fm%d_modscale" , 1),     # msb
                   ("fm%d_moddepth" , 0.0),   # norm
                   ("fm%d_lag" , 0.00),       # norm
                   ("fm%d_lfo1" , 0.00),      # norm
                   ("fm%d_lfo2" , 0.00),      # norm
                   ("fm%d_external" , 0.00),  # norm
                   ("fm%d_left" , 0),         # msb
                   ("fm%d_right" , 0)):       # msb
        prototype[p%op] = dflt
prototype["nse3_mix"] = 0.0                   # noise mix
prototype["nse3_bw"] = 1                      # noise band width (1,1000)
prototype["bzz4_n"] = 1
prototype["bzz4_env"] = 16
prototype["bzz4_mix"] = 0.0
prototype["bzz4_lag"] = 0.0

class Corvus(Program):

    def __init__(self,name):
        super(Corvus,self).__init__(name,Corvus,prototype)
        self.performance = performance()

program_bank = ProgramBank(Corvus("Init"))
program_bank.enable_undo = False

def op(n, 
       enable= 1,
       ratio= 1.0,
       bias= 0.0,
       amp= 1.0,
       velocity= 0.0,
       lfo1= 0.0,
       lfo2= 0.0,
       external= 0.0,
       left= 0,
       right= 0,
       key= 60,
       attack= 0.00,
       decay1= 0.00,
       decay2= 0.00,
       release= 0.00,
       breakpoint= 1.0,
       sustain= 1.0,
       env_mode= 0,
       nse_mix = 0.0,    # op3 only
       nse_bw = 1,       # op3 only
       bzz_n = 1,        # op4 only buzz initial n-harmonics
       bzz_env = 16,     # env -> buzz n-harmonics   -/+ 200
       bzz_mix = 0.0):   # c4/buzz mix
    map = {"op%d_ratio" % n : float(ratio),
           "op%d_bias" % n : float(bias),
           "op%d_amp" % n : float(amp),
           "op%d_velocity" % n : float(velocity),
           "op%d_lfo1" % n : float(lfo1),
           "op%d_lfo2" % n : float(lfo2),
           "op%d_external" % n : float(external),
           "op%d_attack" % n : float(attack),
           "op%d_decay1" % n : float(decay1),
           "op%d_decay2" % n : float(decay2),
           "op%d_release" % n : float(release),
           "op%d_breakpoint" % n : float(breakpoint),
           "op%d_sustain" % n : float(sustain),
           "op%d_left" % n : int(left),
           "op%d_right" % n : int(right),
           "op%d_key" % n : int(key),
           "op%d_enable" % n : int(enable),
           "op%d_env_mode" % n : int(env_mode)}
    if n==3:
        map["nse3_mix"] = float(nse_mix)
        map["nse3_bw"] = int(nse_bw)
    if n==4:
        map["bzz4_n"] = int(bzz_n)
        map["bzz4_env"] = int(bzz_env)
        map["bzz4_mix"] = float(bzz_mix)
            
    return map

def fm(n,
       ratio = 1.00,
       modscale = 1,
       moddepth = 0.0,
       lag = 0.00,
       lfo1 = 0.00,
       lfo2 = 0.00,
       external = 0.00,
       left = 0,
       right = 0):
    map = {"ratio" : float(ratio),
           "modscale" : float(modscale),
           "moddepth" : float(moddepth),
           "lag" : float(lag),
           "lfo1" : float(lfo1),
           "lfo2" : float(lfo2),
           "external" : float(external),
           "left" : int(left),
           "right" : int(right)}
    return map

def corvus(slot, name,
           port = 0.00,
           amp = 0.1,
           vfreq = 7.0,
           vdelay = 0.0,
           vsens = 0.0,
           vdepth = 0.0,
           xpitch = 0.0,
           lfo1_ratio = 1.0,
           lfo1_delay = 0.0,
           lfo2_ratio = 0.5,
           lfo2_delay = 0.0,
           op1 = op(1),
           fm1 = fm(1),
           op2 = op(2),
           fm2 = fm(2),
           op3 = op(3),
           fm3 = fm(3),
           op4 = op(4),
           fm4 = fm(4),
           ):
    p = Corvus(name)
    p["port"] = float(port)
    p["amp"] = float(amp)
    p["vfreq"] = float(vfreq)
    p["vdelay"] = float(vdelay)
    p["vsens"] = float(vsens)
    p["vdepth"] = float(vdepth)
    p["xpitch"] = float(xpitch)
    p["lfo1_ratio"] = float(lfo1_ratio)
    p["lfo1_delay"] = float(lfo1_delay)
    p["lfo2_ratio"] = float(lfo2_ratio)
    p["lfo2_delay"] = float(lfo2_delay)
    def copymap(m):
        for param,value in m.items():
            p[param] = value
    for m in (op1,op2,op3,op4,fm1,fm2,fm4):
        copymap(m)
    program_bank[slot] = p
    return p


corvus(0,"Crow")


