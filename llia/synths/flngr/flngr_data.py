# llia.synths.flngr.flngr_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.util.lmath import clip, db_to_amp, amp_to_db, coin, rnd, random_sign, pick
from llia.performance_edit import performance

prototype = {"delay" : 0.5,
	     "xmodDepth" : 0.0,
	     "imodDepth" : 0.5,
	     "imodFreq" : 1.0,
	     "feedback" : 0.5,
	     "feedbackLowpass" : 10000,
	     "feedbackHighpass" : 10,
	     "efxMix" : 0.5,
	     "xmixScale" : 0.0,
	     "amp" : 1.00}

class Flngr(Program):

    def __init__(self, name):
        super(Flngr, self).__init__(name, "Flngr", prototype)
        self.performance = performance()

program_bank = ProgramBank(Flngr("Init"))

def flngr(slot, name, amp=0,
          delay = 0.5,
          modDepth = 0.5,
          modFreq = 1.0,
          feedback = 0.5,
          loweq = 10000,
          higheq = 10,
          efxMix = 0.5,
          xmodDepth = 0,
          xmixScale = 0):
    p = Flngr(name)
    p["delay"] = clip(float(delay), 0, 1)
    p["imodDepth"] = clip(float(modDepth), 0, 1)
    p["imodFreq"] = abs(float(modFreq))
    p["feedback"] = clip(float(feedback), -1, 1)
    p["feedbackLowpass"] = clip(int(loweq), 20, 20000)
    p["feedbackHighpass"] = clip(int(higheq), 20, 20000)
    p["efxMix"] = clip(float(efxMix), 0, 1)
    p["xmodDepth"] = clip(float(xmodDepth), 0, 1)
    p["xmixScale"] = clip(float(xmixScale), 0, 1)
    p["amp"] = float(db_to_amp(amp))
    program_bank[slot] = p
    return p

def pp(program, slot=127):
    def fval(key):
        return float(program[key])
    def ival(key):
        return int(program[key])
    pad = ' '*5
    frmt = 'flngr(%d, "%s", amp=%d,  efxMix=%5.3f,\n'
    data = (slot, program.name, int(amp_to_db(program["amp"])), fval("efxMix"))
    acc = frmt % data
    frmt = '%sdelay=%5.3f, modDepth=%5.3f, modFreq=%5.3f,\n'
    data = (pad, fval("delay"), fval("imodDepth"), fval("imodFreq"))
    acc += frmt % data
    frmt = '%sfeedback=%5.3f, loweq=%d, higheq=%d,\n'
    data = (pad, fval("feedback"),ival("feedbackLowpass"),
            ival("feedbackHighpass"))
    acc += frmt % data
    frmt = '%sxmodDepth = %5.3f, xmixScale = %5.3f)\n'
    data = (pad, fval("xmodDepth"), fval("xmixScale"))
    acc += frmt % data
    return acc


def random_flanger(slot=127, *_):
    p = flngr(slot, "Random", amp=0,
              delay = coin(0.75, 0.5, rnd()),
              modDepth = rnd(),
              modFreq = coin(0.75, rnd(), rnd(10)),
              feedback = random_sign()*rnd(0.9),
              loweq = coin(0.75, 20000, pick([1000, 2000, 4000, 8000])),
              higheq = coin(0.75, 20, pick([200, 400, 800, 1600])),
              efxMix = coin(0.75, 0.5+rnd(0.5), rnd()),
              xmodDepth = 0.0,
              xmixScale = 0.0)
    return p
              
              
              
flngr(0, "Bypass", amp=0,  efxMix=0.000,
     delay=0.508, modDepth=0.000, modFreq=0.000,
     feedback=-0.055, loweq=20000, higheq=20,
     xmodDepth = 0.000, xmixScale = 0.000)

flngr(1, "Very Light", amp=0,  efxMix=0.749,
     delay=0.497, modDepth=0.800, modFreq=0.220,
     feedback=-0.005, loweq=10000, higheq=20,
     xmodDepth = 0.000, xmixScale = 0.000)

flngr(2, "Chorus", amp=0,  efxMix=0.508,
     delay=0.508, modDepth=0.018, modFreq=6.585,
     feedback=0.739, loweq=20000, higheq=20,
     xmodDepth = 0.000, xmixScale = 0.000)

flngr(3, "Slow & Hard", amp=0,  efxMix=0.809,
     delay=0.497, modDepth=1.000, modFreq=0.037,
     feedback=-0.960, loweq=3150, higheq=63,
     xmodDepth = 0.000, xmixScale = 0.000)

flngr(4, "High Trem", amp=0,  efxMix=0.809,
     delay=0.256, modDepth=0.048, modFreq=10.000,
     feedback=-0.950, loweq=20000, higheq=500,
     xmodDepth = 0.000, xmixScale = 0.000)

flngr(5, "3 Hertz", amp=0,  efxMix=1.000,
     delay=0.231, modDepth=0.042, modFreq=3.144,
     feedback=0.799, loweq=1600, higheq=160,
     xmodDepth = 0.000, xmixScale = 0.000)

flngr(6, "Slow & Light", amp=0,  efxMix=1.000,
     delay=1.000, modDepth=0.076, modFreq=0.881,
     feedback=0.487, loweq=20000, higheq=125,
     xmodDepth = 0.000, xmixScale = 0.000)
