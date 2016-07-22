# llia.synths.syndrm.sd_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.util.lmath import clip, db_to_amp
from llia.performance_edit import performance


prototype = {
    "amp" : 0.05,
    "hhFreq" : 220,
    "hhAmp" : 1.0,
    "hhAttack" : 0.0,
    "hhDecay1" : 0.01,
    "hhDecay2" : 0.01,
    "hhRandom" : 0.1,
    "hhFilter" : 9000,
    "hhLowKey" : 71,
    "hhHighKey" : 74,
    "cymFreq" : 220,
    "cymAmp" : 1.0,
    "cymAttack" : 0.0,
    "cymDecay1" : 0.01,
    "cymDecay2" : 5.00,
    "cymRandom" : 1.0,
    "cymFilter" : 1000,
    "cymFilterRq" : 0.5,
    "cymEnvToFilter" : 8000,
    "cymLowKey" : 73,
    "cymHighKey" : 79,
    "claveFreq" : 1760,
    "claveAmp" : 0.5,
    "claveLowKey" : 79,
    "claveHighKey" : 81,
    "drum1Freq" : 110,
    "drum1Amp" : 1.0,
    "drum1Click" : 0.33,
    "drum1Attack" : 0.001,
    "drum1Decay1" : 0.001,
    "drum1Decay2" : 1.0,
    "drum1Bend" : 0.01,
    "drum1LowKey" : 59,
    "drum1HighKey" : 67,
    "rdrumFreq" : 110,
    "rdrumAttack" : 0.001,
    "rdrumDecay1" : 0.001,
    "rdrumDecay2" : 2.0,
    "rdrumAmp" : 1.0,
    "rdrumLowKey" : 66,
    "rdrumHighKey" : 73,
    "noiseFreq" : 1000,
    "noiseAmp" : 1.0,
    "noiseAttack" : 0.01,
    "noiseDecay" : 0.2,
    "noiseEnvToFreq" : 0,
    "noiseRq" : 0.5,
    "noiseLowKey" : 81,
    "noiseHighKey" : 93}

class SynDrm(Program):

    def __init__(self, name):
        super(SynDrm, self).__init__(name, "SynDrm", prototype)

program_bank = ProgramBank(SynDrm("Init"))
program_bank.enable_undo = False


