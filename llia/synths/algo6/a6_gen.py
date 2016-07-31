# llia.synths.algo6.a3gen

from __future__ import print_function
from random import randrange

from llia.util.lmath import *
from llia.synths.algo6.a6_data import algo6

def pick_vibrato():
    frq = coin(0.75, 4+rnd(3), rnd(7))
    sen = coin(0.75, 0.01, rnd())
    dly = rnd(4)
    dpth = coin(0.75, 0.00, rnd())
    return {"freq" : frq,
            "sens" : sen,
            "delay" : dly,
            "depth" : dpth}

def pick_harmonic_mode():
    rs = coin(0.75, "HARMONIC",
              coin(0.75, "SEMI-HARMONIC", "RANDOM"))
    return rs



harmonics_1 = (0.5, 0.5, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 5, 6, 8)
harmonics_2 = (0.25, 0.75, 1.5, 1.5, 1.5, 2.25, 3.375, 5.0625)

def pick_harmonic(mode):
    if mode == "HARMONIC":
        return coin(0.75, pick(harmonics_1), pick(harmonics_2))
    elif mode == "RANDOM":
        return coin(0.75, rnd(8), 0.25+rnd(0.75))
    else:
        return pick_harmonic(coin(0.80, "HARMONIC", "RANDOM"))

def pick_carrier(n, harmonic_mode):
    f = pick_harmonic(harmonic_mode)
    if coin(0.125): f = approx(f)
    if n == 1:
        mix = 0
    else:
        mix = pick([0, -3, -6, -9])
    if f >= 3:
        highscale = pick([-3, -6, -9])
    else:
        highscale = 0
    lowscale = 0
    rs = {"mute" : False,
          "freq" : f,
          "mix" : mix,
          "lowscale" : lowscale,
          "highscale" : highscale}
    return rs
          
def pick_modulator(n, harmonic_mode):
    f = pick_harmonic(harmonic_mode)
    if coin(0.125): f = approx(f)
    if harmonic_mode == "RANDOM":
        b = int(coin(0.875, 0, rnd(200)))
    else:
        b = int(coin(0.75, 0, pick([1, 1, 1, 2, 2, 3, rnd(10)])))
    dpth = coin(0.50, rnd(0.5), rnd())
    if f >= 3:
        hs = pick([-3, -6, -6, -9])
    else:
        hs = 0
    if f < 1:
        ls = pick([3, 6, 9])
    else:
        ls = 0
    rs = {"mute" : False,
          "freq" : f,
          "bias" : b,
          "a" : 0.0,
          "modDepth" : dpth,
          "env" : coin(0.80, 1.0, 0.0),
          "lag" : coin(0.50, 0, coin(0.75, rnd(0.5), rnd())),
          "lowScale" : ls,
          "highScale" : hs}
    if n == 3:
        rs["feedback"] = coin(0.75, 0, rnd(3))
        rs["envToFeedback"] = coin(0.75, 0, random_sign(3))
    return rs
    
def pick_break_key():
    return pick([48, 60, 60, 60, 72])

def pick_env_time_range():
    return pick(["FAST", "FAST", "FAST"
                 "MEDIUM", "MEDIUM", "MEDIUM",
                 "SLOW"])

def pick_env_time(time_range):
    if coin(0.125):  # ignore time_range certain percent of time.
        return pick_env_time(pick_env_time_range())
    elif time_range=="FAST":
        return coin(0.75, rnd(0.05), rnd(0.1))
    elif time_range == "MEDIUM":
        return rnd()
    else:
        return 0.5+rnd(7.5)

def pick_adsr(time_range):
    s = coin(0.75, 0.5+rnd(0.5), rnd())
    return [pick_env_time(time_range),
            pick_env_time(time_range),
            s,
            pick_env_time(time_range)]

def pick_percussive(time_range):
    s = coin(0.75, rnd(0.2), rnd(0.5))
    a = coin(0.80, 0.0, pick_env_time("FAST"))
    return [a, pick_env_time(time_range), s, pick_env_time(time_range)]

def pick_envelope(time_range):
    return coin(0.5, pick_adsr(time_range), pick_percussive(time_range))

def a6gen(slot=127, *_):
    harm_mode = pick_harmonic_mode()
    env_time_range = pick_env_time_range()
    e1 = pick_envelope(env_time_range)
    e2 = pick_envelope(env_time_range)
    e3 = pick_envelope(env_time_range)
    p = algo6(slot, "Random", amp=-12,
              aToFreq = 0.0,
              brightness = coin(0.75, 1.0, 0.1+rnd(0.9)),
              vibrato = pick_vibrato(),
              c1 = pick_carrier(1, harm_mode),
              c2 = pick_carrier(2, harm_mode),
              c3 = pick_carrier(3, harm_mode),
              m1 = pick_modulator(1, harm_mode),
              m2 = pick_modulator(2, harm_mode),
              m3 = pick_modulator(3, harm_mode),
              break_keys = [pick_break_key(),
                            pick_break_key(),
                            pick_break_key()],
              env1 = e1,
              env2 = e1,
              env3 = e1)
    return p
    
