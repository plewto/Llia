# llia.synths.tremolo.tremolo_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.util.lmath import clip, db_to_amp, amp_to_db, coin, rnd, random_sign, pick
from llia.performance_edit import performance

prototype = {
    "lfoFreq" : 5.0,
    "modDepth" : 0.0,
    "limit" : 1.0,
    "xDepth" : 0.0,
    "xLfoAmp" : 0.0,
    "xLfoFreq" : 0.0,
    "amp" : 1.0} 

class Tremolo(Program):

    def __init__(self, name):
        super(Tremolo, self).__init__(name, "Tremolo", prototype)
        self.performance = performance()

program_bank = ProgramBank(Tremolo("Init"))
program_bank.enable_undo = False

def trem(slot, name, amp=0,
         lfo = [5.0,  0.0],         # [freq, amp]
         xtern = [0.0, 0.0, 0.0],   # [modDepth, x->lfoFreq, x->lfoAmp]
         limit = 1):
    p = Tremolo(name)
    p["lfoFreq"] = abs(float(lfo[0]))
    p["modDepth"] = clip(abs(float(lfo[1])), 0, 2)
    p["limit"] = abs(float(limit))
    p["amp"] = clip(abs(float(db_to_amp(amp))), 0, 2)
    p["xDepth"] = float(xtern[0])
    p["xLfoFreq"] = float(xtern[1])
    p["xLfoAmp"] = float(xtern[2])
    program_bank[slot] = p
    return p

def pp(program, slot=127):
    def fval(key):
        return float(program[key])
    pad = ' '*5
    frmt = 'trrm(%d, "%s", amp=%d,\n'
    data = (slot, program.name, int(amp_to_db(program['amp'])))
    acc = frmt % data
    frmt = '%slfo = [%5.3f, %5.3f],\n'
    data = (pad, fval('lfoFreq'), fval('modDepth'))
    acc += frmt % data
    frmt = '%sxtern = [%5.3f, %5.3f, %5.3f],\n'
    data = (pad, fval('xDepth'), fval('xLfoFreq'), fval('xLfoAmp'))
    acc += frmt % data
    frmt = '%slimit = %5.3f)\n'
    data = (pad, fval('limit'))
    acc += frmt % data
    return acc

def random_tremolo(slot=127, *_):
    freq = 0.01 + rnd(10)
    dpth = rnd()
    with_external = coin(0.25)
    if with_external:
        xdepth = coin(0.5, 0, rnd())
        fm = coin(0.5, 0, rnd())
        am = coin(0.5, 0, rnd())
        p = trem(slot, "Random", amp=0,
                 lfo = [freq, dpth],
                 xtern = [xdepth, fm, am],
                 limit = 1)
    else:
        p = trem(slot, "Random", amp=0,
                 lfo = [freq, dpth],
                 xtern = [0.0, 0.0, 0.0],
                 limit = 1)
    return p

trem(0, "Bypass",  amp=0,
     lfo = [5.0, 0.0],
     xtern = [0.0, 0.0, 0.0],
     limit = 1)

trem(1, "Five", amp=0,
     lfo = [5.0, 0.75],
     xtern = [0.0, 0.0, 0.0],
     limit = 1)

trem(2, "Slow & Deep", amp=0,
     lfo = [1.0, 1.0],
     xtern = [0.0, 0.0, 0.0],
     limit = 1)

trem(3, "External Only", amp=0,
     lfo = [1.0, 0.0],
     xtern = [1.0, 0.0, 0.0],
     limit = 1)

trem(4, "External LFO Mod", amp=0,
     lfo = [7.0, 1.0],
     xtern = [0.0, 0.0, 1.0],
     limit = 1)

trem(5, "External LFO FM", amp=0,
     lfo = [5.0, 1.0],
     xtern = [0.0, 2.0, 0.0],
     limit = 1)
     
     
