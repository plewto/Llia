# llia.synths.stepfilter.sf_data
# 2016.06.11

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.util.lmath import clip, db_to_amp
from llia.performance_edit import performance

prototype = {
    "dryAmp" : 0.0,
    "dryPan" : 0.0,
    "amp" : 1.0,
    "clockFreq" : 1,
    "r1" : 0.5,
    "r2" : 0.75,
    "r3" : 1.00,
    "r4" : 2.00,
    "r5" : 3.00,
    "r6" : 4.00,
    "r7" : 5.00,
    "r8" : 6.00,
    "a1" : 0.00,
    "a2" : 0.00,
    "a3" : 1.00,
    "a4" : 0.00,
    "a5" : 0.00,
    "a6" : 0.00,
    "a7" : 0.00,
    "a8" : 0.00,
    "aLag" : 0.00,
    "aMin" : 100,
    "aMax" : 2000,
    "aRes" : 0.3,
    "aPan" : -0.75,
    "aAmp" : 1.0,
    "b1" : 0.00,
    "b2" : 0.00,
    "b3" : 0.00,
    "b4" : 1.00,
    "b5" : 0.00,
    "b6" : 0.00,
    "b7" : 0.00,
    "b8" : 0.00,
    "bLag" : 0.00,
    "bMin" : 100,
    "bMax" : 2000,
    "bRes" : 0.30,
    "bPan" : -0.75,
    "bAmp" : 1.0,
    "panLfoFreq" : 1.00,
    "panLfoDry" : 0.00,
    "panLfoA" : 0.00,
    "panLfoB" : 0.00,
    "panLfoBRatio" : 1.00}

class StepFilter(Program):

    def __init__(self, name):
        super(StepFilter, self).__init__(name, "StepFilter", prototype)

INIT_PROGRAM = StepFilter("Init");
program_bank = ProgramBank(INIT_PROGRAM)
program_bank.enable_undo = False

def fill (lst, template):
    acc = []
    for i, v in enumerate(template):
        try:
            acc.append(lst[i])
        except IndexError:
            acc.append(v)
    return acc

def fclip(n, mn, mx):
    return float(clip(n, mn, mx))

def sfilter(slot, name,
            clockFreq = 1.000,
            r = [0.500, 0.750, 1.000, 2.000, 3.000, 4.000, 5.000, 6.000],
            a = [0.000, 0.000, 1.000, 1.000, 0.000, 0.000, 0.000, 0.000],
            b = [0.000, 0.500, 1.000, 0.000, 1.000, 0.500, 0.000, 0.000],
            alag = 0.2, arange=[100, 2000], ares = 0.2, 
            blag = 0.2, brange=[100, 2000], bres = 0.3,
            lfofreq = 1.00,             # panLFO
            apan = [-0.75, 0.00],       # [fixed-pos, lfo-mod]
            bpan = [+0.75, 0.00, 1.00], # [fixed-pos, lfo-mod, lfo-freq-ratio]
            drypan = [0.00, 0.00],      # [fixed-pos, lfo-mod]
            mix = [0.00, 1.00, 1.00],   # [dry, a, b]
            amp =  1.00):               # overall amp
    p = StepFilter(name)
    r = fill(r, [0.5, 0.75, 1, 2, 3, 4, 5, 6])
    a = fill(a, [0, 0, 1, 1, 0, 0, 0, 0])
    b = fill(b, [0, 0, 0, 1, 1, 0, 0, 0])
    p["clockFreq"] = fclip(clockFreq, 0.01, 10)
    p["aLag"] = fclip(alag, 0, 1)
    p["aRes"] = fclip(ares, 0, 1)
    arange = fill(arange, [100, 2000])
    p["aMin"] = fclip(arange[0], 100, 16000)
    p["aMax"] = fclip(arange[1], 100, 16000)
    p["bLag"] = fclip(blag, 0, 1)
    p["bRes"] = fclip(bres, 0, 1)
    brange = fill(brange, [100, 2000])
    p["bMin"] = fclip(brange[0], 100, 16000)
    p["bMax"] = fclip(brange[1], 100, 16000)
    p["panLfoFreq"] = fclip(lfofreq, 0.01, 10)
    p["aPan"] = fclip(apan[0], -1, 1)
    p["panLfoA"] = fclip(apan[1], 0, 1)
    p["bPan"] = fclip(bpan[0], -1, 1)
    p["panLfoB"] = fclip(bpan[1], 0, 1)
    p["panLfoBRatio"] = fclip(bpan[2], 0.01, 10)
    drypan = fill(drypan, [0.0, 0.0])
    p["dryPan"] = fclip(drypan[0], -1, 1)
    p["dryLfoPan"] = fclip(drypan[1], -1, 1)
    p["dryMix"] = fclip(mix[0], 0, 1)
    p["aMix"] = fclip(mix[1], 0, 1)
    p["bMix"] = fclip(mix[2], 0, 1)
    p["amp"] = fclip(amp, 0, 1)
    for i in range(8):
        rk = "r%d" % i
        ak = "a%d" % i
        bk = "b%d" % i
        p[rk] = fclip(r[i], 0.125, 12)
        p[ak] = fclip(a[i], 0, 1)
        p[bk] = fclip(b[i], 0, 1)
    p.performance = performance()
    program_bank[slot] = p
    return p

