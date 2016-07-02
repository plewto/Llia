# llia.synths.stepfilter.sf_constants
# 2016.07.02


# Pulse ratio gamuts, min 0.125, mac 8.000, resolution 0.125
#
DEFAULT_GAMUT = [0.5, 0.75, 1, 2, 3, 4, 5, 6]
HARMONIC_GAMUT = [1, 2, 3, 4, 5, 6, 7, 8]
ODD_GAMUT = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 7.5]
CLUSTER_GAMUT = [0.125, 0.250, 0.375, 0.500, 3.000, 3.125, 3.250, 3.50]

FILTER_FREQUENCIES = [100, 150, 200, 300, 400, 600, 800,
                      1200, 2400, 3200, 4800, 6400, 9600, 12800]

# B LFO frequency ratios realtive to LFO.
#
BLFO_RATIOS = [0.5, 0.75, 1, 1.5, 2, 3, 4]


# LFO frequency relative to clock.   Used only by random generator.
#
LFO_FREQUENCIES = [0.1, 0.2, 0.25, 0.333, 0.5, 0.75, 1,
                   1.5, 2, 3, 4, 5, 6, 8]
