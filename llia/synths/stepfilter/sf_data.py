# llia.synths.stepfilter.sf_data
# 2016.06.11

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.util.lmath import clip, db_to_amp
from llia.performance_edit import performance


prototype = {
    "sub1" : 0.000,
    "sub2" : 0.000,
    "n1" : 1.000,
    "n2" : 0.000,
    "n3" : 0.000,
    "n4" : 0.000,
    "n5" : 0.000,
    "n6" : 0.000,
    "shFreq" : 1.000,
    "sh" : 1.000,
    "clkFreq" : 1.000,
    "minFreq" : 100,
    "maxFreq" : 2000,
    "rq" : 1.0,
    "lag" : 0.1,
    "volume" : 1,
    "wet" : 0.0,
    "pan" : 0.0}

class StepFilter(Program):

    def __init__(self, name):
        super(StepFilter, self).__init__(name, "StepFilter", prototype)

INIT_PROGRAM = StepFilter("Init");
program_bank = ProgramBank(INIT_PROGRAM)
program_bank.enable_undo = False

def fill (lst, template):
    acc = []
    for i, v in enumerate(template):
        try:
            acc.append(lst[i])
        except IndexError:
            acc.append(v)
    return acc

def sfilter(slot, name,
            pulse = [0.00, 0.00, 1.00, 0.00, 0.00, 0.00, 0.00, 0.00],
            sh = 0.00,
            shclock = 1.0,
            clock = 1.00,
            frange = [100, 2000],
            rq = 0.5,
            lag = 0.1,
            wet = 1.0,
            pan = 0.0):
    p = StepFilter(name)
    pulse = fill(pulse, (0.00, 0.00, 1.00, 0.00, 0.00, 0.00, 0.00, 0.00))
    for i, k in enumerate(("sub1","sub2", "n1", "n2", "n3", "n4", "n5", "n6")):
        amp = clip(float(pulse[i]), 0, 1)
        p[k] = amp
    p["shFreq"] = float(clip(shclock, 0.01, 10))
    p["sh"] = float(clip(sh, 0, 1))
    p["clkFreq"] = float(clip(clock, 0.01, 10))
    frange = fill(frange, (100, 10000))
    mn, mx = min(frange[0], frange[1]), max(frange[0], frange[1])
    p["minFreq"] = int(clip(mn, 10, 16000))
    p["maxFreq"] = int(clip(mx, 100, 16000))
    p["rq"] = float(clip(rq, 0.1, 1))
    p["lag"] = float(clip(lag, 0, 1))
    p["pan"] = float(clip(pan, -1, 1))
    p["wet"] = float(clip(wet, -1, 1))
    p.performance = performance()
    program_bank[slot] = p
    return p

sfilter(  0, "Saw",
          pulse = [0.000, 0.000, 1.000, 0.500, 0.333, 0.250, 0.200, 0.167],
          sh = 0.000,  shclock = 3.00,
          clock = 1.00,
          frange = [100, 2000],
          rq = 0.3,
          lag = 0.05,
          wet = 1.0,
          pan = 0.0)

sfilter(  1, "SH",
          pulse = [0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000],  
          sh = 1.00, shclock = 3.00,
          clock = 1.00,
          frange = [100, 2000],
          rq = 0.3,
          lag = 0.05,
          wet = 1.0,
          pan = 0.0)

sfilter(  2, "Pulser",
          pulse = [1.000, 1.000, 1.000, 1.000, 0.000, 0.000, 0.000, 0.000],
          sh = 0.1, shclock = 3.00,
          clock = 1.00,
          frange = [100, 3000],
          rq = 0.3,
          lag = 0.05,
          wet = 1.0,
          pan = 0.0)
          
          
    
        

