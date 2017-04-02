# llia.synths.klstr2.constants

LFO_RATIOS = (1/8.0,
              1/4.0,
              1/3.0,
              1/2.0,
              2/3.0,
              3/4.0,
              1.0,
              5/4.0,
              4/3.0,
              3/2.0,
              5/3.0,
              7/4.0,
              2.0, 2.5,
              3.0, 4.0, 5.0, 6.0, 8.0)

MAX_ENV_SEGMENT_TIME = 30
CLUSTER_RANGE = (0,4)
HARMONIC_COUNT_RANGE = (1,64)
HARMONIC_MOD_RANGE = (-HARMONIC_COUNT_RANGE[1],HARMONIC_COUNT_RANGE[1])
LOWPASS_RANGE = (50,16000)
HIGHPASS_RANGE = LOWPASS_RANGE
FILTER_MOD_RANGE = (-LOWPASS_RANGE[1],LOWPASS_RANGE[1])
