# llia.synths.lfo3.lfo3_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance

# HARMONICS = [0.125, 0.25, 0.375, 0.5, 0.675,0.75,0.875,
#              1, 1.125, 1.25, 1.5, 1.75,
#              2, 2.25, 2.5, 3, 4, 5, 6, 7, 8, 9, 12, 16] 

HARMONICS = ((0.125, "1/8"),
             (0.25, "1/4"),
             (0.375, "3/8"),
             (0.5, "1/2"),
             (0.675,"5/8"),
             (0.75,"3/4"),
             (0.875,"7/8"),
             (1, "1"),
             (1.125, "1 1/8"),
             (1.25, "1 1/4"),
             (1.5, "1 1/2"),
             (1.75,"1 3/4"),
             (2, "2"),
             (2.25, "2 1/4"),
             (2.5, "2 1/5"),
             (3, "3"),
             (4, "4"),
             (5, "5"),
             (6, "6"),
             (7, "7"),
             (8, "8"),
             (9, "9"),
             (12, "12"),
             (16, "16"))

prototype = {
    "lfoScale" : 1.0,      # Common scale factor  (1/4 ... 4)
    "lfoBias" : 0,         # Common bias (-4 ... +4)
    "lfoFreq" : 1.0,       # Common frequency (0.01 ... 100)
    "lfoModFreq" : 1,      # restric to harmonics
    "lfoFM" : 0.0,         # MOD LFO -> FM depth (0 ... 4) 
    "lfoAM" : 0.0,         # MOD LFO -> AM depth (0 ... 1)


    "lfoDelay" : 0.0,      # env onset delay (0 ... 8)
    "lfoAttack" : 0.0,     # env attack time (0 ... 8)
    "lfoHold" : 1.0,       # env hold time (0 ... 8)
    "lfoRelease" : 0.0,    # env release time (0 ... 8)
    "lfoEnvToFreq" : 0.0,  # env -> LFO freq (0 ... 4)
    "lfoBleed" : 1.0,      # amp envelope signal bleed (0 ... 1)

    
    "lfoRatioA" : 1.0,     # LFO A freq ratio (restric to harmonics)
    "lfoRatioB" : 1.0,     # LFO B freq ratio (restric to harmonics)
    "lfoRatioC" : 1.0,     # LFO C freq ratio (restric to harmonics)
    "lfoAmpA" : 1.0,       # LFO A amp (0 ... 1)
    "lfoAmpB" : 1.0,       # LFO B amp (0 ... 1)
    "lfoAmpC" : 1.0        # LFO C amp (0 ... 1)
}

class Lfo3(Program):

    def __init__(self, name):
        super(Lfo3, self).__init__(name, "LFO3", prototype)
        self.performance = performance()

program_bank = ProgramBank(Lfo3("Init"))
program_bank.enable_undo = False

def _fill(lst, template):
    acc = []
    for i,dflt in enumerate(template):
        try:
            v = lst[i]
        except IndexError:
            v = dflt
        acc.append(float(v))
    return acc
                   

def lfo3(slot, name,
         freq = 1.0,
         ratios = [1.0, 1.0, 1.0],
         amps = [1.0, 1.0, 1.0],
         env = [0.0, 0.0, 0.0, 0.0],    # [delay attack hold release]
         am = [1.0, 0.0],               # [bleed, mod-lfo]
         fm = [0.0, 0.0],               # [env, mod-lfo]
         mod_freq = 1.0,                # mod osc frequency
         scale = 1.0,
         bias = 0.0):
    ratios = _fill(ratios, [1,1,1])
    amps = _fill(amps, [1,1,1])
    env = _fill(env, [0,0,0,0])
    am = _fill(am, [1,0])
    fm = _fill(fm, [0,0])
    p = Lfo3(name)
    p["lfoScale"] = float(scale)
    p["lfoBias"] = float(bias)
    p["lfoFreq"] = float(freq)
    p["lfoModFreq"] = float(mod_freq)
    p["lfoFM"] = fm[1]
    p["lfoAM"] = am[1]
    p["lfoEnvToFreq"] = fm[0]
    p["lfoBleed"] = am[0]
    p["lfoDelay"] = env[0]
    p["lfoAttack"] = env[1]
    p["lfoHold"] = env[2]
    p["lfoRelease"] = env[3]
    p["lfoRatioA"] = ratios[0]
    p["lfoRatioB"] = ratios[1]
    p["lfoRatioC"] = ratios[2]
    p["lfoAmpA"] = amps[0]
    p["lfoAmpB"] = amps[1]
    p["lfoAmpC"] = amps[2]
    program_bank[slot] = p
    return p

