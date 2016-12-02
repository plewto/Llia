# llia.synths.formant.formant_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance

prototype = {
    "hp" : 10,
    "lp" : 20000,
    "f1" : 220,
    "q1" : 1,
    "enable1" : 1,
    "gain1" : 0,
    "f2" : 660,
    "q2" : 1,
    "enable2" : 1,
    "gain2" : 0,
    "f3" : 990,
    "q3" : 1,
    "gain3" : 0,
    "enable3" : 1,
    "f4" : 1200,
    "q4" : 1,
    "gain4" : 0,
    "enable4" : 1,
    "bleed" : 0,
    "amp" :0}

class Formant(Program):

    def __init__(self,name):
        super(Formant,self).__init__(name,Formant,prototype)
        self.performance = performance()

program_bank = ProgramBank(Formant("Init"))
program_bank.enable_undo = False

def band(n,freq=None,q=1,gain=0,enable=1):
    freq = freq or (n*440)
    if enable:
        flag = 1
    else:
        flag = 0
    rs = {"f%d" % n : int(freq),
          "q%d" % n : float(q),
          "gain%d" % n : int(gain),
          "enable%d" % n : flag}
    return rs

def formant(slot, name,
            amp= +0,
            lp = 20000,
            hp = 10,
            b1 = band(1,  440, q=1.0, gain=+0,enable=1),
            b2 = band(2,  880, q=1.0, gain=+0,enable=1),
            b3 = band(3, 1320, q=1.0, gain=+0,enable=1),
            b4 = band(4, 1760, q=1.0, gain=+0,enable=1),
            bleed = 0):
   p = Formant(name)
   p["amp"] = amp
   p["hp"] = int(hp)
   p["lp"] = int(lp)
   p["bleed"] = float(bleed)
   for m in (b1,b2,b3,b4):
       p.update(m)
   program_bank[slot] = p
   return p

def pp(program,slot=127):
    def fval(key):
        return round(float(program[key]),4)
    def ival(key):
        return int(program[key])
    pad = ' '*8
    acc = 'formant(%d,"%s",\n' % (slot,program.name)
    acc += '%samp = %+d,\n' % (pad,ival('amp'))
    acc += '%slp = %5d,\n' % (pad,ival('lp'))
    acc += '%shp = %5d,\n' % (pad,ival('hp'))
    for i in (1,2,3,4):
        frmt = '%sb%d = band(%d, %5d, q=%5.4f, gain=%+3d, enable=%d),\n'
        freq = ival("f%d" % i)
        q = fval("q%d" % i)
        gain = ival("gain%d" % i)
        enable = ival("enable%d" % i)
        values = (pad,i,i,freq,q,gain,enable)
        acc += frmt % values
    acc += '%sbleed = %5.4f)\n' % (pad,fval('bleed'))
    return acc


formant(0,"Bypass",
        amp = +0,
        lp = 20000,
        hp =    10,
        b1 = band(1,   440, q=0.9700, gain= +0, enable=0),
        b2 = band(2,   660, q=1.0000, gain= +0, enable=0),
        b3 = band(3,   880, q=1.0000, gain= +0, enable=0),
        b4 = band(4,  1760, q=1.0000, gain= +0, enable=0),
        bleed = 1.0000)

formant(1,"Flute",
        amp = +0,
        lp = 20000,
        hp =    10,
        b1 = band(1,   220, q=1.0000, gain= +0, enable=0),
        b2 = band(2,   800, q=0.7550, gain=+13, enable=1),
        b3 = band(3,   990, q=1.0000, gain= +0, enable=0),
        b4 = band(4,  1200, q=1.0000, gain= +0, enable=0),
        bleed = 0.0000)

formant(2,"Oboe",
        amp = +0,
        lp = 20000,
        hp =    10,
        b1 = band(1,   220, q=1.0000, gain= +0, enable=0),
        b2 = band(2,  1400, q=0.7550, gain=+13, enable=1),
        b3 = band(3,  3000, q=0.7250, gain= +7, enable=1),
        b4 = band(4,  1200, q=1.0000, gain= +0, enable=0),
        bleed = 0.0000)

formant(3,"English Horn",
        amp = +0,
        lp = 20000,
        hp =    10,
        b1 = band(1,   220, q=1.0000, gain= +0, enable=0),
        b2 = band(2,   930, q=0.7550, gain=+13, enable=1),
        b3 = band(3,  2300, q=0.7550, gain= +9, enable=1),
        b4 = band(4,  1200, q=1.0000, gain= +0, enable=0),
        bleed = 0.0000)

formant(4,"Clarinet",
        amp = +0,
        lp = 20000,
        hp =    10,
        b1 = band(1,   220, q=1.0000, gain= +0, enable=0),
        b2 = band(2,  1660, q=0.7100, gain=+15, enable=1),
        b3 = band(3,  4000, q=0.7150, gain=+10, enable=1),
        b4 = band(4,  1200, q=1.0000, gain= +0, enable=0),
        bleed = 0.0000)

formant(5,"Bassoon",
        amp = +0,
        lp = 20000,
        hp =    10,
        b1 = band(1,   220, q=1.0000, gain= +0, enable=0),
        b2 = band(2,   480, q=0.7250, gain=+16, enable=1),
        b3 = band(3,  1240, q=0.7900, gain= +8, enable=1),
        b4 = band(4,  1200, q=1.0000, gain= +0, enable=0),
        bleed = 0.0000)

formant(6,"Trumnpet",
        amp = +0,
        lp = 20000,
        hp =    10,
        b1 = band(1,   220, q=1.0000, gain= +0, enable=0),
        b2 = band(2,  1300, q=0.6300, gain=+16, enable=1),
        b3 = band(3,  2500, q=0.6450, gain= +8, enable=1),
        b4 = band(4,  1200, q=1.0000, gain= +0, enable=0),
        bleed = 0.0000)

formant(7,"Tuba",
        amp = +0,
        lp = 20000,
        hp =    10,
        b1 = band(1,   300, q=0.7700, gain=+14, enable=1),
        b2 = band(2,  1300, q=0.6300, gain=+16, enable=0),
        b3 = band(3,  2500, q=0.6450, gain= +8, enable=0),
        b4 = band(4,  1200, q=1.0000, gain= +0, enable=0),
        bleed = 0.0000)

formant(8,"French Horn",
        amp = +0,
        lp = 20000,
        hp =    10,
        b1 = band(1,   300, q=0.7700, gain=+14, enable=0),
        b2 = band(2,   450, q=0.6300, gain=+16, enable=1),
        b3 = band(3,  2500, q=0.6450, gain= +8, enable=0),
        b4 = band(4,  1200, q=1.0000, gain= +0, enable=0),
        bleed = 0.0000)

