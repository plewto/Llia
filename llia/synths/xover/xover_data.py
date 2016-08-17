# llia.synths.xover.xover_data
#

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.util.lmath import clip, db_to_amp, amp_to_db
from llia.performance_edit import performance
from llia.util.lmath import (coin,rnd,pick,random)

LF_RATIOS = (0.125, 0.250, 0.333, 0.325, 0.50, 0.625, 0.667, 0.75, 0.875,
             1.0, 1.333, 1.50, 1.667, 1.75,
             2.0, 2.5, 3, 4, 5, 6, 7, 8, 9, 12, 16)

CROSSOVER_FREQUENCIES = (100, 125, 160, 200, 250, 315, 400, 500, 630, 800,
                        1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000,
                        6300, 8000, 10000, 12500, 16000)

prototype = {
    "xScale" : 1.0,           # external control signal scale (0..4)
    "xBias" : 0.0,            # external control bias (-4..+4)
    "lfoFreq" : 1.0,          # Reference LFO frequency in Hertz.
    "crossover" : 500,        # crossover freq in Hertz.
    "minCrossover" : 200,     # min/max crossover frequency in Hz
    "maxCrossover" : 16000,
    "xoverLfoRatio" : 1.0,    # crossover LFO frequency relative to lfoFreq  (LFO 1)
    "xoverLfoDepth" : 0.0,    # LFO -> crossover freq (0..1)
    "xoverX" : 0.0,           # external -> crossover freq (0..1)
    "res" : 0.5,              # resonace (0..1)
    "lpMode" : 1.0,           # 0 -> bandpass, 1 -> lowpass
    "lpMix" : 1.0,            # lowpass filter static gain (0..2)
    "lpMixLfo" : 0.0,         # LFO -> lowpass mix (0..1)
    "lpMixX" : 0.0,           # external -> lowpass mix (0..1)
    "lpLfoRatio" : 1.0,       # lowpass LFO freq ratio
    "hpMode" : 1.0,           # 0 -> band-reject, 1 -> highpass
    "hpMix" : 1.0,            #   highpass LFO is 90 degrees
    "hpMixLfo" : 0.0,         #   relative to lowpass
    "hpMixX" : 0.0,
    "hpLfoRatio" : 1.0,
    "dryMix" : 0.0,           # dry signal gain (0..2)
    "amp" : 1.0               # Overall gain (applies to lowpass, highpass and dry), (0..2)
}

class XOver(Program):

    def __init__(self, name):
        super(XOver, self).__init__(name, "XOver", prototype)
        self.performance = performance()

program_bank = ProgramBank(XOver("Init"))
program_bank.enable_undo = False
        
def fclip (n, mn=0, mx=1):
    return float(clip(n, mn, mx))

def iclip (n, mn=0, mx=1):
    return int(clip(n, mn, mx))


def xover(slot, name, 
          xScale = 1.0,
          xBias = 0.0,
          lfoFreq = 1.0,
          crossover = 500,
          minCrossover = 200,
          maxCrossover = 16000,
          xoverLfoRatio = 1.0,
          xoverLfoDepth = 0.0,
          xoverX = 0.0,
          res = 0.5,
          lpMode = 1.0,
          lpMix = 0,
          lpMixLfo = 0.0,
          lpMixX = 0.0,
          lpLfoRatio = 1.0,
          hpMode = 1.0,
          hpMix = 0,
          hpMixLfo = 0.0,
          hpMixX = 0.0,
          hpLfoRatio = 1.0,
          dryMix = -99,
          amp = 0):
    p = XOver(name)
    p["xScale"] = float(xScale)
    p["xBias"] = float(xBias)
    p["lfoFreq"] = float(lfoFreq)
    p["crossover"] = int(crossover)
    p["minCrossover"] = int(min(minCrossover, maxCrossover))
    p["maxCrossover"] = int(max(minCrossover, maxCrossover))
    p["xoverLfoRatio"] = float(xoverLfoRatio)
    p["xoverLfoDepth"] = float(xoverLfoDepth)
    p["xoverX"] = float(xoverX)
    p["res"] = float(res)
    p["lpMode"] = float(lpMode)
    p["lpMixLfo"] = float(lpMixLfo)
    p["lpMixX"] = float(lpMixX)
    p["lpLfoRatio"] = float(lpLfoRatio)
    p["hpMode"] = float(hpMode)
    p["hpMixLfo"] = float(hpMixLfo)
    p["hpMixX"] = float(hpMixX)
    p["hpLfoRatio"] = float(hpLfoRatio)
    p["dryMix"] = float(db_to_amp(dryMix))
    p["hpMix"] = float(db_to_amp(hpMix))
    p["lpMix"] = float(db_to_amp(lpMix))
    p["amp"] = float(db_to_amp(amp))
    program_bank[slot] = p
    return p
    

