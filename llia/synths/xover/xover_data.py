# llia.synths.xover.xover_data
#

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.util.lmath import coin, pick, rnd
from llia.performance_edit import performance
from llia.util.lmath import (coin,rnd,pick,random)
import llia.synths.xover.xover_constants as xcon

prototype = {
    "lfoFreq" : 1.0,       # Common freq tumber (0,99.999)
    "lfo2Ratio" : 1.0,     # MSB
    "lfo2Wave" : 0.0,      # slider (-1,+1)
    "lfoEnable" : 1.0,     # 1 enable, 0 disable
    "res" : 0,             # norm slider
    "xover" : 800,         # MSB
    "lfoToXover" : 0.0,    # norm slider
    "externToXover" : 0.0, # norm slider
    "minXover" : 200,      # exp slider
    "maxXover" : 20000,    # exp slider
    "filterBMix" : 0.0,    # norm slider
    "filterBRatio" : 1.0,  # MSB
    "filterBLag" : 0.0,    # norm slider
    "dryAmp" : 0.0,        # amp slider
    "filterAAmp" : 1.0,    # amp slider
    "filterBAmp" : 1.0,    # amp slider
    "dryPan" : 0.0,        # bEDi slider
    "filterAPan" : 0.0,    # bi slider
    "filterBPan" : 0.0,    # bi slider
    "xscale" : 1.0,        # linear slider (0,4)
    "xbias" : 0.0,         # linear slider (-4,4)
    "amp"   : 1.0}         # amp slider

class XOver(Program):

    def __init__(self, name):
        super(XOver, self).__init__(name, "XOver", prototype)
        self.performance = performance()

program_bank = ProgramBank(XOver("Init"))
program_bank.enable_undo = False
        
def xover(slot, name,
          lfoFreq = 1.0,
          lfo2Ratio = 1.0,
          lfo2Wave = 0.0,
          lfoEnable = 1.0,
          res = 0,
          xover = 800,
          lfoToXover = 0.0,
          externToXover = 0.0,
          minXover = 200,
          maxXover = 20000,
          filterBMix = 0.0,
          filterBRatio = 1.0,
          filterBLag = 0.0,
          dryAmp = 0.0,
          filterAAmp = 1.0,
          filterBAmp = 1.0,
          dryPan = 0.0,
          filterAPan = 0.0,
          filterBPan = 0.0,
          xscale = 1.0,
          xbias = 0.0,
          amp   = 1.0):
    p = XOver(name)
    p["lfoFreq"] = float(lfoFreq)
    p["lfo2Ratio"] = float(lfo2Ratio)
    p["lfo2Wave"] = float(lfo2Wave)
    p["lfoEnable"] = float(lfoEnable)
    p["res"] = float(res)
    p["xover"] = float(xover)
    p["lfoToXover"] = float(lfoToXover)
    p["externToXover"] = float(externToXover)
    p["minXover"] = float(minXover)
    p["maxXover"] = float(maxXover)
    p["filterBMix"] = float(filterBMix)
    p["filterBRatio"] = float(filterBRatio)
    p["filterBLag"] = float(filterBLag)
    p["dryAmp"] = float(dryAmp)
    p["filterAAmp"] = float(filterAAmp)
    p["filterBAmp"] = float(filterBAmp)
    p["dryPan"] = float(dryPan)
    p["filterAPan"] = float(filterAPan)
    p["filterBPan"] = float(filterBPan)
    p["xscale"] = float(xscale)
    p["xbias"] = float(xbias)
    p["amp"]   = float(amp)
    program_bank[slot] = p
    return p

