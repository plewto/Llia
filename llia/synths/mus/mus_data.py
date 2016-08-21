# llia.synths.snh.snh_data

from __future__ import print_function
from fractions import Fraction

from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance
from llia.util.lmath import coin, rnd, pick

prototype = {
  	"xmin" : 0.0,
	"xmax" : 1.0,
	"xcurve" : 0,    # 0 -> linear   1 -> exponential
	"xlag" : 0.2,
	"ymin" : 0.0,
	"ymax" : 1.0,
	"ycurve" : 0,
	"ylag" : 0.2,
	"buttonOff" : 0.0,
	"buttonOn" : 1.0,
	"attack" : 0.0,
	"decay" : 0.0,
	"sustain" : 1.0,
	"release" : 1.0,
	"envScale" : 1.0,
	"envBias" : 0.0
}

class Mus(Program):

    def __init__(self, name):
        super(Mus, self).__init__(name, "SNH", prototype)
        self.performance = performance()

program_bank = ProgramBank(Mus("Init"))
program_bank.enable_undo = False

def mus(slot, name,
        x = [0.0, 1.0, "lin", 0.2],  # [min, max, curve, lag]
        y = [0.0, 1.0, "lin", 0.2],
        button = [0.0, 1.0],
        adsr = [0.0, 0.1, 1.0, 0.0, 1.0, 0.0]): # [A, D, S, R, scale, bias]
    def fill(lst, template):
        bcc = []
        for i,dflt in enumerate(template):
            try:
                v = lst[i]
            except INdexError:
                v = dflt
            if v == 'lin':
                v = 0
            elif v == 'exp':
                v = 1
            bcc.append(float(v))
        return bcc
    x = fill(x, [0.0, 1.0, "lin", 0.2])
    y = fill(y, [0.0, 1.0, "lin", 0.2])
    button = fill(button, [0.0, 1.0])
    adsr = fill(adsr, [0.0, 0.1, 1.0, 1.0, 1.0, 0.0])
    p = Mus(name)
    p["xmin"] = x[0]
    p["xmax"] = x[1]
    p["xcurve"] = x[2]
    p["xlag"] = x[3]
    p["ymin"] = y[0]
    p["ymax"] = y[1]
    p["ycurve"] = y[2]
    p["ylag"] = y[3]
    p["buttonOff"] = button[0]
    p["buttonOn"] = button[1]
    p["attack"] = adsr[0]
    p["decay"] = adsr[1]
    p["sustain"] = adsr[2]
    p["release"] = adsr[3]
    p["envScale"] = adsr[4]
    p["envBias"] = adsr[5]
    program_bank[slot] = p
    return p

def pp(program, slot=127):
    def fval(key):
        v = program[key]
        return float(program[key])
    pad = ' '*5
    acc = 'mus(%d, "%s",\n' % (slot, program.name);
    xcurve = fval('xcurve')
    if xcurve:
        xcurve == "exp"
    else:
        xcurve == "lin"
    values = (pad, fval('xmin'), fval('xmax'), xcurve, fval('xlag'))
    acc += '%sx = [%5.3f, %5.3f, "%s", %5.3f],\n' % values
    ycurve = fval('ycurve')
    if ycurve:
        ycurve == "exp"
    else:
        ycurve == "lin"
    values = (pad, fval('ymin'), fval('ymax'), ycurve, fval('ylag'))
    acc += '%sy = [%5.3f, %5.3f, "%s", %5.3f],\n' % values
    values = (pad, fval('buttonOff'), fval('buttonOn'))
    acc += '%sbutton = [%5.3f, %5.3f],\n' % values
    values = (pad, fval('attack'), fval('decay'), fval('sustain'),
              fval('release'), fval('envScale'), fval('envBias'))
    acc += '%sadsr = [%5.3f, %5.3f, %5.3f, %5.3f, %5.3f, %5.3f])\n' % values
    return acc

def random_mus(*_):
    return None
