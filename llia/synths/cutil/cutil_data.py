# llia.synths.cutil.cutil_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance

prototype = {"wave" : 0,                 # int [0,1,2] -> [none,abs,cube]
             "polarityComp" : 0,         # int [0,1,2] -> [none, ->bipolr ->polar]
             "clipMin" : -1.0,           # float, range -/+ 10
             "clipMax" : 1.0,            # floaT, range -/+ 10
             "lag" : 0.0,                # float, 0..1
             "scale" : 1.0,              # float, -/+ 10
             "bias" : 0.0}               # float, -/+ 10

class CUtil(Program):

    def __init__(self,name):
        super(CUtil,self).__init__(name,CUtil,prototype)
        self.performance = performance()

program_bank = ProgramBank(CUtil("Init"))

def cutil(slot, name,
          wave = 0,
          polarityComp = 0,
          clipMin = -1.0,
          clipMax = 1.0,
          lag = 0.0,
          scale = 1.0,
          bias = 0.0):
   p = CUtil(name)
   p["wave"] = int(wave)  
   p["polarityComp"] = int(polarityComp)  
   p["clipMin"] = float(clipMin)  
   p["clipMax"] = float(clipMax)  
   p["lag"] = float(lag)  
   p["scale"] = float(scale)  
   p["bias"] = float(bias)  
   program_bank[slot] = p
   return p

def pp(program,slot=127):
    return ""

cutil(0,"Init")
