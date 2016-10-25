# llia.synths.ghostbus.ghostbus_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance
from llia.util.lmath import clip, coin, rnd, random_sign

MAX_DELAY = 4

prototype = {
    "enableMod" : 0,
    "enableHpA" : 0,
    "lagA" : 0.0,
    "scaleA" : 1.0,
    "biasA" : 0.0,
    "delay" : 1.0,
    "feedback" : 0.0,
    "lagDelay" : 0.0,
    "enableHpDelay" : 0,
    "scaleDelay" : 1.0,
    "biasDelay" : 0.0}
    
class Ghostbus(Program):

    def __init__(self, name):
        super(Ghostbus, self).__init__(name, "GHOSTBUS", prototype)
        self.performance = performance()

program_bank = ProgramBank(Ghostbus("Init"))
program_bank.enable_undo = False

def ghostbus(slot, name,
             enableMod = 0,
             enableHpA = 0,
             lagA = 0.0,
             scaleA = 1.0,
             biasA = 0.0,
             delay = 1.0,
             feedback = 0.0,
             lagDelay = 0.0,
             enableHpDelay = 0,
             scaleDelay = 1.0,
             biasDelay = 0.0):
    p = Ghostbus(name)
    p["enableMod"] = int(enableMod)
    p["enableHpA"] = int(enableHpA)
    p["enableHpDelay"] = int(enableHpDelay)
    p["lagA"] = float(lagA)
    p["scaleA"] = float(scaleA)
    p["biasA"] = float(biasA)
    p["delay"] = float(delay)
    p["feedback"] = float(feedback)
    p["lagDelay"] = float(lagDelay)
    p["scaleDelay"] = float(scaleDelay)
    p["biasDelay"] = float(biasDelay)
    program_bank[slot] = p
    return p

def pp(program, slot=127):
    def fval(key):
        return float(program[key])
    def bool(key):
        v = int(program[key])
        if v:
            return 1
        else:
            return 0
    pad = ' '*9
    acc = 'ghostbus(%d, "%s",\n' % (slot, program.name)
    mlst = ("enableMod","enableHpA","enableHpDelay")
    plst = ("lagA","scaleA","biasA","delay","feedback",
            "lagDelay","scaleDelay","biasDelay")
    terminal = plst[-1]
    for param in mlst:
        v = bool(param)
        acc += '%s%s = %d,\n' % (pad,param,v)
    for param in plst:
        v = fval(param)
        acc += '%s%s = %5.4f' % (pad,param,v)
        if param == terminal:
            acc += ')\n'
        else:
            acc += ',\n'
    return acc
