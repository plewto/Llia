# llia.synths.pitchshifter.pitchshifter_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
#from llia.util.lmath import (clip,db_to_amp,amp_to_db,rnd,coin,pick)
from llia.performance_edit import performance

MAX_DELAY = 1

prototype = {"pitchRatio" : 1.5,       # 0..4
             "pitchDispersion" : 0.0,  # 0..1
             "timeDispersion" : 0.0,   # 0..1
             "delay" : 0.1,            # 0..1
             "feedback" : 0,           # 0..1
             "dryAmp" : 1.0,           # 0..2
             "psAmp" : 1.0,            # 0..2
             "delayAmp" : 0.0,         # 0..2
             "dryPan" : 0.0,           # -1..+1
             "psPan" : 0.0,            # -1..+1
             "delayPan" : 0.0}         # -1..+1

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
             delayPan = -0.00502512562814,
             dryAmp = 1.0,
             dryPan = -0.00502512562814,
             feedback = 0.0,
             pitchDispersion = 0.0,
             pitchRatio = 1.5,
             psAmp = 0.0,
             psPan = -0.00502512562814,
             timeDispersion = 0.0)

pitchshifter(1,"2 Octaves Down",
             delay = 0.0,
             delayAmp = 0.0,
             delayPan = 0.0,
             dryAmp = 1.0,
             dryPan = -0.00502512562814,
             feedback = 0.0,
             pitchDispersion = 0.0,
             pitchRatio = 0.25,
             psAmp = 0.354813389234,
             psPan = -0.00502512562814,
             timeDispersion = 0.0)

pitchshifter(2,"1 Octave Down",
             delay = 0.0,
             delayAmp = 0.0,
             delayPan = 0.0,
             dryAmp = 1.0,
             dryPan = -0.00502512562814,
             feedback = 0.0,
             pitchDispersion = 0.0,
             pitchRatio = 0.5,
             psAmp = 0.354813389234,
             psPan = -0.00502512562814,
             timeDispersion = 0.0)

pitchshifter(3,"Chorus 1",
             delay = 0.0,
             delayAmp = 0.0,
             delayPan = 0.0,
             dryAmp = 1.0,
             dryPan = -0.00502512562814,
             feedback = 0.0,
             pitchDispersion = 0.0,
             pitchRatio = 1.01,
             psAmp = 0.354813389234,
             psPan = -0.00502512562814,
             timeDispersion = 0.070351758794)

pitchshifter(4,"Chorus 2",
             delay = 0.321608040201,
             delayAmp = 0.0,
             delayPan = 0.0,
             dryAmp = 1.0,
             dryPan = -0.00502512562814,
             feedback = 0.100502512563,
             pitchDispersion = 0.0,
             pitchRatio = 1.01,
             psAmp = 0.354813389234,
             psPan = -0.00502512562814,
             timeDispersion = 0.35175879397)

pitchshifter(5,"Fifth",
             delay = 0.0954773869347,
             delayAmp = 0.0,
             delayPan = 0.0,
             dryAmp = 1.0,
             dryPan = 0.0,
             feedback = 0.0,
             pitchDispersion = 0.0,
             pitchRatio = 1.5,
             psAmp = 1.0,
             psPan = 0.0,
             timeDispersion = 0.0)

pitchshifter(6,"Falling Fourths",
             delay = 0.206030150754,
             delayAmp = 0.0,
             delayPan = 0.0,
             dryAmp = 1.0,
             dryPan = 0.0,
             feedback = 0.994974874372,
             pitchDispersion = 0.0,
             pitchRatio = 0.753,
             psAmp = 1.0,
             psPan = 0.0,
             timeDispersion = 0.0)

pitchshifter(7,"Fouth Climb",
             delay = 0.226130653266,
             delayAmp = 0.0,
             delayPan = 0.0,
             dryAmp = 0.891250938134,
             dryPan = 0.0,
             feedback = 0.743718592965,
             pitchDispersion = 0.0,
             pitchRatio = 1.333,
             psAmp = 0.891250938134,
             psPan = 0.0,
             timeDispersion = 0.0)

pitchshifter(8,"Climbing Chorus",
             delay = 0.0653266331658,
             delayAmp = 0.0,
             delayPan = 0.0,
             dryAmp = 1.0,
             dryPan = 0.0,
             feedback = 0.994974874372,
             pitchDispersion = 0.0,
             pitchRatio = 1.013,
             psAmp = 1.0,
             psPan = 0.0,
             timeDispersion = 0.190954773869)

pitchshifter(9,"Klusters",
             delay = 0.0653266331658,
             delayAmp = 0.0,
             delayPan = 0.0,
             dryAmp = 1.0,
             dryPan = 0.0,
             feedback = 0.994974874372,
             pitchDispersion = 0.0,
             pitchRatio = 1.303,
             psAmp = 1.0,
             psPan = 0.0,
             timeDispersion = 0.190954773869)

pitchshifter(10,"Strident Discussion",
             delay = 0.0653266331658,
             delayAmp = 0.0,
             delayPan = 0.0,
             dryAmp = 1.0,
             dryPan = 0.0,
             feedback = 0.994974874372,
             pitchDispersion = 1.0,
             pitchRatio = 1.003,
             psAmp = 1.0,
             psPan = 0.0,
             timeDispersion = 0.0)

pitchshifter(11,"Close Delay",
             delay = 0.0804020100503,
             delayAmp = 0.0,
             delayPan = 0.0,
             dryAmp = 1.0,
             dryPan = 0.0,
             feedback = 1.0,
             pitchDispersion = 0.0,
             pitchRatio = 1.001,
             psAmp = 1.0,
             psPan = 0.0,
             timeDispersion = 0.889447236181)


