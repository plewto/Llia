# llia.synths.lfo3.lfo3_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance



# scale and bias values are applied only to signal outputs,
# they do not effect internal modulation values.
#
prototype = {
    "lfoFreq" : 1.00,    #  Common frequency                       
    "rA" : 1.000,        #  LFO A freq ratio                   
    "phaseA" : 0.000,    #  LFO A phase 0..1                        
    "bleedA" : 1.000,    #  LFO A envelope bleed 0->use env, 1->bypass env                       
    "scaleA" : 1.000,    #  LFO A output scale                       
    "biasA" : 0.000,     #  LFO A output bias                      
    "bToAFreq" : 0.0,    #  LFO B -> LFO A frequency (possible feedback)
    
    "rB" : 1.000,        #  LFO B freq ratio                   
    "phaseB" : 0.333,    #  LFO B phase
    "bleedB" : 1.000,    #  LFO B envelope bleed                       
    "scaleB" : 1.000,    #  LFO B output scale                       
    "biasB" : 0.000,     #  LFO B outbus bias                           
    "envToFreqB" : 0.00, #  env -> LFO B freq. 
    "aToBFreq" : 0.00,   #  LFO A -> LFO B freq (possible feedback)                        
    "cToBAmp" : 0.00,    #  LFO C -> LFO B amp (possibl feedback)
    
    "rC" : 1.000,        #  LFO C freq ratio                   
    "phaseC" : 0.667,    #  LFO C phase                        
    "bleedC" : 1.000,    #  LFO C envelope bleed                       
    "scaleC" : 1.000,    #  LFO C output scale                       
    "biasC" : 0.000,     #  LFO C output bias                      
    "bToCAmp" : 0.00,    #  LFO B -> LFO C amp (possible feedback)
    
    "lfoDelay" : 0.0,    #  env onset delay after gate transition to high                       
    "lfoAttack" : 0.0,   #  env attack tim after delay segment                        
    "lfoHold" : 0.0,     #  env hold time after gate low                      
    "lfoRelease" : 0.0,  #  env release time after hold segmnet      
}

class Lfo3(Program):

    def __init__(self, name):
        super(Lfo3, self).__init__(name, "LFO3", prototype)
        self.performance = performance()

program_bank = ProgramBank(Lfo3("Init"))
program_bank.enable_undo = False

def _fill(dic, template):
    rs = {}
    for key,dflt in template.items():
        v = dic.get(key, dflt)
        rs[key] = float(v)
    return rs

# Translate pp parameters to synth parameters
_a_transmap = {"ratio" : "rA",
               "phase" : "phaseA",
               "bleed" : "bleedA",
               "scale" : "scaleA",
               "bias" : "biasA",
               "bFreqMod" : "bToAFreq"}
_b_transmap =  {"ratio" : "rB",
                "phase" : "phaseB",
                "bleed" : "bleedB",
                "scale" : "scaleB",
                "bias" : "biasB",
                "envFreqMod" : "envToFreqB",
                "aFreqMod" : "aToBFreq",
                "cAmpMod" : "cToBAmp"}
_c_transmap =  {"ratio" : "rC",
                "phase" : "phaseC",
                "bleed" : "bleedC",
                "scale" : "scaleC",
                "bias" : "biasC",
                "bAmpMod" : "bToCAmp"}
_env_transmap = {"delay" : "lfoDelay",
                 "attack" : "lfoAttack",
                 "hold" : "lfoHold",
                 "release" : "lfoRelease"}

def _reverse_map(src):
    rs = {}
    for key,val in src.items():
        rs[val] = key
    return rs

_a_rvsmap = _reverse_map(_a_transmap)
_b_rvsmap = _reverse_map(_b_transmap)
_c_rvsmap = _reverse_map(_c_transmap)
_env_rvsmap = _reverse_map(_env_transmap)


