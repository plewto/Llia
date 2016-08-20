# llia.synths.ghostbus.ghostbus_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance
from llia.util.lmath import clip, coin, rnd, random_sign

MAX_DELAY = 1.0

prototype = {
    "delay" : 0.25,
    "feedback" : 0.0,
    "lag" : 0.0,
    "scale" : 1.0,
    "bias" : 0.0
    }

class Ghostbus(Program):

    def __init__(self, name):
        super(Ghostbus, self).__init__(name, "GHOSTBUS", prototype)
        self.performance = performance()

program_bank = ProgramBank(Ghostbus("Init"))
program_bank.enable_undo = False

def ghostbus(slot, name,
             delay = 0.0,
             feedback = 0.0,
             lag = 0.0,
             scale = 1.0,
             bias = 0.0):
    p = Ghostbus(name)
    p["delay"] = float(clip(delay, 0.0, MAX_DELAY))
    p["feedback"] = float(clip(feedback, -1, 1))
    p["lag"] = float(clip(lag, 0, 1))
    p["scale"] = float(clip(scale, -4, 4))
    p["bias"] = float(clip(bias, -4, 4))
    program_bank[slot] = p
    return p

def pp(program, slot=127):
    def fval(key):
        return float(program[key])
    pad = ' '*9
    acc = 'ghostbus(%d,"%s",\n' % (slot, program.name)
    acc += '%sdelay = %5.3f,\n' % (pad, fval("delay"))
    acc += '%sfeedback = %5.3f,\n' % (pad, fval('feedback'))
    acc += '%slag = %5.3f,\n' % (pad, fval('lag'))
    acc += '%sscale = %5.3f,\n' % (pad, fval('scale'))
    acc += '%sbias = %5.3f)\n' % (pad, fval('bias'))
    return acc

def random_ghostbus(slot=127, *_):
    p = ghostbus(slot, 'Random',
                 delay = rnd(MAX_DELAY),
                 feedback = random_sign()*rnd(),
                 lag = coin(0.5, 0.0, rnd()),
                 scale = 1.0,
                 bias = 0.0)
    return p

