# llia.synths.io.io_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance
from llia.util.lmath import coin,rnd,pick

prototype = {
    "amp" : 0.07,             # 0..2
    "port" : 0.0,             # 0..1
    "vfreq" : 7.0,            # 0..99
    "vdelay" : 0.0,           # 0..2
    "vsens" : 0.1,            # 0..1
    "vdepth" : 0.1,           # 0..1
    "vlock" : 0,              # 0|1   0->Off, 1->lock vib freq to sub-harmonic
    "trem" : 0.1,             # 0..1 tremolo & FM Mod depth
    "chiffAttack" : 0.03,     # 0..0.5
    "chiffDecay" : 0.2,       # 0..0.5
    "chiffAmp" : 0.05,        # 0..1
    "chiffVelocity" : 0.0,    # 0..1
    "noiseAmp" : 1.0,         # 0..1
    "envScale" : 1.1,         # 0..10 
    "attack" : 0.05,          # 0..2
    "decay"  : 0.1,           # 0..2 (modulator only)
    "release" : 0.1,          # 0..2
    "modDepth" : 1.0,         # 0..3
    "feedback" : 0.0,         # 0..4
    "modHP" : 30,             # [3,6,9,...,30]
    "velocityDepth" : 0.5,    # 0..1
    "ff1" : 600,              # 100..10K
    "ff2" : 1100,             # 100..10K
    "ff3" : 2300,             # 100..10K
    "amp1" : 1.0,             # 0..1
    "amp2" : 1.0,             # 0..1
    "amp3" : 1.0,             # 0..1
    "lag1" : 0.0,             # 0..1
    "lag2" : 0.0,             # 0..1
    "lag3" : 0.0              # 0..1
}

class Io(Program):

    def __init__(self,name):
        super(Io,self).__init__(name,Io,prototype)
        self.performance = performance()

program_bank = ProgramBank(Io("Init"))
program_bank.enable_undo = False

def io(slot, name,
       amp = 0.07,    
       port = 0.0,
       vfreq = 7.0,
       vdelay = 0.0,
       vsens = 0.1,
       vdepth = 0.1,
       vlock = 0,
       trem = 0.1,
       chiffAttack = 0.03,
       chiffDecay = 0.2,
       chiffAmp = 0.05,
       chiffVelocity = 0.0,
       noiseAmp = 1.0,
       envScale = 1.1,
       attack = 0.05,
       decay = 0.3,
       release = 0.1,
       modDepth = 1.0,
       feedback = 0.0,
       modHP = 30,
       velocityDepth = 0.5,
       ff1 = 600,
       ff2 = 1100,
       ff3 = 2300,
       amp1 = 1.0,
       amp2 = 1.0,
       amp3 = 1.0,
       lag1 = 0.0,
       lag2 = 0.0,
       lag3 = 0.0):
    p = Io(name)
    p["amp"] = float(amp)
    p["port"] = float(port)
    p["vfreq"] = float(vfreq)
    p["vdelay"] = float(vdelay)
    p["vsens"] = float(vsens)
    p["vdepth"] = float(vdepth)
    p["vlock"] = int(vlock)
    p["trem"] = float(trem)
    p["chiffAttack"] = float(chiffAttack)
    p["chiffDecay"] = float(chiffDecay)
    p["chiffAmp"] = float(chiffAmp)
    p["chiffVelocity"] = float(chiffVelocity)
    p["noiseAmp"] = float(noiseAmp)
    p["envScale"] = abs(float(envScale))
    p["attack"] = float(attack)
    p["decay"] = float(decay)
    p["release"] = float(release)
    p["modDepth"] = float(modDepth)
    p["feedback"] = float(feedback)
    p["modHP"] = float(modHP)
    p["velocityDepth"] = float(velocityDepth)
    p["ff1"] = float(ff1)
    p["ff2"] = float(ff2)
    p["ff3"] = float(ff3)
    p["amp1"] = float(amp1)
    p["amp2"] = float(amp2)
    p["amp3"] = float(amp3)
    p["lag1"] = float(lag1)
    p["lag2"] = float(lag2)
    p["lag3"] = float(lag3)
    program_bank[slot] = p
    return p

def pp(program,slot=127):
    pad =" "*3
    acc = 'io(%d,"%s",\n' % (slot,program.name)
    for p in ("amp","port","vfreq","vdelay","vsens","vdepth","trem",
              "chiffAttack","chiffDecay","chiffAmp","chiffVelocity",
              "noiseAmp","envScale","attack","decay","release",
              "modDepth","velocityDepth","feedback","modHP",
              "ff1","ff2","ff3","amp1",
              "amp2","amp3","lag1","lag2","lag3"):
        v = round(float(program[p]),4);
        acc += "%s%s = %5.4f,\n" % (pad,p,v)
    p = "vlock"
    v = int(program[p])
    acc += "%s%s = %d)\n" % (pad,p,v)
    return acc

