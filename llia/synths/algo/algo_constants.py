# llia.synths.algo.algo_constants

CFILL = "black"
CFOREGROUND = "white"
COUTLINE = "white"

MOD_RANGE_COUNT = 6
KEYSCALES = (-18,-12,-9,-6,-3,0,3,6,9,12,18)
LFO_RATIOS = ((0.125,"1/8"),
              (0.250,"1/4"),
              (0.375,"3/8"),
              (0.500,"1/2"),
              (0.625,"5/8"),
              (0.750,"3/4"),
              (0.875,"7/8"),
              (1.000,"1"),
              (1.250,"1 1/4"),
              (4/3.0, "1 1/3"),
              (1.500, "1 1/2"),
              (5/3.0, "1 2/3"),
              (1.750, "1 3/4"),
              (2.000, "2"),
              (2.500, "2 1/2"),
              (3.000, "3"),
              (4.000, "4"),
              (5.000, "5"),
              (6.000, "6"),
              (8.000, "8"),
              (9.000, "9"),
              (12.00, "12"),
              (16.00, "16"))

_a = range(0,128,12)
_b = range(6,128,12)
_c = _a+_b
_c.sort()
KEY_BREAKPOINTS = tuple(_c)

MAX_ENV_SEGMENT = 12


HARMONICS = []
for n,f in (( 1, 0.25),
            ( 8, 0.50), 
            ( 3, 0.75),
            (24, 1.00),
            ( 3, 1.333),
            ( 8, 1.5),
            (24, 2.0),
            (18, 3.0),
            (12, 4.0),
            ( 7, 5.0),
            ( 9, 6.0),
            ( 1, 7.0),
            ( 6, 8.0),
            ( 4, 9.0),
            ( 2,10.0),
            ( 2,12.0),
            ( 1,16.0)):
    for i in range(n):
        HARMONICS.append(f)

# Envelope times
#

ULTRA_FAST = 1
FAST = 2
MEDIUM = 3
SLOW = 4
GLACIAL = 5
FULL = 6


ENV_TIME_NAMES = {ULTRA_FAST : "Ultra-fast",   # (0.00, 0.01)
                  FAST : "Fast",               # (0.00, 0.10)
                  MEDIUM : "Medium",           # (0.10, 1.00)
                  SLOW : "Slow",               # (1.00, 4.00)
                  GLACIAL : "Glacial",         # (4.00, 12.0)
                  FULL : "Full",               # (0.00, 12.0)
                  None : ""}

# Envelope contours
#
GATE = 1
PERCUSSIVE = 2
ASR = 3
ADSR = 4

