# llia.synths.Slug.Slug_data

from __future__ import print_function
from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance
from llia.synths.slug.slug_constants import *

prototype = {
    "port" : 0.00,                  # Portemento 0..1
    "velocity_port" : 0.00,         # Velocity to port time
    "break_key" : 60,               # MIDI key number
    "amp" : 0.333,                  # Main amplitude
    "vfreq" : 5.00,                 # Vibrato frequency
    "vdelay" : 0.00,                # Vibrato onset delay 0..2
    "vsens" : 0.1,                  # Vibrato sensitivity 0..1
    "vdepth" : 0.00,                # Vibrato depth 0..1 (programmed)
    "vibrato" : 0.00,               # Vibrato depth 0..1
    "vnoise" : 0.00,                # Vibrato low freq noise amp 0..1 (noise always delayed)
    "xpitch" : 0.00,                # xbus -> pitch 0..1
    "env_mode" : 0,                 # Common envelope mode. 0:gate, 1=trig.
    "env1_attack" : 0.01,           # 0..4
    "env1_decay" : 0.10,            # 0..4
    "env1_sustain" : 1.00,          # 0..1
    "env1_release" : 0.01,          # 0..4
    "env1_velocity_attack":0,       # velocity --> attack -1 .. +1
    "env1_key_attack" : 0.00,       # keynumber --> attack -1 .. +1
    "penv1_decay" : 1.00,           # Percussive envelope 1 decay 0..4
    "env2_attack" : 0.01,
    "env2_decay" : 0.10,
    "env2_sustain" : 1.00,
    "env2_release" : 0.01,
    "env2_velocity_attack" : 0,
    "env2_key_attack" : 0,
    "penv2_decay" : 1.00,
    "pulse_ratio" : 1.00,           # >0 (tune)
    "pulse_width" : 0.5,            # 0..1
    "pulse_width_env1" : 0.00,      # 0..1
    "pulse_width_lfo" : 0.00,       # 0..1
    "pulse_filter_res" : 0.5,       # 0..1
    "pulse_filter_cutoff" : 16000,  # Hz
    "pulse_filter_env1" : 0,        # -+ Hz.
    "pulse_filter_penv1" : 0,       # -+ Hz.
    "pulse_filter_lfo" : 0,         # -+ Hz.
    "pulse_filter_x" : 0,           # -+ Hz. external -> filter
    "pulse_filter_velocity" : 0,    # -+ Hz
    "pulse_filter_left_track" : 0,  # -+ Hz (per octave)
    "pulse_filter_right_track" : 0, # -+ Hz (per octave)
    "pulse_amp_env" : 1.00,         # cross mix env2 and penv2,  0=env2, 1=penv2
    "pulse_amp" : 1.00,             # 0..2
    "pulse_pan" : 0.5,
    "pluck_ratio" : 1.00,           # >0 (tune)
    "pluck_decay" : 3.00,           # >0
    "pluck_harmonic" : 1,           # (1,2,3,...,16?)
    "pluck_width" : 1,              # 0|1  0=50%  1=75%
    "pluck_excite" : 0.0,           # Excitation signal 0=pulse, 1=white noise
    "pluck_damp" : 0.5,             # 0..1
    "pluck_velocity" : 0.00,        # 0..1 velocity -> pluck amp
    "pluck_left_scale" : 0,         # left key scale in db/oct
    "pluck_right_scale" : 0,        # right key scale in db/oct
    "pluck_amp" : 1.00,             # 0..2
    "pluck_pan" : 0.5,
    "car1_ratio" : 0.5,             # 0 <= ratio <= 16
    "car1_bias" : 0,                # 0 <= bias <= 999  in Hz.
    "car1_velocity" : 0.0,          # velocity -> car1 amp
    "car1_left_scale" : 0,          # left key -> car1 amp in db/oct.
    "car1_right_scale" : 0,         # right key -> car1 amp in db/oct.
    "car1_mod_scale" : 1,           # FM depth scale factor 1,2,8,16,...,512,1024,2048(?)
    "car1_xmod_depth" : 0.00,       # 0..1, external sig -> car 1 mod depth
    "car1_mod_depth" : 1.0,         # FM depth mod1 -> car1
    "car1_mod_pluck" : 0.0,         # FM depth pluck -> car1
    "car1_amp_env" : 0.00,          # main amp env cross mix, 0:env2, 1=penv2
    "car1_pan" : 0.5,
    "car1_amp" : 1.0,               # 0..2
    "mod1_ratio" : 0.5,             # 0 < ratio <= 16
    "mod1_mod_pluck" : 0.0,         # 0..1 pluck -> mod1 FM
    "mod1_velocity" : 0.00,         # 0..1
    "mod1_left_scale" : 0,          # db/octave
    "mod1_right_scale" : 0,         # db/octave
    "mod1_env" : 0.00,              # 0:env1, 1=penv1
    "car2_ratio" : 0.5,             # 0 <= ratio <= 16
    "car2_bias" : 0,                # 0 <= bias <= 999  in Hz.
    "car2_velocity" : 0.0,          # velocity -> car2 amp
    "car2_left_scale" : 0,          # left key -> car2 amp in db/oct.
    "car2_right_scale" : 0,         # right key -> car2 amp in db/oct.
    "car2_mod_scale" : 1,           # FM depth scale factor 1,2,8,16,...,512,1024,2048(?)
    "car2_xmod_depth" : 0.00,       # 0..1, external sig -> car 1 mod depth
    "car2_mod_depth" : 1.0,         # FM depth mod1 -> car2
    "car2_mod_pluck" : 0.0,         # FM depth pluck -> car2
    "car2_amp_env" : 0.00,          # main amp env cross mix, 0=env2, 1=penv2
    "car2_pan" : 0.5,
    "car2_amp" : 1.0,               # 0..2
    "mod2_ratio" : 0.5,             # 0 < ratio <= 16
    "mod2_mod_pluck" : 0.0,         # 0..1 pluck -> mod2 FM
    "mod2_velocity" : 0.00,         # 0..1
    "mod2_left_scale" : 0,          # db/octave
    "mod2_right_scale" : 0,         # db/octave
    "mod2_env" : 0.00}              # 0=env1, 1=penv1

