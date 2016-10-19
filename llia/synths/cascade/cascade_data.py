# llia.synths.cascade.cascade_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance
from llia.util.lmath import coin, rnd, pick

prototype = {
    "clkfreq" : 1.000,          # float 0..?
    "clksrc" : 0,               # int, 0=internal, 1=external
    "hold" : 1.0,               # float, ?..?
    "n" : 8,                    # int, 7..32
    "amp1" : 1.00,              # float, 0..1
    "amp2" : 0.00,
    "amp3" : 0.00,
    "amp4" : 0.00,
    "amp5" : 0.00,
    "amp6" : 0.00,
    "ampn" : 0.00,
    "gate1" : 0,                # int, 0=not gated, 1=gated
    "gate2" : 0,
    "gate3" : 0,
    "gate4" : 0,
    "gate5" : 0,
    "gate6" : 0,
    "gaten" : 0,
    "scale" : 1.0,              # float, 0..1
    "bias" : 0,                 # float -4..+4
    "lag" : 0.0}                # float 0..1

class Cascade(Program):

    def __init__(self, name):
        super(Cascade, self).__init__(name, "Cascade", prototype)
        self.performance = performance()

program_bank = ProgramBank(Cascade("Init"))
program_bank.enable_undo = False

def _fill_amp_list(lst):
    template = [1.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
    acc = []
    for i,dflt in enumerate(template):
        try:
            acc.append(float(lst[i]))
        except IndexError:
            acc.append(dflt)
    return acc

def _bool(obj):
    if obj:
        return 1
    else:
        return 0

def _fill_gate_list(lst):
    template = [0]*7
    acc = []
    for i,dflt in enumerate(template):
        try:
            a = _bool(lst[i])
            acc.append(a)
        except IndexError:
            acc.append(dflt)
    return acc

def cascade(slot, name,
            clkfreq = 1.00,
            clkselect = 0,
            hold = 1.00,
            n = 8,
            amp = [1.00,0.00,0.00,0.00,0.00,0.00,0.00],
            gate = [0,0,0,0,0,0,0],
            scale = 1.0,
            bias = 0.0,
            lag = 0.0):
    p = Cascade(name)
    p["clkfreq"] = float(max(0,clkfreq))
    p["clksrc"] = _bool(clkselect)
    p["hold"] = float(max(0,hold))
    p["n"] = int(max(min(n,99),1))
    amp = _fill_amp_list(amp)
    gate = _fill_gate_list(gate)
    for i,a in enumerate(amp):
        j = i+1
        g = gate[i]
        aparam = "amp%d" % j
        gparam = "gate%d" % j
        p[aparam] = a
        p[gparam] = g
    p["scale"] = float(max(0, scale))
    p["bias"] = float(max(min(bias,4),-4))
    p["lag"] = float(max(min(lag,1),0))
    program_bank[slot] = p
    return p

def pp(program, slot=127):

    def fval(key):
        return float(program[key])

    def ival(key):
        return int(program[key])
    
    def bool(key):
        q = program[key]
        return _bool(q)
    pad = ' '*8
    acc = 'cascade(%d,"%s",\n' % (slot, program.name)
    acc += '%sclkfreq = %5.3f,\n' % (pad,fval('clkfreq'))
    acc += '%sclksrc = %d,\n' % (pad,ival('clksrc'))
    acc += '%shold = %5.3f,\n' % (pad,fval('hold'))
    acc += '%sn = %d,\n' % (pad,ival('hold'))
    bcc = '%samp = [' % pad
    gcc = '%sgate = [' % pad
    for i in range(6):
        j = i+1
        a = fval("amp%d" % j)
        g = bool("gate%d" % j)
        bcc += "%5.3f," % a
        gcc += "%d," % g
    bcc += '%5.3f],\n' % fval("ampn")
    gcc += '%d],\n' % bool("gaten")
    acc += bcc
    acc += gcc
    acc += '%sscale = %5.3f,\n' % (pad, fval("scale"))
    acc += '%sbias = %5.3f,\n' % (pad, fval("bias"))
    acc += '%slag = %5.3f)\n' % (pad, fval('lag'))
    return acc
            

def random_cascade(slot=127, *_):
    return None


cascade(0,"Test")
cascade(1,"Calibrate",
        amp=[0.9, 0.8, 0.7, 0.6,
             0.4, 0.3, 0.2, 0.1])
