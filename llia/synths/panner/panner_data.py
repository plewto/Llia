# llia.synths.panner.panner_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance
from llia.util.lmath import (clip, db_to_amp, amp_to_db,
                             random_sign, rnd, coin)


prototype = {
    "pos" : 0.0,
    "lfoFreq" : 1.0,
    "lfoDepth" : 0.0,
    "xscale" : 0.0,
    "xbias" : 0.0,
    "amp" : 1.0
}

class Panner(Program):

    def __init__(self, name):
        super(Panner, self).__init__(name, "Panner", prototype)
        self.performance = performance()

program_bank = ProgramBank(Panner("Init"))


def panner(slot, name,
           amp = 0,             # db
           pos = 0.0,           # pan position (-1..+1)
           lfoFreq = 1.0,       # Hertz
           lfoDepth = 0.0,      # (0..1)
           xscale = 0.0,        # external signal scale
           xbias = 0.0):
    p = Panner(name)
    p["amp"] = float(db_to_amp(amp))
    p["pos"] = float(clip(pos, -1, 1))
    p["lfoFreq"] = float(abs(lfoFreq))
    p["lfoDepth"] = float(clip(lfoDepth, -1, 1))
    p["xscale"] = float(xscale)
    p["xbias"] = float(xbias)
    program_bank[slot] = p
    return p

def pp(program, slot=127):
    pad = ' '*5
    acc = 'panner(%d, "%s",\n' % (slot, program.name)
    acc += '%samp = %d,\n' % (pad, int(amp_to_db(program['amp'])))
    acc += '%spos = %5.3f,\n' % (pad, float(program['pos']))
    acc += '%slfoFreq = %5.3f,\n' % (pad, float(program['lfoFreq']))
    acc += '%slfoDepth = %5.3f,\n' % (pad, float(program['lfoDepth']))
    acc += '%sxscale = %5.3f,\n' % (pad, float(program['xscale']))
    acc += '%sxbias = %5.3f)\n' % (pad, float(program['xbias']))
    return acc

def random_panner(slot=127, *_):
    static = coin(0.20)
    if static:
        pos = random_sign()
        p = panner(slot, "Random",
                   amp = 0,
                   pos = pos,
                   lfoDepth = 0,
                   xscale = 0)
    else:
        pos = coin(0.75, 0.0, random_sign())
        lfoFreq= coin(0.75, rnd(0.1), rnd(5))
        lfoDepth = rnd()
        p = panner(slot, "Random",
                   amp = 0,
                   pos = pos,
                   lfoFreq = lfoFreq,
                   lfoDepth = lfoDepth,
                   xscale = 0)
    return p
        

panner(0, "Center", pos=0)
panner(1, "Hard Left", pos=-1.0)
panner(2, "Soft Left", pos=-0.5)
panner(3, "Hard Right", pos=1.0)
panner(4, "Soft Right", pos=0.5)
panner(5, "Autopan 1", pos = 0.0, lfoFreq=1.0, lfoDepth=1.00)
panner(6, "Autopan 2", pos = 0.0, lfoFreq=1.0, lfoDepth=0.50)
panner(7, "Autopan 3", pos = 0.0, lfoFreq=5.0, lfoDepth=1.00)
panner(8, "Autopan 4", pos = 0.0, lfoFreq=5.0, lfoDepth=0.50)
