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


flngr2(0,"Bypass",
       timebase = 1.0000,
       delay1 = 0.0100,
       xmod1 = 0.0000,
       depth1 = 0.5000,
       lfoRatio1 = 1.0000,
       feedback1 = 0.0000,
       xfeedback1 = 0.0000,
       lowpass1 = 16000.0000,
       efxMix1 = 0.0045,
       efxPan1 = 0.0000,
       delay2 = 0.0100,
       xmod2 = 0.0000,
       depth2 = 0.5000,
       lfoRatio2 = 1.0000,
       feedback2 = 0.0000,
       xfeedback2 = 0.0000,
       lowpass2 = 16000.0000,
       efxMix2 = 0.0000,
       efxPan2 = 0.0000,
       dryMix2 = 1.0000,
       dryPan2 = -1.0000)

flngr2(1,"Light Vibrato",
       timebase = 7.0000,
       delay1 = 0.0071,
       xmod1 = 0.0000,
       depth1 = 0.0225,
       lfoRatio1 = 1.0000,
       feedback1 = -0.4400,
       xfeedback1 = 0.4100,
       lowpass1 = 7507.6000,
       efxMix1 = 1.0000,
       efxPan1 = 0.7000,
       delay2 = 0.0074,
       xmod2 = 0.0000,
       depth2 = 0.0225,
       lfoRatio2 = 0.8333,
       feedback2 = -0.4200,
       xfeedback2 = 0.4400,
       lowpass2 = 7728.4000,
       efxMix2 = 1.0000,
       efxPan2 = -0.7700,
       dryMix2 = 1.0000,
       dryPan2 = 0.7400)

flngr2(2,"Stereo Fade",
       timebase = 0.1000,
       delay1 = 0.0052,
       xmod1 = 0.0000,
       depth1 = 0.3080,
       lfoRatio1 = 1.0000,
       feedback1 = -0.8700,
       xfeedback1 = 0.5200,
       lowpass1 = 10497.6000,
       efxMix1 = 1.0000,
       efxPan1 = 0.7700,
       delay2 = 0.0060,
       xmod2 = 0.0000,
       depth2 = 0.5000,
       lfoRatio2 = 0.7500,
       feedback2 = -0.8100,
       xfeedback2 = 0.5500,
       lowpass2 = 9610.0000,
       efxMix2 = 1.0000,
       efxPan2 = -0.8100,
       dryMix2 = 1.0000,
       dryPan2 = -0.7700)

flngr2(3,"Very Slow Cross Flange",
       timebase = 0.1000,
       delay1 = 0.0052,
       xmod1 = 0.0000,
       depth1 = 0.6320,
       lfoRatio1 = 0.0833,
       feedback1 = -0.8700,
       xfeedback1 = 0.5200,
       lowpass1 = 10497.6000,
       efxMix1 = 1.0000,
       efxPan1 = 0.7700,
       delay2 = 0.0060,
       xmod2 = 0.0000,
       depth2 = 0.7832,
       lfoRatio2 = 0.0625,
       feedback2 = -0.8100,
       xfeedback2 = 0.5500,
       lowpass2 = 9610.0000,
       efxMix2 = 1.0000,
       efxPan2 = -0.8100,
       dryMix2 = 1.0000,
       dryPan2 = -0.7700)

flngr2(4,"99 Highlands",
       timebase = 99.0000,
       delay1 = 0.0053,
       xmod1 = 0.0000,
       depth1 = 0.5476,
       lfoRatio1 = 1.0000,
       feedback1 = -0.5500,
       xfeedback1 = 0.0000,
       lowpass1 = 16000.0000,
       efxMix1 = 1.0000,
       efxPan1 = 0.5800,
       delay2 = 0.0051,
       xmod2 = 0.0000,
       depth2 = 1.0000,
       lfoRatio2 = 0.0625,
       feedback2 = -0.7200,
       xfeedback2 = 0.0000,
       lowpass2 = 16000.0000,
       efxMix2 = 1.0000,
       efxPan2 = -0.6600,
       dryMix2 = 1.0000,
       dryPan2 = -0.5500)

flngr2(5,"Deep 1:16",
       timebase = 1.0000,
       delay1 = 0.0053,
       xmod1 = 0.0000,
       depth1 = 0.5000,
       lfoRatio1 = 1.0000,
       feedback1 = -0.8100,
       xfeedback1 = 0.0000,
       lowpass1 = 8410.0000,
       efxMix1 = 1.0000,
       efxPan1 = 0.0000,
       delay2 = 0.0053,
       xmod2 = 0.0000,
       depth2 = 0.5000,
       lfoRatio2 = 0.0625,
       feedback2 = 0.5200,
       xfeedback2 = 0.3300,
       lowpass2 = 7075.6000,
       efxMix2 = 1.0000,
       efxPan2 = 0.0000,
       dryMix2 = 1.0000,
       dryPan2 = 0.0000)

