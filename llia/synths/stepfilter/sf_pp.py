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
    acc += '%sclockFreq = %5.4f,\n' % (pad, fval("clockFreq"))
    r = '%sr = [' % pad
    a = '%sa = [' % pad
    b = '%sb = [' % pad
    for i in range(8):
        j = i+ 1
        rk = 'r%d' % j
        ak = 'a%d' % j
        bk = 'b%d' % j
        r += '%5.3f, ' % fval(rk)
        a += '%5.3f, ' % fval(ak)
        b += '%5.3f, ' % fval(bk)
    acc += '%s],\n' % r[:-2]
    acc += '%s],\n' % a[:-2]
    acc += '%s],\n' % b[:-2]
    frmt = '%salag = %5.3f, arange = [%4d, %4d], ares = %5.3f,\n'
    acc += frmt % (pad, fval("aLag"), ival("aMin"), ival("aMax"), fval("aRes"))
    frmt = '%sblag = %5.3f, brange = [%4d, %4d], bres = %5.3f,\n'
    acc += frmt % (pad, fval("bLag"), ival("bMin"), ival("bMax"), fval("bRes"))
    acc += '%slfofreq = %5.3f,\n' % (pad, fval("panLfoFreq"))
    frmt = '%sapan = [%+5.3f, %5.3f],\n'
    acc += frmt % (pad, fval("aPan"), fval("panLfoA"))
    frmt = '%sbpan = [%+5.3f, %5.3f, %5.3f],\n'
    acc += frmt % (pad, fval("bPan"), fval("panLfoB"), fval("panLfoBRatio"))

    frmt = '%sdrypan = [%+5.3f, %5.3f],\n'
    acc += frmt % (pad, fval("dryPan"), fval("panLfoDry"))
    frmt = '%smix = [%5.3f, %5.3f, %5.3f],\n'
    acc += frmt % (pad, fval("dryAmp"), fval("aAmp"), fval("bAmp"))
    frmt = "%samp = %5.3f)\n"
    acc += frmt % (pad, fval("amp"))
    return acc
    
    
    
    
    
