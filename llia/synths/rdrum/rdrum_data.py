# llia.synths.rdrum.rdrum_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.util.lmath import clip, db_to_amp
from llia.performance_edit import performance

prototype = {
    "amp" : 0.1,           # linear overall amplitude,  0 <= amp <= 2  (+6db)                    
    "aRatio" : 1.000,      # tone A freq ratio, 0.25 <= aRatio <= 8                            
    "aAttack" : 0.001,     # tone A attack time,  0 <= aAttack <= 6                              
    "aDecay" : 0.7500,     # tone A decay time, 0 <= aDecay <= 6                              
    "aAmp" : 1.000,        # tone A relative linear amplitude,  0 <= amp <= 1
    "aBend" : 0.000,       # tone A bend,  -1 <= aBend <= +1                                
    "aTone" : 0.000,       # tone A wave,  0 = sine, 1 = clipped
    "aVelocity" : 0.000,   # tone A velocity sensitivity 0 <= vsens <= 1
    "bRatio" : 1.000,      # tone B freq ratio, 1 <= bRatio <= 8                             
    "bAttack" : 0.001,     # tone B attack time, 0 <= bAttack <= 6                              
    "bDecay" : 0.50,       # tone B decay time, 0 <= bDecay <= 6                            
    "bAmp" : 0.750,        # tone B relative linear amplitude,  0 <= amp <= 1
    "bBend" : 0.000,       # tone B bend, -1 <= bBend <= +1                              
    "bTune" : 1.0,         # tone B Tune, 0 <= tune <= 4, 0= ~unison, 1=Risset, >1 other.
    "bVelocity" : 0.000,   # tone B velocity sensitivity 0 <= vsens <= 1
    "noiseRatio" : 1.000,  # noise filter track, 0 <= track <= 16                                  
    "noiseBias" : 0,       # noise filer floor, HZ, 0 <= bias 9999
    "noiseAttack" : 0.001, # noise attack time,  0 <= attack <= 6                                  
    "noiseDecay" : 0.500,  # noise decay time,   0 <= decay <= 6                                 
    "noiseAmp" : 0.000,    # noise relative linear amplitude, 0 <= amp <= 1
    "noiseRes" : 0,        # noise filter resonance,  0 <= res <= 1                          
    "noiseBend" : 0.00,     # noise filter modulation, -1 <= bend <= +1
    "noiseVelocity" : 0.000,   # noise velocity sensitivity 0 <= vsens <= 1
}

class Rdrum(Program):

    def __init__(self, name):
        super(Rdrum, self).__init__(name, "Rdrum", prototype)

program_bank = ProgramBank(Rdrum("Init"))
program_bank.enable_undo = False


def fget(d, key, default, mn=0.0, mx=1):
    v = d.get(key, default)
    return float(clip(v, mn, mx))

def _envTime(d, param, default):
    v = clip(float(d.get(param, default)), 0, 6)
    return v

def _freq_ratio(d, param, default):
    v = abs(float(d.get(param, default)))
    return v

def _bend(d, param):
    v = clip(float(d.get(param, 0)), -1, 1)
    return v

def _norm(d, param, default):
    v = clip(float(d.get(param, default)), 0, 1)
    return v

def _db(d, param):
    v = clip(int(db_to_amp(d.get(param, 0))), 0, 2)
    return v

def rdrum(slot, name, amp=-12,
          a = {"ratio"  : 1.000,
               "attack" : 0.000,
               "decay"  : 0.750,
               "bend"   : 0.0,
               "tone"   : 0.0,
               "amp"    : 0,
               "velocity" : 0.0},
          b = {"ratio"  : 1.000,
               "attack" : 0.000,
               "decay"  : 0.375,
               "bend"   : 0.000,
               "tune"   : 1.000,
               "amp"    : 0,
               "velocity" : 0.0},
          noise = {"ratio" : 6.0,
                   "bias"  : 0,
                   "attack" : 0.001,
                   "decay"  : 0.500,
                   "res"    : 0.50,
                   "bend"   : 0.00,
                   "amp"    : -99,
                   "velocity" : 0.0},
          remarks = ""):
    p = Rdrum(name)
    p.remarks = remarks
    p.performance = performance()
    p["amp"] = db_to_amp(amp)
    p["aRatio"] = _freq_ratio(a, "ratio", 1.0)
    p["aAttack"] = _envTime(a, "attack", 0.001)
    p["aDecay"] = _envTime(a, "decay", 0.75)
    p["aBend"] = _bend(a, "bend")
    p["aTone"] = _norm(a, "bend", 0)
    p["aAmp"] = _db(a, "amp")
    p["aVelocity"] = _norm(a, "velocity", 0)
    p["bRatio"] = _freq_ratio(b, "ratio", 1.0)
    p["bAttack"] = _envTime(b, "attack", 0.001)
    p["bDecay"] = _envTime(b, "decay", 0.75)
    p["bBend"] = _bend(b, "bend")
    p["bTune"] = clip(float(b.get("tune", 0)), 0, 4)
    p["bAmp"] = _db(b, "amp")
    p["bVelocity"] = _norm(b, "velocity", 0)
    p["noiseRatio"] = _freq_ratio(noise, "ratio", 6)
    p["noiseBias"] = int(clip(noise.get("bias", 0), 0, 9999))
    p["noiseAttack"] = _envTime(noise, "attack", 0.001)
    p["noiseDecay"] = _envTime(noise, "decay", 0.5)
    p["noiseBend"] = _bend(noise, "bend")
    p["noiseRes"] = _norm(noise, "res", 0)
    p["noiseAmp"] = _db(noise, "amp")
    p["noiseVelocity"] = _norm(noise, "velocity", 0)
    
    program_bank[slot] = p
    return p

