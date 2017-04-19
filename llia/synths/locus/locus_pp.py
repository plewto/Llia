# llia.synths.locus.locus_pp


def locus_pp(program,slot):
    def fval(key):
        return float(program[key])
    def ival(key):
        return int(program[key])
    pad = ' '*6
    acc = 'locus(%d,"%s",amp=%s,\n' % (slot,program.name,fval("amp"))
    acc += '%sxamp=%5.3f,yamp=%5.3f,\n' % (pad,fval("xamp"),fval("yamp"))
    for e in '12':
        head = "env%s_" % e
        data = (fval(head+"attack"),
                fval(head+"decay1"),
                fval(head+"decay2"),
                fval(head+"release"),
                fval(head+"breakpoint"),
                fval(head+"sustain"))
        acc += '%senv%s=env%s(' % (pad,e,e)
        acc += 'a=%5.3f,d1=%5.3f,d2=%5.3f,r=%5.3f,bp=%5.3f,s=%5.3f),\n' % data
    frm='%svibrato=vibrato(freq=%5.3f,sens=%5.3f,depth=%5.3f,delay=%5.3f),\n'
    acc += frm % (pad,
                  fval("vfreq"),
                  fval("vsens"),
                  fval("vdepth"),
                  fval("vdelay"))
    for e in 'xy':
        pos = fval("%spos" % e)
        lfo = fval("%spos_lfo" % e)
        env = fval("%spos_env1" % e)
        ext = fval("%spos_%sbus" % (e,e))
        ratio = fval("lfo%s_ratio" % e)
        delay = fval("lfo%s_delay" % e)
        frm1='%s%svector=%svector(' % (pad,e,e)
        frm2='pos=%5.3f,lfo=%5.3f,env=%5.3f,external=%5.3f),\n' % (pos,lfo,env,ext)
        frm3='%s%slfo=%slfo(' % (pad,e,e)
        frm4='ratio=%5.3f,delay=%5.3f),\n' % (ratio,delay)
        acc += frm1+frm2
        acc += frm3+frm4
    for e in "ab":
        head="op%s_" % e
        mhead = head+"mod_"
        chead = head+"car_"
        mratio = fval(mhead+"ratio")
        mdepth = fval(mhead+"depth")
        mscale = fval(mhead+"scale")
        menv = fval(mhead+"env1")
        mlfo = fval(mhead+"lfo")
        frm1 = '%s%smod=%smod(' % (pad,e,e)
        frm2 = 'ratio=%6.4f,depth=%5.3f,scale=%5.3f,env1=%5.3f,lfo=%5.3f),\n'
        frm2 = frm2 % (mratio,mdepth,mscale,menv,mlfo)
        cratio = fval(chead+"ratio")
        cbias = ival(chead+"bias")
        feedback=fval("op%s_feedback" % e)
        frm3 = '%s%scar=%scar(' % (pad,e,e)
        frm4 = 'ratio=%6.4f,bias=%d,feedback=%5.3f),\n'
        frm4 = frm4 % (cratio,cbias,feedback)
        acc += frm1+frm2+frm3+frm4
    for e in "abcd":
        head="op%s_" % e
        lfo_ratio = fval(head+"lfo_ratio")
        lfo_wave = fval(head+"lfo_wave")
        plfo = fval(head+"pitch_lfo")
        penv = fval(head+"pitch_env1")
        delay = fval(head+"env_delay")
        amp = fval(head+"amp")
        frm1 = '%s%slfo=%slfo(' % (pad,e,e)
        frm2 = 'ratio=%6.4f,wave=%5.3f),\n' % (lfo_ratio,lfo_wave)
        frm3 = '%sop%s=op%s(' % (pad,e,e)
        frm4 = 'plfo=%6.4f,penv1=%6.4f,delay=%5.3f,amp=%5.3f),\n'
        frm4 = frm4 % (plfo,penv,delay,amp)
        acc += frm1+frm2+frm3+frm4
    for e in "cd":
        head="op%s_" % e
        wave = fval(head+"wave")
        lfo = fval(head+"wave_lfo")
        env = fval(head+"wave_env1")
        frm1 = '%s%swave=%swave(' % (pad,e,e)
        frm2 = 'wave=%5.3f,lfo=%5.3f,env1=%5.3f),\n' % (wave,lfo,env)
        acc += frm1+frm2
        sine = fval(head+"sine_ratio")
        pulse = fval(head+"pulse_ratio")
        saw = fval(head+"saw_ratio")
        frm3 = '%s%stune=%stune(sine=%6.4f,pulse=%6.4f,saw=%6.4f),\n'
        acc += frm3 % (pad,e,e,sine,pulse,saw)
        pw = fval(head+"pulse_width")
        pwm = fval(head+"pulse_width_lfo")
        frm4 = '%s%spulse=%spulse(width=%5.3f,lfo=%5.3f),\n'
        acc += frm4 % (pad,e,e,pw,pwm)
        lp = ival(head+"noise_lowpass")
        hp = ival(head+"noise_highpass")
        namp = fval(head+"noise_amp")
        frm5 = '%s%snoise=%snoise(lowpass=%d,highpass=%d,amp=%5.3f),\n'
        acc += frm5 % (pad,e,e,lp,hp,namp)
        ff = ival(head+"filter_freq")
        flfo = ival(head+"filter_freq_lfo")
        fenv = ival(head+"filter_freq_env1")
        fres = fval(head+"filter_res")
        frm6 = '%s%cfilter=%sfilter(' % (pad,e,e)
        frm7 = 'freq=%d,lfo=%d,env1=%d,res=%5.3f)' % (ff,flfo,fenv,fres)
        acc += frm6+frm7
        if e == 'c':
            acc += ',\n'
        else:
            acc += ')\n'
    return acc

