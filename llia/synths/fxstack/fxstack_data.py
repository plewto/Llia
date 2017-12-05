# llia.synths.Fxstack.Fxstack_data

from __future__ import print_function
from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance

prototype = {
 	"inputGain" : 1.0,          #  0..2
	"outputGain" : 1.0,         #  0..2
	"envGain" : 1.0,            #  1..100
	"attack" : 0.0,             #  0..2
	"release" : 0.0,            #  0..2
	"lfo1Freq" : 1.0,           #  0..99.999
	"lfo2Freq" : 1.0,           #  0..99.999
	"lfo2Mod" : 0.0,            #  0..1

        "clipDrive" : 1.0,          #  0..1
	"clipLfo1" : 0.0,           #  0..1
	"clipMix" : 0.0,            #  0..1
    
	"filterFreq" : 0.5,         #  0..1
	"filterEnv" : 0.0,          #  0..1
	"filterLfo2" : 0.0,         #  0..1
	"filterRes" : 0.0,          #  0..1
	"filterMix" : 0.0,          #  0..1

        "flangerDelay1" : 0.5,      #  0..1
	"flangerDelay2" : 0.6,      #  0..1
	"flangerLfo1" : 0.0,        #  0..1
	"flangerFeedback" : 0.0,    # -1..+1 
	"flangerMix" : 0.0,         #  0..1

        "delay1Time" : 0.1,         #  0..1
	"delay1Lfo1" : 0.0,         #  0..1
	"delay1Feedback" : 0.0,     # -1..+1
	"delay1XFeedback" : 0.0,    # -1..+1
	"delay1Lowpass" : 1.0,      #  0..1
	"delay1Mix" : 0.0,          #  0..1
	"delay1Pan" : -0.75,        # -1..+1
    
	"delay2Time" : 0.1,         #  0..1
	"delay2Lfo2" : 0.0,         #  0..1
	"delay2Feedback" : 0.0,     # -1..+1
	"delay2XFeedback" : 0.0,    # -1..+1
	"delay2Highpass" : 0.0,     #  0..1
	"delay2Mix" : 0.0,          #  0..1
	"delay2Pan" : 0.75,         # -1..+1

        "reverbRoomSize" : 0.5,     #  0..1
	"reverbDamping" : 0.5,      #  0..1
	"reverbEnv" : 0.0,          #  0..1
	"reverbLfo2" : 0.0,         #  0..1
	"reverbMix" : 0.0}          #  0..1


class Fxstack(Program):

    def __init__(self,name):
        super(Fxstack,self).__init__(name,Fxstack,prototype)
        self.performance = performance()

program_bank = ProgramBank(Fxstack("Init"))

def fval(n, mn=0,mx=1):
    return round(min(max(float(n),mn),mx), 4)

def gain(input=1.00, output=1.00):
    return {"inputGain" : fval(input,0,2),
            "outputGain" : fval(output,0,2)}

def env(gain=1, attack=0, release=0):
    return {"envGain": fval(gain,mx=100),
            "attack" : fval(attack),
            "release" : fval(release)}

def lfo(freq1=1.00, freq2=1.00, mod2=0.00):
    return {"lfo1Freq":fval(freq1,0,99.999),
            "lfo2Freq":fval(freq2,0,99.999),
            "lfo2Mod":fval(mod2)}

def clipper(drive=1, lfo1=0.00, mix=0.00):
    return {"clipDrive" : fval(drive),
            "clipLfo1" : fval(lfo1),
            "clipMix" : fval(mix)}

def wha(freq=0.50, env=0.50, lfo2=0.00, res=0.3, mix=0.0):
    return {"filterFreq" : fval(freq),
            "filterEnv" : fval(env),
            "filterLfo2" : fval(lfo2),
            "filterRes" : fval(res),
            "filterMix" : fval(mix)}

