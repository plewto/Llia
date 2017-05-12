# llia.synths.ss2.ss2_pp

def ss2_pp(program,slot):
    pad=" "*4
    def fval(key):
        return round(float(program[key]),4)
    def ival(key):
        return int(program[key])
    acc = 'ss2(%d,"%s",\n' % (slot,program.name)
    acc += '%s%s = %5.4f,\n' % (pad,'pw',fval('pw'))
    acc += '%s%s = %d,\n' % (pad,'track',ival('track'))
    acc += '%s%s = %d,\n' % (pad,'wave',ival('wave'))
    acc += '%s%s = %d,\n' % (pad,'filter',ival('filter'))
    acc += '%s%s = %d,\n' % (pad,'envSelect',ival('envSelect'))
    acc += '%s%s = %5.4f,\n' % (pad,'attack',fval('attack'))
    acc += '%s%s = %5.4f,\n' % (pad,'decay',fval('decay'))
    acc += '%s%s = %5.4f,\n' % (pad,'sustain',fval('sustain'))
    acc += '%s%s = %5.4f,\n' % (pad,'release',fval('release'))
    acc += '%s%s = %5.4f)\n' % (pad,'amp',fval('amp'))
    return acc

