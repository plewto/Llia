# llia.synths.combo.combo_pp

def combo_pp(program,slot):
    pad=" "*6
    def fval(key):
        return round(float(program[key]),4)
    # def ival(key):
    #     return int(program[key])
    acc = 'combo(%d,"%s",\n' % (slot,program.name)
    acc += '%s%s = %5.4f,\n' % (pad,'flute8',fval('flute8'))
    acc += '%s%s = %5.4f,\n' % (pad,'flute4',fval('flute4'))
    acc += '%s%s = %5.4f,\n' % (pad,'flute3',fval('flute3'))
    acc += '%s%s = %5.4f,\n' % (pad,'flute2',fval('flute2'))
    acc += '%s%s = %5.4f,\n' % (pad,'reed16',fval('reed16'))
    acc += '%s%s = %5.4f,\n' % (pad,'reed8',fval('reed8'))
    acc += '%s%s = %5.4f,\n' % (pad,'reedWave',fval('reedWave'))
    acc += '%s%s = %5.4f,\n' % (pad,'vspeed',fval('vspeed'))
    acc += '%s%s = %5.4f,\n' % (pad,'vdepth',fval('vdepth'))
    acc += '%s%s = %5.4f,\n' % (pad,'chorus',fval('chorus'))
    acc += '%s%s = %5.4f)\n' % (pad,'amp',fval('amp'))
    return acc

