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

def noise(attack=0.01, decay=3.0,lowpass=20000, highpass=20,
          ex1_amp = 0.0, ex2_amp = 0.0,velocity=0.0, amp=0.0):
    return {"nse_attack" : float(attack),
            "nse_decay" : float(decay),
            "nse_lowpass" : int(lowpass),
            "nse_highpass" : int(highpass),
            "nse_velocity" : float(velocity),
            "ex1_amp" : float(ex1_amp),
            "ex2_amp" : float(ex2_amp),
            "nse_amp" : float(amp)}

def filter(cutoff=16000, track=0, env=0, vlfo=0, velocity=0, res=0.0):
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

siris(0, "Zero",amp=0.3548,port=0.0000,
      vibrato=vibrato(timebase=6.5810,vratio=1.0000,vsens=0.0000,
                      vdepth=0.0000,vdelay=1.6281),
      adsr=adsr(a=4.0,d=0.01,s=1.0,r=3.0,mode=0),
      ex_lfo=0.066,
      ex_attack=0.005,
      ex_decay=0.153,
      excite1=excite(1,harmonic=4,harmonic_lfo=3,harmonic_env=-2,
                     pw=0.6000,pwm_lfo=0.2000,pwm_env=0.0000),
      ks1_excite=ks_excite(1,ex1=1.0000,ex2=0.0000,noise=0.0000,white=1),
      ks1_trig=ks_trig(1,mode=1,lfo_ratio=3.0000),
      ks1=ks(1,ratio=0.750,attack=0.001,decay=0.202,coef=0.494,
             velocity=0.000,amp=1.000),
      clip1=clip(1,enable=0,gain=1.000,threshold=1.000),
      excite2=excite(2,harmonic=1,harmonic_lfo=0,harmonic_env=0,
                     pw=0.7000,pwm_lfo=0.0000,pwm_env=0.0000),
      ks2_excite=ks_excite(2,ex1=0.0000,ex2=1.0000,noise=0.3618,white=1),
      ks2_trig=ks_trig(2,mode=0,lfo_ratio=2.0000),
      ks2=ks(2,ratio=2.000,attack=0.002,decay=2.341,coef=0.076,
             velocity=0.000,amp=0.316,delay=0.073),
      clip2=clip(2,enable=0,gain=3.300,threshold=0.342),
      noise=noise(attack=0.005,decay=0.929,lowpass=16000,highpass=100,
                  ex1_amp=0.000,ex2_amp=0.000,velocity=0.854,amp=0.000),
      filter=filter(cutoff=4000,track=0.000,env=-2611,vlfo=0,velocity=0,res=0.422))

siris(1, "One",amp=0.2818,port=0.0804,
      vibrato=vibrato(timebase=3.7840,vratio=1.0000,vsens=0.0000,
                      vdepth=0.5302,vdelay=1.0355),
      adsr=adsr(a=4.0,d=0.01,s=1.0,r=3.0,mode=0),
      ex_lfo=0.200,
      ex_attack=0.003,
      ex_decay=7.039,
      excite1=excite(1,harmonic=4,harmonic_lfo=0,harmonic_env=0,
                     pw=0.5000,pwm_lfo=0.1000,pwm_env=0.5000),
      ks1_excite=ks_excite(1,ex1=1.0000,ex2=0.8894,noise=0.0000,white=1),
      ks1_trig=ks_trig(1,mode=1,lfo_ratio=0.5000),
      ks1=ks(1,ratio=2.000,attack=1.185,decay=0.327,coef=0.237,
             velocity=0.000,amp=1.000),
      clip1=clip(1,enable=0,gain=1.000,threshold=0.166),
      excite2=excite(2,harmonic=5,harmonic_lfo=0,harmonic_env=0,
                     pw=0.4000,pwm_lfo=0.0000,pwm_env=0.0000),
      ks2_excite=ks_excite(2,ex1=0.0000,ex2=1.0000,noise=0.0000,white=1),
      ks2_trig=ks_trig(2,mode=0,lfo_ratio=12.0000),
      ks2=ks(2,ratio=3.000,attack=0.000,decay=0.256,coef=0.261,
             velocity=0.000,amp=1.000,delay=0.000),
      clip2=clip(2,enable=1,gain=1.000,threshold=1.000),
      noise=noise(attack=0.003,decay=3.340,lowpass=8000,highpass=100,
                  ex1_amp=0.794,ex2_amp=0.282,velocity=0.261,amp=0.000),
      filter=filter(cutoff=600,track=0.000,env=0,vlfo=494,velocity=2497,res=0.462))

