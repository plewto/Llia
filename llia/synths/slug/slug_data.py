# llia.synths.Slug.Slug_data

from __future__ import print_function
from llia.program import Program
from llia.bank import ProgramBank
from llia.performance_edit import performance

prototype = {
    # FIXME
}

class Slug(Program):

    def __init__(self,name):
        super(Slug,self).__init__(name,Slug,prototype)
        self.performance = performance()

program_bank = ProgramBank(Slug("Init"))
def slug(slot, name,
     ):
    p = Slug(name)
    # FIXME
    program_bank[slot] = p
    return p

slug(0,"Init")
