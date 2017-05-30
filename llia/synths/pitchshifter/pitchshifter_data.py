# llia.synths.pitchshifter.pitchshifter_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance

MAX_DELAY = 1

prototype = {"pitchRatio" : 1.5,        # 0..4
             "pitchDispersion" : 0.0,   # 0..1
             "timeDispersion" : 0.0,    # 0..1
             "delay" : 0.1,             # 0..1
             "feedback" : 0,            # 0..1
             "dryAmp" : 1.0,            # 0..2
             "psAmp" : 1.0,             # 0..2
             "delayAmp" : 0.0,          # 0..2
             "dryPan" : 0.0,            # -1..+1
             "psPan" : 0.0,             # -1..+1
             "delayPan" : 0.0,          # -1..+1
             "lowpass" : 16000,         # 100..16k
             "delayInSelect" : 0,       # 0=pitch shifter, 1=drysig
             "feedbackDestination" : 0, # 0=pitch shifter, 1=delay
             "delayMod" : 0.0,          # 0..1  lfo -> delay
             "lfoFreq" : 1}             # Hz.
             
class PitchShifter(Program):

    def __init__(self, name):
        super(PitchShifter, self).__init__(name, "PitchShifter", prototype)
        self.performance = performance()

program_bank = ProgramBank(PitchShifter("Init"))

def pitchshifter(slot, name, **pmap):
    p = PitchShifter(name)
    for param,dflt in prototype.items():
        try:
            value = pmap[param]
        except KeyError:
            value = dflt
        p[param] = float(value)
    program_bank[slot] = p
    return p

def pp(program, slot=127):
    pad = ' '*13
    acc = 'pitchshifter(%d,"%s",\n' % (slot, program.name)
    params = sorted(prototype.keys())
    for p in params:
        v = program[p]
        acc += '%s%s = %s' % (pad,p,v)
        if p != params[-1]:
            acc += ',\n'
        else:
            acc += ')\n'
    return acc

pitchshifter(0,"Bypass",
             delay = 0.0954773869347,
             delayAmp = 0.0,
             delayInSelect = 0.0,
             delayMod = 0.0,
             delayPan = -0.01,
             dryAmp = 1.0,
             dryPan = -0.01,
             feedback = 0.0,
             feedbackDestination = 0.0,
             lfoFreq = 1.0,
             lowpass = 16000.0,
             pitchDispersion = 0.0,
             pitchRatio = 1.5,
             psAmp = 0.0,
             psPan = -0.01,
             timeDispersion = 0.0)

pitchshifter(1,"2 Octaves Down",
             delay = 0.0,
             delayAmp = 0.0,
             delayInSelect = 0.0,
             delayMod = 0.0,
             delayPan = 0.0,
             dryAmp = 1.0,
             dryPan = -0.00502512562814,
             feedback = 0.0,
             feedbackDestination = 0.0,
             lfoFreq = 1.0,
             lowpass = 16000.0,
             pitchDispersion = 0.0,
             pitchRatio = 0.25,
             psAmp = 0.398107170553,
             psPan = -0.00502512562814,
             timeDispersion = 0.0)

pitchshifter(2,"1 Octave Down",
             delay = 0.0,
             delayAmp = 0.0,
             delayInSelect = 0.0,
             delayMod = 0.0,
             delayPan = 0.0,
             dryAmp = 1.0,
             dryPan = -0.00502512562814,
             feedback = 0.0,
             feedbackDestination = 0.0,
             lfoFreq = 1.0,
             lowpass = 16000.0,
             pitchDispersion = 0.0,
             pitchRatio = 0.5,
             psAmp = 0.354813389234,
             psPan = -0.00502512562814,
             timeDispersion = 0.0)

