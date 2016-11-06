# llia.synths.algo.algogen.ampgen
#
# Select operstor amplitudes
#

from llia.util.lmath import (rnd,coin,pick)


def _principle_stack():
    return pick("ABC")

def _round(n):
    return round(n,3)

def carrier_amps():
    ps = _principle_stack()
    a,b,c = 0,0,0
    def pick_amps():
        q = coin(0.1, 1.0, coin(0.75, 0.3+rnd(0.7), coin(0.5, rnd(0.3),0)))
        r = coin(0.1, 1.0, coin(0.75, 0.3+rnd(0.7), coin(0.5, rnd(0.3),0)))
        return 1.0,_round(r),_round(q)
    if ps == "A":
        a,b,c = pick_amps()
    elif ps == "B":
        b,a,c = pick_amps()
    else:
        c,a,b = pick_amps()
    return a,b,c



def _pick_mod_scale(p_deep_modulation=0.1):
    s = coin(p_deep_modulation,
             coin(0.75, pick((1e2,1e3)), pick((1e4,1e5))),
             coin(0.50, 1,10))
    return s

def modulation_scales(p_deep_modulation=0.1):
    acc = []
    for i in range(8):
        acc.append(_pick_mod_scale(p_deep_modulation))
    return acc

def operator_amps():
    a,b,c = carrier_amps()
    def modamp():
        return _round(rnd())
    acc = [a,modamp(),modamp(),
           modamp(),b,modamp(),
           c,modamp()]
    return acc
           

