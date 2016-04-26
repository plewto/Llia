# llia.program
# 2016.03.19

from __future__ import print_function
import json
from zlib import crc32

from llia.generic import is_program, dump, is_list, clone, hash_
from llia.performance import Performance

# "Virtual" parameters begin with underscore _like_this
# and are use to impart additional information.
# A typical use is to break a frequency parameter in to
# coarse and fine components.
#   oscFreq = x
#   _oscFreqCoarse = c
#   _oscFreqFine = f
# Virtual parameters are not transmitted to the synth
# as part of a program change. 

class Program(dict):

    def __init__(self, name, data_format, keyset):
        dict.__init__(self)
        self.name = str(name)
        self.data_format = str(data_format)
        self.keyset = keyset
        self.remarks = ""
        self.performance = Performance()
        self.filename = ""
        self.initialize()

    def initialize(self):
        for p,v in self.keyset.items():
            dict.__setitem__(self, p, v)
        self.performance.initialize()

    def __setitem__(self, param, value):
        if self.keyset.has_key(param):
            dict.__setitem__(self, param, value)

    def add_parameter(self, param, default_value):
        self.keyset[param] = defalut_value
        self[param] = default_value

    @staticmethod
    def is_virtual_param(param):
        return param[0] == "_"
        
    def clone(self):
        other = Program(self.name, self.data_format, self.keyset)
        for p,v in self.items():
            dict.__setitem__(other, p, v)
        other.remarks = self.remarks
        other.performance = self.performance.clone()
        return other

    def copy_program(self, other):
        if is_program(other):
            if other.data_format == self.data_format:
                self.name = other.name
                self.remarks = other.remarks
                for p,v in other.items():
                    self[p] = v
                self.performance.copy_performance(other.performance)
            else:
                msg = "Can not copy %s Program into %s Program"
                msg = msg % (other.data_format, self.data_format)
                raise ValueError(msg)
        else:
            msg = "Can not copy %s into Program"
            msg = msg & type(other)
            raise TypeError(msg)

    def hash_(self):
        return crc32(str(self.serialize()))
        
    def __eq__(self, other):
        if self is other:
            return True
        else:
            return self.hash_() == other.hash_()

    def __ne__(self, other):
        return not self.__eq__(other)

    def extension(self):
        return self.data_format.lower()

    def serialize(self):
        acc = ["llia.Program",
               self.data_format,
               self.name,
               self.remarks,
               len(self)]
        for p in sorted(list(self.keys())):
            if self.keyset.has_key(p):
                v1 = self[p]
                v2 = self.keyset[p]
                acc.append((p,v1,v2))
        bcc = self.performance.serialize()
        return (acc, bcc)

    @staticmethod
    def deserialize(ser):
        if is_list(ser) and len(ser) == 2:
            prg, prf = ser
            id = prg[0]
            if id == "llia.Program":
                frm, name, rem, count = prg[1:5]
                keyset = {}
                program = Program(name, frm, keyset)
                for i in range(5, 5+count):
                    p, v, dflt = prg[i]
                    keyset[p] = dflt
                    program[p] = v
                program.remarks = rem
                program.performance = Performance.deserialize(prf)
                return program
            else:
                msg = "Program.deserialize did not find expected id."
                raise ValueError(msg)
        else:
            msg = "Argument to Program.deserialize must be list or tuple. "
            msg += "Encounters %s" % type(ser)
            raise TypeError(msg)
    
    def save(self, filename):
        with open(filename, 'w') as output:
            s = self.serialize()
            json.dump(s, output, indent=4)
        self.filename = filename

    @staticmethod
    def read_program(filename):
        try:
            with open(filename, 'r') as input:
                obj = json.load(input)
                return Program.deserialize(obj)
        except(ValueError, TypeError, IOError) as err:
            msg = "Error while reading Program file '%s'" % filename
            msg = err.message + "\n" + msg
            raise IOError(msg)
            
    def load(self, filename):
        other = Program.read_program(filename)
        self.copy_program(other)
        self.filename = filename
    
    def __str__(self):
        return "%s Program '%s'" % (self.data_format, self.name)
    
    def dump(self, tab=0, verbosity=1):
        pad = ' '*4*tab
        pad1 = pad+' '*4
        pad2 = pad1+' '*4
        acc = "%sProgram format %s  name '%s'\n" % \
              (pad, self.data_format, self.name)
        if verbosity > 1:
            acc += "%sRemarks:\n" % pad1
            for line in self.remarks.split('\n'):
                acc += "%s%s\n" % (pad2, line)
        if verbosity > 0:
            acc += "%sData:\n" % pad1
            for key in sorted(list(self.keys())):
                if self.keyset.has_key(key):
                    flag = "  "
                else:
                    flag = "* "
                value = self[key]
                acc += "%s[%-12s] = %s\n" % (pad2, key, value)
        acc += self.performance.dump(tab+1, 1)
        return acc
        
@is_program.when_type(Program)
def _is_prog(obj):
    return True
    
@clone.when_type(Program)
def _clone_program(obj):
    return obj.clone()

@dump.when_type(Program)
def _dmp_prog(obj):
    print(obj.dump(0, verbosity=2))

@hash_.when_type(Program)
def _hash_prog(obj):
    return prog.hash_()
    
def test():
    keyset = {"Alpha": 1,
              "Beta" : 2,
              "Gamma" : 3}
    p1 = Program("Test", "Test", keyset)
    p1.remarks = "These are remarks\nAnd so are these."
    dump(p1)

    # Set parameter values
    p1.name = "Primes"
    p1["Alpha"] = 2
    p1["Beta"] = 3
    p1["Gamma"] = 5
    p1["Delta"] = 7  # Ignore, Delta is not a recognized parameter.
    dump(p1)
    
    # Create clone
    print("\nCreate clone")
    p2 = clone(p1)
    dump(p2)

    print("\nequality test")
    print(p1 == p1)
    print(p1 == p2)
    p2["Alpha"] = 13
    print(p1 == p2)

    print("\nextension = '%s'" % p1.extension())
    print("\nSerilization")
    s = p1.serialize()
    p2 = Program.deserialize(s)
    print(p1 == p2, p1 is p2)
    dump(p2)

    print("\nsave and load")
    filename = "/tmp/test_program"
    p1.save(filename)
    p2.initialize()
    p2.load(filename)
    dump(p1)
    dump(p2)
    
   


