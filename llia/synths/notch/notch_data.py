# llia.synths.notch.notch_data

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

class Notch(Program):

    def __init__(self,name):
        super(Notch,self).__init__(name,Notch,prototype)
        self.performance = performance()

program_bank = ProgramBank(Notch("Init"))

def notch(slot, name,
          lfoFreq = 1.0,
          cFreq = 1000,
          cFreqLfo = 0,
          cFreqX = 0,
          q = 1,
          qLfo = 0,
          qX = 0,
          filterGain = 0,
          bleed = 0.0):
    p = Notch(name)
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
    pad = ' '*6
    def fval(key):
        return round(float(program[key]),4)
    acc = 'notch(%d, "%s",\n' % (slot,program.name)
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



notch(0, "Bypass",
      lfoFreq = 1.0000,
      cFreq = 1000.0000,
      cFreqLfo = 0.0000,
      cFreqX = 0.0000,
      q = 1.0000,
      qLfo = 0.0000,
      qX = 0.0000,
      filterGain = 0.0000,
      bleed = 1.0000)

notch(1, "116Hz Cut",
      lfoFreq = 1.0000,
      cFreq = 116.6400,
      cFreqLfo = 0.0000,
      cFreqX = 0.0000,
      q = 14.8877,
      qLfo = 0.0000,
      qX = 0.0000,
      filterGain = 0.6000,
      bleed = 0.0000)

notch(2, "415Hz Cut",
      lfoFreq = 1.0000,
      cFreq = 415.9375,
      cFreqLfo = 0.0000,
      cFreqX = 0.0000,
      q = 6.4000,
      qLfo = 0.0000,
      qX = 0.0000,
      filterGain = 0.3600,
      bleed = 0.0000)

notch(3, "Light Sweep",
      lfoFreq = 1.0000,
      cFreq = 1186.3800,
      cFreqLfo = 762.1563,
      cFreqX = 0.0000,
      q = 37.3248,
      qLfo = 0.0000,
      qX = 0.0000,
      filterGain = 0.0000,
      bleed = 0.0000)

notch(4, "4Hz Sweep",
      lfoFreq = 4.2000,
      cFreq = 933.1200,
      cFreqLfo = 601.5260,
      cFreqX = 0.0000,
      q = 0.0000,
      qLfo = 0.0000,
      qX = 0.0000,
      filterGain = 0.0000,
      bleed = 0.0000)

notch(5, "Very Slow Sweep",
      lfoFreq = 0.1000,
      cFreq = 933.1200,
      cFreqLfo = 601.5260,
      cFreqX = 0.0000,
      q = 21.0645,
      qLfo = 0.0000,
      qX = 0.0000,
      filterGain = 0.0000,
      bleed = 0.0000)

