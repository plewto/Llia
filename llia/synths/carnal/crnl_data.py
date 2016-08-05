# llia.synths.carnal.crnl_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.util.lmath import (clip,db_to_amp,amp_to_db,rnd,coin,pick)
from llia.performance_edit import performance

MAX_DELAY = 1.5

prototype = {
    "delayTime" : 0.125,     # mean delay time, seconds
    "wow" : 0.0,             # periodic delay time modulation, normalized
    "wowFreq" : 1.0,         # wow signal frequency, Hertz (0.1, 5)
    "flutter" : 0.0,         # noise delay time modulation, normalized
    "xDelayMod" : 0.0,       # external delay time modulation, normalized
                             #   assuming (0..1) signal amplitude
    "feedback" : 0.0,        # delay feedback, normalized
    "gain" : 1.0,            # feedback path gain (pre-clipper) (0.5, 2)
    "threshold" : 1.0,       # feedback clipping threshold, normalized
    "lowcut" : 10000,        # feedback lowpass cutoff, Hertz
    "highcut" : 100,         # feedback highpass cutoff, Hertz
    "efxMix" : 0.5,          # wet/dry signal mix, 0 -> dry, 1 -> wet
    "xEfxMix" : 0.0,         # external efx-mix modulation, normalized
    "amp" : 1.0}             # overall gain


class CarnalDelay(Program):

    def __init__(self, name):
        super(CarnalDelay, self).__init__(name, "CarnalDelay", prototype)
        self.performance = performance()

program_bank = ProgramBank(CarnalDelay("Init"))
program_bank.enable_undo = False

MAX_DELAY = 1.5

def carnal(slot, name, amp=-12,
           delayTime = 0.125,
           xDelay = 0.0,
           wow = 0.0,
           wowFreq = 1.0,
           flutter = 0,
           feedback = 0.5,
           gain = 1.0,
           threshold = 1.0,
           eq = [10000, 100],   # [lowpass, highpass]
           wetMix = 0.5,
           xWetMix = 0.0):
    p = CarnalDelay(name)
    p["delayTime"] = float(clip(delayTime, 0, MAX_DELAY))
    p["wow"] = float(clip(wow, 0, 1))
    p["wowFreq"] = float(clip(wowFreq, 0.1, 5))
    p["flutter"] = float(clip(flutter, 0, 1))
    p["xDelayMod"] = float(clip(xDelay, 0, 1))
    p["feedback"] = float(clip(feedback, 0, 1))
    p["gain"] = float(clip(gain, 0.5, 2))
    p["threshold"] = float(clip(threshold, 0, 1))
    p["lowcut"] = int(clip(eq[0], 20, 20000))
    p["highcut"] = int(clip(eq[1], 20, 20000))
    p["efxMix"] = float(clip(wetMix, 0, 1))
    p["xEfxMix"] = float(clip(xWetMix, 0, 1))
    p["amp"] = float(clip(db_to_amp(amp), 0, 2))
    program_bank[slot] = p
    return p


def pp(program, slot=12):
    def fval(key):
        return float(program[key])
    def ival(key):
        return int(program[key])
    pad = ' '*5
    frmt = 'carnal(%d, "%s", amp=%d,\n'
    data = (slot, program.name, int(amp_to_db(fval("amp"))))
    acc = frmt % data
    frmt = '%sdelayTime=%5.3f, xDelay=%5.3f,\n'
    data = (pad, fval('delayTime'), fval('xDelayMod'))
    acc += frmt % data
    frmt = '%swow=%5.3f, wowFreq=%5.3f, flutter=%5.3f,\n'
    data = (pad, fval('wow'), fval('wowFreq'), fval('flutter'))
    acc += frmt % data
    frmt = '%sfeedback=%5.3f, gain=%5.3f, threshold=%5.3f,\n'
    data = (pad, fval('feedback'), fval('gain'), fval('threshold'))
    acc += frmt % data
    frmt = '%seq=[%d, %d],\n'
    data = (pad, ival('lowcut'), ival('highcut'))
    acc += frmt % data
    frmt = '%swetMix=%5.3f, xWetMix=%5.3f)\n'
    data = (pad, fval('efxMix'), fval('xEfxMix'))
    acc += frmt % data
    return acc
    