siris(2, "Two",amp=0.1122,port=0.0000,
      vibrato=vibrato(timebase=3.6990,vratio=1.0000,vsens=0.0000,
                      vdepth=0.2859,vdelay=1.5257),
      adsr=adsr(a=8.0,d=0.01,s=1.0,r=3.0,mode=0),
      ex_lfo=0.333,
      ex_attack=0.003,
      ex_decay=3.757,
      excite1=excite(1,harmonic=1,harmonic_lfo=0,harmonic_env=0,
                     pw=0.6000,pwm_lfo=0.3000,pwm_env=0.0000),
      ks1_excite=ks_excite(1,ex1=1.0000,ex2=1.0000,noise=0.5829,white=1),
      ks1_trig=ks_trig(1,mode=2,lfo_ratio=9.0000),
      ks1=ks(1,ratio=6.000,attack=0.001,decay=4.517,coef=0.385,
             velocity=0.000,amp=1.000),
      clip1=clip(1,enable=0,gain=1.000,threshold=0.668),
      excite2=excite(2,harmonic=4,harmonic_lfo=0,harmonic_env=0,
                     pw=0.6000,pwm_lfo=0.1000,pwm_env=0.0000),
      ks2_excite=ks_excite(2,ex1=0.0000,ex2=1.0000,noise=0.0000,white=1),
      ks2_trig=ks_trig(2,mode=1,lfo_ratio=4.0000),
      ks2=ks(2,ratio=4.000,attack=0.002,decay=1.619,coef=0.252,
             velocity=0.000,amp=1.000,delay=0.000),
      clip2=clip(2,enable=1,gain=3.050,threshold=1.000),
      noise=noise(attack=0.002,decay=6.481,lowpass=16000,highpass=100,
                  ex1_amp=0.891,ex2_amp=0.000,velocity=0.347,amp=0.000),
      filter=filter(cutoff=10000,track=0.000,env=0,vlfo=0,velocity=0,res=0.452))

siris(3, "Three",amp=0.0562,port=0.0000,
      vibrato=vibrato(timebase=5.9840,vratio=1.0000,vsens=0.0000,
                      vdepth=0.0804,vdelay=1.5100),
      adsr=adsr(a=0.405,d=0.00999999999998,s=1.0,r=5.2488,mode=0),
      ex_lfo=0.333,
      ex_attack=0.762,
      ex_decay=1.331,
      excite1=excite(1,harmonic=1,harmonic_lfo=0,harmonic_env=0,
                     pw=0.2000,pwm_lfo=0.0000,pwm_env=0.0000),
      ks1_excite=ks_excite(1,ex1=0.0000,ex2=0.0000,noise=1.0000,white=1),
      ks1_trig=ks_trig(1,mode=2,lfo_ratio=1.0000),
      ks1=ks(1,ratio=4.038,attack=0.080,decay=3.432,coef=0.133,
             velocity=0.000,amp=0.708),
      clip1=clip(1,enable=0,gain=1.000,threshold=1.000),
      excite2=excite(2,harmonic=2,harmonic_lfo=1,harmonic_env=0,
                     pw=0.2000,pwm_lfo=0.0000,pwm_env=0.0000),
      ks2_excite=ks_excite(2,ex1=0.0000,ex2=0.0000,noise=0.9095,white=0),
      ks2_trig=ks_trig(2,mode=2,lfo_ratio=6.0000),
      ks2=ks(2,ratio=2.000,attack=1.526,decay=3.380,coef=0.071,
             velocity=0.000,amp=0.562,delay=0.064),
      clip2=clip(2,enable=0,gain=1.000,threshold=0.915),
      noise=noise(attack=0.001,decay=0.977,lowpass=16000,highpass=8000,
                  ex1_amp=0.000,ex2_amp=0.000,velocity=0.764,amp=0.000),
      filter=filter(cutoff=685,track=0.000,env=6353,vlfo=0,velocity=0,res=0.302))

