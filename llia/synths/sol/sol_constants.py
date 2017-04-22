# llia.synths.sol.sol_constants

from fractions import Fraction

MAX_LFO_DELAY = 4.0
MAX_ENV_SEGMENT_TIME = 16

def r(n,d):
    return Fraction(n,d)

LFO_RATIOS = [16,15,12,9,8,6,5,4,3,
              r(9,4),2,r(3,2),1,
              r(7,8),
              r(3,4),
              r(2,3),
              r(5,8),
              r(1,2),
              r(1,3),
              r(3,8),
              r(1,4),
              r(1,5),
              r(1,6),
              r(1,8),
              r(1,9),
              r(1,10),
              r(1,12),
              r(1,16),
              r(1,20),
              r(1,24),
              r(1,32),
              r(1,40),
              r(1,48),
              r(1,64),
              r(1,80),
              r(1,96),
              r(1,128),
              r(1,192),
              r(1,256)]
LFO_RATIOS.sort()
