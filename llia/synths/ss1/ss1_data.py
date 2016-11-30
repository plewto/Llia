# llia.synths.ss1.ss1_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance
from llia.util.lmath import coin,rnd,pick,random_sign


# Constants

HIGHPASS_CUTOFF = [10,100,500,1000]
LOWPASS_CUTOFF = [10,100,200,400,800,1600,3200,6400,
                  10000,16000]
MID_CUTOFF = ((LOWPASS_CUTOFF[0]+LOWPASS_CUTOFF[-1])/2)
LOWPASS_TRACK = [0,1,2,4]

CFILL = "black"
CFOREGROUND = "white"
COUTLINE = CFOREGROUND

prototype = {
    "port" : 0.0,
    "vsens" : 0.1,
    "vdepth" : 0.0,
    "xPitch" : 0.0,
    "chorus" : 0,
    "lfoFreq" : 7.0,
    "lfoWave" : 0,
    "lfoDelay" : 0.0,
    "lfoAmp" : 0.0,
    "attack" : 0.0,
    "decay" : 0.1,
    "sustain" : 1.0,
    "release" : 0.1,
    "sawMix" : 0.0,
    "pulseMix" : 0.5,
    "subOctave" : 0,
    "subMix" : 0.0,
    "noiseSelect" : 0,
    "noiseMix" : 0.0,
    "wave" : 0.5,
    "waveLFO" : 0.0,
    "waveEnv" : 0.0,
    "highPass" : 10,
    "filterFreq" : 10000,
    "filterTrack" : 0,
    "filterLFO" : 0,
    "filterEnv" : 0,
    "xFilter" : 0,
    "filterRes" : 0.0,
    "gateMode" : 0,
    "amp" : 0.3}


class SS1(Program):

    def __init__(self,name):
        super(SS1,self).__init__(name,SS1,prototype)
        self.performance = performance()

program_bank = ProgramBank(SS1("Init"))
program_bank.enable_undo = False

def ss1(slot, name,
        port = 0.0,
        vsens = 0.1,
        vdepth = 0.0,
        xPitch = 0.0,
        chorus = 0,
        lfoFreq = 7.0,
        lfoWave = 0,
        lfoDelay = 0.0,
        lfoAmp = 0.0,
        attack = 0.0,
        decay = 0.1,
        sustain = 1.0,
        release = 0.1,
        sawMix = 0.0,
        pulseMix = 0.5,
        subOctave = 0,
        subMix = 0.0,
        noiseSelect = 0,
        noiseMix = 0.0,
        wave = 0.5,
        waveLFO = 0.0,
        waveEnv = 0.0,
        highPass = 10,
        filterFreq = 10000,
        filterTrack = 0,
        filterLFO = 0,
        filterEnv = 0,
        xFilter = 0,
        filterRes = 0.0,
        gateMode = 0,
        amp = 0.3):
   p = SS1(name)
   p["chorus"] = int(chorus)
   p["lfoWave"] = int(lfoWave)
   p["subOctave"] = int(subOctave)
   p["noiseSelect"] = int(noiseSelect)
   p["highPass"] = int(highPass)
   p["filterFreq"] = int(filterFreq)
   p["filterTrack"] = int(filterTrack)
   p["filterLFO"] = int(filterLFO)
   p["filterEnv"] = int(filterEnv)
   p["xFilter"] = int(xFilter)
   p["gateMode"] = int(gateMode)
   p["port"] = float(port)
   p["vsens"] = float(vsens)
   p["vdepth"] = float(vdepth)
   p["xPitch"] = float(xPitch)
   p["lfoFreq"] = float(lfoFreq)
   p["lfoDelay"] = float(lfoDelay)
   p["lfoAmp"] = float(lfoAmp)
   p["attack"] = float(attack)
   p["decay"] = float(decay)
   p["sustain"] = float(sustain)
   p["release"] = float(release)
   p["sawMix"] = float(sawMix)
   p["pulseMix"] = float(pulseMix)
   p["subMix"] = float(subMix)
   p["noiseMix"] = float(noiseMix)
   p["wave"] = float(wave)
   p["waveLFO"] = float(waveLFO)
   p["waveEnv"] = float(waveEnv)
   p["filterRes"] = float(filterRes)
   p["amp"] = float(amp)
   program_bank[slot] = p
   return p

