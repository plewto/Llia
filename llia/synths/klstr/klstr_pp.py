# llia.synths.klstr.klstr_pp

from __future__ import print_function

import llia.util.lmath as math
from llia.performance_edit import performance_pp

def amp_to_db(amp):
    return int(math.amp_to_db(amp))

def pp_klstr(program, slot=127):
    def db (key):
        return int(amp_to_db(program[key]))
    def fval(key):
        return float(program[key])
    def ival(key):
        return int(program[key])
    pad = ' '*7
    pad2 = pad + ' '*7
    pad3 = pad + ' '*10
    pad4 = pad + ' '*11
    pad5 = pad4
    pad6 = pad4 + ' '
    acc = 'klstr(%d, "%s", amp=%+d,\n' % (slot, program.name, db('amp'))
    acc += '%slfo = {"freq"    : %6.4f,\n' % (pad, fval("lfoFreq"))
    acc += '%s"ratio"   : %6.4f,\n' % (pad2, fval("lfo2FreqRatio"))
    acc += '%s"xmod"    : %6.4f,\n' % (pad2, fval("lfoXMod"))
    acc += '%s"delay"   : %5.3f,\n' % (pad2, fval("lfoDelay"))
    acc += '%s"depth"   : %5.3f,\n' % (pad2, fval("lfoDepth"))
    acc += '%s"vibrato" : %5.3f},\n' % (pad2, fval("vibrato"))
    frmt = '%senv = {"gated"    : %s,\n'
    gatted = fval("envMode") == 0
    acc += frmt % (pad, gatted)
    acc += '%s"attack"  : %5.3f,\n' % (pad2, fval("attack"))
    acc += '%s"decay"   : %5.3f,\n' % (pad2, fval("decay"))
    acc += '%s"sustain" : %5.3f,\n' % (pad2, fval("sustain"))
    acc += '%s"release" : %5.3f},\n' % (pad2,  fval("release"))
    acc += '%sspread = {"depth" : %5.3f,\n' % (pad, fval("spread"))
    acc += '%s"lfo"   : %5.3f,\n' % (pad3, fval("spreadLfo"))
    acc += '%s"env"   : %5.3f},\n' % (pad3, fval("spreadEnv"))

    acc += '%scluster = {"depth" : %5.3f,\n' % (pad, fval("cluster"))
    acc += '%s"lfo"   : %5.3f,\n' % (pad4, fval("clusterLfo"))
    acc += '%s"env"   : %5.3f,\n' % (pad4, fval("clusterEnv"))
    acc += '%s"lag"   : %5.3f},\n' % (pad4, fval("clusterLag"))

    acc += '%sfilter_ = {"freq" : %5d,\n' % (pad, ival("filterFreq"))
    acc += '%s"lfo"  : %5d,\n' % (pad5, ival("filterLfo"))
    acc += '%s"env"  : %5d,\n' % (pad5, ival("filterEnv"))
    acc += '%s"lag"  : %5.3f,\n' % (pad5, fval("filterLag"))
    acc += '%s"res"  : %5.3f,\n' % (pad5, fval("res"))
    acc += '%s"mix"  : %5.3f},\n' % (pad5, fval("filterMix"))

    acc += '%sexternal = {"spread" : %5.3f,\n' % (pad, fval("xToSpread"))
    acc += '%s"noise"  : %5.3f,\n' % (pad6, fval('xToNoise'))
    acc += '%s"filter" : %5.3f,\n' % (pad6, fval('xToFilter'))
    acc += '%s"scale"  : %5.3f,\n' % (pad6, fval('xScale'))
    acc += '%s"bias    : %5.3f},\n' % (pad6, fval('xBias'))
    
    acc += '%spw = %5.3f,\n' % (pad, fval("pw"))
    acc += '%spwLfo = %5.3f,\n' % (pad, fval("pwLfo"))
    acc += '%snoise = %+d)\n' % (pad, db("noiseAmp"))
    return acc