def io_random(slot=127,*_):
    if coin(0.75):
        ff1 = 100+rnd(400)
        ff2 = ff1+100+rnd(600)
        ff3 = ff2+100+rnd(600)
    else:
        ff1 = 100+rnd(1000)
        ff2 = ff1+rnd(1000)
        ff3 = ff2+rnd(2000)
    amps = []
    for i in range(3):
        amps.append(coin(0.75,rnd(0.5),rnd()))
    amps[pick([0,1,2])] = 1.0
    p = Io("Random")
    p["amp"] = 0.1
    p["port"] = coin(0.80, 0, rnd(0.3))
    p["vfreq"] = 3+rnd(5)
    p["vdelay"] = rnd(2)
    p["vsens"] = coin(0.8, rnd(0.3), rnd())
    p["vdepth"] = coin(0.50, 0, coin(0.75, rnd(0.3), rnd()))
    p["vlock"] = coin(0.75, 1, 0)
    p["trem"] = coin(0.5, 0.0, coin(0.75, rnd(0.4), rnd()))
    p["chiffAttack"] = coin(0.75, rnd(0.07), rnd(0.5))
    p["chiffDecay"] = coin(0.75, 0.1+rnd(0.2), rnd(0.5))
    p["chiffAmp"] = rnd()
    p["noiseAmp"] = coin(0.75, rnd(0.1), rnd())
    p["envScale"] = coin(0.75, rnd(4), rnd(10))
    p["attack"] = coin(0.75, rnd(0.1), rnd())
    p["decay"] = coin(0.75, 0.1+rnd(0.4), rnd())
    p["release"] = coin(0.75, rnd(0.3),rnd())
    p["modDepth"] = coin(0.75, rnd(2),rnd(4))
    p["feedback"] = coin(0.50, 0.0, coin(0.75, rnd(2),rnd(4)))
    p["ff1"] = int(ff1)
    p["ff2"] = int(ff2)
    p["ff3"] = int(ff3)
    p["amp1"] = amps[0]
    p["amp2"] = amps[1]
    p["amp3"] = amps[2]
    p["lag1"] = coin(0.75, 0, rnd())
    p["lag2"] = coin(0.75, 0, rnd())
    p["lag3"] = coin(0.75, 0, rnd())
    return p
    

io(0,"A",
   amp = 0.1778,
   port = 0.0000,
   vfreq = 5.6580,
   vdelay = 0.5000,
   vsens = 0.0955,
   vdepth = 0.0000,
   trem = 0.0151,
   chiffAttack = 0.0300,
   chiffDecay = 0.1775,
   chiffAmp = 0.4191,
   chiffVelocity = 0.9397,
   noiseAmp = 0.0181,
   envScale = 1.3500,
   attack = 0.0700,
   decay = 0.4400,
   release = 0.0300,
   modDepth = 0.2200,
   velocityDepth = 0.4975,
   feedback = 0.0000,
   modHP = 30.0000,
   ff1 = 449.0000,
   ff2 = 1039.0000,
   ff3 = 1360.0000,
   amp1 = 0.0198,
   amp2 = 0.3390,
   amp3 = 0.9689,
   lag1 = 0.8141,
   lag2 = 0.0000,
   lag3 = 0.2161,
   vlock = 0)

io(1,"B",
   amp = 0.1778,
   port = 0.0000,
   vfreq = 3.9360,
   vdelay = 1.7400,
   vsens = 0.0352,
   vdepth = 0.0000,
   trem = 0.3417,
   chiffAttack = 0.0675,
   chiffDecay = 0.1475,
   chiffAmp = 0.3093,
   chiffVelocity = 0.0000,
   noiseAmp = 0.1030,
   envScale = 5.5000,
   attack = 0.0100,
   decay = 0.3900,
   release = 0.2600,
   modDepth = 2.0000,
   velocityDepth = 0.5000,
   feedback = 1.9600,
   modHP = 8.5400,
   ff1 = 522.0000,
   ff2 = 866.0000,
   ff3 = 1155.0000,
   amp1 = 0.9689,
   amp2 = 0.3696,
   amp3 = 0.2350,
   lag1 = 0.0000,
   lag2 = 0.0000,
   lag3 = 0.0000,
   vlock = 1)

io(2,"C",
   amp = 0.2239,
   port = 0.0000,
   vfreq = 4.0850,
   vdelay = 1.8300,
   vsens = 0.1809,
   vdepth = 0.1156,
   trem = 0.0704,
   chiffAttack = 0.0300,
   chiffDecay = 0.2325,
   chiffAmp = 0.9390,
   chiffVelocity = 1.0000,
   noiseAmp = 0.0940,
   envScale = 8.0000,
   attack = 0.1000,
   decay = 1.6900,
   release = 0.3500,
   modDepth = 1.8800,
   velocityDepth = 1.0000,
   feedback = 1.9400,
   modHP = 4.3350,
   ff1 = 1000.0000,
   ff2 = 1696.0000,
   ff3 = 3156.0000,
   amp1 = 0.9489,
   amp2 = 0.7776,
   amp3 = 0.0285,
   lag1 = 0.5930,
   lag2 = 0.0000,
   lag3 = 0.8141,
   vlock = 1)