def pp(program, slot=127):
    def fval(key):
        return float(program[key])
    pad = ' '*5
    acc = 'xover(%d, "%s",\n' % (slot, program.name)
    acc += "%slfoFreq = %5.3f,\n" % (pad, fval("lfoFreq"))
    acc += "%slfo2Ratio = %5.3f,\n" % (pad, fval("lfo2Ratio"))
    acc += "%slfo2Wave = %5.3f,\n" % (pad, fval("lfo2Wave"))
    acc += "%slfoEnable = %d,\n" % (pad, int(program["lfoEnable"]))
    acc += "%sres = %5.3f,\n" % (pad, fval("res"))
    acc += "%sxover = %5.3f,\n" % (pad, fval("xover"))
    acc += "%slfoToXover = %5.3f,\n" % (pad, fval("lfoToXover"))
    acc += "%sexternToXover = %5.3f,\n" % (pad, fval("externToXover"))
    acc += "%sminXover = %5.3f,\n" % (pad, fval("minXover"))
    acc += "%smaxXover = %5.3f,\n" % (pad, fval("maxXover"))
    acc += "%sfilterBMix = %5.3f,\n" % (pad, fval("filterBMix"))
    acc += "%sfilterBRatio = %5.3f,\n" % (pad, fval("filterBRatio"))
    acc += "%sfilterBLag = %5.3f,\n" % (pad, fval("filterBLag"))
    acc += "%sdryAmp = %5.3f,\n" % (pad, fval("dryAmp"))
    acc += "%sfilterAAmp = %5.3f,\n" % (pad, fval("filterAAmp"))
    acc += "%sfilterBAmp = %5.3f,\n" % (pad, fval("filterBAmp"))
    acc += "%sdryPan = %5.3f,\n" % (pad, fval("dryPan"))
    acc += "%sfilterAPan = %5.3f,\n" % (pad, fval("filterAPan"))
    acc += "%sfilterBPan = %5.3f,\n" % (pad, fval("filterBPan"))
    acc += "%sxscale = %5.3f,\n" % (pad, fval("xscale"))
    acc += "%sxbias = %5.3f,\n" % (pad, fval("xbias"))
    acc += "%samp = %5.3f)\n" % (pad, fval("amp"))
    return acc
   
def random_xover(slot=127, *_):
    lfrq = coin(0.75, rnd(), coin(0.75, rnd(10),rnd(100)))
    p = xover(slot, "Random",
              lfoFreq = lfrq,
              lfo2Ratio = pick(xcon.LFO_RATIOS)[0],
              lfo2Wave = coin(0.75, 0.5, rnd()),
              lfoEnable = coin(0.75, 1, 0),
              res = coin(0.75, rnd(0.5), rnd()),
              xover = pick(xcon.CROSSOVER_FREQUENCIES),
              lfoToXover = coin(0.50, 0, rnd()),
              externToXover = 0.0,
              minXover = xcon.CROSSOVER_FREQUENCIES[0],
              maxXover = xcon.CROSSOVER_FREQUENCIES[-1],
              filterBMix = rnd(),
              filterBRatio = pick(xcon.FILTER_B_RATIOS)[0],
              filterBLag = coin(0.50, rnd(), 0.0),
              dryAmp = coin(0.75, 0.5+rnd(0.5), coin(0.50, 0, rnd())),
              filterAAmp = coin(0.75, 0.5+rnd(0.5), coin(0.50, 0, rnd())),
              filterBAmp = coin(0.75, 0.5+rnd(0.5), coin(0.50, 0, rnd())),
              dryPan = 0.0,
              filterAPan = 0.0,
              filterBPan = 0.0,
              xscale = 1.0,
              xbias = 0.0)
    return p

xover(0, "Bypass",
     lfoFreq = 1.000,
     lfo2Ratio = 1.000,
     lfo2Wave = 0.000,
     lfoEnable = 1,
     res = 0.000,
     xover = 800.000,
     lfoToXover = 0.000,
     externToXover = 0.000,
     minXover = 200.000,
     maxXover = 20000.000,
     filterBMix = 0.000,
     filterBRatio = 1.000,
     filterBLag = 0.000,
     dryAmp = 1.000,
     filterAAmp = 0.000,
     filterBAmp = 0.000,
     dryPan = 0.000,
     filterAPan = -0.005,
     filterBPan = -0.005,
     xscale = 1.000,
     xbias = 0.000,
     amp = 1.000)

xover(1, "Endless Prairie",
     lfoFreq = 0.160,
     lfo2Ratio = 1.000,
     lfo2Wave = 0.492,
     lfoEnable = 1,
     res = 0.332,
     xover = 600.000,
     lfoToXover = 0.161,
     externToXover = 0.000,
     minXover = 200.000,
     maxXover = 20000.000,
     filterBMix = 0.472,
     filterBRatio = 2.000,
     filterBLag = 0.618,
     dryAmp = 1.000,
     filterAAmp = 0.562,
     filterBAmp = 0.562,
     dryPan = 0.000,
     filterAPan = 0.427,
     filterBPan = -0.357,
     xscale = 1.000,
     xbias = 0.000,
     amp = 1.000)

