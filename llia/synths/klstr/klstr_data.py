# llia.synths.klstr.klstr_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.util.lmath import clip, db_to_amp
from llia.performance_edit import performance

prototype = {
    "amp" : 1.0,            # linear main amplitude (0,1)                     
    "lfoFreq" : 1.0,        # Hz, (0.01,100)                           
    "lfo2FreqRatio"  : 1.0, # Ratio (1, 100)                                  
    "lfoXMod" : 0,          # Hz (0, 100)                              
    "lfoDelay" : 0.0,       # sec (0, 8)                            
    "lfoDepth" : 0.0,       # norm (0,1)                            
    "vibrato" : 0.0,        # norm (0,1)                         
    "attack" : 0.00,        # sec (0, 60)                           
    "decay" : 0.10,         # sec (0, 60)                          
    "sustain" : 1.00,       # norm (0,1)                            
    "release" : 1.00,       # sec (0,60)                            
    "envMode" : 0,          # switch 0 = ADSR gated, 1 = ADR trigger
    "pw" : 0.5,             # norm (0,1)                      
    "pwLfo" : 0.0,          # norm (0,1)
    "spread" : 0.0,         # (0,4)                          
    "spreadLfo" : 0.0,      # (0,4)                             
    "spreadEnv" : 0.0,      # (0,4)
    "cluster" : 1.0,        # (0,16)                           
    "clusterLfo" : 0.0,     #(0,16)                              
    "clusterEnv" : 0.0,     # (-16,16)                              
    "clusterLag" : 0.0,     # norm (0,1)
    "filterMix" : 0.0,      # norm (0,1) 0 = no filter, 1 = band-pass                             
    "filterFreq" : 100,     # Hz (100, 16000)                              
    "filterLfo" : 0,        # Hz (-9999, +9999)                           
    "filterEnv" : 7000,     # Hz (-9999, +9999)                              
    "filterLag" : 0.0,      # norm (0,1)                             
    "res" : 0.5,            # norm (0,1)
    "noiseAmp" : 0.0        # linear noise amp (0,1)
}

class Klstr(Program):

    def __init__(self, name):
        super(Klstr, self).__init__(name, "Klstr", prototype)

program_bank = ProgramBank(Klstr("Init"))
program_bank.enable_undo = False


def fget(d, key, default, mn=0.0, mx=1):
    v = d.get(key, default)
    return float(clip(v, mn, mx))

def klstr(slot, name, amp=-12,
          lfo = {"freq" : 1.00,
                 "ratio" : 1.00,
                 "xmod"  : 0.00,
                 "delay" : 0.00,
                 "depth" : 1.00,
                 "vibrato" : 0.00},
          env = {"gated" : True,
                 "attack" : 0.00,
                 "decay" : 0.00,
                 "sustain" : 1.00,
                 "release" : 0.00},
          spread = {"depth" : 0.0,
                    "lfo" : 0.0,
                    "env" : 0.0},
          cluster = {"depth" : 1.0,
                     "lfo" : 0.0,
                     "env" : 0.0,
                     "lag" : 0.0},
          filter_ = {"freq" : 100,
                     "lfo" : 0,
                     "env" : 7000,
                     "lag" : 0.0,
                     "res" : 0.5,
                     "mix" : 1.0},
           pw = 0.5,
          pwLfo = 0.0,
          noise = -99):
    
    p = Klstr(name)
    p.performance = performance()
    p["amp"] = db_to_amp(amp)
    p["lfoFreq"] = float(clip(lfo.get("freq", 1.0), 0.01, 100))
    p["lfo2FreqRatio"] = float(clip(lfo.get("lfo2FreqRatio", 1.0),0.01, 100))
    p["lfoXMod"] = float(clip(lfo.get("xmod", 0), 0, 100))
    p["lfoDelay"] = float(clip(lfo.get("delay", 0), 0, 8))
    p["vibrato"] = float(clip(lfo.get("vibrato",0), 0, 1))
    p["pw"] = float(clip(pw, 0, 1))
    p["pwLfo"] = float(clip(pwLfo, 0, 1))
    p["attack"] = float(clip(env.get("attack", 0), 0, 16))
    p["decay"] = float(clip(env.get("decay", 0), 0, 16))
    p["release"] = float(clip(env.get("release", 0), 0, 16))
    p["sustain"] = float(clip(env.get("sustain", 0), 0, 1))
    # if int(env.get("adsr", 1)) == 0:
    #     adsr = 1.0
    # else:
    #     adsr = 0.0
    if env.get("gatted", True):
        env_mode = 0
    else:
        env_mode = 1
    p["envMode"] = env_mode
    p["spread"] = float(clip(spread.get("depth"), 0, 4))
    p["spreadLfo"] = float(clip(spread.get("lfo"), 0, 4))
    p["spreadEnv"] = float(clip(spread.get("env"), 0, 4))
    p["cluster"] = float(clip(cluster.get("depth"), 0, 16))
    p["clusterLfo"] = float(clip(cluster.get("lfo"), 0, 16))
    p["clusterEnv"] = float(clip(cluster.get("env"), -16, 16))
    p["cluserLag"] = float(clip(cluster.get("lag"), 0, 1))
    p["filterFreq"] = int(clip(filter_.get("freq",100), 100, 16000))
    p["filterLfo"] = int(clip(filter_.get("lfo", 0), -9999, 9999))
    p["filterEnv"] = int(clip(filter_.get("env", 7000), -9999, 9999))
    p["filterLag"] = float(clip(filter_.get("lag"), 0, 1))
    p["res"] = float(clip(filter_.get("res"),0,1))
    p["filterMix"] = float(clip(filter_.get("mix", 1.0),0,1))
    p["noise"] = db_to_amp(noise)
    program_bank[slot] = p
    return p


