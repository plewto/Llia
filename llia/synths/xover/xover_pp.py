# llia.synths.xover.xover_pp
#

from __future__ import print_function

import llia.util.lmath as math
from llia.performance_edit import performance_pp


def amp_to_db(amp):
    return int(math.amp_to_db(amp))

def pp_xover(program, slot=127):
    
    def db(key):
        return int(amp_to_db(program[key]))
    
    def fval(key):
        return float(program[key])

    def ival(key):
        return int(program[key])

    pad = ' '*5
    acc = ''
    acc = 'xover(%3d, "%s",\n' % (slot, program.name)
    acc += '%slfoFreq = %5.4f\n' % (pad, fval('lfoFreq'))

    frmt = '%scrossover = %4d, lfoCrossover = %5.3f,\n'
    acc += frmt % (pad, ival('crossover'), fval('lfoCrossover'))

    frmt = '%slfoCrossoverRatio = %5.3f, res = %5.3f\n'
    acc += frmt % (pad, fval('lfoCrossoverRatio'), fval('res'))

    frmt = '%slpMode = %5.3f, lpMod = %5.3f, lpAmp = %2d\n'
    acc += frmt % (pad, fval('lpMode'), fval('lpMod'), db('lpAmp'))

    frmt = '%shpMode = %5.3f, hpMod = %5.3f, hpAmp = %2d\n'
    acc += frmt % (pad, fval('hpMode'), fval('hpMod'), db('hpAmp'))

    frmt = '%sspread = %5.3f, lfoPanMod = %5.3f, lfoPanRation = %5.3f,\n'
    acc += frmt % (pad, fval('spread'), fval('lfoPanMode'), fval('lfoPanRatio'))

    frmt = '%sdryAmp = %d, dryPan = %5.3f,\n'
    acc += frmt % (pad, db('dryAmp'), fval('dryPan'))

    frmt = '%samp = %d)\n'
    acc += % (pad, db('amp'))
    return acc

    

    
    
    

