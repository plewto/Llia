# llia.synths.saw3.s3_pp
# 2016.06.06

from __future__ import print_function

import llia.util.lmath as math
from llia.performance_edit import performance_pp

def amp_to_db(amp):
    return int(math.amp_to_db(amp))

def pp_saw3(program, slot=127):

    def db(key):
        return int(amp_to_db(program[key]))
    
    def fval(key):
        return float(program[key])

    def ival(key):
        return int(program[key])
    
    pad = ' '*5
    acc = 'saw3(%3d, "%s", %-d,\n' % (slot, program.name, db('amp'))

    frmt = '%svibrato(%5.3f, delay=%5.3f, depth=%5.3f, sens=%5.3f),\n'
    s = frmt % (pad, fval('vfreq'), fval('vdelay'), fval('vdepth'), fval('vsens'))
    acc += s

    frmt = '%slfo(%5.3f, delay=%5.3f, depth=%5.3f),\n'
    s = frmt % (pad, fval('lfoFreq'), fval('lfoDelay'), fval('lfoDepth'))
    acc += s

    frmt = '%sadsr1(%5.3f,%5.3f,%5.3f,%5.3f),\n'
    s = frmt % (pad, fval('env1Attack'),fval('env1Decay'),
                fval('env1Sustain'),fval('env1Release'))
    acc += s

    frmt = '%sadsr2(%5.3f,%5.3f,%5.3f,%5.3f),\n'
    s = frmt % (pad, fval('env2Attack'),fval('env2Decay'),
                fval('env2Sustain'),fval('env2Release'))
    acc += s

    frmt = '%sosc1(%5.3f, wave=%5.3f, env1=%5.3f, lfo=%5.3f),\n'
    s = frmt % (pad, fval('osc1Freq'), fval('osc1Wave'),
                fval('osc1Wave_env1'), fval('osc1Wave_lfo'))
    acc += s

    frmt = '%sosc2(%5.3f, wave=%5.3f, env1=%5.3f, lfo=%5.3f),\n'
    s = frmt % (pad, fval('osc2Freq'), fval('osc2Wave'),
                fval('osc2Wave_env1'), fval('osc2Wave_lfo'))
    acc += s

    frmt = '%sosc3(%5.3f, wave=%5.3f, env1=%5.3f, lfo=%5.3f, lag=%5.3f, bias=%f),\n'
    s = frmt % (pad, fval('osc3Freq'), fval('osc3Wave'),
                fval('osc3Wave_env1'), fval('osc3Wave_lfo'),
                fval('osc3WaveLag'), fval('osc3Bias'))
    acc += s

    frmt = '%snoise(%5.3f, bw=%5.3f),\n'
    s = frmt % (pad, fval('noiseFreq'), fval('noiseBW'))
    acc += s

    frmt = '%sfilter_(%d, keytrack=%d, env1=%d, lfo=%d, bpoffset=%5.3f, bplag=%5.3f),\n'
    s = frmt % (pad, ival('filterFreq'), ival('filterKeytrack'),
                ival('filterFreq_env1'), ival('filterFreq_lfo'),
                fval('bandpassOffset'), fval('bandpassLag'))
    acc += s
    
    frmt = '%sres(%5.3f, env1=%5.3f, lfo=%5.3f),\n'
    s = frmt % (pad, fval('filterRes'), fval('filterRes_lfo'),
                fval('filterRes_env1'))
    acc += s

    frmt = '%sfilter_mix(%5.3f, env1=%5.3f, lfo=%5.3f),\n'
    s = frmt % (pad, fval('filterMix'),fval('filterMix_env1'),
                fval('filterMix_lfo'))
    acc += s
    acc += '%sport = %5.3f)\n' % (pad, fval('port'))
    return acc


