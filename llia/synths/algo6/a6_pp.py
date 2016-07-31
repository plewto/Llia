# llia.synths.algo6.a6_pp

from __future__ import print_function

import llia.util.lmath as math
from llia.performance_edit import performance_pp

def amp_to_db(amp):
    return int(math.amp_to_db(amp))


def pp_algo6(program, slot=127):

    def db(key):
        amp = program[key]
        v = int(amp_to_db(amp))
        return v

    def fval(key):
        return float(program[key])

    def ival(key):
        return int(program[key])

    pad = ' '*6
    padv = pad + ' '*11
    padc = pad + ' '*6
    
    def pp_modulator(n):
        mcc = ""
        frmt = '%sm%d = {"mute" : %s,\n'
        value = program["m%dEnable" % n] != 0
        data = (pad, n, value)
        mcc += frmt % data
        mcc += '%s"freq" : %6.4f,\n' % (padc, fval("m%d" % n))
        mcc += '%s"bias" : %d,\n' % (padc, ival("m%dBias" % n))
        mcc += '%s"a"    : %6.4f,\n' % (padc, fval("aToMod%d" % n))
        mcc += '%s"env"  : %5.3f,\n' % (padc, fval("envToMod%d" % n))
        mcc += '%s"lag"  : %5.3f,\n' % (padc, fval("envMod%dLag" % n))
        mcc += '%s"modDepth" : %5.3f,\n' % (padc, fval("modDepth%d" % n))
        if n == 3:
            mcc += '%s"feedback" : %5.3f,\n' % (padc, fval("fb3"))
            mcc += '%s"envToFeedback" :  %5.3f,\n' % (padc, fval("envToFb3"))
        mcc += '%s"lowScale"  : %d,\n' % (padc, ival("m%dLowKeyScale" % n))
        mcc += '%s"highScale" : %d},\n' % (padc, ival("m%dHighKeyScale" % n))
        return mcc
    
    def pp_carrier(n):
        ccc = ""
        frmt = '%sc%d = {"mute" : %s,\n'
        value = program["c%dEnable" % n] != 0
        data = (pad, n, value)
        ccc += frmt % data
        ccc += '%s"freq" : %6.4f,\n' % (padc, fval("c%d" % n))
        ccc += '%s"mix"  : %5.3f,\n' % (padc, amp_to_db(fval("c%dMix" % n)))
        ccc += '%s"lowScale"  : %d,\n' % (padc, ival("c%dLowKeyScale" % n))
        ccc += '%s"highScale" : %d},\n' % (padc, ival("c%dHighKeyScale" % n))
        return ccc

    def pp_env(n):
        bcc = "%senv%d = " % (pad, n)
        frmt = "[%5.3f, %5.3f, %5.3f, %5.3f]"
        data = (fval("attack%d" % n),
                fval("decay%d" % n),
                fval("sustain%d" % n),
                fval("release%d" % n))
        bcc += frmt % data
        if n == 3:
            bcc += ")\n"
        else:
            bcc += ",\n"
        return bcc
    acc = 'algo6(%3d, "%s", amp=%d,\n' % (slot, program.name,db("amp"))
    acc += '%sport = %5.3f,\n' % (pad, program["port"])
    acc += '%saToFreq = %6.4f,\n' % (pad, program['aToFreq'])
    acc += '%sbrightness = %5.3f,\n' % (pad, program['brightness'])
    acc += '%svibrato = {' % pad
    acc += '"freq"  : %5.3f,\n' % (fval("vfreq"),)
    acc += '%s"delay" : %5.3f,\n' % (padv, fval('vdelay'))
    acc += '%s"sens"  : %5.3f,\n' % (padv, fval("vsens"))
    acc += '%s"depth" : %5.3f},\n' % (padv, fval("vdepth"))
    acc += pp_carrier(1)
    acc += pp_modulator(1)
    acc += pp_carrier(2)
    acc += pp_modulator(2)
    acc += pp_carrier(3)
    acc += pp_modulator(3)
    frmt = '%sbreak_keys = [%d, %d, %d],\n'
    data = (pad, ival("keyBreak1"), ival("keyBreak2"), ival("keyBreak3"))
    acc += frmt % data
    acc += pp_env(1)
    acc += pp_env(2)
    acc += pp_env(3)
    
    return acc
