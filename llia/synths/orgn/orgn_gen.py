# llia.synths.organ.orgn_gen

from __future__ import print_function
from random import randrange
from llia.synths.orgn.orgn_data import orgn
from llia.util.lmath import *

def _pick_time_scale():
    ts = coin(0.80, "NORMAL",
              (coin, 0.50, "SLOW", "FAST"))
    return ts

def _pick_env_time(tscale):
    if coin(0.1):
        ts = None
        while ts != tscale:
            ts = _pick_time_scale()
        return _pick_env_time(ts)
    elif tscale == "NORMAL":
        return rnd(0.5)
    elif tscale == "FAST":
        return rnd(0.1)
    else:
        return 0.5 + rnd(4)
    
def _fill_env_list(tscale):
    if coin(0.25):
        acc = [0.00, 0.00, 1.00, 0.00]
    else:
        acc = [_pick_env_time(tscale),
               _pick_env_time(tscale),
               coin(0.75, 0.5+rnd(0.5), rnd()),
               _pick_env_time(tscale)]
    return acc

def _select_harmonic_mode():
    return coin(0.90, "HARMONIC", "RANDOM")


def _select_op_ratio(hmode):
    if hmode == "HARMONIC":
        plist = [0.5, 0.5, 0.75,
                 1, 1, 1, 1, 1.5, 1.5,
                 2, 2, 2, 2, 2.25, 3, 3,
                 4, 5, 6, 8]
        return pick(plist)
    else:
        return 0.5+rnd(8)


def gen_orgn_program(slot=127, *_):
    tscale = _pick_time_scale()
    hmode = _select_harmonic_mode()
    p = orgn(slot, "Random", amp = -12,
             cenv = _fill_env_list(tscale),
             menv = _fill_env_list(tscale),
             op1 = [_select_op_ratio(hmode), 0],
             op3 = [_select_op_ratio(hmode), pick([0, -3, 6, -9, -12])],
             op2 = [_select_op_ratio(hmode), rnd()],
             op4 = [_select_op_ratio(hmode), rnd()],
             vibrato = [2 + rnd(7),
                        coin(0.5, 0.0, rnd(4)),
                        coin(0.5, 0.0, coin(0.75, rnd(0.1), rnd())),
                        0.0],
             chorus = [coin(0.5, 0.0, rnd(4)),
                       coin(0.5, 0.0, rnd(1))],
             mod_depth = [1.0, 0.0])
    return p
             
             
             
             
             
             
    
         
         
         
