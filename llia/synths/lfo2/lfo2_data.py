# llia.synths.lfo2.lfo2_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance

RATIOS = (0.125, 0.25, 0.5, 0.75, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 7, 8,
          9, 10, 11, 12, 13, 14, 15, 16)

RANDOM_RATIOS = (0.125, 0.25, 0.5, 0.5, 0.75,
                 1, 1, 1.5, 1.5,
                 2, 2, 2, 2.5, 3, 3, 3,
                 4, 4, 4, 5, 6, 6, 7, 8, 9,
                 10, 11, 12, 13, 14, 15, 16)

prototype = {
	"clkFreq" : 1.00, 
	"clkPw" : 0.5,    
	"clkAmp" : 0.0,   
	"sawRatio" : 4.00,
	"sawSlew" : 0.0,  
	"sawAmp" : 1.0,   
	"sawBleed" : 0.0, 
	"pulseRatio" : 4.00,
	"pulseWidth" : 0.5,
	"pulseAmp" : 1.0,
	"pulseBleed" : 0.0,
	"lag" : 0.0,
	"sawBias" : 0,
	"pulseBias" : 0}


class Lfo2(Program):

    def __init__(self, name):
        super(Lfo2, self).__init__(name, "LFO2", prototype)
        self.performance = performance()


program_bank = ProgramBank(Lfo2("Init"))
program_bank.enable_undo = False

def _fill(lst, template):
    acc = []
    for i,dflt in enumerate(template):
        try:
            v = lst[i]
        except IndexError:
            v = dflt
        acc.append(float(v))
    return acc
            

def lfo2(slot, name,
         clock = [1.0, 0.5, 0.0],      # [freq, pw, amp]
         saw = [1.0, 0.0, 1.0, 0.0],   # [ratio, shape, amp, bleed]
         pulse = [1.0, 0.5, 1.0, 0.0], # [ratio, pw, amp, bleed]
         bias = [0.0, 0.0],            # [saw, pulse]
         lag = 0.0):
    clock = _fill(clock, [1.0,0.5,1.0])
    saw = _fill(saw, [1.0, 0.0,1.0,0.0])
    pulse = _fill(pulse, [1.0,0.5,1.0,0.0])
    bias = _fill(bias, [0.0,0.0])
    p = Lfo2(name)
    p["clkFreq"] = clock[0]
    p["clkPw"] = clock[1]
    p["clkAmp"] = clock[2]
    p["sawRatio"] = saw[0]
    p["sawSlew"] = saw[1]
    p["sawAmp"] = saw[2]
    p["sawBleed"] = saw[3]
    p["pulseRatio"] = pulse[0]
    p["pulseWidth"] = pulse[1]
    p["pulseAmp"] = pulse[2]
    p["pulseBleed"] = pulse[3]
    p["lag"] = float(lag)
    p["sawBias"] = bias[0]
    p["pulseBias"] = bias[1]
    program_bank[slot] = p
    return p

def pp(program, slot=127):
    pad = ' '*5
    def fval(key):
        return float(program[key])
    def values(* params):
        bcc = [pad]
        for p in params:
            bcc.append(float(program[p]))
        return tuple(bcc)
    acc = 'lfo2(%d, "%s",\n' % (slot, program.name)
    frmt = '%sclock = [%5.3f, %5.3f, %5.3f],\n'
    acc += frmt % values('clkFreq','clkPw','clkAmp')
    frmt = '%ssaw = [%5.3f, %5.3f, %5.3f, %5.3f],\n'
    acc += frmt % values('sawRatio','sawSlew','sawAmp','sawBleed')
    frmt = '%spulse = [%5.3f, %5.3f, %5.3f, %5.3f],\n'
    acc += frmt % values('pulseRatio','pulseWidth','pulseAmp','pulseBleed')
    frmt = '%sbias = [%5.3f, %5.3f],\n'
    acc += frmt % values('sawBias','pulseBias')
    frmt = '%slag = %5.3f)\n'
    acc += frmt % (pad, float(program['lag']))
    return acc

lfo2(0,  "square",
     clock = [1.0, 0.5, 0.0],
     saw = [3.0, 0.0, 0.0, 1.0],
     pulse = [3.0, 0.5, 1.0, 1.0],
     bias = [0.0, 0.0],
     lag = 0.0)

lfo2(1,  "saw",
     clock = [1.0, 0.5, 0.0],
     saw = [3.0, 0.0, 1.0, 1.0],
     pulse = [3.0, 0.5, 0.0, 1.0],
     bias = [0.0, 0.0],
     lag = 0.0)

lfo2(2,  "tri",
     clock = [1.0, 0.5, 0.0],
     saw = [3.0, 0.5, 1.0, 1.0],
     pulse = [3.0, 0.5, 0.0, 1.0],
     bias = [0.0, 0.0],
     lag = 0.0)

lfo2(3,  "pulse-burst",
     clock = [1.0, 0.5, 0.0],
     saw = [4.0, 0.0, 0.0, 0.0],
     pulse = [4.0, 0.5, 1.0, 0.0],
     bias = [0.0, 0.0],
     lag = 0.0)

lfo2(4,  "saw-burst",
     clock = [1.0, 0.5, 0.0],
     saw = [4.0, 0.0, 1.0, 0.0],
     pulse = [4.0, 0.5, 0.0, 0.0],
     bias = [0.0, 0.0],
     lag = 0.0)

lfo2(5, "alternate-saw-pulse",
     clock = [1.0, 0.5, 0.0],
     saw = [4.0, 0.0, 1.0, 0.0],
     pulse = [4.0, 0.5, 1.0, 0.0],
     bias = [0.0, 0.0],
lag = 0.0)

lfo2(6, "Machine-1",
     clock = [1.095, 0.500, 0.000],
     saw = [6.000, 0.000, 1.000, 0.000],
     pulse = [3.000, 0.500, 1.000, 0.000],
     bias = [0.000, 0.000],
     lag = 0.000)

lfo2(7, "Fast Burst",
     clock = [1.892, 0.500, 0.000],
     saw = [7.000, 0.149, 1.000, 0.000],
     pulse = [4.000, 0.500, 1.000, 0.000],
     bias = [0.000, 0.000],
     lag = 0.000)

lfo2(8, "Machine-2",
     clock = [1.557, 0.500, 0.000],
     saw = [1.000, 0.384, 1.000, 0.000],
     pulse = [7.000, 0.264, 1.000, 0.000],
     bias = [0.000, 0.000],
     lag = 0.000)
