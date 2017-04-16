# llia.performance
# 2016.03.19

from __future__ import print_function
import json
from zlib import crc32

from llia.generic import is_performance, dump, clone, is_list, hash_
from llia.source_mapper import SourceMapper
from llia.ccmapper import CCMapper

class Performance(object):

    '''
    A Performance defines parameters common to all Synth programs. 
    Performance parameters include:
      1) Transpose in MIDI key numbers
      2) Active key range as key number pair
      3) Pitch bend depth in cents.
      4) Velocity mapping functions.
      5) Aftertouch mapping functions.
      6) Pitch wheel mapping functions (separate from simply pitch bend).
      7) Kynumber mapping functions.
      8) MIDI controller mapping functions.
    There may be an arbitrary number of functions for each mapping source.
    Velocity for example may map to filter cutoff and overall amplitude, or
    any number of other parameters, simultaneously.
    '''
    
    def __init__(self):
        '''
        Construct new Performance object.
        '''
        object.__init__(self)
        self.initialize()

    def initialize(self):
        '''
        Sets all values to defaults.
        All mapping functions are removed.
        '''
        self.transpose = 0
        self._key_range = (0, 127)
        self.bend_range = 200
        self.bend_parameter = "detune"
        self.velocity_maps = SourceMapper("velocity")
        self.aftertouch_maps = SourceMapper("aftertouch")
        self.pitchwheel_maps = SourceMapper("pitchwheel")
        self.keynumber_maps = SourceMapper("keynumber")
        self.controller_maps = CCMapper()

    def clone(self):
        '''
        Returns a cloned copy of self.
        '''
        other = Performance()
        other.transpose = self.transpose
        other._key_range = self._key_range
        other.bend_range = self.bend_range
        other.bend_parameter = self.bend_parameter
        other.velocity_maps = clone(self.velocity_maps)
        other.aftertouch_maps = clone(self.aftertouch_maps)
        other.pitchwheel_maps = clone(self.pitchwheel_maps)
        other.keynumber_maps = clone(self.keynumber_maps)
        other.controller_maps = clone(self.controller_maps)
        return other

    def copy_performance(self, other):
        '''
        Copy all values from another Performance into self.

        ARGS:
          other - Performance, the source object.
        '''
        self.transpose = other.transpose
        self._key_range = other._key_range
        self.bend_range = other.bend_range
        self.bend_parameter = other.bend_parameter
        self.velocity_maps = clone(other.velocity_maps)
        self.aftertouch_maps = clone(other.aftertouch_maps)
        self.pitchwheel_maps = clone(other.pitchwheel_maps)
        self.keynumber_maps = clone(other.keynumber_maps)
        self.controller_maps = clone(other.controller_maps)
        
    def hash_(self):
        return crc32(str(self.serialize()))
        
    def __eq__(self, other):
        if self is other:
            return True
        else:
            return self.hash_() == other.hash_()

    def __ne__(self, other):
        return not self.__eq__(other)

    def key_range(self, new_range=None):
        '''
        Retrieve/change key range.

        ARGS:
          new_range - optional tuple (low, high).
                      If specified update the current key range.
                      
        RETURNS:
             tuple (low, high) where low and high are MIDI keynumbers
             0 <= low < high < 128. 
             Reception of keynumbers outside this range are ignored.
        '''
        if new_range is not None:
            self._key_range = new_range
            self.keynumber_maps.change_domain(self._key_range)
        return self._key_range 
    
    @staticmethod
    def extension():
        '''
        Returns filename extension for saving Performance data.
        '''
        return "aprf"

    # Old style serilizatin (prior to v0.1.3)
    # def serialize(self):
    #     '''
    #     Convert self to serialized form.
    #     Returns List
    #     '''
    #     acc = ["llia.Performance",
    #            {"transpose" : self.transpose,
    #             "key_range" : self._key_range,
    #             "bend_range" : self.bend_range,
    #             "bend_parameter" : self.bend_parameter,
    #             "velocity_maps" : self.velocity_maps.serialize(),
    #             "aftertouch_maps" : self.aftertouch_maps.serialize(),
    #             "pitchwheel_maps" : self.pitchwheel_maps.serialize(),
    #             "keynumber_maps" : self.keynumber_maps.serialize(),
    #             "controller_maps" : self.controller_maps.serialize()}]
    #     return acc

    # Old style deserilization (prior to v0.1.3)
    # @staticmethod
    # def deserialize(ser):
    #     '''
    #     Convert serial form back to Performance
    #
    #     ARGS:
    #       ser - list, must have the same format as produced by serialize
    #
    #     RETURNS:
    #       Performance
    #     '''
    #     if is_list(ser):
    #         id = ser[0]
    #         if id == "llia.Performance":
    #             other = Performance()
    #             data = ser[1]
    #             other.transpose = data["transpose"]
    #             other._key_range = data["key_range"]
    #             other.bend_range = data["bend_range"]
    #             other.bend_parameter = data["bend_parameter"]
    #             other.velocity_maps = SourceMapper.deserialize(data["velocity_maps"])
    #             other.aftertouch_maps = SourceMapper.deserialize(data["aftertouch_maps"])
    #             other.pitchwheel_maps = SourceMapper.deserialize(data["pitchwheel_maps"])
    #             other.keynumber_maps = SourceMapper.deserialize(data["keynumber_maps"])
    #             other.controller_maps = CCMapper.deserialize(data["controller_maps"])
    #             return other
    #         else:
    #             msg = "Performance.deserialize did not find expected id."
    #             raise ValueError(msg)
    #     else:
    #         msg = "Argument to Performance.deserialize must be a list or "
    #         msg = msg + "tuple,  encountered %s" % type(ser)
    #         raise TypeError(msg)


    # New style serilizatin introduced v0.1.3
    def serialize(self):
        '''
        Convert self to serialized form.
        Returns List
        '''
        acc = ["llia.Performance", [self.transpose,
                                    self._key_range,
                                    self.bend_range,
                                    self.bend_parameter,
                                    self.velocity_maps.serialize(),
                                    self.aftertouch_maps.serialize(),
                                    self.pitchwheel_maps.serialize(),
                                    self.keynumber_maps.serialize(),
                                    self.controller_maps.serialize()]]
        return acc

    # New style deserilization introduced v0.1.3
    @staticmethod
    def deserialize(ser):
        '''
        Convert serial form back to Performance
    
        ARGS:
          ser - list, must have the same format as produced by serialize
    
        RETURNS:
          Performance
        '''
        if is_list(ser):
            id = ser[0]
            if id == "llia.Performance":
                other = Performance()
                data = ser[1]
                other.transpose = data[0]
                other._key_range = data[1]
                other.bend_range = data[2]
                other.bend_parameter = data[3]
                other.velocity_maps = SourceMapper.deserialize(data[4])
                other.aftertouch_maps = SourceMapper.deserialize(data[5])
                other.pitchwheel_maps = SourceMapper.deserialize(data[6])
                other.keynumber_maps = SourceMapper.deserialize(data[7])
                other.controller_maps = CCMapper.deserialize(data[8])
                return other
            else:
                msg = "Performance.deserialize did not find expected id."
                raise ValueError(msg)
        else:
            msg = "Argument to Performance.deserialize must be a list or "
            msg = msg + "tuple,  encountered %s" % type(ser)
            raise TypeError(msg)
                
    def save(self, filename):
        '''
        Save self to file.
        
        ARGS:
          filename - String

        Raises: IOError
        '''
        with open(filename, 'w') as output:
            s = self.serialize()
            json.dump(s, output, indent=4)
        
    def load(self, filename):   # ISSUE: Performance.load not implemented
        '''
        Load performance from file.
        ISSUE Performance load is not implemented!
        '''
        pass

    def dump(self, tab=0, verbosity=1):
        '''
        Produce diagnostic data.

        ARGS:
          tab  - optional int, sets indentation depth 
          verbosity - optional int, higher values produce more detail

        RETURNS:
            String
        '''
        pad = ' '*4*tab
        pad1 = pad+' '*4
        pad2 = pad1+' '*4
        acc = "%sPerformance:\n" % pad
        if verbosity > 0:
            acc += "%stranspose %s\n" % (pad1, self.transpose)
            acc += "%skey range %s\n" % (pad1, self.key_range())
            acc += "%sbend range %s,  parameter '%s'\n" % \
                   (pad1, self.bend_range, self.bend_parameter)
            tab2 = tab+1
            acc += self.velocity_maps.dump(tab2)
            acc += self.aftertouch_maps.dump(tab2)
            acc += self.pitchwheel_maps.dump(tab2)
            acc += self.keynumber_maps.dump(tab2)
            acc += self.controller_maps.dump(tab2)
        return acc

@is_performance.when_type(Performance)
def _is_perf(obj):
    return True

@dump.when_type(Performance)
def _dump_perf(obj, tab=0, verbosity=1):
    print(obj.dump(tab, verbosity))

@clone.when_type(Performance)
def _clone_perf(obj):
    return obj.clone()

@hash_.when_type(Performance)
def _hash_perf(obj):
    return obj.hash_()
