# llia.synths.orgn.orgn_pp

from __future__ import print_function

import llia.util.lmath as math
from llia.performance_edit import performance_pp


def amp_to_db(amp):
    return int(math.amp_to_db(amp))

def pp_rdrum(program, slot=127):

    def db (key):
        amp = program[key]
        rs = int(amp_to_db(program[key]))
        #print("DEBUG key '%s'  amp = %s   db = %s" % (key, amp, rs))
        return rs
    
    def fval(key):
        return float(program[key])
    
    pad = ' '*5
    pad2 = pad + ' '* 3
    acc = 'rdrum(%3d, "%s", amp=%d,\n' % (slot, program.name, db('amp'))

    acc += '%sa = {"ratio"  : %6.4f,\n' % (pad2, fval("aRatio"))
    acc += '%s     "attack" : %5.3f,\n' % (pad2, fval("aAttack"))
    acc += '%s     "decay"  : %5.3f,\n' % (pad2, fval("aDecay"))
    acc += '%s     "bend"   : %-6.3f,\n' % (pad2, fval("aBend"))
    acc += '%s     "tone"   : %5.3f,\n' % (pad2, fval("aTone"))
    acc += '%s     "velocity" : %5.3f,\n' % (pad2, fval("aVelocity"))
    acc += '%s     "amp"    : %d},\n' % (pad2, db("aAmp"))
    
    acc += '%sb = {"ratio"  : %6.4f,\n' % (pad2, fval("bRatio"))
    acc += '%s     "attack" : %5.3f,\n' % (pad2, fval("bAttack"))
    acc += '%s     "decay"  : %5.3f,\n' % (pad2, fval("bDecay"))
    acc += '%s     "bend"   : %-6.3f,\n' % (pad2, fval("bBend"))
    acc += '%s     "tune"   : %6.4f,\n' % (pad2, fval("bTune"))
    acc += '%s     "velocity" : %5.3f,\n' % (pad2, fval("bVelocity"))
    acc += '%s     "amp"    : %d},\n' % (pad2, db("bAmp"))

    acc += '%snoise = {"ratio"  : %6.4f,\n' % (pad2, fval("noiseRatio"))
    acc += '%s         "attack" : %5.3f,\n' % (pad2, fval("noiseAttack"))
    acc += '%s         "decay"  : %5.3f,\n' % (pad2, fval("noiseDecay"))
    acc += '%s         "bend"   : %-6.3f,\n' % (pad2, fval("noiseBend"))
    acc += '%s         "res"    : %6.4f,\n' % (pad2, fval("noiseRes"))
    acc += '%s         "velocity" : %5.3f,\n' % (pad2, fval("noiseVelocity"))
    acc += '%s         "amp"    : %d})\n' % (pad2, db("noiseAmp"))
    return acc
    
