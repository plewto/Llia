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
        lfoFreq = 1.0,
        crossover = 800, lfoCrossover = 0.00, 
        lfoCrossoverRatio = 1.00, res=0.5,
        lpMode = 1.00, lpMod = 1.00, lpAmp = 0,
        hpMode = 1.00, hpMod = 1.00, hpAmp = 0,
        spread = 0.75, lfoPanMod = 0.00, lfoPanRatio = 1.00,
        dryAmp = -99, dryPan= 0.0, 
        amp = 0)

# xover(  1, "Alpha",
#         lfoFreq = 2.0,
#         crossover = 800, lfoCrossover = 0.00, 
#         lfoCrossoverRatio = 1.00, res=0.5,
#         lpMode = 1.00, lpMod = 1.00, lpAmp = 0,
#         hpMode = 1.00, hpMod = 1.00, hpAmp = 0,
#         spread = 0.75, lfoPanMod = 0.00, lfoPanRatio = 1.00,
#         dryAmp = -99, dryPan= 0.0, 
#         amp = 0)

# xover(  2, "Beta",
#         lfoFreq = 4.0,
#         crossover = 800, lfoCrossover = 0.00, 
#         lfoCrossoverRatio = 1.00, res=0.5,
#         lpMode = 1.00, lpMod = 1.00, lpAmp = 0,
#         hpMode = 1.00, hpMod = 1.00, hpAmp = 0,
#         spread = 0.75, lfoPanMod = 0.00, lfoPanRatio = 1.00,
#         dryAmp = -99, dryPan= 0.0, 
#         amp = 0)

# xover(  3, "Gamma",
#      lfoFreq = 6.0000,
#      crossover =  800, lfoCrossover = 0.000,
#      lfoCrossoverRatio = 1.000, res = 0.500,
#      lpMode = 1.000, lpMod = 1.000, lpAmp =  0,
#      hpMode = 1.000, hpMod = 1.000, hpAmp =  0,
#      spread = 0.750, lfoPanMod = 0.000, lfoPanRatio = 1.000,
#      dryAmp = -99, dryPan = 0.000,
#      amp = 0)



xover(  1, "One",
     lfoFreq = 0.8068,
     crossover =  800, lfoCrossover = 0.000,
     lfoCrossoverRatio = 1.500, res = 0.500,
     lpMode = 1.000, lpMod = 1.000, lpAmp =  0,
     hpMode = 1.000, hpMod = 0.703, hpAmp =  0,
     spread = 0.000, lfoPanMod = 0.000, lfoPanRatio = 4.000,
     dryAmp = -18, dryPan = 0.000,
     amp = 0)

xover(  2, "Two",
     lfoFreq = 2.0543,
     crossover = 1600, lfoCrossover = 0.000,
     lfoCrossoverRatio = 1.000, res = 0.500,
     lpMode = 1.000, lpMod = 1.000, lpAmp =  0,
     hpMode = 1.000, hpMod = 1.000, hpAmp =  0,
     spread = 1.000, lfoPanMod = 0.000, lfoPanRatio = 1.000,
     dryAmp = -99, dryPan = 0.000,
     amp = 0)

xover(  3, "Three",
     lfoFreq = 6.1588,
     crossover =  200, lfoCrossover = 0.000,
     lfoCrossoverRatio = 1.500, res = 0.500,
     lpMode = 1.000, lpMod = 1.000, lpAmp =  0,
     hpMode = 1.000, hpMod = 1.000, hpAmp =  0,
     spread = 0.000, lfoPanMod = 0.241, lfoPanRatio = 1.000,
     dryAmp = -99, dryPan = 0.000,
     amp = 0)

xover( 4, "Four",
     lfoFreq = 0.3165,
     crossover = 1600, lfoCrossover = 0.000,
     lfoCrossoverRatio = 0.750, res = 0.500,
     lpMode = 1.000, lpMod = 1.000, lpAmp =  0,
     hpMode = 0.676, hpMod = 0.567, hpAmp =  0,
     spread = 1.000, lfoPanMod = 0.136, lfoPanRatio = 2.000,
     dryAmp = -6, dryPan = 0.000,
     amp = 0)


xover(  5, "Five",
     lfoFreq = 0.6288,
     crossover =  100, lfoCrossover = 0.499,
     lfoCrossoverRatio = 1.000, res = 0.256,
     lpMode = 0.092, lpMod = 1.000, lpAmp =  0,
     hpMode = 1.000, hpMod = 1.000, hpAmp =  0,
     spread = 0.000, lfoPanMod = 0.772, lfoPanRatio = 1.000,
     dryAmp = -99, dryPan = 0.000,
     amp = 0)

xover(  6, "Six",
     lfoFreq = 120,
     crossover =  200, lfoCrossover = 0.997,
     lfoCrossoverRatio = 1.000, res = 0.841,
     lpMode = 1.000, lpMod = 0.621, lpAmp =  0,
     hpMode = 1.000, hpMod = 1.000, hpAmp =  0,
     spread = 0.000, lfoPanMod = 0.000, lfoPanRatio = 4.000,
     dryAmp = -99, dryPan = 0.000,
     amp = 0)

xover(  7, "Seven",
     lfoFreq = 5.0,
     crossover = 8000, lfoCrossover = 0.100,
     lfoCrossoverRatio = 2.000, res = 0.722,
     lpMode = 1.000, lpMod = 0.636, lpAmp =  0,
     hpMode = 1.000, hpMod = 1.000, hpAmp =  0,
     spread = 0.000, lfoPanMod = 0.75, lfoPanRatio = 0.125,
     dryAmp = -99, dryPan = 0.000,
     amp = 0)

xover(  8, "Eight",
     lfoFreq = 0.03,
     crossover =  400, lfoCrossover = 0.500,
     lfoCrossoverRatio = 2.500, res = 0.8,
     lpMode = 0.500, lpMod = 1.000, lpAmp =  0,
     hpMode = 0.500, hpMod = 1.000, hpAmp =  0,
     spread = 0.000, lfoPanMod = 1.000, lfoPanRatio = 0.75,
     dryAmp = -99, dryPan = 0.000,
     amp = 0)
