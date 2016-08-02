# llia.synths.lfo1.lfo1_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance
from llia.util.lmath import coin, rnd, pick


MIN_FREQ = 0.01
MAX_FREQ = 100
MAX_TIME = 60

prototype = {
	"lfoFreq" : 2.0,
	"lfoWave" : 0,  #  0 -> sine, 1 -> sine**2
	"lfoAmp" : 1.0,
	"lfoScale" : 1.0,
	"lfoBias" : 0.0,
	"lfoDelay" : 0.0,
	"lfoAttack" : 0.0,
	"lfoHold" : 1.0,
	"lfoRelease" : 1.0
    }

class Lfo1(Program):

    def __init__(self, name):
        super(Lfo1, self).__init__(name, "LFO1", prototype)

init_program = Lfo1("Init")        
program_bank = ProgramBank(init_program)
program_bank.enable_undo = False





def lfo1(slot, name,
         freq = 1.0, wave = 0.0, amp = 1.0,
         delay = 1.0, attack = None, hold = 1.0, release = None,
         bias = 0.0, scale = 1.0):
    p = Lfo1(name)
    p.performance = performance()
    p["lfoFreq"] = float(freq)
    p["lfoWave"] = float(wave)
    p["lfoAmp"] = float(amp)
    p["lfoScale"] = float(scale)
    p["lfoBias"] = float(bias)
    p["lfoDelay"] = float(delay)
    p["lfoHold"] = float(hold)
    if attack is None: attack = float(delay)
    if release is None: release = float(hold)
    p["lfoAttack"] = attack
    p["lfoRelease"] = release
    program_bank[slot] = p
    return p

def pp(program, slot=127):
    def fval(key):
        return float(program[key])
    pad = ' '*5
    acc = 'lfo1(%d, "%s",\n' % (slot, program.name)
    frmt = '%sfreq = %5.3f, wave = %5.3f, amp = %5.3f,\n'
    data = (pad, fval("lfoFreq"), fval("lfoWave"), fval("lfoAmp"))
    acc += frmt % data
    frmt = '%sdelay = %5.3f, attack = %5.3f, hold = %5.3f, release = %5.3f,\n'
    data = (pad, fval("lfoDelay"), fval("lfoAttack"), fval("lfoHold"), fval("lfoRelease"))
    acc += frmt % data
    frmt = '%sbias = %5.3f, scale = %5.3f)\n'
    data = (pad, fval("lfoBias"), fval("lfoScale"))
    acc += frmt % data
    return acc
    
def gen_lfo1(slot=127, *_):
    freq = coin(0.75, pick([1,2,3,4,4,5,5,5,6,6,6,7,7,8]),
                coin(0.75, MIN_FREQ+rnd(),
                     MIN_FREQ + rnd(MAX_FREQ-MIN_FREQ)))
    wave = coin(0.75, 0, rnd())
    delay = coin(0.50, 0, rnd(4))
    attack = coin(0.75, delay, rnd(4))
    hold = 1
    release = coin(0.75, hold, rnd(2))
    p = lfo1(slot, "Random",
             freq, wave, 1.0,
             delay, attack, hold, release)
    return p
                 
    

         
lfo1( 0, "Delay Vibrato", 5.0,  0.0, 1.0, delay = 2.0, hold = 1)
lfo1( 1, "1Hz", 1)
lfo1( 2, "2Hz", 2)
lfo1( 3, "3Hz", 3)
lfo1( 4, "4Hz", 4)
lfo1( 5, "5Hz", 5)
lfo1( 6, "6Hz", 6)
lfo1( 7, "7Hz", 7)
lfo1( 8, "8Hz", 8)