def pp(program,slot=127):
    pad = ' '*4
    acc = 'ss1(%d, "%s",\n' % (slot,program.name)
    for p in ("port","vsens","vdepth","xPitch","lfoFreq","lfoDelay",
              "lfoAmp","attack","decay","sustain","release","sawMix",
              "pulseMix","subMix","noiseMix","wave","waveLFO","waveEnv",
              "filterRes","amp"):
        acc += '%s%s = %5.4f,\n' % (pad,p,round(float(program[p]),4))
    iparams = ("chorus","lfoWave","subOctave","noiseSelect","highPass",
               "filterFreq","filterTrack","filterLFO","filterEnv","xFilter",
               "gateMode")
    terminal = iparams[-1]
    for p in iparams:
        acc += '%s%s = %d' % (pad,p,int(program[p]))
        if p == terminal:
            acc += ")\n"
        else:
            acc += ",\n"
    return acc


def random_ss1(slot, *_):
    ff = pick(LOWPASS_CUTOFF)
    ft = pick(LOWPASS_TRACK)
    open_filter = (ft >=2) or (ff > MID_CUTOFF)
    if open_filter:
        fenv_sign = -1
    else:
        fenv_sign = 1
    def envtime(seg):
        if seg == 'a':
            return coin(0.75, rnd(0.5), coin(0.75, rnd(), rnd(4)))
        else:
            return coin(0.75, rnd(2), rnd(4))
    amps = []
    for i in range(3):
        amps.append(rnd())
    amps[pick([0,1,2])] = 1.0
    p = ss1(slot,"Random",
            port = coin(0.90, 0.0, rnd()),
            vsens = coin(0.75, 0.1, rnd()),
            xPitch = 0.0,
            chorus = coin(0.50, 1, 0),
            lfoFreq = coin(0.75, 3+rnd(4), coin(0.5, rnd(3), rnd(16))),
            lfoWave = pick([0,0,0,0,0,0,1,2]),
            lfoDelay = rnd(2),
            lfoAmp = coin(0.25, 0.0, rnd()),
            attack = envtime("a"),
            decay = envtime("d"),
            sustain = coin(0.75, 0.5+rnd(0.5), coin(0.75, rnd(), coin(0.5, 0.0, 1.0))),
            release = envtime("r"),
            sawMix = amps[0],
            pulseMix = amps[1],
            subMix = amps[2],
            subOctave = coin(0.5, 0, 1),
            noiseSelect = coin(0.5, 0, 1),
            noiseMix = coin(0.75, 0, coin(0.75, rnd(0.5), rnd())),
            wave = coin(0.75, 0.5, rnd()),
            waveLFO = coin(0.75, 0.0, rnd()),
            waveEnv = coin(0.75, 0.0, rnd()),
            highPass = coin(0.75, HIGHPASS_CUTOFF[0], pick(HIGHPASS_CUTOFF)),
            filterFreq = ff,
            filterTrack = ft,
            filterLFO = int(coin(0.75, 0, rnd(MID_CUTOFF))),
            filterEnv = int(fenv_sign*coin(0.75, rnd(LOWPASS_CUTOFF[-2]), 0)),
            xFilter = 0,
            gateMode = coin(0.75, 0, 1),
            amp = 0.3)
    return p

ss1(0, "A",
    port = 0.0000,
    vsens = 0.1000,
    vdepth = 0.0000,
    xPitch = 0.0000,
    lfoFreq = 5.6060,
    lfoDelay = 0.1881,
    lfoAmp = 0.9726,
    attack = 0.2532,
    decay = 1.4079,
    sustain = 0.6600,
    release = 1.8985,
    sawMix = 0.7950,
    pulseMix = 1.0000,
    subMix = 0.0713,
    noiseMix = 0.0000,
    wave = 0.1799,
    waveLFO = 0.0000,
    waveEnv = 0.4445,
    filterRes = 0.0000,
    amp = 0.3000,
    chorus = 1,
    lfoWave = 0,
    subOctave = 1,
    noiseSelect = 1,
    highPass = 10,
    filterFreq = 800,
    filterTrack = 0,
    filterLFO = 0,
    filterEnv = 0,
    xFilter = 0,
    gateMode = 0)

