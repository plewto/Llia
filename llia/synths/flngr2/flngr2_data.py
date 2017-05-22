# llia.synths.Flngr2.Flngr2_data

from __future__ import print_function
from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance

prototype = {
    "delay1" : 0.5,
    "xmod1" : 0.0,
    "timebase" : 1.0,
    "depth1" : 0.5,
    "lfoRatio1" : 1.0,
    "feedback1" : 0.0,
    "xfeedback1" : 0.0,
    "lowpass1" : 16000,
    "efxMix1" : 1.0,
    "efxPan1" : 0.0,
    "delay2" : 0.5,
    "xmod2" : 0.0,
    "depth2" : 0.5,
    "lfoRatio2" : 1.0,
    "feedback2" : 0.0,
    "xfeedback2" : 0.0,
    "lowpass2" : 16000,
    "efxMix2" : 1.0,
    "efxPan2" : 0.0,
    "dryMix1" : 1.0,
    "dryPan1" : 0.0,
    "dryMix2" : 1.0,
    "dryPan2" : 0.0}

class Flngr2(Program):

    def __init__(self,name):
        super(Flngr2,self).__init__(name,Flngr2,prototype)
        self.performance = performance()

program_bank = ProgramBank(Flngr2("Init"))
def flngr2(slot, name,
           delay1 = 0.5,
           timebase = 1.0,
           xmod1 = 0.0,
           depth1 = 0.5,
           lfoRatio1 = 1.0,
           feedback1 = 0.0,
           xfeedback1 = 0.0,
           lowpass1 = 16000,
           efxMix1 = 1.0,
           efxPan1 = 0.0,
           dryMix1 = 1.0,
           dryPan1 = 0.0,
           delay2 = 0.5,
           xmod2 = 0.0,
           depth2 = 0.5,
           lfoRatio2 = 1.0,
           feedback2 = 0.0,
           xfeedback2 = 0.0,
           lowpass2 = 16000,
           efxMix2 = 1.0,
           efxPan2 = 0.0,
           dryMix2 = 1.0,
           dryPan2 = 0.0):
    def fval(x):
        return round(float(x),4)
    p = Flngr2(name)
    p["delay1"] = fval(delay1)
    p["timebase"] = fval(timebase)
    p["xmod1"] = fval(xmod1)
    p["depth1"] = fval(depth1)
    p["lfoRatio1"] = fval(lfoRatio1)
    p["feedback1"] = fval(feedback1)
    p["xfeedback1"] = fval(xfeedback1)
    p["lowpass1"] = fval(lowpass1)

    p["efxMix1"] = fval(efxMix1)
    p["efxPan1"] = fval(efxPan1)

    p["dryMix1"] = fval(efxMix1)
    p["dryPan1"] = fval(efxPan1)
    
    p["delay2"] = fval(delay2)
    p["xmod2"] = fval(xmod2)
    p["depth2"] = fval(depth2)
    p["lfoRatio2"] = fval(lfoRatio2)
    p["feedback2"] = fval(feedback2)
    p["xfeedback2"] = fval(xfeedback2)
    p["lowpass2"] = fval(lowpass2)
    p["efxMix2"] = fval(efxMix2)
    p["efxPan2"] = fval(efxPan2)

    p["dryMix2"] = fval(efxMix2)
    p["dryPan2"] = fval(efxPan2)

    program_bank[slot] = p
    return p

flngr2(0,"Init")
