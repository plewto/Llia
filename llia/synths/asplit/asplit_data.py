# llia.synths.asplit.asplit_data

from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance
from llia.util.lmath import (clip, db_to_amp, amp_to_db)

prototype = {
    "gainA" : 1.0,
    "gainB" : 1.0,
    "gainC" : 1.0,
    "gainD" : 1.0,
    "gain"  : 1.0,
    "unmuteA" : 1,  # 0 -> mute  1 -> unmute
    "unmuteB" : 1,
    "unmuteC" : 1,
    "unmuteD" : 1,
    "unmute"  : 1}
    

class ASplit(Program):

    def __init__(self, name):
        super(ASplit, self).__init__(name, "ASplit", prototype)
        self.performance = performance()

program_bank = ProgramBank(ASplit("Init"))

def asplit(slot, name,
           gainA=0, gainB=0, gainC=0, gainD=0, gain=0,
           unmuteA=1, unmuteB=1, unmuteC=1, unmuteD=1, unmute=1):
    p = ASplit(name)
    p["gainA"] = float(db_to_amp(gainA))
    p["gainB"] = float(db_to_amp(gainB))
    p["gainC"] = float(db_to_amp(gainC)) 
    p["gainD"] = float(db_to_amp(gainD))
    p['gain'] = float(db_to_amp(gain))
    p['unmuteA'] = int(unmuteA)
    p['unmuteB'] = int(unmuteB)
    p['unmuteC'] = int(unmuteC)
    p['unmuteD'] = int(unmuteD)
    p['unmute'] = int(unmute)
    program_bank[slot] = p
    return p

def pp(program, slot=1276):
    pad = ' '*5
    acc = 'asplit(%d, "%s",\n' % (slot, program.name)
    for b in 'ABCD':
        if b == ' ': b = ''
        param = 'gain%s' % b
        db = int(amp_to_db(program[param]))
        acc += '%s%s = %+3d, ' % (pad, param, db)
        param = 'unmute%s' % b
        v = int(program[param])
        acc += '%s = %d,\n' % (param, v)
    db = int(amp_to_db(program["gain"]))
    acc += '%sgain  = %+3d, ' % (pad, db)
    v = int(program["unmute"])
    acc += 'unmute  = %d)\n' % v
    return acc


asplit(0, "All Off",
       gainA = -99, unmuteA = 0,
       gainB = -99, unmuteB = 0,
       gainC = -99, unmuteC = 0,
       gainD = -99, unmuteD = 0,
       gain  = -99, unmute  = 0)

asplit(1, "All On",
       gainA = 0, unmuteA = 1,
       gainB = 0, unmuteB = 1,
       gainC = 0, unmuteC = 1,
       gainD = 0, unmuteD = 1,
       gain  = 0, unmute = 1)
