# llia.synths.masa.masa_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.util.lmath import db_to_amp
from llia.performance_edit import performance

prototype = {"amp" : 0.1,
             "xBias" : 1.0,    
	     "xScale" : 0.5,   
	     "xToFreq" : 0.0,  
	     "vfreq" : 5.0,    
	     "vdelay" : 0.0,   
	     "vsens" : 0.01,   
	     "vdepth" : 0.0,   
	     "vibrato" : 0.0,  
	     "attack" : 0.01,  
	     "decay" : 0.20,   
	     "a1" : 1.00,      
	     "a2" : 0.00,      
	     "a3" : 0.00,
	     "a4" : 0.00,
	     "a5" : 0.00,
	     "a6" : 0.00,
	     "a7" : 0.00,
	     "a8" : 0.00,
	     "a9" : 0.00,
	     "x1" : 0.00,      
	     "x2" : 0.00,      
	     "x3" : 0.00,
	     "x4" : 0.00,
	     "x5" : 0.00,
	     "x6" : 0.00,
	     "x7" : 0.00,
	     "x8" : 0.00,
	     "x9" : 0.00,
	     "p1" : 0.00,      
	     "p2" : 0.00,      
	     "p3" : 0.00,      
	     "p4" : 0.00,      
	     "p5" : 0.00,
	     "p6" : 0.00,
	     "p7" : 0.00,
	     "p8" : 0.00,
	     "p9" : 0.00}

class Masa(Program):

    def __init__(self, name):
        super(Masa, self).__init__(name, "MASA", prototype)

program_bank = ProgramBank(Masa("Init"))

def _fill_xbus(prog, xmap):
    prog["xBias"] = float(xmap.get("bias", 1.0))
    prog["xScale"] = float(xmap.get("scale", 0.5))
    prog["xToFreq"] = float(xmap.get("freq", 0.0))

def _fill_vibrato(prog, vmap):
    prog["vfreq"] = float(vmap.get("freq", 5.0))
    prog["vdelay"] = float(vmap.get("delay", 0.0))
    prog["vsens"] = float(vmap.get("sens", 0.1))
    prog["vdepth"] = float(vmap.get("depth", 0.0))
    prog["vibrato"] = 0.0
    
def _fill_amps(prog, alst):
    v = 0
    for i in range(9):
        j = i+1
        p = "a%d" % j
        try:
            v = float(alst[i])
        except IndexError:
            v = 0.0
        prog[p] = v

def _fill_xtrem(prog, tlst):
    v = 0
    for i in range(9):
        j = i+1
        p = "x%d" % j
        try:
            v = float(tlst[i])
        except IndexError:
            v = 0.0
        prog[p] = v

def _fill_perc(prog, plst):
    v = 0
    for i in range(9):
        j = i+1
        p = "p%d" % j
        try:
            v = float(plst[i])
        except IndexError:
            v = 0.0
        prog[p] = v
    
def masa(slot, name, amp=-12,
         xbus = {"bias" : 1.0,
                 "scale" : 0.5,
                 "freq" : 0.0},
         vibrato = {"freq" : 5.0,
                    "delay" : 0.0,
                    "sens" : 0.1,
                    "depth" : 0.0},
         env = [0.01, 0.20],     # [attack, decay]
         amps = [0.00, 0.00, 1.00,  0.00, 0.00, 0.00,  0.00, 0.00, 0.00],
         xtrem = [0.00, 0.00, 0.00,  0.00, 0.00, 0.00,  0.00, 0.00, 0.00],
         perc = [0.00, 0.00, 0.00,  0.00, 0.00, 0.00,  0.00, 0.00, 0.00]):
    p = Masa(name)
    p.performance = performance()
    _fill_xbus(p, xbus)
    _fill_vibrato(p, vibrato)
    _fill_amps(p, amps)
    _fill_xtrem(p, xtrem)
    _fill_perc(p, perc)
    p["amp"] = db_to_amp(amp)
    program_bank[slot] = p
    return p
    
