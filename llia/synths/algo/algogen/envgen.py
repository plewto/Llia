# llia.synths.algo.algogen.envgen
#
# Random envelope generator

from llia.util.lmath import (rnd,coin,approx,pick)
from llia.synths.algo.algo_constants import *

verbose=True


# Envelope times
#

def pick_env_time_hint(is_percussive=None):
    if is_percussive:
        h = pick((MEDIUM,MEDIUM,
                  SLOW,SLOW,SLOW,SLOW,SLOW,SLOW,SLOW,
                  GLACIAL))
    else:
        h = coin(0.75,
                 pick((ULTRA_FAST,FAST,MEDIUM)),
                 pick((ULTRA_FAST,FAST,MEDIUM,SLOW,GLACIAL,FULL)))
    return h

def pick_env_segment_time(hint=FULL, p_changeup=0.1):
    hint = coin(p_changeup, pick_env_time_hint(),hint)
    mn,mx = 0.0,MAX_ENV_SEGMENT
    try:
        mn,mx = {ULTRA_FAST : (0.00, 0.01),
                 FAST : (0.00, 0.10),
                 MEDIUM : (0.10, 1.0),
                 SLOW : (1.0,4.0),
                 GLACIAL : (4.0,MAX_ENV_SEGMENT)}[hint]
    except KeyError:
        pass
    return mn+rnd(mx-mn)

# hint - envelope time hint
#        If None, select a hint
# p_changeup - probability of using a different hint
#
# returns tuple (attack,decay1,decay2,release) times
#
def pick_envelope_times(hint=None,p_changeup=0.1):
    hint = hint or pick_env_time_hint()
    acc = []
    for i in range(4):
        t = pick_env_segment_time(hint,p_changeup)
        acc.append(t)
    return tuple(acc)

# if not hint, select one
# with probability p_changeup, select another hint
# returns one of constants: GATE,PERCUSSIVE,ASR,ADSR
#
def pick_env_type_hint(hint=None, p_changeup=1.0):
    hint = hint or pick((GATE,
                         PERCUSSIVE,PERCUSSIVE,PERCUSSIVE,PERCUSSIVE,
                         ADSR,ADSR,ADSR,ADSR,
                         ASR,ASR))
    #hint = coin(p_changeup, pick_env_type_hint(None,0), hint)
    if coin(p_changeup):
        return pick_env_type_hint(hint,0)
    return hint

def _round_env_values(envlst):
    acc = []
    for v in envlst[:-1]:
        acc.append(round(v,4))
    acc.append(envlst[-1])
    return acc

def status(etype,time_hint):
    if verbose:
        print("Env type = %s, time_hint = %s" % (etype,ENV_TIME_NAMES[time_hint]))

def _gate_envelope(*_):
    status("gate", None)
    return (0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0)
    
def _asr_envelope(time_hint):
    status("ASR", time_hint)
    att,dcy1,dcy2,rel = pick_envelope_times(time_hint,0.0)
    bp = sus = 1.0
    return _round_env_values((att,dcy1,dcy2,rel,bp,sus,0))

def _adsr_envelope(time_hint):
    status("ADSR", time_hint)
    att,dcy1,dcy2,rel = pick_envelope_times(time_hint,0.0)
    sus = coin(0.75, 0.5+rnd(0.5),rnd())
    bp = coin(0.50, sus, sus+rnd(1-sus))
    return _round_env_values((att,dcy1,dcy2,rel,bp,sus,0))

def _percussive_envelope(time_hint):
    if time_hint < MEDIUM:
        time_hint = pick_env_time_hint(True)
    status("Percussive", time_hint)
    junk,dcy1,dcy2,rel = pick_envelope_times(time_hint,0.0)
    att = coin(0.80, 0.00, rnd(0.01))
    dcy1, dcy2 = min(dcy1,dcy2),max(dcy1,dcy2)
    if dcy1 > 1:
        dcy1 = coin(0.75, rnd(), dcy1)
    if dcy2 < 0.5:
        dcy2 = coin(0.25, dcy2, pick((dcy1*2,dcy1*3,dcy1*4)))
    bp = coin(0.50,rnd(0.75),0.75)
    sus = coin(0.90, 0.0, rnd(0.12))
    return _round_env_values((att,dcy1,dcy2,rel,bp,sus,0))


# p_duplicate_carrier - probability modulator env will be same as carrier
#                       has priority over p_type_change and p_time_change
# returns nested tuple of 3 envelopes,  carrier env is at index 0
# 
def _pick_stack_envelopes(type_hint=None,
                          time_hint=None,
                          p_type_changeup=0.1,
                          p_time_changeup=0.1,
                          p_duplicate_carrier=0.35):
    acc = []
    type_hint = type_hint or pick_env_type_hint()
    time_hint = time_hint or pick_env_time_hint()
    for i in range(3):
        if i > 0 and coin(p_duplicate_carrier):
            acc.append(acc[0])
        else:
            env_type = pick_env_type_hint(type_hint,p_type_changeup)
            tihint = coin(p_time_changeup, pick_env_time_hint(), time_hint)
            if env_type == ADSR:
                acc.append(_adsr_envelope(tihint))
            elif env_type == ASR:
                acc.append(_asr_envelope(tihint))
            elif env_type == PERCUSSIVE:
                acc.append(_percussive_envelope(tihint))
            else:
                acc.append(_gate_envelope())
    return tuple(acc)


# Returns nested tuple of 8 envelopes in operator order
# Envelopes are specified as tuple
# (attack,decay1,decay2,release,breakpoint,sustain,mode)
#
def pick_envelopes(type_hint=None,
                   time_hint=None,
                   p_type_changeup=0.1,
                   p_time_changeup=0.1,
                   p_duplicate_carrier=0.35):
    type_hint = type_hint or pick_env_type_hint()
    time_hint = time_hint or pick_env_time_hint()
    acc = []
    for stk in "ABC":
        tyhint = coin(p_type_changeup,pick_env_type_hint(),type_hint)
        tihint = coin(p_time_changeup,pick_env_time_hint(),time_hint)
        stack = _pick_stack_envelopes(tyhint,tihint,p_type_changeup,p_time_changeup)
        if stk == "A":
            for e in stack: acc.append(e)
        elif stk == "B":
            acc.append(stack[1])
            acc.append(stack[0])
            acc.append(stack[2])
        else:
            acc.append(stack[0])
            acc.append(stack[1])
    return acc
                