rdrum(  0, "Risset 1", amp=-6,
        a = {"ratio"  : 1.0000,
             "attack" : 0.000,
             "decay"  : 0.750,
             "bend"   : 0.000 ,
             "tone"   : 0.000,
             "velocity" : 0.357,
             "amp"    : 0},
        b = {"ratio"  : 1.0000,
             "attack" : 0.000,
             "decay"  : 0.500,
             "bend"   : 0.000 ,
             "tune"   : 1.0000,
             "velocity" : 1.000,
             "amp"    : -3},
        noise = {"ratio"  : 0.0000,
                 "attack" : 0.000,
                 "decay"  : 0.643,
                 "bend"   : -0.055,
                 "res"    : 0.4472,
                 "velocity" : 0.442,
                 "amp"    : -9})

rdrum(  1, "Risset 2", amp=0,
        a = {"ratio"  : 0.5000,
             "attack" : 0.000,
             "decay"  : 0.208,
             "bend"   : 0.000 ,
             "tone"   : 0.995,
             "velocity" : 0.719,
             "amp"    : 0},
        b = {"ratio"  : 0.5000,
             "attack" : 0.005,
             "decay"  : 1.228,
             "bend"   : 0.000 ,
             "tune"   : 1.0200,
             "velocity" : 0.834,
             "amp"    : -8},
        noise = {"ratio"  : 0.0000,
                 "attack" : 0.032,
                 "decay"  : 2.274,
                 "bend"   : -0.025,
                 "res"    : 0.4476,
                 "velocity" : 0.759,
                 "amp"    : -10})

rdrum(  2, "Risset 3", amp=-6,
        a = {"ratio"  : 1.0000,
             "attack" : 0.000,
             "decay"  : 0.750,
             "bend"   : 0.095 ,
             "tone"   : 0.095,
             "velocity" : 0.678,
             "amp"    : 0},
        b = {"ratio"  : 1.0000,
             "attack" : 0.000,
             "decay"  : 0.500,
             "bend"   : 0.095 ,
             "tune"   : 1.0000,
             "velocity" : 0.000,
             "amp"    : -99},
        noise = {"ratio"  : 3.0000,
                 "attack" : 0.032,
                 "decay"  : 0.750,
                 "bend"   : -0.005,
                 "res"    : 0.4476,
                 "velocity" : 0.734,
                 "amp"    : -2})

rdrum(  3, "Click1", amp=0,
        a = {"ratio"  : 6.0000,
             "attack" : 0.000,
             "decay"  : 0.007,
             "bend"   : -0.005,
             "tone"   : 0.000,
             "velocity" : 0.000,
             "amp"    : 0},
        b = {"ratio"  : 4.0000,
             "attack" : 0.005,
             "decay"  : 0.005,
             "bend"   : -0.005,
             "tune"   : 3.2400,
             "velocity" : 1.000,
             "amp"    : -3},
        noise = {"ratio"  : 0.0000,
                 "attack" : 0.000,
                 "decay"  : 0.035,
                 "bend"   : 1.000 ,
                 "res"    : 0.4476,
                 "velocity" : 0.000,
                 "amp"    : -7})

rdrum(  4, "Tone1", amp=-2,
        a = {"ratio"  : 2.0200,
             "attack" : 0.000,
             "decay"  : 1.609,
             "bend"   : 0.000 ,
             "tone"   : 0.000,
             "velocity" : 0.965,
             "amp"    : -23},
        b = {"ratio"  : 1.0000,
             "attack" : 0.002,
             "decay"  : 2.000,
             "bend"   : 0.000 ,
             "tune"   : 0.0000,
             "velocity" : 0.578,
             "amp"    : 0},
        noise = {"ratio"  : 4.0000,
                 "attack" : 0.076,
                 "decay"  : 0.003,
                 "bend"   : 1.000 ,
                 "res"    : 0.9196,
                 "velocity" : 0.000,
                 "amp"    : -99})

rdrum(  5, "LongBendDown", amp=-5,
        a = {"ratio"  : 2.0000,
             "attack" : 0.000,
             "decay"  : 1.532,
             "bend"   : 0.779 ,
             "tone"   : 0.000,
             "velocity" : 0.648,
             "amp"    : 0},
        b = {"ratio"  : 2.0100,
             "attack" : 0.000,
             "decay"  : 1.688,
             "bend"   : 0.859 ,
             "tune"   : 0.0000,
             "velocity" : 1.000,
             "amp"    : -99},
        noise = {"ratio"  : 1.0000,
                 "attack" : 1.749,
                 "decay"  : 0.083,
                 "bend"   : 1.000 ,
                 "res"    : 0.4925,
                 "velocity" : 0.000,
                 "amp"    : -99})

