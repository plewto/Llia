# llia.synths.m.m_constants

from llia.util.frange import frange


# Pallet
CFILL = 'black'
CFOREGROUND = 'white'
CPOS_FOREGROUND = '#ace6ac'
CNEG_FOREGROUND = 'red'
COUTLINE = 'blue'


BREAKKEYS = tuple(range(0,128,6))
KEYSCALES = tuple(range(-18,21,3))

LFO_RATIOS = (0.01,0.02,0.04,0.08,0.10,0.125,0.250,0.333,0.50,0.667,
              0.75,1.00,1.333,1.50,1.667,2,3,4,5,6,8)
LFO_DELAYS = tuple(frange(0,4,0.5))
TREMOLO = tuple(frange(0,1,0.1))
ENVPITCH = tuple(frange(-1.0, 2.0, 0.2))


                      
# Tone A
#
A_QUOTIENTS = tuple(range(1,17))
A_Q_LFO = tuple(range(0,9))
A_Q_ENV = tuple(range(-8,9,1))
A_Q_EXTERNAL = A_Q_ENV
A_PW = tuple(frange(0,4,0.2))
A_PW_LFO = A_PW
A_PW_ENV = tuple(frange(-4,4,0.2))
A_PW_EXTERNAL = A_PW_ENV
A_CLK_MIX = tuple(frange(0,1,0.2))

# Tone B
#
B_N = tuple(range(1,33))
B_N_LFO = tuple(range(0,33))
B_N_ENV = tuple(range(-32,33))
B_N_EXTERNAL = B_N_ENV
B_N2_LAG = tuple(frange(0,2,0.2))
B_N2_POLARITY = (-1,0,1)


# Tone C
#
C_FB = (-1,0,1)
C_PRATIO = [0.01, 0.1, 0.125, 0.25, 0.333, 0.50, 0.667, 0.75, 1.0,
            1.5, 2, 3, 4, 5, 6, 7, 8]
C_PRATIO_LFO = [0]+C_PRATIO
C_PRATIO_ENV = C_PRATIO_LFO
C_PW = tuple(frange(0,1,0.1))


# Noise
#
NOISE_LP_RANGE = (100,10000)
NOISE_HP_RANGE = (10,4000)

def msb_aspect(msb,index,value,text=None):
    if value >= 0:
        foreground = CPOS_FOREGROUND
    else:
        foreground = CNEG_FOREGROUND
    if text is None:
        text = str(value)    
    d = {'fill' : CFILL,
         'foreground' : foreground,
         'outline' : COUTLINE,
         'value' : value,
         'text' : text}
    msb.define_aspect(index,value,d)
    return d
         
def define_aspects(msb,lst):
    for i,v in enumerate(lst):
        a=msb_aspect(msb,i,lst[i])
    msb.update_aspect()
    return msb
