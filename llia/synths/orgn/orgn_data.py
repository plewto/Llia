
from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.util.lmath import clip, db_to_amp
from llia.performance_edit import performance

prototype = {"amp" : 0.05,
             "vfreq" : 5.0,
             "vdelay" : 0.0,
             "vdepth" : 0.0,
             "vibrato" : 0.0,
             "chorus" : 0.0,
             "chorusDelay" : 2.0,
             "r1" : 1.00,
             "r2" : 1.00,
             "r3" : 2.00,
             "r4" : 4.00,
             "amp1" : 1.00,
             "amp2" : 1.00,
             "amp3" : 1.00,
             "amp4" : 1.00,
             "cattack" : 0.0,
             "cdecay" : 0.0,
             "csustain" : 1.0,
             "crelease" : 0.0,
             "mattack" : 2.0,
             "mdecay" : 0.0,
             "msustain" : 1.0,
             "mrelease" : 4.0,
             "modulationDepth" : 1.0,
             "xToModulationDepth" : 0.0,
             "xToPitch" : 0.0}

class Orgn(Program):

    def __init__(self, name):
        super(Orgn, self).__init__(name, "Orgn", prototype)

program_bank = ProgramBank(Orgn("Init"))

def _fill(lst, template):
    acc = []
    for i,d in enumerate(template):
        try:
            v = lst[i]
        except IndexError:
            v = d
        acc.append(v)
    return acc


def orgn(slot, name, amp=-12,
         cenv = [0.00, 0.00, 1.00, 0.00], # ADSR
         menv = [0.00, 0.00, 1.00, 0.00],
         op1 = [1.00, 0],   # freq-ratio, amp(db)
         op2 = [1.00, 0],   # freq-ratio, modulation-depth
         op3 = [2.00, -99], # freq-ratio, amp(db)
         op4 = [2.00, 0],   # freq-ratio, modulation-depth
         vibrato = [5.00, 0.00, 0.00, 0.00], # freq, delay, depth, x->pitch
         chorus = [0.00, 0.00], # delay, depth
         mod_depth = [1.0, 0.0]): # [depth, x->depth]
    cenv = _fill(cenv, [0.0, 0.0, 1.0, 0.0])
    menv = _fill(menv, [0.0, 0.0, 1.0, 0.0])
    op1 = _fill(op1, [1.0, 0])
    op2 = _fill(op2, [1.0, 0.0])
    op3 = _fill(op3, [2.0, -99])
    op4 = _fill(op4, [2.0, 0.0])
    vibrato = _fill(vibrato, [5.0, 0.0, 0.0, 0.0])
    chorus = _fill(chorus, [0.0, 0.0])
    mod_depth = _fill(mod_depth, [1.0, 0.0])
    p = Orgn(name)
    p.performance = performance()
    p["amp"] = db_to_amp(amp)
    for i,param in enumerate(("cattack","cdecay","csustain","crelease")):
        p[param] = float(cenv[i])
    for i,param in enumerate(("mattack","mdecay","msustain","mrelease")):
        p[param] = float(menv[i])
    p["r1"] = float(op1[0])
    p["r2"] = float(op2[0])
    p["r3"] = float(op3[0])
    p["r4"] = float(op4[0])
    p["amp1"] = float(db_to_amp(op1[1]))
    p["amp2"] = float(op2[1])
    p["amp3"] = float(db_to_amp(op3[1]))
    p["amp4"] = float(op4[1])
    for i,param in enumerate(("vfreq","vdelay","vdepth","xToPitch")):
        v = float(vibrato[i])
        p[param] = v
    p["chorusDelay"] = float(chorus[0])
    p["chorus"] = float(chorus[1])
    p["modulationDepth"] = float(mod_depth[0])
    p["xToModulationDepth"] = float(mod_depth[1])
    program_bank[slot] = p
    return p
   
    
    
    
orgn(0  , "Boxholm", amp=-12,
         cenv = [0.339,0.128,0.900,0.252],
         menv = [0.330,0.449,0.668,0.394],
         op1 = [1.5000,   0],
         op2 = [2.2500, 0.083],
         op3 = [1.5000,  -9],
         op4 = [0.5000, 0.355],
         vibrato = [8.476,0.000,0.000,0.0000],
         chorus = [0.000, 0.000],
         mod_depth = [1.000, 0.000])