ss1(1, "B",
    port = 0.0000,
    vsens = 0.1000,
    vdepth = 0.0000,
    xPitch = 0.0000,
    lfoFreq = 6.0470,
    lfoDelay = 0.4800,
    lfoAmp = 0.0352,
    attack = 3.3891,
    decay = 0.0908,
    sustain = 0.8241,
    release = 0.5460,
    sawMix = 0.9899,
    pulseMix = 1.0000,
    subMix = 0.8342,
    noiseMix = 0.0000,
    wave = 0.4975,
    waveLFO = 0.4724,
    waveEnv = 0.0000,
    filterRes = 0.0000,
    amp = 0.3000,
    chorus = 1,
    lfoWave = 0,
    subOctave = 1,
    noiseSelect = 0,
    highPass = 10,
    filterFreq = 16000,
    filterTrack = 0,
    filterLFO = 7873,
    filterEnv = -4395,
    xFilter = 0,
    gateMode = 0)

ss1(2, "C",
    port = 0.0000,
    vsens = 0.1000,
    vdepth = 0.0000,
    xPitch = 0.0000,
    lfoFreq = 4.3960,
    lfoDelay = 1.2900,
    lfoAmp = 0.3618,
    attack = 0.2488,
    decay = 1.0986,
    sustain = 0.9548,
    release = 1.5913,
    sawMix = 0.4171,
    pulseMix = 1.0000,
    subMix = 0.6834,
    noiseMix = 0.0000,
    wave = 0.5000,
    waveLFO = 0.0000,
    waveEnv = 0.9196,
    filterRes = 0.0000,
    amp = 0.3000,
    chorus = 0,
    lfoWave = 0,
    subOctave = 0,
    noiseSelect = 1,
    highPass = 500,
    filterFreq = 400,
    filterTrack = 1,
    filterLFO = 0,
    filterEnv = 4278,
    xFilter = 0,
    gateMode = 0)

ss1(3, "D",
    port = 0.0000,
    vsens = 0.5578,
    vdepth = 0.0000,
    xPitch = 0.0000,
    lfoFreq = 4.4560,
    lfoDelay = 1.2900,
    lfoAmp = 0.0000,
    attack = 0.1586,
    decay = 0.3702,
    sustain = 0.7136,
    release = 1.1412,
    sawMix = 1.0000,
    pulseMix = 0.8894,
    subMix = 0.9196,
    noiseMix = 0.0000,
    wave = 0.5000,
    waveLFO = 0.0000,
    waveEnv = 0.0000,
    filterRes = 0.0000,
    amp = 0.3000,
    chorus = 1,
    lfoWave = 0,
    subOctave = 0,
    noiseSelect = 0,
    highPass = 10,
    filterFreq = 10000,
    filterTrack = 1,
    filterLFO = 0,
    filterEnv = -7715,
    xFilter = 0,
    gateMode = 0)

ss1(4, "E",
    port = 0.0000,
    vsens = 0.0955,
    vdepth = 0.0000,
    xPitch = 0.0000,
    lfoFreq = 4.0160,
    lfoDelay = 0.9750,
    lfoAmp = 0.0000,
    attack = 0.1329,
    decay = 0.9283,
    sustain = 0.6683,
    release = 1.2537,
    sawMix = 0.0000,
    pulseMix = 1.0000,
    subMix = 0.5879,
    noiseMix = 0.1005,
    wave = 0.5000,
    waveLFO = 0.1457,
    waveEnv = 0.0000,
    filterRes = 0.0000,
    amp = 0.3000,
    chorus = 0,
    lfoWave = 0,
    subOctave = 0,
    noiseSelect = 0,
    highPass = 500,
    filterFreq = 800,
    filterTrack = 0,
    filterLFO = 0,
    filterEnv = 5748,
    xFilter = 0,
    gateMode = 1)

