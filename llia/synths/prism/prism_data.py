# llia.synths.prism.prism_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance

prototype = {"fLow" : 400,
             "fHigh" : 1200,
             "bwScale" : 1.0,
             "gainLow" : 0,
             "gainCenter" : 0,
             "gainHigh" : 0}

class Prism(Program):

    def __init__(self,name):
        super(Prism,self).__init__(name,Prism,prototype)
        self.performance = performance()

program_bank = ProgramBank(Prism("Init"))

def prism(slot, name,
          fLow = 400,
          fHigh = 1200,
          bwScale = 1.0,
          gainLow = 0,
          gainCenter = 0,
          gainHigh = 0):
   p = Prism(name)
   p["fLow"] = int(fLow)
   p["fHigh"] = int(fHigh)
   p["bwScale"] = float(bwScale)
   p["gainLow"] = int(gainLow)
   p["gainCenter"] = int(gainCenter)
   p["gainHigh"] = int(gainHigh)
   program_bank[slot] = p
   return p

def pp(program,slot=127):
    pad = ' '*6
    def i(key,comma=True):
        s = "%s%s = %d" % (pad,key,int(program[key]))
        if comma:
            s += ',\n'
        else:
            s += ')\n'
        return s
    acc = 'prism(%d,"%s",\n' % (slot,program.name)
    acc += i("fLow")
    acc += i("fHigh")
    acc += "%sbwScale = %5.3f,\n" % (pad,round(float(program["bwScale"]),4))
    acc += i("gainLow")
    acc += i("gainCenter")
    acc += i("gainHigh",False)
    return acc

prism(0,"Bypass")
prism(1,"400 1200")
