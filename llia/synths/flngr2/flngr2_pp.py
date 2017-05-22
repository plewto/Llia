# llia.synths.flngr2.flngr2_pp

def flngr2_pp(program,slot):
    pad=" "*7
    def fval(key):
        return round(float(program[key]),4)
    def ival(key):
        return int(program[key])
    acc = 'flngr2(%d,"%s",\n' % (slot,program.name)
    acc += '%s%s = %5.4f,\n' % (pad,'timebase',fval('timebase'))
    acc += '%s%s = %5.4f,\n' % (pad,'delay1',fval('delay1'))
    acc += '%s%s = %5.4f,\n' % (pad,'xmod1',fval('xmod1'))
    acc += '%s%s = %5.4f,\n' % (pad,'depth1',fval('depth1'))
    acc += '%s%s = %5.4f,\n' % (pad,'lfoRatio1',fval('lfoRatio1'))
    acc += '%s%s = %5.4f,\n' % (pad,'feedback1',fval('feedback1'))
    acc += '%s%s = %5.4f,\n' % (pad,'xfeedback1',fval('xfeedback1'))
    acc += '%s%s = %5.4f,\n' % (pad,'lowpass1',fval('lowpass1'))
    acc += '%s%s = %5.4f,\n' % (pad,'efxMix1',fval('efxMix1'))
    acc += '%s%s = %5.4f,\n' % (pad,'efxPan1',fval('efxPan1'))
    acc += '%s%s = %5.4f,\n' % (pad,'delay2',fval('delay2'))
    acc += '%s%s = %5.4f,\n' % (pad,'xmod2',fval('xmod2'))
    acc += '%s%s = %5.4f,\n' % (pad,'depth2',fval('depth2'))
    acc += '%s%s = %5.4f,\n' % (pad,'lfoRatio2',fval('lfoRatio2'))
    acc += '%s%s = %5.4f,\n' % (pad,'feedback2',fval('feedback2'))
    acc += '%s%s = %5.4f,\n' % (pad,'xfeedback2',fval('xfeedback2'))
    acc += '%s%s = %5.4f,\n' % (pad,'lowpass2',fval('lowpass2'))
    acc += '%s%s = %5.4f,\n' % (pad,'efxMix2',fval('efxMix2'))
    acc += '%s%s = %5.4f)\n' % (pad,'efxPan2',fval('efxPan2'))
    acc += '%s%s = %5.4f,\n' % (pad,'dryMix2',fval('dryMix2'))
    acc += '%s%s = %5.4f)\n' % (pad,'dryPan2',fval('dryPan2'))
    acc += '%s%s = %5.4f,\n' % (pad,'dryMix1',fval('dryMix1'))
    acc += '%s%s = %5.4f,\n' % (pad,'dryPan1',fval('dryPan1'))
    return acc

