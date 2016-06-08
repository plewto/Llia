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
        osc1Env1 = 0.0, 
        osc2Env1 = 0.0, 
        osc3Env1 = 0.0, 
        noiseEnv1 = 0.0):
    return {"osc1Amp" : db_to_amp(osc1),
            "osc2Amp" : db_to_amp(osc2),
            "osc3Amp" : db_to_amp(osc3),
            "noiseAmp" : db_to_amp(noise),
            "osc1Amp_env1" : nclip(osc1Env1),
            "osc2Amp_env1" : nclip(osc2Env1),
            "osc3Amp_env1" : nclip(osc3Env1),
            "noiseAmp_env1" : nclip(noiseEnv1)}

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

saw3(  0, "FatGate", -12,
     vibrato(5.659, delay=1.240, depth=0.100, sens=0.05),
     lfo(0.050, delay=0.000, depth=1.000),
     adsr1(1.000,0.000,1.000,0.000),
     adsr2(0.000,0.000,1.000,0.000),
     osc1(0.500, wave=1.000, env1=-1.00, lfo=0.000),
     osc2(1.000, wave=0.500, env1=0.000, lfo=0.300),
     osc3(1.010, wave=0.000, env1=0.000, lfo=0.000, lag=1.690, bias=0),
     noise(4.000, bw=0.407),
     mix(osc1 =   +0, osc1Env1=0.000,
         osc2 =   +0, osc2Env1=0.000,
         osc3 =   +0, osc3Env1=0.000,
         noise = -99, noiseEnv1=0.000),
     filter_(5000, keytrack=1, env1=5000 , lfo=0, bpoffset=4.000, bplag=0.000),
     res(0.500, env1=0.000, lfo=0.000),
     filter_mix(0.111, env1=0.000, lfo=0.000),
     port = 0.000)


saw3(  1, "Slow5", -12,
     vibrato(5.659, delay=1.240, depth=0.100, sens=0.05),
     lfo(0.050, delay=0.000, depth=1.000),
     adsr1(1.500,0.000,1.000,0.500),
     adsr2(0.010,0.100,0.850,1.000),
     osc1(0.500, wave=1.000, env1=-1.00, lfo=0.000),
     osc2(1.500, wave=0.050, env1=0.850, lfo=0.100),
     osc3(1.000, wave=0.000, env1=0.000, lfo=0.000, lag=1.690, bias=0),
     noise(4.000, bw=0.407),
     mix(osc1 =   +0, osc1Env1=0.000,
         osc2 =  -99, osc2Env1=0.700,
         osc3 =   +0, osc3Env1=0.000,
         noise = -99, noiseEnv1=0.000),
     filter_(5000, keytrack=0, env1=5000 , lfo=0, bpoffset=4.000, bplag=2.000),
     res(0.500, env1=0.000, lfo=0.000),
     filter_mix(-1.000, env1=1.000, lfo=0.000),
     port = 0.000)

saw3(  2, "Stack5", -12,
     vibrato(5.659, delay=1.240, depth=0.100, sens=0.05),
     lfo(3.050, delay=2.000, depth=1.000),
     adsr1(1.500,0.000,1.000,3.500),
     adsr2(0.010,0.100,0.850,4.500),
     osc1(2.250, wave=0.000, env1=0.000, lfo=0.000),
     osc2(1.500, wave=0.500, env1=0.000, lfo=0.300),
     osc3(1.000, wave=0.000, env1=0.100, lfo=0.300, lag=1.690, bias=0),
     noise(3.375 , bw=0.1),
     mix(osc1 =   +0, osc1Env1=0.000,
         osc2 =   +0, osc2Env1=0.000,
         osc3 =   +0, osc3Env1=0.000,
         noise = -15, noiseEnv1=0.100),
     filter_(0000, keytrack=1, env1=8000 , lfo=0, bpoffset=2.000, bplag=2.000),
     res(0.500, env1=0.000, lfo=0.000),
     filter_mix(-1.000, env1=1.000, lfo=0.100),
     port = 0.000)

