# llia.synths.chronos.chronos_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.util.lmath import (clip,db_to_amp,amp_to_db,rnd,coin,pick)
from llia.performance_edit import performance

MAX_DELAY = 2

prototype = {
    "lfoCommonFreq" : 1.0,      # tumbler 0..16
    "d1Dry1In" : 1.0,           # vol slider
    "d1Dry2In" : 0.0,           # vol slider
    "d1DelayTime" : 0.1,        # tumbler 0..2000 ms
    "d1LfoRatio" : 1.0,         # MSB
    "d1LfoModDepth" : 0.0,      # norm slider  (exp slider ?)
    "d1ExternalModDepth" : 0.0, # norm slider
    "d1Feedback" : 0.0,         # bipolar slider
    "d1Lowpass" : 20000,        # 3rd octave
    "d1Highpass" : 40,          # 3rd octave
    "d2Dry1In" : 0.0,           # vol slider
    "d2Dry2In" : 1.0,           # vol slider
    "d2Delay1In" : 0.0,         # vol slider
    "d2DelayTime" : 0.2,        # tumbler
    "d2LfoRatio" : 1.0,         # MSB
    "d2LfoModDepth" : 0.0,      # norm slider
    "d2ExternalModDepth" : 0.0, # norm slider
    "d2Feedback" : 0.0,         # bipolar
    "d2Lowpass" : 20000,        # 3rd octave
    "d2Highpass" : 40,          # 3rd octave
    "dry1Amp" : 1.0,            # vol slider
    "dry2Amp" : 1.0,            # vol slider
    "d1Amp" : 1.0,              # vol slider
    "d2Amp" : 1.0,              # vol slider
    "dry1Pan" : 0.0,            # bipolar
    "dry2Pan" : 0.0,            # bipolar
    "d1Pan" : 0.0,              # bipolar
    "d2Pan" : 0.0}              # bipolar
    
    


class Chronos(Program):

    def __init__(self, name):
        super(Chronos, self).__init__(name, "Chronos", prototype)
        self.performance = performance()

program_bank = ProgramBank(Chronos("Init"))
program_bank.enable_undo = False

def chronos(slot, name, **pmap):
    p = Chronos(name)
    for param,dflt in prototype.items():
        try:
            value = pmap[param]
        except KeyError:
            value = dflt
        p[param] = float(value)
    program_bank[slot] = p
    return p

def pp(program, slot=127):
    pad = ' '*8
    acc = 'chronos(%d,"%s",\n' % (slot, program.name)
    params = sorted(prototype.keys())
    for p in params:
        v = program[p]
        acc += '%s%s = %s' % (pad,p,v)
        if p != params[-1]:
            acc += ',\n'
        else:
            acc += ')\n'
    return acc


chronos(0,"Bypass", d1Amp=0,d2Amp=0,dry1Amp=1,dry2Amp=1,
        dry1Pan=0.0, dry2Pan=0.0,
        d1Feedback=0, d2Feedback=0)

