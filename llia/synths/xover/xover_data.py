# llia.synths.xover.xover_data
#

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.util.lmath import clip, db_to_amp
from llia.performance_edit import performance

prototype = {
    "amp" : 1.00,
    "dryAmp" : 1.00,
    "wetAmp" : 1.00,
    "crossover" : 500,
    "res" : 0.0,
    "lfoFreq" : 1.00,
    "lfoPhase" : 1.00,
    "ringmod" : 0.00,
    "rev" : 0.00,
    "room" : 0.5,
    "dryPan" : 0.00,
    "lpPan" : 0.00,
    "hpPan" : 0.00,
    "lfoPan" : 0.00}


class XOver(Program):

    def __init__(self, name):
        super(XOver, self).__init__(name, "XOver", prototype)


INIT_PROGRAM = XOver("Init");
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

def fclip(n, mn=0,mx=1):
    return float(clip(n, mn, mx))

def xover(slot, name,
          crossover = 900,
          res = 0.5,
          lfoFreq = 1.0,
          lfoPhase = 1.0,
          ringmod = -1,
          reverb = -1,
          room = 0.5,
          pan = [0.00, 0.00, 0.00], # [dry, lp, hp]
          lfoPan = 0.00,
          mix = [0.5, 1.0], # [dry wet]
          amp = 1.0):
    mix = fill(mix, [0.5, 1.0, 1.0])
    pan = fill(pan, [0, 0, 0])
    p = XOver(name)
    p["amp"] = fclip(amp)
    p["dryAmp"] = fclip(mix[0])
    p["wetAmp"] = fclip(mix[1])
    p["crossover"] = fclip(crossover, 100, 16000)
    p["res"] = fclip(res)
    p["lfoFreq"] = fclip(lfoFreq, 0.1, 500)
    p["lfoPhase"] = fclip(lfoPhase, 0, 1)
    p["ringmod"] = fclip(ringmod, -1, 1)
    p["rev"] = fclip(reverb, -1, 1)
    p["room"] = fclip(room, 0, 1)
    p["dryPan"] = fclip(pan[0], -1, 1)
    p["lpPan"] = fclip(pan[1], -1, 1)
    p["hpPan"] = fclip(pan[2], -1, 1)
    p["lfoPan"] = fclip(lfoPan, 0, 1)
    p.performacne = performance()
    program_bank[slot] = p
    return p


xover(0, "Init")

xover(1, "SlowAndHard",
      crossover = 900,
      res = 0.7,
      lfoFreq = 0.1,  lfoPhase = 1.0,
      ringmod = -1.00, reverb= -1.00, room = 0.5,
      pan = [0.0, 0.0, 0.0],  lfoPan = 1.0,
      mix = [0.3, 1.0],
      amp = 1.0)


xover(2, "RingMod",
      crossover = 900,
      res = 0.7,
      lfoFreq = 0.1,  lfoPhase = 1.0,
      ringmod = 1.00, reverb= -1.00, room = 0.5,
      pan = [0.0, 0.0, 0.0],  lfoPan = 1.0,
      mix = [0.3, 1.0],
      amp = 1.0)

xover(3, "Reverb",
      crossover = 900,
      res = 0.7,
      lfoFreq = 0.1,  lfoPhase = 1.0,
      ringmod = -1.00, reverb= 1.00, room = 0.5,
      pan = [0.0, 0.0, 0.0],  lfoPan = 1.0,
      mix = [0.3, 1.0],
      amp = 1.0)

