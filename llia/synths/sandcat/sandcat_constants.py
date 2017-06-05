# llia.synths.sanscat.sandcat_constants

EX_HARMONICS = tuple(range(1,9))
EX_HARMONICS_MOD = tuple(range(-8,9))
EX_PW =  (0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9)
EX_PWM = (0.0,0.1,0.2,0.3,0.4,0.5)
MAX_ENV_SEGMENT = 8.0
MAX_RELEASE_SEGMENT = 16
MAX_FILTER_CUTOFF = 16000
MAX_FILTER_MOD = 8000
MAX_FILTER_TRACK = 2
FILTER_SLIDER_DEGREE = 3

# Brackets indicate source is gated.
#    foo   -> non-gated
#    [foo] -> gated
#
TRIGER_SOURCES = ((0,"[Gate]"),
                  (1,"[Clock 1]"),
                  (2,"[Clock 2]"),
                  (3,"[LFO 1]"),
                  (4,"[LFO 2]"),
                  (5,"[Extern 1]"),
                  (6,"[Extern 2]"),
                  (7,"[Random 1]"),
                  (8,"[Random 2]"),
                  (9,"Clock 1"),
                  (10,"Clock 2"),
                  (11,"LFO 1"),
                  (12,"LFO 2"),
                  (13,"Extern 1"),
                  (14,"Extern 2"),
                  (15,"Random 1"),
                  (16,"Random 2")) 

BREAK_KEYS = ((24,"24......"),
              (36,".36....."),
              (48,"..48...."),
              (60,"...60..."),
              (72,"....72.."),
              (84,".....84."),
              (96,"......96"))

KEY_SCALES = (-99,-48,-24,-18,-15,-12,-9,-6,-3,0,3,6,9,12,15,18)
MAX_FM_DEPTH = 5000
FM_SLIDER_DEGREE = 6
MAX_LFO_XMOD = 16

