# llia.synths.dirtyburger.dirty_p
# 2016.06.09

from __future__ import print_function

import llia.util.lmath as math
from llia.performance_edit import performance_pp

def amp_to_db(amp):
    return int(math.amp_to_db(amp))


def pp_dirty(program, slot=127):

    def db(key):
        return int(amp_to_db(program[key]))

    def fval(key):
        return float(program[key])

    def ival(key):
        return int(program[key])

    pad = ' '*5
    acc = ''
    frmt = 'dirty(%3d, "%s", %5.3f,\n'
    acc += frmt % (slot, program.name, fval('delayTime'))

    fb, gain, clip = fval('feedback'), fval('gain'), fval('threshold')
    frmt = '%sfeedback = [%5.3f, %5.3f, %5.3f],\n' % (pad, fb, gain, clip)
    acc += frmt

    lo,hi = ival('lowcut'), ival('highcut')
    frmt = '%seq = [%d, %d],\n' % (pad, lo, hi)
    acc += frmt

    wow, flutter = fval('wow'), fval('flutter')
    frmt = '%swow = [%5.3f, %5.3f],\n' % (pad, wow, flutter)
    acc += frmt
    
    amp, pan = db('dryAmp'), fval('dryPan')
    frmt = '%sdry = [%d, %5.3f],\n' % (pad, amp, pan)
    acc += frmt

    amp, pan = db('wetAmp'), fval('wetPan')
    frmt = '%swet = [%d, %5.3f])\n' % (pad, amp, pan)
    acc += frmt
    return acc