siris(4, "Four",amp=0.0708,port=0.1960,
      vibrato=vibrato(timebase=7.4580,vratio=1.0000,vsens=0.0000,
                      vdepth=0.0201,vdelay=0.0000),
      adsr=adsr(a=2.0,d=0.01,s=1.0,r=3.0,mode=0),
      ex_lfo=0.200,
      ex_attack=0.005,
      ex_decay=1.627,
      excite1=excite(1,harmonic=3,harmonic_lfo=0,harmonic_env=0,
                     pw=0.3000,pwm_lfo=0.0000,pwm_env=0.0000),
      ks1_excite=ks_excite(1,ex1=1.0000,ex2=0.0000,noise=0.0352,white=0),
      ks1_trig=ks_trig(1,mode=1,lfo_ratio=15.0000),
      ks1=ks(1,ratio=0.500,attack=0.003,decay=1.131,coef=0.347,
             velocity=0.000,amp=0.040),
      clip1=clip(1,enable=0,gain=1.000,threshold=1.000),
      excite2=excite(2,harmonic=2,harmonic_lfo=1,harmonic_env=0,
                     pw=0.4000,pwm_lfo=0.0000,pwm_env=0.1000),
      ks2_excite=ks_excite(2,ex1=1.0000,ex2=1.0000,noise=0.0000,white=1),
      ks2_trig=ks_trig(2,mode=2,lfo_ratio=3.0000),
      ks2=ks(2,ratio=1.000,attack=0.386,decay=1.483,coef=0.480,
             velocity=0.769,amp=0.708,delay=0.000),
      clip2=clip(2,enable=0,gain=1.500,threshold=1.000),
      noise=noise(attack=0.004,decay=0.815,lowpass=16000,highpass=100,
                  ex1_amp=0.000,ex2_amp=0.018,velocity=0.965,amp=0.000),
      filter=filter(cutoff=2000,track=0.000,env=207,vlfo=0,velocity=0,res=0.864))

siris(5, "Five",amp=0.1778,port=0.0000,
      vibrato=vibrato(timebase=7.9750,vratio=1.0000,vsens=0.0917,
                      vdepth=0.2419,vdelay=0.6485),
      adsr=adsr(a=2.0,d=0.01,s=1.0,r=3.0,mode=0),
      ex_lfo=0.333,
      ex_attack=0.212,
      ex_decay=1.400,
      excite1=excite(1,harmonic=3,harmonic_lfo=0,harmonic_env=1,
                     pw=0.4000,pwm_lfo=0.0000,pwm_env=0.0000),
      ks1_excite=ks_excite(1,ex1=1.0000,ex2=0.0000,noise=0.6834,white=0),
      ks1_trig=ks_trig(1,mode=1,lfo_ratio=3.0000),
      ks1=ks(1,ratio=1.500,attack=0.002,decay=0.594,coef=0.447,
             velocity=0.000,amp=1.000),
      clip1=clip(1,enable=0,gain=1.000,threshold=0.060),
      excite2=excite(2,harmonic=1,harmonic_lfo=0,harmonic_env=0,
                     pw=0.5000,pwm_lfo=0.1000,pwm_env=0.2000),
      ks2_excite=ks_excite(2,ex1=1.0000,ex2=1.0000,noise=0.0000,white=1),
      ks2_trig=ks_trig(2,mode=2,lfo_ratio=0.5000),
      ks2=ks(2,ratio=2.590,attack=0.003,decay=0.034,coef=0.085,
             velocity=0.000,amp=0.251,delay=0.000),
      clip2=clip(2,enable=0,gain=1.000,threshold=1.000),
      noise=noise(attack=0.002,decay=1.701,lowpass=16000,highpass=100,
                  ex1_amp=0.000,ex2_amp=0.000,velocity=0.970,amp=0.000),
      filter=filter(cutoff=4000,track=0.500,env=-2361,vlfo=0,velocity=0,res=0.387))