saw3(  3, "FatTuseday", -12,
     vibrato(5.00, delay=1.240, depth=0.100, sens=0.05),
     lfo(3.750, delay=0.000, depth=1.000),
     adsr1(0.750,2.000,0.500,0.500),
     adsr2(0.000,0.100,0.850,0.500),
     osc1(1.010, wave=0.000, env1=0.000, lfo=0.000),
     osc2(0.990, wave=0.500, env1=0.000, lfo=0.200),
     osc3(0.500, wave=0.000, env1=0.000, lfo=0.000, lag=1.690, bias=0),
     noise(1.00 , bw=0.1),
     mix(osc1 =   +0, osc1Env1=0.000,
         osc2 =   +0, osc2Env1=0.000,
         osc3 =   +0, osc3Env1=0.000,
         noise = -99, noiseEnv1=0.000),
     filter_(10000, keytrack=1, env1=0, lfo=0, bpoffset=1.000, bplag=2.000),
     res(0.500, env1=0.000, lfo=0.000),
     filter_mix(-1.000, env1=0.000, lfo=0.000),
     port = 0.000)

saw3(  4, "ColdWaterFlat", -12,
     vibrato(5.00, delay=1.240, depth=0.100, sens=0.05),
     lfo(0.010, delay=2.000, depth=1.000),
     adsr1(3.000,2.000,0.500,4.500),
     adsr2(2.000,0.700,0.850,4.500),
     osc1(2.000, wave=0.000, env1=1.000, lfo=0.000),
     osc2(1.000, wave=0.100, env1=0.900, lfo=0.000),
     osc3(0.500, wave=0.000, env1=0.400, lfo=0.000, lag=2.000, bias=0),
     noise(1.00 , bw=0.1),
     mix(osc1 =   +0, osc1Env1=0.000,
         osc2 =   +0, osc2Env1=-0.33,
         osc3 =  -99, osc3Env1=0.300,
         noise = -99, noiseEnv1=0.000),
     filter_(100, keytrack=0, env1=7000, lfo=0, bpoffset=3.000, bplag=2.000),
     res(0.800, env1=-0.400, lfo=0.000),
     filter_mix(1.000, env1=-2.000, lfo=0.000),
     port = 0.000)

saw3(  5, "SaltFlats", -15,
     vibrato(6.741, delay=2.776, depth=0.000, sens=0.100),
     lfo(0.230, delay=3.800, depth=1.000),
     adsr1(0.131,0.475,0.758,2.235),
     adsr2(1.338,0.126,0.911,2.419),
     osc1(2.380, wave=0.376, env1=0.000, lfo=0.000),
     osc2(1.000, wave=0.500, env1=-0.975, lfo=0.000),
     osc3(1.000, wave=0.120, env1=0.942, lfo=0.000, lag=1.046, bias=0.000000),
     noise(4.000, bw=0.511),
     mix(osc1 =   0, osc1Env1=0.000,
         osc2 =  -3, osc2Env1=0.000,
         osc3 =  -3, osc3Env1=0.000,
         noise = -12, noiseEnv1=0.000),
     filter_(688, keytrack=0, env1=7629, lfo=6194, bpoffset=2.000, bplag=0.513),
     res(0.532, env1=0.000, lfo=0.000),
     filter_mix(-0.676, env1=0.000, lfo=0.000),
     port = 0.000)

saw3(  6, "FauxEcho", -18,
     vibrato(4.096, delay=2.870, depth=0.000, sens=0.100),
     lfo(1.639, delay=0.000, depth=1.000),
     adsr1(0.179,0.287,0.974,2.766),
     adsr2(0.011,0.171,0.760,2.097),
     osc1(1.000, wave=0.630, env1=-0.325, lfo=0.141),
     osc2(0.500, wave=0.500, env1=0.434, lfo=0.000),
     osc3(0.996, wave=0.500, env1=-0.124, lfo=0.864, lag=1.677, bias=0.000000),
     noise(6.000, bw=0.244),
     mix(osc1 = -12, osc1Env1=0.000,
         osc2 =  -3, osc2Env1=1.000,
         osc3 =  -3, osc3Env1=1.000,
         noise =  +0, noiseEnv1=1.000),
     filter_(872, keytrack=0, env1=6803, lfo=6822, bpoffset=4.000, bplag=0.000),
     res(0.651, env1=0.000, lfo=0.000),
     filter_mix(0.898, env1=0.000, lfo=0.000),
     port = 0.000)