orgn(1, "Buckeye", amp = -12,
     cenv = [0.00, 0.10, 0.70, 2.25],
     menv = [0.20, 0.50, 0.70, 1.00],
     op1 = [1.00, 0],
     op2 = [1.00, 0.5],
     op3 = [1.50, -6],
     op4 = [1.50, 0.3],
     vibrato = [6.00, 1.00, 0.00, 0.05],
     chorus = [0.0, 0.0],
     mod_depth = [1.0, 0.0])

orgn(2  , "High8", amp=-12,
         cenv = [4.045,1.924,0.846,1.819],
         menv = [1.334,2.315,0.523,1.085],
         op1 = [8.0000,   0],
         op2 = [8.0000, 0.740],
         op3 = [2.0000,  -9],
         op4 = [8.0000, 0.355],
         vibrato = [4.149,1.585,0.000,0.0000],
         chorus = [1.340, 0.000],
         mod_depth = [1.000, 0.000])

orgn(3, "Fm Ensemble Winds", amp=-12,
         cenv = [4.074,3.274,0.098,0.567],
         menv = [3.870,1.362,0.582,0.907],
         op1 = [3.0000,   0],
         op2 = [2.0000, 0.230],
         op3 = [1.0000, -12],
         op4 = [0.5000, 0.251],
         vibrato = [2.385,2.140,0.000,0.0000],
         chorus = [0.911, 0.000],
         mod_depth = [1.000, 0.000])

orgn(4, "Thin Gate", amp=-18,
         cenv = [0.000,0.000,1.000,0.000],
         menv = [0.000,0.000,1.000,0.000],
         op1 = [8.0000,   0],
         op2 = [1.0000, 0.835],
         op3 = [4.0000,  -9],
         op4 = [5.0000, 0.355],
         vibrato = [6.161,0.000,0.022,0.0000],
         chorus = [0.000, 0.000],
         mod_depth = [1.000, 0.000])

orgn(5, "Low Reed", amp=-12,
         cenv = [0.371,0.372,0.756,0.177],
         menv = [0.178,0.415,0.753,0.036],
         op1 = [0.5000,   0],
         op2 = [6.0000, 0.812],
         op3 = [0.5000,   5],
         op4 = [2.0000, 1.995],
         vibrato = [2.799,0.505,0.096,0.0000],
         chorus = [0.000, 0.000],
         mod_depth = [1.000, 0.000])

orgn(6, "Release Trigger", amp=-12,
         cenv = [2.787,0.973,0.199,0.788],
         menv = [0.000,0.000,1.000,0.000],
         op1 = [2.0000,   0],
         op2 = [5.0000, 0.335],
         op3 = [5.0000,  -9],
         op4 = [2.0000, 0.355],
         vibrato = [2.925,0.000,0.017,0.0000],
         chorus = [0.293, 0.000],
         mod_depth = [1.000, 0.000])

orgn(7, "Combo 1", amp=-12,
         cenv = [0.000,0.000,1.000,0.000],
         menv = [0.000,0.000,1.000,0.000],
         op1 = [3.0000,   0],
         op2 = [1.0000, 0.213],
         op3 = [0.5000, -12],
         op4 = [1.5000, 0.251],
         vibrato = [5.00,3.00,0.00,0.0000],
         chorus = [1.506, 0.00],
         mod_depth = [1.000, 0.000])

orgn(  8, "DeepVibe", amp=-12,
         cenv = [6.000,0.000,1.000,6.000],
         menv = [6.000,0.000,1.000,6.000],
         op1 = [1.0000, -99],
         op2 = [1.0000, 0.000],
         op3 = [1.9988,   0],
         op4 = [1.9988, 1.000],
         vibrato = [6.985,1.000,0.894,0.0452],
         chorus = [0.000, 1.000],
         mod_depth = [1.000, 0.000])

orgn(  9, "Combo 2", amp=-11,
         cenv = [0.000,0.000,1.000,0.000],
         menv = [0.000,0.000,1.000,0.000],
         op1 = [1.0000,  -6],
         op2 = [3.0000, 0.362],
         op3 = [2.0000,  -9],
         op4 = [2.0000, 0.324],
         vibrato = [5.830,3.520,0.176,0.0000],
         chorus = [0.920, 0.156],
         mod_depth = [1.000, 0.000])