def flanger(delay1=0.50, delay2=0.55, lfo1=0.2, feedback=-0.2, mix=0.0):
    return {"flangerDelay1" : fval(delay1),
            "flangerDelay2" : fval(delay2),
            "flangerLfo1" : fval(lfo1),
            "flangerFeedback" : fval(feedback, -1, 1),
            "flangerMix" : fval(mix)}

def delay1(delay=0.100, lfo1=0.00, fb=0.00, xfb=0.00, lowpass=1.00, mix=0.00, pan=-0.75):
    return {"delay1Time" : fval(delay),
            "delay1Lfo1" : fval(lfo1),
            "delay1Feedback" : fval(fb,-1,1),
            "delay1XFeedback" : fval(xfb,-1,1),
            "delay1Lowpass" : fval(lowpass),
            "delay1Mix" : fval(mix),
            "delay1Pan" : fval(pan,-1,1)}

def delay2(delay=0.100, lfo2=0.00, fb=0.00, xfb=0.00, highpass=0.00, mix=0.00, pan=-0.75):
    return {"delay2Time" : fval(delay),
            "delay2Lfo2" : fval(lfo2),
            "delay2Feedback" : fval(fb,-1,1),
            "delay2XFeedback" : fval(xfb,-1,1),
            "delay2Highpass" : fval(highpass),
            "delay2Mix" : fval(mix),
            "delay2Pan" : fval(pan,-1,1)}
            
def reverb(room=0.5, damping=0.5, env=0.00, lfo2=0.00, mix=0.00):
    return {"reverbRoomSize" : fval(room),
            "reverbDamping" : fval(damping),
            "reverbEnv" : fval(env),
            "reverbLfo2" : fval(lfo2),
            "reverbMix" : fval(mix)}

def fxstack(slot, name,
            gain=gain(input=1.0, output=1.0),
            env=env(gain=1, attack=0.00, release=0.00),
            lfo=lfo(freq1=1.00, freq2=4.00, mod2=0.00),
            clipper=clipper(drive=1.00, lfo1=0.00, mix=0.00),
            wha=wha(freq=0.5, env=0.50, lfo2=0.00, res=0.3, mix=0.0),
            flanger=flanger(delay1=0.50,delay2=0.55,lfo1=0.20, feedback=-0.20, mix=0.00),
            delay1=delay1(delay=0.100, lfo1=0.00, fb=0.00, xfb=0.00, lowpass=1.00, mix=0.00, pan=0.00),
            delay2=delay2(delay=0.100, lfo2=0.00, fb=0.00, xfb=0.00, highpass=1.00, mix=0.00, pan=0.00),
            reverb=reverb(room=0.5,damping=0.5,env=0.0, lfo2=0.0, mix=0.0)):
    p = Fxstack(name)
    p.update(gain)
    p.update(env)
    p.update(lfo)
    p.update(clipper)
    p.update(wha)
    p.update(flanger)
    p.update(delay1)
    p.update(delay2)
    p.update(reverb)
    program_bank[slot] = p
    return p

fxstack(0,"Bypass",
        gain(input=1.0000, output=1.0000),
        env(gain=1.0000, attack=0.0000, release=0.0000),
        lfo(freq1=1.0000, freq2=4.0000, mod2=0.0000),
        clipper(drive=1.0000, lfo1=0.0000, mix=0.0000),
        wha(freq=0.5000, env=0.4975, lfo2=0.0000, res=0.2965, mix=0.0000),
        flanger(delay1=0.5000, delay2=0.5477, lfo1=0.2000, feedback=-0.2000, mix=0.0000),
        delay1(delay=0.1000, lfo1=0.0000, fb=0.0000, xfb=0.0000, lowpass=1.0000, mix=0.0000, pan=0.0000),
        delay2(delay=0.1000, lfo2=0.0000, fb=0.0000, xfb=0.0000, highpass=1.0000, mix=0.0000, pan=0.0000),
        reverb(room=0.5000, damping=0.5000, env=0.0000, lfo2=0.0000, mix=0.0000))

