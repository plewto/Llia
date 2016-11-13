# llia.synths.corvus.rndgen.rutil
# Utility functions

from __future__ import print_function
from llia.util.lmath import (rnd,coin,pick,approx,random_sign)
from llia.synths.corvus.corvus_constants import *


def _harmonic_ratio():
    lst1 = [0.5]*3 + [1.0,2.0]*8 + [3.0,4.0]*6 
    lst2 = lst1*2 + [0.75,1.333]+[1.5]*4
    lst3 = lst2*2 + [5,6,6,6]*4 + [8,8,9,10,12,16]*2 + [7]
    return pick(lst3)

def _random_ratio():
    rs = coin(0.75, 0.5+rnd(6), rnd())
    return round(rs,4)

# pick operator frequency ratio
#
def pick_ratio(pconfig={}):
    p = pconfig.get("p-harmonic",0.80)
    return coin(p, _harmonic_ratio(),_random_ratio())

# pick carrier bias frequency
#
def pick_bias(pconfig={}):
    p = pconfig.get("p-bias",0.05)
    low = round(rnd(4),4)
    high = round(rnd(300),4)
    return coin(p, coin(0.75, low, high), 0.0)

def pick_vibrato_frequency():
    rs = coin(0.75, 4+rnd(4),
              coin(0.90, rnd(10), rnd(90)))
    return round(rs,4)

def pick_lfo_frequency():
    half = len(LFO_RATIOS)/2
    q1 = pick(LFO_RATIOS[:half])[0]
    q2 = pick(LFO_RATIOS)[0]
    q3 = coin(0.75, q1, q2)
    return round(float(q3),4)


# populate dictionary with all vibrato/lfo related values.
# 
def lfos(pconfig={}):
    vfreq = pick_vibrato_frequency()
    lfo1 = pick_lfo_frequency()
    lfo2 = lfo1
    while lfo2 == lfo1:
        lfo2 = pick_lfo_frequency()
    pvib = pconfig.get("p-vibrato")
    rs = {"vfreq" : vfreq,
          "vdelay" : round(rnd(4),4),
          "vsens" : round(coin(0.75, rnd(0.3),rnd()),4),
          "vdepth" : round(coin(pvib, rnd(),0.0),4),
          "lfo1_ratio" : lfo1,
          "lfo2_ratio" : lfo2,
          "lfo1_delay" : round(coin(0.5, 0.0, rnd()), 4),
          "lfo2_delay" : round(coin(0.5, 0.0, rnd()), 4)}
    return rs
    

# Returns param/value map for all op parameters
# except fm,amp,enable,envelope
#
def op_params(op, pconfig={}):
    vel = coin(pconfig.get("p-velocity",0.4), rnd(), 0.0)
    lf1 = coin(pconfig.get("p-lfo",0.1), rnd(), 0.0)
    lf2 = coin(pconfig.get("p-lfo",0.1), rnd(), 0.0)
    penv = random_sign()*coin(pconfig.get("p-pitch-env", 0.02), rnd(2)-1, 0.0)
    rs = {"op%d_ratio" % op : pick_ratio(pconfig),
          "op%d_bias" % op : pick_bias(pconfig),
          "op%d_velocity" % op : round(vel,4),
          "op%d_lfo1" % op : round(lf1,4),
          "op%d_lfo2" % op : round(lf2,4),
          "op%d_external" % op : 0.0,
          "op%d_key" % op : 60,
          "op%d_left" % op : 0,
          "op%d_right" % op : 0,
          "op%d_pe" % op : round(penv,4)}
    if op == 3:
        p = pconfig.get("p-noise",0.1)
        nsmix = round(coin(p, coin(0.5, rnd(), 1.0), 0.0),4)
        nsbw = pick(NOISE_BANDWIDTHS)
        rs["nse3_mix"] = nsmix
        rs["nse3_bw"] = nsbw
    elif op == 4:
        p = pconfig.get("p-buzz", 0.4)
        plfo = pconfig.get("p-lfo",0.1)
        n = int(coin(0.60, rnd(8), rnd(128)))
        if n < 16:
            s = 1
        elif n > 84:
            s = -1
        else:
            s = coin(0.5,-1,1)
        env = int(s * coin(0.50, rnd(128), 0.0))
        lfo = int(coin(plfo, coin(0.75, rnd(64),rnd(128))))
        lag = round(coin(0.50, rnd(), 0.0), 4)
        mix = round(coin(p, rnd(), 0), 4)
        rs["bzz4_n"] = max(n,1)
        rs["bzz4_env"] = env
        rs["bzz4_lfo2"] = lfo
        rs["bzz4_lag"] = lag
        rs["bzz4_mix"] = mix
    return rs
        
        
def fm_params(op, pconfig={}):
    pdeep = pconfig.get("p-deep-modulation", 0.1)
    plfo = pconfig.get("p-lfo", 0.1)
    mscale = coin(pdeep, pick([1,10,100,1000,10000]),pick([1,1,10,10,10,10]))
    rs = {"fm%d_ratio" % op : pick_ratio(pconfig),
          "fm%d_moddepth" % op : round(coin(0.75, rnd(), 0.0),4),
          "fm%d_modscale" % op : float(mscale),
          "fm%d_lag" % op : round(coin(0.50, 0.0, rnd()), 4),
          "fm%d_lfo1" % op : round(coin(plfo, coin(0.5, rnd(0.25), rnd()), 0.0),4),
          "fm%d_lfo2" % op : round(coin(plfo, coin(0.5, rnd(0.25), rnd()), 0.0),4),
          "fm%d_external" % op : 0.0,
          "fm%d_left" % op : 0,
          "fm%d_right" % op : 0}
    return rs
          
          
            
