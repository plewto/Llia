# llia.synths.chronos.chronos_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.util.lmath import (clip,db_to_amp,amp_to_db,rnd,coin,pick)
from llia.performance_edit import performance

MAX_DELAY = 2

prototype = {"lfoCommonFreq" : 1.0,      # tumbler 0..16
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

chronos(0,"Bypass",
        d1Amp = 0.0,
        d1DelayTime = 0.1,
        d1Dry1In = 1.0,
        d1Dry2In = 0.0,
        d1ExternalModDepth = 0.0,
        d1Feedback = 0.0,
        d1Highpass = 40.0,
        d1LfoModDepth = 0.0,
        d1LfoRatio = 1.0,
        d1Lowpass = 20000.0,
        d1Pan = 0.0,
        d2Amp = 0.0,
        d2Delay1In = 0.0,
        d2DelayTime = 0.2,
        d2Dry1In = 0.0,
        d2Dry2In = 1.0,
        d2ExternalModDepth = 0.0,
        d2Feedback = 0.0,
        d2Highpass = 40.0,
        d2LfoModDepth = 0.0,
        d2LfoRatio = 1.0,
        d2Lowpass = 20000.0,
        d2Pan = 0.0,
        dry1Amp = 1.0,
        dry1Pan = 0.0,
        dry2Amp = 1.0,
        dry2Pan = 0.0,
        lfoCommonFreq = 1.0)

chronos(1,"Dual Slapback",
        d1Amp = 1.0,
        d1DelayTime = 0.075,
        d1Dry1In = 1.0,
        d1Dry2In = 0.0,
        d1ExternalModDepth = 0.0,
        d1Feedback = 0.0251256281407,
        d1Highpass = 800,
        d1LfoModDepth = 0.0,
        d1LfoRatio = 1.0,
        d1Lowpass = 20000.0,
        d1Pan = -0.758793969849,
        d2Amp = 0.707945784384,
        d2Delay1In = 0.0,
        d2DelayTime = 0.1,
        d2Dry1In = 0.0,
        d2Dry2In = 1.0,
        d2ExternalModDepth = 0.0,
        d2Feedback = 0.0251256281407,
        d2Highpass = 40.0,
        d2LfoModDepth = 0.0,
        d2LfoRatio = 4.0,
        d2Lowpass = 2000,
        d2Pan = 0.748743718593,
        dry1Amp = 1.0,
        dry1Pan = 0.748743718593,
        dry2Amp = 1.0,
        dry2Pan = -0.758793969849,
        lfoCommonFreq = 2.032)

chronos(2,"Slapback + Fast Echos",
        d1Amp = 0.707945784384,
        d1DelayTime = 0.05,
        d1Dry1In = 1.0,
        d1Dry2In = 0.0,
        d1ExternalModDepth = 0.0,
        d1Feedback = 0.195979899497,
        d1Highpass = 125,
        d1LfoModDepth = 0.0,
        d1LfoRatio = 1.0,
        d1Lowpass = 20000,
        d1Pan = 0.517587939698,
        d2Amp = 0.794328234724,
        d2Delay1In = 0.0,
        d2DelayTime = 0.1,
        d2Dry1In = 0.0,
        d2Dry2In = 1.0,
        d2ExternalModDepth = 0.0,
        d2Feedback = -0.618090452261,
        d2Highpass = 100,
        d2LfoModDepth = 0.0,
        d2LfoRatio = 1.0,
        d2Lowpass = 20000,
        d2Pan = -0.427135678392,
        dry1Amp = 1.0,
        dry1Pan = -0.467336683417,
        dry2Amp = 1.0,
        dry2Pan = 0.477386934673,
        lfoCommonFreq = 1.0)

chronos(3,"Flanger + Fast Echos",
        d1Amp = 0.707945784384,
        d1DelayTime = 0.004,
        d1Dry1In = 1.0,
        d1Dry2In = 0.0,
        d1ExternalModDepth = 0.0,
        d1Feedback = -0.869346733668,
        d1Highpass = 40,
        d1LfoModDepth = 0.070351758794,
        d1LfoRatio = 0.125,
        d1Lowpass = 20000,
        d1Pan = 0.628140703518,
        d2Amp = 0.707945784384,
        d2Delay1In = 0.0,
        d2DelayTime = 0.13,
        d2Dry1In = 0.0,
        d2Dry2In = 1.0,
        d2ExternalModDepth = 0.0,
        d2Feedback = 0.537688442211,
        d2Highpass = 125,
        d2LfoModDepth = 0.0,
        d2LfoRatio = 1.33333333333,
        d2Lowpass = 20000,
        d2Pan = -0.467336683417,
        dry1Amp = 1.0,
        dry1Pan = -0.356783919598,
        dry2Amp = 1.0,
        dry2Pan = 0.668341708543,
        lfoCommonFreq = 1.0)

chronos(4,"3ms Echo -> Echo",
        d1Amp = 0.316227766017,
        d1DelayTime = 0.3,
        d1Dry1In = 1.0,
        d1Dry2In = 0.0,
        d1ExternalModDepth = 0.0,
        d1Feedback = 0.678391959799,
        d1Highpass = 160,
        d1LfoModDepth = 0.0,
        d1LfoRatio = 1.0,
        d1Lowpass = 10000,
        d1Pan = 0.477386934673,
        d2Amp = 0.446683592151,
        d2Delay1In = 1.0,
        d2DelayTime = 0.31,
        d2Dry1In = 0.0,
        d2Dry2In = 1.0,
        d2ExternalModDepth = 0.0,
        d2Feedback = -0.768844221106,
        d2Highpass = 200,
        d2LfoModDepth = 0.0,
        d2LfoRatio = 1.0,
        d2Lowpass = 8000,
        d2Pan = -0.396984924623,
        dry1Amp = 1.0,
        dry1Pan = -0.396984924623,
        dry2Amp = 1.0,
        dry2Pan = 0.668341708543,
        lfoCommonFreq = 1.0)

chronos(5,"2sec Echo -> Echo",
        d1Amp = 0.316227766017,
        d1DelayTime = 1.3,
        d1Dry1In = 1.0,
        d1Dry2In = 0.0,
        d1ExternalModDepth = 0.0,
        d1Feedback = 0.678391959799,
        d1Highpass = 160,
        d1LfoModDepth = 0.190954773869,
        d1LfoRatio = 1.0,
        d1Lowpass = 10000,
        d1Pan = 0.477386934673,
        d2Amp = 0.446683592151,
        d2Delay1In = 1.0,
        d2DelayTime = 2.0,
        d2Dry1In = 0.0,
        d2Dry2In = 1.0,
        d2ExternalModDepth = 0.0,
        d2Feedback = -0.768844221106,
        d2Highpass = 200,
        d2LfoModDepth = 0.0,
        d2LfoRatio = 1.0,
        d2Lowpass = 8000,
        d2Pan = -0.396984924623,
        dry1Amp = 1.0,
        dry1Pan = -0.396984924623,
        dry2Amp = 1.0,
        dry2Pan = 0.668341708543,
        lfoCommonFreq = 1.0)

chronos(6,"Echo -> Can",
        d1Amp = 0.316227766017,
        d1DelayTime = 0.5,
        d1Dry1In = 1.0,
        d1Dry2In = 0.0,
        d1ExternalModDepth = 0.0,
        d1Feedback = 0.678391959799,
        d1Highpass = 160,
        d1LfoModDepth = 0.190954773869,
        d1LfoRatio = 1.0,
        d1Lowpass = 10000,
        d1Pan = 0.477386934673,
        d2Amp = 0.446683592151,
        d2Delay1In = 1.0,
        d2DelayTime = 0.002,
        d2Dry1In = 0.0,
        d2Dry2In = 1.0,
        d2ExternalModDepth = 0.0,
        d2Feedback = -0.909547738693,
        d2Highpass = 200,
        d2LfoModDepth = 0.0,
        d2LfoRatio = 1.0,
        d2Lowpass = 8000,
        d2Pan = -0.396984924623,
        dry1Amp = 1.0,
        dry1Pan = -0.396984924623,
        dry2Amp = 1.0,
        dry2Pan = 0.668341708543,
        lfoCommonFreq = 1.0)

chronos(7,"Echo -> Flange",
        d1Amp = 0.0,
        d1DelayTime = 0.3,
        d1Dry1In = 1.0,
        d1Dry2In = 0.0,
        d1ExternalModDepth = 0.0,
        d1Feedback = 0.286432160804,
        d1Highpass = 160,
        d1LfoModDepth = 0.190954773869,
        d1LfoRatio = 1.0,
        d1Lowpass = 10000,
        d1Pan = 0.477386934673,
        d2Amp = 0.316227766017,
        d2Delay1In = 1.0,
        d2DelayTime = 0.003,
        d2Dry1In = 0.0,
        d2Dry2In = 1.0,
        d2ExternalModDepth = 0.0,
        d2Feedback = -0.668341708543,
        d2Highpass = 200,
        d2LfoModDepth = 0.070351758794,
        d2LfoRatio = 1.0,
        d2Lowpass = 8000,
        d2Pan = -0.427135678392,
        dry1Amp = 1.0,
        dry1Pan = -0.396984924623,
        dry2Amp = 1.0,
        dry2Pan = 0.668341708543,
        lfoCommonFreq = 1.0)

chronos(8,"Flanger -> Flanger",
        d1Amp = 0.0,
        d1DelayTime = 0.003,
        d1Dry1In = 1.0,
        d1Dry2In = 0.0,
        d1ExternalModDepth = 0.0,
        d1Feedback = -0.939698492462,
        d1Highpass = 40,
        d1LfoModDepth = 0.0150753768844,
        d1LfoRatio = 0.125,
        d1Lowpass = 10000,
        d1Pan = 0.477386934673,
        d2Amp = 0.354813389234,
        d2Delay1In = 1.0,
        d2DelayTime = 0.001,
        d2Dry1In = 0.0,
        d2Dry2In = 1.0,
        d2ExternalModDepth = 0.0,
        d2Feedback = 0.849246231156,
        d2Highpass = 100,
        d2LfoModDepth = 0.0402010050251,
        d2LfoRatio = 0.5,
        d2Lowpass = 6300,
        d2Pan = -0.396984924623,
        dry1Amp = 1.0,
        dry1Pan = -0.396984924623,
        dry2Amp = 1.0,
        dry2Pan = 0.668341708543,
        lfoCommonFreq = 6.009)

