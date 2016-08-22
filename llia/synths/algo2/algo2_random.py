# llia.synths.algo2.algo2_random

from __future__ import print_function
from llia.synths.algo2.algo2_data import algo2
from llia.util.lmath import (coin, pick, rnd, random_sign, random, approx)
import llia.synths.algo2.algo2_constants as con


def select_time_hint():
    rs = coin(0.75, "MODERATE", coin(0.5, "SLOW", "FAST"))
    return rs

def pick_slow_time():
    t = 1 + rnd(6)
    return t

def pick_moderate_time():
    return rnd()

def pick_fast_time():
    return rnd(0.25)

def pick_time(hint):
    if hint == "MODERATE":
        t = coin(0.75, pick_moderate_time(),
                 coin(0.5, pick_slow_time(), pick_fast_time()))
    elif hint == "SLOW":
        t = coin(0.75, pick_slow_time(),
                 coin(0.5, pick_moderate_time(), pick_fast_time()))
    else:
        t = coin(0.75, pick_fast_time(),
                 coin(0.5, pick_moderate_time(), pick_slow_time()))
    return t



def select_harmonic_hint():
    rs = coin(0.75, "HARMONIC",
              coin(0.75, "SEMI-HARMONIC", "RANDOM"))
    return rs


def select_op_ratios(hint):
    acc = []   # op ratios
    if hint == "HARMONIC":
        for i in range(8):
            r = pick(con.P_HARMONICS)
            r = r * coin(0.75, r, approx(r, 0.005))
            acc.append(r)
    elif hint == "SEMI-HARMONIC":
        for i in range(8):
            r = coin(0.75, pick(con.P_HARMONICS), 0.25+rnd(8))
            r = r * coin(0.75, r, approx(r, 0.01))
            acc.append(r)
    else:
        for i in range(8):
            acc.append(0.25+rnd(8))
    return acc

def select_modulator_bias(hint):
    acc = []
    for op in (2,3,5,6,8):
        if hint == "HARMONIC":
            b = coin(0.80, 0, int(rnd(5)))
        elif hint == "SEMI-HARMONIC":
            b = coin(0.75, 0, coin(0.5, int(rnd(5)), int(rnd(100))))
        else:
            b = coin(0.90, 0, int(rnd(100)))
        acc.append(b)
    return acc

def select_carrier_envelope():
    return pick([0,1,2,3])
            

def select_modulator_envelope():
    return pick([0,1,2,3,0,1,2,3,4,5,6,7])