klstr(0, "Random-0", amp=-12,
       lfo = {"freq"    : 9.7026,
              "ratio"   : 1.0000,
              "xmod"    : 0.0000,
              "delay"   : 2.339,
              "depth"   : 0.000,
              "vibrato" : 0.000},
       env = {"gated"    : True,
              "attack"  : 3.486,
              "decay"   : 2.636,
              "sustain" : 0.956,
              "release" : 0.592},
       spread = {"depth" : 3.002,
                 "lfo"   : 0.000,
                 "env"   : 0.000},
       cluster = {"depth" : 0.551,
                  "lfo"   : 0.687,
                  "env"   : 0.000,
                  "lag"   : 0.000},
       filter_ = {"freq" :  3884,
                  "lfo"  :     0,
                  "env"  :   606,
                  "lag"  : 0.000,
                  "res"  : 0.251,
                  "mix"  : 1.000},
       pw = 0.500,
       pwLfo = 0.332,
       noise = -99)

klstr(1, "Random-1", amp=-12,
       lfo = {"freq"    : 0.0966,
              "ratio"   : 1.0000,
              "xmod"    : 0.0000,
              "delay"   : 0.000,
              "depth"   : 0.000,
              "vibrato" : 0.000},
       env = {"gated"    : True,
              "attack"  : 1.000,
              "decay"   : 2.152,
              "sustain" : 0.883,
              "release" : 5.361},
       spread = {"depth" : 3.818,
                 "lfo"   : 0.855,
                 "env"   : 0.088},
       cluster = {"depth" : 10.613,
                  "lfo"   : 0.000,
                  "env"   : 0.830,
                  "lag"   : 0.000},
       filter_ = {"freq" :  8353,
                  "lfo"  :     0,
                  "env"  : -5006,
                  "lag"  : 0.000,
                  "res"  : 0.584,
                  "mix"  : 1.000},
       pw = 0.500,
       pwLfo = 0.000,
       noise = -99)

klstr(2, "SynWind", amp=-6,
       lfo = {"freq"    : 0.9681,
              "ratio"   : 1.0000,
              "xmod"    : 1.7884,
              "delay"   : 3.290,
              "depth"   : 0.000,
              "vibrato" : 0.000},
       env = {"gated"    : True,
              "attack"  : 1.439,
              "decay"   : 2.659,
              "sustain" : 0.770,
              "release" : 5.456},
       spread = {"depth" : 1.613,
                 "lfo"   : 0.805,
                 "env"   : 0.000},
       cluster = {"depth" : 0.113,
                  "lfo"   : 0.039,
                  "env"   : 9.713,
                  "lag"   : 0.000},
       filter_ = {"freq" :  3834,
                  "lfo"  :     0,
                  "env"  :  4482,
                  "lag"  : 0.000,
                  "res"  : 0.278,
                  "mix"  : 0.831},
       pw = 0.024,
       pwLfo = 0.000,
       noise = -99)