saw3(   7, "SlowPad", -12,
     vibrato(6.961, delay=0.916, depth=0.000, sens=0.100),
     lfo(0.283, delay=0.421, depth=1.000),
     adsr1(3.420,0.932,0.990,6.425),
     adsr2(6.348,6.894,0.751,6.527),
     osc1(0.500, wave=0.500, env1=-0.357, lfo=0.786),
     osc2(0.500, wave=0.500, env1=0.688, lfo=0.000),
     osc3(1.989, wave=0.500, env1=0.000, lfo=0.000, lag=1.085, bias=0.000000),
     noise(2.000, bw=0.338),
     mix(osc1 =  +0, osc1Env1=0.000,
         osc2 =  -3, osc2Env1=0.000,
         osc3 =  +0, osc3Env1=0.000,
         noise = -96, noiseEnv1=0.000),
     filter_(9272, keytrack=0, env1=-3937, lfo=0, bpoffset=6.000, bplag=0.632),
     res(0.074, env1=0.545, lfo=0.000),
     filter_mix(-0.344, env1=-1.000, lfo=0.000),
     port = 0.000)


saw3(   8, "Epsilon", -12,
     vibrato(6.356, delay=2.778, depth=0.000, sens=0.100),
     lfo(9.535, delay=2.000, depth=0.750),
     adsr1(2.549,1.834,0.766,0.517),
     adsr2(1.489,0.109,0.788,2.069),
     osc1(2.000, wave=0.500, env1=0.000, lfo=0.000),
     osc2(1.000, wave=0.500, env1=0.000, lfo=0.525),
     osc3(1.000, wave=0.428, env1=0.000, lfo=0.000, lag=0.841, bias=2.000000),
     noise(2.000, bw=0.627),
     mix(osc1 =  -9, osc1Env1=0.000,
         osc2 =  +0, osc2Env1=0.000,
         osc3 =  +0, osc3Env1=0.000,
         noise = -93, noiseEnv1=0.000),
     filter_(2184, keytrack=0, env1=0, lfo=0, bpoffset=4.000, bplag=0.903),
     res(0.372, env1=0.000, lfo=-1.000),
     filter_mix(-0.232, env1=0.000, lfo=0.010),
     port = 0.000)

saw3(  9, "Query", -9,
     vibrato(5.150, delay=3.810, depth=0.000, sens=0.100),
     lfo(2.182, delay=3.712, depth=0.500),
     adsr1(0.469,0.536,0.914,1.680),
     adsr2(0.259,0.248,0.822,1.908),
     osc1(1.000, wave=0.938, env1=-0.877, lfo=0.770),
     osc2(0.990, wave=0.101, env1=-0.897, lfo=0.015),
     osc3(2.000, wave=0.500, env1=0.000, lfo=0.956, lag=0.646, bias=0.000000),
     noise(4.000, bw=0.890),
     mix(osc1 =  +0, osc1Env1=0.000,
         osc2 = -15, osc2Env1=0.000,
         osc3 =  -3, osc3Env1=0.000,
         noise = -99, noiseEnv1=0.000),
     filter_(40, keytrack=1, env1=1714, lfo=0, bpoffset=2.000, bplag=0.000),
     res(0.305, env1=0.063, lfo=0.000),
     filter_mix(-0.923, env1=1.000, lfo=0.000),
     port = 0.162)

saw3( 10, "GhostWalk", -12,
     vibrato(4.956, delay=2.861, depth=0.000, sens=0.100),
     lfo(1.239, delay=0.000, depth=1.000),
     adsr1(0.169,0.162,0.122,4.104),
     adsr2(1.144,0.146,0.994,4.321),
     osc1(1.000, wave=0.500, env1=0.000, lfo=0.456),
     osc2(0.500, wave=0.070, env1=0.000, lfo=0.000),
     osc3(0.496, wave=0.500, env1=0.067, lfo=0.213, lag=0.774, bias=0.000000),
     noise(6.000, bw=0.721),
     mix(osc1 =  +0, osc1Env1=0.000,
         osc2 =  -9, osc2Env1=0.000,
         osc3 = -18, osc3Env1=0.000,
         noise =  +0, noiseEnv1=0.000),
     filter_(184, keytrack=1, env1=2602, lfo=0, bpoffset=3.000, bplag=0.000),
     res(0.898, env1=0.000, lfo=0.000),
     filter_mix(0.511, env1=0.000, lfo=0.000),
     port = 0.510)

