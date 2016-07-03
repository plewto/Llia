# llia.synths.stepfilter.sf_data
# 2016.06.11

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.util.lmath import clip, db_to_amp
from llia.performance_edit import performance
import llia.synths.stepfilter.sf_constants as sfcon

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
            r = sfcon.DEFAULT_GAMUT,
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
        j = i + 1
        rk = "r%d" % j
        ak = "a%d" % j
        bk = "b%d" % j
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

sfilter(  1, "Westcott",
       clockFreq = 0.5854,
       r = [0.500, 0.750, 1.000, 2.000, 3.000, 4.000, 5.000, 6.000],
       a = [1.000, 0.000, 1.000, 1.000, 0.000, 0.000, 0.000, 0.000],
       b = [0.070, 0.000, 0.000, 1.000, 1.000, 0.000, 0.000, 0.000],
       alag = 0.714, arange = [ 200, 2400], ares = 0.814,
       blag = 0.950, brange = [2400, 3200], bres = 0.186,
       lfofreq = 1.903,
       apan = [-0.005, 0.146],
       bpan = [-0.005, 0.000, 3.000],
       drypan = [+1.000, 0.000],
       mix = [0.277, 0.556, 0.658],
       amp = 1.000)

sfilter(  2, "Leatherman",
       clockFreq = 1.2789,
       r = [1.000, 2.000, 3.000, 4.000, 5.000, 6.000, 7.000, 8.000],
       a = [0.520, 0.310, 0.100, 1.000, 0.000, 0.000, 0.000, 0.000],
       b = [0.080, 0.380, 0.770, 0.360, 0.350, 1.000, 0.000, 0.000],
       alag = 0.000, arange = [ 600, 1200], ares = 0.693,
       blag = 0.126, brange = [ 600, 3200], bres = 0.176,
       lfofreq = 2.596,
       apan = [+0.427, 0.000],
       bpan = [-0.548, 0.000, 1.000],
       drypan = [-0.015, 0.000],
       mix = [0.040, 0.512, 1.000],
       amp = 0.695)

sfilter(  3, "Tivole",
       clockFreq = 0.2387,
       r = [1.000, 2.000, 3.000, 4.000, 5.000, 6.000, 7.000, 8.000],
       a = [0.350, 0.960, 0.660, 1.000, 0.000, 0.000, 0.000, 0.000],
       b = [1.000, 0.001, 0.001, 1.000, 1.000, 0.001, 0.000, 0.000],
       alag = 0.151, arange = [ 600, 9600], ares = 0.859,
       blag = 0.050, brange = [ 200,  400], bres = 0.844,
       lfofreq = 0.100,
       apan = [+0.487, 0.000],
       bpan = [-0.487, 0.533, 3.000],
       drypan = [+0.065, 0.000],
       mix = [0.050, 1.000, 1.000],
       amp = 0.756)

sfilter(  4, "Purell",
       clockFreq = 0.7241,
       r = [1.000, 2.000, 3.000, 4.000, 5.000, 6.000, 7.000, 8.000],
       a = [0.850, 0.001, 0.550, 0.001, 0.001, 0.000, 0.000, 0.000],
       b = [0.001, 0.001, 0.590, 0.890, 0.530, 0.790, 0.001, 0.001],
       alag = 0.261, arange = [ 200, 3200], ares = 0.201,
       blag = 0.291, brange = [ 600, 6400], bres = 0.362,
       lfofreq = 1.418,
       apan = [-0.598, 0.000],
       bpan = [+0.437, 0.000, 0.500],
       drypan = [-0.025, 0.000],
       mix = [0.091, 0.234, 0.445],
       amp = 1.000)

sfilter(  5, "Becks",
       clockFreq = 2.5271,
       r = [0.125, 0.250, 0.375, 0.500, 3.000, 3.125, 3.250, 3.500],
       a = [1.000, 1.000, 1.000, 1.000, 0.000, 0.000, 0.000, 0.000],
       b = [0.001, 0.001, 0.001, 0.001, 1.000, 0.820, 0.700, 0.410],
       alag = 0.111, arange = [ 600, 2400], ares = 0.291,
       blag = 0.302, brange = [ 400, 1200], bres = 0.372,
       lfofreq = 0.169,
       apan = [+0.347, 0.533],
       bpan = [-0.307, 0.080, 0.750],
       drypan = [-0.005, 0.000],
       mix = [0.198, 0.248, 0.605],
       amp = 0.409)

sfilter(  6, "Shuffle",
       clockFreq = 1.7643,
       r = [0.500, 0.750, 1.000, 2.000, 3.000, 4.000, 5.000, 6.000],
       a = [0.550, 0.420, 0.130, 1.000, 1.000, 0.000, 0.000, 0.000],
       b = [0.620, 0.930, 0.990, 1.000, 1.000, 1.000, 0.000, 0.000],
       alag = 0.342, arange = [1200, 4800], ares = 0.347,
       blag = 0.131, brange = [1200, 2400], bres = 0.121,
       lfofreq = 0.343,
       apan = [+1.000, 0.000],
       bpan = [+1.000, 0.296, 3.000],
       drypan = [+1.000, 0.000],
       mix = [0.000, 0.999, 0.588],
       amp = 1.000)

sfilter(  7, "Sudo",
       clockFreq = 2.9779,
       r = [0.125, 0.250, 0.375, 0.500, 3.000, 1.000, 2.000, 4.000],
       a = [0.780, 0.850, 0.280, 1.000, 1.000, 0.000, 0.000, 0.000],
       b = [0.001, 0.001, 0.001, 0.320, 0.500, 0.970, 0.780, 0.900],
       alag = 0.955, arange = [ 100,  300], ares = 0.447,
       blag = 1.000, brange = [1200, 4800], bres = 0.176,
       lfofreq = 1.591,
       apan = [+0.236, 0.804],
       bpan = [-0.176, 0.417, 0.500],
       drypan = [-0.216, 0.000],
       mix = [0.000, 0.433, 1.000],
       amp = 1.000)