klstr(3, "Pad-1", amp=-12,
       lfo = {"freq"    : 0.0181,
              "ratio"   : 1.0000,
              "xmod"    : 0.9263,
              "delay"   : 0.757,
              "depth"   : 0.000,
              "vibrato" : 0.000},
       env = {"gated"    : True,
              "attack"  : 0.645,
              "decay"   : 1.483,
              "sustain" : 0.833,
              "release" : 3.481},
       spread = {"depth" : 0.009,
                 "lfo"   : 0.000,
                 "env"   : 0.000},
       cluster = {"depth" : 0.901,
                  "lfo"   : 0.000,
                  "env"   : 0.284,
                  "lag"   : 0.000},
       filter_ = {"freq" :  2092,
                  "lfo"  :  1901,
                  "env"  :     0,
                  "lag"  : 0.301,
                  "res"  : 0.285,
                  "mix"  : 1.000},
       pw = 0.500,
       pwLfo = 0.139,
       noise = -99)

klstr(4, "Random-4", amp=-12,
       lfo = {"freq"    : 0.8834,
              "ratio"   : 1.0000,
              "xmod"    : 2.4811,
              "delay"   : 0.000,
              "depth"   : 0.000,
              "vibrato" : 0.000},
       env = {"gated"    : True,
              "attack"  : 3.495,
              "decay"   : 2.516,
              "sustain" : 0.215,
              "release" : 1.683},
       spread = {"depth" : 2.706,
                 "lfo"   : 0.000,
                 "env"   : 0.000},
       cluster = {"depth" : 0.660,
                  "lfo"   : 0.000,
                  "env"   : 0.000,
                  "lag"   : 0.000},
       filter_ = {"freq" :   785,
                  "lfo"  :  2926,
                  "env"  :  1084,
                  "lag"  : 0.000,
                  "res"  : 0.517,
                  "mix"  : 1.000},
       pw = 0.500,
       pwLfo = 0.962,
       noise = -99)

klstr(5, "Pad-2", amp=-12,
       lfo = {"freq"    : 0.2986,
              "ratio"   : 1.0000,
              "xmod"    : 0.0000,
              "delay"   : 0.731,
              "depth"   : 0.000,
              "vibrato" : 0.000},
       env = {"gated"    : True,
              "attack"  : 0.719,
              "decay"   : 2.266,
              "sustain" : 0.942,
              "release" : 2.892},
       spread = {"depth" : 0.006,
                 "lfo"   : 0.000,
                 "env"   : 0.000},
       cluster = {"depth" : 5.834,
                  "lfo"   : 0.888,
                  "env"   : -0.715,
                  "lag"   : 0.000},
       filter_ = {"freq" :  3629,
                  "lfo"  :    80,
                  "env"  :     0,
                  "lag"  : 0.848,
                  "res"  : 0.337,
                  "mix"  : 0.774},
       pw = 0.500,
       pwLfo = 0.000,
       noise = -99)

klstr(6, "Pad-3", amp=-12,
       lfo = {"freq"    : 0.2828,
              "ratio"   : 1.0000,
              "xmod"    : 0.0000,
              "delay"   : 0.179,
              "depth"   : 0.000,
              "vibrato" : 0.000},
       env = {"gated"    : True,
              "attack"  : 0.953,
              "decay"   : 3.558,
              "sustain" : 0.763,
              "release" : 4.695},
       spread = {"depth" : 0.006,
                 "lfo"   : 0.000,
                 "env"   : 0.000},
       cluster = {"depth" : 0.344,
                  "lfo"   : 0.319,
                  "env"   : 0.856,
                  "lag"   : 0.000},
       filter_ = {"freq" :  5779,
                  "lfo"  :   128,
                  "env"  : -4088,
                  "lag"  : 0.000,
                  "res"  : 0.254,
                  "mix"  : 1.000},
       pw = 0.500,
       pwLfo = 0.000,
       noise = -99)

klstr(7, "Random-7", amp=-12,
       lfo = {"freq"    : 0.3774,
              "ratio"   : 1.0000,
              "xmod"    : 0.0000,
              "delay"   : 1.049,
              "depth"   : 0.000,
              "vibrato" : 0.000},
       env = {"gated"    : True,
              "attack"  : 0.182,
              "decay"   : 0.056,
              "sustain" : 0.864,
              "release" : 0.667},
       spread = {"depth" : 0.005,
                 "lfo"   : 0.001,
                 "env"   : 0.000},
       cluster = {"depth" : 0.439,
                  "lfo"   : 0.844,
                  "env"   : 0.000,
                  "lag"   : 0.000},
       filter_ = {"freq" :  8604,
                  "lfo"  :     0,
                  "env"  :     0,
                  "lag"  : 0.438,
                  "res"  : 0.193,
                  "mix"  : 0.530},
       pw = 0.500,
       pwLfo = 0.000,
       noise = -99)

