# llia.synths.orgn,orgn_data
# 2016.04.23

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.util.lmath import clip, db_to_amp

prototype = {"amp" : 0.50,
             "pan" : 0.0,
             "lfoFreq" : 5.0,
             "lfoDepth" : 0.0,
             "lfoDelay" : 0.0,
             "vibrato" : 0.0,
             "vsens" : 0.01,
             "chorus" : 0.0,
             "chorusDelay" : 0.0,
             "tremoloA" : 0.0,
             "modDepthA" : 0.4,
             "mixA" : 1.0,
             "tremoloB" : 0.0,
             "modDepthB" : 0.0,
             "detuneB" : 1.0,
             "ratioB" : 1.0,
             "decayB" : 0.0,
             "sustainB" : 1.0,
             "mixB" : 0.0}

class Orgn(Program):

    def __init__(self, name):
        super(Orgn, self).__init__(name, "ORGN", prototype)

program_bank = ProgramBank(Orgn("Init"))
program_bank.enable_undo = False

def nlimit(value):
    return clip(float(value), 0.0, 1.0)


def orgn(slot, name, amp=0.05, pan=0.0,
         lfo = [5.0, 0.0, 0.0],
         vib = [0.0, 0.01],
         chorus = [0.0, 0.0],
         a = [0.4, 0.0, 1.0],
         b = [0.4, 0.0, 1.0],
         bfreq = [2, 2],
         benv = [1.0, 1.0]):
    p = Orgn(name)
    p["amp"] = db_to_amp(min(amp, 12))
    p["pan"] = pan
    p["lfoFreq"] = max(0.01, float(lfo[0]))
    p["lfoDepth"] = nlimit(lfo[1])
    p["vibrato"] = nlimit(vib[0])
    p["vsens"] = nlimit(vib[1])
    p["chorus"] = nlimit(chorus[0])
    p["chorusDelay"] = max(0.0, float(chorus[1]))
    p["tremoloA"] = nlimit(a[1])
    p["modDepthA"] = nlimit(a[0])
    p["mixA"] = db_to_amp(a[2])
    p["tremoloB"] = nlimit(b[1])
    p["modDepthB"] = nlimit(b[0])
    p["mixB"] = db_to_amp(b[2])
    p["detuneB"] = float(bfreq[0])
    p["ratioB"] = float(bfreq[1])
    p["decayB"] = nlimit(benv[0])
    p["sustainB"] = nlimit(benv[1])
    program_bank[slot] = p
    return p


#orgn(0, "Init")

orgn(  0, "Boxholm",
          amp=-12, pan=+0.000,
          lfo=[5.000, 0.010, 1.000],
          vib=[0.000, 0.010],
          chorus=[0.300, 1.000],
          a=[0.400, 0.000,  +0],
          b=[0.400, 0.000,  +0],
          bfreq=[1, 2],
          benv=[1.000, 1.000])

orgn(  1, "Buckeye",
          amp=-12, pan=+0.000,
          lfo=[6.000, 0.100, 1.000],
          vib=[0.001, 0.010],
          chorus=[0.650, 2.000],
          a=[0.400, 0.000,  +0],
          b=[0.500, 0.000,  +0],
          bfreq=[1, 1],
          benv=[1.000, 1.000])

orgn(  2, "Cleghorn",
          amp=-12, pan=+0.000,
          lfo=[5.000, 0.900, 1.000],
          vib=[0.000, 0.000],
          chorus=[0.100, 1.000],
          a=[0.900, 1.000, -12],
          b=[0.400, 0.000,  +0],
          bfreq=[0, 0],
          benv=[1.000, 1.000])



orgn(  4, "Cresco",
          amp=-12, pan=+0.000,
          lfo=[5.000, 0.250, 0.840],
          vib=[0.000, 0.010],
          chorus=[0.000, 0.000],
          a=[0.400, 0.000,  +0],
          b=[0.400, 0.300,  +0],
          bfreq=[2, 0],
          benv=[1.000, 1.000])

orgn(  5, "Dubuque",
          amp=-12, pan=+0.000,
          lfo=[5.000, 0.620, 0.560],
          vib=[0.000, 0.010],
          chorus=[0.000, 0.000],
          a=[0.400, 1.000, -32],
          b=[0.730, 0.000,  +0],
          bfreq=[1, 2],
          benv=[1.000, 1.000])

orgn(  6, "Dunkerton",
          amp=-12, pan=+0.000,
          lfo=[5.000, 0.180, 3.240],
          vib=[0.000, 0.000],
          chorus=[0.790, 1.160],
          a=[0.400, 0.000,  +0],
          b=[0.820, 0.380,  -1],
          bfreq=[0, 3],
          benv=[0.220, 0.570])

orgn(  7, "Earlham",
          amp=-12, pan=+0.000,
          lfo=[5.140, 0.230, 3.560],
          vib=[0.000, 0.010],
          chorus=[0.000, 0.000],
          a=[0.190, 0.360,  -2],
          b=[0.400, 0.000,  -8],
          bfreq=[0, 3],
          benv=[1.000, 0.000])

orgn(  8, "Keokuk",
          amp= -4, pan=+0.000,
          lfo=[4.960, 0.000, 0.000],
          vib=[0.000, 0.010],
          chorus=[0.000, 0.000],
          a=[0.320, 0.000,  +0],
          b=[0.400, 0.000, -99],
          bfreq=[0, 0],
          benv=[1.000, 1.000])

orgn(  9, "Bayard",
          amp=-12, pan=+0.000,
          lfo=[5.000, 0.010, 1.000],
          vib=[0.000, 0.010],
          chorus=[0.300, 1.000],
          a=[0.400, 0.000,  +0],
          b=[0.400, 0.000,  +0],
          bfreq=[0, 0],
          benv=[1.000, 1.000])
