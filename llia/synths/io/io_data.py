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
    ff1 = 100+int(rnd(400))
    ff2 = ff1+100+rnd(600)
    ff3 = ff2+100+rnd(600)
    amps = []
    for i in range(3):
        amps.append(coin(0.75,rnd(0.5),rnd()))
    amps[pick([0,1,2])] = 1.0
    
    p = Io("Random")
    p["amp"] = 0.07
    p["port"] = coin(0.80, 0, rnd(0.3))
    p["vfreq"] = 3+rnd(5)
    p["vdelay"] = rnd(2)
    p["vsens"] = coin(0.8, rnd(0.3), rnd())
    p["vdepth"] = coin(0.50, 0, coin(0.75, rnd(0.3), rnd()))
    p["vlock"] = coin(0.75, 1, 0)
    p["trem"] = coin(0.75, rnd(0.4), rnd())
    p["chiffAttack"] = coin(0.75, rnd(0.07), rnd(0.5))
    p["chiffDecay"] = coin(0.75, 0.1+rnd(0.2), rnd(0.5))
    p["chiffAmp"] = rnd()
    p["noiseAmp"] = coin(0.75, rnd(0.1), rnd())
    p["envScale"] = coin(0.75, rnd(4), rnd(10))
    p["attack"] = coin(0.75, rnd(0.1), rnd())
    p["decay"] = coin(0.75, 0.1+rnd(0.4), rnd())
    p["release"] = coin(0.75, rnd(0.3),rnd())
    p["modDepth"] = rnd(3)
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
    

io(0,"A")

io(1,"B",
   amp = 0.0700,
   port = 0.0693,
   vfreq = 3.5045,
   vdelay = 0.5228,
   vsens = 0.1995,
   vdepth = 0.0048,
   trem = 0.0199,
   chiffAttack = 0.0000,
   chiffDecay = 0.2092,
   chiffAmp = 0.1165,
   chiffVelocity = 0.0000,
   noiseAmp = 0.0555,
   envScale = 2.1582,
   attack = 0.0823,
   decay = 0.1524,
   release = 0.2427,
   modDepth = 2.3063,
   velocityDepth = 0.5000,
   ff1 = 186.0000,
   ff2 = 539.0000,
   ff3 = 799.0000,
   amp1 = 0.2128,
   amp2 = 1.0000,
   amp3 = 0.4230,
   lag1 = 0.0000,
   lag2 = 0.2790,
   lag3 = 0.0000,
   vlock = 1)

io(2,"C",
   amp = 0.0700,
   port = 0.0000,
   vfreq = 6.9387,
   vdelay = 1.9623,
   vsens = 0.1575,
   vdepth = 0.0000,
   trem = 0.0380,
   chiffAttack = 0.0598,
   chiffDecay = 0.1490,
   chiffAmp = 0.7651,
   chiffVelocity = 0.0000,
   noiseAmp = 0.7258,
   envScale = 4.0698,
   attack = 0.0386,
   decay = 0.1374,
   release = 0.0680,
   modDepth = 1.0510,
   velocityDepth = 0.5000,
   ff1 = 475.0000,
   ff2 = 1106.0000,
   ff3 = 1786.0000,
   amp1 = 1.0000,
   amp2 = 0.1322,
   amp3 = 0.3713,
   lag1 = 0.0000,
   lag2 = 0.0000,
   lag3 = 0.0000,
   vlock = 1)