klstr(8, "Random-8", amp=-12,
       lfo = {"freq"    : 0.2148,
              "ratio"   : 1.0000,
              "xmod"    : 2.0901,
              "delay"   : 2.936,
              "depth"   : 0.000,
              "vibrato" : 0.000},
       env = {"gated"    : True,
              "attack"  : 5.200,
              "decay"   : 0.852,
              "sustain" : 0.335,
              "release" : 4.325},
       spread = {"depth" : 0.003,
                 "lfo"   : 0.041,
                 "env"   : 0.002},
       cluster = {"depth" : 12.895,
                  "lfo"   : 0.000,
                  "env"   : 0.549,
                  "lag"   : 0.000},
       filter_ = {"freq" :  2905,
                  "lfo"  :  3116,
                  "env"  :     0,
                  "lag"  : 0.959,
                  "res"  : 0.129,
                  "mix"  : 1.000},
       pw = 0.500,
       pwLfo = 0.000,
       noise = -99)

klstr(9, "Metal Bell 1", amp=-12,
       lfo = {"freq"    : 51.0472,
              "ratio"   : 1.0000,
              "xmod"    : 0.0000,
              "delay"   : 1.201,
              "depth"   : 0.000,
              "vibrato" : 0.000},
       env = {"gated"    : True,
              "attack"  : 0.000,
              "decay"   : 0.400,
              "sustain" : 0.162,
              "release" : 1.438},
       spread = {"depth" : 1.504,
                 "lfo"   : 0.299,
                 "env"   : 0.000},
       cluster = {"depth" : 0.947,
                  "lfo"   : 0.000,
                  "env"   : 7.911,
                  "lag"   : 0.000},
       filter_ = {"freq" :   944,
                  "lfo"  :   233,
                  "env"  :     0,
                  "lag"  : 0.000,
                  "res"  : 0.416,
                  "mix"  : 1.000},
       pw = 0.500,
       pwLfo = 0.086,
       noise = -99)

klstr(10, "Sicks", amp=-6,
       lfo = {"freq"    : 0.3021,
              "ratio"   : 1.0000,
              "xmod"    : 2.7089,
              "delay"   : 0.000,
              "depth"   : 0.000,
              "vibrato" : 0.000},
       env = {"gated"    : True,
              "attack"  : 0.000,
              "decay"   : 0.022,
              "sustain" : 0.388,
              "release" : 1.426},
       spread = {"depth" : 2.509,
                 "lfo"   : 0.000,
                 "env"   : 0.381},
       cluster = {"depth" : 0.436,
                  "lfo"   : 0.588,
                  "env"   : 0.000,
                  "lag"   : 0.000},
       filter_ = {"freq" :  2775,
                  "lfo"  :   801,
                  "env"  :     0,
                  "lag"  : 0.000,
                  "res"  : 0.732,
                  "mix"  : 0.000},
       pw = 0.500,
       pwLfo = 0.000,
       noise = -99)

klstr(11, "Random-11", amp=-12,
       lfo = {"freq"    : 0.1921,
              "ratio"   : 1.0000,
              "xmod"    : 0.0000,
              "delay"   : 0.000,
              "depth"   : 0.000,
              "vibrato" : 0.000},
       env = {"gated"    : True,
              "attack"  : 0.000,
              "decay"   : 0.055,
              "sustain" : 0.752,
              "release" : 9.349},
       spread = {"depth" : 0.005,
                 "lfo"   : 0.000,
                 "env"   : 0.000},
       cluster = {"depth" : 0.897,
                  "lfo"   : 0.000,
                  "env"   : 9.482,
                  "lag"   : 0.000},
       filter_ = {"freq" :  7650,
                  "lfo"  :     0,
                  "env"  :     0,
                  "lag"  : 0.000,
                  "res"  : 0.174,
                  "mix"  : 0.000},
       pw = 0.500,
       pwLfo = 0.765,
       noise = -99)

