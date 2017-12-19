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

    '''
    Program is a dictionary like object which defines a single synth 'patch'
    '''
    
    def __init__(self, name, data_format, keyset):
        '''
        Constructs new Program object.

        ARGS:
          name         - String, the program name.
          data_format  - String, indicates the data format and should be 
                         identical to the synth type ("Orgn", "Saw3", ,,,).
          keyset       - A dictionary of parameter/value pairs used to define 
                         the data format and default values.
        '''
        dict.__init__(self)
        self.name = str(name)
        self.data_format = str(data_format)
        self.keyset = keyset
        self.remarks = ""
        self.performance = Performance()
        self.filename = ""
        self.initialize()


    def diff(self, other):
        '''
        Diagnostic, returns diff of two programs.
        The test program must have the same format as self.
        
        Returns dictionary
            
              {param1 : (v1,v2),
               param2 : (v1,v2),
              ................}

              The dictionary keys are the parameter names (strings) where 
              two programs have different values.  The dictionary values
              are tuples (v1,v2) where v1 and v2 are the values for self
              and the other program respectively.
        '''
        if self.data_format != other.data_format:
            msg = "Can not apply Program.diff to different program types: %s and %s"
            raise TypeError(msg % (self.data_format, other.data_format))
        else:
            acc = {}
            for k in self.keys():
                v1 = self[k]
                v2 =other[k]
                if not v1 == v2:
                    acc[k] = (v1,v2)
            return acc
            
        
    def initialize(self):
        '''
        Set all parameters to default values and initialize the Performance
        values.
        '''
        for p,v in self.keyset.items():
            dict.__setitem__(self, p, v)
        self.performance.initialize()

    def __setitem__(self, param, value):
        '''
        Sets parameter value.
        Ignore if param is not in the keyset established at construction 
        time.
        '''
        if self.keyset.has_key(param):
            dict.__setitem__(self, param, value)

    def add_parameter(self, param, default_value):
        '''
        Add a new parameter to keyset.
        '''
        self.keyset[param] = defalut_value
        self[param] = default_value

    @staticmethod
    def is_virtual_param(param):
        '''
        Predicate test if parameter name is a "virtual" parameter.
        A virtual parameter is one that is saved in the Program but is 
        not an actual synth parameter.  They are used for storing extra
        information about a Program.

        ISSUE: Are virtual parameters actually being used?
        '''
        return param[0] == "_"
        
    def clone(self):
        '''
        Return cloned copy of self.
        '''
        other = Program(self.name, self.data_format, self.keyset)
        for p,v in self.items():
            dict.__setitem__(other, p, v)
        other.remarks = self.remarks
        other.performance = self.performance.clone()
        return other

    def copy_program(self, other):
        '''
        Copy all values of another program into self.

        ARGS:
           other - Program, the source program must have the same 
                   format as self.

        Raises TypeError if other is not a Program.
        Raises ValueError if other is a Program but has the wrong format. 
        '''
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
        return crc32(str(self.__serialize()))
        
    def __eq__(self, other):
        if self is other:
            return True
        else:
            return self.hash_() == other.hash_()

    def __ne__(self, other):
        return not self.__eq__(other)

    def extension(self):
        '''
        Returns filename extension.
        '''
        return self.data_format.lower()

    def serialize(self, params):
        acc = ["llia.Program",
               self.data_format,
               self.name,
               self.remarks,
               len(self)]
        for p in params:
            v = self[p[0]]
            acc.append(v)
        acc.append(self.performance.serialize())
        return acc
  
    # New style deserialize, introduced v0.1.3
    @staticmethod
    def deserialize(s, parameters, prototype):
        id = s[0]
        if id == "llia.Program":
            data_format = s[1]
            name = s[2]
            remarks = s[3]
            count = s[4]
            prog = Program(name, data_format, prototype)
            if count == len(parameters):
                for i,p in enumerate(parameters):
                    param = p[0]
                    value = s[i+5]
                    prog[param] = float(value)
                prog.remarks = remarks
                prog.performance = Performance.deserialize(s[-1])
                return prog
            else:
                msg = "Program.deserialize did not find expected data count: "
                msg += "%s != %s" % (count,len(parameters))
                raise ValueError(msg)
        else:
            msg = "Program.deserialize did not find expected id."
            raise ValueError(msg)
        
    
    def save(self, filename):
        '''
        Save self to file.
        
        ARGS:
           filename - String

        Raise IOError

        '''
        with open(filename, 'w') as output:
            s = self.serialize()
            json.dump(s, output, indent=4)
        self.filename = filename

    @staticmethod
    def read_program(filename):
        '''
        Read Program data from file.

        ARGS:
           filename - String

        RETURNS: 
           Program

        Raises IOError
        '''
        try:
            with open(filename, 'r') as input:
                obj = json.load(input)
                return Program.deserialize(obj)
        except(ValueError, TypeError, IOError) as err:
            msg = "Error while reading Program file '%s'" % filename
            msg = err.message + "\n" + msg
            raise IOError(msg)
            
    def load(self, filename):
        '''
        Read program data from file into self.
        
        ARGS:
           filename - String

        Raises IOError
        '''
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
