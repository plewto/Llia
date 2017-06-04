# llia.synths.sandcat.sandcat_pp

from __future__ import print_function


def _vibrato(pad,fval):
    freq = fval("freq","vfreq")
    delay = fval("delay","vdelay")
    sens = fval("sens","vsens")
    depth= fval("depth","vdepth")
    x = fval("x1","vxbus1")
    frmt = "%svibrato=vibrato(%s,%s,%s,%s,%s),\n"
    return frmt % (pad,freq,delay,sens,depth,x)

def _lfo(n,pad,fval):
    if n==1:
        kxmod = "lfo1_freq_lfo2"
    else:
        kxmod = "lfo2_freq_lfo1"
    ratio = fval("ratio","lfo%d_ratio" % n)
    xmod = fval("xmod",kxmod)
    frmt = "%slfo%d=lfo(%d,%s,%s),\n"
    data = (pad,n,n,ratio,xmod)
    return frmt % data

def _clock(n,pad,fval):
    k = "clk%d_ratio" % n
    r = fval("ratio",k)
    return "%sclk%d=clock(%d,%s),\n" % (pad,n,n,r)

def _adsr(n,pad,program):
    def key(suffix):
        return "env%d_%s" % (n,suffix)
    def fval(suffix):
        return "%5.4f" % program[key(suffix)]
    def ival(suffix):
        k = "env%d_trig_%s" % (n,suffix)
        i = int(program[k])
        return "%d" % i
    frmt="%senv%d=adsr(%d,%s,%s,%s,%s,src=%s,mode=%s),\n"
    data = (pad,n,n,fval("attack"),fval("decay"),fval("sustain"),
            fval("release"),ival("src"),ival("mode"))
    return frmt % data

def _excite(n,pad,program):
    def key(suffix):
        return "ex%d_%s" % (n,suffix)
    kharm = key("harmonic")
    klfo = "ex%d_lfo%d" % (n,n)
    kenv = "ex%d_env%d" % (n,n)
    kpw = key("pw")
    kpwm = "ex%d_lfo%d" % (n,n)
    knse = key("noise_select")
    kmix = key("source_mix")
    harm = int(program[kharm])
    lfo = int(program[klfo])
    env = int(program[kenv])
    pw = float(program[kpw])
    pwm = float(program[kpwm])
    nse = int(program[knse])
    mix = float(program[kmix])
    pad2 = pad+' '*11
    frmt1 = "%sex%d=excite(%d,harmonic=%d,lfo=%d,env=%d,pw=%5.4f,pwm=%5.4f,\n"
    data1 = (pad,n,n,harm,lfo,env,pw,pwm)
    frmt2 = "%snoise=%d, mix=%5.4f),\n"
    data2 = (pad2,nse,mix)
    return (frmt1 % data1) + (frmt2 % data2)
    
def _pluck(n,pad,program):
    def key(suffix):
        return "ks%d_%s" % (n,suffix)
    def fval(suffix):
        k = key(suffix)
        v = float(program[k])
        frmt = "%5.4f"
        return frmt % v
    def ival(suffix):
        k = key(suffix)
        v = int(program[k])
        frmt = "%d"
        return frmt % v
    frmt = "%sks%d=pluck(%d,ratio=%s,decay=%s,coef=%s,trig=%s,velocity=%s),\n"
    data = (pad,n,n,fval("ratio"),fval("decay"),fval("coef"),
            ival("trig_src"),fval("velocity"))
    return frmt % data

def _stack(n,pad,program):
    def key(suffix):
        return "stack%d_%s" % (n,suffix)
    frmt="%sstack%d=stack(%d,break_key=%d,feedback=%s,feedback_lfo=%s),\n"
    data = (pad,n,n,
            int(program[key("break_key")]),
            "%5.4f" % float(program[key("fb")]),
            "%5.4f" % float(program[key("fb_lfo%d" % n)]))
    return frmt % data

