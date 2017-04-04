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
              3.0, 4.0, 5.0, 6.0, 8.0,
              12,16,24,32)

MAX_ENV_SEGMENT_TIME = 12
CLUSTER_RANGE = (0,1)

HARMONICS = [1,2,3,4,6,8,12,16,24,32,48,64]
HARMONIC_COUNT_RANGE = (HARMONICS[0],HARMONICS[-1])
HARMONIC_MOD_RANGE = [0]+HARMONICS

acc = []
for r in reversed(HARMONICS):
    acc.append(-r)
acc.append(0)
POLAR_HARMONIC_MOD_RANGE = acc + HARMONICS

FILTER_FREQUENCIES = [67,125,250,500,750,1000,2000,4000,6000,8000,12000,16000]
acc=[]
for f in reversed(FILTER_FREQUENCIES):
    acc.append(-f)
acc.append(0)
FILTER_MOD_VALUES = acc+FILTER_FREQUENCIES
FILTER_RANGE = (FILTER_FREQUENCIES[0],FILTER_FREQUENCIES[-1])
FILTER_MOD_RANGE = (FILTER_MOD_VALUES[0],FILTER_MOD_VALUES[-1])

FILTER_2B_OFFSETS = (-2400,-1600,-800,-600,-400,-300,-200,0,200,300,400,600,800,1200,1600,2400)

NEGATIVE_FILL_COLOR = "#380407"
POSITIVE_FILL_COLOR = "black"
NORMAL_MOD_DEPTH_COLOR = None
MODERATE_MOD_DEPTH_COLOR = "orange"
DEEP_MOD_DEPTH_COLOR = "yellow"
