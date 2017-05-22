# llia.synths.TTone.TTone_data

from __future__ import print_function
from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance

prototype = {
    "ratio" : 1.0,
    "bias" : 0.0,
    "wave" : 0,
    "amp" : 1.000}

class TTone(Program):

    def __init__(self,name):
        super(TTone,self).__init__(name,TTone,prototype)
        self.performance = performance()

program_bank = ProgramBank(TTone("Init"))
def ttone(slot, name,
          ratio = 1.0,
          bias = 0.0,
          wave = 0,
          amp = 1):
    def fval(x):
        return round(float(x),4)
    p = TTone(name)
    p["ratio"] = fval(ratio)
    p["bias"] = fval(bias)
    p["wave"] = int(wave)
    p["amp"] = fval(amp)
    program_bank[slot] = p
    return p

ttone(0,"6db",amp=1.995)
ttone(1,"3db",amp=1.413)
ttone(2,"0db",amp=1.000)
ttone(3,"-3db",amp=0.708)
ttone(4,"-6db",amp=0.501)
ttone(5,"-9db",amp=0.355)
ttone(6,"-12db",amp=0.251)
      
