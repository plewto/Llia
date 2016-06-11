# llia.synths.stepfilter.sf_pp
# 2016.06.11

from __future__ import print_function

import llia.util.lmath as math
from llia.performance_edit import performance_pp


def pp_stepfilter(program, slot=127):

    def fval(key):
        return float(program[key])

    def ival(key):
        return int(program[key])

    pad = ' '*7
    acc = 'sfilter(%3d, "%s",\n' % (slot, program.name)

    pcc = "%spulse = [" % pad
    for k in ("sub1", "sub2", "n1", "n2", "n3", "n4", "n5", "n6"):
        v = fval(k)
        pcc += "%5.3f, " % v
    pcc = pcc[:-2] + "],\n"
    acc += pcc

    acc += "%ssh = %5.3f, shclock = %5.3f,\n" % (pad, fval("sh"), fval("shFreq"))
    acc += "%sclock = %5.3f,\n" % (pad, fval("clkFreq"))
    acc += "%sfrange[%d, %d], \n" % (pad, ival("minFreq"), ival("maxFreq"))
    acc += "%srq = %5.3f,\n" % (pad, fval("rq"))
    acc += "%slag = %5.3f,\n" % (pad, fval("lag"))
    acc += "%swet = %+6.3f,\n" % (pad, fval("wet"))
    acc += "%span = %+6.3f)\n" % (pad, fval("pan"))
    return acc
    
    
    
