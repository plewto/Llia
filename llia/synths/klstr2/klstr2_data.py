# llia.synths.Klstr2.Klstr2_data

from __future__ import print_function
from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance

from llia.synths.klstr2.klstr2_constants import *

prototype = {
    "amp" : 0.1,
    "lfoFreq" : 1.0,          # Modulation LFO
    "lfo2Ratio" : 1.0,        # Vibrato LFO
    "vibrato" : 0.0,
    "env1_attack" : 0.0,      # Modulation env
    "env1_decay1" : 0.0,
    "env1_decay2" : 0.0,
    "env1_release" : 0.0,   
    "env1_breakpoint" : 1.0,  
    "env1_sustain" : 1.0,
    "env1_mode" : 0,
    "env2_attack" : 0.0,      # Amplitude env
    "env2_decay1" : 0.0,
    "env2_decay2" : 0.0,
    "env2_release" : 0.0,
    "env2_breakpoint" : 1.0,
    "env2_sustain" : 1.0,
    "env2_mode" : 0,
    "spread" : 0.0,
    "spread_env1" : 0.0,
    "spread_lfo1" : 0.0,
    "spread_external" : 0.0,
    "cluster" : 0.0,
    "cluster_env1" : 0.0,
    "cluster_lfo1" : 0.0,
    "cluster_lfo2" : 0.0,
    "cluster_external" : 0.0,
    "pw" : 0.5,
    "pw_lfo1" : 0.0,
    "pw_env1" : 0.0,
    "harm1" : 4,
    "harm1_env1" : 0,
    "harm1_env2" : 0,
    "harm1_lfo1" : 0,
    "harm1_lfo2" : 0,
    "harm2" : 4,
    "harm2_env1" : 0,
    "harm2_lfo1" : 0,
    "harm2_external" : 0,
    "harm2_lag" : 0.0,
    "noise_lowpass" : 16000,
    "noise_lowpass_env1" : 0,
    "noise_lowpass_lfo1" : 0,
    "noise_highpass" : 10,
    "noise_amp" : 0.0,
    "balance_a" : 0.0,
    "balance_b" : 0.0,
    "balance_noise" : 0.0,
    "f1_freq" : 16000,
    "f1_freq_env1" : 0,
    "f1_freq_lfo1" : 0,
    "f1_freq_lfo2" : 0,
    "f1_freq_external" : 0,
    "f1_res" : 0.0,
    "f1_amp" : 1,
    "f1_pan" : 0.25,
    "f2_freq" : 1000,
    "f2_freq_env1" : 0,
    "f2_freq_lfo1" : 0,
    "f2_freq_lfo2" : 0,
    "f2_freq_lag" : 0.0,
    "f2_res" : 0.0,
    "f2_amp" : 1,
    "f2_pan" : -0.25}

class Klstr2(Program):

    def __init__(self,name):
        super(Klstr2,self).__init__(name,Klstr2,prototype)
        self.performance = performance()

program_bank = ProgramBank(Klstr2("Init"))
program_bank.enable_undo = False

