# llia.synths.saw3.s3_data
# 2016.06.05

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.util.lmath import clip, db_to_amp
from llia.performance_edit import performance, smap, ccmap

prototype = {
    "outbus"          : 0     , # Main output bus number.
    "amp"             : 0.1   , # Main linear amplitude.
    "port"            : 0.0   , # Portamento time.
    "env1Attack"      : 0.0   , # 
    "env1Decay"       : 0.0   , # 
    "env1Sustain"     : 1.0   , # 
    "env1Release"     : 0.0   , # 
    "env2Attack"      : 0.0   , # 
    "env2Decay"       : 0.0   , # 
    "env2Sustain"     : 1.0   , # 
    "env2Release"     : 0.0   , # 
    "vfreq"           : 5.0   , # Vibrato frequency in Hertz.
    "vsens"           : 0.1   , # Vibrato sensitivity.
    "vdelay"          : 0.0   , # Vibrato onset delay in seconds.
    "vdepth"          : 0.0   , # Programmed vibrato depth.
    "vibrato"         : 0.0   , # Manual vibrato depth.
    "lfoFreq"         : 5.0   , # LFO frequency in Hertz.
    "lfoDelay"        : 0.0   , # LFO onset delay in seconds 
    "lfoDepth"        : 1.0   , # LFO output amplitude.
    
    "osc1Freq"        : 0.5   , # OSC1 frequency ratio.
    "osc1Wave"        : 0.5   , # OSC1 waveshape, [0.0,1.0].
    "osc1Wave_env1"   : 0.0   , # OSC1 waveshape mod by env1.
    "osc1Wave_lfo"    : 0.0   , # OSC1 waveshape mod by lfo.
    "osc1Amp"         : 1.0   , # OSC1 linear amplitude.
    "osc1Amp_env1"    : 0.0   , # OSC1 amplitude mod by env1.
    
    "osc2Freq"        : 1.0   , # OSC2 frequency ratio.
    "osc2Wave"        : 0.5   , # OSC2 pulse width [0.0, 1.0].
    "osc2Wave_env1"   : 0.0   , # OSC2 PWM from env1.
    "osc2Wave_lfo"    : 0.0   , # OSC2 PWM from lfo.
    "osc2Amp"         : 1.0   , # OSC2 linear amplitude.
    "osc2Amp_env1"    : 0.0   , # OSC2 amplitude mod by env1.
    
    "osc3Freq"        : 0.5   , # OSC3 frequency ratio.
    "osc3Bias"        : 0     , # OSC3 frequency bias in Hertz.
    "osc3Wave"        : 0.5   , # OSC3 sync frequency [0.0, 1.0].
    "osc3Wave_env1"   : 0.0   , # OSC3 sync freq mod by env1.
    "osc3Wave_lfo"    : 0.0   , # OSC3 sync freq mod by lfo.
    "osc3WaveLag"     : 0.0   , # OSC3 sync freq mod lag time >= 0.
    "osc3Amp"         : 1.0   , # OSC3 linear amplitude.
    "osc3Amp_env1"    : 0.0   , # OSC3 amplitude mod by env1.
    
    "noiseFreq"       : 1.0   , # Noise filter frequency ratio.
    "noiseBW"         : 0.5   , # Noise filter width [0.0, 1.0].
    "noiseAmp"        : 0.0   , # Noise linear amplitude.
    "noiseAmp_env1"   : 0.0   , # Noise amplitude mod by env1.
    
    "filterFreq"      : 10000 , # Filter frequency in Hertz.
    "filterKeytrack"  : 0     , # Filter keyboard track (ratio)
    "filterFreq_env1" : 0     , # Filter freq mod by env1 in Hertz.
    "filterFreq_lfo"  : 0     , # Filter freq mod by lfo in Hertz.
    "filterRes"       : 0.0   , # Filter resonance, [0.0, 1.0].
    "filterRes_env1"  : 0.0   , # Resonance mod by env1.
    "filterRes_lfo"   : 0.0   , # Resonance mod by lfo.
    
    "filterMix"       : 0.0   , # Filter mode mix [-1=lowpass, +1=bandpass].
    "filterMix_lfo"   : 0.0   , # Filter mix mod by lfo.
    "filterMix_env1"  : 0.0   , # Filter mix mod by env1.
    
    "bandpassOffset"  : 1.0   , # Bandpass filter frequency offset (ratio)
    "bandpassLag"     : 0.0   , # Bandpass frequency mod lag time.
}