saw3( 11, "RedOut", -12,
     vibrato(7.894, delay=2.933, depth=0.000, sens=0.100),
     lfo(0.050, delay=1.292, depth=0.800),
     adsr1(0.039,0.914,0.933,0.528),
     adsr2(0.029,0.456,0.993,0.065),
     osc1(1.000, wave=0.500, env1=0.000, lfo=0.734),
     osc2(0.500, wave=0.500, env1=0.203, lfo=0.200),
     osc3(0.505, wave=0.449, env1=0.000, lfo=0.100, lag=1.213, bias=0.000000),
     noise(1.000, bw=0.857),
     mix(osc1 =  -3, osc1Env1=0.000,
         osc2 =  +0, osc2Env1=0.000,
         osc3 =  -6, osc3Env1=0.000,
         noise = -96, noiseEnv1=0.000),
     filter_(463, keytrack=0, env1=1888, lfo=4963, bpoffset=6.000, bplag=0.000),
     res(0.608, env1=0.000, lfo=0.300),
     filter_mix(0.674, env1=-1.000, lfo=0.000),
     port = 0.000)


saw3( 12, "BazFnk", -9,
     vibrato(6.695, delay=1.060, depth=0.000, sens=0.300),
     lfo(0.300, delay=0.000, depth=1.000),
     adsr1(0.101,0.780,0.806,0.263),
     adsr2(0.053,0.482,0.851,0.350),
     osc1(0.250, wave=0.500, env1=0.000, lfo=0.121),
     osc2(1.000, wave=0.236, env1=-0.048, lfo=0.000),
     osc3(0.250, wave=0.500, env1=-0.236, lfo=0.000, lag=1.101, bias=0.000000),
     noise(3.000, bw=0.661),
     mix(osc1 =  +0, osc1Env1=0.000,
         osc2 = -24, osc2Env1=0.000,
         osc3 = -24, osc3Env1=0.000,
         noise = -99, noiseEnv1=0.000),
     filter_(156, keytrack=1, env1=0, lfo=0, bpoffset=6.000, bplag=0.000),
     res(0.268, env1=0.757, lfo=0.000),
     filter_mix(-0.150, env1=-1.000, lfo=0.000),
     port = 0.000)

saw3( 13, "237", -15,
     vibrato(7.382, delay=2.174, depth=0.552, sens=0.100),
     lfo(3.691, delay=1.000, depth=1.000),
     adsr1(0.584,0.854,0.823,0.270),
     adsr2(0.618,0.199,0.968,0.721),
     osc1(0.500, wave=0.500, env1=-0.411, lfo=0.644),
     osc2(0.502, wave=0.225, env1=0.000, lfo=0.884),
     osc3(1.000, wave=0.500, env1=0.000, lfo=0.274, lag=1.064, bias=0.000000),
     noise(4.000, bw=0.044),
     mix(osc1 =  +0, osc1Env1=0.000,
         osc2 = -21, osc2Env1=0.000,
         osc3 = -21, osc3Env1=0.000,
         noise =  -9, noiseEnv1=0.000),
     filter_(893, keytrack=0, env1=4694, lfo=100, bpoffset=1.000, bplag=0.204),
     res(0.600, env1=0.3, lfo=0.200),
     filter_mix(-0.731, env1=0.000, lfo=0.300),
     port = 0.000)

