# llia.synths.scanner.scanner_pp

def scanner_pp(program,slot):
    pad=" "*8
    def fval(key):
        return round(float(program[key]),4)
    def ival(key):
        return int(program[key])
    acc = 'scanner(%d,"%s",\n' % (slot,program.name)
    acc += '%s%s = %5.4f,\n' % (pad,'scanRate',fval('scanRate'))
    acc += '%s%s = %5.4f,\n' % (pad,'wave',fval('wave'))
    acc += '%s%s = %5.4f,\n' % (pad,'delay',fval('delay'))
    acc += '%s%s = %5.4f,\n' % (pad,'modDepth',fval('modDepth'))
    acc += '%s%s = %5.4f,\n' % (pad,'feedback',fval('feedback'))
    acc += '%s%s = %d,\n' % (pad,'lowpass',ival('lowpass'))
    acc += '%s%s = %5.4f,\n' % (pad,'dryMix',fval('dryMix'))
    acc += '%s%s = %5.4f,\n' % (pad,'wet1Mix',fval('wet1Mix'))
    acc += '%s%s = %5.4f,\n' % (pad,'wet2Mix',fval('wet2Mix'))
    acc += '%s%s = %5.4f)\n' % (pad,'xmodDepth',fval('xmodDepth'))
    return acc

