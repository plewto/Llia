# llia.synths.pitchshifter.rm_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance

MAX_DELAY = 1

prototype = {"imodfreq" : 1000,           # internal modulator frequency
             "imodamp" : 1.0,             # internal modulator linear amp
             "xmodamp" : 0.0,             # external modulator amp
             "xmodbleed" : 0.0,           # external mod bleed to output
             "carbleed" : 0.0,            # carrier bleed to output
             "amp"     : 1}               # main linear amplitude

class RingModulator(Program):

    def __init__(self, name):
        super(RingModulator, self).__init__(name, "RingModulator", prototype)
        self.performance = performance()

program_bank = ProgramBank(RingModulator("Init"))

def rm(slot, name,
       imodfreq = 1000,
       imodamp = 1.0,
       xmodamp = 1.0,
       xmodbleed = 0.0,
       carbleed = 0.0,
       amp = 1.0):
    p = RingModulator(name)
    p["imodfreq"] = int(imodfreq)
    p["imodamp"] = float(imodamp)
    p["xmodamp"] = float(xmodamp)
    p["xmodbleed"] = float(xmodbleed)
    p["carbleed"] = float(carbleed)
    p["amp"] = float(amp)
    program_bank[slot] = p

def pp(program, slot=127):
    pad = ' '*4
    acc = 'rm(%d,"%s",\n' % (slot, program.name)
    def frmt(key, end=",\n"):
        val = float(program[key])
        bcc= "%s%s = %5.3f" % (pad, key, val)
        bcc += end
        return bcc
    acc += "%simodfreq = %d,\n" % (pad, int(program["imodfreq"]))
    acc += frmt("imodamp")
    acc += frmt("xmodamp")
    acc += frmt("xmodbleed")
    acc += frmt("carbleed")
    acc += frmt("amp", ")\n")
    return acc


    rm(0,"Bypass",
    imodfreq = 1000,
    imodamp = 0.000,
    xmodamp = 0.000,
    xmodbleed = 0.000,
    carbleed = 1.000,
    amp = 1.000)

rm(1,"Self Mod",
    imodfreq = 1000,
    imodamp = 0.000,
    xmodamp = 1.000,
    xmodbleed = 0.000,
    carbleed = 0.891,
    amp = 1.000)

rm(2,"1K",
    imodfreq = 1000,
    imodamp = 1.000,
    xmodamp = 0.000,
    xmodbleed = 0.000,
    carbleed = 0.000,
    amp = 1.000)

rm(3,"5K",
    imodfreq = 5000,
    imodamp = 1.000,
    xmodamp = 0.000,
    xmodbleed = 0.000,
    carbleed = 0.000,
    amp = 1.000)

rm(4,"5Hz Tremolo",
    imodfreq = 5,
    imodamp = 1.000,
    xmodamp = 0.000,
    xmodbleed = 0.000,
    carbleed = 0.000,
    amp = 1.000)

rm(5,"Asymetric Tremolo",
    imodfreq = 1,
    imodamp = 1.000,
    xmodamp = 0.000,
    xmodbleed = 0.000,
    carbleed = 0.316,
    amp = 1.000)

          
