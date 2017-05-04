# llia.synths.envgen.envgen_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance

prototype = {"aAttack" : 0.0,
             "aDecay1" : 0.0,
             "aDecay2" : 0.0,
             "aRelease" : 0.0,
             "aBreakpoint" : 1.0,
             "aSustain" : 1.0,
             "aEnvmode" : 0,
             "aInvert" : 0,
             "bAttack" : 0.0,
             "bDecay1" : 0.0,
             "bDecay2" : 0.0,
             "bRelease" : 0.0,
             "bBreakpoint" : 1.0,
             "bSustain" : 1.0,
             "bEnvmode" : 0,
             "bInvert" : 0}

class Envgen(Program):

    def __init__(self,name):
        super(Envgen,self).__init__(name,Envgen,prototype)
        self.performance = performance()

program_bank = ProgramBank(Envgen("Init"))

def envgen(slot, name,
           aAttack = 0.0,
           aDecay1 = 0.0,
           aDecay2 = 0.0,
           aRelease = 0.0,
           aBreakpoint = 1.0,
           aSustain = 1.0,
           aEnvmode = 0,
           aInvert = 0,
           bAttack = 0.0,
           bDecay1 = 0.0,
           bDecay2 = 0.0,
           bRelease = 0.0,
           bBreakpoint = 1.0,
           bSustain = 1.0,
           bEnvmode = 0,
           bInvert = 0):
    p = Envgen(name)
    p["aAttack"] = float(aAttack)
    p["aDecay1"] = float(aDecay1)
    p["aDecay2"] = float(aDecay2)
    p["aRelease"] = float(aRelease)
    p["aBreakpoint"] = float(aBreakpoint)
    p["aSustain"] = float(aSustain)
    p["aEnvmode"] = int(aEnvmode)
    p["aInvert"] = int(aInvert)
    p["bAttack"] = float(bAttack)
    p["bDecay1"] = float(bDecay1)
    p["bDecay2"] = float(bDecay2)
    p["bRelease"] = float(bRelease)
    p["bBreakpoint"] = float(bBreakpoint)
    p["bSustain"] = float(bSustain)
    p["bEnvmode"] = int(bEnvmode)
    p["bInvert"] = int(bInvert)
    program_bank[slot] = p
    return p

def pp(program,slot=127):
    def fval(key):
        return round(float(program[key]),4)
    def ival(key):
        return int(program[key])
    pad = ' '*7
    acc = 'envgen(%d,"%s",\n' % (slot,program.name)
    for q in ('a','b'):
        for r in ("Attack","Decay1","Decay2",
                   "Release","Breakpoint","Sustain"):
            param = "%s%s" % (q,r)
            val = fval(param)
            acc += "%s%s = %5.4f,\n" % (pad,param,val)
        for r in ("Envmode","Invert"):
            param = "%s%s" % (q,r)
            val = ival(param)
            acc += "%s%s = %d" % (pad,param,val)
            if q == 'b' and r == 'Invert':
                acc += ")\n"
            else:
                acc += ',\n'
    return acc

envgen(0,"Init")
envgen(1,"A",
       aAttack = 1.0000,
       aDecay1 = 1.0000,
       aDecay2 = 1.0000,
       aRelease = 1.0000,
       aBreakpoint = 1.0000,
       aSustain = 1.0000,
       aEnvmode = 0,
       aInvert = 0,
       bAttack = 1.0000,
       bDecay1 = 1.0000,
       bDecay2 = 1.0000,
       bRelease = 1.0000,
       bBreakpoint = 1.0000,
       bSustain = 1.0000,
       bEnvmode = 0,
       bInvert = 1)

envgen(2,"B",
       aAttack = 2.0000,
       aDecay1 = 2.0000,
       aDecay2 = 2.0000,
       aRelease = 2.0000,
       aBreakpoint = 1.0000,
       aSustain = 1.0000,
       aEnvmode = 0,
       aInvert = 0,
       bAttack = 2.0000,
       bDecay1 = 2.0000,
       bDecay2 = 2.0000,
       bRelease = 2.0000,
       bBreakpoint = 1.0000,
       bSustain = 1.0000,
       bEnvmode = 0,
       bInvert = 1)
