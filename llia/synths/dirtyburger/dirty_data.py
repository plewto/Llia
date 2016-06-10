# llia.synths.dirtyburger.dirty_data
# 2016.04.26

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.util.lmath import clip, db_to_amp
from llia.performance_edit import performance

MAX_DELAY = 1.5

prototype = {
    "delayTime" : 0.125,
    "gain" : 1.0,
    "threshold" : 1.0,
    "lowcut" : 10000,
    "highcut" : 100,
    "feedback" : 0.8,
    "flutter" : 0.1,
    "wow" : 0.1,
    "wowFreq" : 1.0,
    "wetAmp" : 0.5,
    "dryAmp" : 1.0,
    "wetPan" : 0.25,
    "dryPan" : -0.25,
    "volume" : 1.0}



class DirtyBurger(Program):

    def __init__(self, name):
        super(DirtyBurger, self).__init__(name, "DirtyBurger", prototype)

INIT_PROGRAM = DirtyBurger("Init")        
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
    
        
def dirty(slot, name,
          delayTime = 0.125,
          feedback = [0.50, 1.00, 1.00],  # fb, gain, clip-threshold 
          eq = [10000, 100],        # low, high cutoff
          wow = [0.0, 0.0],         # wow, flutter
          dry = [  0, 0.0],         # db, pan
          wet = [  0, 0.0]):        # db, pan
    p = DirtyBurger(name)
    p["delayTime"] = float(clip(delayTime, 0, MAX_DELAY))
    fb, gain, threshold = fill(feedback, [0.5, 1.0, 1.0])
    p["feedback"] = float(clip(fb, 0.0, 1.0))
    p["gain"] = float(gain)
    p["threshold"] = float(threshold)
    low, high = fill(eq, [10000, 100])
    p["lowcut"] = int(clip(low, 100, 12000))
    p["highcut"] = int(clip(high, 1, 8000))
    w, flt = fill(wow, [0.0, 0.0])
    p["wow"] = float(clip(w, 0, 1))
    p["flutter"] = float(clip(flt, 0, 1))
    db, pan = fill(dry, [0, 0])
    p["dryAmp"] = float(clip(db_to_amp(db), 0, 1))
    p["dryPan"] = float(clip(pan, -1, 1))
    db, pan = fill(wet, [0, 0])
    p["wetAmp"] = float(clip(db_to_amp(db), 0, 1))
    p["wetPan"] = float(clip(pan, -1, 1))
    p.performance = performance()
    program_bank[slot] = p
    return p
                          
    
dirty(  0, "SlapBack", 0.050,
      feedback = [0.5, 1.0, 1.0],
      eq = [10000, 100],
      wow = [0.01, 0.01],
      dry = [0, -0.25],
      wet = [0,  0.25])

dirty(  1, "FastEcho", 0.100,
      feedback = [0.7, 1.0, 0.5],
      eq = [8000, 100],
      wow = [0.1, 0.1],
      dry = [0, -0.25],
      wet = [0,  0.25])
      
dirty(  2, "LongEcho", 1.500,
        feedback = [0.9, 1.0, 0.3],
        eq = [7000, 200],
        wow = [0.0, 0.0],
        dry = [0, -0.25],
        wet = [0,  0.25])
        
        

