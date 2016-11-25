# llia.synths.m.pp

def _lfo(pad,fval,ival,program):
    pad2=' '*13
    bcc='%slfo = lfo(' % pad
    for a,p in (('vFreq','vfreq'),('vSens','vsens'),
                ('vDepth','vdepth'),('xPitch','xPitch')):
        bcc += '%s=%5.4f,' % (a,fval(p))
    bcc += '\n%s' % pad2
    for n in 'abc':
        a,p = '%sRatio' % n, '%sLfoRatio' % n
        bcc += '%s=%5.4f,' % (a,fval(p))
    bcc += '\n%svDelay=%5.4f,' % (pad2,fval('vdelay'))
    for n in 'abc':
        a,p = '%sDelay' % n, '%sLfoDelay' % n
        bcc += '%s=%5.4f,' % (a,fval(p))
    bcc += 'tLag=%5.4f),\n' % fval('tremoloLag')
    return bcc

def _env(pad,n,fval,program):
    bcc='%senv%s = env("%s",[' % (pad,n,n)
    for a in ('attack','decay1','decay2','release'):
        p = "%s%s" % (n, a.capitalize())
        bcc += '%5.4f' % fval(p)
        if a=='release':
            bcc += '],['
        else:
            bcc += ','
    for a in ('breakpoint','sustain'):
        p = '%s%s' % (n,a.capitalize())
        bcc += '%5.4f' % fval(p)
        if a == 'sustain':
            bcc += '],'
        else:
            bcc += ','
    bcc += '%d),\n' % int(program['%sTrigMode' % n])
    return bcc

def _keyscale(n,pad,ival):
    ccc = '%skeyscale=[' % pad
    for b in ('Key','KeyscaleLeft','KeyscaleRight'):
        p = '%s%s' % (n,b)
        ccc += '%d' % ival(p)
        if b == 'KeyscaleRight':
            ccc += '],\n'
        else:
            ccc += ','
    return ccc

def _toneA(pad,fval,ival):
    pad2 = ' '*13
    bcc = '%sa = toneA(ratio=%5.4f,\n' % (pad,fval('aRatio'))
    bcc += _keyscale('a',pad2,ival)
    bcc += '%squotient=[' % pad2
    for p in ('aQuotient','aQLfo','aQEnv','aQExternal'):
        bcc += '%d' % ival(p)
        if p == 'aQExternal':
            bcc += '],\n'
        else:
            bcc += ','
    bcc += '%spulse=[' % pad2
    for p in ('aPulseWidth','aPwmLfo','aPwmEnv','aPwmExternal'):
        bcc += '%5.4f' % fval(p)
        if p == 'aPwmExternal':
            bcc += '],\n'
        else:
            bcc += ','
    bcc += '%sclkmix=%5.4f,\n' % (pad2,fval('aClkMix'))
    bcc += '%stremolo=%5.4f),\n' % (pad2,fval('aLfo'))
    return bcc

def _toneB(pad,fval,ival):
    pad2=' '*13
    bcc = '%sb = toneB(ratio1=%5.4f,\n' % (pad,fval('bRatio1'))
    bcc += '%sratio2=%5.4f,\n' % (pad2,fval('bRatio2'))
    bcc += _keyscale('b',pad2,ival)
    bcc += '%sn1=[' % pad2
    for p in ('bN1','bNLfo','bNEnv','bNExternal'):
        bcc += '%d' % ival(p)
        if p == 'bNExternal':
            bcc += '],\n'
        else:
            bcc += ','
    bcc += '%sn2=[' % pad2
    for p in ('bN2','bN2Lag','b2Polarity'):
        if p == 'bN2Lag':
            bcc += '%5.4f' % fval(p)
        else:
            bcc += '%d' % ival(p)
        if p == 'b2Polarity':
            bcc += '],\n'
        else:
            bcc += ','
    bcc += '%stremolo=%5.4f),\n' % (pad2,fval('bLfo'))
    return bcc