pitchshifter(3,"Chorus 1",
             delay = 0.0,
             delayAmp = 0.0,
             delayInSelect = 0.0,
             delayMod = 0.0,
             delayPan = 0.0,
             dryAmp = 1.0,
             dryPan = -0.00502512562814,
             feedback = 0.0,
             feedbackDestination = 0.0,
             lfoFreq = 1.0,
             lowpass = 16000.0,
             pitchDispersion = 0.0,
             pitchRatio = 1.01,
             psAmp = 0.354813389234,
             psPan = -0.00502512562814,
             timeDispersion = 0.070351758794)

pitchshifter(4,"Chorus 2",
             delay = 0.321608040201,
             delayAmp = 0.0,
             delayInSelect = 0.0,
             delayMod = 0.0,
             delayPan = 0.0,
             dryAmp = 1.0,
             dryPan = -0.00502512562814,
             feedback = 0.1,
             feedbackDestination = 0.0,
             lfoFreq = 1.0,
             lowpass = 16000.0,
             pitchDispersion = 0.0,
             pitchRatio = 1.01,
             psAmp = 0.354813389234,
             psPan = -0.00502512562814,
             timeDispersion = 0.35175879397)

pitchshifter(5,"Fifth",
             delay = 0.0954773869347,
             delayAmp = 0.0,
             delayInSelect = 0.0,
             delayMod = 0.0,
             delayPan = 0.0,
             dryAmp = 1.0,
             dryPan = 0.0,
             feedback = 0.0,
             feedbackDestination = 0.0,
             lfoFreq = 1.0,
             lowpass = 16000.0,
             pitchDispersion = 0.0,
             pitchRatio = 1.5,
             psAmp = 1.0,
             psPan = 0.0,
             timeDispersion = 0.0)

pitchshifter(6,"Falling Fourths",
             delay = 0.206030150754,
             delayAmp = 0.0,
             delayInSelect = 0.0,
             delayMod = 0.0,
             delayPan = 0.0,
             dryAmp = 1.0,
             dryPan = 0.0,
             feedback = 0.99,
             feedbackDestination = 0.0,
             lfoFreq = 1.0,
             lowpass = 16000.0,
             pitchDispersion = 0.0,
             pitchRatio = 0.753,
             psAmp = 1.0,
             psPan = 0.0,
             timeDispersion = 0.0)

pitchshifter(7,"Fouth Climb",
             delay = 0.226130653266,
             delayAmp = 0.0,
             delayInSelect = 0.0,
             delayMod = 0.0,
             delayPan = 0.0,
             dryAmp = 0.891250938134,
             dryPan = 0.0,
             feedback = 0.74,
             feedbackDestination = 0.0,
             lfoFreq = 1.0,
             lowpass = 16000.0,
             pitchDispersion = 0.0,
             pitchRatio = 1.333,
             psAmp = 0.891250938134,
             psPan = 0.0,
             timeDispersion = 0.0)

pitchshifter(8,"Climbing Chorus",
             delay = 0.0653266331658,
             delayAmp = 0.0,
             delayInSelect = 0.0,
             delayMod = 0.0,
             delayPan = 0.0,
             dryAmp = 1.0,
             dryPan = 0.0,
             feedback = 0.99,
             feedbackDestination = 0.0,
             lfoFreq = 1.0,
             lowpass = 16000.0,
             pitchDispersion = 0.0,
             pitchRatio = 1.012,
             psAmp = 1.0,
             psPan = 0.0,
             timeDispersion = 0.185929648241)

pitchshifter(9,"Klusters",
             delay = 0.0653266331658,
             delayAmp = 0.0,
             delayInSelect = 0.0,
             delayMod = 0.0,
             delayPan = 0.0,
             dryAmp = 1.0,
             dryPan = 0.0,
             feedback = 0.994974874372,
             feedbackDestination = 0.0,
             lfoFreq = 1.0,
             lowpass = 16000.0,
             pitchDispersion = 0.0,
             pitchRatio = 1.303,
             psAmp = 1.0,
             psPan = 0.0,
             timeDispersion = 0.190954773869)

