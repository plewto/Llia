# slug_constants

ULTRA_FAST = 0
FAST = 1
MEDIUM = 2
SLOW = 3
VERY_SLOW = 4

MAX_ENV_SEGMENT_TIME = 8
MAX_MOD_SCALE = 1000
MAX_PLUCK_MOD = 1000

FILTER_KEY_SCALES = ((-16000,"-16k"),
                     (-12000,"-12k"),
                     (-8000,"-8k"),
                     (-6000,"-6k"),
                     (-4000,"-4k"),
                     (-3000,"-3k"),
                     (-2000,"-2k"),
                     (-1000,"-1k"),
                     (-500,"-0.5k"),
                     (-200,"-0.2k"),
                     (-100,"-0.1k"),
                     (0,"0"),
                     (100,"+0.1k"),
                     (200,"+0.2k"),
                     (500,"+0.5k"),
                     (1000,"+1k"),
                     (2000,"+2k"),
                     (3000,"+3k"),
                     (4000,"+4k"),
                     (6000,"+6k"),
                     (8000,"+8k"),
                     (12000,"+12k"),
                     (16000,"+16k"))
                      
DB_KEY_SCALES = (-99, -18, -15,-12,-9,-6,-3,0,3,6,9,12,15)


MAX_PLUCK_DECAY = 12
PLUCK_HARMONICS = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)

_acc = []
_q = 24
while _q <= 96:
    octave = _q/12
    left = octave-2
    right = 8-octave
    txt = ("."*left)+str(octave)+("."*right)
    _acc.append((_q,txt))
    _q += 12
BREAK_KEYS = tuple(_acc)