siris(6, "Six",amp=0.2239,port=0.0000,
      vibrato=vibrato(timebase=7.1300,vratio=1.0000,vsens=0.0000,
                      vdepth=0.0000,vdelay=1.6500),
      adsr=adsr(a=0.0,d=0.01,s=1.0,r=3.0,mode=0),
      ex_lfo=0.250,
      ex_attack=0.950,
      ex_decay=0.231,
      excite1=excite(1,harmonic=4,harmonic_lfo=0,harmonic_env=0,
                     pw=0.6000,pwm_lfo=0.0000,pwm_env=0.2000),
      ks1_excite=ks_excite(1,ex1=1.0000,ex2=0.0000,noise=0.1206,white=1),
      ks1_trig=ks_trig(1,mode=0,lfo_ratio=9.0000),
      ks1=ks(1,ratio=1.000,attack=0.000,decay=7.373,coef=0.081,
             velocity=0.000,amp=1.000),
      clip1=clip(1,enable=0,gain=1.000,threshold=1.000),
      excite2=excite(2,harmonic=3,harmonic_lfo=0,harmonic_env=0,
                     pw=0.6000,pwm_lfo=0.0000,pwm_env=0.0000),
      ks2_excite=ks_excite(2,ex1=0.0000,ex2=1.0000,noise=0.0000,white=1),
      ks2_trig=ks_trig(2,mode=0,lfo_ratio=1.0000),
      ks2=ks(2,ratio=1.500,attack=0.001,decay=0.055,coef=0.309,
             velocity=0.935,amp=0.562,delay=0.079),
      clip2=clip(2,enable=1,gain=3.350,threshold=0.417),
      noise=noise(attack=0.326,decay=0.073,lowpass=16000,highpass=1000,
                  ex1_amp=0.000,ex2_amp=0.000,velocity=0.050,amp=0.000),
      filter=filter(cutoff=137,track=0.000,env=2315,vlfo=0,velocity=5030,res=0.724))

siris(7, "Seven",amp=0.3162,port=0.0000,
      vibrato=vibrato(timebase=5.5210,vratio=1.0000,vsens=0.1000,
                      vdepth=0.0804,vdelay=0.0000),
      adsr=adsr(a=0.0,d=0.01,s=1.0,r=3.0,mode=0),
      ex_lfo=0.200,
      ex_attack=0.000,
      ex_decay=2.398,
      excite1=excite(1,harmonic=3,harmonic_lfo=0,harmonic_env=2,
                     pw=0.8000,pwm_lfo=0.0000,pwm_env=0.0000),
      ks1_excite=ks_excite(1,ex1=1.0000,ex2=0.9397,noise=0.0000,white=1),
      ks1_trig=ks_trig(1,mode=0,lfo_ratio=1.0000),
      ks1=ks(1,ratio=3.000,attack=0.000,decay=5.936,coef=0.214,
             velocity=0.191,amp=1.000),
      clip1=clip(1,enable=1,gain=1.575,threshold=0.950),
      excite2=excite(2,harmonic=1,harmonic_lfo=0,harmonic_env=0,
                     pw=0.6000,pwm_lfo=0.0000,pwm_env=0.0000),
      ks2_excite=ks_excite(2,ex1=0.7387,ex2=1.0000,noise=0.9347,white=1),
      ks2_trig=ks_trig(2,mode=0,lfo_ratio=2.0000),
      ks2=ks(2,ratio=5.017,attack=0.001,decay=5.184,coef=0.081,
             velocity=0.965,amp=0.562,delay=0.098),
      clip2=clip(2,enable=0,gain=1.000,threshold=1.000),
      noise=noise(attack=0.003,decay=0.106,lowpass=2755,highpass=883,
                  ex1_amp=0.000,ex2_amp=0.000,velocity=0.261,amp=0.000),
      filter=filter(cutoff=16000,track=0.000,env=0,vlfo=0,velocity=0,res=0.382))

siris(8, "Eight",amp=0.3162,port=0.0000,
      vibrato=vibrato(timebase=3.3700,vratio=1.0000,vsens=0.0000,
                      vdepth=0.0000,vdelay=0.0000),
      adsr=adsr(a=0.0,d=0.01,s=1.0,r=3.0,mode=0),
      ex_lfo=0.250,
      ex_attack=0.001,
      ex_decay=0.218,
      excite1=excite(1,harmonic=5,harmonic_lfo=0,harmonic_env=1,
                     pw=0.5000,pwm_lfo=0.0000,pwm_env=0.0000),
      ks1_excite=ks_excite(1,ex1=1.0000,ex2=0.9749,noise=0.0000,white=1),
      ks1_trig=ks_trig(1,mode=2,lfo_ratio=2.0000),
      ks1=ks(1,ratio=1.000,attack=0.001,decay=0.235,coef=0.323,
             velocity=0.000,amp=0.355),
      clip1=clip(1,enable=0,gain=1.000,threshold=0.397),
      excite2=excite(2,harmonic=1,harmonic_lfo=0,harmonic_env=5,
                     pw=0.2000,pwm_lfo=0.0000,pwm_env=0.8000),
      ks2_excite=ks_excite(2,ex1=0.0000,ex2=1.0000,noise=0.2613,white=1),
      ks2_trig=ks_trig(2,mode=0,lfo_ratio=1.0000),
      ks2=ks(2,ratio=5.000,attack=0.003,decay=8.000,coef=0.000,
             velocity=0.000,amp=1.000,delay=0.000),
      clip2=clip(2,enable=0,gain=0.260,threshold=1.000),
      noise=noise(attack=0.002,decay=1.173,lowpass=16000,highpass=1000,
                  ex1_amp=0.000,ex2_amp=0.000,velocity=0.643,amp=0.000),
      filter=filter(cutoff=2185,track=0.000,env=4496,vlfo=0,velocity=0,res=0.327))

