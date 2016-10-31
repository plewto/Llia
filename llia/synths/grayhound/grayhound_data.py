# llia.synths.grayhound.grayhound_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance

FILTER_FREQUENCIES = [100,200,400,800,
                      1000,2000,4000,8000,20000]
GAINS = []
for v in (8,4,2):
    tx = "1/%d" % v
    r = 1.0/v
    GAINS.append((r,tx))
for v in (1,2,3,4,6,8,12,16):
    GAINS.append((v,str(v)))



prototype = {
    "pregain" : 1,        # [1/8,1/4,1/2, ..., 1, 2, ... 8]
    "attack" : 0.01,      # 0.01 .. 0.25  
    "release" : 0.01,     # 0.01 .. 0.25
    "filterFreq" : 1000,  # msb [...]
    "res" : 0.5,          # norm
    "modDepth" : 0.0,     # bi-polar
    "xmod" : 0.0,         # bi-polar
    "dryamp" : 1.0,       # volume
    "wetamp" : 1.0}       # volume

class Grayhound(Program):

    def __init__(self,name):
        super(Grayhound,self).__init__(name,Grayhound,prototype)
        self.performance = performance()

program_bank = ProgramBank(Grayhound("Init"))
program_bank.enable_undo = False

def grayhound(slot, name,
              pregain = 1,
              attack = 0.01,
              release = 0.01,
              filterFreq = 1000,  # int
              res = 0.5,
              modDepth = 0.0,
              xmod = 0.0,
              dryamp = 1.0,
              wetamp = 1.0):
   p = Grayhound(name)
   p["filterFreq"] = int(filterFreq)
   p["pregain"] = float(pregain)
   p["attack"] = float(attack)
   p["release"] = float(release)
   p["res"] = float(res)
   p["modDepth"] = float(modDepth)
   p["xmod"] = float(xmod)
   p["dryamp"] = float(dryamp)
   p["wetamp"] = float(wetamp)   
   program_bank[slot] = p
   return p

def pp(program,slot=127):
    pad = ' '*len("grayhound")
    acc = 'grayhound(%d,"%s",\n' % (slot,program.name)
    acc += '%sfilterFreq = %d,\n' % (pad, int(program["filterFreq"]))
    params = ("pregain","attack","release","res","modDepth",
              "xmod","dryamp","wetamp")
    terminal = params[-1]
    for p in params:
        acc += '%s%s = %5.3f' % (pad,p,float(program[p]))
        if p == terminal:
            acc += ")\n"
        else:
            acc += ",\n"
    return acc

grayhound(0,"Bypass",
          dryamp = 1.0,
          wetamp = 0.0)

grayhound(1,"Static 4k",
          filterFreq = 4000,
          res = 0.5,
          modDepth = 0.0,
          xmod = 0.0,
          dryamp = 0.0,
          wetamp = 1.0)

grayhound(2,"pos mod",
          filterFreq=400,
          res=0.7,
          modDepth = 1.0,
          xmod = 0.0,
          dryamp = 0.0,
          wetamp = 1.0)

grayhound(3,"neg mod",
          filterFreq=20000,
          res=0.7,
          modDepth = -1.0,
          xmod = 0.0,
          dryamp = 0.0,
          wetamp = 1.0)

grayhound(4,"External mod",
          filterFreq=400,
          res=0.7,
          modDepth = 0.0,
          xmod = 1.0,
          dryamp = 0.0,
          wetamp = 1.0)
          
