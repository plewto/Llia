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
    "penv2_decay" : 1.00
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
    "pulse_enable" : 1,             # 0=off, 1=on
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
    "pluck_enable" : 1,             # 0=off, 1=on
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
    "car1_enable" : 1,              # 0=off, 1=on
    "car1_amp" : 1.0,               # 0..2
    "mod1_ratio" : 0.5,             # 0 < ratio <= 16
    "mod1_mod_pluck" : 0.0,         # 0..1 pluck -> mod1 FM
    "mod1_velocity" : 0.00,         # 0..1
    "mod1_left_scale" : 0,          # db/octave
    "mod1_right_scale" : 0,         # db/octave
    "mod1_env" : 0.00,              # 0:env1, 1=penv1
    "mod1_enable" : 1,              # 0=off, 1=on
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
    "car2_enable" : 1,              # 0=off, 1=on
    "car2_amp" : 1.0,               # 0..2
    "mod2_ratio" : 0.5,             # 0 < ratio <= 16
    "mod2_mod_pluck" : 0.0,         # 0..1 pluck -> mod2 FM
    "mod2_velocity" : 0.00,         # 0..1
    "mod2_left_scale" : 0,          # db/octave
    "mod2_right_scale" : 0,         # db/octave
    "mod2_env" : 0.00,              # 0=env1, 1=penv1
    "mod2_enable" : 1}              # 0=off, 1=on

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

def pulse(enable=1, amp=1.0, tune=1.0,
          width=0.5, width_env1=0.0, width_lfo=0.0,x=0.0,
          env=0.0):
    return {"pulse_ratio" : float(tune),
            "pulse_width" : float(width),
            "pulse_width_env1" : float(width_env1),
            "pulse_width_lfo" : float(width_lfo),
            "pulse_filter_x" : float(x),
            "pulse_amp_env" : float(env),
            "pulse_amp" : float(amp),
            "pulse_enable" : int(enable)}

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

def pluck(enable=1, amp=1.00, tune=1.000, decay=3.0,
          harmonic=1, width=1, damp=0.5, noise=0.5,
          velocity=0.00, left_scale=0, right_scale=0):
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
            "pluck_enable" : int(enable)}

def carrier(n, enable=1, amp=1.0, tune=1.0, bias=0.0,
            velocity=0.0, left_scale=0, right_scale=0,
            mod_scale=1, xmod=0.0, fm=0.0, pluck=0.0,env=0.0):
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
            param("enable") : int(enable),
            param("amp") : float(amp)}
            
