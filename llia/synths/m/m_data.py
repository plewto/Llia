# llia.synths.m.m_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance

prototype = {
    "port" : 0.0,                 # Portamento 0..1
    "amp" : 0.1,                  # Main amp 0..2
    "vfreq" : 5.00,               # primary (vibrato) LFO frequency (0..99)
    "vdelay" : 0.0,               # vibrato delay (0..4)
    "vsens" : 0.1,                # vibrato sensitivity (0..1)
    "vdepth" : 0.0,               # vibrato depth (0..1)
    "xPitch" : 0.0,               # external -> pitch (0..1)
    "tremoloLag" : 0.1,           # Common tremolo lag time (0..1)
    
    "aAttack" : 0.0,              # Tone A envelope
    "aDecay1" : 0.0,              #
    "aDecay2" : 0.0,              #
    "aRelease" : 0.0,             #
    "aBreakpoint" : 1.0,          #
    "aSustain" : 1.0,             #
    "aTrigMode" : 0,              # Tone A envelope mode, 0=gate, 1=triggered
    "aLfoRatio" : 1.0,            # Frequency ratio of LFO A relative to vfreq
    "aLfoDelay" : 0.0,            # LFO A onset delay in seconds.
    "aRatio" : 1.0,               # Tone A frequency ratio (0.001 -> 16.000)
    "aKey" : 60,                  # Tone A keyscale reference key (MIDI keynumber) (0..127)
    "aKeyscaleLeft" : 0,          # Tone A left keyscale depth, db/octave  (-18..+18)
    "aKeyscaleRight" : 0,         # Tone A right keyscale depth, db/octave (-18..+18)
    "aQuotient" : 1,              # Tone A pulse divider quotient (0.125, 0.25, 0.5, 1, 2, 3, ..., 16)
    "aQLfo" : 0,                  # LFO -> divider quotient (0..16)
    "aQEnv" : 0,                  # Env -> divider quotient (-16..+16)
    "aQExternal" : 0,             # External -> divider quotient (-16..+16)
    "aPulseWidth" : 0.5,          # Tone A divider output pulse width (0..16)
    "aPwmLfo" : 0.0,              # LFO -> divider pulse width (0..8)
    "aPwmEnv" : 0.0,              # Env -> divider pulse width (0..8)
    "aPwmExternal" : 0.0,         # External -> divider pulse width (0..8)
    "aClkMix" : 0.0,              # Tone A master clock (sine) mix, (0->divider only, 1->sine only)
    "aLfo" : 0.0,                 # LFO -> Tone A tremolo
 
    "bAttack" : 0.0,              # Tone B envelope
    "bDecay1" : 0.0,              #
    "bDecay2" : 0.0,              #
    "bRelease" : 0.0,             #
    "bBreakpoint" : 1.0,          #
    "bSustain" : 1.0,             #
    "bTrigMode" : 0,              #
    "bLfoRatio" : 1.0,            #
    "bLfoDelay" : 0.0,            #
    "bRatio1" : 1.0,              # Tone B1 frequency ratio
    "bRatio2" : 1.0,              # Tone B2 frequency ratio
    "bKey" : 60,                  #
    "bKeyscaleLeft" : 0,          #
    "bKeyscaleRight" : 0,         #
    "bN1" : 32,                   # Tone B1 harmonic count (0..32)
    "bN2" : 24,                   # Tone B2 harmonic count (0..32)

    "bNLfo" : 0,                  # LFO -> (joint 1&2) harmonic count
    "bNEnv" : 0,                  # Env -> (joint 1&2) harmonic count
    "bNExternal" : 0,             # External -> (joint 1&2) harmonic count 

    "bN2Lag" : 0.0,               # Tone B2 harmonic count lagtime (0..2)
    "b2Polarity" : 1,             # Tone B2 polarity (-1, 0(off), +1)
    "bLfo" : 0.0,                 # LFO -> Tone B tremolo

    "noiseLP" : 16000,            # Noise LP cutoff, Hz
    "noiseHP" : 10,               # Noise HP cutoff, Hz
    "noiseLfo" : 0.0,             # LFOB -> noise tremolo
    "noiseLag" : 0.0,             # Noise envelope lag time (0..2)
    
    "cAttack" : 0.0,              # Tone C envelope
    "cDecay1" : 0.0,              #
    "cDecay2" : 0.0,              #
    "cRelease" : 0.0,             #
    "cBreakpoint" : 1.0,          #
    "cSustain" : 1.0,             #
    "cTrigMode" : 0,              #
    "cLfoRatio" : 1.0,            #
    "cLfoDelay" : 0.0,            #

    
    "cRatio" : 1.0,               # Tone C frequency ratio (0.25..16)
    "cKey" : 60,                  #
    "cKeyscaleLeft" : 0,          #
    "cKeyscaleRight" : 0,         #
    "cFb" : -1,                   # Tone C feedback (-1,0,+1)
    "cPulseRatio" : 1.0,          # Tone C incite pulse freq ratio (0.01,..16)
    "cPw" : 0.5,                  # Tone C incite pulse width (0..1)
    "cPulseRatioLfo" : 0.0,       # LFO -> incite pulse freq ratio (0..16)
    "cPulseRatioEnv" : 0.0,       # Env -> incite pulse freq ratio (-16..+16)
    "cPulseRatioExternal" : 0.0,  # External -> incite pulse freq ratio (-16..+16)
    "cPwmLfo" : 0.0,              # LFO -> incite pulse width (0..1)
    "cPwmEnv" : 0.0,              # Env -> incite pulse width (0..1)
    "cPwmExternal" : 0.0,         # External -> incite pulse width (0..1)
    "cInciteSelect" : -1,         # incite signal mix  -1-> pulse  +1-> pink noise
    "cLfo" : 0.0,                 # LFO -> Tone C tremolo


    "aAmp" : 0.333,               # Filter mixer input amps
    "bAmp" : 0.333,               #
    "cAmp" : 0.333,               #
    "noiseAmp" : 0.00,            #
    "aFilter" : -1,               # Filter mixer pan -1->lowpass, +1->bandpass
    "bFilter" : -1,               #
    "cFilter" : -1,               #
    "noiseFilter" : -1,           #
    
    "f1Freq" : 16000,             # Filter 1 (lowpass) static cutoff, (100,...,10k) Hz
    "f1Keytrack" : 0,             # Filter 1 keytrack (0,0.5,1,1.5,2)
    "f1Res" : 0.0,                # Filter 1 resonance (0..1)
    "f1FreqLfoA" : 0,             # LFOA -> filter 1 cutoff (0..1K)
    "f1FreqEnvA" : 0,             # EnvA -> filter 1 cutoff (-10k..+10k)
    "f1FreqLfoB" : 0,             # LFOB -> filter 1 cutoff (0..1k)
    "f1FreqEnvB" : 0,             # EnvB -> filter 1 cutoff (-10k..+10k)
    "f1FreqExternal" : 0,         # External -> filter 1 cutoff (-10k..+10k)
    "f1Pan" : 0.0,                # Filter 1 output pan (-1..+1)
    "f2Freq" : 400,               # Filter 2 (bandpass) static cutoff, (100,...,10k) Hz
    "f2Keytrack" : 0,             #
    "f2Res" : 0.0,                #
    "f2FreqLfoB" : 0,             #
    "f2FreqEnvB" : 0,             #
    "f2FreqLfoC" : 0,             #
    "f2FreqEnvC" : 0,             #
    "f2FreqExternal" : 0,         #
    "f2Pan" : 0.0}


