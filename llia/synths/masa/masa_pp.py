# llia.synths.masa.masa_pp

from __future__ import print_function

import llia.util.lmath as math

def amp_to_db(amp):
    return int(math.amp_to_db(amp))

def pp_masa(program, slot=127):
    pad = ' '*5
    pad2 = pad + ' '*8
    pad3 = pad + ' '*11
    acc = 'masa(%d, "%s", amp=%d,\n' % (slot, program.name, amp_to_db(program["amp"]))
    acc += '%sxbus = {"bias"  : %5.3f,\n' % (pad, float(program["xBias"]))
    acc += '%s"scale" : %5.3f,\n' % (pad2, float(program["xScale"]))
    acc += '%s"freq"  : %5.3f},\n' % (pad2, float(program["xToFreq"]))

    acc += '%svibrato = {"freq"  : %5.3f,\n' % (pad, float(program["vfreq"]))
    acc += '%s"delay" : %5.3f,\n' % (pad3, float(program["vdelay"]))
    acc += '%s"sens"  : %5.3f,\n' % (pad3, float(program["vsens"]))
    acc += '%s"depth" : %5.3f},\n' % (pad3, float(program["vdepth"]))

    acc += '%senv = [%5.3f, %5.3f],\n' % (pad,
                                          float(program["attack"]),
                                          float(program["decay"]))
    bcc = "%samps  = [" % pad
    xcc = "%sxtrem = [" % pad
    pcc = "%sperc  = [" % pad
    for i in range(9):
        j = i+1
        bcc += "%3.2f" % float(program["a%d" % j])
        xcc += "%3.2f" % float(program["x%d" % j])
        pcc += "%3.2f" % float(program["p%d" % j])
        if j == 9:
            bcc += "],\n"
            xcc += "],\n"
            pcc += "])\n"
        else:
            bcc += ","
            xcc += ","
            pcc += ","
    acc += bcc
    acc += xcc
    acc += pcc
    return acc