def pp(program, slot=127):

    def db(key):
        return int(amp_to_db(program[key]))

    def fval(key):
        return float(program[key])

    def ival(key):
        return int(program[key])

    pad = ' '*5
    acc = 'xover(%d, "%s",\n' % (slot, program.name)
    acc += '%scrossover = %d,\n' % (pad, ival('crossover'))
    acc += '%sminCrossover = %d,\n' % (pad, ival("minCrossover"))
    acc += '%smaxCrossover = %d,\n' % (pad, ival("maxCrossover"))
    acc += '%sxScale = %5.4f,\n' % (pad, fval('xScale'))
    acc += '%sxBias = %5.4f,\n' % (pad, fval('xBias'))
    acc += '%slfoFreq = %5.4f,\n' % (pad, fval('lfoFreq'))
    acc += '%sxoverLfoRatio = %5.4f,\n' % (pad, fval('xoverLfoRatio'))
    acc += '%sxoverLfoDepth = %5.4f,\n' % (pad, fval('xoverLfoDepth'))
    acc += '%sxoverX = %5.4f,\n' % (pad, fval('xoverX'))
    acc += '%sres = %5.4f,\n' % (pad, fval('res'))
    acc += '%slpMode = %5.4f,\n' % (pad, fval('lpMode'))
    acc += '%slpMixLfo = %5.4f,\n' % (pad, fval('lpMixLfo'))
    acc += '%slpMixX = %5.4f,\n' % (pad, fval('lpMixX'))
    acc += '%slpLfoRatio = %5.4f,\n' % (pad, fval('lpLfoRatio'))
    acc += '%shpMode = %5.4f,\n' % (pad, fval('hpMode'))
    acc += '%shpMixLfo = %5.4f,\n' % (pad, fval('hpMixLfo'))
    acc += '%shpMixX = %5.4f,\n' % (pad, fval('hpMixX'))
    acc += '%shpLfoRatio = %5.4f,\n' % (pad, fval('hpLfoRatio'))
    acc += '%shpMix = %d,\n' % (pad, db('hpMix'))
    acc += '%slpMix = %d,\n' % (pad, db('lpMix'))
    acc += '%sdryMix = %d,\n' % (pad, db('dryMix'))
    acc += '%samp = %d)\n' % (pad, db('amp'))
    return acc