fxstack(1,"Simple Clipping",
        gain(input=1.0000, output=1.0000),
        env(gain=1.0000, attack=0.0000, release=0.0000),
        lfo(freq1=1.0000, freq2=4.0000, mod2=0.0000),
        clipper(drive=0.7990, lfo1=0.0000, mix=0.7839),
        wha(freq=0.4975, env=0.4975, lfo2=0.0000, res=0.2965, mix=0.0000),
        flanger(delay1=0.4975, delay2=0.5477, lfo1=0.1960, feedback=-0.2000, mix=0.0000),
        delay1(delay=0.1000, lfo1=0.0000, fb=0.0000, xfb=0.0000, lowpass=1.0000, mix=0.0000, pan=0.0000),
        delay2(delay=0.1000, lfo2=0.0000, fb=0.0000, xfb=0.0000, highpass=1.0000, mix=0.0000, pan=0.0000),
        reverb(room=0.4975, damping=0.4975, env=0.0000, lfo2=0.0000, mix=0.2663))

fxstack(2,"Env Follow",
        gain(input=1.0000, output=1.0000),
        env(gain=76.2400, attack=0.0000, release=0.0000),
        lfo(freq1=1.0000, freq2=1.0000, mod2=0.0000),
        clipper(drive=0.2613, lfo1=0.0000, mix=0.7085),
        wha(freq=0.1106, env=0.4020, lfo2=0.0000, res=0.7387, mix=0.8392),
        flanger(delay1=0.4975, delay2=0.5980, lfo1=0.0000, feedback=0.0000, mix=0.0000),
        delay1(delay=0.1000, lfo1=0.0000, fb=0.0000, xfb=0.0000, lowpass=1.0000, mix=0.0000, pan=-0.7500),
        delay2(delay=0.1000, lfo2=0.0000, fb=0.0000, xfb=0.0000, highpass=0.0000, mix=0.0000, pan=0.7500),
        reverb(room=0.5000, damping=0.5000, env=0.0000, lfo2=0.0000, mix=0.0000))

fxstack(3,"Light Flanging",
        gain(input=1.0000, output=1.0000),
        env(gain=1.0000, attack=0.0000, release=0.0000),
        lfo(freq1=1.0000, freq2=1.0000, mod2=0.0000),
        clipper(drive=1.0000, lfo1=0.0000, mix=0.0000),
        wha(freq=0.4975, env=0.0000, lfo2=0.0000, res=0.0000, mix=0.0000),
        flanger(delay1=0.5000, delay2=0.6000, lfo1=0.1558, feedback=-0.1700, mix=0.8392),
        delay1(delay=0.1000, lfo1=0.0000, fb=0.0000, xfb=0.0000, lowpass=1.0000, mix=0.0000, pan=-0.7500),
        delay2(delay=0.1000, lfo2=0.0000, fb=0.0000, xfb=0.0000, highpass=0.0000, mix=0.0000, pan=0.7500),
        reverb(room=0.5000, damping=0.1256, env=0.0000, lfo2=0.0000, mix=0.3668))

fxstack(4,"Chorusing",
        gain(input=1.0000, output=1.0000),
        env(gain=1.0000, attack=0.0000, release=0.0000),
        lfo(freq1=2.0000, freq2=6.0000, mod2=0.0000),
        clipper(drive=1.0000, lfo1=0.0000, mix=0.0000),
        wha(freq=0.5477, env=0.0000, lfo2=0.3367, res=0.5729, mix=0.4925),
        flanger(delay1=0.2915, delay2=0.6000, lfo1=0.1558, feedback=-0.2500, mix=0.5176),
        delay1(delay=0.0100, lfo1=0.2513, fb=0.4800, xfb=-0.4400, lowpass=0.7387, mix=0.5276, pan=-0.7500),
        delay2(delay=0.0230, lfo2=0.7236, fb=0.5800, xfb=-0.4400, highpass=0.2261, mix=0.4925, pan=0.7500),
        reverb(room=0.8643, damping=0.2965, env=0.0000, lfo2=0.0000, mix=0.5327))

