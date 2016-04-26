# llia.performance
# 2016.03.19

from __future__ import print_function
import json
from zlib import crc32

from llia.generic import is_performance, dump, clone, is_list, hash_
from llia.source_mapper import SourceMapper, CCMapper

class Performance(object):

    def __init__(self):
        object.__init__(self)
        self.initialize()

    def initialize(self):
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
        if new_range is not None:
            self._key_range = new_range
            self.keynumber_maps.change_domain(self._key_range)
        return self._key_range 
    
    @staticmethod
    def extension():
        return "aprf"

    def serialize(self):
        acc = ["llia.Performance",
               {"transpose" : self.transpose,
                "key_range" : self._key_range,
                "bend_range" : self.bend_range,
                "bend_parameter" : self.bend_parameter,
                "velocity_maps" : self.velocity_maps.serialize(),
                "aftertouch_maps" : self.aftertouch_maps.serialize(),
                "pitchwheel_maps" : self.pitchwheel_maps.serialize(),
                "keynumber_maps" : self.keynumber_maps.serialize(),
                "controller_maps" : self.controller_maps.serialize()}]
        return acc

    @staticmethod
    def deserialize(ser):
        if is_list(ser):
            id = ser[0]
            if id == "llia.Performance":
                other = Performance()
                data = ser[1]
                other.transpose = data["transpose"]
                other._key_range = data["key_range"]
                other.bend_range = data["bend_range"]
                other.bend_parameter = data["bend_parameter"]
                other.velocity_maps = SourceMapper.deserialize(data["velocity_maps"])
                other.aftertouch_maps = SourceMapper.deserialize(data["aftertouch_maps"])
                other.pitchwheel_maps = SourceMapper.deserialize(data["pitchwheel_maps"])
                other.keynumber_maps = SourceMapper.deserialize(data["keynumber_maps"])
                other.controller_maps = CCMapper.deserialize(data["controller_maps"])
                return other
            else:
                msg = "Performance.deserialize did not find expected id."
                raise ValueError(msg)
        else:
            msg = "Argument to Performance.deserialize must be a list or "
            msg = msg + "tuple,  encountered %s" % type(ser)
            raise TypeError(msg)
                
    def save(self, filename):
        with open(filename, 'w') as output:
            s = self.serialize()
            json.dump(s, output, indent=4)
        
    def load(self, filename):   # ISSUE: Performance.load not implemented
        pass

    def dump(self, tab=0, verbosity=0):
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

#  ---------------------------------------------------------------------- 
#                                    Test

def test():
    p1 = Performance()
    dump(p1)

    p1.velocity_maps.add_parameter("filterFreq", "exp", codomain=(1000, 9999))
    p1.velocity_maps.add_parameter("volume", "exp")
    p1.controller_maps.add_parameter(1, "vibrato")
    p1.controller_maps.add_parameter(4, "attack")
    dump(p1)

    p2 = clone(p1)
    dump(p2)
    print("p1 == p2", p1 == p2, "  p1 is p2", p1 is p2)

    print("\n*** serilization ***")
    s = p1.serialize()
    p3 = Performance.deserialize(s)
    dump(p3)
    print("p1 == p3", p1 == p3, "  p1 is p3", p1 is p3)
