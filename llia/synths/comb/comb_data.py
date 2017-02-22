# llia.synths.Comb.Comb_data

from __future__ import print_function
from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance

prototype = {
    "delayScale" : 0.01,
    "delay" : 0.50,
    "phase" : -1,
    "wet" : 1.0}

class Comb(Program):

    def __init__(self,name):
        super(Comb,self).__init__(name,Comb,prototype)
        self.performance = performance()

program_bank = ProgramBank(Comb("Init"))
program_bank.enable_undo = False

def comb(slot, name,
         delayScale = 0.01,     # 0.001|0.010|0.100
         delay = 0.50,          # 0.0 .. 1.0
         phase = -1,            # -1 .. +1
         wet = 1.0):            # 0.0 .. 2.0  
    def fval(x):
        return round(float(x),4)
    p = Comb(name)
    p["delayScale"] = fval(delayScale)
    p["delay"] = fval(delay)
    p["phase"] = int(phase)
    p["wet"] = fval(wet)
    program_bank[slot] = p
    return p

comb(0,"Bypass", delayScale=0.001, delay=0.5, phase=-1, wet=0.0)

slot = 1

for p in (-1, 1):
    if p == -1:
        sign = "-"
    else:
        sign = "+"
    for ds in (0.001, 0.01, 0.1):
        for d in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0):
            delay = ds*d
            name = (sign+"%s ms") % delay
            comb(slot,name,ds,d,p,1.0)
            slot = slot + 1
            
