# llia.synths.ghostbus.ghostbus_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance
from llia.util.lmath import clip, coin, rnd, random_sign

MAX_DELAY = 1.0

# prototype = {
#     "delay" : 0.25,
#     "feedback" : 0.0,
#     "lag" : 0.0,
#     "scale" : 1.0,
#     "bias" : 0.0
#     }

prototype = {
    "scaleA" : 1.0,
    "biasA" : 0.0,
    "muteA" : 0,

    "scaleB" : 1.0,
    "biasB" : 0.0,
    "muteB" : 0,

    "scaleC" : 1.0,
    "biasC" : 0.0,
    "muteC" : 0,

    "scaleD" : 1.0,
    "biasD" : 0.0,
    "muteD" : 0,

    "delay" : 0.0,
    "lag" : 0.0,
    "masterScale" : 1.0,
    "masterBias" : 0.0,
    "masterMute" : 0}
    

class Ghostbus(Program):

    def __init__(self, name):
        super(Ghostbus, self).__init__(name, "GHOSTBUS", prototype)
        self.performance = performance()

program_bank = ProgramBank(Ghostbus("Init"))
program_bank.enable_undo = False

# def ghostbus(slot, name,
#              delay = 0.0,
#              feedback = 0.0,
#              lag = 0.0,
#              scale = 1.0,
#              bias = 0.0):
#     p = Ghostbus(name)
#     p["delay"] = float(clip(delay, 0.0, MAX_DELAY))
#     p["feedback"] = float(clip(feedback, -1, 1))
#     p["lag"] = float(clip(lag, 0, 1))
#     p["scale"] = float(clip(scale, -4, 4))
#     p["bias"] = float(clip(bias, -4, 4))
#     program_bank[slot] = p
#     return p

def ghostbus(slot, name,
             a = [1.0, 0.0, 0], # [scale,bias, mute]
             b = [1.0, 0.0, 0],
             c = [1.0, 0.0, 0],
             d = [1.0, 0.0, 0],
             master = [1.0, 0.0, 0],
             delay = 0.0,
             lag = 0.0):
    def fill(ary):
        acc = []
        template = [1.0, 0.0, 0]
        for i,dflt in enumerate(template):
            try:
                v = ary[i]
            except INdexError:
                v = dflt
            if i < 2:
                v = float(v)
            else:
                v = int(v)
            acc.append(v)
        return acc
    p = Ghostbus(name)
    for n,ary in (('A', fill(a)),('B',fill(b)),('C',fill(c)),('D',fill(d))):
        p['scale%s' % n] = ary[1]
        p['bias%s' % n] = ary[2]
        p['mute%s' % n] = ary[3]
    master = fill(master)
    p['masterScale'] = master[0]
    p['masterBias'] = master[1]
    p['masterMute'] = master[2]
    p['delay'] = float(max(min(delay, MAX_DELAY), 0))
    p['lag'] = float(lag)  
    program_bank[slot] = p
    return p
    


# def pp(program, slot=127):
#     def fval(key):
#         return float(program[key])
#     pad = ' '*9
#     acc = 'ghostbus(%d,"%s",\n' % (slot, program.name)
#     acc += '%sdelay = %5.3f,\n' % (pad, fval("delay"))
#     acc += '%sfeedback = %5.3f,\n' % (pad, fval('feedback'))
#     acc += '%slag = %5.3f,\n' % (pad, fval('lag'))
#     acc += '%sscale = %5.3f,\n' % (pad, fval('scale'))
#     acc += '%sbias = %5.3f)\n' % (pad, fval('bias'))
#     return acc

def pp(program, slot=127):
    def fval(key):
        return float(program[key])
    def ival(key):
        return int(program[key])
    pad = ' '*9
    acc = 'ghostbus(%d, "%s",\n' % (slot, program.name)
    for n in 'abcd':
        acc += '%s%s = [' % (pad,n)
        scale = fval("scale%s" % n.upper())
        bias = fval("bias%s" % n.upper())
        mute = ival("mute%s" % n.upper())
        acc += '%5.3f,%5.3f,%d],\n' % (scale, bias,mute)
    acc += '%smaster = [' % pad
    acc += '%5.3f,%5.3f,%d],\n' % (fval('masterScale'),
                                   fval('masterBias'),
                                   ival('masterMute'))
    acc += '%sdelay = %5.3f,\n' % (pad, fval('delay'))
    acc += '%slag = %5.3f)\n' % (pad, fval('lag'))
    return acc
    


# def random_ghostbus(slot=127, *_):
#     p = ghostbus(slot, 'Random',
#                  delay = rnd(MAX_DELAY),
#                  feedback = random_sign()*rnd(),
#                  lag = coin(0.5, 0.0, rnd()),
#                  scale = 1.0,
#                  bias = 0.0)
#     return p

