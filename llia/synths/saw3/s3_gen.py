# llia.synths.saw3.s3_gen
# 2016.06.06

from __future__ import print_function
from random import randrange


from llia.synths.saw3.s3_data import (saw3, vibrato, lfo, adsr1, adsr2, 
                                      osc1, osc2, osc3, noise, mix,
                                      filter_, res, filter_mix)
from llia.util.lmath import *


# LFO and Vibrato


def pick_vibrato_frequency():
    return coin(0.75, 4+rnd(4), rnd(10))

def rnd_vibrato(vfreq):
    return vibrato(vfreq,
                   delay = rnd(4),
                   depth = coin(0.85, 0, rnd()),
                   sens = coin(0.75, 0.1, rnd()))

# sync lfo to vibrato 25% of time
# otherwise use very slow lfo 75%
#
def rnd_lfo(vfreq):
    if coin(0.25):
        n = pick([1,2,3])
        d = float(pick([1,2,4,8,3,6,9,12,5]))
        freq = (n*vfreq)/d
    else:
        freq = coin(0.75, rnd(), rnd(7))
    return lfo(freq,
               delay = coin(0.5, 0, rnd(4)),
               depth = 1.0)

# Envelopes
#
def pick_env_timescale():
    tlst = []
    tlst += [0.2] * 10
    tlst += [0.5] * 30
    tlst += [1.0] * 40
    tlst += [4.0] * 15
    tlst += [8.0] * 5
    return pick(tlst)
    
def pick_env_time(scale):
    # 25% ignore scale 
    s = coin(0.75, scale, pick_env_timescale())
    return rnd(s)

def pick_envelope(scale):
    a = pick_env_time(scale)
    d = pick_env_time(scale)
    r = pick_env_time(scale)
    s = coin(0.85, 0.75+rnd(0.25), rnd())
    return [a,d,s,r]

# Harmonic structure
#
def pick_harmonic_mode():
    return coin(0.75, "harmonic", coin(0.75, "semi-harmonic", "random"))

def osc_freq(hmode):
    if hmode == "harmonic":
        return pick([0.25, 0.5, 0.5, 1.0, 1.0, 1.0, 2.0])
    elif hmode == "random":
       return 0.5+rnd(2)
    else:
        return coin(0.75, osc_freq("harmonic"), osc_freq("random")) 

def apply_detune(freq):
    return coin(0.75, freq, approx(freq))

def pick_bias3(hmode):
    if hmode == "harmonic":
        return coin(0.75, 0, pick([1,2]))
    else:
        return coin(0.85, 0, rnd(300))

def pick_osc1(freq):
    return osc1(freq,
                wave = coin(0.75, 0.5, rnd()),
                env1 = coin(0.5, 0, random_sign(0.5, rnd())),
                lfo = coin(0.5, 0, rnd()))

def pick_osc2(freq):
    return osc2(freq,
                wave = coin(0.75, 0.5, rnd()),
                env1 = coin(0.5, 0, random_sign(0.5, rnd())),
                lfo = coin(0.5, 0, rnd()))    

def pick_osc3(freq, bias):
    return osc3(freq,
                wave = coin(0.75, 0.5, rnd()),
                env1 = coin(0.5, 0, random_sign(0.5, rnd())),
                lfo = coin(0.5, 0, rnd()),
                lag = rnd(2),
                bias=bias)
    
def pick_noise():
    return noise(pick([1, 2, 2, 3, 4, 4, 6]),
                 rnd())
    
def pick_mix_level():
    lst = [-24, -18, -15, -12, -9, -9, -6, -6, -6, -3, -3, -3, 0]
    nse = coin(0.80, -99, pick([-18, -15, -12, -12, -12, -9, -6, -3, 0]))
    mixes = [pick(lst), pick(lst), pick(lst), nse]
    comp = max(*mixes)
    acc = []
    for db in mixes:
        acc.append(db-comp)
    return mix(acc[0], acc[1], acc[2], acc[3],
               coin(0.75, 0, random_sign(rnd())),
               coin(0.75, 0, random_sign(rnd())),
               coin(0.75, 0, random_sign(rnd())),
               coin(0.75, 0, random_sign(rnd())))

# Filters

def pick_filter():
    freq = int(coin(0.5, rnd(1000), rnd(10000)))
    e1 = coin(0.75, rnd(10000), 0)
    if freq > 7500:
        e1 = random_sign(0.5, e1)
    return filter_(freq,
                   keytrack = pick([0, 1]),
                   env1 = e1,
                   lfo = coin(0.85, 0, rnd(10000)),
                   bpoffset = pick([1, 2, 3, 4, 6]),
                   bplag = coin(0.5, 0, rnd()))
                   
def pick_res():
    return res(coin(0.75, rnd(0.8), 0.6+rnd(0.4)),
               env1 = coin(0.75, 0, random_sign(rnd())),
               lfo = coin(0.75, 0, rnd()))

def pick_filter_mix():
    return filter_mix(coin(0.75, -rnd(), rnd()),
                      env1 = coin(0.75, 0, random_sign(rnd())),
                      lfo = coin(0.75, 0, rnd()))


def s3gen(slot=127, *_) :
    vfreq = pick_vibrato_frequency()
    envscale = pick_env_timescale()
    harmonic_mode = pick_harmonic_mode()
    freq1 = osc_freq(harmonic_mode)
    freq2 = apply_detune(osc_freq(harmonic_mode))
    freq3 = apply_detune(osc_freq(harmonic_mode))
    bias3 = pick_bias3(harmonic_mode)
    print("# envscale      %s" % envscale)
    print("# harmonic_mode %s" % harmonic_mode)
    rs = saw3(slot, "Random", -12,
              rnd_vibrato(vfreq),
              rnd_lfo(vfreq),
              adsr1(*pick_envelope(envscale)),
              adsr2(*pick_envelope(envscale)),
              pick_osc1(freq1),
              pick_osc2(freq2),
              pick_osc3(freq3, bias3),
              pick_noise(),
              pick_mix_level(),
              pick_filter(),
              pick_res(),
              pick_filter_mix(),
              port = coin(0.75, 0, rnd()))
    return rs
          
         
         
         
