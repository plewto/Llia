# llia.synths.slug.slug_pp


def lfo(fval):
    pad, pad2 = ' '*5, ' '*15
    bcc = '%slfo = lfo(freq=%s, delay=%s,\n' % (pad,
                                                fval("vfreq"),
                                                fval("vdelay"))
    bcc += '%svsens=%s, depth=%s, noise=%s, x=%s),\n' % (pad2,
                                                         fval("vsens"),
                                                         fval("vdepth"),
                                                         fval("vnoise"),
                                                         fval("xpitch"))
    return bcc
                                                          
def adsr(program,n):
    pad, pad2 = ' '*5, ' '*17
    def fval(key):
        param = "env%d_%s" % (n,key)
        f = float(program[param])
        return "%5.3f" % f
    bcc = '%senv%d = adsr(%d, ' % (pad,n,n)
    bcc += 'a=%s, d=%s, s=%s, r=%s,\n' % (fval("attack"),fval("decay"),
                                          fval("sustain"),fval("release"))
    bcc += '%svelocity=%s, key_scale=%s),\n' % (pad2,
                                                fval("velocity_attack"),
                                                fval("key_attack"))
    return bcc
    
def pulse(fval,ival):
    pad, pad2 = ' '*5, ' '*19
    bcc = '%spulse = pulse(amp=%s, tune=%s,\n' % (pad,
                                                  fval("pulse_amp"),
                                                  fval("pulse_ratio"))
    bcc += '%swidth=%s, width_env1=%s, width_lfo=%s,\n' % (pad2,
                                                           fval("pulse_width"),
                                                           fval("pulse_width_env1"),
                                                           fval("pulse_width_lfo"))
    bcc += '%senv=%s, pan=%s ),\n' % (pad2, fval("pulse_amp"),fval("pulse_pan"))
    return bcc

def pulse_filter(fval,ival):
    pad,pad2 = ' '*5, ' '*33
    bcc = '%spulse_filter = pulse_filter(res=%s, cutoff=%s,\n' % (pad,
                                                                  fval("pulse_filter_res"),
                                                                  ival("pulse_filter_cutoff"))
    bcc += '%senv1=%s, penv1=%s, lfo=%s, x=%s,\n' % (pad2,
                                                    ival("pulse_filter_env1"),
                                                    ival("pulse_filter_penv1"),
                                                    ival("pulse_filter_lfo"),
                                                    ival("pulse_filter_x"))
    frmt= '%svelocity=%s, left_track=%s, right_track=%s),\n'
    bcc += frmt % (pad2,
                   ival("pulse_filter_velocity"),
                   ival("pulse_filter_left_track"),
                   ival("pulse_filter_right_track"))
    return bcc


def pluck(fval, ival):
    pad, pad2 = ' '*5, ' '*19
    frmt = '%spluck = pluck(amp=%s, tune=%s, decay=%s,\n'
    bcc = frmt % (pad,
                  fval("pluck_amp"),
                  fval("pluck_ratio"),
                  fval("pluck_decay"))
    frmt = '%sharmonic=%s, width=%s, damp=%s, noise=%s,\n'
    bcc += frmt % (pad2,
                   ival("pluck_harmonic"),
                   ival("pluck_width"),
                   fval("pluck_damp"),
                   fval("pluck_excite"))
    frmt = '%svelocity=%s, left_scale=%s, right_scale=%s, pan=%s),\n'
    bcc += frmt % (pad2,
                   fval("pluck_velocity"),
                   ival("pluck_left_scale"),
                   ival("pluck_right_scale"),
                   fval("pluck_pan"))
    return bcc
                   
def carrier(n, program):
    pad, pad2 = ' '*5, ' '*12
    def fval(key):
        param = "car%d_%s" % (n, key)
        f = float(program[param])
        return "%5.3f" % f
    def ival(key):
        param = "car%d_%s" % (n, key)
        i = int(program[param])
        return "%d" % i
    frmt = '%scar%d = carrier(%d, amp=%s, tune=%s, bias=%s,\n'
    bcc = frmt % (pad, n,n,
                  fval("amp"),
                  fval("ratio"),
                  fval("bias"))
    frmt = '%svelocity=%s, left_scale=%s, right_scale=%s, env=%s,\n'
    bcc += frmt % (pad2,
                   fval("velocity"),
                   ival("left_scale"),
                   ival("right_scale"),
                   fval("amp_env"))
    frmt = '%smod_scale=%s, xmod=%s, fm=%s, pluck=%s, pan=%s),\n'
    bcc += frmt % (pad2,
                   ival("mod_scale"),
                   fval("xmod_depth"),
                   fval("mod_depth"),
                   fval("mod_pluck"),
                   fval("pan"))
    return bcc
                   
def modulator(n, program):
    pad, pad2 = ' '*5, ' ' *12
    def fval(key):
        param = "mod%d_%s" % (n, key)
        f = float(program[param])
        return "%5.3f" % f
    def ival(key):
        param = "mod%d_%s" % (n, key)
        i = int(program[param])
        return "%d" % i
    frmt = '%smod%d = modulator(%d, tune=%s, pluck=%s,\n'
    bcc = frmt % (pad,n,n,
                  fval("ratio"),
                  fval("mod_pluck"))
    frmt = '%svelocity=%s, left_scale=%s, right_scale=%s, env=%s)'
    bcc += frmt % (pad2,
                   fval("velocity"),
                   ival("left_scale"),
                   ival("right_scale"),
                   fval("env"))
    if n == 1:
        bcc += ',\n'
    else:
        bcc += ')\n'
    return bcc

def slug_pp(program,slot):
    def fval(key,frmt="%5.3f"):
        f = float(program[key])
        return frmt % f
    def ival(key,frmt="%d"):
        n = int(program[key])
        return frmt % n
    pad = ' '*5 
    acc = 'slug(%d,"%s",amp=%s,\n' % (slot,program.name,fval("amp"))
    acc += '%sbreak_key=%s, env_mode=%s,\n' % (pad,
                                               ival("break_key"),
                                               ival("env_mode"))
    acc += '%sport=%s, port_velocity=%s,\n' % (pad,
                                               fval("port"),
                                               fval("velocity_port"))
    acc += lfo(fval)+adsr(program,1)+adsr(program,2)
    acc += '%spdecay1 = %s,\n' % (pad,fval("penv1_decay"))
    acc += '%spdecay2 = %s,\n' % (pad,fval("penv2_decay"))
    acc += pulse(fval,ival) + pulse_filter(fval,ival)+pluck(fval,ival)
    acc += carrier(1,program) + carrier(2, program)
    acc += modulator(1,program) + modulator(2, program)
    return acc