rdrum(  6, "NoiseSwash", amp=-6,
        a = {"ratio"  : 1.0000,
             "attack" : 0.001,
             "decay"  : 0.750,
             "bend"   : 0.000 ,
             "tone"   : 0.000,
             "velocity" : 0.000,
             "amp"    : 0},
        b = {"ratio"  : 4.0000,
             "attack" : 0.001,
             "decay"  : 0.500,
             "bend"   : 0.000 ,
             "tune"   : 0.0000,
             "velocity" : 0.000,
             "amp"    : -99},
        noise = {"ratio"  : 4.0000,
                 "attack" : 0.961,
                 "decay"  : 2.077,
                 "bend"   : 1.000 ,
                 "res"    : 0.8844,
                 "velocity" : 0.000,
                 "amp"    : 0})

rdrum(  7, "Bender", amp=-9,
        a = {"ratio"  : 1.0000,
             "attack" : 0.649,
             "decay"  : 0.804,
             "bend"   : 0.000 ,
             "tone"   : 0.000,
             "velocity" : 0.000,
             "amp"    : 0},
        b = {"ratio"  : 3.0000,
             "attack" : 4.354,
             "decay"  : 0.003,
             "bend"   : -0.910,
             "tune"   : 0.0000,
             "velocity" : 0.000,
             "amp"    : 0},
        noise = {"ratio"  : 0.0000,
                 "attack" : 1.098,
                 "decay"  : 0.086,
                 "bend"   : 1.000 ,
                 "res"    : 0.3719,
                 "velocity" : 0.000,
                 "amp"    : -99})

rdrum(  8, "Shaker1", amp=-3,
        a = {"ratio"  : 2.0000,
             "attack" : 0.006,
             "decay"  : 0.001,
             "bend"   : 0.000 ,
             "tone"   : 0.000,
             "velocity" : 0.000,
             "amp"    : -99},
        b = {"ratio"  : 1.0000,
             "attack" : 0.005,
             "decay"  : 0.001,
             "bend"   : -0.005,
             "tune"   : 0.0000,
             "velocity" : 0.000,
             "amp"    : -99},
        noise = {"ratio"  : 4.0000,
                 "attack" : 0.056,
                 "decay"  : 0.047,
                 "bend"   : 1.000 ,
                 "res"    : 0.2010,
                 "velocity" : 0.548,
                 "amp"    : 0})

rdrum(  9, "Clave", amp=0,
        a = {"ratio"  : 16.0400,
             "attack" : 0.001,
             "decay"  : 0.180,
             "bend"   : 0.000 ,
             "tone"   : 0.000,
             "velocity" : 0.000,
             "amp"    : 0},
        b = {"ratio"  : 4.0000,
             "attack" : 0.001,
             "decay"  : 0.510,
             "bend"   : 0.000 ,
             "tune"   : 1.7000,
             "velocity" : 0.000,
             "amp"    : -99},
        noise = {"ratio"  : 1.0400,
                 "attack" : 0.000,
                 "decay"  : 0.510,
                 "bend"   : 0.000 ,
                 "res"    : 0.7186,
                 "velocity" : 0.000,
                 "amp"    : -99})

rdrum( 10, "Kick Drum", amp=0,
        a = {"ratio"  : 2.0000,
             "attack" : 0.000,
             "decay"  : 0.044,
             "bend"   : 0.005 ,
             "tone"   : 0.000,
             "velocity" : 1.000,
             "amp"    : -5},
        b = {"ratio"  : 1.0000,
             "attack" : 0.001,
             "decay"  : 1.620,
             "bend"   : 0.000 ,
             "tune"   : 0.3400,
             "velocity" : 0.472,
             "amp"    : 0},
        noise = {"ratio"  : 1.0000,
                 "attack" : 0.001,
                 "decay"  : 0.500,
                 "bend"   : -0.015,
                 "res"    : 0.0000,
                 "velocity" : 0.000,
                 "amp"    : 3})

rdrum( 11, "Metal Bell", amp=-3,
        a = {"ratio"  : 2.0000,
             "attack" : 0.005,
             "decay"  : 0.750,
             "bend"   : 0.025 ,
             "tone"   : 0.211,
             "velocity" : 1.000,
             "amp"    : -14},
        b = {"ratio"  : 4.0000,
             "attack" : 0.000,
             "decay"  : 0.500,
             "bend"   : 0.000 ,
             "tune"   : 2.7400,
             "velocity" : 0.000,
             "amp"    : 0},
        noise = {"ratio"  : 6.0000,
                 "attack" : 0.000,
                 "decay"  : 0.007,
                 "bend"   : -0.005,
                 "res"    : 0.0000,
                 "velocity" : 0.523,
                 "amp"    : 0})

