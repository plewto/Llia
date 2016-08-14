# llia.synths.pulsegen.pulsegen_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance
from llia.util.lmath import coin, rnd, pick

RATIOS = (0.0625, 0.125, 0.25, 0.333, 0.5, 0.667, 1.0,
          1.333, 1.5, 1.667, 2, 2.5, 3, 3.5, 4, 5, 6,
          7, 8, 9, 10, 11, 12, 13, 14, 15, 16)

PROB_RATIOS = (0.0625, 0.125, 0.25, 0.25, 0.333, 0.5, 0.5, 0.5, 0.667,
               1, 1, 1, 1.333, 1.333, 1.5, 1.5, 1.667, 2, 2, 2, 2.5, 3, 3, 3,
               3.5, 4, 5, 6, 7, 8)
               

AMPS = (0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0)

prototype = {
    "clockFreq" : 1.0,
    "ratioA" : 1.0,
    "ratioB" : 2.0,
    "ratioC" : 3.0,
    "ratioD" : 4.0,
    "ratioE" : 5.0,
    "ratioF" : 6.0,
    "yAmpA" : 1.0, 
    "yAmpB" : 1.0,
    "yAmpC" : 1.0,
    "yAmpD" : 0.0,
    "yAmpE" : 0.0,
    "yAmpF" : 0.0,
    "yLag" : 0.0,  
    "yScale" : 1.0,
    "yBias" : 0.0,
    "zAmpA" : 0.0,
    "zAmpB" : 0.0,
    "zAmpC" : 0.0,
    "zAmpD" : 1.0,
    "zAmpE" : 1.0,
    "zAmpF" : 1.0,
    "zLag" : 0.0,
    "zScale" : 1.0,
    "zBias" : 0.0}


class Pulsegen(Program):

    def __init__(self, name):
        super(Pulsegen, self).__init__(name, "PulseGen", prototype)
        self.performance = performance()

program_bank = ProgramBank(Pulsegen("Init"))
program_bank.enable_undo = False


def _fill(lst, template):
    acc = []
    for i, dflt in enumerate(template):
        try:
            v = lst[i]
        except IndexError:
            v = dflt
        acc.append(float(v))
    return acc
        
def pulsegen(slot, name,
             clockFreq = 1.0,
             ratios = [1.00, 2.00, 3.00, 4.00, 5.00, 6.00],
             ymix = [1.00, 1.00, 1.00, 0.00, 0.00, 0.00],
             zmix = [0.00, 0.00, 0.00, 1.00, 1.00, 1.00],
             ylag = 0.0, yscale = 1.0, ybias = 0.0,
             zlag = 0.0, zscale = 1.0, zbias = 0.0):
    p = Pulsegen(name)
    ratios = _fill(ratios, [1.00, 2.00, 3.00, 4.00, 5.00, 6.00])
    ymix = _fill(ymix, [1.00, 1.00, 1.00, 0.00, 0.00, 0.00])
    zmix = _fill(zmix, [0.00, 0.00, 0.00, 1.00, 1.00, 1.00])
    p['clockFreq'] = abs(float(clockFreq))
    for i,a in enumerate('ABCDEF'):
        p['ratio%s' % a] = ratios[i]
        p['yAmp%s' % a] = ymix[i]
        p['zAmp%s' % a] = zmix[i]
    p['yLag'] = float(ylag)
    p['yScale'] = float(yscale)
    p['ybias'] = float(ybias)
    p['zLag'] = float(zlag)
    p['zScale'] = float(zscale)
    p['zbias'] = float(zbias)
    program_bank[slot] = p
    return p
        
        
def pp(program, slot=127):
    def fval(key):
        return float(program[key])
    pad = ' '*5
    acc = 'pulsegen(%d, "%s",\n' % (slot, program.name)
    acc += '%sclockFreq = %5.4f,\n' % (pad, fval('clockFreq'))
    rcc = '%sratios = [' % pad
    ycc = '%symix = [' % pad
    zcc = '%szmix = [' % pad
    for a in 'ABCDEF':
        rcc += '%5.4f' % fval('ratio%s' % a)
        ycc += '%5.4f' % fval('yAmp%s' % a)
        zcc += '%5.4f' % fval('zAmp%s' % a)
        if a == 'F':
            end = '],\n'
        else:
            end = ','
        rcc += end
        ycc += end
        zcc += end
    acc += rcc
    acc += ycc
    acc += zcc
    values = (pad, fval('yLag'), fval('yScale'), fval('yBias'))
    acc += '%sylag=%5.4f, yscale=%5.4f, ybias=%5.4f,\n' % values
    values = (pad, fval('zLag'), fval('zScale'), fval('zBias'))
    acc += '%szlag=%5.4f, zscale=%5.4f, zbias=%5.4f)\n' % values
    return acc
    
