# llia.synths.orgn.orgn_data
# 2016.06.04

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.util.lmath import clip, db_to_amp
from llia.performance_edit import performance

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
     brightness = 0.342)

orgn(  1, "Buckeye", amp=-18,
     vfreq=5.000, vdelay=0.000, vsens=0.300, vdepth=0.000,
     chorus = [0.296, 1.000],
     a = [0.500, 0.500, 1.000, 0],
     b = [1.000, 0.500, 1.000, -35],
     c = [3.000, 3.000, 0.296, 0],
     adsr = [0.015, 1.000, 1.000, 0.000],
     brightness = 0.387)

orgn(  2, "Cleghorn", amp=-11,
     vfreq=5.994, vdelay=1.338, vsens=0.261, vdepth=0.000,
     chorus = [0.261, 0.573],
     a = [0.500, 0.500, 0.503, 0],
     b = [2.020, 1.001, 0.427, -11],
     c = [2.000, 3.002, 0.055, -17],
     adsr = [0.000, 1.000, 1.000, 0.000],
     brightness = 0.302)

orgn(  3, "Cresco", amp=-12,
     vfreq=7.000, vdelay=1.532, vsens=0.191, vdepth=0.000,
     chorus = [0.734, 0.281],
     a = [0.500, 1.000, 0.156, 0],
     b = [1.000, 1.000, 0.151, -20],
     c = [2.000, 1.000, 0.724, -14],
     adsr = [0.000, 0.734, 0.965, 0.628],
     brightness = 0.714)

orgn(  4, "Albion", amp=-17,
     vfreq=4.989, vdelay=1.761, vsens=0.065, vdepth=0.000,
     chorus = [0.000, 1.000],
     a = [0.500, 1.000, 0.352, -17],
     b = [1.005, 1.000, 0.749, 0],
     c = [3.025, 0.997, 0.402, -8],
     adsr = [0.000, 1.000, 1.000, 0.000],
     brightness = 0.513)

orgn(  5, "Amboy", amp=-18,
     vfreq=5.890, vdelay=2.679, vsens=0.387, vdepth=0.246,
     chorus = [0.327, 0.673],
     a = [0.500, 0.500, 0.477, 0],
     b = [2.000, 2.000, 0.286, -8],
     c = [3.005, 2.000, 0.628, -29],
     adsr = [0.000, 1.000, 1.000, 0.000],
     brightness = 0.628)

orgn(  6, "Arcadia", amp=-18,
     vfreq=4.989, vdelay=0.000, vsens=0.146, vdepth=0.000,
     chorus = [0.950, 1.000],
     a = [0.500, 0.500, 0.709, 0],
     b = [1.000, 0.500, 0.352, -17],
     c = [3.000, 3.005, 0.005, -8],
     adsr = [0.000, 1.000, 1.000, 0.000],
     brightness = 1.000)

orgn(  7, "Avon", amp=-18,
     vfreq=4.989, vdelay=1.018, vsens=0.241, vdepth=0.000,
     chorus = [0.427, 0.000],
     a = [0.500, 0.250, 0.704, -20],
     b = [1.000, 1.000, 0.281, 0],
     c = [1.500, 1.000, 0.462, -9],
     adsr = [0.000, 0.387, 0.754, 0.930],
     brightness = 0.573)

orgn(  8, "Birdseye", amp=-18,
     vfreq=4.989, vdelay=0.000, vsens=0.266, vdepth=0.000,
     chorus = [0.271, 1.000],
     a = [0.500, 0.500, 0.106, -29],
     b = [1.000, 1.000, 0.598, 0],
     c = [3.000, 2.000, 0.633, -9],
     adsr = [0.000, 0.503, 0.317, 0.769],
     brightness = 0.618)

orgn(  9, "Blountsville", amp=-18,
     vfreq=5.682, vdelay=1.421, vsens=0.186, vdepth=0.427,
     chorus = [0.000, 0.000],
     a = [1.000, 2.000, 0.769, 0],
     b = [2.000, 4.000, 0.342, -5],
     c = [4.000, 8.000, 0.548, -11],
     adsr = [0.000, 0.950, 0.618, 0.518],
     brightness = 0.271)

orgn( 10, "Boswell", amp=-18,
     vfreq=6.965, vdelay=0.911, vsens=0.045, vdepth=0.000,
     chorus = [0.000, 1.000],
     a = [0.500, 0.500, 0.819, 0],
     b = [0.993, 0.991, 0.477, 0],
     c = [1.508, 2.010, 0.307, -12],
     adsr = [0.000, 1.000, 1.000, 0.000],
     brightness = 1.000)

orgn( 11, "Brocksburg", amp=-18,
     vfreq=5.994, vdelay=0.000, vsens=0.794, vdepth=0.000,
     chorus = [0.181, 0.000],
     a = [0.500, 0.500, 0.844, 0],
     b = [1.503, 3.518, 0.327, -2],
     c = [4.010, 2.000, 0.060, -4],
     adsr = [0.000, 0.663, 0.563, 0.141],
     brightness = 0.573)

orgn( 12, "Bristol", amp=-18,
     vfreq=4.989, vdelay=0.112, vsens=0.065, vdepth=0.000,
     chorus = [0.000, 1.000],
     a = [0.500, 0.500, 0.337, -23],
     b = [2.000, 2.000, 0.568, 0],
     c = [2.000, 1.503, 0.095, -8],
     adsr = [0.000, 0.774, 0.724, 0.367],
     brightness = 0.734)

orgn( 13, "Cadiz", amp=-18,
     vfreq=4.989, vdelay=2.453, vsens=0.068, vdepth=0.000,
     chorus = [0.698, 4.000],
     a = [0.500, 0.250, 0.005, -5],
     b = [1.005, 0.500, 0.166, 0],
     c = [3.005, 1.000, 0.482, -15],
     adsr = [0.101, 1.000, 1.000, 1.000],
     brightness = 0.859)

orgn( 14, "Cayuga", amp=-11,
     vfreq=6.965, vdelay=2.263, vsens=0.296, vdepth=0.000,
     chorus = [0.095, 2.090],
     a = [0.500, 0.500, 0.226, 0],
     b = [3.005, 1.000, 0.513, -31],
     c = [2.000, 2.000, 0.085, 0],
     adsr = [0.000, 0.332, 0.226, 0.000],
     brightness = 0.789)

orgn( 15, "Chalmers", amp=-17,
     vfreq=5.994, vdelay=1.157, vsens=0.899, vdepth=0.000,
     chorus = [0.698, 0.111],
     a = [0.500, 0.250, 1.000, 0],
     b = [1.000, 0.500, 0.749, 0],
     c = [3.005, 3.005, 0.497, -8],
     adsr = [0.000, 0.563, 0.905, 0.347],
     brightness = 0.327)

