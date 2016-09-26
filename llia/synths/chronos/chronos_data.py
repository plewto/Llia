# llia.synths.chronos.chronos_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.util.lmath import (clip,db_to_amp,amp_to_db,rnd,coin,pick)
from llia.performance_edit import performance

MAX_DELAY = 2

prototype = {
	"d1InMixDry1" : 1.0,    # dry 1 -> delay 1 mix
	"d1InMixDry2" : 0.0,    # dry 2 -> delay 1 mix
	"d1Feedback" : 0.0,     # delay 1 feedback
	"d1XFeedback" : 0.0,    # delay 1 cross feedback from delay 2
	"d1DelayTime" : 0.1,    # delay 1 delay time
	"d1Lowpass" : 20000,    # delay 1 lowpass cutoff, Hz
	"d1Highpass" : 20,      # delay 1 highpass cutoff, Hz
	"d1LfoFreq" : 1,        # delay 1 LFO freq, Hz
	"d1InternalMod" : 0,    # LFO -> delay 1 time
	"d1ExternalMod" : 0,    # external -> delay 1 time
	"d1Gatted" : 0,         # delay 1 gate mode, 0=disabled, 1=enabled
	"d1WetAmp" : 1.0,       # delay 1 output mix
	"d1Pan" : 0.75,         # delay 1 pan 
	"d2InMixDry1" : 0.0,
	"d2InMixDry2" : 1.0,
	"d2Feedback" : 0.0,
	"d2XFeedback" : 0.0,
	"d2DelayTime" : 1,
	"d2Lowpass" : 20000,
	"d2Highpass" : 20,
	"d2LfoFreq" : 1,
	"d2LfoPhase" : 0,
	"d2InternalMod" : 0,
	"d2ExternalMod" : 0,
	"d2Gatted" : 0,
	"d2WetAmp" : 1.0,
	"d2Pan" : -0.75,
	"dry1Amp" : 1.0,        # dry 1 -> output mix
	"dry1Pan" : 0.0,        # dry 1 -> output pan
	"dry2Amp" : 1.0,
	"dry2Pan" : 0.0,
	"xScale" : 1.0,         # external control signal scale
	"xBias" : 0.0           # external control signal bias
    }


class Chronos(Program):

    def __init__(self, name):
        super(Chronos, self).__init__(name, "Chronos", prototype)
        self.performance = performance()

program_bank = ProgramBank(Chronos("Init"))
program_bank.enable_undo = False

def chronos(slot, name,
            delay1 = {"in1" : 0,             # db
                      "in2" : -99,           # db
                      "feedback" : 0.0,
                      "xfeedback" : 0.0,
                      "delay" : 0.1,         # seconds
                      "lowpass" : 20000,     # Hz
                      "highpass" : 20,       # Hz
                      "lfoFreq"  : 1,        # Hz
                      "internal" : 0.0,      # LFO -> mod depth
                      "external" : 0.0,      # X -> mod depth
                      "amp" : 0.0,           # output mix, db
                      "pan" : -0.75},
            delay2 = {"in1" : 0,             # db
                      "in2" : -99,           # db
                      "feedback" : 0.0,
                      "xfeedback" : 0.0,
                      "delay" : 0.1,         # seconds
                      "lowpass" : 20000,     # Hz
                      "highpass" : 20,       # Hz
                      "lfoFreq"  : 1,        # Hz
                      "lfoPhase" : 0.25,     # phase (0..1)
                      "internal" : 0.0,      # LFO -> mod depth
                      "external" : 0.0,      # X -> mod depth
                      "amp" : 0.0,           # output mix, db
                      "pan" : -0.75},
            dry1_amp = 0,                    # db
            dry1_pan = 0.0,
            dry2_amp = 0,
            dry2_pan = 0.0,
            xscale = 1.0,
            xbias = 0.0):
    p = Chronos(name)


    program_bank[slot] = p
    return p

chronos(0,"Test")