def random_algo2(slot=127, *_):
    time_hint = select_time_hint()
    harmonic_hint = select_harmonic_hint()
    op_ratios = select_op_ratios(harmonic_hint)
    op_bias = select_modulator_bias(harmonic_hint)
    p = algo2(slot, "Random",
              amp = -12,
              port = coin(0.90, 0.0, rnd()),
              external = {
                  "pitch" : 0.0,
                  "scale" : 1.0,
                  "bias" : 0.0},
              lfo = {
                  "freq" : coin(0.75, 1+rnd(6), rnd(10)),
                  "ratio" : pick(con.LFO_RATIOS),
                  "mix" : coin(0.5, 0.0, rnd()),
                  "delay" : rnd(4.0),
                  "depth" : coin(0.75, 0.5+rnd(0.5), rnd()),
                  "vsens" : coin(0.90, rnd(0.01), rnd()),
                  "vdepth" : coin(0.75, rnd(0.4), rnd())},
              enva = {
                  "attack" : pick_time(time_hint),
                  "decay1" : pick_time(time_hint),
                  "decay2" : pick_time(time_hint),
                  "release" : pick_time(time_hint),
                  "breakpoint" : coin(0.75, 0.75+rnd(0.25), rnd()),
                  "sustain" : coin(0.75, 0.5+rnd(0.5), rnd())},
              envb = {
                  "attack" : pick_time(time_hint),
                  "decay1" : pick_time(time_hint),
                  "decay2" : pick_time(time_hint),
                  "release" : pick_time(time_hint),
                  "breakpoint" : coin(0.75, 0.75+rnd(0.25), rnd()),
                  "sustain" : coin(0.75, 0.5+rnd(0.5), rnd())},
              envc = {
                  "attack" : pick_time(time_hint),
                  "decay1" : pick_time(time_hint),
                  "decay2" : pick_time(time_hint),
                  "release" : pick_time(time_hint),
                  "breakpoint" : coin(0.75, 0.75+rnd(0.25), rnd()),
                  "sustain" : coin(0.75, 0.5+rnd(0.5), rnd())},
              envd = {
                  "attack" : pick_time(time_hint),
                  "decay1" : pick_time(time_hint),
                  "decay2" : pick_time(time_hint),
                  "release" : pick_time(time_hint),
                  "breakpoint" : coin(0.75, 0.75+rnd(0.25), rnd()),
                  "sustain" : coin(0.75, 0.5+rnd(0.5), rnd())},
              op1 = {
                  "ratio" : op_ratios[0],
                  "amp" : coin(0.75, 0, pick([-3, -3, -6, -6, -9, -12])),
                  "enable" : coin(0.90, 1, 0),
                  "x" : 0.0,
                  "lfo" : coin(0.75, 0, rnd()),
                  "break-point" : 60,
                  "right-scale": -3,
                  "left_scxale": 0,
                  "env" : select_carrier_envelope()},
              op4 = {
                  "ratio" : op_ratios[1],
                  "amp" : coin(0.75, 0, pick([-3, -3, -6, -6, -9, -12])),
                  "enable" : coin(0.90, 1, 0),
                  "x" : 0.0,
                  "lfo" : coin(0.75, 0, rnd()),
                  "break-point" : 60,
                  "right-scale": -3,
                  "left_scxale": 0,
                  "env" : select_carrier_envelope()},
              op7 = {
                  "ratio" : op_ratios[2],
                  "amp" : coin(0.75, 0, pick([-3, -3, -6, -6, -9, -12])),
                  "enable" : coin(0.90, 1, 0),
                  "x" : 0.0,
                  "lfo" : coin(0.75, 0, rnd()),
                  "break-point" : 60,
                  "right-scale": -3,
                  "left_scxale": 0,
                  "env" : select_carrier_envelope()},
              op3 = {
                  "ratio" : op_ratios[3],
                  "bias" : op_bias[0],
                  "amp" : coin(0.75, rnd(4), rnd(8)),
                  "enable" : coin(0.75, 1, 0),
                  "x" : 0.0,
                  "lfo" : coin(0.75, 0, rnd()),
                  "break-point" : 60,
                  "right-scale": -3,
                  "left_scxale": +3,
                  "env" : select_modulator_envelope()},
              op2 = {
                  "ratio" : op_ratios[4],
                  "bias" : op_bias[1],
                  "amp" : coin(0.75, rnd(4), rnd(8)),
                  "enable" : coin(0.90, 1, 0),
                  "x" : 0.0,
                  "lfo" : coin(0.75, 0, rnd()),
                  "break-point" : 60,
                  "right-scale": -3,
                  "left_scxale": +3,
                  "env" : select_modulator_envelope()},
              op5 = {
                  "ratio" : op_ratios[5],
                  "bias" : op_bias[2],
                  "amp" : coin(0.75, rnd(4), rnd(8)),
                  "enable" : coin(0.90, 1, 0),
                  "x" : 0.0,
                  "lfo" : coin(0.75, 0, rnd()),
                  "break-point" : 60,
                  "right-scale": -3,
                  "left_scxale": +3,
                  "env" : select_modulator_envelope()},
              op6 = {
                  "ratio" : op_ratios[6],
                  "bias" : op_bias[3],
                  "amp" : coin(0.75, rnd(4), rnd(8)),
                  "enable" : coin(0.90, 1, 0),
                  "x" : 0.0,
                  "lfo" : coin(0.75, 0, rnd()),
                  "break-point" : 60,
                  "right-scale": -3,
                  "left_scxale": +3,
                  "env" : select_modulator_envelope(),
                  "feedback" : coin(0.75, 0, rnd(2)),
                  "env->feedback" : coin(0.90, 0, rnd()),
                  "lfo->feedback" : coin(0.90, 0, rnd()),
                  "x->feedback" : 0.0},
              op8 = {
                  "ratio" : op_ratios[7],
                  "bias" : op_bias[4],
                  "amp" : coin(0.75, rnd(4), rnd(8)),
                  "enable" : coin(0.90, 1, 0),
                  "x" : 0.0,
                  "lfo" : coin(0.75, 0, rnd()),
                  "break-point" : 60,
                  "right-scale": -3,
                  "left_scxale": +3,
                  "env" : select_modulator_envelope(),
                  "feedback" : coin(0.75, 0, rnd(2)),
                  "env->feedback" : coin(0.90, 0, rnd()),
                  "lfo->feedback" : coin(0.90, 0, rnd()),
                  "x->feedback" : 0.0})
    return p
              
                  
              
    
        
