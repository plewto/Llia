# llia.synths.Combo.Combo_data

from __future__ import print_function
from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance

prototype = {
    "flute8" : 1.0,     # All stop tabs have three values:
    "flute4" : 0.0,     #   0.0  0.5  and 1.0
    "flute3" : 0.0,
    "flute2" : 0.0,
    "reed16" : 1.0,
    "reed8"  : 0.0,
    "reedWave" : 0.0,   # 0 (33%pulse)  1 (square)
    "vspeed" : 0.0,     # 0  0.5  1
    "vdepth" : 0.0,     # 0  0.5  1
    "chorus" : 0.0,     # 0  1
    "amp" : 0.3}      # linear

class Combo(Program):

    def __init__(self,name):
        super(Combo,self).__init__(name,Combo,prototype)
        self.performance = performance()

program_bank = ProgramBank(Combo("Init"))
def combo(slot, name,
          flute8 = 1.0,
          flute4 = 0.0,
          flute3 = 0.0,
          flute2 = 0.0,
          reed16 = 1.0,
          reed8 = 0.0,
          reedwave = 0.0,
          vspeed = 0.0,
          vdepth = 0.0,
          chorus = 0.0,
          amp = 0.3):
    def fval(x):
        return round(float(x),4)
    p = Combo(name)
    p["flute8"] = float(flute8)
    p["flute4"] = float(flute4)
    p["flute3"] = float(flute3)
    p["flute2"] = float(flute2)
    p["reed16"] = float(reed16)
    p["reed8"] = float(reed8)
    p["vspeed"] = float(vspeed)
    p["vdepth"] = float(vdepth)
    p["chorus"] = float(chorus)
    p["amp"] = fval(amp)
    program_bank[slot] = p
    return p

combo(0,"Init")