def _toneC(pad,fval,ival):
    pad2=' '*13
    bcc = '%sc = toneC(ratio=%5.4f,\n' % (pad,fval('cRatio'))
    bcc += _keyscale('c',pad2,ival)
    bcc += '%sfb=%+6.4f,\n' % (pad2,fval('cFb'))
    bcc += '%spulseFreq=[' % pad2
    for p in ('cPulseRatio','cPulseRatioLfo',
              'cPulseRatioEnv','cPulseRatioExternal'):
        bcc += '%5.4f' % fval(p)
        if p == 'cPulseRatioExternal':
            bcc += '],\n'
        else:
            bcc += ','
    bcc += '%spwm=[' % pad2
    for p in ('cPw','cPwmLfo','cPwmEnv','cPwmExternal'):
        bcc += '%5.4f' % fval(p)
        if p == 'cPwmExternal':
            bcc += '],\n'
        else:
            bcc += ','
    bcc += '%sinciteSelect=%5.4f,\n' % (pad2,fval('cInciteSelect'))
    bcc += '%stremolo=%5.4f),\n' % (pad2,fval('cLfo'))
    return bcc
        
def _noise(pad,fval,ival):
    bcc = '%snoise = noise(' % pad
    for a,p in (('lp','noiseLP'),('hp','noiseHP')):
        bcc += '%s=%d,' % (a,ival(p))
    for a,p in (('lag','noiseLag'),('tremolo','noiseLfo')):
        bcc += '%s=%5.4f' % (a,fval(p))
        if a == 'tremolo':
            bcc += '),\n'
        else:
            bcc += ','
    return bcc

def _mixer(pad,fval):
    pad2=' '*15
    mcc = 'mix=['
    pcc = 'pan=['
    for n in ('a','b','c','noise'):
        pamp = '%sAmp' % n
        ppan = '%sFilter' % n
        mcc += '%5.4f' % fval(pamp)
        pcc += '%+5.3f' % fval(ppan)
        if n == 'noise':
            mcc += '],\n'
            pcc += ']),\n'
        else:
            mcc += ','
            pcc += ','
    bcc = '%smix = mixer(%s' % (pad,mcc)
    bcc += '%s%s' % (pad2,pcc)
    return bcc

def _filter(n,pad,fval,ival):
    pad2=' '*16
    bcc = '%sf%d = filter_(%d,' % (pad,n,n)
    for a,b in (('freq','Freq'),('track','Keytrack'),('res','Res')):
        p = 'f%d%s' % (n,b)
        if a == 'freq':
            bcc += '%s=%d,' % (a,ival(p))
        else:
            bcc += '%s=%5.4f,' % (a,fval(p))
    bcc += '\n'
    if n == 1:
        plfo = ('f1FreqLfoA','f1FreqLfoB')
        penv = ('f1FreqEnvA','f1FreqEnvB')
    else:
        plfo = ('f2FreqLfoB','f2FreqLfoC')
        penv = ('f2FreqEnvB','f2FreqEnvC')
    bcc += '%slfo=[%d,%d],\n' % (pad2,ival(plfo[0]),ival(plfo[1]))
    bcc += '%senv=[%d,%d],\n' % (pad2,ival(penv[0]),ival(penv[1]))
    bcc += '%sexternal=%d,\n' % (pad2,ival('f%dFreqExternal'%n))
    bcc += '%span=%5.4f' % (pad2,fval('f%dPan'%n))
    if n == 1:
        bcc += '),\n'
    else:
        bcc += '))\n'
    return bcc
        
def pp(program, slot=127):
    pad = ' '*3
    def fval(key):
        return round(float(program[key]),4)
    def ival(key):
        return int(program[key])
    
    acc = 'm(%d,"%s",\n' % (slot,program.name)
    acc += '%sport=%5.4f,amp=%5.4f,\n' % (pad,fval('port'),fval('amp'))
    acc += _lfo(pad,fval,ival,program)
    for n in 'abc':
        acc += _env(pad,n,fval,program)
    acc += _toneA(pad,fval,ival)
    acc += _toneB(pad,fval,ival)
    acc += _toneC(pad,fval,ival)
    acc += _noise(pad,fval,ival)
    acc += _mixer(pad,fval)
    acc += _filter(1,pad,fval,ival)
    acc += _filter(2,pad,fval,ival)
    return acc