class M(Program):

    def __init__(self,name):
        super(M,self).__init__(name,M,prototype)
        self.performance = performance()

program_bank = ProgramBank(M("Init"))
program_bank.enable_undo = False

def lfo(vFreq = 7.0,
        vSens = 0.1,
        vDepth = 0.0,
        xPitch = 0.0,
        aRatio = 1.0,
        bRatio = 1.0,
        cRatio = 1.0,
        vDelay = 0.0,
        aDelay = 0.0,
        bDelay = 0.0,
        cDelay = 0.0,
        tLag = 0.0):
    def f(v):
        return round(float(v),4)
    d = {"vfreq" : f(vFreq),
         "vdelay" : f(vDelay),
         "vsens" : f(vSens),
         "vdepth" : f(vDepth),
         "xPitch" : f(xPitch),
         "aLfoRatio" : f(aRatio),
         "aLfoDelay" : f(aDelay),
         "bLfoRatio" : f(bRatio),
         "bLfoDelay" : f(bDelay),
         "cLfoRatio" : f(cRatio),
         "cLfoDelay" : f(cDelay),
         "tremoloLag" : f(tLag)}
    return d

def env(n, times = [0.0, 0.0, 0.0, 0.0], levels = [1.0, 1.0], mode = 0):
    def f(v):
        return round(float(v),4)
    def p(suffix):
        return n+suffix[0].upper()+suffix[1:]
    times = fill(times, [0.0, 0.0, 0.0, 0.0])
    levels = fill(levels, [1.0, 1.0])
    d = {p("attack") : times[0],
         p("decay1") : times[1],
         p("decay2") : times[2],
         p("release") : times[3],
         p("breakpoint") : levels[0],
         p("sustain") : levels[1],
         p("trigMode") : int(mode)}
    return d

