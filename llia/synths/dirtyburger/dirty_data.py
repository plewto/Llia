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
     feedback = [0.500, 1.000, 1.000],
     eq = [10000, 100],
     wow = [0.010, 0.010],
     dry = [0, -0.250],
     wet = [0, 0.250])

dirty(  1, "FastEcho", 0.100,
     feedback = [0.700, 1.000, 0.500],
     eq = [8000, 100],
     wow = [0.100, 0.100],
     dry = [0, -0.250],
     wet = [0, 0.250])

dirty(  2, "LongEcho", 1.500,
     feedback = [0.900, 1.000, 0.300],
     eq = [7000, 200],
     wow = [0.000, 0.000],
     dry = [0, -0.250],
     wet = [0, 0.250])

dirty(  3, "Fast & Dark", 0.128,
     feedback = [0.734, 1.040, 0.362],
     eq = [2500, 100],
     wow = [0.095, 0.095],
     dry = [0, -0.250],
     wet = [-18, 0.250])

dirty(  4, "Fast & High", 0.082,
     feedback = [0.774, 1.228, 0.693],
     eq = [20000, 1250],
     wow = [0.000, 0.100],
     dry = [0, -0.250],
     wet = [-12, 0.250])

dirty(  5, "ThreeQuarters", 0.750,
     feedback = [0.774, 1.055, 1.000],
     eq = [5000, 400],
     wow = [0.000, 0.000],
     dry = [0, -0.250],
     wet = [-12, 0.250])

dirty(  6, "Wow & Flutter", 0.323,
     feedback = [0.548, 1.055, 1.000],
     eq = [20000, 20],
     wow = [0.372, 0.126],
     dry = [0, -0.250],
     wet = [-6, 0.250])

dirty(  7, "Dirty 3rd second", 0.285,
     feedback = [0.573, 1.228, 0.412],
     eq = [10000, 80],
     wow = [0.141, 0.040],
     dry = [0, -0.005],
     wet = [-8, -0.337])

dirty(  8, "Clean 3rd second", 0.285,
     feedback = [0.603, 1.040, 1.000],
     eq = [20000, 20],
     wow = [0.000, 0.000],
     dry = [0, -0.005],
     wet = [-8, -0.337])

