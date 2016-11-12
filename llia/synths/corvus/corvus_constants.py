# llia.synths.corvus.corvus_constants

from __future__ import print_function
from fractions import Fraction

CFILL = "black"
CFOREGROUND = "white"
COUTLINE = "white"

KEYSCALES = (-18,-15,-12,-9,-6,-5,-4,-3,-2,-1,0,
             1,2,3,4,5,6,9,12,15,18)

_acc = []
_n = 0
while _n < 128:
    _acc.append(_n)
    _n += 6
KEYBREAK = tuple(_acc)


MODSCALES = (0,1,2,3,4)
             
MAX_ENV_SEGMENT = 8



_acc = [(round(1.0/16,3),"1/16")]
for n in range(7):
    v = (n+1)/8.0
    f = Fraction(n+1,8)
    _acc.append((v,str(f)))

_acc.append((1.0,"1"))
for n,d in ((1,8),(1,4),(1,3),(3,8),(1,2),(5,8),(2,3),(3,4),(7,8)):
    f = Fraction(n,d)
    v = round(float(1 + f), 3)
    tx = "1 %s" % f
    _acc.append((v,tx))
for v in range(2,17):
    _acc.append((float(v), str(v)))

# ((float,str),(float,str)...)
LFO_RATIOS = tuple(_acc)
            
_acc= []
for i in range(1,10,1):
    _acc.append(i)
for i in range(10,100, 10):
    _acc.append(i)
for i in range(100,1100,100):
    _acc.append(i)
NOISE_BANDWIDTHS = tuple(_acc)


PENV_HOLD_NODES = (0,1,2,3,4)
PENV_LOOP_NODES = (0,1,2)
