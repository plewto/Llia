# llia.synths.bandpass.bandpass_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance

prototype = {"lfoFreq" : 1.0,
             "cFreq" : 1000,
             "cFreqLfo" : 0,    # LFO -> freq
             "cFreqX" : 0,      # External -> freq
             "q" : 1,           # Filter Q
             "qLfo" : 0,        # LFO -> Q
             "qX" : 0,          # External -> Q
             "filterGain" : 0,  # Filter gain in db
             "bleed" : 0.0}     # dry signal bypass  0 -> filter 1 -> no filter

class Bandpass(Program):

    def __init__(self,name):
        super(Bandpass,self).__init__(name,Bandpass,prototype)
        self.performance = performance()

program_bank = ProgramBank(Bandpass("Init"))

def bandpass(slot, name,
          lfoFreq = 1.0,
          cFreq = 1000,
          cFreqLfo = 0,
          cFreqX = 0,
          q = 1,
          qLfo = 0,
          qX = 0,
          filterGain = 0,
          bleed = 0.0):
    p = Bandpass(name)
    p["lfoFreq"] = float(lfoFreq)
    p["cFreq"] = float(cFreq)
    p["cFreqLfo"] = float(cFreqLfo)
    p["cFreqX"] = float(cFreqX)
    p["q"] = float(q)
    p["qLfo"] = float(qLfo)
    p["qX"] = float(qX)
    p["filterGain"] = float(filterGain)
    p["bleed"] = float(bleed)
    program_bank[slot] = p
    return p

def pp(program,slot=127):
    pad = ' '*9
    def fval(key):
        return round(float(program[key]),4)
    acc = 'bandpass(%d, "%s",\n' % (slot,program.name)
    params = ("lfoFreq","cFreq","cFreqLfo","cFreqX",
              "q","qLfo","qX","filterGain","bleed")
    terminal = params[-1]
    for p in params:
        acc += '%s%s = %5.4f' % (pad,p,fval(p))
        if p == terminal:
            acc += ')\n'
        else:
            acc += ',\n'
    return acc

bandpass(0, "Bypass",
         lfoFreq = 1.0000,
         cFreq = 1000.0000,
         cFreqLfo = 0.0000,
         cFreqX = 0.0000,
         q = 1.0000,
         qLfo = 0.0000,
         qX = 0.0000,
         filterGain = 0.0000,
         bleed = 1.0000)

bandpass(1, "1K Emph",
         lfoFreq = 1.2000,
         cFreq = 1000.0000,
         cFreqLfo = 0.0000,
         cFreqX = 0.0000,
         q = 2.0797,
         qLfo = 0.0000,
         qX = 0.0000,
         filterGain = 3.3600,
         bleed = 0.3166)

bandpass(2, "1Hz mod",
         lfoFreq = 1.0000,
         cFreq = 1328.6025,
         cFreqLfo = 1228.2500,
         cFreqX = 0.0000,
         q = 4.1064,
         qLfo = 0.0000,
         qX = 0.0000,
         filterGain = 5.5200,
         bleed = 0.5025)

bandpass(3, "Very Slow Mod",
         lfoFreq = 0.0500,
         cFreq = 1186.3800,
         cFreqLfo = 930.9688,
         cFreqX = 0.0000,
         q = 14.4703,
         qLfo = 0.0000,
         qX = 0.0000,
         filterGain = 9.3600,
         bleed = 0.3568)

bandpass(4, "5Hz Tremolo",
         lfoFreq = 5.0000,
         cFreq = 0.0000,
         cFreqLfo = 118.6380,
         cFreqX = 0.0000,
         q = 0.0000,
         qLfo = 0.0000,
         qX = 0.0000,
         filterGain = 7.8000,
         bleed = 0.3568)

bandpass(5, "Flutter Noise",
         lfoFreq = 31.0000,
         cFreq = 2977.5400,
         cFreqLfo = 949.1040,
         cFreqX = 0.0000,
         q = 7.9507,
         qLfo = 0.0000,
         qX = 0.0000,
         filterGain = 2.0400,
         bleed = 0.4724)