def random_program(slot=127, *_):
    lp = [400, 800, 1600, 3150, 6300, 8000,
          10000, 10000, 10000, 10000,
          16000, 16000, 16000, 16000]
    hp = [20, 100, 100, 100, 100, 200, 400, 800, 1600, 3150]
    p = carnal(slot, "Random", amp=0,
               delayTime = coin(0.5, rnd(0.5), rnd(MAX_DELAY)),
               xDelay = 0,
               wow = coin(0.75,0,coin(0.75, rnd(0.1), rnd())),
               wowFreq = coin(0.75, rnd(), rnd(5)),
               flutter = coin(0.75, 0, coin(0.75, rnd(0.2), rnd())),
               feedback = coin(0.75, 0.5+rnd(0.4), rnd(0.95)),
               gain = 1.0,
               threshold = 1.0,
               eq = [pick(lp), pick(hp)],
               wetMix = coin(0.75, 0.5+rnd(0.25), rnd()),
               xWetMix=0)
    return p

carnal(0, "Bypass", amp=0,
       delayTime = 0.125,  xDelay = 0.00,
       wow = 0.00, wowFreq = 1.00, flutter = 0.00,
       feedback = 0.0, gain = 1.0, threshold = 1.0,
       eq = [20000, 20],
       wetMix = 0.0, xWetMix = 0.0)

carnal(1, "Slapback", amp=0,
     delayTime=0.070, xDelay=0.000,
     wow=0.000, wowFreq=1.000, flutter=0.000,
     feedback=0.300, gain=1.000, threshold=1.000,
     eq=[10000, 100],
     wetMix=0.500, xWetMix=0.000)

carnal(2, "MaxEcho", amp=0,
     delayTime=1.500, xDelay=0.000,
     wow=0.000, wowFreq=1.000, flutter=0.000,
     feedback=0.700, gain=1.000, threshold=1.000,
     eq=[10000, 100],
     wetMix=0.500, xWetMix=0.000)

carnal(3, "Light Chorus", amp=0,
     delayTime=0.202, xDelay=0.000,
     wow=0.774, wowFreq=0.595, flutter=0.000,
     feedback=0.628, gain=1.000, threshold=1.000,
     eq=[10000, 100],
     wetMix=0.256, xWetMix=0.000)

carnal(4, "Highpass Delay", amp=0,
     delayTime=0.795, xDelay=0.000,
     wow=0.090, wowFreq=0.722, flutter=0.090,
     feedback=0.749, gain=1.205, threshold=0.265,
     eq=[20000, 1000],
     wetMix=0.211, xWetMix=0.000)

carnal(5, "Band Limit Delay", amp=0,
     delayTime=0.120, xDelay=0.000,
     wow=0.391, wowFreq=3.003, flutter=0.009,
     feedback=0.864, gain=1.152, threshold=0.476,
     eq=[2500, 500],
     wetMix=0.558, xWetMix=0.000)

carnal(6, "Fast Echos", amp=0,
     delayTime=0.255, xDelay=0.000,
     wow=0.000, wowFreq=0.942, flutter=0.000,
     feedback=0.799, gain=1.000, threshold=1.000,
     eq=[20000, 20],
     wetMix=0.508, xWetMix=0.000)

carnal(7, "Clipped Feedback", amp=0,
     delayTime=0.300, xDelay=0.000,
     wow=0.093, wowFreq=0.288, flutter=0.007,
     feedback=0.719, gain=1.310, threshold=0.058,
     eq=[10000, 100],
     wetMix=0.538, xWetMix=0.000)