class Saw3(Program):

    def __init__(self, name):
        super(Saw3, self).__init__(name, "Saw3", prototype)

program_bank = ProgramBank(Saw3("Init"))
program_bank.enable_undo = False

def nclip(v):
    return float(clip(v, 0.0, 1.0))

def pclip(v):
    return float(clip(v, -1.0, 1.0))

def vibrato (freq, delay=0.0, depth=0.0, sens=0.1):
    return {"vfreq" : float(clip(freq, 0.001, 15)),
            "vsens" : nclip(sens),
            "vdelay" : abs(float(delay)),
            "vdepth" : nclip(depth),
            "vibrato" : 0}

def _adsr(prefix,a,d,s,r):
    def fkey(param):
        return "env%d%s" % (prefix, param)
    return {fkey("Attack") : float(max(a, 0)),
            fkey("Decay") : float(max(d, 0)),
            fkey("Release") : float(max(r, 0)),
            fkey("Sustain") : nclip(s)}

def adsr1(a,d,s,r):
    return _adsr(1, a, d, s, r)

def adsr2(a,d,s,r):
    return _adsr(2,a,d,s,r)

def lfo(freq, delay=0.0, depth=1.0):
    return {"lfoFreq" : float(clip(freq, 0.001, 15)),
            "lfoDelay" : float(min(abs(delay), 8)),
            "lfoDepth" : nclip(depth)}

def osc1(freq, wave=0.5, env1=0.0, lfo=0.0):
    return {"osc1Freq" : float(max(freq, 0.125)),
            "osc1Wave" : nclip(wave),
            "osc1Wave_env1" : pclip(env1),
            "osc1Wave_lfo" : pclip(lfo)}

def osc2(freq, wave=0.5, env1=0.0, lfo=0.0):
    return {"osc2Freq" : float(max(freq, 0.125)),
            "osc2Wave" : nclip(wave),
            "osc2Wave_env1" : pclip(env1),
            "osc2Wave_lfo" : pclip(lfo)}

def osc3(freq, bias=0, wave=0.0, env1=0.0, lfo=0.0, lag=0.0): 
    return {"osc3Freq" : float(max(freq, 0)),
            "osc3Bias" : float(bias),
            "osc3Wave" : nclip(wave),
            "osc3Wave_env1" : pclip(env1),
            "osc3Wave_lfo" : pclip(lfo),
            "osc3WaveLag" : float(max(lag, 0))}

def noise(freq, bw=0.1):
    return {"noiseFreq" : float(clip(freq, 0.125, 16)),
            "noiseBW" : nclip(bw)}

def mix(osc1=0, osc2=0, osc3=0, noise=-99,
          osc1Env1 = 0.0, osc2Env1 = 0.0, osc3Env1 = 0.0, noiseEnv1 = 0.0):
    return {"osc1Amp" : db_to_amp(osc1),
            "osc2Amp" : db_to_amp(osc2),
            "osc3Amp" : db_to_amp(osc3),
            "noiseAmp" : db_to_amp(noise),
            "osc1Amp_env1" : nclip(osc1Env1),
            "osc2Amp_env1" : nclip(osc2Env1),
            "osc3Amp_env1" : nclip(osc3Env1),
            "noiseAmp_env1" : nclip(osc3Env1)}

def filter_(freq=10000, keytrack=0.0, env1=0.0, lfo=0.0, bpoffset = 1.0, bplag=0.0):
    return {"filterFreq" : float(clip(freq, 0, 12000)),
            "filterKeytrack" : float(clip(keytrack, 0, 4)),
            "filterFreq_env1" : float(clip(env1, -12000, 12000)),
            "filterFreq_lfo" : float(clip(lfo, -12000, 12000)),
            "bandpassOffset" : float(clip(bpoffset, 1, 16)),
            "bandpassLag" : float(max(bplag, 0))}

def res(n, env1=0.0, lfo=0.0):
    return {"filterRes" : nclip(n),
            "filterRes_env1" : pclip(env1),
            "filterRes_lfo" : pclip(lfo)}

def filter_mix(n, env1=0.0, lfo=0.0):
    return {"filterMix" : pclip(n),
            "filterMix_env1" : pclip(env1),
            "filterMix_lfo" : pclip(lfo)}