def _mod(n,pad,program):
    def key(suffix):
        return "mod%d_%s" % (n,suffix)
    def fval(param,suffix):
        k = key(suffix)
        v = float(program[k])
        return "%s=%5.4f" % (param,v)
    def ival(param,suffix):
        k = key(suffix)
        v = int(program[k])
        return "%s=%d" % (param,v)
    frmt1="%smod%d=mod(%d,%s,%s,%s,%s,%s,\n"
    data1 = (pad,n,n,
             fval("ratio","ratio"),
             fval("bias","bias"),
             fval("ks","ks%d" % n),
             fval("env","env%d" % n),
             fval("lag","lag"))
    pad2 = pad+' '*9
    frmt2 = "%s%s,%s,%s),\n"
    data2 = (pad2,
             fval("velocity","velocity"),
             ival("left","left_scale"),
             ival("right","right_scale"))
    return (frmt1 % data1) + (frmt2 % data2)
             

def _car(n,pad,program):
    def key(suffix):
        return "car%d_%s" % (n,suffix)
    def fval(param,suffix):
        k = key(suffix)
        v = float(program[k])
        return "%s=%5.4f" % (param,v)
    def ival(param,suffix):
        k = key(suffix)
        i = int(program[k])
        return "%s=%d" % (param,i)
    frmt1 = "%scar%d=car(%d,%s,%s,%s,"
    data = (pad,n,n,fval("ratio","ratio"),fval("bias","bias"),fval("mod1","mod1"))
    bcc = frmt1 % data
    if n==2: bcc += "%s," % fval("mod2","mod2")
    bcc += "%s,\n" % fval("ks","ks%d" % n)
    pad2 = pad+' '*9

    frmt2 = "%s%s,%s,%s,%s,%s),\n"
    data2 = (pad2,
             ival("env_mode","env_mode"),
             fval("lfo","lfo%d" % n),
             fval("velocity","velocity"),
             ival("left","left_scale"),
             ival("right","right_scale"))
    bcc += frmt2 % data2
    return bcc

def _mixer(pad,fval):
    frmt = "%smixer=mixer(%s,%s,%s,%s),\n"
    data = (pad,fval("ks1","ks1_amp"),fval("ks2","ks2_amp"),
            fval("stack1","stack1_amp"),fval("stack2","stack2_amp"))
    return frmt % data

def _panner(pad,fval):
    frmt = "%spanner=panner(%s,%s,%s,%s))\n"
    data = (pad,fval("ks1","ks1_amp"),fval("ks2","ks2_amp"),
            fval("stack1","stack1_amp"),fval("stack2","stack2_amp"))
    return frmt % data

def sandcat_pp(program,slot):
    pad = ' '*8
    def fval(param, key):
        v = float(program[key])
        frmt = "%s=%5.4f"
        return frmt % (param,v)
    def ival(param, key):
        #print("DEBUG ival  param='%s'    key='%s'" % (param,key))
        n = int(program[key])
        frmt = "%s=%d"
        return frmt % (param,n)
    data = (slot,program.name,program['amp'])
    acc = 'sandcat(%d,"%s",amp=%5.4f,\n' % data
    acc += _vibrato(pad,fval)
    for n in (1,2):
        acc += _lfo(n,pad,fval)
        acc += _clock(n,pad,fval)
        # acc += _adsr(n,pad,program)
        acc += _excite(n,pad,program)
        acc += _pluck(n,pad,program)
        acc += _stack(n,pad,program)
        acc += _mod(n,pad,program)
        acc += _car(n,pad,program)
        pcutoff = "f%d_cutoff" % n
        ptrack = "f%d_track" % n
        penv3 = "f%d_env3" % n
        plfov = "f%d_lfov" % n
        pvelocity = "f%d_velocity" % n
        pres = "f%d_res" % n
        ppan = "f%d_pan" % n
        if n == 1:
            plfox = "f%d_lfo1" % n
            penvx = "f%d_env3" % n
        else:
            plfox = "f%d_lfo2" % n
            penvx = "f%d_env4" % n

        frmt1 = "%s%s,%s,%s,\n"
        data1 = (pad,
                 ival(pcutoff,pcutoff),
                 fval(ptrack,ptrack),
                 ival(penvx,penvx))
        frmt2 = "%s%s,%s,%s,%s,%s,\n"
        data2 = (pad,
                 ival(plfov,plfov),
                 ival(plfox,plfox),
                 ival(pvelocity,pvelocity),
                 fval(pres,pres),
                 fval(ppan,ppan))
        acc += (frmt1 % data1) + (frmt2 % data2)
    for n in (1,2,3,4):
        acc += _adsr(n,pad,program)
    acc += _mixer(pad,fval)
    acc += _panner(pad,fval)
    return acc

