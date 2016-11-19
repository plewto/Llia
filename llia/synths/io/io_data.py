# llia.synths.io.io_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance
from llia.util.lmath import coin,rnd,pick

prototype = {
    "amp" : 0.10,
    "vfreq" : 7.0,
    "vlock" : 1,
    "vnoise" : 0.3,
    "vdelay" : 1.0,
    "vsens" : 0.1,
    "vdepth" : 0.0,
    "vibrato" : 0.0,
    "xPitch" : 0.0,
    "tremRatio" : 1.0,
    "noiseRatio" : 1,
    "chiffAttack" : 0.03,
    "chiffDecay" : 0.2,
    "chiffAmp" : 0.05,
    "chiffVelocity" : 0.5,
    "noiseAmp" : 1.0,
    "blipAttack" : 0.03,
    "blipDecay" : 0.1,
    "blipDepth" : 0.0,
    "blipVelocity" : 0.0,
    "op4Ratio" : 1.0,
    "op4Feedback" : 0.0,
    "op4LFO" : 0.0,
}

for op in (1,2,3):
    for p,v in {"op%dFormant" : 300,
                "op%dRatio" : 1.0,
                "op%dMode" : 0,
                "op%dVelocity" : 0.0,
                "op%dTremolo" : 0.0,
                "op%dModDepth" : 1.0,
                "op%dAttack" : 0.05,
                "op%dDecay" : 0.30,
                "op%dSustain" : 0.5,
                "op%dRelease" : 0.1,
                "op%dModLag" : 0.0,
                "op%dBreakKey" : 60,
                "op%dLeftKeyScale" : 0,
                "op%dRightKeyScale" : 0,
                "op%dAmp" : 1.0,
                "op%dX" : 0.0}.items():
        prototype[p%op] = v
   

        

class Io(Program):

    def __init__(self,name):
        super(Io,self).__init__(name,Io,prototype)
        self.performance = performance()

program_bank = ProgramBank(Io("Init"))
program_bank.enable_undo = False

def vibrato(freq = 7.0,
            lock = 1,
            noise = 0.3,
            delay = 0.0,
            sens = 0.1,
            depth = 0.0,
            x = 0.0,
            tremRatio = 1.0):
    a = {"vfreq" : freq,
         "vlock" : lock,
         "vnoise" : noise,
         "vdelay" : delay,
         "vsens" : sens,
         "vdepth" : depth,
         "vibrato" : 0.0,
         "xPitch" : x,
         "tremRatio" : tremRatio}
    return a
            

def blip(attack = 0.03,
         decay = 0.1,
         depth = 0.0,
         velocity = 0.0):
    return {"blipAttack" : attack,
            "blipDecay" : decay,
            "blipDepth" : depth,
            "blipVelocity" : velocity}

def noise(ratio = 1.0,
          amp = 1.0):
    return {"noiseRatio" : ratio,
            "noiseAmp" : amp}

def chiff(attack = 0.03,
          decay = 0.2,
          velocity = 0.5,
          amp = 1.0):
    a = {"chiffAttack" : attack,
         "chiffDecay" : decay,
         "chiffVelocity" : velocity,
         "chiffAmp" : amp}
    return a
          
def modulator(ratio = 1.0,
              feedback = 0.0,
              lfo = 0.0):
    return {"op4Ratio" : ratio,
            "op4Feedback" : feedback,
            "op4LFO" : lfo}

def carrier(op,
            formant = 1000,
            ratio = 1.0,
            mode = 0,
            velocity = 0.0,
            tremolo = 0.0,
            modDepth = 1.0,
            attack = 0.1,
            decay = 0.2,
            sustain = 1.0,
            release = 0.1,
            lag = 0.0,
            key = 60,
            leftScale = 0,
            rightScale = 0,
            x = 0.0,
            amp = 1.0):
    a = {"op%dFormant" % op : formant,
         "op%dRatio" % op : ratio,
         "op%dMode" % op : mode,
         "op%dVelocity" % op : velocity,
         "op%dTremolo" % op : tremolo,
         "op%dModDepth" % op : modDepth,
         "op%dAttack" % op : attack,
         "op%dDecay" % op : decay,
         "op%dSustain" % op : sustain,
         "op%dRelease" % op : release,
         "op%dModLag" % op : lag,
         "op%dBreakKey" % op : key,
         "op%dLeftKeyScale" % op : leftScale,
         "op%dRightKeyScale" % op : rightScale,
         "op%dAmp" % op : amp,
         "op%dX" % op : x}
    return a

def io(slot, name,
       amp = 0.1,
       vibrato = vibrato(),
       blip = blip(),
       noise = noise(),
       chiff = chiff(),
       modulator = modulator(),
       op1 = carrier(1),
       op2 = carrier(2),
       op3 = carrier(3)):
    p = Io(name)
    p["amp"] = float(amp)
    for d in (vibrato,blip,noise,chiff,modulator,op1,op2,op3):
        for param,val in d.items():
            p[param] = val
    program_bank[slot] = p
    return p

io(0,"Ape")