masa(0, "Albatross", amp=-19,
     xbus = {"bias"  : 1.000,
             "scale" : 0.500,
             "freq"  : 0.000},
     vibrato = {"freq"  : 5.056,
                "delay" : 0.980,
                "sens"  : 0.040,
                "depth" : 0.226},
     env = [0.002, 0.951],
     amps  = [0.00,0.00,0.76,0.95,0.44,0.66,0.00,0.80,0.58],
     xtrem = [0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00],
     perc  = [0.00,0.00,0.00,0.00,0.00,0.00,0.73,0.64,0.35])

masa(1, "Auklet", amp=-18,
     xbus = {"bias"  : 1.000,
             "scale" : 0.500,
             "freq"  : 0.000},
     vibrato = {"freq"  : 5.056,
                "delay" : 0.980,
                "sens"  : 0.040,
                "depth" : 0.226},
     env = [0.000, 0.148],
     amps  = [0.00,0.58,1.00,0.00,0.68,0.00,0.54,0.02,0.78],
     xtrem = [0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00],
     perc  = [0.00,0.00,0.00,0.00,0.00,0.00,0.85,0.00,0.35])

masa(2, "Least Bittern", amp=-17,
     xbus = {"bias"  : 1.000,
             "scale" : 0.500,
             "freq"  : 0.000},
     vibrato = {"freq"  : 5.056,
                "delay" : 0.980,
                "sens"  : 0.040,
                "depth" : 0.000},
     env = [0.000, 0.148],
     amps  = [0.00,0.72,1.00,1.00,0.80,0.00,0.00,0.00,0.28],
     xtrem = [0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00],
     perc  = [0.00,0.00,0.00,0.00,0.00,0.00,0.85,0.00,0.35])

masa(3, "Indigo Bunting", amp=-19,
     xbus = {"bias"  : 1.000,
             "scale" : 0.500,
             "freq"  : 0.000},
     vibrato = {"freq"  : 6.337,
                "delay" : 1.780,
                "sens"  : 0.055,
                "depth" : 0.342},
     env = [0.010, 0.200],
     amps  = [0.00,0.00,1.00,0.00,0.00,0.00,0.00,0.91,0.93],
     xtrem = [0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00],
     perc  = [0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00])

masa(4, "American Coot", amp=-19,
     xbus = {"bias"  : 1.000,
             "scale" : 0.500,
             "freq"  : 0.000},
     vibrato = {"freq"  : 5.000,
                "delay" : 0.000,
                "sens"  : 0.010,
                "depth" : 0.000},
     env = [0.000, 1.000],
     amps  = [1.00,0.00,1.00,0.78,0.32,0.84,0.54,0.61,0.36],
     xtrem = [0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00],
     perc  = [0.00,0.00,0.00,0.00,0.00,0.00,0.19,0.00,0.17])

masa(5, "Fish Crow", amp=-19,
     xbus = {"bias"  : 1.000,
             "scale" : 0.500,
             "freq"  : 0.000},
     vibrato = {"freq"  : 6.919,
                "delay" : 0.000,
                "sens"  : 0.131,
                "depth" : 0.000},
     env = [0.010, 0.200],
     amps  = [1.00,1.00,0.00,0.00,0.00,1.00,0.00,0.00,0.00],
     xtrem = [0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00],
     perc  = [0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00])

masa(6, "Black Duck", amp=-18,
     xbus = {"bias"  : 1.000,
             "scale" : 0.500,
             "freq"  : 0.000},
     vibrato = {"freq"  : 6.919,
                "delay" : 0.000,
                "sens"  : 0.131,
                "depth" : 0.000},
     env = [0.010, 0.200],
     amps  = [0.00,0.00,1.00,0.78,0.64,0.00,0.59,0.55,0.18],
     xtrem = [0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00],
     perc  = [0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00])

masa(7, "Marbled Godwit", amp=-27,
     xbus = {"bias"  : 1.000,
             "scale" : 0.500,
             "freq"  : 0.000},
     vibrato = {"freq"  : 6.480,
                "delay" : 1.480,
                "sens"  : 0.070,
                "depth" : 0.276},
     env = [0.010, 0.200],
     amps  = [1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00],
     xtrem = [0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00],
     perc  = [0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00])
