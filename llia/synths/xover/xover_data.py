# llia.synths.xover.xover_data
#

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.util.lmath import clip, db_to_amp, amp_to_db
from llia.performance_edit import performance

prototype = {
    "res" : 0.5,                # Resonace (0, 1)
    "crossover" : 500,          # Filter crossover (100, 16000) Hz
    "lfoCrossover" : 0.0,       # LFO -> crossover (0, 1)
    "lfoCrossoverRatio" : 1.0,  # Freq ratio for crossover LFO > 0
    "lfoFreq" : 1.0,            # Primary LFO frequency in Hz
    "lpMode" : 1.0,             # Filter 1 mode (0=bandpass, 1=lowpass)
    "lpMod" : 1.0,              # LFO -> filter1 amp mod (0, 1)
    "lpAmp" : 1.0,              # Filter1 linear amplitude.
    "hpMode" : 1.0,             # Filter 2 mode (0=bandpass, 1=highpass)
    "hpMod"  : 1.0,             # LFO -> filter2 amp (90 out of phase with lp)
    "hpAmp"  : 1.0,             # Filter 2 linear amp.
    "spread" : 0.0,             # Filter1, filter2, pan (0=center, 1=left & right)
    "lfoPanMod" : 0.0,          # LFO -> filter pan
    "lfoPanRatio" : 1.0,        # Panning LFO frequency ratio
    "dryAmp" : 1.0,             # Dry signal, linear amp
    "dryPan" : 0.0,             # Dry signal pan position (-1,+1)
    "amp" : 1.0                 # Main linear amp.
    }



class XOver(Program):

    def __init__(self, name):
        super(XOver, self).__init__(name, "XOver", prototype)
        self.performance = performance()

INIT_PROGRAM = XOver("Init");
program_bank = ProgramBank(INIT_PROGRAM)
program_bank.enable_undo = False
        
def fclip (n, mn=0, mx=1):
    return float(clip(n, mn, mx))

def iclip (n, mn=0, mx=1):
    return int(clip(n, mn, mx))

def xover(slot, name,
          lfoFreq = 1.0,
          crossover = 800,
          lfoCrossover = 0.00,
          lfoCrossoverRatio = 1.00,
          res = 0.5,
          lpMode = 1.00,
          lpMod = 1.00,
          lpAmp = 0,
          hpMode = 1.00,
          hpMod = 1.00,
          hpAmp = 0,
          spread = 0.75,
          lfoPanMod = 0.00,
          lfoPanRatio = 1.00,
          dryAmp = 0,
          dryPan = 0,
          amp = 0):
    p = XOver(name)
    p["res"] = fclip(res)
    p["crossover"] = iclip(crossover, 100, 16000)
    p["lfoCrossover"] = fclip(lfoCrossover)
    p["lfoCrossoverRatio"] = float(abs(lfoCrossoverRatio))
    p["lfoFreq"] = float(abs(lfoFreq))
    p["lpMode"] = fclip(lpMode)
    p["lpMod"] = fclip(lpMod)
    p["lpAmp"] = db_to_amp(lpAmp)
    p["hpMode"] = fclip(hpMode)
    p["hpMod"] = fclip(hpMod)
    p["hpAmp"] = db_to_amp(hpAmp)
    p["spread"] = fclip(spread, -1, 1)
    p["lfoPanMod"] = fclip(lfoPanMod, -1, 1)
    p["lfoPanRatio"] = abs(float(lfoPanRatio))
    p["dryAmp"] = db_to_amp(dryAmp)
    p["dryPan"] = fclip(dryPan, -1, 1)
    p["amp"] = db_to_amp(amp)
    program_bank[slot] = p
    return p


def pp_xover(program, slot=127):
    
    def db(key):
        return int(amp_to_db(program[key]))
    
    def fval(key):
        return float(program[key])

    def ival(key):
        return int(program[key])

    pad = ' '*5
    acc = ''
    acc = 'xover(%3d, "%s",\n' % (slot, program.name)
    acc += '%slfoFreq = %5.4f,\n' % (pad, fval('lfoFreq'))
    frmt = '%scrossover = %4d, lfoCrossover = %5.3f,\n'
    acc += frmt % (pad, ival('crossover'), fval('lfoCrossover'))
    frmt = '%slfoCrossoverRatio = %5.3f, res = %5.3f,\n'
    acc += frmt % (pad, fval('lfoCrossoverRatio'), fval('res'))
    frmt = '%slpMode = %5.3f, lpMod = %5.3f, lpAmp = %2d,\n'
    acc += frmt % (pad, fval('lpMode'), fval('lpMod'), db('lpAmp'))
    frmt = '%shpMode = %5.3f, hpMod = %5.3f, hpAmp = %2d,\n'
    acc += frmt % (pad, fval('hpMode'), fval('hpMod'), db('hpAmp'))
    frmt = '%sspread = %5.3f, lfoPanMod = %5.3f, lfoPanRatio = %5.3f,\n'
    acc += frmt % (pad, fval('spread'), fval('lfoPanMod'), fval('lfoPanRatio'))
    frmt = '%sdryAmp = %d, dryPan = %5.3f,\n'
    acc += frmt % (pad, db('dryAmp'), fval('dryPan'))
    frmt = '%samp = %d)\n'
    acc += frmt % (pad, db('amp'))
    return acc