def random_pulsegen(slot=127, *_):
    freq = coin(0.75, 1, rnd(5))
    ratios, ymix, zmix = [], [], []
    for n in "ABCDEF":
        r = None
        while r is None or r in ratios:
            r = pick(PROB_RATIOS)
        y = coin(0.25, 0.0, pick(AMPS))
        z = coin(0.25, 0.0, pick(AMPS))
        ratios.append(r)
        ymix.append(y)
        zmix.append(z)
    p = pulsegen(slot, "Random",
                 freq, ratios, ymix, zmix,
                 ylag = coin(0.75, 0, rnd()),
                 yscale = 1.0, ybias = 0,
                 zlag = coin(0.50, 0, rnd()),
                 zscale = 1.0, zbias = 0)
    return p
                 

pulsegen(0, "ClockWerk 1",
     clockFreq = 2.0000,
     ratios = [0.5000,1.0000,2.0000,0.0625,0.0625,0.0625],
     ymix = [0.6000,1.0000,0.0000,0.0000,0.0000,0.0000],
     zmix = [0.0000,1.0000,1.0000,0.0000,0.0000,0.0000],
     ylag=0.0000, yscale=0.9600, ybias=-0.0800,
     zlag=0.0000, zscale=0.9800, zbias=0.1200)

pulsegen(1, "Chorus 1",
     clockFreq = 7.6000,
     ratios = [8.0000,0.6670,3.0000,1.0000,1.6670,2.5000],
     ymix = [0.2000,0.0000,0.2000,0.9000,0.3000,0.0000],
     zmix = [0.0000,0.2000,0.0000,0.0000,0.4000,0.4000],
     ylag=0.5729, yscale=1.0000, ybias=0.0000,
     zlag=0.7337, zscale=1.0000, zbias=0.0000)

pulsegen(2, "Pattern 2",
     clockFreq = 1.0000,
     ratios = [8.0000,0.6670,1.0000,1.3330,0.2500,1.5000],
     ymix = [0.5000,0.0000,0.1000,0.0000,0.3000,0.7000],
     zmix = [0.0000,1.0000,0.5000,0.7000,0.0000,0.0000],
     ylag=0.0000, yscale=1.0000, ybias=0.0000,
     zlag=0.0000, zscale=2.0000, zbias=0.0000)

pulsegen(3, "Pattern 3",
     clockFreq = 1.1000,
     ratios = [0.5000,1.6670,1.5000,1.3330,2.0000,5.0000],
     ymix = [1.0000,1.0000,1.0000,0.0000,0.0000,0.0000],
     zmix = [0.0000,0.1000,0.0000,1.0000,1.0000,0.3000],
     ylag=0.0000, yscale=1.0000, ybias=0.0000,
     zlag=0.0000, zscale=0.9800, zbias=0.0000)

pulsegen(4, "Pattern 4",
     clockFreq = 1.0000,
     ratios = [1.3330,2.0000,2.5000,1.0000,0.5000,6.0000],
     ymix = [0.0000,0.4000,0.2000,0.0000,0.6000,0.0000],
     zmix = [1.0000,1.0000,0.0000,0.5000,0.2000,0.0000],
     ylag=0.0000, yscale=1.0000, ybias=0.0000,
     zlag=0.0000, zscale=1.0000, zbias=0.0000)

pulsegen(5, "Pattern 5",
     clockFreq = 1.0000,
     ratios = [0.5000,1.0000,1.5000,2.0000,2.5000,3.5000],
     ymix = [1.0000,0.6000,0.4000,0.2000,0.1000,0.2000],
     zmix = [0.2000,0.2000,0.2000,0.3000,0.5000,1.0000],
     ylag=0.0000, yscale=1.0000, ybias=0.0000,
     zlag=0.0000, zscale=0.9800, zbias=0.0000)
