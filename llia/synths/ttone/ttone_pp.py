# llia.synths.ttone.ttone_pp

def ttone_pp(program,slot):
    pad=" "*6
    def fval(key):
        return round(float(program[key]),4)
    def ival(key):
        return int(program[key])
    acc = 'ttone(%d,"%s",\n' % (slot,program.name)
    acc += '%s%s = %5.4f,\n' % (pad,'ratio',fval('ratio'))
    acc += '%s%s = %5.4f,\n' % (pad,'bias',fval('bias'))
    acc += '%s%s = %d,\n' % (pad,'wave',ival('wave'))
    acc += '%s%s = %5.4f)\n' % (pad,'amp',fval('amp'))
    return acc