xover(  0, "Init",
     lfoFreq = 1.0000,
     crossover =  500, lfoCrossover = 0.000,
     lfoCrossoverRatio = 1.000, res = 0.500,
     lpMode = 1.000, lpMod = 1.000, lpAmp =  0,
     hpMode = 1.000, hpMod = 1.000, hpAmp =  0,
     spread = 0.000, lfoPanMod = 0.000, lfoPanRatio = 1.000,
     dryAmp = 0, dryPan = 0.000,
     amp = 0)

xover(  1, "One",
     lfoFreq = 1.4000,
     crossover = 1600, lfoCrossover = 0.141,
     lfoCrossoverRatio = 1.000, res = 0.387,
     lpMode = 0.000, lpMod = 1.000, lpAmp =  0,
     hpMode = 0.000, hpMod = 1.000, hpAmp =  0,
     spread = 0.638, lfoPanMod = 0.000, lfoPanRatio = 1.000,
     dryAmp = -4, dryPan = 0.000,
     amp = 0)

xover(  2, "Slow Fade",
     lfoFreq = 0.1500,
     crossover =  800, lfoCrossover = 0.000,
     lfoCrossoverRatio = 1.000, res = 0.663,
     lpMode = 1.000, lpMod = 1.000, lpAmp =  0,
     hpMode = 0.372, hpMod = 1.000, hpAmp =  0,
     spread = -1.000, lfoPanMod = 0.583, lfoPanRatio = 1.000,
     dryAmp = -99, dryPan = 0.000,
     amp = 0)

xover(  3, "Three",
     lfoFreq = 2.5000,
     crossover =  600, lfoCrossover = 0.915,
     lfoCrossoverRatio = 0.125, res = 0.432,
     lpMode = 1.000, lpMod = 1.000, lpAmp = -16,
     hpMode = 1.000, hpMod = 1.000, hpAmp =  0,
     spread = -0.055, lfoPanMod = 0.859, lfoPanRatio = 1.000,
     dryAmp = 0, dryPan = 0.000,
     amp = 0)

xover(  4, "Slow & Deep",
     lfoFreq = 0.3300,
     crossover =  400, lfoCrossover = 0.246,
     lfoCrossoverRatio = 1.500, res = 0.518,
     lpMode = 1.000, lpMod = 1.000, lpAmp =  0,
     hpMode = 0.583, hpMod = 1.000, hpAmp =  0,
     spread = -0.005, lfoPanMod = 0.558, lfoPanRatio = 0.250,
     dryAmp = -99, dryPan = 0.000,
     amp = 0)

xover(  5, "Fast & Shallow",
     lfoFreq = 6.6000,
     crossover =  600, lfoCrossover = 0.286,
     lfoCrossoverRatio = 0.500, res = 0.497,
     lpMode = 0.000, lpMod = 1.000, lpAmp =  0,
     hpMode = 1.000, hpMod = 1.000, hpAmp = -3,
     spread = 0.000, lfoPanMod = 0.528, lfoPanRatio = 0.750,
     dryAmp = 0, dryPan = 0.000,
     amp = 0)

xover(  6, "Bandpass 1k",
     lfoFreq = 0.9200,
     crossover = 1200, lfoCrossover = 0.111,
     lfoCrossoverRatio = 1.000, res = 0.814,
     lpMode = 0.111, lpMod = 0.563, lpAmp =  0,
     hpMode = 0.000, hpMod = 1.000, hpAmp =  0,
     spread = 1.000, lfoPanMod = 0.286, lfoPanRatio = 0.250,
     dryAmp = -3, dryPan = 0.000,
     amp = 0)

xover(  7, "Slow Res",
     lfoFreq = 0.2372,
     crossover =  100, lfoCrossover = 0.950,
     lfoCrossoverRatio = 0.125, res = 0.915,
     lpMode = 1.000, lpMod = 0.980, lpAmp = -5,
     hpMode = 1.000, hpMod = 1.000, hpAmp =  0,
     spread = -1.000, lfoPanMod = 0.352, lfoPanRatio = 1.000,
     dryAmp = -99, dryPan = 0.000,
     amp = 0)

xover(  8, "Tenth Second",
     lfoFreq = 0.1000,
     crossover =  600, lfoCrossover = 0.271,
     lfoCrossoverRatio = 1.000, res = 0.477,
     lpMode = 0.583, lpMod = 1.000, lpAmp =  0,
     hpMode = 1.000, hpMod = 1.000, hpAmp =  0,
     spread = -0.538, lfoPanMod = 0.975, lfoPanRatio = 1.000,
     dryAmp = -9, dryPan = 0.000,
     amp = 0)

