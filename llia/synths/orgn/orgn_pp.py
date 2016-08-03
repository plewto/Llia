# llia.synths.orgn.orgn_pp
# 2016.06.04

from __future__ import print_function

import llia.util.lmath as math
from llia.performance_edit import performance_pp


def amp_to_db(amp):
    return int(math.amp_to_db(amp))

def pp_orgn(program, slot):

    def db(key):
        return int(amp_to_db(program[key]))

    def fval(key):
        return float(program[key])

    pad = ' '*5
    pad2 = pad + ' '*4
    acc = 'orgn(%3d, "%s", amp=%d,\n' % (slot, program.name, db('amp'))
    frmt = '%scenv = [%5.3f,%5.3f,%5.3f,%5.3f],\n'
    data = (pad2,fval('cattack'),fval('cdecay'),fval('csustain'),fval('crelease'))
    acc += frmt % data
    frmt = '%smenv = [%5.3f,%5.3f,%5.3f,%5.3f],\n'
    data = (pad2,fval('mattack'),fval('mdecay'),fval('msustain'),fval('mrelease'))
    acc += frmt % data
    acc += '%sop1 = [%6.4f, %3d],\n' % (pad2, fval('r1'), db('amp1'))
    acc += '%sop2 = [%6.4f, %5.3f],\n' % (pad2, fval('r2'), fval('amp2'))
    acc += '%sop3 = [%6.4f, %3d],\n' % (pad2, fval('r3'), db('amp3'))
    acc += '%sop4 = [%6.4f, %5.3f],\n' % (pad2, fval('r4'), fval('amp3'))
    frmt = '%svibrato = [%5.3f,%5.3f,%5.3f,%6.4f],\n'
    data = (pad2,fval('vfreq'),fval('vdelay'),fval('vdepth'),fval('xToPitch'))
    acc += frmt % data
    
    frmt = '%schorus = [%5.3f, %5.3f],\n'
    data = (pad2,fval('chorusDelay'),fval('chorus'))
    acc += frmt % data

    frmt = '%smod_depth = [%5.3f, %5.3f])\n'
    data = (pad2,fval('modulationDepth'),fval('xToModulationDepth'))
    acc += frmt % data
    return acc
    
    
