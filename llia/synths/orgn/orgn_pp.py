# llia.synths.orgn.orgn_pp
# 2016.04.01

from __future__ import print_function

import llia.util.lmath as math
# from llia.synths.orgn.orgn_data import inv_b_detune, inv_b_mod_ratio


def amp_to_db(amp):
    return int(math.amp_to_db(amp))

def pp_orgn(program, slot=127):
    db = int(amp_to_db(program["amp"]))
    pad = ' '*10
    acc = 'orgn(%3d, "%s",\n' % (slot, program.name)
    acc += '%samp=%+3d, pan=%+6.3f,\n' % (pad, db, program["pan"])
    acc += '%slfo=[%5.3f, %5.3f, %5.3f],\n' % (pad, program["lfoFreq"], 
                                               program["lfoDepth"], 
                                               program["lfoDelay"])
    acc += '%svib=[%5.3f, %5.3f],\n' % (pad, program["vibrato"], 
                                        program["vsens"])
    acc += '%schorus=[%5.3f, %5.3f],\n' % (pad, program["chorus"], 
                                           program["chorusDelay"])
    acc += '%sa=[%5.3f, %5.3f, %+3d],\n' % (pad, program["modDepthA"], 
                                            program["tremoloA"], 
                                            amp_to_db(program["mixA"]))
    acc += '%sb=[%5.3f, %5.3f, %+3d],\n' % (pad, program["modDepthB"], 
                                            program["tremoloB"], 
                                            amp_to_db(program["mixB"]))
    acc += '%sbfreq=[%d, %d],\n' % (pad, program["detuneB"],program["ratioB"])
    acc += '%sbenv=[%5.3f, %5.3f])\n' % (pad, program["decayB"], 
                                         program["sustainB"])
    return acc
