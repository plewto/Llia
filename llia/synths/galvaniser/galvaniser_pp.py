# llia.synths.galvaniser.galvaniser_pp

def galvaniser_pp(program,slot):
    pad=" "*11
    def fval(key):
        return round(float(program[key]),4)
    def ival(key):
        return int(program[key])
    acc = 'galvaniser(%d,"%s",\n' % (slot,program.name)
    acc += '%s%s = %5.4f,\n' % (pad,'feedback',fval('feedback'))
    acc += '%s%s = %5.4f,\n' % (pad,'tone',fval('tone'))
    acc += '%s%s = %5.4f,\n' % (pad,'filter',fval('filter'))
    acc += '%s%s = %5.4f,\n' % (pad,'res',fval('res'))
    acc += '%s%s = %5.4f,\n' % (pad,'lfoFreq',fval('lfoFreq'))
    acc += '%s%s = %5.4f,\n' % (pad,'modDepth',fval('modDepth'))
    acc += '%s%s = %5.4f,\n' % (pad,'efxmix',fval('efxmix'))
    acc += '%s%s = %5.4f)\n' % (pad,'amp',fval('amp'))
    return acc

