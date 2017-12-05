# llia.synths.fxstack.fxstack_pp

def fxstack_pp(program,slot):
    pad=" "*8
    def fval(key):
        return round(float(program[key]),4)
    def ival(key):
        return int(program[key])
    def gain():
        i,o = fval("inputGain"), fval("outputGain")
        frmt = "%sgain(input=%5.4f, output=%5.4f),\n"
        return frmt % (pad, i, o)
    def env():
        gain = fval("envGain")
        att = fval("attack")
        rel = fval("release")
        frmt = "%senv(gain=%5.4f, attack=%5.4f, release=%5.4f),\n"
        return frmt % (pad,gain,att,rel)
    def lfo():
        f1,f2,mod = fval("lfo1Freq"),fval("lfo2Freq"),fval("lfo2Mod")
        frmt = "%slfo(freq1=%5.4f, freq2=%5.4f, mod2=%5.4f),\n"
        return frmt % (pad,f1,f2,mod)
    def clipper():
        drive,lfo,mix = fval("clipDrive"),fval("clipLfo1"),fval("clipMix")
        frmt = "%sclipper(drive=%5.4f, lfo1=%5.4f, mix=%5.4f),\n"
        return frmt % (pad,drive,lfo,mix)
    def wha():
        freq,env,lfo = fval("filterFreq"),fval("filterEnv"),fval("filterLfo2")
        res, mix = fval("filterRes"), fval("filterMix")
        frmt = "%swha(freq=%.4f, env=%5.4f, lfo2=%5.4f, res=%5.4f, mix=%5.4f),\n"
        return frmt % (pad,freq,env,lfo,res,mix)
    def flanger():
        d1,d2,lfo = fval("flangerDelay1"),fval("flangerDelay2"),fval("flangerLfo1")
        fb,mix = fval("flangerFeedback"),fval("flangerMix")
        frmt = "%sflanger(delay1=%5.4f, delay2=%5.4f, lfo1=%5.4f, feedback=%5.4f, mix=%5.4f),\n"
        return frmt % (pad,d1,d2,lfo,fb,mix)
    def delay1():
        dly,lfo = fval("delay1Time"),fval("delay1Lfo1")
        fb,xfb = fval("delay1Feedback"),fval("delay1XFeedback")
        filt = fval("delay1Lowpass")
        mix,pan = fval("delay1Mix"),fval("delay1Pan")
        frmt = "%sdelay1(delay=%5.4f, lfo1=%5.4f, fb=%5.4f, xfb=%5.4f, lowpass=%5.4f, mix=%5.4f, pan=%5.4f),\n"
        return frmt % (pad,dly,lfo,fb,xfb,filt,mix,pan)
    def delay2():
        dly,lfo = fval("delay2Time"),fval("delay2Lfo2")
        fb,xfb = fval("delay2Feedback"),fval("delay2XFeedback")
        filt = fval("delay2Highpass")
        mix,pan = fval("delay2Mix"),fval("delay2Pan")
        frmt = "%sdelay2(delay=%5.4f, lfo2=%5.4f, fb=%5.4f, xfb=%5.4f, highpass=%5.4f, mix=%5.4f, pan=%5.4f),\n"
        return frmt % (pad,dly,lfo,fb,xfb,filt,mix,pan)
    def reverb():
        room,damp = fval("reverbRoomSize"),fval("reverbDamping")
        env,lfo = fval("reverbEnv"),fval("reverbLfo2")
        mix = fval("reverbMix")
        frmt = "%sreverb(room=%5.4f, damping=%5.4f, env=%5.4f, lfo2=%5.4f, mix=%5.4f))\n"
        return frmt % (pad,room,damp,env,lfo,mix)
                       
    acc = 'fxstack(%d,"%s",\n' % (slot,program.name)
    acc += gain()
    acc += env()
    acc += lfo()
    acc += clipper()
    acc += wha()
    acc += flanger()
    acc += delay1()
    acc += delay2()
    acc += reverb()
    return acc