ss1(5, "F",
    port = 0.0000,
    vsens = 0.3015,
    vdepth = 0.0000,
    xPitch = 0.0000,
    lfoFreq = 3.0450,
    lfoDelay = 0.0600,
    lfoAmp = 0.5628,
    attack = 2.6934,
    decay = 1.2696,
    sustain = 0.7638,
    release = 2.5865,
    sawMix = 1.0000,
    pulseMix = 0.4975,
    subMix = 0.0000,
    noiseMix = 0.0854,
    wave = 0.7437,
    waveLFO = 0.2814,
    waveEnv = 0.7437,
    filterRes = 0.0000,
    amp = 0.3000,
    chorus = 0,
    lfoWave = 0,
    subOctave = 0,
    noiseSelect = 1,
    highPass = 10,
    filterFreq = 100,
    filterTrack = 2,
    filterLFO = 45,
    filterEnv = 2256,
    xFilter = 0,
    gateMode = 0)

ss1(6, "Triangle Wave",
    port = 0.0000,
    vsens = 0.0955,
    vdepth = 0.0000,
    xPitch = 0.0000,
    lfoFreq = 3.1850,
    lfoDelay = 0.8850,
    lfoAmp = 0.0000,
    attack = 0.0000,
    decay = 0.4789,
    sustain = 1.0000,
    release = 0.0000,
    sawMix = 1.0000,
    pulseMix = 0.0000,
    subMix = 0.0000,
    noiseMix = 0.0000,
    wave = 0.4975,
    waveLFO = 0.0000,
    waveEnv = 0.0000,
    filterRes = 0.0000,
    amp = 0.3000,
    chorus = 1,
    lfoWave = 0,
    subOctave = 0,
    noiseSelect = 1,
    highPass = 10,
    filterFreq = 16000,
    filterTrack = 1,
    filterLFO = 0,
    filterEnv = -2487,
    xFilter = 0,
    gateMode = 0)

ss1(7, "Sawtooth wave",
    port = 0.0000,
    vsens = 0.0955,
    vdepth = 0.0000,
    xPitch = 0.0000,
    lfoFreq = 3.1850,
    lfoDelay = 0.8850,
    lfoAmp = 0.0000,
    attack = 0.0000,
    decay = 0.4789,
    sustain = 1.0000,
    release = 0.0000,
    sawMix = 1.0000,
    pulseMix = 0.0000,
    subMix = 0.0000,
    noiseMix = 0.0000,
    wave = 1.0000,
    waveLFO = 0.0000,
    waveEnv = 0.0000,
    filterRes = 0.0000,
    amp = 0.3000,
    chorus = 1,
    lfoWave = 0,
    subOctave = 0,
    noiseSelect = 1,
    highPass = 10,
    filterFreq = 16000,
    filterTrack = 1,
    filterLFO = 0,
    filterEnv = -2487,
    xFilter = 0,
    gateMode = 0)

ss1(8, "Square wave",
    port = 0.0000,
    vsens = 0.0955,
    vdepth = 0.0000,
    xPitch = 0.0000,
    lfoFreq = 3.1850,
    lfoDelay = 0.8850,
    lfoAmp = 0.0000,
    attack = 0.0000,
    decay = 0.4789,
    sustain = 1.0000,
    release = 0.0000,
    sawMix = 0.0000,
    pulseMix = 1.0000,
    subMix = 0.0000,
    noiseMix = 0.0000,
    wave = 0.4975,
    waveLFO = 0.0000,
    waveEnv = 0.0000,
    filterRes = 0.0000,
    amp = 0.3000,
    chorus = 1,
    lfoWave = 0,
    subOctave = 0,
    noiseSelect = 1,
    highPass = 10,
    filterFreq = 16000,
    filterTrack = 1,
    filterLFO = 0,
    filterEnv = -2487,
    xFilter = 0,
    gateMode = 0)

ss1(9, "Light PWM",
    port = 0.0000,
    vsens = 0.0955,
    vdepth = 0.0000,
    xPitch = 0.0000,
    lfoFreq = 0.1850,
    lfoDelay = 0.0000,
    lfoAmp = 0.0000,
    attack = 0.0000,
    decay = 0.4789,
    sustain = 1.0000,
    release = 0.0000,
    sawMix = 0.0000,
    pulseMix = 1.0000,
    subMix = 0.2161,
    noiseMix = 0.0000,
    wave = 0.4322,
    waveLFO = 0.6131,
    waveEnv = 0.0000,
    filterRes = 0.0000,
    amp = 0.3000,
    chorus = 1,
    lfoWave = 0,
    subOctave = 0,
    noiseSelect = 1,
    highPass = 10,
    filterFreq = 16000,
    filterTrack = 1,
    filterLFO = 0,
    filterEnv = -2487,
    xFilter = 0,
    gateMode = 0)

