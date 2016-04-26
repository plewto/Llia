# llia.test.bank_test
# 2016.04.22

from __future__ import print_function

import llia.constants
llia.constants.BANK_LENGTH = 4   # FOR TESTING ONLY

from llia.generic import dump
from llia.program import Program
from llia.bank import ProgramBank

prototype = {"Alpha" : 0.00,
             "Beta" : 0.33,
             "Gamma" : 0.67,
             "Delta" : 1.00}

template = Program("Template", "Greek", prototype)


def test1():
    print("Test1  Create ProgramBank and dump programs.")
    bnk = ProgramBank(template)
    dump(bnk)

def test2():
    print("Test2 Select current program, modify it and stor back to bank.")
    bnk = ProgramBank(template)
    bnk.use(2)
    prog = bnk[None]
    prog.name = "Primes"
    prog["Alpha"] = 2
    prog["Beta"] = 3
    prog["Gamma"] = 5
    prog["Delta"] = 7
    bnk[2] = prog
    bnk.remarks = "Slot number 2 changed to 'primes'"
    dump(bnk)
    print("slot[2] is prog ? --> %s" % (bnk[2] is prog))
    print("slot[2] == prog ? --> %s" % (bnk[2] == prog))

def test3():
    print("Test3 serialize/deserilize/clone test")
    bnk1 = ProgramBank(template)
    bnk1.name = "Source bnk1"
    bnk1.remarks = "These are bnk1 remarks"
    prog = bnk1[2]
    prog.name = "Primes"
    prog["Alpha"] = 2
    prog["Beta"] = 3
    prog["Gamma"] = 5
    prog["Delta"] = 7
    bnk1[2] = prog
    s = bnk1.serialize()
    bnk2 = ProgramBank.deserialize(s)
    dump(bnk2)
    print("bnk1 is bnk2 --> %s" % (bnk1 is bnk2, ))
    print("bnk1 == bnk2 --> %s" % (bnk1 == bnk2, ))

def test4():
    print("Bank clipboard functions")
    bnk1 = ProgramBank(template)
    bnk1.name = "Source bnk1"
    bnk1.remarks = "These are bnk1 remarks"
    prog = bnk1[2]
    prog.name = "Primes"
    prog["Alpha"] = 2
    prog["Beta"] = 3
    prog["Gamma"] = 5
    prog["Delta"] = 7
    bnk1[0] = prog
    bnk1.use(0)
    bnk1.copy_to_clipboard()  # Copies current to clipboard
    bnk2 = ProgramBank(template)
    bnk2.paste_clipboard()
    prog1 = bnk2[None]
    dump(prog1)
    print("prog == prog1 --> %s" % (prog == prog1, ))


test4()
    
    


llia.constants.BANK_LENGTH = 127   # FOR TESTING ONLY
