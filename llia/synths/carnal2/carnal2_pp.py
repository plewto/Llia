# llia.synths.carnal2.carnal2_pp

def carnal2_pp(program,slot):
    pad=" "*8
    def fval(key):
        return round(float(program[key]),4)
    def ival(key):
        return int(program[key])
    acc = 'carnal2(%d,"%s",\n' % (slot,program.name)
    acc += '%s%s = %5.4f,\n' % (pad,'timebase',fval('timebase'))
    acc += '%s%s = %5.4f,\n' % (pad,'delayTime1',fval('delayTime1'))
    acc += '%s%s = %5.4f,\n' % (pad,'modDepth1',fval('modDepth1'))
    acc += '%s%s = %5.4f,\n' % (pad,'xmodDepth1',fval('xmodDepth1'))
    acc += '%s%s = %5.4f,\n' % (pad,'lfoRatio1',fval('lfoRatio1'))
    acc += '%s%s = %5.4f,\n' % (pad,'feedback1',fval('feedback1'))
    acc += '%s%s = %5.4f,\n' % (pad,'efxMix1',fval('efxMix1'))
    acc += '%s%s = %5.4f,\n' % (pad,'efxPan1',fval('efxPan1'))
    acc += '%s%s = %5.4f,\n' % (pad,'dryMix1',fval('dryMix1'))
    acc += '%s%s = %5.4f,\n' % (pad,'dryPan1',fval('dryPan1'))
    acc += '%s%s = %5.4f,\n' % (pad,'lowcut1',fval('lowcut1'))
    acc += '%s%s = %5.4f,\n' % (pad,'highcut1',fval('highcut1'))
    acc += '%s%s = %d,\n' % (pad,'clipEnable1',ival('clipEnable1'))
    acc += '%s%s = %5.4f,\n' % (pad,'clipGain1',fval('clipGain1'))
    acc += '%s%s = %5.4f,\n' % (pad,'clipThreshold1',fval('clipThreshold1'))
    acc += '%s%s = %5.4f,\n' % (pad,'xfeedback1',fval('xfeedback1'))
    acc += '%s%s = %5.4f,\n' % (pad,'delayTime2',fval('delayTime2'))
    acc += '%s%s = %5.4f,\n' % (pad,'modDepth2',fval('modDepth2'))
    acc += '%s%s = %5.4f,\n' % (pad,'xmodDepth2',fval('xmodDepth2'))
    acc += '%s%s = %5.4f,\n' % (pad,'lfoRatio2',fval('lfoRatio2'))
    acc += '%s%s = %5.4f,\n' % (pad,'feedback2',fval('feedback2'))
    acc += '%s%s = %5.4f,\n' % (pad,'efxMix2',fval('efxMix2'))
    acc += '%s%s = %5.4f,\n' % (pad,'efxPan2',fval('efxPan2'))
    acc += '%s%s = %5.4f,\n' % (pad,'dryMix2',fval('dryMix2'))
    acc += '%s%s = %5.4f,\n' % (pad,'dryPan2',fval('dryPan2'))
    acc += '%s%s = %5.4f,\n' % (pad,'lowcut2',fval('lowcut2'))
    acc += '%s%s = %5.4f,\n' % (pad,'highcut2',fval('highcut2'))
    acc += '%s%s = %d,\n' % (pad,'clipEnable2',ival('clipEnable2'))
    acc += '%s%s = %5.4f,\n' % (pad,'clipGain2',fval('clipGain2'))
    acc += '%s%s = %5.4f,\n' % (pad,'clipThreshold2',fval('clipThreshold2'))
    acc += '%s%s = %5.4f)\n' % (pad,'xfeedback2',fval('xfeedback2'))
    return acc

