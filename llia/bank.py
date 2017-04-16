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

    '''
    ProgramBank provides storage of 128 synth programs for immediate
    recall, either manually or via MIDI program change.
    '''

    clipboard = {}
    
    def __init__(self, template):
        '''
        Constructs new ProgramBank instance.
        ARGS:
           template - dict holding with synth parameter keys and default
                      values.
        '''
        list.__init__(self)
        self.template = template
        for i in range(BANK_LENGTH):
            list.append(self, clone(template))
        # List parameters/default-values in order
        # [(p1, dflt1),(p2,dflt2)...]
        self._parameters = []
        for p in sorted(template.keys()):
            self._parameters.append((p,template[p]))
        self.current_slot = 0
        self.current_program = self[0]
        self.name = "%s Bank" % template.data_format
        self.remarks = ""
        self.filename = ""
        self.undostack = UndoRedoStack()
        self.enable_undo = True
        self.lock_current_program = False # if true ignore program changes

    def append(self, _):
        msg = "Can not append to ProgramBank"
        raise NotImplementedError(msg)
        
    def extension(self):
        '''
        Returns filename extension.
        '''
        return self.template.data_format.lower()

    def push_undo(self, action):
        '''
        Pushes the current state of the bank to the undo stack.
        The undo feature is not being used at this point.
        '''
        if self.enable_undo:
            self.undostack.push_undo(action, clone(self))

    def undo(self):
        '''
        Restore state of self from undo stack.
        The undo feature is not currently being used.
        '''
        try:
            obj = self.undostack.pop_undo()
            self.undostack.push_redo(obj.action, clone(self))
            self.copy_bank(obj.payload)
        except IndexError:
            msg = "Nothing to undo"
            raise IndexError(msg)

    def redo(self):
        '''
        Redo the previous undo.
        Redo is not currently being used.
        '''
        try:
            obj = self.undostack.pop_redo()
            self.undostack.push_undo(obj.action, clone(self))
            self.copy_bank(obj.payload)
        except IndexError:
            msg = "Nothing to redo"
            raise IndexError(msg)

    def __getitem__(self, slot):
        '''
        Returns indicated Program

        ARGS:
          slot - int MIDI program number, 0 <= slot < 128.
                 If slot is None, the 'current' slot is used.

        RETURNS: Program

        Raises IndexError
        '''
        if slot is None:
            return self.current_program
        else:
            return clone(list.__getitem__(self, slot))

    def __setitem__(self, slot, obj):
        '''
        Sets indicated program slot.
        
        ARGS:
          slot - int MIDI program number, 0 <= slot < 128.
                 If slot is None, the 'current' slot is used.
          obj  - an instance of Program.

        Raises TypeError if obj is not a Program.
        Raises ValueError if obj is a Program but has the wrong format.
        '''
        slot = slot or self.current_slot
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
        '''
        Mark slot as the 'current' slot, ignore if self.lock_current_program
        is True.
        
        ARGS:
          slot - int, MIDI program number, 0 <= slot < 1
          undo_action - optional Sting sets undo message text.

        RETURNS:
          int - the current program slot.
        '''
        if not self.lock_current_program:
            if not undo_action:
                undo_action = "Recall slot %d" % self.current_slot
            self.push_undo(undo_action)
            self.current_slot = slot
            self.current_program = clone(self[slot])
        return self.current_program
        
    def copy_to_clipboard(self, slot=None):
        '''
        Copy program to clipboard.  The clipboard is global and may 
        contain multiple programs at once but will only store a 
        a single Program of any one type.
        
        ARGS:
          slot - optional int, MIDI program number, the source slot
                 If not specified, the current slot is used.
        '''
        prog = self[slot]
        frmt = self.template.data_format
        ProgramBank.clipboard[frmt] = prog

    def paste_clipboard(self, slot=None):
        '''
        Paste contents of clipboard into the bank.

        ARGS:
         slot - optional MIDI program number. If not specified
                the current slot is used.
         
        Raises KeyError if the clipboard does not contain an
        appropriate Program.
        '''
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
        '''
        Copies contents of bank into self.

        ARGS:
          other - The source bank

        Raises TypeError if other is not a ProgramBank.
        Raises ValueError if other is a ProgramBank but has the wrong format.
        '''
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
                #self.performance.copy_erformance(other.performance)
            else:
                msg = "Can not copy %s bank into %s bank"
                msg = msg % (frmt2, frmt1)
                raise ValueError(msg)
        else:
            msg = "Can not copy %s to ProgramBank"
            msg = msg % type(other)
            raise TypeError(msg)

    def create_program(self):
        '''
        Creates a new Program based using the template passed to self at
        construction time.   The Program is not contained in the bank.

        RETURNS: Program
        '''
        df = self.template.data_format
        ks = self.template.keyset
        prog = Program("Init", df, ks)
        return prog
    
    def initialize_slot(self, slot=None):
        '''
        Creates a new initialized program an stores it in the bank.

        ARGS:
          slot - optional MIDI program number,the location to store
                 the program.  If not specified use the current slot.
        '''
        p = self.create_program()
        self.push_undo("Initialize slot [%s]" % slot)
        if slot == None:
            self.current_program = p
        else:
            list.__setitem__(self, slot, p)

    def initialize_slot_range(self, start, end=None):
        '''
        Initialize a range of bank slots .
        
        ARGS:
          start - MIDI program number
          end   - optional MIDI program number. If not 
                  specified end = start+1
        '''
        end = end or start + 1
        self.push_undo("Initialize slot range")
        for i in range(slot, end):
            list.__setitem__(self, i, self.create_program())

    def initialize(self):
        '''
        Initialize the bank by filling it with default programs.
        '''
        self.push_undo("Initialize Bank")
        for i in range(len(self)):
            list.__setitem__(self, i, self.create_program())
        self.name = "Init"
        self.remarks = ""
        self.current_slot = 0
        self.current_program = clone(self[0])

    def clone(self):
        '''
        Returns an exact copy of self.
        '''
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
    
 
    def save(self, filename):
        '''
        Save bank contents to file.
        
        ARGS:
          filename

        Raises IOError
        '''
        s = self.serialize()
        with open(filename, 'w') as output:
            json.dump(s, output, indent=4)
        self.filename = filename

    # Old style serialization (prior t v0.1.3)
    # def serialize(self):
    #     '''
    #     Convert bank to serial data preparatory to saving it.
    #     '''
    #     acc = ["Llia.ProgramBank",
    #            {"format" : self.template.data_format,
    #             "name" : self.name,
    #             "remarks" : self.remarks,
    #             "count" : len(self),
    #             "template" : self.template.serialize()}]
    #     payload = []
    #     for p in self:
    #         payload.append(p.serialize())
    #     acc.append(payload)
    #     return acc

    # Old style deserilization (prior to v0.1.3)
    # @staticmethod
    # def deserialize(s):
    #     '''
    #     Convert serialized data to an instance of Bank.  deserialize
    #     is used as part of the bank read operation.
    #     ARGS:
    #       s - List, 
    #
    #     RETURNS: 
    #       ProgramBank
    #
    #     Raise TypeError if s is not a list
    #     Raises ValueError if s does not have the proper format.
    #     Raises IndexError if s is too short.
    #     '''
    #     try:
    #         if is_list(s):
    #             id = s[0]
    #             if id == "Llia.ProgramBank":
    #                 header, payload = s[1:3]
    #                 count = header["count"]
    #                 template = Program.deserialize(header["template"])
    #                 bank = ProgramBank(template)
    #                 for slot in range(count):
    #                     ps = payload[slot]
    #                     list.__setitem__(bank, slot, Program.deserialize(ps))
    #                 bank.use(0)
    #                 bank.name = header["name"]
    #                 bank.remarks = header["remarks"]
    #                 bank.undostack.clear()
    #                 return bank
    #             else:
    #                 msg = "ProgramBank.deserialize did not find expected class id"
    #                 raise ValueError(msg)
    #         else:
    #             msg = "ProgramBank.deserialize, wrong type: %s" % type(s)
    #             raise TypeError(msg)
    #     except IndexError:
    #         msg = "ProgramBank.deserialize, IndexError"
    #         raise IndexError(msg)

    def serialize(self):
        payload = []
        previous = Program("Dummy","",{})
        pid = previous.hash_()
        for slot, prog in enumerate(self):
            cid =prog.hash_()
            if cid == pid:
                payload.append("X")
            else:
                previous = prog
                pid = previous.hash_()
                payload.append(prog.serialize(self._parameters))
        acc = ["Llia.ProgramBank",
               {"format" : self.template.data_format,
                "name" : self.name,
                "remarks" : self.remarks,
                "count" : len(self),
                "parameters" : self._parameters,
                "data" : payload}]
        return acc
                

    # New style deserilization
    # ui - User interface
    #      ui should implement update_progressbar(count, value)
    #      where count is maximum number and value is current value.
    @staticmethod
    def deserialize(s, ui=None):
        try:
            id = s[0]
            if id == "Llia.ProgramBank":
                count = s[1]["count"]
                name = s[1]["name"]
                data_format = s[1]["format"]
                remarks = s[1]["remarks"]
                parameters = s[1]["parameters"]
                prototype = {}
                for a,b in parameters:
                    prototype[a] = b
                data = s[1]["data"]
                template_program = Program("Init",data_format,prototype)
                bank = ProgramBank(template_program)
                previous = template_program
                for slot in range(count):
                    if ui: ui.update_progressbar(count, slot)
                    prog_data = data[slot]
                    if prog_data == "X":
                        bank[slot] = previous
                    else:
                        program = Program.deserialize(prog_data,parameters,prototype)
                        bank[slot] = program
                        previous = program
                return bank
            else:
                msg = "ProgramBank.deserilize did not find exptected class id"
                raise ValueError(msg)
        except IndexError:
            msg = "ProgramBank.deserialize IndexError"
            raise IndexError(msg)
            
            
    # See deserialize for ui usage
    @staticmethod
    def read_bank(filename, ui=None):
        '''
        Read bank file.
        
        ARGS:
           filename - String

        RETURNS:
          ProgramBank

        Raises IOError
        '''
        try:
            with open(filename, 'r') as input:
                obj = json.load(input)
                rs = ProgramBank.deserialize(obj, ui)
                return rs
        except(ValueError, TypeError, IOError) as err:
            msg = "Error while reading ProgramBank file '%s'" % filename
            msg = err.message + "\n" + msg
            raise IOError(msg)

    # See deserialize for ui usage.
    def load(self, filename, ui=None):
        '''
        Load bank data from file into self.

        ARGS:
          filename - String

        Raises IOError
        '''
        try:
            self.push_undo("Load bank file '%s'" % filename)
            other = ProgramBank.read_bank(filename, ui)
            self.copy_bank(other)
            self.current_slot = 0
            self.current_program = clone(self[0])
            self.filename = filename
        except(ValueError, TypeError, IOError) as err:
            self.undostack.pop_undo()
            msg = "Error while reading ProgramBank file '%s'" % filename
            raise IOError(msg)

    def copy_performance(self, slot=None):
        '''
        Copy performance portion of program to clipboard.

        ARGS:
          slot - optional MIDI program number.  If not specified use
                 current slot.
        '''
        ProgramBank.clipboard["Performance"] = self[slot].performance
        
    def paste_performance(self):
        '''
        Paste clipboard contents into performance portion of program.
        
        ARGS:
          slot - optional MIDI program number.  If not specified use
                 current slot.

        Raises KeyError if clipboard does not contain performance data.
        '''
        try:
            self[None].performance = ProgramBank.clipboard["Performance"]
        except KeyError:
            msg = "Bank clipboard does not contain Performance."
            raise KeyError(msg)

    # Copy clipboard performance to all program slots
    # in range(start, end)
    def fill_performance(self, start, end):
        '''
        Fill range of program slots with identical performance data from 
        clipboard.

        ARGS:
          start - int MIDI program number.
          end   - int MIDI program number, 0 <= start < end < 128.

        Raises KeyError if clipboard does not contain performance.
        '''
        try:
            p = ProgramBank.clipboard["Performance"]
            for i in range(start,end):
                program = self[i]
                program.performance = p
                self[i] = program
        except KeyError:
            msg = "Bank clipboard does not contain Performance."
            raise KeyError(msg)
        
    def dump(self, tab=0, verbosity=1):
        '''
        Produce diagnostic dump.

        RETURNS:  String
        '''
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
