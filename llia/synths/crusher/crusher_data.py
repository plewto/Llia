# llia.synths.pitchshifter.rm_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance

MAX_DELAY = 1

prototype = {
    "clockFreq" : 20000,        # sample clock frequency
    "low"  : 20000,             # low pass filter cutoff
    "wet" : 0.5,                # wet signal amp
    "dry" : 0.5,                # dry signal amp
    "amp" : 1.0}                # overall amp

class Crusher(Program):

    def __init__(self, name):
        super(Crusher, self).__init__(name, "Crusher", prototype)
        self.performance = performance()

program_bank = ProgramBank(Crusher("Init"))
program_bank.enable_undo = False

def crusher(slot, name,
            clockFreq = 20000,
            low = 20000,
            wet = 0.5,
            dry = 0.5,
            amp = 1.0):
    p = Crusher(name)
    p["clockFreq"] = int(clockFreq)
    p["low"] = int(low)
    p["wet"] = float(wet)
    p["dry"] = float(dry)
    p["amp"] = float(amp)
    program_bank[slot] = p

def pp(program, slot=127):
    pad = ' '*7
    acc = 'crusher(%d,"%s",\n' % (slot, program.name)
    def frmt(key, end=",\n"):
        val = float(program[key])
        bcc= "%s%s = %5.3f" % (pad, key, val)
        bcc += end
        return bcc
    acc += "%simodfreq = %d,\n" % (pad, int(program["clockFreq"]))
    acc += "%slow = %d,\n" % (pad, int(program["low"]))
    acc += frmt("wet")
    acc += frmt("dry")
    acc += frmt("amp")
    return acc

crusher(0,"Bypass",
        clockFreq = 10000,
        low = 20000,
        wet = 0.0,
        dry = 1.0,
        amp = 1.0  )

crusher(1, "10k",
        clockFreq=10000,
        low=20000,
        wet = 1.0,
        dry = 0.0,
        amp = 1.0)

crusher(2, "5k",
        clockFreq=5000,
        low=20000,
        wet = 1.0,
        dry = 0.0,
        amp = 1.0)

crusher(3, "2k",
        clockFreq=2000,
        low=20000,
        wet = 1.0,
        dry = 0.0,
        amp = 1.0)

crusher(4, "1k",
        clockFreq=1000,
        low=20000,
        wet = 1.0,
        dry = 0.0,
        amp = 1.0)




