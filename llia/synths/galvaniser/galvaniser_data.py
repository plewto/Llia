# llia.synths.Galvaniser.Galvaniser_data

from __future__ import print_function
from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance

prototype = {
    "feedback" : 0.1,
    "tone" : 0.5,
    "filter" : 0.5,
    "res" : 0.0,
    "lfoFreq" : 1.0,
    "modDepth" : 0.1,
    "xmodDepth" : 0.0,
    "efxmix" : 0.75,
    "amp" : 1.0}

class Galvaniser(Program):

    def __init__(self,name):
        super(Galvaniser,self).__init__(name,Galvaniser,prototype)
        self.performance = performance()

program_bank = ProgramBank(Galvaniser("Init"))
def galvaniser(slot, name,
               feedback = 0.0,
               tone = 0.5,
               filter = 0.5,
               res = 0.0,
               lfoFreq = 0.1,
               modDepth = 0.1,
               xmodDepth = 0.0,
               efxmix = 0.5,
               amp = 1.0):
    def fval(x):
        return round(float(x),4)
    p = Galvaniser(name)
    p["feedback"] = fval(feedback)
    p["tone"] = fval(tone)
    p["filter"] = fval(filter)
    p["res"] = fval(res)
    p["lfoFreq"] = fval(lfoFreq)
    p["modDepth"] = fval(modDepth)
    p["xmodDepth"] = fval(xmodDepth)
    p["efxmix"] = fval(efxmix)
    p["amp"] = fval(amp)
    program_bank[slot] = p
    return p


galvaniser(0,"Bypass",
           feedback = 0.0000,
           tone = 0.5000,
           filter = 0.5000,
           res = 0.0000,
           lfoFreq = 1.1436,
           modDepth = 0.0000,
           efxmix = 0.0000,
           amp = 1.0000)

galvaniser(1,"Vibra",
           feedback = 0.4400,
           tone = 0.5000,
           filter = 0.1709,
           res = 0.0000,
           lfoFreq = 4.0968,
           modDepth = 0.4020,
           efxmix = 0.9598,
           amp = 1.0000)

galvaniser(2,"Slow Fade",
           feedback = 0.3000,
           tone = 0.1709,
           filter = 0.4724,
           res = 0.3920,
           lfoFreq = 0.1186,
           modDepth = 0.7839,
           efxmix = 0.7990,
           amp = 1.0000)

galvaniser(3,"Slow Fade Odd",
           feedback = -0.6700,
           tone = 0.2965,
           filter = 0.4724,
           res = 0.3920,
           lfoFreq = 0.1186,
           modDepth = 0.7839,
           efxmix = 0.7990,
           amp = 1.0000)

galvaniser(4,"Wha1",
           feedback = 1.0000,
           tone = 0.6734,
           filter = 0.4975,
           res = 0.5477,
           lfoFreq = 1.3629,
           modDepth = 0.4774,
           efxmix = 1.0000,
           amp = 1.0000)

galvaniser(5,"Fast Mod",
           feedback = -0.5600,
           tone = 0.8894,
           filter = 0.4975,
           res = 0.8693,
           lfoFreq = 13.9357,
           modDepth = 0.4774,
           efxmix = 0.4925,
           amp = 1.0000)
