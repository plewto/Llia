# llia.synths.orgn.orgn_pp
# 2016.06.04

from __future__ import print_function

import llia.util.lmath as math
from llia.performance_edit import performance_pp


def amp_to_db(amp):
    return int(math.amp_to_db(amp))

def pp_orgn(program, slot=127):
    def db (key):
        return int(amp_to_db(program[key]))
    def flt(key):
        return float(program[key])
    pad = ' '*5
    acc = ''
    acc = 'orgn(%3d, "%s", amp=%d,\n' % (slot, program.name, db('amp'))
    s = '%svfreq=%5.3f, vdelay=%5.3f, vsens=%5.3f, vdepth=%5.3f,\n'
    s = s % (pad,flt('vfreq'),flt('vdelay'),flt('vsens'),flt('vdepth'))
    acc += s
    s = '%schorus = [%5.3f, %5.3f],\n'
    s = s % (pad, flt("chorus"), flt("chorusDelay"))
    acc += s
    s = '%s%s = [%5.3f, %5.3f, %5.3f, %d],\n'
    d = (pad,'a',flt('c1'),flt('m1'),flt('mod1'),db("amp1"))
    acc += s % d
    d = (pad,'b',flt('c2'),flt('m2'),flt('mod2'),db("amp2"))
    acc += s % d
    d = (pad,'c',flt('c3'),flt('m3'),flt('mod3'),db("amp3"))
    acc += s % d
    s = '%sadsr = [%5.3f, %5.3f, %5.3f, %5.3f],\n'
    d = (pad,flt('attack3'),flt('decay3'),flt('sustain3'),flt('release3'))
    acc += s % d
    s = '%sbrightness = %5.3f)\n' % (pad, flt('brightness'))
    acc += s
    return acc
    
    
