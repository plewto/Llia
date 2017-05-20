# llia.synths.Carnal2.Carnal2_data

from __future__ import print_function
from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance

prototype = {
    "timebase" : 1.00,
    "delayTime1" : 0.1,
    "modDepth1" : 0.0,
    "xmodDepth1" : 0.0,
    "lfoRatio1" : 1.0,
    "feedback1" : 0.0,
    "efxMix1" : 0.5,
    "efxPan1" : 0.5,
    "dryMix1" : 0.5,
    "dryPan1" : 0.5,
    "lowcut1" : 20000,
    "highcut1" : 10,
    "clipEnable1" : 0,
    "clipGain1" : 1.0,
    "clipThreshold1" : 1.0,
    "xfeedback1" : 0.0,
    "delayTime2" : 0.1,
    "modDepth2" : 0.0,
    "xmodDepth2" : 0.0,
    "lfoRatio2" : 1.0,
    "feedback2" : 0.0,
    "efxMix2" : 0.5,
    "efxPan2" : 0.5,
    "dryMix2" : 0.5,
    "dryPan2" : 0.5,
    "lowcut2" : 20000,
    "highcut2" : 10,
    "clipEnable2" : 0,
    "clipGain2" : 1.0,
    "clipThreshold2" : 1.0,
    "xfeedback2" : 0.0}

class Carnal2(Program):

    def __init__(self,name):
        super(Carnal2,self).__init__(name,Carnal2,prototype)
        self.performance = performance()

program_bank = ProgramBank(Carnal2("Init"))
def carnal2(slot, name,
            timebase = 1.00,
            delayTime1 = 0.1,
            modDepth1 = 0.0,
            xmodDepth1 = 0.0,
            lfoRatio1 = 1.0,
            feedback1 = 0.0,
            efxMix1 = 0.5,
            efxPan1 = 0.5,
            dryMix1 = 0.5,
            dryPan1 = 0.5,
            lowcut1 = 20000,
            highcut1 = 10,
            clipEnable1 = 0,
            clipGain1 = 1.0,
            clipThreshold1 = 1.0,
            xfeedback1 = 0.0,
            delayTime2 = 0.1,
            modDepth2 = 0.0,
            xmodDepth2 = 0.0,
            lfoRatio2 = 1.0,
            feedback2 = 0.0,
            efxMix2 = 0.5,
            efxPan2 = 0.5,
            dryMix2 = 0.5,
            dryPan2 = 0.5,
            lowcut2 = 20000,
            highcut2 = 10,
            clipEnable2 = 0,
            clipGain2 = 1.0,
            clipThreshold2 = 1.0,
            xfeedback2 = 0.0):
    def fval(x):
        return round(float(x),4)
    p = Carnal2(name)
    p["timebase"] = fval(timebase)
    p["delayTime1"] = fval(delayTime1)
    p["modDepth1"] = fval(modDepth1)
    p["xmodDepth1"] = fval(xmodDepth1)
    p["lfoRatio1"] = fval(lfoRatio1)
    p["feedback1"] = fval(feedback1)
    p["efxMix1"] = fval(efxMix1)
    p["efxPan1"] = fval(efxPan1)
    p["dryMix1"] = fval(dryMix1)
    p["dryPan1"] = fval(dryPan1)
    p["lowcut1"] = fval(lowcut1)
    p["highcut1"] = fval(highcut1)
    p["clipEnable1"] = int(clipEnable1)
    p["clipGain1"] = fval(clipGain1)
    p["clipThreshold1"] = fval(clipThreshold1)
    p["xfeedback1"] = fval(xfeedback1)
    p["delayTime2"] = fval(delayTime2)
    p["modDepth2"] = fval(modDepth2)
    p["xmodDepth2"] = fval(xmodDepth2)
    p["lfoRatio2"] = fval(lfoRatio2)
    p["feedback2"] = fval(feedback2)
    p["efxMix2"] = fval(efxMix2)
    p["efxPan2"] = fval(efxPan2)
    p["dryMix2"] = fval(dryMix2)
    p["dryPan2"] = fval(dryPan2)
    p["lowcut2"] = fval(lowcut2)
    p["highcut2"] = fval(highcut2)
    p["clipEnable2"] = int(clipEnable2)
    p["clipGain2"] = fval(clipGain2)
    p["clipThreshold2"] = fval(clipThreshold2)
    p["xfeedback2"] = fval(xfeedback2)
    program_bank[slot] = p
    return p

carnal2(0,"Init")
