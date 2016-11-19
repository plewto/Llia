# llia.synths.io.io_constants

CFILL = "black"
CFOREGROUND = "WHITE"
COUTLINE = CFOREGROUND

_acc = []
_kn = 0
while _kn<128:
    _acc.append(_kn)
    _kn += 6
KEY_BREAKPOINTS = tuple(_acc)

_acc = []
_db = -18
while _db<18:
    _acc.append(_db)
    _db+=3
KEY_SCALES = tuple(_acc)


MAX_ENV_SEGMENT_TIME = 8
MAX_BLIP_SEGMENT_TIME = 1


NOISE_RATIOS = (1,2,3,4,6,8)
TREMOLO_RATIOS = ((0.125, "1/8"),
                  (0.25,  "1/4"),
                  (0.50,  "1/2"),
                  (0.75,  "3/4"),
                  (1.00,   "1"),
                  (1.25,   "1 1/4"),
                  (1.333,  "1 1/3"),
                  (1.50,   "1 1/2"),
                  (1.667,   "1 2/3"),
                  (1.75,    "1 3/4"),
                  (2.00,    "2"),
                  (3.00,    "3"),
                  (4.00,    "4"))

MAX_MOD_DEPTH = 16
