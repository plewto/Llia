# llia.synths.qmod.qmod_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance

FILTER_VALUES = (1000,2000,5000,10000,20000)
MAX_INPUT_GAIN_MAGNITUDE = 6

prototype = {
	"keyTrack" : 0.0,       # float 0..16  (tumbler)
	"fixedFrequency" : 1.0, # int   0..8k  (tumbler)
	"inputFilter" : 5000,   # int   msb
	"inputGain" : 1.0,      # int msb powers of 10
	"modDepth" : 1.0,       # norm
	"attack" : 0.01,        # 0..4
	"release" : 0.01,       # 0..4
	"envelopeSelect" : 0,   # int 0->env follower, 1->ASR
	"wetAmp" : 1.0,         # volume
	"dryAmp" : 1.0          # volume
}


class QMod(Program):

    def __init__(self,name):
        super(QMod,self).__init__(name,QMod,prototype)
        self.performance = performance()

program_bank = ProgramBank(QMod("Init"))
program_bank.enable_undo = False

def qmod(slot, name,
	 keyTrack = 0.0,
	 fixedFrequency = 1.0,
	 inputFilter = 5000,
	 inputGain = 1.0,
	 modDepth = 1.0,
	 attack = 0.01,
	 release = 0.01,
	 envelopeSelect = 0,
	 wetAmp = 1.0,
	 dryAmp = 1.0,):
   p = QMod(name)
   p["keyTrack"] = float(keyTrack)
   p["fixedFrequency"] = int(fixedFrequency)
   p["inputFilter"] = int(inputFilter)
   p["inputGain"] = int(inputGain)
   p["modDepth"] = float(modDepth)
   p["attack"] = float(attack)
   p["release"] = float(release)
   p["envelopeSelect"] = int(envelopeSelect)
   p["wetAmp"] = float(wetAmp)
   p["dryAmp"] = float(dryAmp)
   program_bank[slot] = p
   return p

def pp(program,slot=127):
    pad = ' '*5
    acc = 'qmod(%d,"%s",\n' % (slot,program.name)
    iparams = ("fixedFrequency","inputFilter","inputGain","envelopeSelect")
    for p in iparams:
        val = int(program[p])
        acc += '%s%s = %d,\n' % (pad,p,val)
    fparams = ("keyTrack","modDepth","attack","release","wetAmp","dryAmp")
    terminal = fparams[-1]
    for p in fparams:
        val = float(program[p])
        acc += '%s%s = %5.3f' % (pad,p,val)
        if p == terminal:
            acc += ")\n"
        else:
            acc += ",\n"
    return acc


qmod(0,"Bypass",
     dryAmp = 0.0,
     wetAmp = 1.0,)

qmod(1,"drive100",
     keyTrack = 1.0,
     fixedFrequency = 0.0,
     inputFilter = 20000,
     inputGain = 100,
     modDepth = 0.0,
     attack = 0.01,
     release = 0.01,
     envelopeSelect = 1,
     wetAmp = 1.0,
     dryAmp = 1.0)

qmod(2,"drive1000",
     keyTrack = 1.0,
     fixedFrequency = 0.0,
     inputFilter = 20000,
     inputGain = 1000,
     modDepth = 0.0,
     attack = 0.01,
     release = 0.01,
     envelopeSelect = 1,
     wetAmp = 1.0,
     dryAmp = 1.0)

qmod(3,"drive5x ",
     keyTrack = 1.0,
     fixedFrequency = 0.0,
     inputFilter = 20000,
     inputGain = 100000,
     modDepth = 0.0,
     attack = 0.01,
     release = 1.01,
     envelopeSelect = 1,
     wetAmp = 1.0,
     dryAmp = 1.0)

qmod(4,"drive6x  ",
     keyTrack = 1.0,
     fixedFrequency = 0.0,
     inputFilter = 20000,
     inputGain = 1000000,
     modDepth = 0.0,
     attack = 0.01,
     release = 1.01,
     envelopeSelect = 1,
     wetAmp = 1.0,
     dryAmp = 1.0)

