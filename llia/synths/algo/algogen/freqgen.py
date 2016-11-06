# llia.synths.algo.algogen.freqgen
#
# Functions for selecting operator frequencies
#

from llia.synths.algo.algo_constants import *
from llia.util.lmath import (coin,pick,rnd,approx)

verbose=True


# Return operator frequency ratio
# p_harmonic -> probability of value from harmonics list
#
def _pick_op_ratio(p_harmonic=0.75):
    return coin(p_harmonic, pick(HARMONICS),
                coin(0.75, 0.5+rnd(3), 0.5+rnd(8)))


def _pick_op_bias(p_harmonic=0.75, p_nonzero=0.10):
    return coin(p_harmonic,
                coin(p_nonzero, rnd(),0),
                coin(p_nonzero, rnd(90),0))


def _round(lst):
    acc = []
    for p in lst:
        acc.append(round(p,4))
    return tuple(acc)


# Returns nested tuples:
#  ((op_ratios...)(op_bias...))
#
def pick_frequencies(p_harmonic=None):
    if p_harmonic is None:
        p_harmonic = coin(0.75, 0.90, rnd())
    if verbose:
        print("Probability of harmonic frequencies: %s" % p_harmonic)
    acc,bcc = [],[]
    for i in range(8):
        acc.append(_pick_op_ratio(p_harmonic))
        bcc.append(_pick_op_bias(p_harmonic))
    return _round(acc),_round(bcc)
                   
