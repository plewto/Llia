# llia.synths.rumklang.rumklang_data


from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance
from llia.util.lmath import db_to_amp,amp_to_db

prototype = {
    "preDelay" : 0.01,
    "roomSize" : 0.5,
    "damp" : 0.5,
    "lpcutoff" : 16000,
    "hpcutoff" : 10,
    "gatted" : 0,
    "modDepth" : 0.0,
    "wetAmp" : 1.0,
    "wetPan" : 0.75,
    "dryAmp" : 1.0,
    "dryPan" : 0.25}

class Rumklang(Program):

    def __init__(self, name):
        super(Rumklang,self).__init__(name, "Rumklang", prototype)
        self.performance = performance()

program_bank = ProgramBank(Rumklang("Init"))
program_bank.enable_undo = False


MAX_DELAY = 0.33

def rumklang(slot, name,
             delay = 0.0,
             roomSize = 0.5,
             damp = 0.5,
             eq = [16000, 20],   # [lp hp] in Hz
             gatted = 0,
             modDepth = 0.0,     # external wet signal modulation
             wet = [0, 0.25],    # [db, pan]
             dry = [0, 0.75]):   # [db, pan]
    p = Rumklang(name)
    p["preDelay"] = float(min(abs(delay),MAX_DELAY))
    p["roomSize"] = float(roomSize)
    p["damp"] = float(damp)
    p["lpcutoff"] = int(eq[0])
    p["hpcutoff"] = int(max(eq[1],20))
    p["gatted"] = int(gatted)
    p["modDepth"] = float(modDepth)
    p["wetAmp"] = int(db_to_amp(wet[0]))
    p["wetPan"] = float(wet[1])
    p["dryAmp"] = int(db_to_amp(dry[0]))
    p["dryPan"] = float(dry[1])
    program_bank[slot] = p
    return p

def pp(program, slot=127):
    pad = ' '*9
    def fval(key):
        return float(program[key])
    def ival(key):
        return int(program[key])
    def db(key):
        return int(amp_to_db(program[key]))
    acc = 'rumklang(%d, "%s",\n' % (slot, program.name)
    acc += '%sdelay = %5.3f,\n' % (pad,fval('preDelay'))
    acc += '%sroomSize = %5.3f,\n' % (pad,fval('roomSize'))
    acc += '%sdamp = %5.3f,\n' % (pad, fval('damp'))
    acc += '%seq = [%d,%d],\n' % (pad,ival('lpcutoff'),ival('hpcutoff'))
    acc += '%sgatted = %d,\n' % (pad, ival('gatted'))
    acc += '%smodDepth = %5.3f,\n' % (pad,fval('modDepth'))
    acc += '%swet = [%d,%5.3f],\n' % (pad, db("wetAmp"), fval('wetPan'))
    acc += '%sdry = [%d,%5.3f])\n' % (pad, db("dryAmp"), fval('dryPan'))
    return acc
    

rumklang(0,"Default")
rumklang(1,"Big Room", roomSize = 1.0)
rumklang(2,"with delay", roomSize=0.75, delay = 0.25)
rumklang(3,"gate on", roomSize=1.0,gatted=1)