siris(9, "Nine",amp=0.3981,port=0.0000,
      vibrato=vibrato(timebase=3.3700,vratio=2.0000,vsens=0.0272,
                      vdepth=0.4020,vdelay=0.9100),
      adsr=adsr(a=0.4608,d=0.01,s=1.0,r=3.0,mode=0),
      ex_lfo=0.010,
      ex_attack=0.001,
      ex_decay=0.218,
      excite1=excite(1,harmonic=5,harmonic_lfo=1,harmonic_env=1,
                     pw=0.5000,pwm_lfo=0.0000,pwm_env=0.0000),
      ks1_excite=ks_excite(1,ex1=1.0000,ex2=0.9749,noise=0.0000,white=0),
      ks1_trig=ks_trig(1,mode=2,lfo_ratio=2.0000),
      ks1=ks(1,ratio=1.000,attack=1.125,decay=2.247,coef=0.090,
             velocity=0.000,amp=0.355),
      clip1=clip(1,enable=0,gain=1.000,threshold=0.397),
      excite2=excite(2,harmonic=4,harmonic_lfo=2,harmonic_env=5,
                     pw=0.2000,pwm_lfo=0.0000,pwm_env=0.8000),
      ks2_excite=ks_excite(2,ex1=0.0000,ex2=1.0000,noise=0.0000,white=0),
      ks2_trig=ks_trig(2,mode=2,lfo_ratio=1.0000),
      ks2=ks(2,ratio=1.500,attack=0.980,decay=8.000,coef=0.380,
             velocity=0.000,amp=0.316,delay=0.057),
      clip2=clip(2,enable=0,gain=0.260,threshold=1.000),
      noise=noise(attack=0.002,decay=1.173,lowpass=16000,highpass=1000,
                  ex1_amp=0.007,ex2_amp=0.000,velocity=0.643,amp=0.000),
      filter=filter(cutoff=7592,track=0.000,env=-4496,vlfo=1062,velocity=0,res=0.327))

siris(10, "Ten",amp=0.2818,port=0.0000,
      vibrato=vibrato(timebase=1.0000,vratio=7.0000,vsens=0.0090,
                      vdepth=0.1558,vdelay=0.0000),
      adsr=adsr(a=0.01,d=0.1,s=1.0,r=3.0,mode=0),
      ex_lfo=0.060,
      ex_attack=0.001,
      ex_decay=3.000,
      excite1=excite(1,harmonic=1,harmonic_lfo=1,harmonic_env=0,
                     pw=0.5000,pwm_lfo=0.5000,pwm_env=0.0000),
      ks1_excite=ks_excite(1,ex1=1.0000,ex2=0.0000,noise=0.0000,white=1),
      ks1_trig=ks_trig(1,mode=1,lfo_ratio=4.0000),
      ks1=ks(1,ratio=1.000,attack=0.000,decay=3.000,coef=0.299,
             velocity=0.000,amp=1.000),
      clip1=clip(1,enable=0,gain=1.000,threshold=1.000),
      excite2=excite(2,harmonic=1,harmonic_lfo=0,harmonic_env=0,
                     pw=0.5000,pwm_lfo=0.0000,pwm_env=0.0000),
      ks2_excite=ks_excite(2,ex1=0.0000,ex2=1.0000,noise=0.5176,white=0),
      ks2_trig=ks_trig(2,mode=1,lfo_ratio=2.0000),
      ks2=ks(2,ratio=3.000,attack=0.000,decay=5.249,coef=0.128,
             velocity=0.000,amp=1.000,delay=0.000),
      clip2=clip(2,enable=1,gain=2.400,threshold=1.000),
      noise=noise(attack=0.010,decay=3.000,lowpass=20000,highpass=20,
                  ex1_amp=0.000,ex2_amp=0.000,velocity=0.000,amp=0.000),
      filter=filter(cutoff=16000,track=0.000,env=0,vlfo=746,velocity=0,res=0.000))

