# llia.synths.notch.notch_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance

prototype = {
    "lfoFreq" : 1.0,
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
program_bank.enable_undo = False

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

notch(0,"Bypass", bleed = 1.0)