def lfo3(slot, name, freq=5.0,
         a = {"ratio" : 1.00,
              "phase" : 0.00,
              "bleed" : 1.00,
              "scale" : 1.00,
              "bias"  : 0.00,
              "bFreqMod" : 0.00},
         b = {"ratio" : 1.00,
              "phase" : 0.333,
              "bleed" : 1.00,
              "scale" : 1.00,
              "bias"  : 0.00,
              "envFreqMod" : 0.00,
              "aFreqMod"   : 0.00,
              "cAmpMod"    : 0.00},
         c = {"ratio" : 1.00,
              "phase" : 0.667,
              "bleed" : 1.00,
              "scale" : 1.00,
              "bias"  : 0.00,
              "bAmpMod" : 0.00},
         env = {"delay" : 0.00,
                "attack" : 0.00,
                "hold" : 1.00,
                "release" : 0.00}):
    a = _fill(a, {"ratio" : 1.00,
                  "phase" : 0.00,
                  "bleed" : 1.00,
                  "scale" : 1.00,
                  "bias"  : 0.00,
                  "bFreqMod" : 0.00})
    b = _fill(b, {"ratio" : 1.00,
                  "phase" : 0.333,
                  "bleed" : 1.00,
                  "scale" : 1.00,
                  "bias"  : 0.00,
                  "envFreqMod" : 0.00,
                  "aFreqMod"   : 0.00,
                  "cAmpMod"    : 0.00})
    c = _fill(c, {"ratio" : 1.00,
                  "phase" : 0.667,
                  "bleed" : 1.00,
                  "scale" : 1.00,
                  "bias"  : 0.00,
                  "bAmpMod" : 0.00})
    env = _fill(env, {"delay" : 0.00,
                      "attack" : 0.00,
                      "hold" : 1.00,
                      "release" : 0.00})
    p = Lfo3(name)
    p["lfoFreq"] = float(freq)
    for pp,s in _a_transmap.items():
        p[s] = a[pp]
    for pp,s in _b_transmap.items():
        p[s] = b[pp]
    for pp,s in _c_transmap.items():
        p[s] = c[pp]
    for pp,s in _env_transmap.items():
        p[s] = env[pp]
    program_bank[slot] = p
    return p

def pp(program, slot=127):
    pad = ' '*5
    frmt = 'lfo3(%d, "%s", freq=%6.4f,\n'
    data = (slot, program.name, float(program['lfoFreq']))
    acc = frmt % data
    acc += '%sa = {' % pad
    a_keys = ('ratio','phase','bleed','scale','bias','bFreqMod')
    for ak in a_keys:
        sk = _a_transmap[ak]
        val= float(program[sk])
        apad = None
        if ak == a_keys[0]:
            frmt = '%s"%s" : %6.4f,\n'
            apad = ''
        elif ak == a_keys[-1]:
            frmt = '%s"%s" : %6.4f},\n'
            apad = pad + ' '*5
        else:
            frmt = '%s"%s" : %6.4f,\n'
            apad = pad + ' '*5
        acc += frmt % (apad, ak, val)
    acc += '%sb = {' % pad    
    b_keys = ('ratio','phase','bleed','scale','bias',
              'envFreqMod','aFreqMod','cAmpMod')
    for bk in b_keys:
        sk = _b_transmap[bk]
        val= float(program[sk])
        apad = None
        if bk == b_keys[0]:
            frmt = '%s"%s" : %6.4f,\n'
            apad = ''
        elif bk == b_keys[-1]:
            frmt = '%s"%s" : %6.4f},\n'
            apad = pad + ' '*5
        else:
            frmt = '%s"%s" : %6.4f,\n'
            apad = pad + ' '*5
        acc += frmt % (apad, bk, val)
    acc += '%sc = {' % pad    
    c_keys = ('ratio','phase','bleed','scale','bias','bAmpMod')
    for ck in c_keys:
        sk = _c_transmap[ck]
        val= float(program[sk])
        apad = None
        if ck == c_keys[0]:
            frmt = '%s"%s" : %6.4f,\n'
            apad = ''
        elif ck == c_keys[-1]:
            frmt = '%s"%s" : %6.4f},\n'
            apad = pad + ' '*5
        else:
            frmt = '%s"%s" : %6.4f,\n'
            apad = pad + ' '*5
        acc += frmt % (apad, ck, val)
    acc += '%senv = {' % pad    
    env_keys = ('delay','attack','hold','release')
    for ek in env_keys:
        sk = _env_transmap[ek]
        val= float(program[sk])
        apad = None
        if ek == env_keys[0]:
            frmt = '%s"%s" : %6.4f,\n'
            apad = ''
        elif ek == env_keys[-1]:
            frmt = '%s"%s" : %6.4f})\n'
            apad = pad + ' '*7
        else:
            frmt = '%s"%s" : %6.4f,\n'
            apad = pad + ' '*7
        acc += frmt % (apad, ek, val)
    return acc



lfo3(0, "4 Hz Tri Phase", freq=4.0,
     a = {"ratio" : 1.0000,
          "phase" : 0.0000,
          "bleed" : 1.0000,
          "scale" : 1.0000,
          "bias" : 0.0000,
          "bFreqMod" : 0.0000},
     b = {"ratio" : 1.0000,
          "phase" : 0.3330,
          "bleed" : 1.0000,
          "scale" : 1.0000,
          "bias" : 0.0000,
          "envFreqMod" : 0.0,
          "aFreqMod" : 0.0000,
          "cAmpMod" : 0.0000},
     c = {"ratio" : 1.0000,
          "phase" : 0.6670,
          "bleed" : 1.0000,
          "scale" : 1.0000,
          "bias" : 0.0000,
          "bAmpMod" : 0.0000},
     env = {"delay" : 0.0000,
            "attack" : 0.0000,
            "hold" : 1.000,
            "release" : 0.000})



