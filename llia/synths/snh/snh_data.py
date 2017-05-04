# llia.synths.snh.snh_data

from __future__ import print_function
from fractions import Fraction

from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance
from llia.util.lmath import coin, rnd, pick

prototype = {"clockSource" : 0,     # 0 -> internal, 1 -> external
             "clockRate" : 1.0,
             "sawFreq" : 3.0,
             "sawMix" : 0.0,
             "noiseMix" : 1.0,
             "externalMix" : 0.0,
             "lag" : 0.0,
             "scale" : 1.0,
             "bias" : 0.0}

class SnH(Program):

    def __init__(self, name):
        super(SnH, self).__init__(name, "SNH", prototype)
        self.performance = performance()

program_bank = ProgramBank(SnH("Init"))

def snh(slot, name,
        clockSource = 0,
        clockRate = 1.0,
        sawFreq = 0.333,
        sawMix = 0.0,
        noiseMix = 0.0,
        externalMix = 0.0,
        lag = 0.0,
        scale = 1.0,
        bias = 0.0):
    p = SnH(name)
    p["clockSource"] = int(clockSource)
    p["clockRate"] = float(clockRate)
    p["sawFreq"] = float(sawFreq)
    p["sawMix"] = float(sawMix)
    p["noiseMix"] = float(noiseMix)
    p["externalMix"] = float(externalMix)
    p["lag"] = float(lag)
    p["scale"] = float(scale)
    p["bias"] = float(bias)
    program_bank[slot] = p
    return p

def pp(program, slot=127):
    def fval(key):
        v = program[key]
        return float(program[key])
    pad = ' '*5
    acc = 'snh(%d, "%s",' % (slot,program.name)
    acc += '%sclockSource = %d,\n' % (pad, int(program['clockSource']))
    plst = ("clockRate","sawFreq","sawMix","noiseMix","externalMix",
            "lag","scale","bias")
    for param in plst:
        val = fval(param)
        acc += '%s%s = %5.4f' % (pad,param,val)
        if param == plst[-1]:
            acc += ')\n'
        else:
            acc += ',\n'
    return acc

def random_snh(slot=127, *_):
    return None


snh(0, "Calssic SH 3Hz",     clockSource = 0,
     clockRate = 3.0000,
     sawFreq = 0.3330,
     sawMix = 0.0000,
     noiseMix = 1.0000,
     externalMix = 0.0000,
     lag = 0.0000,
     scale = 1.0000,
     bias = 0.0000)

snh(1, "Classic SH 8Hz",     clockSource = 0,
     clockRate = 8.0000,
     sawFreq = 3.0000,
     sawMix = 0.0000,
     noiseMix = 1.0000,
     externalMix = 0.0000,
     lag = 0.0000,
     scale = 1.0000,
     bias = 0.0000)

snh(2, "Classic with Lag",     clockSource = 0,
     clockRate = 5.0000,
     sawFreq = 3.0000,
     sawMix = 0.0000,
     noiseMix = 1.0000,
     externalMix = 0.0000,
     lag = 0.3166,
     scale = 1.0000,
     bias = 0.0000)

snh(3, "Five To Three",     clockSource = 0,
     clockRate = 5.0000,
     sawFreq = 3.0000,
     sawMix = 1.0000,
     noiseMix = 0.0000,
     externalMix = 0.0000,
     lag = 0.1005,
     scale = 1.0000,
     bias = 0.0000)

snh(4, "Five To Seven",     clockSource = 0,
     clockRate = 5.0000,
     sawFreq = 7.0000,
     sawMix = 1.0000,
     noiseMix = 0.0000,
     externalMix = 0.0000,
     lag = 0.0000,
     scale = 1.0000,
     bias = 0.0000)

snh(5, "Seven To Five",     clockSource = 0,
     clockRate = 7.0000,
     sawFreq = 5.0000,
     sawMix = 1.0000,
     noiseMix = 0.0000,
     externalMix = 0.0000,
     lag = 0.0704,
     scale = 1.0000,
     bias = 0.0000)

snh(6, "Slow Ascending Saw",     clockSource = 0,
     clockRate = 6.0000,
     sawFreq = 6.1000,
     sawMix = 1.0000,
     noiseMix = 0.0000,
     externalMix = 0.0000,
     lag = 0.0854,
     scale = 1.0000,
     bias = 0.0000)

snh(7, "Slow Desending Saw",     clockSource = 0,
     clockRate = 6.0000,
     sawFreq = 5.9000,
     sawMix = 1.0000,
     noiseMix = 0.0000,
     externalMix = 0.0000,
     lag = 0.0000,
     scale = 1.0000,
     bias = 0.0000)

snh(8, "Stairstep 1",     clockSource = 0,
     clockRate = 6.0000,
     sawFreq = 6.9000,
     sawMix = 1.0000,
     noiseMix = 0.0000,
     externalMix = 0.0000,
     lag = 0.0000,
     scale = 1.0000,
     bias = 0.0000)

snh(9, "Stairstep 2",     clockSource = 0,
     clockRate = 6.0000,
     sawFreq = 4.9000,
     sawMix = 1.0000,
     noiseMix = 0.0000,
     externalMix = 0.0000,
     lag = 0.0000,
     scale = 1.0000,
     bias = 0.0000)

snh(10, "Fast Sawtooth",     clockSource = 0,
     clockRate = 36.0000,
     sawFreq = 31.2000,
     sawMix = 1.0000,
     noiseMix = 0.0000,
     externalMix = 0.0000,
     lag = 0.0000,
     scale = 1.0000,
     bias = 0.0000)

