# llia.synths.lfo1.lfo1_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance
from llia.util.lmath import coin, rnd, pick

FREQ_RATIOS = ((0.125,"1/8"),
               (0.250,"1/4"),
               (1.0/3,"1/3"),
               (0.500,"1/2"),
               (2.0/3,"2/3"),
               (0.750,"3/4"),
               (1.0,"1"),
               (5.0/4,"1 1/4"),
               (4.0/3,"1 1/3"),
               (1.5,  "1 1/2"),
               (5.0/3, "1 2/3"),
               (7.0/4, "1 3/4"),
               (2.0, "2"),
               (2.5, "2 1/2"),
               (3.0, "3"),
               (3.5, "3 1/2"),
               (4.0, "4"),
               (5.0, "5"),
               (6.0, "6"),
               (7.0, "7"),
               (8.0, "8"),
               (9.0, "9"),
               (12.0, "12"),
               (16.0, "16"))

prototype = {
	"lfoFreq" : 1.0,
	"sineAmp" : 1.0,
	"sineRatio" : 1.0,
	"sawAmp" : 1.0,
	"sawRatio" : 1.0,
	"sawWidth" : 0.0,
	"pulseAmp" : 1.0,
	"pulseRatio" : 1.0,
	"pulseWidth" : 0.5,
	"lfoDelay" : 0.0,
	"lfoHold" : 0.5,
	"lfoBleed" : 0.0,
	"lfoScale" : 1.0,
	"lfoBias" : 0}

class LFO1(Program):

    def __init__(self, name):
        super(LFO1, self).__init__(name, "LFO1", prototype)
        self.performance = performance()

program_bank = ProgramBank(LFO1("Init"))
program_bank.enable_undo = False

def lfo1(slot, name,
         freq = 1.0,
         sineRatio = 1.0,
         sineAmp = 1.0,
         sawRatio = 1.0,
         sawWidth = 0.0,
         sawAmp = 0.0,
         pulseRatio = 1.0,
         pulseWidth = 0.5,
         pulseAmp = 0.0,
         delay = 0.0,
         hold = 0.0,
         bleed = 1.0,
         scale = 1.0,
         bias = 0.0):
    p = LFO1(name)
    p["lfoFreq"] = float(freq)
    p["sineAmp"] = float(sineAmp)
    p["sineRatio"] = float(sineRatio)
    p["sawAmp"] = float(sawAmp)
    p["sawRatio"] = float(sawRatio)
    p["sawWidth"] = float(sawWidth)
    p["pulseAmp"] = float(pulseAmp)
    p["pulseRatio"] = float(pulseRatio)
    p["pulseWidth"] = float(pulseWidth)
    p["lfoDelay"] = float(delay)
    p["lfoHold"] = float(hold)
    p["lfoBleed"] = float(bleed)
    p["lfoScale"] = float(scale)
    p["lfoBias"] = float(bias)
    program_bank[slot] = p
    return p

def pp(program,slot=127):
    def fval(key):
        return float(program[key])
    pad = ' '*5
    pmap = (("lfoFreq",  "freq"),
            ("sineAmp",  "sineAmp"),
            ("sineRatio",  "sineRatio"),
            ("sawAmp",  "sawAmp"),
            ("sawRatio",  "sawRatio"),
            ("sawWidth",  "sawWidth"),
            ("pulseAmp",  "pulseAmp"),
            ("pulseRatio",  "pulseRatio"),
            ("pulseWidth",  "pulseWidth"),
            ("lfoDelay",  "delay"),
            ("lfoHold",  "hold"),
            ("lfoBleed",  "bleed"),
            ("lfoScale",  "scale"),
            ("lfoBias",  "bias"))
    pend = pmap[-1][0]
    acc = 'lfo1(%d,"%s",\n' % (slot, program.name)
    for p,a in pmap:
        acc += '%s%s = %s' % (pad,a,fval(p))
        if p != pend:
            acc += ',\n'
        else:
            acc += ')\n'
    return acc

def random_lfo1(slot=127, *_):
    return None



lfo1(0,"Delay Vibrato 5Hz",
     freq = 5.0,
     sineAmp = 1.0,
     sineRatio = 1.0,
     sawAmp = 0.0,
     sawRatio = 1.0,
     sawWidth = 0.0,
     pulseAmp = 0.0,
     pulseRatio = 1.0,
     pulseWidth = 0.50,
     delay = 1.3,
     hold = 0.92,
     bleed = 0.0,
     scale = 0.27,
     bias = 0.0)

lfo1(1,"Delay Complex Vibrato 5Hz",
     freq = 5.0,
     sineAmp = 1.0,
     sineRatio = 1.0,
     sawAmp = 0.18,
     sawRatio = 0.75,
     sawWidth = 0.50,
     pulseAmp = 0.0,
     pulseRatio = 1.0,
     pulseWidth = 0.50,
     delay = 1.3,
     hold = 0.92,
     bleed = 0.0,
     scale = 0.15,
     bias = 0.0)

lfo1(2,"1Hz Sine",
     freq = 1.0,
     sineAmp = 1.0,
     sineRatio = 1.0,
     sawAmp = 0.0,
     sawRatio = 1.0,
     sawWidth = 0.0,
     pulseAmp = 0.0,
     pulseRatio = 1.0,
     pulseWidth = 0.5,
     delay = 0.0,
     hold = 0.5,
     bleed = 1.0,
     scale = 1.0,
     bias = 0.0)

lfo1(3,"1Hz Sawtooth",
     freq = 1.0,
     sineAmp = 0.0,
     sineRatio = 1.0,
     sawAmp = 1.0,
     sawRatio = 1.0,
     sawWidth = 0.0,
     pulseAmp = 0.0,
     pulseRatio = 1.0,
     pulseWidth = 0.5,
     delay = 0.0,
     hold = 0.5,
     bleed = 0.0,
     scale = 1.0,
     bias = 0.0)

lfo1(4,"Square Triangle",
     freq = 1.0,
     sineAmp = 0.0,
     sineRatio = 1.0,
     sawAmp = 0.45,
     sawRatio = 2.0,
     sawWidth = 0.50,
     pulseAmp = 1.0,
     pulseRatio = 1.0,
     pulseWidth = 0.5,
     delay = 0.0,
     hold = 0.5,
     bleed = 1.0,
     scale = 1.0,
     bias = 0.0)