def fill(lst, template):
    acc = []
    for i,dflt in enumerate(template):
        try:
            v = lst[i]
        except IndexError:
            v = dflt
        acc.append(round(float(v),4))
    return acc

def toneA(ratio = 1.0,
          keyscale = [60, 0, 0],            # [key, left, right]
          quotient = [1.0, 0.0, 0.0, 0.0],  # [n, lfo, env, external]
          pulse = [0.5, 0.0, 0.0, 0.0],     # [pw,lfo, env, external]
          clkmix = 0.0,
          tremolo = 0.0):
    def f(v):
        return round(float(v), 4)
    keyscale = fill(keyscale, [60,0,0])
    quotient = fill(quotient,[1,0,0,0])
    pulse = fill(pulse,[0.5,0,0,0])
    d = {"aRatio" : f(ratio),
         "aKey" : int(keyscale[0]),
         "aKeyscaleLeft" : int(keyscale[1]),
         "aKeyscaleRight" : int(keyscale[2]),
         "aQuotient" : quotient[0],
         "aQLfo" : quotient[1],
         "aQEnv" : quotient[2],
         "aQExternal" : quotient[3],
         "aPulseWidth" : pulse[0],
         "aPwmLfo" : pulse[1],
         "aPwmEnv" : pulse[2],
         "aPwmExternal" : pulse[3],
         "aClkMix" : f(clkmix),
         "aLfo" : f(tremolo)}
    return d

def toneB(ratio1 = 1.0, ratio2 = 1.0,
          keyscale = [60,0,0],
          n1 = [32, 0, 0, 0],    # [n1, lfo, env, external]
          n2 = [24, 0.0, 1.0],   # [n2, lag, polarity]
          tremolo = 0.0):
    keyscale = fill(keyscale, [60,0,0])
    n1 = fill(n1,[32,0,0,0])
    n2 = fill(n2,[24,0,0])
    d = {"bRatio1" : float(ratio1),
         "bRatio2" : float(ratio2),
         "bKey" : int(keyscale[0]),
         "bKeyscaleLeft" : int(keyscale[1]),
         "bKeyscaleRight" : int(keyscale[2]),
         "bN1" : int(n1[0]),
         "bNLfo" : int(n1[1]),
         "bNEnv" : int(n1[2]),
         "bNExternal" : int(n1[3]),
         "bN2" : int(n2[0]),
         "bN2Lag" : float(n2[1]),
         "b2Polarity" : int(n2[2]),
         "bLfo" : round(float(tremolo),4)}
    return d

def toneC(ratio = 1.0,
          keyscale = [60,0,0],
          fb = -1,
          pulseFreq = [1.0, 0.0, 0.0, 0.0],  # [ratio, lfo, env, external
          pwm = [0.5, 0.0, 0.0, 0.0],        # [iwidth, lfo, env, external]
          inciteSelect = -1.0,
          tremolo = 0.0):
    keyscale = fill(keyscale, [60,0,0])
    pulseFreq = fill(pulseFreq,[1.0,0.0,0.0,0.0])
    pwm = fill(pwm,[0.5,0.0,0.0,0.0])
    d = {"cRatio" : round(float(ratio),4),
         "cKey" : int(keyscale[0]),
         "cKeyscaleLeft" : int(keyscale[1]),
         "cKeyscaleRight" : int(keyscale[2]),
         "cFb" : float(fb),
         "cPulseRatio" : pulseFreq[0],
         "cPulseRatioLfo" : pulseFreq[1],
         "cPulseRatioEnv" : pulseFreq[2],
         "cPulseRatioExternal" : pulseFreq[3],
         "cPw" : pwm[0],
         "cPwmLfo" : pwm[1],
         "cPwmEnv" : pwm[2],
         "cPwmExternal" : pwm[3],
         "cInciteSelect" : round(float(inciteSelect), 4),
         "cLfo" :round(float(tremolo),4)}
    return d