pitchshifter(10,"Strident Discussion",
             delay = 0.0653266331658,
             delayAmp = 0.0,
             delayInSelect = 0.0,
             delayMod = 0.0,
             delayPan = 0.0,
             dryAmp = 1.0,
             dryPan = 0.0,
             feedback = 0.994974874372,
             feedbackDestination = 0.0,
             lfoFreq = 1.0,
             lowpass = 16000.0,
             pitchDispersion = 1.0,
             pitchRatio = 1.002,
             psAmp = 1.0,
             psPan = 0.0,
             timeDispersion = 0.0)

pitchshifter(11,"Close Delay",
             delay = 0.0804020100503,
             delayAmp = 0.0,
             delayInSelect = 0.0,
             delayMod = 0.0,
             delayPan = 0.0,
             dryAmp = 1.0,
             dryPan = 0.0,
             feedback = 1.0,
             feedbackDestination = 0.0,
             lfoFreq = 1.0,
             lowpass = 16000.0,
             pitchDispersion = 0.0,
             pitchRatio = 1.0,
             psAmp = 1.0,
             psPan = 0.0,
             timeDispersion = 0.889447236181)

pitchshifter(12,"Delayed Octave ",
             delay = 0.2916,
             delayAmp = 0.316227766017,
             delayInSelect = 0.0,
             delayMod = 0.0,
             delayPan = 0.0,
             dryAmp = 1.0,
             dryPan = 0.0,
             feedback = 0.77,
             feedbackDestination = 1.0,
             lfoFreq = 1.0,
             lowpass = 4000.0,
             pitchDispersion = 0.0,
             pitchRatio = 2.0,
             psAmp = 0.0,
             psPan = 0.0,
             timeDispersion = 0.462311557789)

pitchshifter(13,"Flanged Octave Down",
             delay = 0.0016,
             delayAmp = 0.501187233627,
             delayInSelect = 0.0,
             delayMod = 0.2916,
             delayPan = 0.0,
             dryAmp = 1.0,
             dryPan = 0.0,
             feedback = 0.94,
             feedbackDestination = 1.0,
             lfoFreq = 0.4,
             lowpass = 8761.6,
             pitchDispersion = 0.0,
             pitchRatio = 0.5,
             psAmp = 0.446683592151,
             psPan = 0.0,
             timeDispersion = 0.110552763819)

pitchshifter(14,"Flanged Octave Up",
             delay = 0.0016,
             delayAmp = 0.316227766017,
             delayInSelect = 0.0,
             delayMod = 0.0361,
             delayPan = 0.0,
             dryAmp = 1.0,
             dryPan = 0.0,
             feedback = -0.86,
             feedbackDestination = 1.0,
             lfoFreq = 3.2,
             lowpass = 10497.6,
             pitchDispersion = 0.0,
             pitchRatio = 2.01,
             psAmp = 0.281838293126,
             psPan = 0.0,
             timeDispersion = 0.120603015075)

pitchshifter(15,"Unanswerd Question",
             delay = 0.442225,
             delayAmp = 1.0,
             delayInSelect = 0.0,
             delayMod = 0.837225,
             delayPan = 0.0,
             dryAmp = 0.281838293126,
             dryPan = 0.0,
             feedback = -0.62,
             feedbackDestination = 1.0,
             lfoFreq = 0.01,
             lowpass = 10497.6,
             pitchDispersion = 0.527638190955,
             pitchRatio = 2.5,
             psAmp = 1.0,
             psPan = 0.0,
             timeDispersion = 0.0)

pitchshifter(16,"Two Octave Ghost",
             delay = 0.4096,
             delayAmp = 0.891250938134,
             delayInSelect = 0.0,
             delayMod = 0.0324,
             delayPan = 0.0,
             dryAmp = 0.0,
             dryPan = 0.0,
             feedback = -0.83,
             feedbackDestination = 1.0,
             lfoFreq = 0.01,
             lowpass = 16000,
             pitchDispersion = 0.140703517588,
             pitchRatio = 4.0,
             psAmp = 1.0,
             psPan = 0.0,
             timeDispersion = 0.457286432161)

