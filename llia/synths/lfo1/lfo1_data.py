# llia.synths.lfo1.lfo1_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance
from llia.util.lmath import coin, rnd, pick

prototype = {
	"lfoFreq" : 1.0,
	"lfoFeedback" : 0.0,
	"lfoDelay" : 0.0,
	"lfoAttack" : 0.0,
	"lfoHold" : 0.5,
	"lfoRelease" : 0.5,
	"lfoBleed" : 0.0,
	"lfoScale" : 1.0,
	"lfoBias" : 0.0}

class Lfo1(Program):

    def __init__(self, name):
        super(Lfo1, self).__init__(name, "LFO1", prototype)
        self.performance = performance()

init_program = Lfo1("Init")        
program_bank = ProgramBank(init_program)
program_bank.enable_undo = False

def lfo1(slot, name,
         freq=1, feedback=0, bleed=0,
         delay=0, attack=0, hold=0, release=0,
         scale=1, bias=0):
    p = Lfo1(name)
    p["lfoFreq"] = float(freq)
    p["lfoFeedback"] = float(feedback)
    p["lfoDelay"] = float(delay)
    p["lfoAttack"] = float(attack)
    p["lfoHold"] = float(hold)
    p["lfoRelease"] = float(release)
    p["lfoBleed"] = float(bleed)
    p["lfoScale"] = float(scale)
    p["lfoBias"] = float(bias)
    program_bank[slot] = p
    return p

def pp(program, slot=127):
    def fval(key):
        return float(program[key])
    pad = ' '*5
    acc = 'lfo1(%d,"%s",\n' % (slot, program.name)
    frmt = '%sfreq=%5.3f, feedback=%5.3f, bleed=%5.3f,\n'
    acc += frmt % (pad,fval("lfoFreq"),fval("lfoFeedback"),fval("lfoBleed"))
    frmt = '%sscale=%5.3f, bias=%5.3f)\n'
    acc += frmt % (pad,fval("lfoScale"),fval("lfoBias"))
    return acc

def random_lfo1(slot=127, *_):
    p = lfo1(slot, "Random",
             freq = coin(0.75, rnd(5), rnd(10)),
             feedback = coin(0.75, 0, coin(0.75, rnd(0.75), rnd())),
             bleed = coin(0.5, 0, rnd()),
             delay = coin(0.5, 0, rnd(4)),
             attack = coin(0.75, delay, rnd(4)),
             hold = 1,
             release = coin(0.75, hold, rnd(4)),
             scale = 1.0,
             bias = 0)
    return p

lfo1( 0, "scale=1", freq=1, bleed=1,
      delay = 1, attack=2, hold=3, release=4,
      scale = 1)


lfo1( 1, "scale=2", freq=2, bleed=1,
      delay=5, attack=6, hold=7, release=8,
      scale = 2)


lfo1( 2, "scale=3", freq=3, bleed=1,
      scale = 3)
      
lfo1( 3, "scale=4", freq=4, bleed=1,
      scale = 4)

lfo1( 4, "scale = 0.5", freq=5, bleed=1, scale=0.5)
lfo1( 5, "scale = 0.25", freq=6, bleed=1, scale = 0.25)
lfo1( 6, "7Hz", freq=7, bleed=1)
lfo1( 7, "8Hz", freq=8, bleed=1)
