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
    

rumklang(0, "Bypass",
         delay = 0.000,
         roomSize = 0.497,
         damp = 0.497,
         eq = [16000,20],
         gatted = 0,
         modDepth = 0.000,
         wet = [-99,0.025],
         dry = [0,-0.055])

rumklang(1, "Small Room",
         delay = 0.000,
         roomSize = 0.040,
         damp = 0.593,
         eq = [8000,125],
         gatted = 0,
         modDepth = 0.000,
         wet = [-8,0.246],
         dry = [0,0.749])

rumklang(2, "Medium Small Room",
         delay = 0.013,
         roomSize = 0.246,
         damp = 0.332,
         eq = [6300,20],
         gatted = 0,
         modDepth = 0.000,
         wet = [-7,0.317],
         dry = [0,-0.417])

rumklang(3, "Large Space 1",
         delay = 0.048,
         roomSize = 0.814,
         damp = 0.905,
         eq = [4000,40],
         gatted = 0,
         modDepth = 0.000,
         wet = [-3,0.286],
         dry = [0,-0.317])

rumklang(4, "Large Space 2",
         delay = 0.157,
         roomSize = 1.000,
         damp = 0.905,
         eq = [20000,63],
         gatted = 0,
         modDepth = 0.000,
         wet = [-3,0.286],
         dry = [0,-0.317])

rumklang(5, "High SlapBack",
         delay = 0.236,
         roomSize = 0.362,
         damp = 0.000,
         eq = [8000,1250],
         gatted = 0,
         modDepth = 0.000,
         wet = [-8,0.286],
         dry = [0,-0.317])

rumklang(6, "Gated Highpass",
         delay = 0.000,
         roomSize = 1.000,
         damp = 0.241,
         eq = [8000,500],
         gatted = 1,
         modDepth = 0.000,
         wet = [-3,0.286],
         dry = [0,-0.317])

rumklang(7, "Full Gate",
         delay = 0.320,
         roomSize = 1.000,
         damp = 0.000,
         eq = [8000,20],
         gatted = 1,
         modDepth = 0.000,
         wet = [-3,0.286],
         dry = [0,-0.317])

rumklang(8, "Dark And Long",
         delay = 0.048,
         roomSize = 1.000,
         damp = 0.487,
         eq = [315,10],
         gatted = 0,
         modDepth = 0.000,
         wet = [-3,-0.216],
         dry = [0,0.246])

rumklang(9, "Wet Gate",
         delay = 0.000,
         roomSize = 1.000,
         damp = 0.487,
         eq = [20000,10],
         gatted = 1,
         modDepth = 0.000,
         wet = [0,0.005],
         dry = [-99,0.246])

rumklang(10, "High Wet Gate",
         delay = 0.000,
         roomSize = 0.719,
         damp = 0.000,
         eq = [8000,1000],
         gatted = 1,
         modDepth = 0.000,
         wet = [5,-0.196],
         dry = [-25,0.246])


