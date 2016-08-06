# llia.synths.snh.snh_data

from __future__ import print_function
from fractions import Fraction

from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance
from llia.util.lmath import coin, rnd, pick

prototype = {
    "shRate" : 1.0,        # sample rate
    "srcFreq" : 3.0,       # internal LFO freq
    "srcSelect" : 0,       # sample source, 0 -> saw  1 -> noise
    "shLag" : 0.0,         # lag time
    "shBleed" : 0.0,       # envelope bypass, 0 -> use env. 1-> ignore env
    "shDelay" : 0.0,       # env onset delay
    "shAttack" : 0.0,      # env onset attack time
    "shHold" : 1.0,        # env hold time after gate low
    "shRelease" : 1.0,     # env release after hold segment
    "shScale" : 1.0,       # output scale factor
    "shBias" : 0.0}
    

class Snh(Program):

    def __init__(self, name):
        super(Snh, self).__init__(name, "SNH", prototype)
        self.performance = performance()

init_program = Snh("Init")        
program_bank = ProgramBank(init_program)
program_bank.enable_undo = False

def snh(slot, name,
        srate = 5.0, srcFreq = 3.0, srcSelect = 0.0, lag = 0.0,
        env = [0.0, 0.0, 0.0, 0.0], # [delay attack hold release
        bleed = 0.0, scale = 1.0, bias = 0.0):
    p = Snh(name)
    p["shRate"] = float(srate)
    p["srcFreq"] = float(srcFreq)
    p["srcSelect"] = float(srcSelect)
    p["shLag"] = float(lag)
    p["shBleed"] = float(bleed)
    p["shDelay"] = float(env[0])
    p["shAttack"] = float(env[1])
    p["shHold"] = float(env[2])
    p["shRelease"] = float(env[3])
    p["shScale"] = float(scale)
    p["shBias"] = float(bias)
    program_bank[slot] = p
    return p

def int3(f):
    return int(round(f,3)*1000)

def pp(program, slot=127):
    def fval(key):
        v = program[key]
        return float(program[key])
    pad = ' '*5
    try:
        a,b = int3(fval("shRate")), int3(fval("srcFreq"))
        f = Fraction(a,b)
        acc = "# sh Ratio is %d:%d\n" % (f.numerator,f.denominator)
    except ZeroDivisionError:
        acc = 0
    acc += 'snh(%d,"%s",\n' % (slot, program.name)
    frmt = '%ssrate=%5.3f, srcFreq=%5.3f, srcSelect=%5.3f, lag=%5.3f,\n'
    data = (pad, fval('shRate'), fval('srcFreq'),
            fval('srcSelect'), fval('shLag'))
    acc += frmt % data
    frmt = '%senv = [%5.3f, %5.3f, %5.3f, %5.3f],\n'
    data = (pad,fval('shDelay'),fval('shAttack'),fval('shHold'),fval('shRelease'))
    acc += frmt % data
    frmt = '%sbleed=%5.3f, scale=%5.3f, bias=%5.3f)\n'
    data = (pad,fval('shBleed'),fval('shScale'),fval('shBias'))
    acc += frmt % data

   
    return acc

def random_snh(slot=127, *_):
    n = pick([1.25, 1.2, 1.333, 1.5, 1.667, 1.75, 2, 2.5, 3,
              3.333, 4, 4.5, 5, 6, 6.667, 7, 8, 9, 10, 11,
              12, 13,14,15,16])
    ratio = coin(0.90, 1.0/n, 0.01*rnd(0.09))
    srate = coin(0.75, 3+rnd(4), coin(0.75, rnd(10), rnd(100)))
    p = snh(slot, "Random")
    p["shRate"] = srate
    p["srcFreq"] = srate*ratio
    p["srcSelect"] = coin(0.75, 0, coin(0.5, 1, rnd()))
    p["shLag"] = coin(0.75, 0, rnd())
    p["shBleed"] = coin(0.75, 1.0, 0.0)
    delay = rnd(4)
    attack = coin(0.75, delay, rnd(4))
    hold = 1
    release = coin(0.75, hold, rnd(4))
    p["shDelay"] = delay
    p["shAttack"] = attack
    p["shHold"] = hold
    p["shRelease"] = release
    p["shScale"] = 1
    p["shBias"] = 0
    try:
        a,b = int3(p["shRate"]), int3(p["srcFreq"])
        f = Fraction(a,b)
        rem = "# sh Ratio is %d:%d\n" % (f.numerator,f.denominator)
        p.remarks = rem
    except ZeroDivisionError:
        pass
    return p


# sh Ratio is 6781:1507
snh(0,"Alpha",
     srate=6.781, srcFreq=1.507, srcSelect=0.000, lag=0.000,
     env = [2.785, 1.531, 1.000, 1.000],
     bleed=0.000, scale=1.000, bias=0.000)

# sh Ratio is 5275:879
snh(1,"Beta",
     srate=5.275, srcFreq=0.879, srcSelect=0.000, lag=0.000,
     env = [3.173, 3.173, 1.000, 1.000],
     bleed=1.000, scale=1.000, bias=0.000)

snh(2,"Slew Saw",
     srate=4.716, srcFreq=0.295, srcSelect=0.000, lag=0.585,
     env = [0.653, 0.653, 1.000, 0.596],
     bleed=1.000, scale=1.000, bias=0.000)

# sh Ratio is 4605:2762
snh(3,"Gamma",
     srate=4.605, srcFreq=2.762, srcSelect=0.000, lag=0.000,
     env = [0.310, 0.310, 1.000, 3.652],
     bleed=0.000, scale=1.000, bias=0.000)

# sh Ratio is 3299:275
snh(4,"Ascending stair w delay",
     srate=6.598, srcFreq=0.550, srcSelect=0.000, lag=0.000,
     env = [1.454, 1.367, 1.000, 1.000],
     bleed=0.000, scale=1.000, bias=0.000)

snh(5,"Classic Sample & Hold",
     srate=5.955, srcFreq=1.191, srcSelect=1.000, lag=0.000,
     env = [1.822, 1.822, 1.000, 1.000],
     bleed=1.000, scale=1.000, bias=0.000)

# sh Ratio is 6195:3098
snh(6,"Wandering somewhere",
     srate=6.195, srcFreq=3.098, srcSelect=1.000, lag=0.000,
     env = [3.585, 3.585, 1.000, 1.000],
     bleed=1.000, scale=1.000, bias=0.000)

# sh Ratio is 4133:919
snh(7,"Getting things done",
     srate=4.133, srcFreq=0.919, srcSelect=0.000, lag=0.000,
     env = [2.316, 2.316, 1.000, 1.000],
     bleed=1.000, scale=1.000, bias=0.000)
