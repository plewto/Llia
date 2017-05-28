# llia.synths.Siris.Siris_data

from __future__ import print_function
from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance

prototype = {
    "port" : 0.0,                # portamento time 0..1
    "amp" : 1.0,                 # main linear amp
    "timebase" : 1.0,            # common LFO frequenciy >0
    "vratio" : 7.0,              # vibrato LFO freq ratio
    "vsens" : 0.1,               # vibrato sensitivity 0..1
    "vdepth" : 0.0,              # vibrato depth 0..1
    "vdelay" : 0.0,              # vibrato onset delay 0..2
    "env_attack" : 0.01,         # attack time
    "env_decay" : 0.1,           #
    "env_sustain" : 1.0,         #
    "env_release" : 3.0,         #
    "env_mode" : 0,              # 0=gate, 1=trig
    "ex_lfo_ratio" : 1,          # relative ex LFO frequency
    "ex_env_attack" : 0.001,
    "ex_env_decay" : 3.000,
    "ex1_harmonic" : 1,          # int 1,2,3,...
    "ex1_harmonic_lfo" : 0,      # exLFO -> harmonic
    "ex1_harmonic_env" : 0,      # exEnv -> harmonic
    "ex1_pw" : 0.5,              # pulse width 0..1
    "ex1_pwm_lfo" : 0,           # exLFO -> pw
    "ex1_pwm_env" : 0,           # exEnv -> pw
    "ex1_amp" : 0,               # ex1 -> main out amp
    "ex2_harmonic" : 1,          # int 1,2,3,...
    "ex2_harmonic_lfo" : 0,      # exLFO -> harmonic
    "ex2_harmonic_env" : 0,      # exEnv -> harmonic
    "ex2_pw" : 0.5,              # pulse width 0..1
    "ex2_pwm_lfo" : 0,           # exLFO -> pw
    "ex2_pwm_env" : 0,           # exEnv -> pw
    "ex2_amp" : 0,               # ex2 -> main out amp
    "ks1_excite1" : 1.0,         # excite1 pulse -> ks1
    "ks1_excite2" : 0.0,         # excite2 pulse -> ks1
    "ks1_excite_noise" : 0.0,    # noise -> ks1 excite pulse
    "ks1_excite_white" : 1,      # 0=pink 1=white (only applies if ks1_exite_noise is non-zero)
    "ks1_ratio" : 1.0,           # Tuning
    "ks1_decay" : 3,             #
    "ks1_coef" : 0.3,            # ks feedback coeficienat 0..1
    "ks1_trig_mode" : 0,         # 0=gate, 1=trem, 2=continuous
    "ks1_trig_ratio" : 1,        # trig LFO frequency relative to timebase.
    "ks1_clip_enable" : 0,       # 0=disable, 1=enable
    "ks1_clip_gain" : 1,         # pre-clipler gain
    "ks1_clip_threshold" : 1,    # >0..1
    "ks1_attack" : 0.0,          #
    "ks1_velocity" : 0.0,        # velocity -> ks1 amp
    "ks1_amp" : 1.0,             # linear amp
    "ks2_delay" : 0.0,           # trigger delay in seconds
    "ks2_excite1" : 0.0,         # excite1 pulse -> ks2
    "ks2_excite2" : 1.0,         # excite2 pulse -> ks2
    "ks2_excite_noise" : 0.0,    # noise -> ks2 excite pulse
    "ks2_excite_white" : 1,      # 0=pink 1=white (only applies if ks2_exite_noise is non-zero)
    "ks2_ratio" : 1.0,           # Tuning
    "ks2_decay" : 3,             #
    "ks2_coef" : 0.3,            # ks feedback coeficienat 0..1
    "ks2_trig_mode" : 0,         # 0=gate, 1=trem, 2=continuous
    "ks2_trig_ratio" : 1,        # trig LFO frequency relative to timebase.
    "ks2_clip_enable" : 0,       # 0=disable, 1=enable
    "ks2_clip_gain" : 1,         # pre-clipler gain
    "ks2_clip_threshold" : 1,    # >0..1
    "ks2_attack" : 0.0,          #
    "ks2_velocity" : 0.0,        # velocity -> ks2 amp
    "ks2_amp" : 1.0,             # linear amp
    "nse_attack" : 0.01,
    "nse_decay" : 3.0,           #
    "nse_velocity" :0.0,         # velocity -> noise amp
    "nse_lowpass" : 20000,       # Hz
    "nse_highpass" : 20,         # Hz
    "nse_amp" : 0,               # linear amp
    "filter_cutoff" : 16000,     # Hz
    "filter_env" : 0,            # ADSR env -> cutoff, Hz
    "filter_vlfo" : 0,           # vibrato LFO -> cutoff, Hz
    "filter_velocity" : 0,       # velocity -> cutoff
    "filter_track" : 0,          # key freq -> cutoff
    "filter_res" : 0}