def modulator(n, enable=1, tune=1.0, pluck=0.0,
              velocity=0.0, left_scale=0, right_scale=0,
              env=0.0):
    def param(suffix):
        return "mod%d_%s" % (n,suffix)
    return {param("ratio") : float(tune),
            param("mod_pluck") : float(pluck),
            param("velocity") : float(velocity),
            param("left_scale") : int(left_scale),
            param("right_scale") : int(right_scale),
            param("enable") : int(enable),
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

slug(0,"Zero",amp=0.100,
     break_key=60, env_mode=0,
     port=0.000, port_velocity=0.000,
     lfo = lfo(freq=2.947, delay=1.338,
               vsens=0.100, depth=0.295, noise=0.600, x=0.000),
     env1 = adsr(1, a=1.715, d=0.000, s=0.694, r=12.328,
                 velocity=0.000, key_scale=0.000),
     env2 = adsr(2, a=1.366, d=3.139, s=0.637, r=6.534,
                 velocity=0.000, key_scale=0.000),
     pdecay1 = 3.608,
     pdecay2 = 5.797,
     pulse = pulse(enable=1, amp=1.000, tune=2.000,
                   width=0.399, width_env1=0.000, width_lfo=0.325,
                   env = 1.000),
     pulse_filter = pulse_filter(res=0.706, cutoff=10000,
                                 env1=-1, penv1=1, lfo=0, x=0,
                                 velocity=0, left_track=0, right_track=0),
     pluck = pluck(enable=0, amp=1.000, tune=2.000, decay=1.200,
                   harmonic=6, width=1, damp=0.185, noise=0.214,
                   velocity=0.895, left_scale=0, right_scale=0),
     car1 = carrier(1, enable=1, amp=0.777, tune=0.500, bias=1.647,
            velocity=0.232, left_scale=0, right_scale=0, env=0.202,
            mod_scale=4, xmod=0.000, fm=0.830, pluck=233.477),
     car2 = carrier(2, enable=0, amp=0.723, tune=1.500, bias=1.028,
            velocity=0.000, left_scale=0, right_scale=0, env=0.583,
            mod_scale=2, xmod=0.000, fm=0.000, pluck=3.892),
     mod1 = modulator(1, enable=1, tune=0.250, pluck=0.000,
            velocity=0.593, left_scale=0, right_scale=0, env=0.950),
     mod2 = modulator(2, enable=1, tune=8.000, pluck=0.313,
            velocity=0.000, left_scale=0, right_scale=0, env=0.886))

slug(1,"One",amp=0.100,
     break_key=60, env_mode=0,
     port=0.000, port_velocity=0.000,
     lfo = lfo(freq=5.850, delay=1.167,
               vsens=0.100, depth=0.000, noise=0.000, x=0.000),
     env1 = adsr(1, a=1.021, d=0.107, s=0.618, r=0.027,
                 velocity=0.000, key_scale=0.771),
     env2 = adsr(2, a=0.637, d=1.022, s=0.416, r=1.144,
                 velocity=0.000, key_scale=0.358),
     pdecay1 = 1.334,
     pdecay2 = 1.143,
     pulse = pulse(enable=1, amp=1.000, tune=1.000,
                   width=0.543, width_env1=0.000, width_lfo=0.359,
                   env = 1.000),
     pulse_filter = pulse_filter(res=0.049, cutoff=10000,
                                 env1=1, penv1=-1, lfo=0, x=0,
                                 velocity=0, left_track=0, right_track=0),
     pluck = pluck(enable=1, amp=0.537, tune=1.000, decay=6.816,
                   harmonic=1, width=1, damp=0.404, noise=0.163,
                   velocity=0.000, left_scale=0, right_scale=0),
     car1 = carrier(1, enable=1, amp=1.020, tune=3.000, bias=1.462,
            velocity=0.000, left_scale=0, right_scale=0, env=0.629,
            mod_scale=2, xmod=0.000, fm=0.876, pluck=72.896),
     car2 = carrier(2, enable=1, amp=1.230, tune=0.991, bias=0.000,
            velocity=0.000, left_scale=0, right_scale=0, env=0.769,
            mod_scale=1, xmod=0.000, fm=0.000, pluck=2.525),
     mod1 = modulator(1, enable=1, tune=8.000, pluck=3.917,
            velocity=0.000, left_scale=0, right_scale=0, env=0.345),
     mod2 = modulator(2, enable=0, tune=3.027, pluck=2.041,
            velocity=0.994, left_scale=0, right_scale=0, env=0.482))

slug(2,"Two",amp=0.100,
     break_key=60, env_mode=1,
     port=0.000, port_velocity=0.000,
     lfo = lfo(freq=1.098, delay=0.000,
               vsens=0.100, depth=0.000, noise=0.000, x=0.000),
     env1 = adsr(1, a=6.654, d=5.414, s=0.278, r=10.105,
                 velocity=0.000, key_scale=0.000),
     env2 = adsr(2, a=0.036, d=5.584, s=0.176, r=13.257,
                 velocity=0.735, key_scale=0.000),
     pdecay1 = 14.148,
     pdecay2 = 11.437,
     pulse = pulse(enable=0, amp=1.000, tune=0.750,
                   width=0.957, width_env1=0.000, width_lfo=0.336,
                   env = 1.000),
     pulse_filter = pulse_filter(res=0.882, cutoff=3200,
                                 env1=1, penv1=-1, lfo=0, x=0,
                                 velocity=0, left_track=0, right_track=0),
     pluck = pluck(enable=1, amp=1.000, tune=1.000, decay=0.566,
                   harmonic=7, width=1, damp=0.120, noise=0.098,
                   velocity=0.000, left_scale=0, right_scale=0),
     car1 = carrier(1, enable=1, amp=0.478, tune=4.000, bias=0.257,
            velocity=0.352, left_scale=0, right_scale=0, env=0.240,
            mod_scale=2, xmod=0.000, fm=0.520, pluck=0.000),
     car2 = carrier(2, enable=1, amp=0.221, tune=1.000, bias=477.892,
            velocity=0.000, left_scale=0, right_scale=0, env=0.896,
            mod_scale=3, xmod=0.000, fm=0.465, pluck=1.511),
     mod1 = modulator(1, enable=1, tune=0.498, pluck=3.486,
            velocity=0.000, left_scale=0, right_scale=0, env=0.911),
     mod2 = modulator(2, enable=1, tune=1.511, pluck=3.659,
            velocity=0.000, left_scale=0, right_scale=0, env=0.159))

slug(3,"Three",amp=0.200,
     break_key=60, env_mode=0,
     port=0.000, port_velocity=0.000,
     lfo = lfo(freq=7.546, delay=0.000,
               vsens=0.100, depth=0.829, noise=0.000, x=0.000),
     env1 = adsr(1, a=0.454, d=0.496, s=0.749, r=0.086,
                 velocity=0.000, key_scale=0.000),
     env2 = adsr(2, a=0.790, d=0.282, s=0.687, r=1.762,
                 velocity=0.083, key_scale=0.000),
     pdecay1 = 1.296,
     pdecay2 = 1.916,
     pulse = pulse(enable=0, amp=0.605, tune=5.002,
                   width=0.380, width_env1=0.000, width_lfo=0.131,
                   env = 0.605),
     pulse_filter = pulse_filter(res=0.136, cutoff=6400,
                                 env1=1, penv1=1, lfo=200, x=0,
                                 velocity=0, left_track=0, right_track=0),
     pluck = pluck(enable=0, amp=0.024, tune=3.008, decay=5.735,
                   harmonic=3, width=0, damp=0.256, noise=0.700,
                   velocity=0.000, left_scale=1, right_scale=0),
     car1 = carrier(1, enable=1, amp=0.566, tune=1.000, bias=861.013,
            velocity=0.000, left_scale=0, right_scale=0, env=0.500,
            mod_scale=2, xmod=0.000, fm=0.349, pluck=1.290),
     car2 = carrier(2, enable=1, amp=0.691, tune=1.500, bias=0.986,
            velocity=0.000, left_scale=0, right_scale=0, env=0.185,
            mod_scale=4, xmod=0.000, fm=0.237, pluck=0.000),
     mod1 = modulator(1, enable=1, tune=1.004, pluck=0.000,
            velocity=0.000, left_scale=0, right_scale=0, env=0.358),
     mod2 = modulator(2, enable=0, tune=2.000, pluck=1.868,
            velocity=0.000, left_scale=0, right_scale=0, env=0.718))

slug(4,"Four",amp=0.100,
     break_key=60, env_mode=0,
     port=0.000, port_velocity=0.000,
     lfo = lfo(freq=4.182, delay=0.000,
               vsens=0.100, depth=0.000, noise=0.000, x=0.000),
     env1 = adsr(1, a=0.007, d=0.022, s=0.613, r=0.018,
                 velocity=0.000, key_scale=0.000),
     env2 = adsr(2, a=0.005, d=0.006, s=0.204, r=0.081,
                 velocity=0.000, key_scale=0.000),
     pdecay1 = 1.850,
     pdecay2 = 0.059,
     pulse = pulse(enable=1, amp=1.000, tune=2.704,
                   width=0.599, width_env1=0.000, width_lfo=0.000,
                   env = 1.000),
     pulse_filter = pulse_filter(res=0.407, cutoff=200,
                                 env1=-1, penv1=1, lfo=3200, x=0,
                                 velocity=0, left_track=0, right_track=0),
     pluck = pluck(enable=1, amp=1.000, tune=3.676, decay=7.195,
                   harmonic=3, width=1, damp=0.393, noise=0.680,
                   velocity=0.000, left_scale=1, right_scale=0),
     car1 = carrier(1, enable=1, amp=1.277, tune=4.009, bias=1.713,
            velocity=0.000, left_scale=0, right_scale=0, env=0.745,
            mod_scale=4, xmod=0.000, fm=0.374, pluck=0.000),
     car2 = carrier(2, enable=0, amp=1.219, tune=4.138, bias=0.000,
            velocity=0.000, left_scale=0, right_scale=0, env=0.416,
            mod_scale=2, xmod=0.000, fm=0.000, pluck=1.154),
     mod1 = modulator(1, enable=1, tune=7.693, pluck=1.970,
            velocity=0.000, left_scale=0, right_scale=0, env=0.323),
     mod2 = modulator(2, enable=1, tune=7.493, pluck=0.000,
            velocity=0.000, left_scale=0, right_scale=0, env=0.769))
 
slug(5,"Five",amp=0.100,
     break_key=60, env_mode=0,
     port=0.000, port_velocity=0.000,
     lfo = lfo(freq=5.266, delay=0.000,
               vsens=0.100, depth=0.000, noise=0.000, x=0.000),
     env1 = adsr(1, a=4.032, d=0.048, s=0.378, r=7.352,
                 velocity=0.000, key_scale=0.000),
     env2 = adsr(2, a=2.023, d=3.401, s=0.456, r=6.815,
                 velocity=0.374, key_scale=0.000),
     pdecay1 = 0.097,
     pdecay2 = 6.557,
     pulse = pulse(enable=1, amp=1.000, tune=7.387,
                   width=0.700, width_env1=0.000, width_lfo=0.472,
                   env = 1.000),
     pulse_filter = pulse_filter(res=0.575, cutoff=200,
                                 env1=1, penv1=-1, lfo=0, x=0,
                                 velocity=3200, left_track=0, right_track=0),
     pluck = pluck(enable=1, amp=0.583, tune=6.786, decay=0.837,
                   harmonic=6, width=1, damp=0.800, noise=0.317,
                   velocity=0.000, left_scale=0, right_scale=0),
     car1 = carrier(1, enable=1, amp=1.200, tune=3.629, bias=0.951,
            velocity=0.000, left_scale=0, right_scale=0, env=0.579,
            mod_scale=3, xmod=0.000, fm=0.391, pluck=0.763),
     car2 = carrier(2, enable=0, amp=1.278, tune=4.607, bias=1.743,
            velocity=0.000, left_scale=0, right_scale=0, env=0.406,
            mod_scale=1, xmod=0.000, fm=0.463, pluck=0.000),
     mod1 = modulator(1, enable=1, tune=7.805, pluck=101.678,
            velocity=0.000, left_scale=0, right_scale=0, env=0.774),
     mod2 = modulator(2, enable=1, tune=2.937, pluck=0.000,
            velocity=0.000, left_scale=0, right_scale=0, env=0.469))

slug(6,"Six",amp=0.100,
     break_key=60, env_mode=0,
     port=0.000, port_velocity=0.860,
     lfo = lfo(freq=6.341, delay=1.714,
               vsens=0.100, depth=0.000, noise=0.000, x=0.000),
     env1 = adsr(1, a=0.040, d=0.034, s=0.827, r=0.189,
                 velocity=0.000, key_scale=0.000),
     env2 = adsr(2, a=7.630, d=7.911, s=0.898, r=0.092,
                 velocity=0.161, key_scale=0.000),
     pdecay1 = 2.001,
     pdecay2 = 10.059,
     pulse = pulse(enable=1, amp=0.821, tune=2.000,
                   width=0.403, width_env1=0.000, width_lfo=0.167,
                   env = 0.821),
     pulse_filter = pulse_filter(res=0.048, cutoff=1600,
                                 env1=1, penv1=-1, lfo=0, x=0,
                                 velocity=0, left_track=0, right_track=0),
     pluck = pluck(enable=1, amp=1.000, tune=6.000, decay=1.288,
                   harmonic=5, width=1, damp=0.243, noise=0.356,
                   velocity=0.407, left_scale=0, right_scale=0),
     car1 = carrier(1, enable=0, amp=0.908, tune=8.000, bias=1.605,
            velocity=0.000, left_scale=0, right_scale=0, env=0.512,
            mod_scale=2, xmod=0.000, fm=0.000, pluck=973.819),
     car2 = carrier(2, enable=0, amp=0.720, tune=2.000, bias=0.223,
            velocity=0.000, left_scale=0, right_scale=0, env=0.306,
            mod_scale=2, xmod=0.000, fm=0.589, pluck=5.222),
     mod1 = modulator(1, enable=1, tune=7.943, pluck=0.000,
            velocity=0.000, left_scale=0, right_scale=0, env=0.823),
     mod2 = modulator(2, enable=1, tune=0.495, pluck=0.169,
            velocity=0.000, left_scale=0, right_scale=0, env=0.464))

slug(7,"Seven",amp=0.100,
     break_key=60, env_mode=0,
     port=0.000, port_velocity=0.000,
     lfo = lfo(freq=4.030, delay=1.528,
               vsens=0.100, depth=0.374, noise=0.000, x=0.000),
     env1 = adsr(1, a=0.004, d=0.533, s=0.996, r=0.168,
                 velocity=0.000, key_scale=0.000),
     env2 = adsr(2, a=0.013, d=0.042, s=0.422, r=0.169,
                 velocity=0.000, key_scale=0.004),
     pdecay1 = 0.173,
     pdecay2 = 7.424,
     pulse = pulse(enable=1, amp=0.343, tune=1.502,
                   width=0.325, width_env1=0.000, width_lfo=0.000,
                   env = 0.343),
     pulse_filter = pulse_filter(res=0.682, cutoff=100,
                                 env1=1, penv1=1, lfo=0, x=0,
                                 velocity=1600, left_track=0, right_track=0),
     pluck = pluck(enable=0, amp=0.771, tune=3.000, decay=7.243,
                   harmonic=3, width=1, damp=0.045, noise=0.247,
                   velocity=0.000, left_scale=0, right_scale=0),
     car1 = carrier(1, enable=1, amp=0.372, tune=1.000, bias=0.000,
            velocity=0.000, left_scale=0, right_scale=0, env=0.909,
            mod_scale=451, xmod=0.000, fm=0.000, pluck=0.000),
     car2 = carrier(2, enable=1, amp=0.567, tune=6.000, bias=1.916,
            velocity=0.000, left_scale=0, right_scale=0, env=0.387,
            mod_scale=3, xmod=0.000, fm=0.584, pluck=1.080),
     mod1 = modulator(1, enable=1, tune=2.000, pluck=0.000,
            velocity=0.830, left_scale=0, right_scale=0, env=0.594),
     mod2 = modulator(2, enable=1, tune=1.000, pluck=2.914,
            velocity=0.000, left_scale=0, right_scale=0, env=0.562))

slug(8,"Eight",amp=0.100,
     break_key=60, env_mode=0,
     port=0.000, port_velocity=0.000,
     lfo = lfo(freq=3.225, delay=0.445,
               vsens=0.100, depth=0.000, noise=0.766, x=0.000),
     env1 = adsr(1, a=0.039, d=0.033, s=0.253, r=0.656,
                 velocity=0.000, key_scale=0.000),
     env2 = adsr(2, a=0.039, d=6.432, s=0.392, r=0.035,
                 velocity=0.000, key_scale=0.000),
     pdecay1 = 0.059,
     pdecay2 = 1.181,
     pulse = pulse(enable=1, amp=1.000, tune=1.000,
                   width=0.714, width_env1=0.000, width_lfo=0.000,
                   env = 1.000),
     pulse_filter = pulse_filter(res=0.640, cutoff=800,
                                 env1=1, penv1=1, lfo=100, x=0,
                                 velocity=0, left_track=0, right_track=0),
     pluck = pluck(enable=0, amp=1.000, tune=6.000, decay=8.650,
                   harmonic=2, width=0, damp=0.334, noise=0.164,
                   velocity=0.000, left_scale=1, right_scale=1),
     car1 = carrier(1, enable=1, amp=1.418, tune=0.754, bias=1.204,
            velocity=0.000, left_scale=0, right_scale=0, env=0.770,
            mod_scale=3, xmod=0.000, fm=0.652, pluck=0.000),
     car2 = carrier(2, enable=1, amp=0.970, tune=3.000, bias=1.477,
            velocity=0.000, left_scale=0, right_scale=0, env=0.932,
            mod_scale=4, xmod=0.000, fm=0.851, pluck=3.100),
     mod1 = modulator(1, enable=1, tune=3.000, pluck=1.692,
            velocity=0.000, left_scale=0, right_scale=0, env=0.651),
     mod2 = modulator(2, enable=1, tune=1.000, pluck=0.000,
            velocity=0.000, left_scale=0, right_scale=0, env=0.593))
