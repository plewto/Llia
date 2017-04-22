# llia.synths.sol.sol_pp


def sol_pp(program,slot):
    def fval(key,n=5):
        v = program[key]
        #print("DEBUG [%s] -> %s" % (key,v))
        return round(float(v),n)
    def ival(key):
        return int(program[key])
    pad=' '*4
    acc = 'sol(%3d,"%s",amp=%5.3f,\n' % (slot,program.name,fval('amp'))
    frmt = '%sport=%5.3f,\n%stimebase=%6.4f,\n'
    acc += frmt % (pad,fval('port'),pad,fval('timebase'))
    frmt = '%svibrato = vibrato(ratio=%7.5f,sens=%5.3f,depth=%5.3f,\n'
    acc += frmt % (pad,fval('vratio'),fval('vsens'),fval('vdepth'))
    frmt = '%sdelay=%5.3f,extern=%5.3f),\n'
    acc += frmt % (pad+' '*18,fval('vdelay'),fval('pitch_ctrlbus'))
    # alfo, blfo, aenv, benv
    for k in 'ab':
        frmt='%s%slfo = lfo("%s",ratio=%7.5f,delay=%5.4f),\n'
        values = (pad,k,k,fval('%slfo_ratio' % k),fval('%slfo_delay' % k))
        acc += frmt % values

        frmt = '%s%senv = adsr("%s",a=%5.3f,d=%5.3f,s=%5.3f,r=%5.3f,lfo_trig=%d),\n'
        values = (pad,k,k,
                  fval('%senv_attack' % k),
                  fval('%senv_decay' % k),
                  fval('%senv_sustain' % k),
                  fval('%senv_release' % k),
                  ival('%senv_lfo_trig' % k))
        acc += frmt % values
    # cenv
    frmt = '%scenv=addsr(a=%5.3f,d1=%5.3f,d2=%5.3f,r=%5.3f,bp=%5.3f,sus=%5.3f,trig=%d),\n'
    values = (pad,fval('cenv_attack'),fval('cenv_decay1'),fval('cenv_decay2'),
              fval('cenv_release'),fval('cenv_breakpoint'),fval('cenv_sustain'),
              fval('cenv_trig_mode'))
    acc += frmt % values
    # OPS A & B
    pad2=pad+' '*11
    for k in 'ab':
        frmt='%sop%s = fmop("%s",' % (pad,k,k)
        acc += frmt
        frmt = 'mratio=%6.4f,mscale=%d,mdepth=%5.3f,lfo=%5.3f,env=%5.3f,\n'
        values = (fval('op%s_mod_ratio' % k),
                  ival('op%s_mod_scale' % k),
                  fval('op%s_mod_depth' % k),
                  fval('op%s_mod_%slfo' % (k,k)),
                  fval('op%s_mod_%senv' % (k,k)))
        acc += frmt % values
        frmt = '%scratio=%6.4f,cbias=%6.4f,\n'
        values = (pad2,
                  fval('op%s_car_ratio' % k),
                  fval('op%s_car_bias' % k))
        acc += frmt % values
        frmt = '%sfeedback=%6.4f,cross_feedback=%6.4f,amp=%5.3f),\n'
        values = (pad2,
                  fval('op%s_feedback' % k),
                  fval('op%s_cross_feedback' % k),
                  fval('op%s_amp' % k))
        acc += frmt % values
    # OPS C & D
    for k in 'cd':
        if k == 'c':
            mod = 'a'
        else:
            mod = 'b'
        frmt ='%sop%s = wvop("%s",' % (pad,k,k)
        acc += frmt
        frmt='sratio=%6.4f,pratio=%6.4f,pw=%5.3f,pwm=%5.3f,\n'
        values = (fval('op%s_saw_ratio' % k),
                  fval('op%s_pulse_ratio' % k),
                  fval('op%s_pulse_width' % k),
                  fval('op%s_pulse_width_%slfo' % (k,mod)))
        acc += frmt % values
        frmt='%swave=%5.3f,wave_lfo=%5.3f,wave_env=%5.3f,\n'
        values = (pad2,
                  fval('op%s_wave' % k),
                  fval('op%s_wave_%slfo' % (k,mod)),
                  fval('op%s_wave_%senv' % (k,mod)))
        acc += frmt % values
        frmt='%snoise_amp=%5.3f,filter_track=%d,filter_env=%d,amp=%5.3f),\n'
        values = (pad2,
                  fval('op%s_noise_amp' % k),
                  ival('op%s_filter_track' % k),
                  ival('op%s_filter_%senv' % (k,mod)),
                  fval("op%s_amp" % k))
        acc += frmt % values
    # Vectors X & Y
    pad2=pad+' '*11
    pad3=pad+' '*17
    for v in 'xy':
        if v == 'x':
            mod = 'a'
        else:
            mod = 'b'
        acc += '%s%s = vector("%s",' % (pad,v,v)
        frmt = 'pos=%5.3f,ratio=%7.5f,wave=%5.3f,delay=%5.3f,\n'
        values = (fval('%spos' % v),
                  fval('%slfo_ratio' % v),
                  fval('%slfo_wave' % v),
                  fval('%slfo_delay' % v))
        acc += frmt % values
        frmt = '%sadsr=[%5.3f,%5.3f,%5.3f,%5.3f],trig=%d,\n'
        values = (pad2,
                  fval('%senv_attack' % v),
                  fval('%senv_decay' % v),
                  fval('%senv_sustain' % v),
                  fval('%senv_release' % v),
                  ival('%senv_lfo_trig' % v))
        acc += frmt % values
        frmt = '%slfo_depth=%5.3f, env_depth=%5.3f,external=%5.3f),\n'
        values = (pad2,
                  fval('%spos_%slfo' % (v,v)),
                  fval('%spos_%senv' % (v,v)),
                  fval('%spos_v%sbus' % (v,v)))    
        acc += frmt % values

        # Filters
        acc += '%s%sfilter = filter("%s",' % (pad,v,v)
        frmt = 'freq=%d,track=%d,\n'
        values = (ival('%sfilter_freq' % v),
                  ival('%sfilter_track' % v))
        acc += frmt % values
        frmt = '%senv=%d,cenv=%d,lfo=%d,vlfo=%d,res=%5.3f,amp=%5.3f)'
        values = (pad3,
                  ival('%sfilter_freq_%senv' % (v,mod)),
                  ival('%sfilter_freq_cenv' % v),
                  ival('%sfilter_freq_%slfo' % (v,mod)),
                  ival('%sfilter_freq_vlfo' % v),
                  fval('%sfilter_res' % v),
                  fval('%samp' % v))
        acc += frmt % values                  
        if v == 'x':
            acc += ',\n'
        else:
            acc += ')\n'
    return acc