siris(11, "Eleven",amp=0.1413,port=0.0000,
      vibrato=vibrato(timebase=0.4000,vratio=7.0000,vsens=0.0000,
                      vdepth=0.3467,vdelay=1.1600),
      adsr=adsr(a=0.01,d=0.1,s=1.0,r=3.0,mode=0),
      ex_lfo=0.040,
      ex_attack=0.001,
      ex_decay=3.000,
      excite1=excite(1,harmonic=3,harmonic_lfo=1,harmonic_env=0,
                     pw=0.5000,pwm_lfo=0.5000,pwm_env=0.0000),
      ks1_excite=ks_excite(1,ex1=1.0000,ex2=0.0000,noise=0.0000,white=1),
      ks1_trig=ks_trig(1,mode=1,lfo_ratio=6.0000),
      ks1=ks(1,ratio=0.010,attack=0.000,decay=3.000,coef=0.128,
             velocity=0.000,amp=1.000),
      clip1=clip(1,enable=1,gain=3.100,threshold=1.000),
      excite2=excite(2,harmonic=2,harmonic_lfo=0,harmonic_env=0,
                     pw=0.5000,pwm_lfo=0.0000,pwm_env=0.0000),
      ks2_excite=ks_excite(2,ex1=0.0000,ex2=1.0000,noise=0.5176,white=0),
      ks2_trig=ks_trig(2,mode=1,lfo_ratio=4.0000),
      ks2=ks(2,ratio=0.500,attack=0.000,decay=5.249,coef=0.128,
             velocity=0.000,amp=1.000,delay=0.000),
      clip2=clip(2,enable=1,gain=2.400,threshold=1.000),
      noise=noise(attack=0.010,decay=3.000,lowpass=20000,highpass=20,
                  ex1_amp=0.000,ex2_amp=0.000,velocity=0.000,amp=0.000),
      filter=filter(cutoff=8821,track=0.000,env=1661,vlfo=0,velocity=0,res=0.000))

siris(12, "Twelve",amp=0.3162,port=0.0000,
      vibrato=vibrato(timebase=1.0000,vratio=7.0000,vsens=0.1000,
                      vdepth=0.0000,vdelay=0.0000),
      adsr=adsr(a=0.01,d=0.1,s=1.0,r=3.0,mode=0),
      ex_lfo=1.000,
      ex_attack=0.001,
      ex_decay=3.000,
      excite1=excite(1,harmonic=1,harmonic_lfo=0,harmonic_env=0,
                     pw=0.4000,pwm_lfo=0.0000,pwm_env=0.0000),
      ks1_excite=ks_excite(1,ex1=0.0000,ex2=0.0000,noise=0.8191,white=0),
      ks1_trig=ks_trig(1,mode=0,lfo_ratio=1.0000),
      ks1=ks(1,ratio=1.000,attack=0.000,decay=7.144,coef=0.185,
             velocity=0.000,amp=1.000),
      clip1=clip(1,enable=0,gain=1.150,threshold=0.925),
      excite2=excite(2,harmonic=1,harmonic_lfo=0,harmonic_env=0,
                     pw=0.3000,pwm_lfo=0.2000,pwm_env=0.0000),
      ks2_excite=ks_excite(2,ex1=0.0000,ex2=1.0000,noise=0.0000,white=1),
      ks2_trig=ks_trig(2,mode=0,lfo_ratio=1.0000),
      ks2=ks(2,ratio=0.505,attack=0.673,decay=4.993,coef=0.195,
             velocity=0.000,amp=1.000,delay=0.030),
      clip2=clip(2,enable=1,gain=1.425,threshold=1.000),
      noise=noise(attack=0.010,decay=3.000,lowpass=20000,highpass=20,
                  ex1_amp=0.000,ex2_amp=0.000,velocity=0.000,amp=0.000),
      filter=filter(cutoff=4394,track=1.840,env=0,vlfo=0,velocity=2735,res=0.111))