def pp(program, slot=127):
    pad = ' '*5
    
    def fval(key):
        return float(program[key])

    def values(*keys):
        bcc = [pad]
        for k in keys:
            v = fval(k)
            bcc.append(v)
        return tuple(bcc)
    acc = 'lfo3(%d, "%s",\n' % (slot, program.name)
    acc += '%sfreq = %5.3f,\n' % (pad, fval("lfoFreq"))
    frmt = '%sratios = [%5.3f, %5.3f, %5.3f],\n'
    vlst = values('lfoRatioA','lfoRatioB','lfoRatioC')
    acc += frmt % vlst
    frmt = '%samps = [%5.3f, %5.3f, %5.3f],\n'
    vlst = values('lfoAmpA','lfoAmpB','lfoAmpC')
    acc += frmt % vlst
    frmt = '%senv = [%5.3f, %5.3f, %5.3f, %5.3f],\n'
    vlst = values('lfoDelay','lfoAttack','lfoHold','lfoRelease')
    acc += frmt % vlst
    frmt = '%sam = [%5.3f, %5.3f],\n'
    vlst = values('lfoBleed','lfoAM')
    acc += frmt % vlst
    frmt = '%sfm = [%5.3f, %5.3f],\n'
    vlst = values('lfoEnvToFreq', 'lfoFM')
    acc += frmt % vlst
    acc += '%smod_freq = %5.3f,\n' % (pad, fval('lfoModFreq'))
    acc += '%sscale = %5.3f,\n' % (pad, fval('lfoScale'))
    acc += '%sbias = %5.3f)\n' % (pad, fval('lfoBias'))
    return acc



lfo3(0, "Tripartite",
     freq = 1.000,
     ratios = [1.000, 1.000, 1.000],
     amps = [1.000, 1.000, 1.000],
     env = [0.000, 0.000, 0.000, 0.000],
     am = [1.000, 0.000],
     fm = [0.000, 0.000],
     mod_freq = 1.000,
     scale = 1.000,
     bias = 0.000)

lfo3(1, "Syncopated 1:2:3",
     freq = 1.000,
     ratios = [1.000, 2.000, 3.000],
     amps = [1.000, 1.000, 1.000],
     env = [0.000, 0.000, 0.000, 0.000],
     am = [1.000, 0.000],
     fm = [0.000, 0.000],
     mod_freq = 1.000,
     scale = 1.000,
     bias = 0.000)

lfo3(2, "Syncopated 2",
     freq = 1.500,
     ratios = [1.000, 1.500, 1.000],
     amps = [1.000, 1.000, 1.000],
     env = [0.000, 0.000, 1.000, 0.000],
     am = [1.000, 0.965],
     fm = [0.000, 0.000],
     mod_freq = 0.500,
     scale = 1.000,
     bias = 0.000)

lfo3(3, "Delayed Complex 1",
     freq = 4.500,
     ratios = [1.500, 2.000, 4.000],
     amps = [1.000, 0.191, 0.141],
     env = [0.898, 2.000, 1.000, 0.952],
     am = [0.000, 0.000],
     fm = [0.000, 0.000],
     mod_freq = 0.500,
     scale = 0.300,
     bias = 0.000)

lfo3(4, "100 Hz",
     freq = 99.000,
     ratios = [1.000, 2.000, 3.000],
     amps = [1.000, 0.523, 0.342],
     env = [0.442, 1.549, 1.000, 1.037],
     am = [0.000, 0.146],
     fm = [0.000, 0.000],
     mod_freq = 0.125,
     scale = 1.000,
     bias = 0.000)