ss1(10, "Noise Sweep",
    port = 0.0000,
    vsens = 0.0955,
    vdepth = 0.0000,
    xPitch = 0.0000,
    lfoFreq = 0.1850,
    lfoDelay = 0.0000,
    lfoAmp = 0.0000,
    attack = 6.0000,
    decay = 4.9142,
    sustain = 0.5779,
    release = 6.0000,
    sawMix = 0.0000,
    pulseMix = 0.0000,
    subMix = 0.0000,
    noiseMix = 1.0000,
    wave = 0.0000,
    waveLFO = 0.0000,
    waveEnv = 0.0000,
    filterRes = 0.2312,
    amp = 0.3000,
    chorus = 1,
    lfoWave = 0,
    subOctave = 0,
    noiseSelect = 1,
    highPass = 10,
    filterFreq = 200,
    filterTrack = 0,
    filterLFO = 0,
    filterEnv = 2652,
    xFilter = 0,
    gateMode = 0)

ss1(11, "Sample and Hold",
    port = 0.0000,
    vsens = 0.5879,
    vdepth = 1.0000,
    xPitch = 0.0000,
    lfoFreq = 10.0000,
    lfoDelay = 0.0000,
    lfoAmp = 0.0000,
    attack = 0.0000,
    decay = 0.4789,
    sustain = 1.0000,
    release = 0.0000,
    sawMix = 1.0000,
    pulseMix = 0.2714,
    subMix = 0.0000,
    noiseMix = 0.0000,
    wave = 0.4472,
    waveLFO = 0.0452,
    waveEnv = 0.0000,
    filterRes = 0.0000,
    amp = 0.3000,
    chorus = 1,
    lfoWave = 2,
    subOctave = 0,
    noiseSelect = 1,
    highPass = 10,
    filterFreq = 6400,
    filterTrack = 0,
    filterLFO = 0,
    filterEnv = -2487,
    xFilter = 0,
    gateMode = 0)

ss1(12, "Random Filter",
    port = 0.0000,
    vsens = 0.0000,
    vdepth = 0.0000,
    xPitch = 0.0000,
    lfoFreq = 10.0000,
    lfoDelay = 0.0000,
    lfoAmp = 0.0000,
    attack = 0.0434,
    decay = 0.4789,
    sustain = 1.0000,
    release = 0.0794,
    sawMix = 1.0000,
    pulseMix = 0.6030,
    subMix = 0.0000,
    noiseMix = 0.0000,
    wave = 0.4472,
    waveLFO = 0.0000,
    waveEnv = 0.0000,
    filterRes = 0.5779,
    amp = 0.3000,
    chorus = 1,
    lfoWave = 2,
    subOctave = 0,
    noiseSelect = 1,
    highPass = 10,
    filterFreq = 3200,
    filterTrack = 0,
    filterLFO = 259,
    filterEnv = -2487,
    xFilter = 0,
    gateMode = 0)

ss1(13, "Random Filter 2",
    port = 0.0000,
    vsens = 0.0000,
    vdepth = 0.0000,
    xPitch = 0.0000,
    lfoFreq = 10.0000,
    lfoDelay = 0.0000,
    lfoAmp = 0.0000,
    attack = 0.0000,
    decay = 0.4789,
    sustain = 1.0000,
    release = 0.0794,
    sawMix = 0.0000,
    pulseMix = 0.0000,
    subMix = 0.0000,
    noiseMix = 0.8291,
    wave = 0.4472,
    waveLFO = 0.0000,
    waveEnv = 0.0000,
    filterRes = 0.8291,
    amp = 0.3000,
    chorus = 1,
    lfoWave = 2,
    subOctave = 0,
    noiseSelect = 1,
    highPass = 10,
    filterFreq = 800,
    filterTrack = 0,
    filterLFO = 125,
    filterEnv = 0,
    xFilter = 0,
    gateMode = 0)

