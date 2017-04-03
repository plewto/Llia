# llia.synths.klstr2.klstr2_pp


_pmap = {"lfoFreq":"freq",
         "lfo2Ratio":"ratio2",
         "vibrato":"vibrato",
         "env1_attack":"attack",
         "env1_decay1":"decay1",
         "env1_decay2":"decay2",
         "env1_release":"release",
         "env1_breakpoint":"breakpoint",
         "env1_sustain":"sustain",
         "env1_mode":"mode",
         "env2_attack":"attack",
         "env2_decay1":"decay1",
         "env2_decay2":"decay2",
         "env2_release":"release",
         "env2_breakpoint":"breakpoint",
         "env2_sustain":"sustain",
         "env2_mode":"mode",
         "spread":"n",
         "spread_env1":"env1",
         "spread_lfo1":"lfo1",
         "spread_external":"external",
         "cluster":"n",
         "cluster_env1":"env1",
         "cluster_lfo1":"lfo1",
         "cluster_lfo2":"lfo2",
         "cluster_external":"external",
         "pw":"pw",
         "pw_lfo1":"lfo1",
         "pw_env1":"env1",
         "harm1":"n",
         "harm1_env1":"env1",
         "harm1_env2":"env2",
         "harm1_lfo1":"lfo1",
         "harm1_lfo2":"lfo2",
         "harm2":"n",
         "harm2_env1":"env1",
         "harm2_lfo1":"lfo1",
         "harm2_external":"external",
         "harm2_lag":"lag",
         "noise_lowpass":"lowpass",
         "noise_lowpass_env1":"env1",
         "noise_lowpass_lfo1":"lfo1",
         "noise_highpass":"highpass",
         "noise_amp":"noise",
         "balance_a":"balance_a",
         "balance_b":"balance_b",
         "balance_noise":"balance_noise",
         "out2_lag":"out2_lag",
         "f1_freq":"freq",
         "f1_freq_env1":"env1",
         "f1_freq_lfo1":"lfo1",
         "f1_freq_lfo2":"lfo2",
         "f1_freq_external":"external",
         "f1_res":"res",
         "f1_amp":"amp",
         "f1_pan":"pan",
         "f2_freq":"freq",
         "f2_freq_env1":"env1",
         "f2_freq_lfo1":"lfo1",
         "f2_freq_env2":"env2",
         "f2_freq_lag":"lag",
         "f2_res":"res",
         "f2_amp":"amp",
         "f2_pan":"pan"}

def klstr2_pp(program,slot):
    def fval(param):
        v = float(program[param])
        return "%5.4f" % v
    def ival(param):
        v = int(program[param])
        return "%d" % v

    acc = 'klstr2(%d,"%s",amp=%s,\n' % (slot,program.name,fval("amp"))
    lfo_params = ("lfoFreq","lfo2Ratio","vibrato")
    acc += '       lfo = {'
    for p in lfo_params:
        if p != lfo_params[0]: acc += ' '*14
        acc += '"%s":%s' % (_pmap[p],fval(p))
        if p != lfo_params[-1]:
            acc += ',\n'
        else:
            acc += '},\n'

    def env(acc, index):
        eparams = []
        for q in ("attack","decay1","decay2","release","breakpoint","sustain"):
            eparams.append("env%d_%s" % (index,q))
        acc += '       env%d = {' % index
        for p in eparams:
            if p != eparams[0]: acc += ' '*15
            acc += '"%s":%s,\n' % (_pmap[p],fval(p))
        p = "env%d_mode" % index
        acc += ' '*15
        acc += '"%s":%s},\n' % (_pmap[p],ival(p))
        return acc
    acc = env(acc, 1)
    acc = env(acc, 2)
    spread_params = ("spread","spread_env1","spread_lfo1","spread_external")
    acc += '       spread = {'
    for p in spread_params:
        if p != spread_params[0]: acc += ' '*17
        acc += '"%s":%s' % (_pmap[p],fval(p))
        if p != spread_params[-1]:
            acc += ',\n'
        else:
            acc += '},\n'
    cluster_params = ("cluster","cluster_env1","cluster_lfo1","cluster_lfo2",
                      "cluster_external")
    acc += '       cluster = {'
    for p in cluster_params:
        if p != cluster_params[0]: acc += ' '*18
        acc += '"%s":%s' % (_pmap[p],fval(p))
        if p != cluster_params[-1]:
            acc += ',\n'
        else:
            acc += '},\n'
    pw_params = ("pw","pw_lfo1","pw_env1")
    acc += '       pw = {'
    for p in pw_params:
        if p != pw_params[0]: acc += ' ' * 13
        acc += '"%s":%s' % (_pmap[p],fval(p))
        if p != pw_params[-1]:
            acc += ',\n'
        else:
            acc += '},\n'
    h1_params = ("harm1","harm1_env1","harm1_env2",
                 "harm1_lfo1","harm1_lfo2")
    acc += '       harm1 = {'
    for p in h1_params:
        if p != h1_params[0]: acc += ' '*16
        acc += '"%s":%s' % (_pmap[p],ival(p))
        if p != h1_params[-1]:
            acc += ',\n'
        else:
            acc += '},\n'
    h2_params = ("harm2","harm2_env1","harm2_lfo1","harm2_external")
    acc += '       harm2 = {'
    for p in h2_params:
        if p != h2_params[0]: acc += ' '*16
        acc += '"%s":%s,\n' % (_pmap[p],ival(p))
    acc += ' '*16 + '"lag":%s},\n' %  fval("harm2_lag")
    nse_params = ("noise_lowpass","noise_lowpass_env1","noise_lowpass_lfo1",
                  "noise_highpass")
    acc += '       noise_filter = {'
    for p in nse_params:
        if p != nse_params[0]: acc += ' '*23
        acc += '"%s":%s' % (_pmap[p],ival(p))
        if p != nse_params[-1]:
            acc += ',\n'
        else:
            acc += '},\n'
    mix_params = ("noise_amp","balance_a","balance_b","balance_noise")
    acc += '       mixer = {'
    for p in mix_params:
        if p != mix_params[0]: acc += ' '*16
        acc += '"%s":%s' % (_pmap[p],fval(p))
        if p != mix_params[-1]:
            acc += ',\n'
        else:
            acc += '},\n'
    f1_params = ("f1_freq","f1_freq_env1","f1_freq_lfo1","f1_freq_lfo2",
                 "f1_freq_external")
    acc += '       filter_1 = {'
    for p in f1_params:
        if p != f1_params[0]: acc += ' '*19
        acc += '"%s":%s,\n' % (_pmap[p],ival(p))
    f1_params = ("f1_res","f1_amp","f1_pan")
    for p in f1_params:
        acc += ' '*19 + '"%s":%s' % (_pmap[p],fval(p))
        if p != f1_params[-1]:
            acc += ',\n'
        else:
            acc += '},\n'
    f2_params = ("f2_freq","f2_freq_env1","f2_freq_env2","f2_freq_lfo1")
    acc += '       filter_2 = {'
    for p in f2_params:
        if p != f2_params[0]: acc += ' '*19
        acc += '"%s":%s,\n' % (_pmap[p],ival(p))
    f2_params = ("f2_freq_lag","f2_res","f2_amp","f2_pan")
    for p in f2_params:
        acc += ' '*19 + '"%s":%s' % (_pmap[p],fval(p))
        if p != f2_params[-1]:
            acc += ',\n'
        else:
            acc += '})\n'
    return acc



