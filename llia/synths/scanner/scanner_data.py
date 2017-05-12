# llia.synths.Scanner.Scanner_data

from __future__ import print_function
from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance

prototype = {"scanRate" : 5.0,
             "wave" : 0.5,
             "delay" : 0.01,
             "modDepth" : 0.5,
             "feedback" : 0.0,
             "lowpass" : 16000,
             "dryMix" : 0.5,
             "wet1Mix" : 0.5,
             "wet2Mix" : 0.5,
             "xmodDepth" : 0.0}

class Scanner(Program):

    def __init__(self,name):
        super(Scanner,self).__init__(name,Scanner,prototype)
        self.performance = performance()

program_bank = ProgramBank(Scanner("Init"))

def scanner(slot, name,
            scanRate = 5.0,
            wave = 0.5,
            delay = 0.01,
            modDepth = 0.5,
            feedback = 0.0,
            lowpass = 16000,
            dryMix = 0.5,
            wet1Mix = 0.5,
            wet2Mix = 0.5,
            xmodDepth = 0.0):
    def fval(x):
        return round(float(x),4)
    p = Scanner(name)
    p["scanRate"] = fval(scanRate)
    p["wave"] = fval(wave)
    p["delay"] = fval(delay)
    p["modDepth"] = fval(modDepth)
    p["feedback"] = fval(feedback)
    p["lowpass"] = int(lowpass)
    p["dryMix"] = fval(dryMix)
    p["wet1Mix"] = fval(wet1Mix)
    p["wet2Mix"] = fval(wet2Mix)
    p["xmodDepth"] = fval(xmodDepth)
    program_bank[slot] = p
    return p


scanner(0,"Bypass",
        scanRate = 5.0000,
        wave = 0.4975,
        delay = 0.0100,
        modDepth = 0.0000,
        feedback = -0.0000,
        lowpass = 16000,
        dryMix = 0.5000,
        wet1Mix = 0.0000,
        wet2Mix = 0.0000,
        xmodDepth = 0.0000)

scanner(1,"Phasor 1",
        scanRate = 2.7200,
        wave = 0.4774,
        delay = 0.0123,
        modDepth = 0.0050,
        feedback = -0.7623,
        lowpass = 16000,
        dryMix = 0.5000,
        wet1Mix = 0.5000,
        wet2Mix = 0.5000,
        xmodDepth = 0.0000)

scanner(2,"Vibrato",
        scanRate = 6.000,
        wave = 0.5,
        delay = 0.5090,
        modDepth = 0.1,
        feedback = -0.70,
        lowpass = 8000,
        dryMix = 1.0000,
        wet1Mix = 0.60,
        wet2Mix = 0.60,
        xmodDepth = 0.0000)

scanner(3,"Slight Mod",
        scanRate = 0.6270,
        wave = 0.5000,
        delay = 0.0500,
        modDepth = 0.1005,
        feedback = -0.9108,
        lowpass = 16000,
        dryMix = 0.5012,
        wet1Mix = 0.5012,
        wet2Mix = 0.5012,
        xmodDepth = 0.0000)

scanner(4,"Slow And Deep",
        scanRate = 0.0660,
        wave = 0.5025,
        delay = 0.0013,
        modDepth = 0.9648,
        feedback = 0.9900,
        lowpass = 2441,
        dryMix = 0.0000,
        wet1Mix = 0.7079,
        wet2Mix = 0.7079,
        xmodDepth = 0.0000)

scanner(5,"Random 1",
        scanRate = 1.3520,
        wave = 1.0000,
        delay = 0.0408,
        modDepth = 0.6181,
        feedback = -0.9900,
        lowpass = 1000,
        dryMix = 0.5000,
        wet1Mix = 0.8913,
        wet2Mix = 0.7079,
        xmodDepth = 0.0000)

scanner(6,"Random 2",
        scanRate = 4.0620,
        wave = 0.5000,
        delay = 0.0040,
        modDepth = 0.4774,
        feedback = -0.7524,
        lowpass = 2000,
        dryMix = 0.5000,
        wet1Mix = 0.6310,
        wet2Mix = 0.6310,
        xmodDepth = 0.0000)

scanner(7,"Random 3",
        scanRate = 4.3960,
        wave = 0.5000,
        delay = 0.0500,
        modDepth = 0.5779,
        feedback = 0.7227,
        lowpass = 16000,
        dryMix = 0.5000,
        wet1Mix = 0.5000,
        wet2Mix = 0.5000,
        xmodDepth = 0.0000)
