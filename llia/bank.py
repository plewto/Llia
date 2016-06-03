# llia.bank
# 2016.04.21

from __future__ import print_function
import json
from zlib import crc32

from llia.generic import clone, dump, name, is_bank, is_program, is_list, hash_
from llia.constants import BANK_LENGTH
from llia.program import Program
from llia.util.undostack import UndoRedoStack

class ProgramBank(list):

    clipboard = {}
    
    def __init__(self, template):
        list.__init__(self)
        self.template = template
        for i in range(BANK_LENGTH):
            list.append(self, clone(template))
        self.current_slot = 0
        self.current_program = self[0]
        self.name = "%s Bank" % template.data_format
        self.remarks = ""
        self.filename = ""
        self.undostack = UndoRedoStack()
        self.enable_undo = True

    def append(self, _):
        msg = "Can not append to ProgramBank"
        raise NotImplementedError(msg)
        
    def extension(self):
        return self.template.data_format.lower()

    def push_undo(self, action):
        if self.enable_undo:
            self.undostack.push_undo(action, clone(self))

    def undo(self):
        try:
            obj = self.undostack.pop_undo()
            self.undostack.push_redo(obj.action, clone(self))
            self.copy_bank(obj.payload)
        except IndexError:
            msg = "Nothing to undo"
            raise IndexError(msg)

    def redo(self):
        try:
            obj = self.undostack.pop_redo()
            self.undostack.push_undo(obj.action, clone(self))
            self.copy_bank(obj.payload)
        except IndexError:
            msg = "Nothing to redo"
            raise IndexError(msg)

    def __getitem__(self, slot):
        if slot is None:
            return self.current_program
        else:
            return clone(list.__getitem__(self, slot))

    def __setitem__(self, slot, obj):
        if is_program(obj):
            if obj.data_format == self.template.data_format:
                self.push_undo("Store slot [%d] <-- '%s'" % (slot, obj.name))
                list.__setitem__(self, slot, clone(obj))
            else:
                msg = "Can not store %s program into %s bank"
                msg = msg % (obj.data_format, self.template.data_format)
                raise ValueError(msg)
        else:
            msg = "Can not store %s into ProgramBank"
            msg = msg % type(obj)
            raise TypeError(msg)

    def hash_(self):
        return crc32(str(self.serialize()).lower())
    
    def __eq__(self, other):
        if other is self:
            return True
        else:
            return hash_(self) == hash_(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        s = "%s ProgramBank name %s"
        return s % (self.template.data_format, self.name)
        
    def use(self, slot, undo_action=None):
        if not undo_action:
            undo_action = "Recall slot %d" % self.current_slot
        self.push_undo(undo_action)
        self.current_slot = slot
        self.current_program = clone(self[slot])
        return self.current_program
        
    def copy_to_clipboard(self, slot=None):
        prog = self[slot]
        frmt = self.template.data_format
        ProgramBank.clipboard[frmt] = prog

    def paste_clipboard(self, slot=None):
        frmt = self.template.data_format
        try:
            prog = clone(ProgramBank.clipboard[frmt])
            self.push_undo("Paste")
            if slot is None:
                self.current_program = prog
            else:
                list.__setitem__(self, slot, prog)
        except KeyError:
            msg = "ProgramBank clipboard does not contain %s Program"
            msg = msg % frmt
            raise KeyError(msg)

    def copy_bank(self, other):
        # DOES NOT SAVE UNDO STATE
        if is_bank(other):
            frmt1 = self.template.data_format
            frmt2 = other.template.data_format
            if frmt1 == frmt2:
                self.name = other.name
                self.remarks = other.remarks
                for i in range(min(len(self), len(other))):
                    p = list.__getitem__(other, i)
                    list.__setitem__(self, i, clone(p))
                self.current_slot = other.current_slot
                self.current_program = clone(other.current_program)
                #self.performance.copy_performance(other.performance)
            else:
                msg = "Can not copy %s bank into %s bank"
                msg = msg % (frmt2, frmt1)
                raise ValueError(msg)
        else:
            msg = "Can not copy %s to ProgramBank"
            msg = msg % type(other)
            raise TypeError(msg)

    def create_program(self):
        df = self.template.data_format
        ks = self.template.keyset
        prog = Program("Init", df, ks)
        return prog
    
    def initialize_slot(self, slot=None):
        p = self.create_program()
        self.push_undo("Initialize slot [%s]" % slot)
        if slot == None:
            self.current_program = p
        else:
            list.__setitem__(self, slot, p)

    def initialize_slot_range(self, start, end=None):
        end = end or start + 1
        self.push_undo("Initialize slot range")
        for i in range(slot, end):
            list.__setitem__(self, i, self.create_program())

    def initialize(self):
        self.push_undo("Initialize Bank")
        for i in range(len(self)):
            list.__setitem__(self, i, self.create_program())
        self.name = "Init"
        self.remarks = ""
        self.current_slot = 0
        self.current_program = clone(self[0])

    def clone(self):
        other = ProgramBank(self.template)
        other.name = self.name
        other.remarks = self.remarks
        other.current_slot = self.current_slot
        other.current_program = clone(self.current_program)
        for slot, prog in enumerate(self):
            prog2 = clone(prog)
            list.__setitem__(other, slot, prog2)
        other.undostack.clear()
        return other
    
    def serialize(self):
        acc = ["Llia.ProgramBank",
               {"format" : self.template.data_format,
                "name" : self.name,
                "remarks" : self.remarks,
                "count" : len(self),
                "template" : self.template.serialize()}]
        payload = []
        for p in self:
            payload.append(p.serialize())
        acc.append(payload)
        return acc

    def save(self, filename):
        s = self.serialize()
        with open(filename, 'w') as output:
            json.dump(s, output, indent=4)
        self.filename = filename

    @staticmethod
    def deserialize(s):
        try:
            if is_list(s):
                id = s[0]
                if id == "Llia.ProgramBank":
                    header, payload = s[1:3]
                    count = header["count"]
                    template = Program.deserialize(header["template"])
                    bank = ProgramBank(template)
                    for slot in range(count):
                        ps = payload[slot]
                        list.__setitem__(bank, slot, Program.deserialize(ps))
                    bank.use(0)
                    bank.name = header["name"]
                    bank.remarks = header["remarks"]
                    bank.undostack.clear()
                    return bank
                else:
                    msg = "ProgramBank.deserialize did not find expected class id"
                    raise ValueError(msg)
            else:
                msg = "ProgramBank.deserialize, wrong type: %s" % type(s)
                raise TypeError(msg)
        except IndexError:
            msg = "ProgramBank.deserialize, IndexError"
            raise IndexError(msg)

    @staticmethod
    def read_bank(filename):
        try:
            with open(filename, 'r') as input:
                obj = json.load(input)
                return ProgramBank.deserialize(obj)
        except(ValueError, TypeError, IOError) as err:
            msg = "Error while reading ProgramBank file '%s'" % filename
            msg = err.message + "\n" + msg
            raise IOError(msg)

    def load(self, filename):
        try:
            self.push_undo("Load bank file '%s'" % filename)
            other = ProgramBank.read_bank(filename)
            self.copy_bank(other)
            self.current_slot = 0
            self.current_program = clone(self[0])
            self.filename = filename
        except(ValueError, TypeError, IOError) as err:
            self.undostack.pop_undo()
            msg = "Error while reading ProgramBank file '%s'" % filename
            raise IOError(msg)
        

    def dump(self, tab=0, verbosity=1):
        pad = " "*4*tab
        pad2 = pad + " "*4
        pad3 = pad2 + " "*4
        acc = "%sProgramBank:\n" %  pad
        acc += "%sFormat: '%s'\n" % (pad2, self.template.data_format)
        acc += "%sName: '%s'\n" % (pad2, self.name)
        acc += "%sFilename: '%s'\n" % (pad2, self.filename)
        acc += "%sCurrent_slot: %s\n" % (pad2, self.current_slot)
        if verbosity > 0:
            acc += "%sParameters:\n" % pad2
            line = "%s" % pad3
            for k in sorted(self.template.keyset.keys()):
                line += "%s " % k
                if len(line) > 60:
                    acc += line + "\n"
                    line = "%s" % pad3
            acc += line + "\n"
            acc += "%sRemarks:\n" % pad2
            for line in self.remarks.split("\n"):
                acc += "%s%s\n" % (pad3, line)
        if verbosity > 1:
            for slot, p in enumerate(self):
                acc += "%s[%3d] --------------------------------\n" % (pad2, slot)
                acc += p.dump(tab+1)
        return acc
                
            
        
@clone.when_type(ProgramBank)
def _clone_bnk(bnk):
    return bnk.clone()

@dump.when_type(ProgramBank)
def _dump_bank(bnk, tab=0, verbosity=2):
    print(bnk.dump(tab, verbosity))

@is_bank.when_type(ProgramBank)
def _is_bank(bnk):
    return True

@hash_.when_type(ProgramBank)
def _hash_bank(bnk):
    return bnk.hash_()