sfilter(  0, "Init",
          clockFreq = 1.000,
          r = [0.500, 0.750, 1.000, 2.000, 3.000, 4.000, 5.000, 6.000],
          a = [0.000, 0.000, 1.000, 1.000, 0.000, 0.000, 0.000, 0.000],
          b = [0.000, 0.500, 1.000, 0.000, 1.000, 0.500, 0.000, 0.000],
          alag = 0.2, arange=[100, 2000], ares = 0.2, 
          blag = 0.2, brange=[100, 2000], bres = 0.3,
          lfofreq = 1.00,             # panLFO
          apan = [-0.75, 0.00],       # [fixed-pos, lfo-mod]
          bpan = [+0.75, 0.00, 1.00], # [fixed-pos, lfo-mod, lfo-freq-ratio]
          drypan = [0.00, 0.00],      # [fixed-pos, lfo-mod]
          mix = [0.00, 1.00, 1.00],   # [dry, a, b]
          amp =  1.00)                # overall amp

sfilter(  1, "Step1",
          clockFreq = 1.000,
          r = [0.500, 0.750, 1.000, 2.000, 3.000, 4.000, 5.000, 6.000],
          a = [0.000, 0.000, 1.000, 0.500, 0.300, 0.250, 0.200, 0.100],
          b = [1.000, 1.000, 1.000, 0.000, 0.000, 0.000, 0.000, 0.000],
          alag = 0.2, arange=[100, 2000], ares = 0.2, 
          blag = 0.2, brange=[100, 2000], bres = 0.3,
          lfofreq = 1.00,             # panLFO
          apan = [0.00 , 0.50],       # [fixed-pos, lfo-mod]
          bpan = [0.00 , 0.50, 1.00], # [fixed-pos, lfo-mod, lfo-freq-ratio]
          drypan = [0.00, 0.00],
          mix = [0.00, 1.00, 1.00],   # [dry, a, b]
          amp =  1.00)                # overall amp

sfilter(  2, "Spastic",
       clockFreq = 1.7858,
       r = [0.750, 1.000, 2.000, 3.000, 4.000, 5.000, 6.000, 6.000],
       a = [0.487, 0.787, 0.527, 0.440, 0.319, 0.862, 0.355, 0.000],
       b = [0.764, 0.056, 0.000, 0.266, 0.330, 0.315, 0.000, 0.000],
       alag = 0.039, arange = [ 200, 3000], ares = 0.254,
       blag = 0.119, brange = [16000,  800], bres = 0.346,
       lfofreq = 1.786,
       apan = [-1.000, 0.530],
       bpan = [+1.000, 0.000, 3.000],
       drypan = [-1.000, 0.000],
       mix = [0.000, 1.000, 1.000],
       amp = 1.000)