lfo3(1, "1-8-16", freq=4.0,
     a = {"ratio" : 1.0000,
          "phase" : 0.0000,
          "bleed" : 1.0000,
          "scale" : 1.0000,
          "bias" : 0.0000,
          "bFreqMod" : 0.0000},
     b = {"ratio" : 2.0000,
          "phase" : 0.3330,
          "bleed" : 0.0000,
          "scale" : 1.0000,
          "bias" : 0.0000,
          "envFreqMod" : 0.0000,
          "aFreqMod" : 0.0000,
          "cAmpMod" : 0.0000},
     c = {"ratio" : 0.1250,
          "phase" : 0.6670,
          "bleed" : 1.0000,
          "scale" : 1.0000,
          "bias" : 0.0000,
          "bAmpMod" : 0.0000},
     env = {"delay" : 2.8978,
            "attack" : 0.7122,
            "hold" : 1.0000,
            "release" : 1.0000})

lfo3(2, "Env FreqMod", freq=2.1404,
     a = {"ratio" : 1.0000,
          "phase" : 0.0000,
          "bleed" : 1.0000,
          "scale" : 1.0000,
          "bias" : 0.0000,
          "bFreqMod" : 0.0000},
     b = {"ratio" : 0.0625,
          "phase" : 0.3330,
          "bleed" : 1.0000,
          "scale" : 1.0000,
          "bias" : 0.0000,
          "envFreqMod" : 1.5318,
          "aFreqMod" : 0.0000,
          "cAmpMod" : 0.0000},
     c = {"ratio" : 0.1000,
          "phase" : 0.6670,
          "bleed" : 1.0000,
          "scale" : 1.0000,
          "bias" : 0.0000,
          "bAmpMod" : 0.0000},
     env = {"delay" : 2.0628,
            "attack" : 2.0628,
            "hold" : 1.0000,
            "release" : 1.0000})

lfo3(2, "1-6-7", freq=5,
     a = {"ratio" : 1.0000,
          "phase" : 0.0000,
          "bleed" : 1.0000,
          "scale" : 1.0000,
          "bias" : 0.0000,
          "bFreqMod" : 0.0000},
     b = {"ratio" : 1.5000,
          "phase" : 0.1110,
          "bleed" : 1.0000,
          "scale" : 1.0000,
          "bias" : 0.0000,
          "envFreqMod" : 0.0000,
          "aFreqMod" : 0.0000,
          "cAmpMod" : 0.0000},
     c = {"ratio" : 0.7500,
          "phase" : 0.2220,
          "bleed" : 0.1432,
          "scale" : 1.0000,
          "bias" : 0.0000,
          "bAmpMod" : 0.0000},
     env = {"delay" : 1.0453,
            "attack" : 1.0453,
            "hold" : 0.6488,
            "release" : 0.6488})
lfo3(3, "Fm Feedback", freq=2.8534,
     a = {"ratio" : 1.0000,
          "phase" : 0.0000,
          "bleed" : 1.0000,
          "scale" : 1.0000,
          "bias" : 0.0000,
          "bFreqMod" : 1.2180},
     b = {"ratio" : 0.2500,
          "phase" : 0.3330,
          "bleed" : 1.0000,
          "scale" : 1.0000,
          "bias" : 0.0000,
          "envFreqMod" : 0.0000,
          "aFreqMod" : 0.9778,
          "cAmpMod" : 0.0000},
     c = {"ratio" : 0.7500,
          "phase" : 0.6670,
          "bleed" : 1.0000,
          "scale" : 1.0000,
          "bias" : 0.0000,
          "bAmpMod" : 0.1851},
     env = {"delay" : 0.0000,
            "attack" : 0.0000,
            "hold" : 1.0000,
            "release" : 1.0000})

lfo3(4, "Amp Mod C", freq=3.0,
     a = {"ratio" : 1.0000,
          "phase" : 0.0000,
          "bleed" : 0.0000,
          "scale" : 1.0000,
          "bias" : 0.0000,
          "bFreqMod" : 0.0000},
     b = {"ratio" : 2.0000,
          "phase" : 0.3330,
          "bleed" : 1.0000,
          "scale" : 1.0000,
          "bias" : 0.0000,
          "envFreqMod" : 0.0000,
          "aFreqMod" : 0.0000,
          "cAmpMod" : 0.0000},
     c = {"ratio" : 0.2500,
          "phase" : 0.6670,
          "bleed" : 0.0000,
          "scale" : 1.0000,
          "bias" : 0.0000,
          "bAmpMod" : 0.8826},
     env = {"delay" : 0.8295,
            "attack" : 0.8295,
            "hold" : 1.0000,
            "release" : 1.0000})
