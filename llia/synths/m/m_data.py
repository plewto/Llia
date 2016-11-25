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
    "aEnvPitch" : 0.0,            # env -> A pitch 
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
    "bEnvPitch" : 0.0,            # env -> B pitch
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
    "cEnvPitch" : 0.0,            # env -> C Pitch
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
          envpitch = 0.0,
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
         "aEnvPitch" : f(envpitch),
         "aLfo" : f(tremolo)}
    return d

def toneB(ratio1 = 1.0, ratio2 = 1.0,
          keyscale = [60,0,0],
          n1 = [32, 0, 0, 0],    # [n1, lfo, env, external]
          n2 = [24, 0.0, 1.0],   # [n2, lag, polarity]
          envpitch = 0.0,
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
         "bEnvPitch" : round(float(envpitch),4),
         "bLfo" : round(float(tremolo),4)}
    return d

def toneC(ratio = 1.0,
          keyscale = [60,0,0],
          fb = -1,
          pulseFreq = [1.0, 0.0, 0.0, 0.0],  # [ratio, lfo, env, external
          pwm = [0.5, 0.0, 0.0, 0.0],        # [iwidth, lfo, env, external]
          inciteSelect = -1.0,
          envpitch = 0.0,
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
         "cEnvPitch" : round(float(envpitch),4),
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

def m(slot, name,
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

m(0,"A",
   port=0.0000,amp=0.1122,
   lfo = lfo(vFreq=4.1340,vSens=0.3417,vDepth=0.0000,xPitch=0.0000,
             aRatio=0.0100,bRatio=0.1250,cRatio=0.7500,
             vDelay=0.0000,aDelay=2.0000,bDelay=3.5000,cDelay=2.0000,tLag=0.0000),
   enva = env("a",[9.2393,11.3917,2.0063,7.2336],[0.9834,0.8564],0),
   envb = env("b",[2.6060,12.0000,1.1359,0.0000],[1.0000,0.0000],0),
   envc = env("c",[5.4533,4.0239,3.4000,8.5699],[0.8518,0.9616],0),
   a = toneA(ratio=36.0000,
             keyscale=[60,0,0],
             quotient=[9,5,0,0],
             pulse=[0.3888,0.0000,0.0000,0.0000],
             clkmix=0.0000,
             envpitch=0.0000,
             tremolo=0.0000),
   b = toneB(ratio1=1.5000,
             ratio2=1.5010,
             keyscale=[60,0,0],
             n1=[18,0,0,0],
             n2=[12,0.9634,1],
             envpitch=-1.0000,
             tremolo=0.4070),
   c = toneC(ratio=1.5000,
             keyscale=[60,0,0],
             fb=-1.0000,
             pulseFreq=[1.5000,0.0000,0.0000,0.0000],
             pwm=[0.5000,0.2054,0.6033,0.0000],
             inciteSelect=0.1960,
             envpitch=0.0000,
             tremolo=0.0000),
   noise = noise(lp=20000,hp=10,lag=0.4774,tremolo=0.1709),
   mix = mixer(mix=[0.4467,1.4125,0.2818,0.0000],
               pan=[+0.240,-0.380,-0.880,+0.840]),
   f1 = filter_(1,freq=860,track=0.0000,res=0.3166,
                lfo=[0,0],
                env=[0,5999],
                external=0,
                pan=0.0000),
   f2 = filter_(2,freq=2691,track=0.0000,res=0.3819,
                lfo=[0,0],
                env=[0,7496],
                external=0,
                pan=0.0000))



m(1,"B",
   port=0.0000,amp=0.1259,
   lfo = lfo(vFreq=5.5520,vSens=0.0955,vDepth=0.7538,xPitch=0.0000,
             aRatio=0.2500,bRatio=4.0000,cRatio=0.0100,
             vDelay=0.0000,aDelay=3.0000,bDelay=4.0000,cDelay=4.0000,tLag=0.0000),
   enva = env("a",[4.0413,10.9647,1.9764,0.0908],[0.8481,0.6094],0),
   envb = env("b",[10.1471,4.1693,5.6461,7.5346],[0.7917,0.9009],0),
   envc = env("c",[8.0447,7.2359,7.5367,3.3112],[0.7433,0.7215],0),
   a = toneA(ratio=32.0000,
             keyscale=[60,0,0],
             quotient=[4,0,0,0],
             pulse=[0.0780,0.0479,0.0000,0.0000],
             clkmix=0.9799,
             envpitch=0.0000,
             tremolo=0.0000),
   b = toneB(ratio1=12.8630,
             ratio2=12.8630,
             keyscale=[60,0,0],
             n1=[14,0,0,0],
             n2=[22,0.0755,-1],
             envpitch=-0.3299,
             tremolo=0.1960),
   c = toneC(ratio=6.0000,
             keyscale=[60,0,0],
             fb=-1.0000,
             pulseFreq=[1.3330,2.0000,0.0000,0.0000],
             pwm=[0.0439,0.0000,0.0000,0.0000],
             inciteSelect=0.0000,
             envpitch=0.0000,
             tremolo=0.0000),
   noise = noise(lp=20000,hp=10,lag=0.0000,tremolo=0.0000),
   mix = mixer(mix=[0.3548,1.0000,0.7943,0.0000],
               pan=[+0.160,-0.680,-0.650,-0.870]),
   f1 = filter_(1,freq=3001,track=0.0000,res=0.1759,
                lfo=[0,0],
                env=[0,3346],
                external=0,
                pan=0.0000),
   f2 = filter_(2,freq=3009,track=0.0000,res=0.2663,
                lfo=[0,0],
                env=[0,9394],
                external=0,
                pan=0.0000))

m(2,"C",
   port=0.0000,amp=0.1000,
   lfo = lfo(vFreq=4.0380,vSens=0.6882,vDepth=0.0000,xPitch=0.0000,
             aRatio=0.3330,bRatio=0.6670,cRatio=0.5000,
             vDelay=0.0000,aDelay=3.0000,bDelay=2.0000,cDelay=2.5000,tLag=0.0000),
   enva = env("a",[7.3832,3.6277,10.7497,7.3870],[0.5126,0.7834],1),
   envb = env("b",[6.9407,8.1406,10.5928,4.4468],[0.8221,0.5899],1),
   envc = env("c",[4.7745,6.6605,11.4085,8.3461],[0.6727,0.9028],1),
   a = toneA(ratio=4.0000,
             keyscale=[60,0,0],
             quotient=[1,0,3,0],
             pulse=[0.5000,0.0000,0.0000,0.0000],
             clkmix=0.0000,
             envpitch=0.4000,
             tremolo=0.1457),
   b = toneB(ratio1=1.5000,
             ratio2=16.0000,
             keyscale=[60,0,0],
             n1=[6,0,0,0],
             n2=[12,0.4473,-1],
             envpitch=-0.4340,
             tremolo=0.0000),
   c = toneC(ratio=3.3490,
             keyscale=[60,0,0],
             fb=-1.0000,
             pulseFreq=[2.0000,0.0000,1.0000,0.0000],
             pwm=[0.5000,0.0000,0.9135,0.0000],
             inciteSelect=0.5075,
             envpitch=0.6000,
             tremolo=0.0000),
   noise = noise(lp=20000,hp=501,lag=0.3116,tremolo=0.0000),
   mix = mixer(mix=[1.0000,0.7079,0.5623,0.0000],
               pan=[-0.590,+0.780,+0.900,-0.380]),
   f1 = filter_(1,freq=2245,track=1.0000,res=0.3260,
                lfo=[0,0],
                env=[2073,0],
                external=0,
                pan=0.0000),
   f2 = filter_(2,freq=3809,track=0.0000,res=0.1873,
                lfo=[3755,0],
                env=[0,3664],
                external=0,
                pan=0.0000))

m(3,"D",
   port=0.0000,amp=0.1000,
   lfo = lfo(vFreq=6.6000,vSens=0.1000,vDepth=0.5229,xPitch=0.0000,
             aRatio=0.5000,bRatio=0.7500,cRatio=0.0800,
             vDelay=0.0000,aDelay=0.0000,bDelay=2.0000,cDelay=3.0000,tLag=0.0000),
   enva = env("a",[1.7035,0.2649,0.7696,0.1930],[0.7812,0.6825],1),
   envb = env("b",[0.5396,0.6906,1.5085,0.3467],[0.6341,0.5004],1),
   envc = env("c",[0.4900,0.8636,1.8192,1.6345],[0.9756,0.9521],1),
   a = toneA(ratio=0.7500,
             keyscale=[60,0,0],
             quotient=[3,0,0,0],
             pulse=[0.6506,0.0000,0.0000,0.0000],
             clkmix=0.0000,
             envpitch=0.0000,
             tremolo=0.0000),
   b = toneB(ratio1=5.3540,
             ratio2=1.5000,
             keyscale=[60,0,0],
             n1=[4,0,22,0],
             n2=[9,0.3051,-1],
             envpitch=0.0000,
             tremolo=0.0000),
   c = toneC(ratio=8.0000,
             keyscale=[60,0,0],
             fb=-1.0000,
             pulseFreq=[1.6120,0.0000,2.0000,0.0000],
             pwm=[0.5000,0.0000,0.0000,0.0000],
             inciteSelect=0.3869,
             envpitch=0.0000,
             tremolo=0.0000),
   noise = noise(lp=20000,hp=501,lag=0.0000,tremolo=0.0000),
   mix = mixer(mix=[1.0000,0.7079,0.5623,0.0000],
               pan=[+0.610,+0.960,+0.750,-0.530]),
   f1 = filter_(1,freq=80,track=1.0000,res=0.2693,
                lfo=[0,1512],
                env=[9541,0],
                external=0,
                pan=0.0000),
   f2 = filter_(2,freq=1222,track=1.0000,res=0.0137,
                lfo=[0,0],
                env=[0,8428],
                external=0,
                pan=0.0000))

m(4,"E",
   port=0.0000,amp=0.1000,
   lfo = lfo(vFreq=5.2510,vSens=0.6672,vDepth=0.0000,xPitch=0.0000,
             aRatio=0.1250,bRatio=0.6670,cRatio=0.0400,
             vDelay=0.0000,aDelay=2.0000,bDelay=2.5000,cDelay=1.5000,tLag=0.0000),
   enva = env("a",[6.4894,10.6446,7.0869,10.4388],[0.5083,0.8829],0),
   envb = env("b",[8.0390,3.8590,8.0697,11.6941],[0.6193,0.3387],0),
   envc = env("c",[10.2382,11.9817,5.3714,9.3913],[0.5952,0.6152],0),
   a = toneA(ratio=62.9740,
             keyscale=[60,0,0],
             quotient=[11,0,0,0],
             pulse=[0.4803,0.0000,0.0000,0.0000],
             clkmix=0.0000,
             envpitch=0.0000,
             tremolo=0.0000),
   b = toneB(ratio1=16.0000,
             ratio2=1.3330,
             keyscale=[60,0,0],
             n1=[21,15,0,0],
             n2=[5,0.0000,-1],
             envpitch=0.0000,
             tremolo=0.0000),
   c = toneC(ratio=8.0000,
             keyscale=[60,0,0],
             fb=-1.0000,
             pulseFreq=[3.7230,2.0000,0.0000,0.0000],
             pwm=[0.5816,0.1942,0.0000,0.0000],
             inciteSelect=0.0000,
             envpitch=0.5944,
             tremolo=0.0000),
   noise = noise(lp=20000,hp=501,lag=0.1407,tremolo=0.0000),
   mix = mixer(mix=[0.0000,1.0000,1.0000,0.0000],
               pan=[+0.960,-0.230,+0.290,-0.890]),
   f1 = filter_(1,freq=1171,track=0.0000,res=0.4157,
                lfo=[0,3774],
                env=[2124,3263],
                external=0,
                pan=0.0000),
   f2 = filter_(2,freq=10910,track=0.0000,res=0.4646,
                lfo=[0,0],
                env=[0,0],
                external=0,
                pan=0.0000))

m(5,"F",
   port=0.0000,amp=0.1000,
   lfo = lfo(vFreq=4.7550,vSens=0.1000,vDepth=0.0000,xPitch=0.0000,
             aRatio=0.3330,bRatio=0.7500,cRatio=0.1000,
             vDelay=0.0000,aDelay=0.5000,bDelay=1.5000,cDelay=0.5000,tLag=0.0000),
   enva = env("a",[1.3364,4.4770,3.4747,2.0046],[0.9267,0.9400],0),
   envb = env("b",[0.8353,0.0596,0.0885,2.4055],[0.6889,0.8617],0),
   envc = env("c",[3.0270,1.6037,1.8041,1.8041],[0.8800,0.7867],0),
   a = toneA(ratio=60.0100,
             keyscale=[60,0,0],
             quotient=[12,1,2,0],
             pulse=[0.9475,0.2000,0.0000,0.0000],
             clkmix=0.0000,
             envpitch=-0.2203,
             tremolo=0.0000),
   b = toneB(ratio1=6.0000,
             ratio2=0.7500,
             keyscale=[60,0,0],
             n1=[2,19,0,0],
             n2=[3,0.0000,-1],
             envpitch=0.0000,
             tremolo=0.9698),
   c = toneC(ratio=0.0280,
             keyscale=[60,0,0],
             fb=-1.0000,
             pulseFreq=[5.7210,0.0000,0.0000,0.0000],
             pwm=[0.6283,0.0000,0.0000,0.0000],
             inciteSelect=0.2462,
             envpitch=0.0000,
             tremolo=0.1005),
   noise = noise(lp=20000,hp=10,lag=0.0000,tremolo=0.0000),
   mix = mixer(mix=[0.3981,1.4125,1.0000,0.0000],
               pan=[-0.690,-0.820,+0.740,+0.460]),
   f1 = filter_(1,freq=481,track=1.0000,res=0.3390,
                lfo=[0,0],
                env=[-62,5005],
                external=0,
                pan=0.0000),
   f2 = filter_(2,freq=14325,track=0.0000,res=0.0100,
                lfo=[2681,0],
                env=[0,-1508],
                external=0,
                pan=0.0000))

m(6,"G",
   port=0.0000,amp=0.1000,
   lfo = lfo(vFreq=9.7250,vSens=0.1000,vDepth=0.0000,xPitch=0.0000,
             aRatio=0.1000,bRatio=0.2500,cRatio=0.0200,
             vDelay=0.0000,aDelay=0.5000,bDelay=3.5000,cDelay=4.0000,tLag=0.0000),
   enva = env("a",[0.8789,1.0330,1.6077,1.6907],[0.5684,0.7691],0),
   envb = env("b",[0.2686,1.4493,2.1382,0.0759],[0.7056,0.4467],0),
   envc = env("c",[11.1087,0.9685,2.6855,1.9271],[0.5854,0.7079],0),
   a = toneA(ratio=8.0000,
             keyscale=[60,0,0],
             quotient=[8,0,0,0],
             pulse=[0.5000,0.6617,0.0000,0.0000],
             clkmix=0.0000,
             envpitch=0.0000,
             tremolo=0.0000),
   b = toneB(ratio1=1.0000,
             ratio2=1.0100,
             keyscale=[60,0,0],
             n1=[6,21,0,0],
             n2=[11,0.0000,-1],
             envpitch=0.0000,
             tremolo=0.5578),
   c = toneC(ratio=1.6540,
             keyscale=[60,0,0],
             fb=-1.0000,
             pulseFreq=[2.0000,1.0000,0.0000,0.0000],
             pwm=[0.5000,0.0000,0.0000,0.0000],
             inciteSelect=0.0000,
             envpitch=0.0000,
             tremolo=0.0000),
   noise = noise(lp=20000,hp=10,lag=0.0000,tremolo=0.1658),
   mix = mixer(mix=[1.4125,1.0000,0.5012,0.0000],
               pan=[+0.470,+0.680,-0.150,-0.110]),
   f1 = filter_(1,freq=15424,track=1.0000,res=0.1712,
                lfo=[0,0],
                env=[-9349,7357],
                external=0,
                pan=0.0000),
   f2 = filter_(2,freq=56,track=1.0000,res=0.0279,
                lfo=[0,0],
                env=[0,-1286],
                external=0,
                pan=0.0000))

m(7,"H",
   port=0.0000,amp=0.1122,
   lfo = lfo(vFreq=5.1280,vSens=0.0955,vDepth=0.0000,xPitch=0.0000,
             aRatio=0.2500,bRatio=1.0000,cRatio=0.7500,
             vDelay=0.0000,aDelay=2.0000,bDelay=4.0000,cDelay=0.0000,tLag=0.3154),
   enva = env("a",[1.8041,2.4055,3.3410,1.9378],[0.7667,0.8400],0),
   envb = env("b",[2.2719,3.3410,0.9266,2.6060],[0.5400,0.5299],0),
   envc = env("c",[4.0092,7.8848,5.0783,4.2097],[0.4333,0.9133],0),
   a = toneA(ratio=14.0000,
             keyscale=[60,0,0],
             quotient=[12,2,0,0],
             pulse=[0.5000,0.4000,0.0000,0.0000],
             clkmix=0.0000,
             envpitch=0.0000,
             tremolo=0.0000),
   b = toneB(ratio1=1.2500,
             ratio2=5.0000,
             keyscale=[60,0,0],
             n1=[8,3,0,0],
             n2=[29,0.3681,0],
             envpitch=0.0000,
             tremolo=0.2663),
   c = toneC(ratio=3.0000,
             keyscale=[60,0,0],
             fb=-1.0000,
             pulseFreq=[1.3330,0.3330,0.7500,0.0000],
             pwm=[0.0918,0.0063,0.0000,0.0000],
             inciteSelect=0.0402,
             envpitch=-1.0000,
             tremolo=0.0000),
   noise = noise(lp=20000,hp=10,lag=0.0000,tremolo=0.7387),
   mix = mixer(mix=[1.0000,1.0000,0.3548,0.7079],
               pan=[+0.370,-0.010,-0.860,-0.510]),
   f1 = filter_(1,freq=3070,track=1.0000,res=0.3869,
                lfo=[266,978],
                env=[2103,0],
                external=0,
                pan=0.0000),
   f2 = filter_(2,freq=242,track=0.0000,res=0.0503,
                lfo=[0,0],
                env=[578,0],
                external=0,
                pan=0.0000))

