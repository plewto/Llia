# llia.synths.hund.hund_data

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

class Hund(Program):

    def __init__(self,name):
        super(Hund,self).__init__(name,Hund,prototype)
        self.performance = performance()

program_bank = ProgramBank(Hund("Init"))
program_bank.enable_undo = False

def hund(slot, name,
              pregain = 1,
              attack = 0.01,
              release = 0.01,
              filterFreq = 1000,  # int
              res = 0.5,
              modDepth = 0.0,
              xmod = 0.0,
              dryamp = 1.0,
              wetamp = 1.0):
   p = Hund(name)
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
    pad = ' '*len("hund")
    acc = 'hund(%d,"%s",\n' % (slot,program.name)
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


          
hund(0,"Bypass",
    filterFreq = 1000,
    pregain = 1.000,
    attack = 0.010,
    release = 0.010,
    res = 0.497,
    modDepth = 0.000,
    xmod = 0.000,
    dryamp = 1.000,
    wetamp = 0.000)

hund(1,"Static 4k",
    filterFreq = 4000,
    pregain = 1.000,
    attack = 0.010,
    release = 0.010,
    res = 0.500,
    modDepth = 0.000,
    xmod = 0.000,
    dryamp = 0.000,
    wetamp = 1.000)

hund(2,"PosMod",
    filterFreq = 400,
    pregain = 2.000,
    attack = 0.010,
    release = 0.010,
    res = 0.698,
    modDepth = 1.000,
    xmod = 0.000,
    dryamp = 0.000,
    wetamp = 1.000)

hund(3,"NegMod",
    filterFreq = 1000,
    pregain = 4.000,
    attack = 0.010,
    release = 0.010,
    res = 0.588,
    modDepth = -0.890,
    xmod = 0.000,
    dryamp = 0.398,
    wetamp = 1.000)

hund(4,"External mod",
    filterFreq = 400,
    pregain = 1.000,
    attack = 0.010,
    release = 0.010,
    res = 0.698,
    modDepth = 0.000,
    xmod = 1.000,
    dryamp = 0.000,
    wetamp = 1.000)

hund(5,"Gain8",
    filterFreq = 200,
    pregain = 8.000,
    attack = 0.010,
    release = 1.167,
    res = 0.779,
    modDepth = 1.000,
    xmod = 0.030,
    dryamp = 0.141,
    wetamp = 1.000)

hund(6,"Gain8.2",
    filterFreq = 2000,
    pregain = 8.000,
    attack = 0.010,
    release = 2.304,
    res = 0.779,
    modDepth = -0.850,
    xmod = 0.030,
    dryamp = 0.158,
    wetamp = 1.000)

