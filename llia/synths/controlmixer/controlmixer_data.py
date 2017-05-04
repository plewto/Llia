# llia.synths.controlmixer.controlmixer_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance
from llia.util.lmath import clip, coin, rnd, random_sign

prototype = {"scaleA" : 1.0,
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
             "masterScale" : 1.0,
             "masterBias" : 0.0,
             "masterMute" : 0}

class Controlmixer(Program):

    def __init__(self, name):
        super(Controlmixer, self).__init__(name, "ControlMixer", prototype)
        self.performance = performance()

program_bank = ProgramBank(Controlmixer("Init"))

def controlmixer(slot,name,
                 scaleA = 1.0,
                 biasA = 0.0,
                 muteA = 0,
                 scaleB = 1.0,
                 biasB = 0.0,
                 muteB = 0,
                 scaleC = 1.0,
                 biasC = 0.0,
                 muteC = 0,
                 scaleD = 1.0,
                 biasD = 0.0,
                 muteD = 0,
                 masterScale = 1.0,
                 masterBias = 0.0,
                 masterMute = 0):
    p = Controlmixer(name)
    p["muteA"] = int(muteA)
    p["muteB"] = int(muteB)
    p["muteC"] = int(muteC)
    p["muteD"] = int(muteD)
    p["masterMute"] = int(masterMute)
    p["scaleA"] = float(scaleA)
    p["biasA"] = float(biasA)
    p["scaleB"] = float(scaleB)
    p["biasB"] = float(biasB)
    p["scaleC"] = float(scaleC)
    p["biasC"] = float(biasC)
    p["scaleD"] = float(scaleD)
    p["biasD"] = float(biasD)
    p["masterScale"] = float(masterScale)
    p["masterBias"] = float(masterBias)
    program_bank[slot] = p
    return p

def pp(program,slot=127):
    def fval(key):
        return float(program[key])
    def mute(key):
        v = int(program[key])
        if v:
            return 1
        else:
            return 0
    pad = ' '*13
    acc = 'controlmixer(%d,"%s",\n' % (slot,program.name)
    flst = ("scaleA",
            "biasA",
            "scaleB",
            "biasB",
            "scaleC",
            "biasC",
            "scaleD",
            "biasD",
            "masterScale",
            "masterBias")
    for param in flst:
        val = fval(param)
        acc += '%s%s = %5.4f,\n' % (pad,param,val)
    mlst = ("muteA","muteB","muteC","muteD","masterMute")
    terminal = mlst[-1]
    for param in mlst:
        m = mute(param)
        acc += '%s%s = %d' % (pad,param,m)
        if param == terminal:
            acc += ')\n'
        else:
            acc += ',\n'
    return acc

        
controlmixer(0,"Mute all",
             muteA = 1,
             muteB = 1,
             muteC = 1,
             muteD = 1,
             masterMute = 1)
controlmixer(1,"All On")
controlmixer(2,"Channel A Only",
             muteA = 0,
             muteB = 1,
             muteC = 1,
             muteD = 1,
             masterMute = 0)

