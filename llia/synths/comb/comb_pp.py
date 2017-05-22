# llia.synths.comb.comb_pp

def comb_pp(program,slot):
    pad=" "*5
    def fval(key):
        return round(float(program[key]),4)
    def ival(key):
        return int(program[key])
    acc = 'comb(%d,"%s",\n' % (slot,program.name)
    acc += '%s%s = %5.4f,\n' % (pad,'amp',fval('amp'))
    acc += '%s%s = %5.4f,\n' % (pad,'delayScale',fval('delayScale'))
    acc += '%s%s = %5.4f,\n' % (pad,'delay',fval('delay'))
    acc += '%s%s = %d,\n' % (pad,'phase',ival('phase'))
    acc += '%s%s = %5.4f)\n' % (pad,'wet',fval('wet'))
    return acc

