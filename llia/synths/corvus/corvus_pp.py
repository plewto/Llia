# llia.synths.corvus.corvus_pp

def pp(program, slot):
    pad = ' '*8
    acc = 'corvus(%d, "%s",\n' % (slot,program.name)
    for p in ("port","amp","vfreq","vdelay","vsens","vdepth",
              "xpitch","lfo1_ratio","lfo1_delay","lfo2_ratio","lfo2_delay"):
        v = round(float(program[p]),4)
        acc += "%s%s = %5.4f,\n" % (pad,p,v)
    def op(n):
        pad2 = ' '*17
        bcc = '%sop%d = op(%d,\n' % (pad,n,n)
        for p in ("ratio","bias","amp","velocity","lfo1","lfo2","external",
                  "attack","decay1","decay2","release","breakpoint","sustain"):
            param = "op%d_%s" % (n,p)
            value = round(program[param],4)
            bcc += '%s%s = %5.4f,\n' % (pad2,p,value)
        for p in ("left","right","key","enable","env_mode"):
            param = "op%d_%s" % (n,p)
            value = int(program[param])
            bcc += '%s%s = %d' % (pad2,p,value)
            if op < 3 and p == "env_mode":
                bcc += "),\n"
            else:
                bcc += ",\n"
        if n==3:
            bcc += '%snse_mix = %5.4f,\n' % (pad2,float(program["nse3_mix"]))
            bcc += '%snse_bw = %d),\n' % (pad2,int(program["nse3_bw"]))
        if n==4:
            bcc += '%sbzz4_n = %d,\n' % (pad2,int(program["bzz4_n"]))
            bcc += '%sbzz4_env = %d,\n' % (pad2,int(program["bzz4_env"]))
            bcc += '%sbxx4_mix = %5.4f),\n' % (pad2,float(program["bzz4_mix"]))
        return bcc
    
    def fm(n):
        pad2 = ' '*17
        bcc = '%sfm%d = fm(%d,\n' % (pad,n,n)
        for p in ("ratio","modscale","moddepth","lag",
                  "lfo1","lfo2","external"):
            param = "fm%d_%s" % (n,p)
            value = round(program[param],4)
            bcc += '%s%s = %5.4f,\n' % (pad2,p,value)
        bcc += '%sleft = %d,\n' % (pad2,int(program["fm%d_left"%n]))
        bcc += '%sright = %d' % (pad2,int(program["fm%d_right"%n]))
        bcc += "),\n"
        return bcc
    for n in (1,2,3,4):
        acc += op(n)
        acc += fm(n)
    return acc