class Slug(Program):

    def __init__(self,name):
        super(Slug,self).__init__(name,Slug,prototype)
        self.performance = performance()

program_bank = ProgramBank(Slug("Init"))

def lfo(freq=7.000, delay=0.000, vsens=0.10, depth=0.00, noise=0.00, x=0.00):
    return {"vfreq" : float(freq),
            "vdelay" : float(delay),
            "vsens" : float(vsens),
            "vdepth" : float(depth),
            "vibrato" : 0.0,
            "vnoise" : float(noise),
            "xpitch" : float(x)}

def adsr(n, a=0.1, d=1.0, s=1.0, r=0.1,
         velocity=0.0, key_scale=0.0):
    def param(suffix):
        return "env%d_%s" % (n,suffix)
    return {param("attack") : float(a),
            param("decay") : float(d),
            param("sustain") : float(s),
            param("release") : float(r),
            param("velocity_attack") : float(velocity),
            param("key_attack") : float(key_scale)}

def pulse(amp=1.0, tune=1.0,
          width=0.5, width_env1=0.0, width_lfo=0.0,x=0.0,
          env=0.0,pan=0.5):
    return {"pulse_ratio" : float(tune),
            "pulse_width" : float(width),
            "pulse_width_env1" : float(width_env1),
            "pulse_width_lfo" : float(width_lfo),
            "pulse_filter_x" : float(x),
            "pulse_amp_env" : float(env),
            "pulse_amp" : float(amp),
            "pulse_pan" : float(pan)}

def pulse_filter(res=0.75, cutoff=16000,
                 env1=0, penv1=0, lfo=0, x=0,
                 velocity=0, left_track=0, right_track=0):
    return {"pulse_filter_res" : float(res),
            "pulse_filter_cutoff" : int(cutoff),
            "pulse_filter_env1" : int(env1),
            "pulse_filter_penv1" : int(penv1),
            "pulse_filter_lfo" : int(lfo),
            "pulse_filter_velocity" : int(velocity),
            "pulse_filter_left_track" : int(left_track),
            "pulse_filter_right_track" : int(right_track)}

def pluck(amp=1.00, tune=1.000, decay=3.0,
          harmonic=1, width=1, damp=0.5, noise=0.5,
          velocity=0.00, left_scale=0, right_scale=0,pan=0.5):
    return {"pluck_ratio" : float(tune),
            "pluck_decay" : float(decay),
            "pluck_harmonic" : int(harmonic),
            "pluck_width" : int(width),
            "pluck_excite" : float(noise),
            "pluck_damp" : float(damp),
            "pluck_velocity" : float(velocity),
            "pluck_left_scale" : int(left_scale),
            "pluck_right_scale" : int(right_scale),
            "pluck_amp" : float(amp),
            "pluck_pan" : float(pan)}

def carrier(n, amp=1.0, tune=1.0, bias=0.0,
            velocity=0.0, left_scale=0, right_scale=0,
            mod_scale=1, xmod=0.0, fm=0.0, pluck=0.0,env=0.0,pan=0.5):
    def param(suffix):
        return "car%d_%s" % (n,suffix)
    return {param("ratio") : float(tune),
            param("bias") : float(bias),
            param("velocity") : float(velocity),
            param("left_scale") : int(left_scale),
            param("right_scale") : int(right_scale),
            param("mod_scale") : int(mod_scale),
            param("xmod_depth") : float(xmod),
            param("mod_depth") : float(fm),
            param("mod_pluck") : float(pluck),
            param("amp_env") :float(env),
            param("amp") : float(amp),
            param("pan") : float(pan)}
            
def modulator(n, tune=1.0, pluck=0.0,
              velocity=0.0, left_scale=0, right_scale=0,
              env=0.0):
    def param(suffix):
        return "mod%d_%s" % (n,suffix)
    return {param("ratio") : float(tune),
            param("mod_pluck") : float(pluck),
            param("velocity") : float(velocity),
            param("left_scale") : int(left_scale),
            param("right_scale") : int(right_scale),
            param("env") : float(env)}

def slug(slot, name, amp=0.1,
         port=0.000, port_velocity=0.000,
         break_key=60, env_mode=0,
         lfo = lfo(),
         env1 = adsr(1),
         env2 = adsr(2),
         pdecay1 = 1.00,
         pdecay2 = 1.00,
         pulse = pulse(),
         pulse_filter = pulse_filter(),
         pluck = pluck(),
         car1 = carrier(1),
         mod1 = modulator(1),
         car2 = carrier(2),
         mod2 = modulator(2)):
    p = Slug(name)
    p["port"] = float(port)
    p["velocity_port"] = float(port_velocity)
    p["break_key"] = int(break_key)
    p["env_mode"] = int(env_mode)
    p["amp"] = float(amp)
    p["penv1_decay"] = float(pdecay1)
    p["penv2_decay"] = float(pdecay2)
    p.update(lfo)
    p.update(env1)
    p.update(env2)
    p.update(pulse)
    p.update(pulse_filter)
    p.update(pluck)
    p.update(car1)
    p.update(car2)
    p.update(mod1)
    p.update(mod2)
    program_bank[slot] = p
    return p


slug(0,"Dummy",
     pulse_filter=pulse_filter(cutoff=250,env1=120,penv1=60,lfo=30))