io(3,"D",
   amp = 0.1778,
   port = 0.0000,
   vfreq = 5.6030,
   vdelay = 0.6600,
   vsens = 0.1608,
   vdepth = 0.2362,
   trem = 0.0754,
   chiffAttack = 0.0500,
   chiffDecay = 0.1175,
   chiffAmp = 0.5561,
   chiffVelocity = 0.0000,
   noiseAmp = 0.0622,
   envScale = 3.4000,
   attack = 0.0700,
   decay = 0.4000,
   release = 0.3000,
   modDepth = 0.0000,
   velocityDepth = 0.4975,
   feedback = 0.0000,
   modHP = 30.0000,
   ff1 = 230.0000,
   ff2 = 829.0000,
   ff3 = 1144.0000,
   amp1 = 0.9588,
   amp2 = 0.1556,
   amp3 = 0.0651,
   lag1 = 0.0000,
   lag2 = 0.0000,
   lag3 = 0.0000,
   vlock = 1)

io(4,"E",
   amp = 0.1413,
   port = 0.0000,
   vfreq = 7.1200,
   vdelay = 0.3600,
   vsens = 0.9849,
   vdepth = 0.2864,
   trem = 0.0000,
   chiffAttack = 0.0550,
   chiffDecay = 0.2375,
   chiffAmp = 0.8024,
   chiffVelocity = 0.0000,
   noiseAmp = 0.0299,
   envScale = 2.0500,
   attack = 0.0600,
   decay = 0.5500,
   release = 0.2649,
   modDepth = 3.6600,
   velocityDepth = 0.5000,
   feedback = 0.0000,
   modHP = 30.0000,
   ff1 = 359.0000,
   ff2 = 795.0000,
   ff3 = 1177.0000,
   amp1 = 0.9792,
   amp2 = 0.2350,
   amp3 = 0.1785,
   lag1 = 0.0000,
   lag2 = 0.0000,
   lag3 = 0.3819,
   vlock = 1)

io(5,"F",
   amp = 0.1413,
   port = 0.0000,
   vfreq = 3.2550,
   vdelay = 0.2500,
   vsens = 0.1608,
   vdepth = 0.0000,
   trem = 0.0000,
   chiffAttack = 0.4525,
   chiffDecay = 0.2700,
   chiffAmp = 0.4654,
   chiffVelocity = 0.8392,
   noiseAmp = 0.0622,
   envScale = 2.0000,
   attack = 0.0400,
   decay = 0.9900,
   release = 0.2900,
   modDepth = 1.6600,
   velocityDepth = 0.8643,
   feedback = 0.9800,
   modHP = 1.0000,
   ff1 = 583.0000,
   ff2 = 1384.0000,
   ff3 = 2856.0000,
   amp1 = 0.5860,
   amp2 = 0.0217,
   amp3 = 0.4019,
   lag1 = 0.0000,
   lag2 = 0.9698,
   lag3 = 0.0804,
   vlock = 1)

io(6,"G",
   amp = 0.1413,
   port = 0.0000,
   vfreq = 4.8310,
   vdelay = 2.0000,
   vsens = 0.0754,
   vdepth = 0.1608,
   trem = 0.1357,
   chiffAttack = 0.1150,
   chiffDecay = 0.1400,
   chiffAmp = 0.7076,
   chiffVelocity = 0.8945,
   noiseAmp = 0.0227,
   envScale = 7.6500,
   attack = 0.3800,
   decay = 1.3800,
   release = 0.2300,
   modDepth = 1.4400,
   velocityDepth = 0.7136,
   feedback = 0.0000,
   modHP = 1.0000,
   ff1 = 1987.0000,
   ff2 = 2420.0000,
   ff3 = 3569.0000,
   amp1 = 0.9999,
   amp2 = 0.8818,
   amp3 = 0.9792,
   lag1 = 0.0000,
   lag2 = 0.0000,
   lag3 = 0.0000,
   vlock = 1)

io(7,"H",
   amp = 0.1413,
   port = 0.0000,
   vfreq = 5.2760,
   vdelay = 0.5400,
   vsens = 0.6080,
   vdepth = 0.0000,
   trem = 0.0000,
   chiffAttack = 0.4750,
   chiffDecay = 0.1200,
   chiffAmp = 0.1629,
   chiffVelocity = 0.8191,
   noiseAmp = 0.0285,
   envScale = 5.1500,
   attack = 0.2300,
   decay = 0.9800,
   release = 0.2900,
   modDepth = 1.7800,
   velocityDepth = 0.5980,
   feedback = 0.6400,
   modHP = 30.0000,
   ff1 = 593.0000,
   ff2 = 720.0000,
   ff3 = 1086.0000,
   amp1 = 0.2955,
   amp2 = 0.9999,
   amp3 = 0.5984,
   lag1 = 0.2060,
   lag2 = 0.0000,
   lag3 = 0.0000,
   vlock = 1)