def random_xover(slot=127, *_):
    low_ratios = [0.125, 0.250, 0.250, 0.333, 0.333, 0.5, 0.5, 0.5,
                  0.667, 0.667, 0.75, 0.87]
    med_ratios = [1.0, 1.0, 1.0, 1.0, 1.333, 1.5, 1.5, 1.5, 1.667,
                  1.75, 2.0, 2.0, 2.0, 2.5, 3.0, 3.0]
    high_ratios = [4, 4, 4, 4, 4, 5, 5, 6, 6, 6, 7, 8, 9, 12, 16]

    def pick_ratio():
        rs = coin(0.50, pick(med_ratios),
                  coin(0.75, pick(low_ratios), pick(high_ratios)))
        return rs

    lpmode = coin(0.75, 1, 0)
    if lpmode == 0:
        hpmode = 1
    else:
        hpmode = coin(0.75, 1, 0)

    mixLfoDepth = coin(0.75, 0.5+rnd(0.5), rnd())

    mn_crossover = int(coin(0.75, 200, rnd(1500)))
    mx_crossover = mn_crossover + int(coin(0.75, 10000, rnd(5000)))

    rs = xover(slot, "Random",
               xScale = 1.0,
               xBias = 0.0,
               lfoFreq = coin(0.75, rnd(), coin(0.5, rnd(0.2), rnd(10))),
               crossover = coin(0.75, pick(CROSSOVER_FREQUENCIES[6:-6]),
                                pick(CROSSOVER_FREQUENCIES)),
               minCrossover = mn_crossover,
               maxCrossover = mx_crossover,
               xoverLfoRatio = pick_ratio(),
               xoverLfoDepth = coin(0.5, 0, rnd()),
               xoverX = 0.0,
               res = rnd(),
               lpMode = lpmode,
               lpMix = coin(0.80, pick([0, 0, 0, -3, -3, -6, -6]), -99),
               lpMixLfo = mixLfoDepth,
               lpLfoRatio = pick_ratio(),
               lpMixX = 0.0,
               hpMode = hpmode,
               hpMix = coin(0.80, pick([0, 0, 0, -3, -3, -6, -6]), -99),
               hpMixLfo = coin(0.8, mixLfoDepth, rnd()),
               hpMixX = 0.0,
               hpLfoRatio = pick_ratio(),
               dryMix = coin(0.8, -99, pick([0, -3, -6, -9, -12])),
               amp = -12)
    return rs
               
               
               
xover(0, "Bypass",
     crossover = 500,
     minCrossover = 200,
     maxCrossover = 16000,
     xScale = 1.0000,
     xBias = 0.0000,
     lfoFreq = 1.0000,
     xoverLfoRatio = 1.0000,
     xoverLfoDepth = 0.0000,
     xoverX = 0.0000,
     res = 0.5000,
     lpMode = 1.0000,
     lpMixLfo = 0.0000,
     lpMixX = 0.0000,
     lpLfoRatio = 1.0000,
     hpMode = 1.0000,
     hpMixLfo = 0.0000,
     hpMixX = 0.0000,
     hpLfoRatio = 1.0000,
     hpMix = -99,
     lpMix = -99,
     dryMix = 0,
     amp = 0)

xover(1, "Slow And Mild",
     crossover = 1000,
     minCrossover = 200,
     maxCrossover = 16000,
     xScale = 1.0000,
     xBias = 0.0000,
     lfoFreq = 1.0000,
     xoverLfoRatio = 1.0000,
     xoverLfoDepth = 0.0000,
     xoverX = 0.0000,
     res = 0.5000,
     lpMode = 1.0000,
     lpMixLfo = 1.0000,
     lpMixX = 0.0000,
     lpLfoRatio = 1.0000,
     hpMode = 1.0000,
     hpMixLfo = 1.0000,
     hpMixX = 0.0000,
     hpLfoRatio = 1.0000,
     hpMix = 0,
     lpMix = 0,
     dryMix = -99,
     amp = 0)

xover(2, "4 Hz Mild Wha",
     crossover = 400,
     minCrossover = 200,
     maxCrossover = 16000,
     xScale = 1.0000,
     xBias = 0.0000,
     lfoFreq = 4.0000,
     xoverLfoRatio = 0.3250,
     xoverLfoDepth = 0.1307,
     xoverX = 0.0000,
     res = 0.5628,
     lpMode = 1.0000,
     lpMixLfo = 1.0000,
     lpMixX = 0.0000,
     lpLfoRatio = 1.0000,
     hpMode = 1.0000,
     hpMixLfo = 1.0000,
     hpMixX = 0.0000,
     hpLfoRatio = 1.0000,
     hpMix = 0,
     lpMix = 0,
     dryMix = -99,
     amp = 0)

xover(3, "0.66 Hz Wha",
     crossover = 315,
     minCrossover = 200,
     maxCrossover = 10200,
     xScale = 1.0000,
     xBias = 0.0000,
     lfoFreq = 0.6600,
     xoverLfoRatio = 1.6670,
     xoverLfoDepth = 0.9849,
     xoverX = 0.0000,
     res = 0.5126,
     lpMode = 0.8643,
     lpMixLfo = 0.7487,
     lpMixX = 0.0000,
     lpLfoRatio = 0.6670,
     hpMode = 1.0000,
     hpMixLfo = 0.7487,
     hpMixX = 0.0000,
     hpLfoRatio = 0.7500,
     hpMix = 0,
     lpMix = -6,
     dryMix = -99,
     amp = 0)