def saw3(slot, name,
         amp = -12,
         vibrato = vibrato(5.0),
         lfo = lfo(5.0),
         env1 = adsr1(0.0, 0.0, 1.0, 0.0),
         env2 = adsr2(0.0, 0.0, 1.0, 0.0),
         osc1 = osc1(0.5),
         osc2 = osc2(1.0),
         osc3 = osc3(0.5),
         noise = noise(1.0),
         mixer = mix(),
         filter_ = filter_(),
         res = res(0.5),
         filter_mix = filter_mix(0),
         port = 0.0):
    acc = {"amp" : db_to_amp(amp),
           "port" : float(max(port, 0))}
    acc.update(vibrato)
    acc.update(env1)
    acc.update(env2)
    acc.update(lfo)
    acc.update(osc1)
    acc.update(osc2)
    acc.update(osc3)
    acc.update(noise)
    acc.update(mixer)
    acc.update(filter_)
    acc.update(res)
    acc.update(filter_mix)
    p = Saw3(name)
    for k,v in acc.items():
        p[k] = v
    p.performance = performance()
    program_bank[slot] = p
    return p



         
saw3(0, "Alpha",  -12,
     vibrato(5.000, delay=0.000, depth=0.000, sens=0.100),
     lfo(5.000, delay=0.000, depth=1.000),
     adsr1(0.000, 0.000, 1.000, 0.000),
     adsr2(0.000, 0.000, 1.000, 0.000),
     osc1(1.000, wave=0.500, env1=0.000, lfo=0.000),
     osc2(0.500, wave=0.500, env1=0.000, lfo=0.000),
     osc3(0.500, wave=0.000, env1=0.000, lfo=0.000, lag=0.000, bias=0),
     noise(2.000, bw=0.5),
     mix(osc1  =   0, osc1Env1=0.000,
         osc2  =   0, osc2Env1=0.000,
         osc3  =   0, osc3Env1=0.000,
         noise = -99, noiseEnv1=0.000),
     filter_(10000, keytrack=0, env1=0.000, lfo=0.000,
             bpoffset=1.000, bplag=0.000),
     res(0.000, env1=0.000, lfo=0.000),
     filter_mix(0.000, env1=0.000, lfo=0.000),
     port = 0.000)

saw3(1, "Beta",  -12,
     vibrato(5.000, delay=0.000, depth=0.000, sens=0.100),
     lfo(1.000, delay=1.000, depth=1.000),
     adsr1(2.000, 0.000, 1.000, 2.000),
     adsr2(0.000, 0.000, 1.000, 2.000),
     osc1(1.000, wave=1.000, env1=-1.000, lfo=0.000),
     osc2(1.500, wave=0.050, env1=0.800, lfo=0.000),
     osc3(2.250, wave=0.500, env1=0.000, lfo=0.300, lag=0.000, bias=0),
     noise(2.000, bw=0.5),
     mix(osc1  =   0, osc1Env1=0.000,
         osc2  =   0, osc2Env1=0.000,
         osc3  =   0, osc3Env1=0.000,
         noise = -99, noiseEnv1=0.000),
     filter_(100, keytrack=0, env1=10000, lfo=0.000,
             bpoffset=4.000, bplag=1.000),
     res(0.700, env1=0.000, lfo=0.000),

     filter_mix(0.000, env1=0.000, lfo=0.000),

     port = 0.000)
     
         
saw3(  2, "Gamma", -12,
     vibrato(5.000, delay=0.000, depth=0.000, sens=0.100),
     lfo(4.000, delay=1.000, depth=1.000),
     adsr1(2.000,0.000,1.000,2.000),
     adsr2(0.000,0.000,1.000,2.000),
     osc1(1.000, wave=1.000, env1=-1.000, lfo=0.000),
     osc2(1.100, wave=0.050, env1=0.800, lfo=0.300),
     osc3(1.500, wave=0.500, env1=0.000, lfo=0.000, lag=0.000, bias=0.000000),
     noise(2.000, bw=0.500),
     filter_(100, keytrack=0, env1=10000, lfo=0, bpoffset=4.000, bplag=1.000),
     res(0.700, env1=0.000, lfo=0.000),
     filter_mix(0.000, env1=0.000, lfo=0.000),
     port = 0.000)   
         

    
