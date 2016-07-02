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
    p["dryAmp"] = fclip(mix[0], 0, 1)
    p["aAmp"] = fclip(mix[1], 0, 1)
    p["bAmp"] = fclip(mix[2], 0, 1)
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

sfilter(  0, "Step1",
       clockFreq = 0.8281,
       r = [1.000, 2.000, 3.000, 4.000, 5.000, 6.000, 7.000, 6.000],
       a = [0.500, 0.340, 0.250, 0.200, 0.170, 0.140, 0.000, 0.000],
       b = [1.000, 0.000, 0.460, 0.820, 0.000, 0.000, 0.000, 0.000],
       alag = 0.101, arange = [ 300, 2400], ares = 0.362,
       blag = 0.085, brange = [ 200, 1600], bres = 0.864,
       lfofreq = 0.967,
       apan = [-0.005, 0.497],
       bpan = [-0.508, 0.497, 1.000],
       drypan = [-0.005, 0.000],
       mix = [0.000, 0.658, 0.972],
       amp = 1.000)

sfilter(  1, "Spastic",
       clockFreq = 0.5161,
       r = [2.000, 3.000, 4.000, 5.000, 6.000, 7.000, 8.000, 6.000],
       a = [1.000, 0.001, 1.000, 0.001, 1.000, 0.001, 0.020, 0.000],
       b = [0.001, 1.000, 1.000, 1.000, 0.000, 0.000, 0.000, 0.000],
       alag = 0.035, arange = [ 400, 2400], ares = 0.829,
       blag = 0.116, brange = [ 400, 4800], bres = 0.342,
       lfofreq = 1.764,
       apan = [-0.648, 0.528],
       bpan = [+0.588, 0.000, 3.000],
       drypan = [-1.000, 0.000],
       mix = [0.027, 1.000, 0.556],
       amp = 1.000)

sfilter(  2, "OffBeat",
       clockFreq = 0.5161,
       r = [3.000, 0.125, 1.000, 2.000, 4.000, 6.000, 8.000, 6.000],
       a = [0.800, 0.000, 0.001, 0.001, 0.001, 0.001, 1.000, 0.000],
       b = [0.000, 0.001, 0.630, 0.001, 0.001, 0.820, 0.000, 0.000],
       alag = 0.256, arange = [ 300, 3200], ares = 0.764,
       blag = 0.412, brange = [ 300, 3200], bres = 0.799,
       lfofreq = 2.874,
       apan = [+0.457, 0.156],
       bpan = [-0.618, 0.593, 3.000],
       drypan = [-0.005, 0.000],
       mix = [0.069, 0.366, 0.845],
       amp = 1.000)

sfilter(  3, "Persian Blue",
       clockFreq = 0.5508,
       r = [2.000, 3.000, 4.000, 5.000, 6.000, 6.000, 6.000, 6.000],
       a = [1.000, 0.000, 0.000, 1.000, 1.000, 0.000, 0.001, 0.000],
       b = [1.000, 0.000, 0.001, 0.000, 0.000, 0.001, 0.000, 0.000],
       alag = 0.191, arange = [ 100,  800], ares = 0.186,
       blag = 0.161, brange = [ 800, 12800], bres = 0.573,
       lfofreq = 3.394,
       apan = [-1.000, 0.201],
       bpan = [-1.000, 0.744, 0.500],
       drypan = [+1.000, 0.000],
       mix = [0.000, 1.000, 0.293],
       amp = 1.000)

sfilter(  4, "Machine",
       clockFreq = 2.5965,
       r = [0.750, 1.000, 2.000, 3.000, 4.000, 5.000, 6.000, 6.000],
       a = [0.550, 1.000, 1.000, 0.020, 1.000, 1.000, 1.000, 0.000],
       b = [0.001, 0.001, 1.000, 1.000, 0.000, 0.000, 0.000, 0.000],
       alag = 0.598, arange = [ 600, 2400], ares = 0.362,
       blag = 0.000, brange = [ 100,  800], bres = 0.186,
       lfofreq = 3.879,
       apan = [-1.000, 0.191],
       bpan = [-1.000, 0.000, 0.750],
       drypan = [+1.000, 0.000],
       mix = [0.000, 0.799, 0.945],
       amp = 1.000)

sfilter(  5, "Westcott",
       clockFreq = 2.2497,
       r = [0.250, 0.375, 0.500, 3.000, 3.125, 3.250, 3.500, 6.000],
       a = [0.530, 0.130, 1.000, 0.000, 0.000, 0.000, 0.000, 0.000],
       b = [0.030, 0.001, 1.000, 1.000, 0.000, 0.000, 0.000, 0.000],
       alag = 0.166, arange = [ 100,  400], ares = 0.573,
       blag = 0.000, brange = [ 400,  800], bres = 0.176,
       lfofreq = 3.394,
       apan = [+0.407, 0.849],
       bpan = [-0.417, 0.141, 3.000],
       drypan = [-0.005, 0.000],
       mix = [0.005, 1.000, 0.639],
       amp = 1.000)

sfilter(  6, "Chitin",
       clockFreq = 2.3191,
       r = [2.000, 3.000, 4.000, 5.000, 6.000, 7.000, 8.000, 6.000],
       a = [0.000, 0.000, 1.000, 0.270, 0.810, 0.000, 0.000, 0.000],
       b = [1.000, 1.000, 1.000, 1.000, 0.001, 0.000, 0.000, 0.000],
       alag = 0.181, arange = [ 300, 6400], ares = 0.503,
       blag = 0.000, brange = [ 300, 3200], bres = 0.960,
       lfofreq = 0.897,
       apan = [+1.000, 0.543],
       bpan = [-0.337, 0.432, 0.500],
       drypan = [-0.015, 0.000],
       mix = [0.088, 0.099, 1.000],
       amp = 1.000)