xover(2, "Mild 6",
     lfoFreq = 6.000,
     lfo2Ratio = 1.000,
     lfo2Wave = 0.477,
     lfoEnable = 1,
     res = 0.171,
     xover = 300.000,
     lfoToXover = 0.060,
     externToXover = 0.000,
     minXover = 200.000,
     maxXover = 20000.000,
     filterBMix = 0.000,
     filterBRatio = 1.000,
     filterBLag = 0.241,
     dryAmp = 1.000,
     filterAAmp = 0.251,
     filterBAmp = 0.282,
     dryPan = 0.000,
     filterAPan = 0.387,
     filterBPan = -0.417,
     xscale = 1.000,
     xbias = 0.000,
     amp = 1.000)

xover(3, "Slow Res",
     lfoFreq = 0.070,
     lfo2Ratio = 1.667,
     lfo2Wave = 0.497,
     lfoEnable = 1,
     res = 0.518,
     xover = 200.000,
     lfoToXover = 0.779,
     externToXover = 0.000,
     minXover = 200.000,
     maxXover = 20000.000,
     filterBMix = 0.513,
     filterBRatio = 1.000,
     filterBLag = 0.317,
     dryAmp = 0.708,
     filterAAmp = 1.000,
     filterBAmp = 1.000,
     dryPan = 0.000,
     filterAPan = 0.256,
     filterBPan = -0.196,
     xscale = 1.000,
     xbias = 0.000,
     amp = 1.000)

xover(4, "Coachwhip",
     lfoFreq = 10.100,
     lfo2Ratio = 0.250,
     lfo2Wave = 0.513,
     lfoEnable = 0,
     res = 0.191,
     xover = 300.000,
     lfoToXover = 0.090,
     externToXover = 0.000,
     minXover = 200.000,
     maxXover = 20000.000,
     filterBMix = 0.834,
     filterBRatio = 4.000,
     filterBLag = 0.241,
     dryAmp = 0.794,
     filterAAmp = 0.355,
     filterBAmp = 0.794,
     dryPan = 0.000,
     filterAPan = -0.005,
     filterBPan = -0.005,
     xscale = 1.000,
     xbias = 0.000,
     amp = 1.000)

xover(5, "Massasauga",
     lfoFreq = 15.000,
     lfo2Ratio = 0.125,
     lfo2Wave = 0.513,
     lfoEnable = 1,
     res = 0.191,
     xover = 300.000,
     lfoToXover = 0.085,
     externToXover = 0.000,
     minXover = 200.000,
     maxXover = 20000.000,
     filterBMix = 0.834,
     filterBRatio = 1.000,
     filterBLag = 0.241,
     dryAmp = 0.794,
     filterAAmp = 0.562,
     filterBAmp = 0.447,
     dryPan = 0.000,
     filterAPan = -0.005,
     filterBPan = -0.005,
     xscale = 1.000,
     xbias = 0.000,
     amp = 1.000)

xover(6, "Swamp Rabbit",
     lfoFreq = 0.100,
     lfo2Ratio = 0.125,
     lfo2Wave = 0.487,
     lfoEnable = 1,
     res = 0.518,
     xover = 400.000,
     lfoToXover = 0.749,
     externToXover = 0.000,
     minXover = 200.000,
     maxXover = 20000.000,
     filterBMix = 0.834,
     filterBRatio = 1.000,
     filterBLag = 0.487,
     dryAmp = 0.000,
     filterAAmp = 1.000,
     filterBAmp = 1.000,
     dryPan = 0.000,
     filterAPan = 0.000,
     filterBPan = 0.000,
     xscale = 1.000,
     xbias = 0.000,
     amp = 1.000)

xover(7, "Ultra Slow Mod",
     lfoFreq = 0.010,
     lfo2Ratio = 1.333,
     lfo2Wave = 0.513,
     lfoEnable = 1,
     res = 0.312,
     xover = 800.000,
     lfoToXover = 0.427,
     externToXover = 0.000,
     minXover = 200.000,
     maxXover = 20000.000,
     filterBMix = 0.779,
     filterBRatio = 1.000,
     filterBLag = 0.402,
     dryAmp = 0.000,
     filterAAmp = 1.000,
     filterBAmp = 1.000,
     dryPan = 0.000,
     filterAPan = 0.000,
     filterBPan = 0.000,
     xscale = 1.000,
     xbias = 0.000,
     amp = 1.000)

