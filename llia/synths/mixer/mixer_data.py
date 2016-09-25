# llia.synths.mixer.mixer_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance
from llia.util.lmath import clip, db_to_amp, amp_to_db

prototype = {
    "gainA" : 1.0,
    "muteA" : 0,     # 0 -> enable, 1 -> mute
    "modA" : 0.0,    # 0 -> no mod, 1 -> 100% modulation
    "panA" : 0.0,
    "gainB" : 1.0,
    "muteB" : 0,
    "modB" : 0.0,
    "panB" : 0.0,
    "gainC" : 1.0,
    "muteC" : 0,
    "modC" : 0.0,
    "panC" : 0.0,
    "gainD" : 1.0,
    "muteD" : 0,
    "modD" : 0.0,
    "panD" : 0.0,
    "gain1" : 1,
    "gain2" : 1}
    


class Mixer(Program):

    def __init__(self, name):
        super(Mixer, self).__init__(name, "Mixer", prototype)
        self.performance = performance()

program_bank = ProgramBank(Mixer("Init"))


def mixer(slot, name,
          chanA = [-99, 0.0, 0.0, 0],      # [gain(db), mod-depth, pan, mute]
          chanB = [-99, 0.0, 0.0, 0],
          chanC = [-99, 0.0, 0.0, 0],
          chanD = [-99, 0.0, 0.0, 0],
          main = [0,0]):
    program=Mixer(name)
    def fill_channel_list(lst):
        acc = []
        for i,dflt in enumerate([-99.0, 0.0, 0.0, 0]):
            try:
                acc.append(float(lst[i]))
            except (IndexError,ValueError,TypeError):
                acc.append(dflt)
        return acc
    def set_channel_params(prefix,chanlist):
        program["gain%s" % prefix] = db_to_amp(chanlist[0])
        program["mod%s" % prefix] = chanlist[1]
        program["pan%s" % prefix] = chanlist[2]
        program["mute%s" % prefix] = chanlist[3]
    set_channel_params("A", fill_channel_list(chanA))
    set_channel_params("B", fill_channel_list(chanB))
    set_channel_params("C", fill_channel_list(chanC))
    set_channel_params("D", fill_channel_list(chanD))
    program["gain1"]=float(db_to_amp(main[0]))
    program["gain2"]=float(db_to_amp(main[1]))
    program_bank[slot] = program
    return program


def pp(program, slot=127):
    return ""
    

mixer(0, "Unity",
      chanA = [0,0,0,0],
      chanB = [0,0,0,0],
      chanC = [0,0,0,0],
      chanD = [0,0,0,0],
      main = [0,0])

mixer(1, "MuteAll",
      chanA = [-99,0,0,1],
      chanB = [-99,0,0,1],
      chanC = [-99,0,0,1],
      chanD = [-99,0,0,1],
      main = [-99,-99])
      