def klstr2(slot, name, amp=0.1,
           lfo = {"freq": 1.0,                # LFO1 frequency (>0)
                  "ratio2" : 2.0,             # LFO2 freq ratio (see constants)
                  "vibrato" : 0.0},           # LFO2 -> vibrato (0..1)
           env1 = {"attack" : 0.0,            # Env1, modulation
                   "decay1" : 0.0,           
                   "decay2" : 0.0,
                   "breakpoint" : 1.0,
                   "sustain" : 1.0,
                   "release" : 0.0,
                   "mode" : 0},               # 0 -> gated, 1 -> trigger
           env2 = {"attack" : 0.0,            # Env2, amplitude envelope
                   "decay1" : 0.0,
                   "decay2" : 0.0,
                   "breakpoint" : 1.0,
                   "sustain" : 1.0,
                   "release" : 0.0,
                   "mode" : 0},
           spread = {"n" : 0.0,               # Frequency spread (0..1)
                     "env1" : 0.0,            # env1 -> spread (0..1)
                     "lfo1" : 0.0,            # lfo1 -> spread (0..1)
                     "external" : 0.0},       # external -> spread (0..1)
           cluster = {"n" : 0.0,              # Source signal mix, (0 <= n <= 4)
                      "env1" : 0.0,           # env1 -> cluster
                      "lfo1" : 0.0,           # lfo1 ->cluster
                      "lfo2" : 0.0,           # lfo2 -> cluster
                      "external" : 0.0},      # external -> cluster
           pw = {"pw" : 0.5,                  # Pulse width (0.0 <= pw <= 1.0)
                 "lfo1" : 0.0,                # lfo1 -> pw
                 "env1" : 0.0},               # env1 -> pw
           harm1 = {"n" : 8,                  # Tone 1 harmonic count (0 < n <= 64)
                    "env1" : 0,               
                    "env2" : 0,
                    "lfo1" : 0,
                    "lfo2" : 0},
           harm2 = {"n" : 8,                  # Tone 2 harmonic count 
                    "env1" : 0,
                    "lfo1" : 0,
                    "external" : 0,
                    "lag" : 0.0},             # Harmonics 2 lag time (0..1)
           noise_filter = {"lowpass" : 16000, # Noise lowpass filter cutoff
                           "env1" : 0,        # env1 -> lp filter
                           "lfo1" : 0,        # lfo1 -> lp filter
                           "highpass" : 10},  # static highpass filter cutoff
           mixer = {"noise" : 0.0,            # Noise gain (0..2)
                    "balance_a" : -0.75,      # Tone A path selection (-1..+1)
                    "balance_b" : 0.75,       # Tone B path selection (-1..+1)
                    "balance_noise" : 0.0,    # Noise filter selection (-1..+1)
                    "out2_lag" : 0.0},        # Main output 2 lag time (0..1)
           filter_1 = {"freq" : 16000,        # Filter 1 cutoff
                       "env1" : 0,            # env1 -> cutoff
                       "lfo1" : 0,            # lfo1 -> cutoff
                       "lfo2" : 0,            # lfo2 -> cutoff
                       "external" : 0,        # external -> cutoff
                       "res" : 0.0,           # resoance (0..1)
                       "mix" : 1.0,           # output amp (0..2)
                       "pan" : 0.75},         # output pan (-1..+1)
           filter_2 = {"freq" : 3000,         # Filter 2 freq
                       "env1" : 0,            # env1 -> freq
                       "lfo1" : 0,            # lfo1 -> freq
                       "lfo2" : 0,            # lfo2 -> freq
                       "lag"  : 0.0,          # freq lag time (0..1)
                       "res"  : 0.0,          # resoance (0..1)
                       "mix"  : 1.0,          # output amp (0..2)
                       "pan"  : -0.75}):      # output pan (-1..+1)
    p = Klstr2(name)
    
    def fval(d,param,key,dflt=None,minmax=(0.0, 1.0)):
        mn, mx = minmax
        dflt = dflt or mn
        v = min(mx,max(mn,d.get(key,dflt)))
        p[param] = float(v)

    def ival(d,param,key,dflt=0,minmax=(0,1)):
        mn, mx = minmax
        dflt = dflt or mn
        v = min(mx,max(mn,d.get(key,dflt)))
        p[param] = int(v)
        
    fval(lfo,"lfoFreq","freq", dflt=1.0,minmax=(0.001,100))
    fval(lfo,"lfo2Ratio","ratio2",dflt=2.0,minmax=(LFO_RATIOS[0], LFO_RATIOS[1]))
    fval(lfo,"vibrato","vibrato")
    fval(env1,"env1_attack","attack",minmax=(0,MAX_ENV_SEGMENT_TIME))
    fval(env1,"env1_decay1","decay1",minmax=(0,MAX_ENV_SEGMENT_TIME))
    fval(env1,"env1_decay2","decay2",minmax=(0,MAX_ENV_SEGMENT_TIME))
    fval(env1,"env1_release","release",minmax=(0,MAX_ENV_SEGMENT_TIME))
    fval(env1,"env1_breakpoint","breakpoint",1.0)
    fval(env1,"env1_sustain","sustain",1.0)
    ival(env1,"env1_mode","mode",0)
    fval(env2,"env2_attack","attack",minmax=(0,MAX_ENV_SEGMENT_TIME))
    fval(env2,"env2_decay1","decay1",minmax=(0,MAX_ENV_SEGMENT_TIME))
    fval(env2,"env2_decay2","decay2",minmax=(0,MAX_ENV_SEGMENT_TIME))
    fval(env2,"env2_release","release",minmax=(0,MAX_ENV_SEGMENT_TIME))
    fval(env2,"env2_breakpoint","breakpoint",1.0)
    fval(env2,"env2_sustain","sustain",1.0)
    ival(env2,"env2_mode","mode",0)
    fval(spread,"spread","n")
    fval(spread,"spread_env1","env1",minmax=(-1.0, 1.0))
    fval(spread,"spread_lfo1","lfo1")
    fval(spread,"spread_external","external",minmax=(-1.0, 1.0))
    fval(cluster,"cluster","n",minmax=CLUSTER_RANGE)
    fval(cluster,"cluster_env1","env1",minmax=CLUSTER_RANGE)
    fval(cluster,"cluster_lfo1","lfo1",minmax=CLUSTER_RANGE)
    fval(cluster,"cluster_lfo2","lfo2",minmax=CLUSTER_RANGE)
    fval(cluster,"cluster_external","external",minmax=CLUSTER_RANGE)
    fval(pw,"pw","pw",dflt=0.5)
    fval(pw,"pw_lfo1","lfo1")
    fval(pw,"pw_env1","env1")
    ival(harm1,"harm1","n",dflt=8,minmax=HARMONIC_COUNT_RANGE)
    ival(harm1,"harm1_env1","env1",dflt=0,minmax=HARMONIC_MOD_RANGE) 
    ival(harm1,"harm1_env2","env2",dflt=0,minmax=HARMONIC_MOD_RANGE)
    ival(harm1,"harm1_lfo1","lfo1",dflt=0,minmax=(0,HARMONIC_MOD_RANGE[1]))
    ival(harm1,"harm1_lfo2","lfo2",dflt=0,minmax=(0,HARMONIC_MOD_RANGE[1]))
    ival(harm2,"harm2","n",dflt=8,minmax=HARMONIC_COUNT_RANGE)
    ival(harm2,"harm2_env1","env1",dflt=0,minmax=HARMONIC_MOD_RANGE)
    ival(harm2,"harm2_lfo1","lfo1",dflt=0,minmax=(0,HARMONIC_MOD_RANGE[1]))
    ival(harm2,"harm2_external","external",dflt=0,minmax=HARMONIC_MOD_RANGE)
    fval(harm2,"harm2_lag","lag")
    ival(noise_filter,"noise_lowpass","lowpass",16000,minmax=LOWPASS_RANGE)
    ival(noise_filter,"noise_lowpass_env1","env1",minmax=FILTER_MOD_RANGE)
    ival(noise_filter,"noise_lowpass_lfo1","lfo1",0,minmax=FILTER_MOD_RANGE)
    ival(noise_filter,"noise_highpass","highpass",HIGHPASS_RANGE[0],HIGHPASS_RANGE)
    fval(mixer,"noise_amp","noise",0.0,minmax=(0.0, 2.0))
    fval(mixer,"balance_a","balance_a",-0.75,minmax=(-1.0,1.0))
    fval(mixer,"balance_b","balance_b",-0.75,minmax=(-1.0,1.0))
    fval(mixer,"balance_noise","balance_noise",-0.75,minmax=(-1.0,1.0))
    fval(mixer,"out2_lag","out2_lag")
    ival(filter_1,"f1_ferq","freq",16000,minmax=LOWPASS_RANGE)
    ival(filter_1,"f1_freq_env1","env1",0,minmax=FILTER_MOD_RANGE)
    ival(filter_1,"f1_freq_lfo1","lfo1",0,minmax=FILTER_MOD_RANGE)
    ival(filter_1,"f1_freq_lfo2","lfo2",0,minmax=FILTER_MOD_RANGE)
    ival(filter_1,"f1_freq_external","external",0,minmax=FILTER_MOD_RANGE)
    fval(filter_1,"f1_res","res")
    fval(filter_1,"f1_amp","amp",0.5,minmax=(0.0, 2.0))
    fval(filter_1,"f1_pan","pan",-0.75,minmax=(-1.0,1.0))
    ival(filter_2,"f2_ferq","freq",16000,minmax=LOWPASS_RANGE)
    ival(filter_2,"f2_freq_env1","env1",0,minmax=FILTER_MOD_RANGE)
    ival(filter_2,"f2_freq_lfo1","lfo1",0,minmax=FILTER_MOD_RANGE)
    ival(filter_2,"f2_freq_lfo2","lfo2",0,minmax=FILTER_MOD_RANGE)
    fval(filter_2,"f2_freq_lag","lag")
    fval(filter_2,"f2_res","res")
    fval(filter_2,"f2_amp","amp",0.5,minmax=(0.0, 2.0))
    fval(filter_2,"f2_pan","pan",-0.75,minmax=(-1.0,1.0))
    program_bank[slot] = p
    return p

klstr2(0,"Init")