saw3( 14, "LfoSync", -12,
     vibrato(0.459, delay=2.903, depth=0.000, sens=0.100),
     lfo(0.076, delay=0.410, depth=1.000),
     adsr1(0.024,0.290,0.971,0.913),
     adsr2(0.559,0.138,0.837,0.303),
     osc1(2.000, wave=0.500, env1=-0.825, lfo=0.140),
     osc2(1.000, wave=0.794, env1=0.000, lfo=0.000),
     osc3(1.000, wave=0.500, env1=-0.884, lfo=0.613, lag=1.078, bias=0.000000),
     noise(1.000, bw=0.085),
     mix(osc1 =  -9, osc1Env1=0.000,
         osc2 = -15, osc2Env1=0.000,
         osc3 =  +0, osc3Env1=0.000,
         noise = -99, noiseEnv1=0.000),
     filter_(241, keytrack=1, env1=0, lfo=0, bpoffset=3.000, bplag=0.000),
     res(0.858, env1=0.000, lfo=0.000),
     filter_mix(-0.177, env1=0.000, lfo=0.646),
     port = 0.000)

saw3( 15, "Vole", -12,
     vibrato(3.178, delay=1.647, depth=0.000, sens=0.100),
     lfo(0.024, delay=0.000, depth=1.000),
     adsr1(2.619,3.567,0.963,0.447),
     adsr2(1.602,2.653,0.807,2.342),
     osc1(2.292, wave=0.500, env1=0.195, lfo=0.000),
     osc2(1.141, wave=0.500, env1=0.288, lfo=0.362),
     osc3(1.549, wave=0.500, env1=-0.947, lfo=0.000, lag=1.472, bias=0.000000),
     noise(4.000, bw=0.521),
     mix(osc1 =  +0, osc1Env1=0.000,
         osc2 = -12, osc2Env1=0.000,
         osc3 =  +0, osc3Env1=0.000,
         noise = -96, noiseEnv1=0.000),
     filter_(648, keytrack=0, env1=9698, lfo=0, bpoffset=4.000, bplag=0.050),
     res(0.113, env1=0.000, lfo=0.000),
     filter_mix(0.003, env1=0.000, lfo=0.000),
     port = 0.994)

saw3( 16, "Narco", -12,
     vibrato(6.129, delay=3.354, depth=0.000, sens=0.100),
     lfo(0.135, delay=3.328, depth=1.000),
     adsr1(0.949,0.111,0.994,0.520),
     adsr2(0.603,0.487,0.833,0.587),
     osc1(0.500, wave=0.500, env1=0.390, lfo=0.358),
     osc2(0.500, wave=0.433, env1=0.000, lfo=0.000),
     osc3(1.203, wave=0.500, env1=0.591, lfo=0.000, lag=1.039, bias=0.000000),
     noise(2.000, bw=0.815),
     mix(osc1 =  -6, osc1Env1=0.000,
         osc2 = -12, osc2Env1=0.000,
         osc3 =  +0, osc3Env1=0.000,
         noise = -93, noiseEnv1=0.000),
     filter_(601, keytrack=0, env1=6116, lfo=0, bpoffset=1.000, bplag=0.000),
     res(0.447, env1=0.000, lfo=0.400),
     filter_mix(-0.169, env1=0.000, lfo=0.854),
     port = 0.000)

saw3( 17, "Zolpram", -12,
     vibrato(4.765, delay=2.024, depth=0.000, sens=0.383),
     lfo(0.655, delay=1.386, depth=1.000),
     adsr1(0.096,0.054,0.796,0.075),
     adsr2(0.091,0.047,0.754,0.435),
     osc1(0.250, wave=0.500, env1=0.931, lfo=0.000),
     osc2(0.252, wave=0.445, env1=0.000, lfo=0.000),
     osc3(0.992, wave=0.752, env1=0.000, lfo=0.581, lag=1.406, bias=1.000000),
     noise(4.000, bw=0.495),
     mix(osc1 =  +0, osc1Env1=0.000,
         osc2 = -15, osc2Env1=0.000,
         osc3 =  -9, osc3Env1=0.000,
         noise = -96, noiseEnv1=0.000),
     filter_(6412, keytrack=0, env1=5489, lfo=5660, bpoffset=6.000, bplag=0.000),
     res(0.421, env1=0.000, lfo=0.000),
     filter_mix(-0.940, env1=1.000, lfo=0.000),
     port = 0.000)