sfilter(  3, "OffBeat",
       clockFreq = 2.0907,
       r = [1.058, 1.119, 1.183, 1.251, 1.324, 1.400, 1.481, 6.000],
       a = [0.000, 0.000, 0.000, 0.000, 0.000, 1.000, 0.000, 0.000],
       b = [0.000, 0.998, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000],
       alag = 0.028, arange = [ 100, 4000], ares = 0.806,
       blag = 0.082, brange = [16000, 4000], bres = 0.799,
       lfofreq = 6.272,
       apan = [+1.000, 0.492],
       bpan = [-1.000, 0.908, 3.000],
       drypan = [+1.000, 0.000],
       mix = [0.000, 1.000, 1.000],
       amp = 1.000)

sfilter(  4, "Persian Blue",
       clockFreq = 0.5709,
       r = [0.750, 1.000, 2.000, 3.000, 4.000, 5.000, 6.000, 6.000],
       a = [0.000, 0.000, 0.558, 0.000, 0.000, 0.370, 0.189, 0.000],
       b = [0.000, 0.676, 0.140, 0.000, 0.000, 0.000, 0.000, 0.000],
       alag = 0.194, arange = [ 100,  800], ares = 0.187,
       blag = 0.164, brange = [16000,  800], bres = 0.576,
       lfofreq = 3.425,
       apan = [-1.000, 0.202],
       bpan = [-1.000, 0.746, 0.250],
       drypan = [+1.000, 0.000],
       mix = [0.000, 1.000, 1.000],
       amp = 1.000)

sfilter(  5, "Fast",
       clockFreq = 1.7966,
       r = [0.750, 1.000, 2.000, 3.000, 4.000, 5.000, 6.000, 6.000],
       a = [0.000, 0.669, 0.384, 0.640, 0.000, 0.755, 0.198, 0.000],
       b = [0.000, 0.000, 0.020, 0.000, 0.000, 0.000, 0.036, 0.000],
       alag = 0.119, arange = [ 400, 4000], ares = 0.614,
       blag = 0.000, brange = [16000, 2000], bres = 0.359,
       lfofreq = 7.186,
       apan = [-1.000, 0.773],
       bpan = [+1.000, 0.241, 0.250],
       drypan = [+1.000, 0.000],
       mix = [0.000, 1.000, 1.000],
       amp = 1.000)

sfilter(  6, "Purell",
       clockFreq = 1.4158,
       r = [0.750, 1.000, 2.000, 3.000, 4.000, 5.000, 6.000, 6.000],
       a = [0.062, 0.000, 0.000, 0.000, 0.682, 0.000, 0.356, 0.000],
       b = [0.000, 0.480, 0.000, 0.378, 0.837, 0.000, 0.994, 0.000],
       alag = 0.000, arange = [ 100,  800], ares = 0.494,
       blag = 0.162, brange = [16000,  800], bres = 0.064,
       lfofreq = 0.708,
       apan = [+1.000, 0.900],
       bpan = [-1.000, 0.566, 0.250],
       drypan = [-1.000, 0.000],
       mix = [0.000, 1.000, 1.000],
       amp = 1.000)

sfilter(   7, "Chitin",
       clockFreq = 2.3399,
       r = [0.750, 1.000, 2.000, 3.000, 4.000, 5.000, 6.000, 6.000],
       a = [0.716, 0.000, 0.000, 0.000, 0.263, 0.000, 0.000, 0.000],
       b = [0.812, 0.000, 0.621, 0.061, 0.035, 0.711, 0.000, 0.000],
       alag = 0.185, arange = [ 100,  500], ares = 0.504,
       blag = 0.000, brange = [16000, 4000], bres = 0.831,
       lfofreq = 0.585,
       apan = [+1.000, 0.543],
       bpan = [-1.000, 0.435, 0.500],
       drypan = [-1.000, 0.000],
       mix = [0.000, 1.000, 1.000],
       amp = 1.000)
