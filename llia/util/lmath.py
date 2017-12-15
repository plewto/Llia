# llia.util.lmath
# 2016.03.27

from __future__ import print_function
from math import *

import random

# DEPRECIATED Use clip instead
# def clamp(n, mn, mx):
#     return min(max(n, mn), mx)

def logn(x, n):
    "Returns base n logarithm of x."
    return log10(x)/log10(n)

LOG2 = log10(2)
def log2(x):
    "Returns base 2 logarithm of x."
    return log10(x)/LOG2


MIN_DB = -99

def amp_to_db(amp):
    """
    Converts linear gain to db.
    For a gain of 0, return -99 (MIN_DB)
    """
    if amp == 0:
        return MIN_DB
    else:
        return 20*log10(abs(amp))

def db_to_amp(db):
    """
    Converts gain in db to linear gain.
    For gains less then MIN_DB return 0.0
    """
    if db <= MIN_DB:
        return 0.0
    else:
        return 10**(db/20.0)
    
def clip(n, lower, upper):
    """
    Clip value to given range
    lower <= n <= upper
    """
    return max(min(n, upper), lower)

def frequency_to_bpm(f):
    """
    Convert low frequency in Hertz to BPM.
    """
    return 60.0*f

def bpm_to_frequency(t):
    """
    Convert BPM to frequency i Hertz.
    """
    return t/60.0

def rnd(mult=1):
    """
    Returns random float between 0 and mult (default 1).
    """
    return mult*random.random()
    

def coin(p=0.5, heads=True, tails=False):
    """
    Execute one of two actions (heads or tails) at random.
    Either heads or tails may be callable or any value.
    If the selected item is not callable it becomes the function
    return value.   If the selected item is callable the coin
    returns the result of calling it.

    ARGS:
      p    - optional float, probability of head.
             0.0 <= p <= 1.0, default 0.5
      head - optional object, the heads result, default True.
      tail - optional object, the tails result, default False.


    RETURNS:
       Object, either heads or tails, or if they are callable,
       the result of heads() or tails().
    """
    rs = None
    if random.random() < p:
        rs = heads
    else:
        rs = tails
    if callable(rs):
        return rs()
    else:
        return rs

def random_sign(p=0.5, mult=1):
    """
    Select sign at random.

    ARGS:
      p    - optional float, probability of positive, default 0.5
      mult - optional float, multiplier, default 1.0

    RETURNS:
      float, either -mult or +mult.
    """
    return abs(mult)*coin(p, 1, -1)

def approx(n, range_ = 0.01):
    """
    Return approximate value.

    ARGS:
      n       - float, the mean value.
      range_  - float, maximum distance from mean expressed as a ratio.

    RETURNS:
      float, m where n-(n*range_) <= m n+(n*range_)
    """
    q = n*range_
    r = random_sign(mult=q*random.random())
    return n+r

def pick(seq):
    """
    Return random element from sequence.
    """
    return random.choice(seq)

def distance(x0,y0,x1,y1):
    """
    Return distance between two points (x0,y0) and (x1,y1).
    """
    dx = x1-x0
    dy = y1-y0
    return sqrt(dx*dx+dy*dy)
