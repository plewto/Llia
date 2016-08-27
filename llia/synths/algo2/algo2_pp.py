# llia.synths.algo2.algo2_pp

from __future__ import print_function
from llia.util.lmath import amp_to_db

def pp_algo2(program, slot):
    pad = ' '*6
    pad2 = ' '*10
    acc = ''
    def db(key):
        amp = program[key]
        return int(amp_to_db(amp))

    def fval(key):
        return float(program[key])

    def ival(key):
        return int(program[key])
    
    def carrier(op):
        prefix = 'op%s_' % op
        bcc = '%sop%d = {\n' % (pad, op)
        bcc += '%s"ratio"  : %6.4f,\n' % (pad2, fval(prefix+'ratio'))
        bcc += '%s"amp"    : %d,\n' % (pad2, db(prefix+'amp'))
        bcc += '%s"enable" : %d,\n' % (pad2, ival(prefix+'enable'))
        bcc += '%s"x"      : %5.3f,\n' % (pad2, fval(prefix+'x_amp'))
        bcc += '%s"lfo"    : %5.3f,\n' % (pad2, fval(prefix+'lfo_amp'))
        bcc += '%s"break-key"   : %d,\n' % (pad2, ival(prefix+'break_key'))
        bcc += '%s"left-scale"  : %d,\n' % (pad2, db(prefix+'left_scale'))
        bcc += '%s"right-scale" : %d,\n' % (pad2, db(prefix+'right_scale'))
        bcc += '%s"env"         : %d},\n' % (pad2, ival(prefix+'env_select'))
        return bcc

    def modulator(op):
        prefix = 'op%s_' % op
        bcc = '%sop%d = {\n' % (pad, op)
        bcc += '%s"ratio"  : %6.4f,\n' % (pad2, fval(prefix+'ratio'))
        bcc += '%s"bias"   : %d,\n' % (pad2, fval(prefix+'bias'))
        bcc += '%s"amp"    : %d,\n' % (pad2, fval(prefix+'amp'))
        bcc += '%s"enable" : %d,\n' % (pad2, ival(prefix+'enable'))
        bcc += '%s"x"      : %5.3f,\n' % (pad2, fval(prefix+'x_amp'))
        bcc += '%s"lfo"    : %5.3f,\n' % (pad2, fval(prefix+'lfo_amp'))
        bcc += '%s"break-key"   : %d,\n' % (pad2, ival(prefix+'break_key'))
        bcc += '%s"left-scale"  : %d,\n' % (pad2, db(prefix+'left_scale'))
        bcc += '%s"right-scale" : %d,\n' % (pad2, db(prefix+'right_scale'))
        bcc += '%s"env"         : %d' % (pad2, ival(prefix+'env_select'))
        if op in (2,3,5):
            bcc += '},\n'
        else:
            bcc += ',\n'
            bcc += '%s"feedback"      : %5.3f,\n' % (pad2, fval(prefix+'feedback'))
            bcc += '%s"env->feedback" : %5.3f,\n' % (pad2, fval(prefix+'env_feedback'))
            bcc += '%s"lfo->feedback" : %5.3f,\n' % (pad2, fval(prefix+'lfo_feedback'))
            bcc += '%s"x->feedback"   : %5.3f' % (pad2, fval(prefix+'x_feedback'))
            if op == 8:
                bcc += '})\n'
            else:
                bcc += '},\n'
        return bcc
    
    frmt = 'algo2(%d, "%s", amp=%d, port=%5.3f,\n'
    values = (slot, program.name, db("amp"), fval("port"))
    acc += frmt % values
    acc += '%sexternal = {\n' % (pad,)
    acc += '%s"pitch" : %5.3f,\n' % (pad2, fval('x_pitch'))
    acc += '%s"scale" : %5.3f,\n' % (pad2, fval('x_scale'))
    acc += '%s"bias"  : %5.3f},\n' % (pad2, fval('x_bias'))

    acc += '%slfo = {\n' % (pad,)
    acc += '%s"freq"   : %5.3f,\n' % (pad2, fval("lfo_freq"))
    acc += '%s"ratio"  : %5.3f,\n' % (pad2, fval("lfo_ratio"))
    acc += '%s"mix"    : %5.3f,\n' % (pad2, fval("lfo_mix"))
    acc += '%s"delay"  : %5.3f,\n' % (pad2, fval("lfo_delay"))
    acc += '%s"depth"  : %5.3f,\n' % (pad2, fval("lfo_depth"))
    acc += '%s"vsens"  : %5.3f,\n' % (pad2, fval("vsens"))
    acc += '%s"vdepth" : %5.3f},\n' % (pad2, fval("vdepth"))

    acc += '%senva = {\n' % (pad,)
    acc += '%s"attack"     : %5.3f,\n'  % (pad2, fval("enva_attack"))
    acc += '%s"decay1"     : %5.3f,\n'  % (pad2, fval("enva_decay1"))
    acc += '%s"decay2"     : %5.3f,\n'  % (pad2, fval("enva_decay2"))
    acc += '%s"release"    : %5.3f,\n'  % (pad2, fval("enva_release"))
    acc += '%s"breakpoint" : %5.3f,\n'  % (pad2, fval("enva_breakpoint"))
    acc += '%s"sustain"    : %5.3f},\n'  % (pad2, fval("enva_sustain"))
    
    acc += '%senvb = {\n' % (pad,)
    acc += '%s"attack"     : %5.3f,\n'  % (pad2, fval("envb_attack"))
    acc += '%s"decay1"     : %5.3f,\n'  % (pad2, fval("envb_decay1"))
    acc += '%s"decay2"     : %5.3f,\n'  % (pad2, fval("envb_decay2"))
    acc += '%s"release"    : %5.3f,\n'  % (pad2, fval("envb_release"))
    acc += '%s"breakpoint" : %5.3f,\n'  % (pad2, fval("envb_breakpoint"))
    acc += '%s"sustain"    : %5.3f},\n'  % (pad2, fval("envb_sustain"))

    acc += '%senvc = {\n' % (pad,)
    acc += '%s"attack"     : %5.3f,\n'  % (pad2, fval("envc_attack"))
    acc += '%s"decay1"     : %5.3f,\n'  % (pad2, fval("envc_decay1"))
    acc += '%s"decay2"     : %5.3f,\n'  % (pad2, fval("envc_decay2"))
    acc += '%s"release"    : %5.3f,\n'  % (pad2, fval("envc_release"))
    acc += '%s"breakpoint" : %5.3f,\n'  % (pad2, fval("envc_breakpoint"))
    acc += '%s"sustain"    : %5.3f},\n'  % (pad2, fval("envc_sustain"))

    acc += '%senvd = {\n' % (pad,)
    acc += '%s"attack"     : %5.3f,\n'  % (pad2, fval("envd_attack"))
    acc += '%s"decay1"     : %5.3f,\n'  % (pad2, fval("envd_decay1"))
    acc += '%s"decay2"     : %5.3f,\n'  % (pad2, fval("envd_decay2"))
    acc += '%s"release"    : %5.3f,\n'  % (pad2, fval("envd_release"))
    acc += '%s"breakpoint" : %5.3f,\n'  % (pad2, fval("envd_breakpoint"))
    acc += '%s"sustain"    : %5.3f},\n'  % (pad2, fval("envd_sustain"))

    acc += carrier(1)
    acc += carrier(4)
    acc += carrier(7)
    acc += modulator(3)
    acc += modulator(2)
    acc += modulator(5)
    acc += modulator(6)
    acc += modulator(8)
    return acc
    
    