fxstack(5,"Mod4",
        gain(input=1.0000, output=1.0000),
        env(gain=1.0000, attack=0.0000, release=0.0000),
        lfo(freq1=1.1000, freq2=4.0000, mod2=0.4874),
        clipper(drive=0.1709, lfo1=0.9447, mix=0.7538),
        wha(freq=0.3166, env=0.0000, lfo2=0.3668, res=0.5327, mix=0.5678),
        flanger(delay1=0.4975, delay2=0.6000, lfo1=0.0000, feedback=0.0000, mix=0.0000),
        delay1(delay=0.1000, lfo1=0.0000, fb=-0.4800, xfb=0.5000, lowpass=0.7940, mix=0.3065, pan=-0.7500),
        delay2(delay=0.1250, lfo2=0.0000, fb=0.5200, xfb=-0.5600, highpass=0.2613, mix=0.2412, pan=0.7500),
        reverb(room=0.8543, damping=0.4975, env=0.0000, lfo2=0.4221, mix=0.5126))

fxstack(6,"Simple Tremolo",
        gain(input=1.0000, output=1.0000),
        env(gain=1.0000, attack=0.0000, release=0.0000),
        lfo(freq1=6.0000, freq2=1.0000, mod2=0.0000),
        clipper(drive=0.0000, lfo1=0.4724, mix=0.4774),
        wha(freq=0.4975, env=0.0000, lfo2=0.0000, res=0.0000, mix=0.0000),
        flanger(delay1=0.5000, delay2=0.6000, lfo1=0.0000, feedback=0.0000, mix=0.0000),
        delay1(delay=0.1000, lfo1=0.0000, fb=0.0000, xfb=0.0000, lowpass=1.0000, mix=0.0000, pan=-0.7500),
        delay2(delay=0.1000, lfo2=0.0000, fb=0.0000, xfb=0.0000, highpass=0.0000, mix=0.0000, pan=0.7500),
        reverb(room=0.5000, damping=0.5000, env=0.0000, lfo2=0.0000, mix=0.0000))

fxstack(7,"Heavy Clip",
        gain(input=1.0000, output=1.0000),
        env(gain=100.0000, attack=0.0000, release=0.0000),
        lfo(freq1=1.0000, freq2=1.0000, mod2=0.0000),
        clipper(drive=1.0000, lfo1=0.0000, mix=1.0000),
        wha(freq=0.4975, env=0.0000, lfo2=0.0000, res=0.0000, mix=0.0000),
        flanger(delay1=0.4975, delay2=0.5980, lfo1=0.0000, feedback=0.0000, mix=0.0000),
        delay1(delay=0.1000, lfo1=0.0000, fb=0.0000, xfb=0.0000, lowpass=1.0000, mix=0.0000, pan=-0.7500),
        delay2(delay=0.1000, lfo2=0.0000, fb=0.0000, xfb=0.0000, highpass=0.0000, mix=0.0000, pan=0.7500),
        reverb(room=0.9497, damping=0.4975, env=1.0000, lfo2=0.4874, mix=0.5176))

fxstack(8,"Cross Delay",
        gain(input=1.0000, output=1.0000),
        env(gain=1.0000, attack=0.0000, release=0.0000),
        lfo(freq1=4.0000, freq2=0.1000, mod2=0.0000),
        clipper(drive=1.0000, lfo1=0.0000, mix=0.0000),
        wha(freq=0.5000, env=0.0000, lfo2=0.0000, res=0.0000, mix=0.0000),
        flanger(delay1=0.5000, delay2=0.5980, lfo1=0.0000, feedback=0.0000, mix=0.0000),
        delay1(delay=0.5000, lfo1=0.1407, fb=0.8000, xfb=-0.6600, lowpass=0.3317, mix=0.0000, pan=0.0000),
        delay2(delay=0.2540, lfo2=0.1508, fb=0.8000, xfb=-0.5200, highpass=0.4322, mix=0.4925, pan=-0.0200),
        reverb(room=0.5000, damping=0.8543, env=0.0000, lfo2=0.0000, mix=0.4774))