def noise(lp = 16000, hp = 10, lag = 0.0, tremolo = 0.0):
    d = {"noiseLP" : int(lp),
         "noiseHP" : int(hp),
         "noiseLag" : round(float(lag),4),
         "noiseLfo" : round(float(tremolo),4)}
    return d

def mixer(mix = [0.333, 0.333, 0.333, 0.00],    # [a,b,c, noise]
          pan = [-1.0, -1.0, -1.0, -1.0]):
    mix = fill(mix, [0.333,0.333,0.333,0.000])
    pan = fill(pan, [-1.0, -1.0, -1.0, -1.0])
    d = {}
    for i,n in enumerate(("a","b","c","noise")):
        d["%sAmp" % n] = round(float(mix[i]),4)
        d["%sFilter" % n] = round(float(pan[i]),4)
    return d

def filter_(n,freq=16000,track=0,res=0.5,
            lfo = [0.0, 0.0],
            env = [0.0, 0.0],
            external = 0.0,
            pan = 0.0):
    lfo = fill(lfo, [0.0, 0.0])
    env = fill(env, [0.0, 0.0])
    if n == 1:
        lfo_params = ["f1FreqLfoA","f1FreqLfoB"]
        env_params = ["f1FreqEnvA","f1FreqEnvB"]
    else:
        lfo_params = ["f2FreqLfoB","f2FreqLfoB"]
        env_params = ["f2FreqEnvC","f2FreqEnvC"]
    def p(suffix):
        return "f%d%s" % (n,suffix)
    d = {p("Freq") : int(freq),
         p("Keytrack") : round(float(track), 4),
         p("Res") : round(float(res),4),
         lfo_params[0] : lfo[0],
         lfo_params[1] : lfo[1],
         env_params[0] : env[0],
         env_params[1] : env[1],
         p("Pan") :  round(float(pan),4)}
    return d

def m(slot, name, # FIXME
      port = 0.0, amp = 0.1,
      lfo = lfo(),
      enva = env("a"),
      envb = env("b"),
      envc = env("c"),
      a = toneA(),
      b = toneB(),
      c = toneC(),
      noise = noise(),
      mix = mixer(),
      f1 = filter_(1),
      f2 = filter_(2)):
   p = M(name)
   p["port"] = round(float(port),4)
   p["amp"] = round(float(amp),4)
   for d in (lfo,enva,envb,envc,a,b,c,noise,mix,f1,f2):
       p.update(d)
   program_bank[slot] = p
   return p

m(0,"Init",  port=0.000, amp=0.100,
  lfo = lfo(vFreq=7.000,vSens=0.100,vDepth=0.000,xPitch=0.000,
            aRatio=1.000,bRatio=1.000,cRatio=1.000,
            vDelay=0.000,aDelay=0.000,bDelay=0.000,cDelay=0.000,tLag=0.000),
  enva = env("a", [0.000,0.000,0.000,0.000],[1.000,1.000],0),
  envb = env("b", [0.000,0.000,0.000,0.000],[1.000,1.000],0),
  envc = env("c", [0.000,0.000,0.000,0.000],[1.000,1.000],0),
  a = toneA(ratio=1.000,
            keyscale=[60,0,0],
            quotient=[1,0.000,0.000,0.000],
            pulse=[0.500,0.000,0.000,0.000],
            clkmix=0.000,
            tremolo=0.000),
  b = toneB(ratio1=1.000,
            ratio2=1.000,
            keyscale=[60,0,0],
            n1=[32,0,0,0],
            n2=[24,0.000,1],
            tremolo=0.000),
  c = toneC(ratio=1.000,
            keyscale=[60,0,0],
            fb=-1.000,
            pulseFreq=[1.000,0.000,0.000,0.000],
            pwm=[0.500,0.000,0.000,0.000],
            inciteSelect=1.000,
            tremolo=0.000),
  noise = noise(lp=16000,hp=10,lag=0.000,tremolo=0.000),  
  mix = mixer(mix=[0.333,0.333,0.333,0.000],
              pan=[0.000,0.000,0.000,0.000]),
  f1 = filter_(1,freq=16000,track=0.0,res=0.500,
               lfo=[0, 0],
               env=[0, 0],
               external=0,
               pan=0.000),
  f2 = filter_(2,freq=16000,track=0.0,res=0.500,
               lfo=[0, 0],
               env=[0, 0],
               external=0,
               pan=0.000))