xover(4, "No Highpass",
     crossover = 800,
     minCrossover = 200,
     maxCrossover = 16000,
     xScale = 1.0000,
     xBias = 0.0000,
     lfoFreq = 1.0000,
     xoverLfoRatio = 1.0000,
     xoverLfoDepth = 0.5427,
     xoverX = 0.0000,
     res = 0.3618,
     lpMode = 0.4724,
     lpMixLfo = 0.0000,
     lpMixX = 0.0000,
     lpLfoRatio = 7.0000,
     hpMode = 1.0000,
     hpMixLfo = 0.0000,
     hpMixX = 0.0000,
     hpLfoRatio = 2.0000,
     hpMix = -99,
     lpMix = 0,
     dryMix = -99,
     amp = 0)

xover(5, "Only Highpass",
     crossover = 630,
     minCrossover = 200,
     maxCrossover = 16000,
     xScale = 1.0000,
     xBias = 0.0000,
     lfoFreq = 1.0000,
     xoverLfoRatio = 1.0000,
     xoverLfoDepth = 0.9347,
     xoverX = 0.0000,
     res = 0.3618,
     lpMode = 1.0000,
     lpMixLfo = 0.0000,
     lpMixX = 0.0000,
     lpLfoRatio = 0.1250,
     hpMode = 1.0000,
     hpMixLfo = 0.0000,
     hpMixX = 0.0000,
     hpLfoRatio = 0.1250,
     hpMix = 0,
     lpMix = -99,
     dryMix = -99,
     amp = 0)

xover(6, "XOver 6",
     crossover = 630,
     minCrossover = 200,
     maxCrossover = 16000,
     xScale = 1.0000,
     xBias = 0.0000,
     lfoFreq = 0.6600,
     xoverLfoRatio = 6.0000,
     xoverLfoDepth = 0.1759,
     xoverX = 0.0000,
     res = 0.3568,
     lpMode = 1.0000,
     lpMixLfo = 0.5879,
     lpMixX = 0.0000,
     lpLfoRatio = 4.0000,
     hpMode = 1.0000,
     hpMixLfo = 0.5879,
     hpMixX = 0.0000,
     hpLfoRatio = 1.0000,
     hpMix = 3,
     lpMix = -3,
     dryMix = -99,
     amp = 0)

xover(7, "Syncopated",
     crossover = 1000,
     minCrossover = 200,
     maxCrossover = 16000,
     xScale = 1.0000,
     xBias = 0.0000,
     lfoFreq = 0.8200,
     xoverLfoRatio = 9.0000,
     xoverLfoDepth = 0.6734,
     xoverX = 0.0000,
     res = 0.7186,
     lpMode = 1.0000,
     lpMixLfo = 1.0000,
     lpMixX = 0.0000,
     lpLfoRatio = 2.5000,
     hpMode = 1.0000,
     hpMixLfo = 1.0000,
     hpMixX = 0.0000,
     hpLfoRatio = 1.0000,
     hpMix = -7,
     lpMix = 0,
     dryMix = -99,
     amp = 0)

xover(8, "Very Slow Crossfade",
     crossover = 630,
     minCrossover = 100,
     maxCrossover = 16000,
     xScale = 1.0000,
     xBias = 0.0000,
     lfoFreq = 0.1000,
     xoverLfoRatio = 1.0000,
     xoverLfoDepth = 0.2613,
     xoverX = 0.0000,
     res = 0.4975,
     lpMode = 1.0000,
     lpMixLfo = 1.0000,
     lpMixX = 0.0000,
     lpLfoRatio = 1.0000,
     hpMode = 1.0000,
     hpMixLfo = 1.0000,
     hpMixX = 0.0000,
     hpLfoRatio = 1.3330,
     hpMix = -6,
     lpMix = -3,
     dryMix = -99,
     amp = 0)

