# llia.synths.orgn.orgn_data
# 2016.06.04

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.util.lmath import clip, db_to_amp
from llia.performance_edit import performance, smap, ccmap

prototype = {"amp" : 0.05,
             "vfreq" : 5.0,
             "vdelay" : 2.0,
             "vsens" : 0.30,
             "vdepth" : 0.0,
             "vibrato" : 0.0,
             "chorus" : 0.0,
             "chorusDelay" : 1.0,
             "c1" : 0.5,
             "m1" : 0.5,
             "mod1" : 1.0,
             "amp1" : 1.0,
             "c2" : 1.0,
             "m2" : 1.0,
             "mod2" : 1.0,
             "amp2" : 1.0,
             "c3" : 3.0,
             "m3" : 3.0,
             "mod3" : 0.0,
             "amp3" : 1.0,
             "attack3" : 0.0,
             "decay3" : 0.0,
             "sustain3" : 1.0,
             "release3" : 0.0,
             "brightness" : 1.0}

class Orgn(Program):

    def __init__(self, name):
        super(Orgn, self).__init__(name, "Orgn", prototype)

program_bank = ProgramBank(Orgn("Init"))
program_bank.enable_undo = False

def nlimit(value):
    return clip(float(value), 0.0, 1.0)

def fill(lst, template):
    acc = []
    for i, v in enumerate(template):
        try:
            acc.append(lst[i])
        except IndexError:
            acc.append(v)
    return acc

def orgn(slot, name, amp=-12,
         vfreq=5.0, vdelay=0.0, vsens=0.30, vdepth=0.00,
         chorus = [0.00, 1.00],
         a=[0.5, 0.5, 1.00, 0], # [c m mod db]
         b=[1.0, 0.5, 1.00, 0],
         c=[3.0, 3.0, 1.00, 0],
         adsr = [0.0, 1.0, 1.0, 0.0],
         brightness = 1.0):
    p = Orgn(name)
    p["amp"] = db_to_amp(min(amp, 12))
    p["vfreq"] = float(max(0.001, vfreq))
    p["vdelay"] = abs(float(vdelay))
    p["vsens"] = nlimit(vsens)
    chorus = fill(chorus, [0.0, 1.0])
    p["chorus"] = nlimit(chorus[0])
    p["chorusDelay"] = float(max(chorus[1], 0))
    a = fill(a, [0.5, 0.5, 1.0, 0])
    p["c1"] = float(max(a[0], 0.125))
    p["m1"] = float(max(a[1], 0.125))
    p["mod1"] = nlimit(a[2])
    p["amp1"] = db_to_amp(clip(a[3], -99, 0))
    b = fill(b, [1.0, 0.5, 1.0, 0])
    p["c2"] = float(max(b[0], 0.125))
    p["m2"] = float(max(b[1], 0.125))
    p["mod2"] = nlimit(b[2])
    p["amp2"] = db_to_amp(clip(b[3], -99, 0))
    c = fill(c, [3.0, 1.5, 0.0, 0])
    p["c3"] = float(max(c[0], 0.125))
    p["m3"] = float(max(c[1], 0.125))
    p["mod3"] = nlimit(c[2])
    p["amp3"] = db_to_amp(clip(c[3], -99, 0))
    adsr = fill(adsr, [0.0, 1.0, 1.0, 0.0])
    p["attack3"] = float(max(0, adsr[0]))
    p["decay3"] = float(max(0, adsr[1]))
    p["sustain3"] = nlimit(adsr[2])
    p["release3"] = float(max(0, adsr[3]))
    p["brightness"] = nlimit(brightness)
    p.performance = performance()
    program_bank[slot] = p
    return p

orgn(  0, "Boxholm", amp=-18,
     vfreq=5.000, vdelay=0.000, vsens=0.300, vdepth=0.000,
     chorus = [0.000, 1.000],
     a = [0.500, 0.500, 1.000, 0],
     b = [1.000, 0.500, 1.000, 0],
     c = [3.000, 1.500, 0.000, 0],
     adsr = [0.000, 1.000, 1.000, 1.000],
     brightness = 1.000)

orgn(1, "Buckeye", amp=-18,
     vfreq = 5.00, vdelay = 0.0, vsens = 0.30, vdepth = 0.00,
     chorus = [0.30, 1.00],
     a = [0.500, 0.500, 1.000,   0],
     b = [1.000, 0.500, 1.000, -36],
     c = [3.000, 3.000, 0.300,   0],
     adsr = [0.020, 1.000, 1.000, 0.000],
     brightness = 1.00)

orgn(2, "Cleghorn", amp=-12,
     vfreq=6.000, vdelay=1.338, vsens=0.263, vdepth=0.000,
     chorus = [0.000, 0.252],
     a = [0.500, 0.500, 0.504, 0],
     b = [2.018, 1.001, 0.432, -12],
     c = [2.000, 3.002, 0.056, -18],
     adsr = [0.000, 1.000, 1.000, 0.000],
     brightness = 1.000)

orgn(3, "Cresco", amp=-12,
     vfreq=8.000, vdelay=1.532, vsens=0.192, vdepth=0.000,
     chorus = [0.735, 0.282],
     a = [0.500, 1.000, 0.156, 0],
     b = [1.000, 1.000, 0.155, -21],
     c = [2.000, 1.000, 0.727, -15],
     adsr = [0.000, 0.736, 0.968, 0.631],
     brightness = 1.000)

orgn(4, "Dubuque", amp=-12,
     vfreq=6.000, vdelay=1.732, vsens=0.075, vdepth=0.000,
     chorus = [0.886, 2.981],
     a = [0.500, 0.500, 0.115, 0],
     b = [0.992, 1.007, 0.781, -30],
     c = [2.974, 3.021, 0.029, -18],
     adsr = [0.000, 1.000, 1.000, 0.000],
     brightness = 1.000)
