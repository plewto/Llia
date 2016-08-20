# llia.synths.mixer.mixer_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance
from llia.util.lmath import clip, db_to_amp, amp_to_db

prototype = {
    "gain1" : 1.0,             # Channel 1 gain (linear)
    "pan1" : 0.0,              # Channel 1 pan -1 <= pan <= +1
    "reverb1" : 0.0,           # channel 1 reverb send (0..1)
    "gain2" : 1.0,
    "pan2" : 0.0,
    "reverb2" : 0.0,
    "gain3" : 1.0,
    "pan3" : 0.0,
    "reverb3" : 0.0,
    "gain4" : 1.0,
    "pan4" : 0.0,
    "reverb4" : 0.0,
    "reverbReturn" : 0.0,      # Reverb return gain 
    "reverbRoomSize" : 0.25,   # Room size 0 <= size <= 1
    "reverbLowpass" : 16000,   # Hertz
    "reverbHighpass" : 40,     # Hertz
    "reverbDamp" : 0.0,        # Reverb high frequency damping 0 <= damp <= 1
    "reverbBalance" : 0.0,    # left/right balance  -1 <= balance <= +1
    
    "mainAmpA" : 1.0,          # Main out gain 1 
    "mainAmpB" : 1.0           # Main out gain 2
}

class Mixer(Program):

    def __init__(self, name):
        super(Mixer, self).__init__(name, "Mixer", prototype)
        self.performance = performance()

program_bank = ProgramBank(Mixer("Init"))

def mixer(slot, name,
          chan1 = [-99, 0.00, 0.00], # [gain (db), pan, reverb]
          chan2 = [-99, 0.00, 0.00],
          chan3 = [-99, 0.00, 0.00],
          chan4 = [-99, 0.00, 0.00],
          reverb = {"size" : 0.50,
                    "damp" : 0.00,
                    "lowpass" : 20000,
                    "highpass" : 10,
                    "balance" : 0.0,
                    "return" : -99}, #  return in db
          main = [  0,   0]):       # [out-1 out-2] (db)

    program = Mixer(name)
    def fill_channel_list(lst):
        acc = []
        template = (-99, 0.0, 0.0)
        for i,dflt in enumerate(template):
            try:
                v = acc[i]
            except IndexError:
                v = dflt
            if i == 0:
                v = float(db_to_amp(v))
            else:
                v = float(clip(v,0,1))
            acc.append(v)
        return acc

    def fill_main_list(lst):
        acc = []
        template = (0, 0)
        for i,dflt in enumerate(template):
            try:
                v = lst[i]
            except IndexError:
                v = dflt
            acc.append(float(db_to_amp(v)))
        return acc

    def fill_reverb_dict(d):
        rs = {"size" : float(clip(d.get("size", 0.5), 0.0, 1.0)),
              "damp" : float(clip(d.get("damp", 0.0), 0.0, 1.0)),
              "lowpass" : int(clip(d.get("lowpass", 20000), 10, 20000)),
              "highpass" : int(clip(d.get("highpass", 10), 10, 20000)),
              "balance" : float(clip(d.get("balance", 0.0), -1, 1)),
              "return" : float(db_to_amp(d.get("return", -99)))}
        return rs
    
    chan1 = fill_channel_list(chan1)
    chan2 = fill_channel_list(chan2)
    chan3 = fill_channel_list(chan3)
    chan4 = fill_channel_list(chan4)
    main = fill_main_list(main)
    reverb = fill_reverb_dict(reverb)
    for i, clst in enumerate((chan1, chan2, chan3, chan4)):
        for j,p in enumerate(("gain","pan","reverb")):
            param = "p%d" % (i+1,)
            value = clst[j]
            program[param] = value
    program["mainAmpA"] = main[0]
    program["mainAmpB"] = main[1]
    for p,q in (("size","reverbRoomSize"),
                ("damp","reverbDamp"),
                ("lowpass","reverbLowpass"),
                ("highpass","reverbHighpass"),
                ("balance","reverbBalance"),
                ("return","reverbReturn")):
        program[q] = reverb[p]
    program_bank[slot] = program
    return program
    

def pp(program, slot=127):
    pad = ' '*5
    pad2 = pad + ' '*10
    acc = 'mixer(%d, "%s", \n' % (slot, program.name)
    for c in "1234":
        acc += '%schan%s = [' % (pad,c)
        p = "gain%s" % c
        db = int(amp_to_db(program['gain%s' % c]))
        pan = float(program['pan%s' % c])
        rev = float(program['reverb%s' % c])
        acc += '%+3d, %4.2f, %4.2f],\n' % (db, pan, rev)
    values = (pad, float(program["reverbRoomSize"]))
    acc += '%sreverb = {"size" : %4.2f,\n' % values
    values = (pad2, float(program["reverbDamp"]))
    acc += '%s"damp" : %4.2f,\n' % values
    values = (pad2, int(program["reverbLowpass"]))
    acc += '%s"lowpass"  : %5d,\n' % values
    values = (pad2, int(program["reverbHighpass"]))
    acc += '%s"highpass" : %5d,\n' % values
    values = (pad2, float(program["reverbBalance"]))
    acc += '%s"balance" : %4.2f,\n' % values
    values = (pad2, int(amp_to_db(program["reverbReturn"])))
    acc += '%s"return"   : %+3d},\n' % values
    values = (pad,
              int(amp_to_db(program["mainAmpA"])),
              int(amp_to_db(program["mainAmpB"])))
    acc += '%smain = [%+3d, %+3d])\n' % values
    return acc



mixer(0, "Unity",
      chan1 = [  0, 0.00, 0.00],
      chan2 = [  0, 0.00, 0.00],
      chan3 = [  0, 0.00, 0.00],
      chan4 = [  0, 0.00, 0.00],
      reverb = {"size" : 0.50,
                "damp" : 0.50,
                "lowpass"  : 20000,
                "highpass" :    40,
                "balnace"  : 0.0,
                "return"   : -99},
      main = [0, 0])

mixer(1, "All OFF",
      chan1 = [  0, 0.00, 0.00],
      chan2 = [  0, 0.00, 0.00],
      chan3 = [  0, 0.00, 0.00],
      chan4 = [  0, 0.00, 0.00],
      reverb = {"size" : 0.50,
                "damp" : 0.50,
                "lowpass"  : 20000,
                "highpass" :    40,
                "balance"  : 0.0,
                "return"   : -99},
      main = [-99, -99])
