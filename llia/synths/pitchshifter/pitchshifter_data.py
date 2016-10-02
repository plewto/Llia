# llia.synths.pitchshifter.pitchshifter_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
#from llia.util.lmath import (clip,db_to_amp,amp_to_db,rnd,coin,pick)
from llia.performance_edit import performance

MAX_DELAY = 1

prototype = {
    "pitchRatio" : 1.5,       # 0..4
    "pitchDispersion" : 0.0,  # 0..1
    "timeDispersion" : 0.0,   # 0..1
    "delay" : 0.1,            # 0..1
    "feedback" : 0,           # 0..1
    "dryAmp" : 1.0,           # 0..2
    "psAmp" : 1.0,            # 0..2
    "delayAmp" : 0.0,         # 0..2
    "dryPan" : 0.0,           # -1..+1
    "psPan" : 0.0,            # -1..+1
    "delayPan" : 0.0,         # -1..+1
}
    
    


class PitchShifter(Program):

    def __init__(self, name):
        super(PitchShifter, self).__init__(name, "PitchShifter", prototype)
        self.performance = performance()

program_bank = ProgramBank(PitchShifter("Init"))
program_bank.enable_undo = False

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

pitchshifter(0,"Init")
