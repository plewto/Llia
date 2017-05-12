# llia.synths.SS2.SS2_data

from __future__ import print_function
from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance

prototype = {
    "pw" : 0.5,
    "track" : 16,
    "wave" : 0,
    "filter" : 0,
    "envSelect" : 0,
    "attack" : 0.0,
    "decay" : 0.0,
    "sustain" : 1.0,
    "release" : 0.1,
    "amp" : 0.1}

class SS2(Program):

    def __init__(self,name):
        super(SS2,self).__init__(name,SS2,prototype)
        self.performance = performance()

program_bank = ProgramBank(SS2("Init"))
def ss2(slot, name,
        pw = 0.5,
        track = 16,
        wave = 0,
        filter = 0,
        envSelect = 0,
        attack = 0.0,
        decay = 0.0,
        sustain = 1.0,
        release = 0.1,
        amp = 0.1):
    def fval(x):
        return round(float(x),4)
    p = SS2(name)
    p["pw"] = fval(pw)
    p["track"] = int(track)
    p["wave"] = int(wave)
    p["filter"] = int(filter)
    p["envSelect"] = int(envSelect)
    p["attack"] = fval(attack)
    p["decay"] = fval(decay)
    p["sustain"] = fval(sustain)
    p["release"] = fval(release)
    p["amp"] = fval(amp)
    program_bank[slot] = p
    return p

ss2(0,"Saw",amp=0.1, wave=2,filter=0,track=64,pw=0.5,
    attack=0.0, decay=0.0, sustain=1.0, release=0.75, envSelect=0)

ss2(1,"Square",amp=0.1, wave=1,filter=0,track=64,pw=0.5,
    attack=0.0, decay=0.0, sustain=1.0, release=0.75, envSelect=0)

ss2(2,"Pulse1",amp=0.1, wave=1,filter=0,track=64,pw=0.25,
    attack=0.0, decay=0.0, sustain=1.0, release=0.75, envSelect=0)

ss2(3,"Pulse2",amp=0.1, wave=1,filter=0,track=64,pw=0.12,
    attack=0.0, decay=0.0, sustain=1.0, release=0.75, envSelect=0)

ss2(4,"Pulse3",amp=0.1, wave=1,filter=0,track=64,pw=0.06,
    attack=0.0, decay=0.0, sustain=1.0, release=0.75, envSelect=0)

ss2(5,"Tri",amp=0.1, wave=0,filter=0,track=64,pw=0.50,
    attack=0.0, decay=0.0, sustain=1.0, release=0.75, envSelect=0)


ss2( 6,"LPSaw",amp=0.1, wave=2,filter=1,track=6,pw=0.5,
    attack=0.0, decay=0.0, sustain=1.0, release=0.75, envSelect=0)

ss2( 7,"LPSquare",amp=0.1, wave=1,filter=1,track=6,pw=0.5,
    attack=0.0, decay=0.0, sustain=1.0, release=0.75, envSelect=0)

ss2( 8,"LPPulse1",amp=0.1, wave=1,filter=1,track=6,pw=0.25,
    attack=0.0, decay=0.0, sustain=1.0, release=0.75, envSelect=0)

ss2( 9,"LPPulse2",amp=0.1, wave=1,filter=1,track=6,pw=0.12,
    attack=0.0, decay=0.0, sustain=1.0, release=0.75, envSelect=0)

ss2(10,"LPPulse3",amp=0.1, wave=1,filter=1,track=6,pw=0.06,
    attack=0.0, decay=0.0, sustain=1.0, release=0.75, envSelect=0)

ss2(11,"LPTri",amp=0.1, wave=0,filter=1,track=6,pw=0.50,
    attack=0.0, decay=0.0, sustain=1.0, release=0.75, envSelect=0)


ss2(12,"HPSaw",amp=0.1, wave=2,filter=2,track=3,pw=0.5,
    attack=0.0, decay=0.0, sustain=1.0, release=0.75, envSelect=0)

ss2(13,"HPSquare",amp=0.1, wave=1,filter=2,track=3,pw=0.5,
    attack=0.0, decay=0.0, sustain=1.0, release=0.75, envSelect=0)

ss2(14,"HPPulse1",amp=0.1, wave=1,filter=2,track=3,pw=0.25,
    attack=0.0, decay=0.0, sustain=1.0, release=0.75, envSelect=0)

ss2(15,"HPPulse2",amp=0.1, wave=1,filter=2,track=3,pw=0.12,
    attack=0.0, decay=0.0, sustain=1.0, release=0.75, envSelect=0)

ss2(16,"HPPulse3",amp=0.1, wave=1,filter=2,track=3,pw=0.06,
    attack=0.0, decay=0.0, sustain=1.0, release=0.75, envSelect=0)

ss2(17,"HPTri",amp=0.1, wave=0,filter=2,track=1,pw=0.50,
    attack=0.0, decay=0.0, sustain=1.0, release=0.75, envSelect=0)

    
