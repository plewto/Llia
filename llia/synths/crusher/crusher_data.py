# llia.synths.pitchshifter.rm_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance

prototype = {"gain" : 1.0,               # fold/wrap pregain 0..10?
             "wave" : 0,                 # wave select [0,1,2] -> [None,Soft, Distort,Fold,Wrap]
             "clockFreq" : 10000,        # sample clock frequency
             "resampleEnable" : 1,       # 0 -> bypass, 1 -> resample
             "low"  : 20000,             # low pass filter cutoff
             "wet" : 0.5,                # wet signal amp
             "dry" : 0.5,                # dry signal amp
             "amp" : 1.0}                # overall amp

class Crusher(Program):

    def __init__(self, name):
        super(Crusher, self).__init__(name, "Crusher", prototype)
        self.performance = performance()

program_bank = ProgramBank(Crusher("Init"))

def crusher(slot, name,
            gain = 1.0,
            wave = 0,
            clockFreq = 16000,
            resampleEnable = 1,
            low = 20000,
            wet = 0.5,
            dry = 0.5,
            amp = 1.0):
    p = Crusher(name)
    p["gain"] = float(gain)
    p["wave"] = int(wave)
    p["clockFreq"] = int(clockFreq)
    p["resampleEnable"] = int(resampleEnable)
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
    acc += "%swave = %d,\n" % (pad,int(program["wave"]))
    acc += "%sresampleEnable = %d,\n" % (pad,int(program["resampleEnable"]))
    acc += frmt("gain")
    acc += frmt("wet")
    acc += frmt("dry")
    acc += frmt("amp")
    return acc

crusher(0,"Bypass",
       #imodfreq = 16000,
       low = 20000,
       wave = 0,
       resampleEnable = 0,
       gain = 1.000,
       wet = 0.000,
       dry = 1.000,
       amp = 1.000)
