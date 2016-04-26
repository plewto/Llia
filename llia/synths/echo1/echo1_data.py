# llia.synths.echo1.echo1_data
# 2016.04.26

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank


prototype = {"delayTime" : 0.50,
             "feedback" : 0.75,
             "efxmix" : 0.0}

class Echo1(Program):

    def __init__(self, name):
        super(Echo1, self).__init__(name, "Echo1", prototype)

INIT_PROGRAM = Echo1("Init")        
program_bank = ProgramBank(INIT_PROGRAM)
program_bank.enable_undo = False