class Siris(Program):

    def __init__(self,name):
        super(Siris,self).__init__(name,Siris,prototype)
        self.performance = performance()

program_bank = ProgramBank(Siris("Init"))

def vibrato(timebase=1.0, vratio=7.0, vsens=0.1, vdepth=0.0, vdelay=0.0):
    return {"timebase" : float(timebase),
            "vratio" : float(vratio),
            "vsens" : float(vsens),
            "vdepth" : float(vdepth),
            "vdelay" : float(vdelay)}

def adsr(a=0.01, d=0.01, s=1.0, r=3.0, mode=0):
    return {"env_attack" : float(a),
            "env_decay" : float(d),
            "env_sustain" : float(s),
            "env_release" : float(r),
            "env_mode" : int(mode)}

def excite(n, harmonic=1, harmonic_lfo=0, harmonic_env=0,
           pw=0.5, pwm_lfo=0.0, pwm_env=0.0):
    def param(suffix):
        return "ex%d_%s" % (n,suffix)
    return {param("harmonic") : float(harmonic),
            param("harmonic_lfo") : float(harmonic_lfo),
            param("harmonic_env") : float(harmonic_env),
            param("pw") : float(pw),
            param("pwm_lfo") : float(pwm_lfo),
            param("pwm_env") : float(pwm_env)}

def ks_excite(n, ex1=1.0, ex2=0.0, noise=0.0, white=1):
    def param(suffix):
        return "ks%d_%s" % (n, suffix)
    return {param("excite1") : float(ex1),
            param("excite2") : float(ex2),
            param("excite_noise") : float(noise),
            param("excite_white") : int(white)}

def ks_trig(n, mode=0, lfo_ratio=1):
    def param(suffix):
        return "ks%d_%s" % (n,suffix)
    return {param("trig_mode") : int(mode),
            param("trig_ratio") : float(lfo_ratio)}

def ks(n, ratio=1.0, attack=0.01, decay=3.0, coef=0.3, 
       velocity=0.0, amp=1.0, delay=0.0):
    def param(suffix):
        return "ks%d_%s" % (n,suffix)
    rs = {param("ratio") : float(ratio),
          param("attack") : float(attack),
          param("decay") : float(decay),
          param("coef") : float(coef),
          param("velocity") : float(velocity),
          param("amp") : float(amp)}
    if n==2:
        rs["ks2_delay"] = float(delay)
    return rs

def clip(n, enable=0, gain=1, threshold=1):
    def param(suffix):
        return "ks%d_clip_%s" % (n,suffix)
    return {param("enable") : int(enable),
            param("gain") : float(gain),
            param("threshold") : float(threshold)}

def noise(attack=0.01, decay=3.0, lowpass=20000, highpass=20,
          velocity=0.0, amp=0.0):
    return {"nse_attack" : float(attack),
            "nse_decay" : float(decay),
            "nse_lowpass" : int(lowpass),
            "nse_highpass" : int(highpass),
            "nse_velocity" : float(velocity),
            "nse_amp" : float(amp)}

def filter(cutoff=16000, track= 0, env=0, vlfo=0, velocity=0, res=0.0):
    return {"filter_cutoff" : int(cutoff),
            "filter_env" : int(env),
            "filter_vlfo" : int(vlfo),
            "filter_velocity" : int(velocity),
            "filter_track" : float(track),
            "filter_res" : float(res)}

def siris(slot, name, amp=0.1, port=0.0,
          vibrato = vibrato(),
          adsr = adsr(),
          ex_lfo = 1.0,         # excite LFO freq ratio
          ex_attack = 0.01,     # excite env attack/decay
          ex_decay = 3.0,
          excite1 = excite(1),
          excite2 = excite(2, harmonic=2),
          ks1_excite = ks_excite(1),
          ks1_trig = ks_trig(1, mode=0, lfo_ratio=1),
          ks1 = ks(1),
          clip1 = clip(1),
          ks2_excite = ks_excite(2,ex1=0.0, ex2=1.0),
          ks2_trig = ks_trig(2, mode=0, lfo_ratio=1),
          ks2 = ks(2),
          clip2 = clip(2),
          noise = noise(),
          filter=filter()):
    p = Siris(name)
    p["amp"] = float(amp)
    p["port"] = float(port)
    p["ex_lfo_ratio"] = float(ex_lfo)
    p["ex_env_attack"] = float(ex_attack)
    p["ex_env_decay"] = float(ex_decay)
    p.update(vibrato)
    p.update(adsr)
    p.update(excite1)
    p.update(excite2)
    p.update(ks1_excite)
    p.update(ks1_trig)
    p.update(ks1)
    p.update(clip1)
    p.update(ks2_excite)
    p.update(ks2_trig)
    p.update(ks2)
    p.update(clip2)
    p.update(noise)
    p.update(filter)
    program_bank[slot] = p
    return p

siris(0,"Init")
