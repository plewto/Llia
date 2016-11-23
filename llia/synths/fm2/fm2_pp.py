# llia.synths.fm2.fm2_pp

from __future__ import print_function

import llia.util.lmath as math
from llia.performance_edit import performance_pp


def amp_to_db(amp):
    return int(math.amp_to_db(amp))

def pp_fm2(program, slot):
    def cap(s):
        return s[0].upper()+s[1:]
    def db(key):
        return int(amp_to_db(program[key]))
    def fval(key):
        return round(float(program[key]),4)
    def ival(key):
        return int(program[key])
    pad = ' '*8
    pad2 = pad + ' '*10
    pad3 = pad + ' '*7
    frmt = 'fm2(%3d, "%s", amp=%d, port=%5.3f,\n'
    values = (slot, program.name, db("amp"), fval("port"))
    acc = frmt % values
    frmt = '%sexternal={"scale" : %5.3f,\n'
    values = (pad, fval("xScale"))
    acc += frmt % values
    for p in (("xBias","bias"),("xPitch","pitch"),("xModDepth", "mod")):
        value = fval(p[0])
        frmt = '%s"%s" : %5.3f'
        acc += (frmt % (pad2, p[1], value))
        if p[1] == "mod":
            acc += ('},\n')
        else:
            acc += (',\n')
    frmt = '%slfo = {"freq" : %5.3f,\n'
    acc += frmt % (pad,fval("lfoFreq"))
    for p in (("lfoDelay","delay"),("vsens","vsens"),("vdepth","vdepth")):
        value = fval(p[0])
        frmt = '%s"%s" : %5.3f'
        acc += frmt % (pad3, p[1], value)
        if p[1] == "vdepth":
            acc += '},\n'
        else:
            acc += ',\n'

    padefx = pad+' '*7
    frmt = '%sefx = {"attack" : %5.4f,\n'
    acc += frmt % (pad,fval("efxAttack"))
    alst = (("decay1","efxDecay1"),
            ("decay2","efxDecay2"),
            ("release","efxRelease"),
            ("breakPoint","efxBreakpoint"),
            ("sustain","efxSustain"),
            ("lfo-ratio","efxLfoRatio"),
            ("flanger-delay","flangerDelay"),
            ("flanger-feedback","flangerFeedback"),
            ("flanger-lfo-depth","flangerLfoDepth"),
            ("ps-ratio","psRatio"),
            ("ps-pitch-dispersion","psPDispersion"),
            ("ps-time-dispersion","psTDispersion"),
            ("ps-lfo-depth","psLfoDepth"),
            ("efx-mix","efxMix"),
            ("efx-amp","efxAmp"))
    for a,p in alst:
        val = fval(p)
        acc += '%s"%s" : %5.4f,\n' % (padefx,a,val)
    frmt = '%s"env-cycle" :  %d},\n' % (padefx,ival("efxGateHold"))
    acc += frmt
            
    frmt = '%sop1 = {"enable" : %s,\n'
    value = program["op1Enable"] == 1
    acc += frmt % (pad, value)
    for p in (('op1Ratio','ratio'), 
              ('op1Bias','bias'), 
              ('op1Attack',  'attack'),  
              ('op1Decay1','decay1'), 
              ('op1Decay2','decay2'), 
              ('op1Release' , 'release'),  
              ('op1Breakpoint','breakpoint'), 
              ('op1Sustain','sustain'), 
              ('op1Lfo','lfo'), 
              ('op1Velocity','velocity')):
        value = fval(p[0])
        frmt = '%s"%s" : %6.4f,\n'
        acc += frmt % (pad3, p[1], value)
    for p in (('op1Keybreak','break-key'), 
              ('op1LeftScale','left-scale'), 
              ('op1RightScale', 'right-scale')) :
        value = ival(p[0])
        frmt = '%s"%s" : %d,\n'
        acc += frmt % (pad3, p[1], value)
    acc += '%s"amp" : %d,\n' % (pad3, db("amp"))
    hold = int(program["op1GateHold"]) == 1
    acc += '%s"env-cycle" : %s},\n' % (pad3, hold)
    frmt = '%sop2 = {"enable" : %s,\n'
    value = program["op2Enable"] == 1
    acc += frmt % (pad, value)
    for p in (('op2Ratio','ratio'), 
              ('op2Bias','bias'),
              ('op2Amp' , 'amp'),
              ('op2Attack',  'attack'),  
              ('op2Decay1','decay1'), 
              ('op2Decay2','decay2'), 
              ('op2Release' , 'release'),  
              ('op2Breakpoint','breakpoint'), 
              ('op2Sustain','sustain'),
              ('op2Feedback', 'feedback'),
              ('op2Lfo','lfo'), 
              ('op2Velocity','velocity')):
        value = fval(p[0])
        frmt = '%s"%s" : %6.4f,\n'
        acc += frmt % (pad3, p[1], value)
    for p in (('op2AmpRange', 'modRange'),
              ('op2Keybreak','break-key'), 
              ('op2LeftScale','left-scale'), 
              ('op2RightScale', 'right-scale')) :
        value = ival(p[0])
        frmt = '%s"%s" : %d,\n'
        acc += frmt % (pad3, p[1], value)
    hold = int(program["op2GateHold"]) == 1
    acc += '%s"env-cycle" : %s})\n' % (pad3, hold)
    return acc
        
                                                   
