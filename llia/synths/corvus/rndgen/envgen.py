# llia.synths.corvus.rndgen.envgen
#

from llia.util.lmath import (rnd,coin,pick,random_sign)
from llia.synths.corvus.corvus_constants import *

def env_time_hint(pconfig={}):
    hint = pconfig.get("env-time-hint", None)
    pchange = pconfig.get("p-env-changeup",0.1)
    def select():
        return coin(0.75, coin(0.5,FAST,MEDIUM),coin(0.5,SLOW,GLACIAL))
    if not hint: hint = select()
    return coin(pchange, select(), hint)

def env_type_hint(pconfig={}):
    hint = pconfig.get("env-hint",None)
    pchange = pconfig.get("p-env-changeup",0.1)
    def select():
        return pick([GATE,ASR,ADSR,PERCUSSIVE])
    if not hint: hint = select()
    return coin(pchange, select(), hint)

def env(op,pconfig={}):
    type_hint = env_type_hint(pconfig)
    time_hint = env_time_hint(pconfig)
    def pick_time():
        if time_hint == FAST:
            rs =  0.0 + rnd(0.05)
        elif time_hint == MEDIUM:
            rs =  0.05 + rnd(0.5)
        elif time_hint == SLOW:
            rs =  0.5 + rnd(2)
        elif time_hint == GLACIAL:
            d = MAX_ENV_SEGMENT-2
            rs =  2 + rnd(d)
        else:
            rs =  rnd(MAX_ENV_SEGMENT)
        return round(rs,4)
    att=dcy1=dcy2=rel=0.0
    bp=sus=1.0
    mode=0
    if type_hint == PERCUSSIVE:
        att = round(coin(0.75, 0.0, rnd(0.05)),4)
        dcy1 = 0.5*pick_time()
        dcy2 = pick_time()
        rel = pick_time()
        bp = round(coin(0.75, 0.5+rnd(0.5), rnd()),4)
        sus = 0
        mode = coin(0.75, 0, 1)
    elif type_hint == GATE:
        att=dcy1=dcy2=rel = 0.0
        bp=sus = 1.0
        mode = 0
    elif type_hint == ASR:
        att = pick_time()
        rel = pick_time()
        dcy1=dcy2 = 0
        bp=sus = 1
        mode = 0
    else:
        att = pick_time()
        dcy1 = pick_time()
        dcy2 = pick_time()
        rel = pick_time()
        bp = round(coin(0.75, 0.5, rnd()),4)
        sus = round(coin(0.75, rnd(bp), rnd()),4)
        mode = coin(0.90, 0, 1)
    rs = {"op%d_attack" % op : att,
          "op%d_decay1" % op : dcy1,
          "op%d_decay2" % op : dcy2,
          "op%d_release" % op : rel,
          "op%d_breakpoint" % op : bp,
          "op%d_sustain" % op : sus,
          "op%d_env_mode" % op : mode}
    return rs
        
        
    

def pitch_env():
    rs = {}
    for a in (0,1,2,3,4):
        v = round(random_sign()*coin(0.5,0,rnd()),4)
        rs["pe_a%d" % a] = v
    for t in (1,2,3,4):
        v = round(rnd(MAX_ENV_SEGMENT), 4)
        rs["pe_t%d" % a] = v
    return rs
        
    
    
