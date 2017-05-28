# llia.synths.siris.siris_pp

def vibrato(pad,fval):
    pad2 = pad+' '*16
    frmt1 = '%svibrato=vibrato(%s,%s,%s,\n'
    data1 = (pad,fval('timebase'),fval('vratio'),fval('vsens'))
    frmt2 = '%s%s,%s),\n'
    data2 = (pad2,fval('vdepth'),fval('vdelay'))
    return frmt1%data1 + frmt2%data2 

def adsr(pad,program):
    def fval(key,param):
        k = 'env_%s' % key
        v = float(program[k])
        return '%s=%s' % (param,v)
    frmt = '%sadsr=adsr(%s,%s,%s,%s,mode=%d),\n'
    data = (pad,
            fval('attack','a'),
            fval('decay','d'),
            fval('sustain','s'),
            fval('release','r'),
            int(program['env_mode']))
    return frmt % data
            
def excite(n,pad,program):
    def key(suffix):
        return 'ex%d_%s' % (n,suffix)
    def fval(key_suffix):
        param = key_suffix
        k = key(key_suffix)
        v = float(program[k])
        return '%s=%5.4f' % (param,v)
    def ival(key_suffix):
        param = key_suffix
        k = key(key_suffix)
        v = int(program[k])
        return '%s=%d' % (param,v)
    frmt1 = '%sexcite%d=excite(%d,%s,%s,%s,\n'
    data1 = (pad,n,n,ival('harmonic'),ival('harmonic_lfo'),ival('harmonic_env'))
    pad2 = pad + ' '*15
    frmt2 = '%s%s,%s,%s),\n'
    data2 = (pad2,fval('pw'),fval('pwm_lfo'),fval('pwm_env'))
    return frmt1%data1 + frmt2%data2

def ks_excite(n,pad,program):
    def key(suffix):
        return 'ks%d_%s' % (n,suffix)
    def fval(suffix, param):
        k = key(suffix)
        v = float(program[k])
        return '%s=%5.4f' % (param,v)
    frmt='%sks%d_excite=ks_excite(%d,%s,%s,%s,white=%d),\n'
    data=(pad,n,n,fval('excite1','ex1'),fval('excite2','ex2'),
          fval('excite_noise','noise'),
          int(program[key('excite_white')]))
    return frmt%data

def ks_trig(n,pad,program):
    def key(suffix):
        return 'ks%d_%s' % (n,suffix)
    frmt = '%sks%d_trig=ks_trig(%d,mode=%d,lfo_ratio=%s),\n'
    mode = int(program[key('trig_mode')])
    ratio = '%5.4f' % float(program[key('trig_ratio')])
    data = (pad,n,n,mode,ratio)
    return frmt%data

def ks(n,pad,program):
    def key(suffix):
        return 'ks%d_%s' % (n,suffix)
    def fval(suffix):
        return '%5.3f' % program[key(suffix)]
    frmt1='%sks%d=ks(%d,ratio=%s,attack=%s,decay=%s,coef=%s,\n'
    frmt2 ='%svelocity=%s,amp=%s'
    data1 = (pad,n,n,fval('ratio'),fval('attack'),fval('decay'),fval('coef'))
    data2 = (pad+' '*7,fval('velocity'),fval('amp'))
    rs = frmt1%data1 + frmt2%data2
    if n == 2:
        rs += ',delay=%s),\n' % fval('delay')
    else:
        rs += '),\n'
    return rs
        
def clip(n,pad,program):
    def key(suffix):
        return 'ks%d_clip_%s' % (n,suffix)
    frmt='%sclip%d=clip(%d,enable=%d,gain=%5.3f,threshold=%5.3f),\n'
    enable = int(program[key('enable')])
    gain = float(program[key('gain')])
    th = float(program[key('threshold')])
    data = (pad,n,n,enable,gain,th)
    return frmt%data

def noise(pad,program):
    def fval(key):
        v = float(program[key])
        return '%5.3f' % v
    def ival(key):
        v = int(program[key])
        return '%d' % v
    pad2 = pad+' '*12
    frmt1 = '%snoise=noise(attack=%s,decay=%s,lowpass=%s,highpass=%s,\n'
    data1 = (pad,fval('nse_attack'),fval('nse_decay'),
             ival('nse_lowpass'),ival('nse_highpass'))
    frmt2 = '%sex1_amp=%s,ex2_amp=%s,velocity=%s,amp=%s),\n'
    data2 = (pad2,fval('ex1_amp'),fval('ex2_amp'),
             fval('nse_velocity'),fval('nse_amp'))
    return frmt1%data1 + frmt2%data2

def filter(pad,program):
    def fval(suffix):
        key = 'filter_%s' % suffix
        v = float(program[key])
        return '%5.3f' % v
    def ival(suffix):
        key = 'filter_%s' % suffix
        v = int(program[key])
        return '%d' % v
    frmt='%sfilter=filter(cutoff=%s,track=%s,env=%s,vlfo=%s,velocity=%s,res=%s))\n'
    data=(pad,ival('cutoff'),fval('track'),ival('env'),ival('vlfo'),
          ival('velocity'),fval('res'))
    return frmt % data

def siris_pp(program,slot):
    def fval(key,param=None):
        param = param or key
        val = float(program[key])
        return '%s=%5.4f' % (param,val)
    def ival(key,param=None):
        param = param or key
        val = int(program[key])
        return '%s=%d' % (param,pad,val)
    pad = ' '*6
    acc = 'siris(%d, "%s",%s,%s,\n' % (slot,program.name,
                                      fval('amp'),fval('port'))
    acc += vibrato(pad,fval)
    acc += adsr(pad,program)
    acc += '%sex_lfo=%5.3f,\n' % (pad,float(program['ex_lfo_ratio']))
    acc += '%sex_attack=%5.3f,\n' % (pad,float(program['ex_env_attack']))
    acc += '%sex_decay=%5.3f,\n' % (pad,float(program['ex_env_decay']))
    for n in (1,2):
        acc += excite(n,pad,program)
        acc += ks_excite(n,pad,program)
        acc += ks_trig(n,pad,program)
        acc += ks(n,pad,program)
        acc += clip(n,pad,program)
    acc += noise(pad,program)
    acc += filter(pad,program)
    return acc

