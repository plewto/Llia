# llia.synths.corvus.corvus_pp

def pp(program, slot):
    pad = ' '*8
    acc = 'corvus(%d, "%s",\n' % (slot,program.name)
    for p in ('port','amp','vfreq','vdelay','vsens','vdepth',
              'xpitch','lfo1_ratio','lfo1_delay','lfo2_ratio','lfo2_delay'):
        v = round(float(program[p]),4)
        acc += '%s%s = %5.4f,\n' % (pad,p,v)
    def op(n):
        pad2 = ' '*17
        bcc = '%sop%d = op(%d,\n' % (pad,n,n)
        for p in ('ratio','bias','amp','velocity','lfo1','lfo2','external','pe',
                  'attack','decay1','decay2','release','breakpoint','sustain'):
            param = 'op%d_%s' % (n,p)
            value = round(program[param],4)
            bcc += '%s%s = %5.4f,\n' % (pad2,p,value)
        for p in ('left','right','key','enable'):
            param = 'op%d_%s' % (n,p)
            value = int(program[param])
            bcc += '%s%s = %d,\n' % (pad2,p,value)
        p = 'op%d_env_mode' % n
        bcc += '%senv_mode = %d' % (pad2,int(program[p]))
        if n < 3:
            bcc += '),\n'
        elif n==3:
            bcc += ',\n'
            bcc += '%snse_mix = %5.4f,\n' % (pad2,float(program['nse3_mix']))
            bcc += '%snse_bw = %d),\n' % (pad2,int(program['nse3_bw']))
        elif n==4:
            bcc += ',\n'
            bcc += '%sbzz_n = %d,\n' % (pad2,int(program['bzz4_n']))
            bcc += '%sbzz_env = %d,\n' % (pad2,int(program['bzz4_env']))
            bcc += '%sbzz_lfo2 = %d,\n' % (pad2,int(program['bzz4_lfo2']))
            bcc += '%sbzz_mix = %5.4f),\n' % (pad2,float(program['bzz4_mix']))
      
        return bcc
    
    def fm(n):
        pad2 = ' '*17
        bcc = '%sfm%d = fm(%d,\n' % (pad,n,n)
        for p in ('ratio','modscale','moddepth','lag',
                  'lfo1','lfo2','external'):
            param = 'fm%d_%s' % (n,p)
            value = round(program[param],4)
            bcc += '%s%s = %5.4f,\n' % (pad2,p,value)
        bcc += '%sleft = %d,\n' % (pad2,int(program['fm%d_left'%n]))
        bcc += '%sright = %d' % (pad2,int(program['fm%d_right'%n]))
        bcc += '),\n'
        return bcc

    def pitch_env():
        pad2 = ' '*30
        ccc = '['
        for a in (0,1,2,3,4):
            p = 'pe_a%d' % a
            v = round(float(program[p]),4)
            ccc += str(v)
            if a == 4:
                ccc += ']'
            else:
                ccc += ','
        dcc = '['
        for t in (1,2,3,4):
            p = 'pe_t%d' % t
            v = round(float(program[p]),4)
            dcc += str(v)
            if t == 4:
                dcc += ']'
            else:
                dcc += ','
        bcc = '%spitch_env = pitch_env(levels = %s,\n' % (pad,ccc)
        bcc += '%stimes = %s,\n' % (pad2,dcc)
        bcc += '%shold = %d,\n' % (pad2, int(program['pe_rnode']))
        bcc += '%sloop = %d))\n' % (pad2, int(program['pe_loop']))
        return bcc
    for n in (1,2,3,4):
        acc += op(n)
        acc += fm(n)
    acc += pitch_env()
    return acc