klstr(12, "Stilick", amp=0,
       lfo = {"freq"    : 0.5814,
              "ratio"   : 1.0000,
              "xmod"    : 0.0000,
              "delay"   : 1.064,
              "depth"   : 0.000,
              "vibrato" : 0.000},
       env = {"gated"    : True,
              "attack"  : 0.000,
              "decay"   : 0.047,
              "sustain" : 0.477,
              "release" : 0.337},
       spread = {"depth" : 0.082,
                 "lfo"   : 0.000,
                 "env"   : 0.000},
       cluster = {"depth" : 0.992,
                  "lfo"   : 0.000,
                  "env"   : 0.000,
                  "lag"   : 0.000},
       filter_ = {"freq" :  7322,
                  "lfo"  :   127,
                  "env"  :  2655,
                  "lag"  : 0.765,
                  "res"  : 0.470,
                  "mix"  : 0.575},
       pw = 0.500,
       pwLfo = 0.000,
       noise = -99)

klstr(13, "Random-13", amp=-12,
       lfo = {"freq"    : 0.4187,
              "ratio"   : 1.0000,
              "xmod"    : 0.0000,
              "delay"   : 0.000,
              "depth"   : 0.000,
              "vibrato" : 0.000},
       env = {"gated"    : True,
              "attack"  : 0.000,
              "decay"   : 0.915,
              "sustain" : 0.510,
              "release" : 7.033},
       spread = {"depth" : 2.055,
                 "lfo"   : 0.000,
                 "env"   : 0.000},
       cluster = {"depth" : 0.148,
                  "lfo"   : 7.920,
                  "env"   : 0.000,
                  "lag"   : 0.000},
       filter_ = {"freq" :  8037,
                  "lfo"  :   684,
                  "env"  :     0,
                  "lag"  : 0.810,
                  "res"  : 0.288,
                  "mix"  : 0.828},
       pw = 0.960,
       pwLfo = 0.894,
       noise = -99)

klstr(14, "Random-14", amp=-12,
       lfo = {"freq"    : 0.4163,
              "ratio"   : 1.0000,
              "xmod"    : 0.0000,
              "delay"   : 2.597,
              "depth"   : 0.000,
              "vibrato" : 0.000},
       env = {"gated"    : True,
              "attack"  : 0.000,
              "decay"   : 0.799,
              "sustain" : 0.744,
              "release" : 6.024},
       spread = {"depth" : 2.117,
                 "lfo"   : 0.969,
                 "env"   : 0.000},
       cluster = {"depth" : 0.943,
                  "lfo"   : 0.563,
                  "env"   : 0.000,
                  "lag"   : 0.000},
       filter_ = {"freq" :  8545,
                  "lfo"  :   870,
                  "env"  :     0,
                  "lag"  : 0.655,
                  "res"  : 0.210,
                  "mix"  : 0.604},
       pw = 0.500,
       pwLfo = 0.000,
       noise = -99)

klstr(16, "Spinning", amp=-12,
       lfo = {"freq"    : 5.8710,
              "ratio"   : 1.0000,
              "xmod"    : 0.0000,
              "delay"   : 0.000,
              "depth"   : 0.000,
              "vibrato" : 0.000},
       env = {"gated"    : True,
              "attack"  : 0.000,
              "decay"   : 0.553,
              "sustain" : 0.945,
              "release" : 9.907},
       spread = {"depth" : 0.770,
                 "lfo"   : 0.000,
                 "env"   : 0.000},
       cluster = {"depth" : 0.638,
                  "lfo"   : 0.773,
                  "env"   : 0.000,
                  "lag"   : 0.000},
       filter_ = {"freq" :  7890,
                  "lfo"  :     0,
                  "env"  :     0,
                  "lag"  : 0.000,
                  "res"  : 0.649,
                  "mix"  : 0.925},
       pw = 0.500,
       pwLfo = 0.000,
       noise = -99)

klstr(17, "Sticks 2", amp=-12,
       lfo = {"freq"    : 1.1973,
              "ratio"   : 1.0000,
              "xmod"    : 0.0000,
              "delay"   : 1.970,
              "depth"   : 0.000,
              "vibrato" : 0.000},
       env = {"gated"    : True,
              "attack"  : 0.000,
              "decay"   : 0.039,
              "sustain" : 0.089,
              "release" : 0.076},
       spread = {"depth" : 3.483,
                 "lfo"   : 0.000,
                 "env"   : 0.315},
       cluster = {"depth" : 8.040,
                  "lfo"   : 6.232,
                  "env"   : 0.000,
                  "lag"   : 0.000},
       filter_ = {"freq" :  6376,
                  "lfo"  :     0,
                  "env"  :     0,
                  "lag"  : 0.000,
                  "res"  : 0.035,
                  "mix"  : 1.000},
       pw = 0.507,
       pwLfo = 0.175,
       noise = -99)
