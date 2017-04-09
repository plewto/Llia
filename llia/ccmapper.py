# llia.ccmapper
# 2016.02.21

from __future__ import print_function
from zlib import crc32

from llia.generic import is_source_mapper, is_cc_mapper, dump, clone, hash_
import llia.constants as constants
from llia.parameter_map import ParameterMap
from llia.source_mapper import SourceMapper

class CCMapper(object):

    """
    Maps MIDI controller to any number of synth parameters.
    CCMapper is essentially an sparse array of SourceMapper objects.
    """
    
    def __init__(self):
        """Constructs new CCMapper object"""
        self.domain = constants.MIDI_7BIT_DOMAIN
        self._maps = None
        self.reset()

    def __len__(self):
        return len(self._maps)

    def __eq__(self, other):
        return hash_(self) == hash_(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def clone(self):
        other = CCMapper()
        for cc,sm in self._maps.items():
            other._maps[cc] = clone(sm)
        return other
    
    def reset(self):
        """Removes all parameter maps"""
        self._maps = {}

    def remove_parameter(self, ctrl, param="ALL"):
        """
        Removes parameter maps for single controller.
        
        ARGS:
          ctrl  - MIDI controller number 
          param - Optional String, parameter.  If not specified or has the 
                  value "ALL" then all parameter maps for ctrl are removed.
        """
        try:
            maps = self._maps[ctrl]
            maps.remove_parameter(param)
            if len(maps) == 0:
                del self._maps[ctrl]
        except KeyError:
            pass

    def add_parameter(self, ctrl, param, curve=None, modifier=None,
                      range_=None, limits=None):
        """
        Adds controller parameter map.
        
        ARGS:
          ctrl     - MIDI controller number
          param    - String, synth parameter
          curve    - Optional String, may be one of "linear", "exp", "s"
                     or "step".  Defaults to "linear"
          modifier - Optional float, curve modification coefficient.
                     See llia.curves
          range_ - Optional tuple, parameter range_.
                     Default (0.0, 1.0)
          limits   - Optional tuple clipping limits, defaults to range_.
        """
        maps = None
        try:
            maps = self._maps[ctrl]
        except KeyError:
            source_name = "cc-%s" % ctrl
            maps = SourceMapper(source_name)
            self._maps[ctrl] = maps
        maps.add_parameter(param, curve, modifier, range_, limits)

    def __call__(self, ctrl, param, curve=None, modifier=None,
                 range_=None, limits=None):
        self.add_parameter(ctrl, param, curve, modifier, range_, limits)
        
    def __len__(self):
        return len(self._maps)

    def keys(self):
        """
        Returns list of MIDI controller numbers which have active
        parameter maps.
        """
        klst = list(self._maps.keys())
        klst.sort()
        return klst

    def items(self):
        """
        Returns nested list of controller number SourceMapper objects
        ((ctrl1 mapper1), (crtl2, mapper2) ...)
        """
        acc = []
        for k in self.keys():
            ccmap = self._maps[k]
            acc.append((k, ccmap))
        return acc

    def __getitem__(self, ctrl):
        """Returns SourceMapper for controller ctrl"""
        return self._maps[ctrl]

    def update_synths(self, ctrl, x, instrument):
        """
        Updates synth parameters in response to controller change.
        
        ARGS:
          ctrl - MIDI controller number.
          x    - int, controller position (0,1,2,...127).
          instrument - an instance of Instrument.
        """
        try:
            self[ctrl].update_synths(x, instrument)
        except KeyError:
            pass
            
    def copy_ccmapper(self, other):
        self.reset()
        for ctrl,pm in other._maps.items():
            self._maps[ctrl] = clone(pm)
        return None
        
    def dump(self, tab=0):
        pad = ' '*4*tab
        pad2 = pad+' '*4
        acc = "%sCCMapper domain %s\n" % (pad, self.domain)
        for k,pm in self.items():
            acc += pm.dump(tab+1)
        return acc

    def __str__(self):
        if len(self) == 0:
            return "# No MIDI controller maps"
        else:
            acc = ""
            for k,pm in self.items():
                acc += "%s\n" % pm
            return acc

    # Old style serilizatin (prior to v0.1.3)
    # def serialize(self):
    #     count = len(self._maps)
    #     acc = ["llia.CCMapper",
    #            {"domain" : self.domain,
    #             "count" : count}]
    #     maps = {}
    #     for k,v in self._maps.items():
    #         maps[k] = v.serialize()
    #     acc.append(maps)
    #     return acc

    # Old style deserilization (prior to v0.1.3)
    # @staticmethod
    # def deserialize(obj):
    #     cls = obj[0]
    #     if cls == "llia.CCMapper":
    #         maps = obj[2]
    #         ccm = CCMapper()
    #         for ctrl, v in maps.items():
    #             sm = SourceMapper.deserialize(v)
    #             ccm._maps[ctrl] = sm
    #         return ccm
    #     else:
    #         msg = "Can not read %s as CCMapper" % type(obj)
    #         raise RuntimeError(msg)

    # New style serialization (introduced v0.1.3)
    def serialize(self):
        count = len(self._maps)
        acc = ["llia.CCMapper", [self.domain,count]]
        maps = {}
        for k,v in self._maps.items():
            maps[k] = v.serialize()
        acc.append(maps)
        return acc

    # New style deserilization (introduced v0.1.3 - no change over v.0.1.3)
    @staticmethod
    def deserialize(obj):
        cls = obj[0]
        if cls == "llia.CCMapper":
            maps = obj[2]
            ccm = CCMapper()
            for ctrl, v in maps.items():
                sm = SourceMapper.deserialize(v)
                ccm._maps[ctrl] = sm
            return ccm
        else:
            msg = "Can not read %s as CCMapper" % type(obj)
            raise RuntimeError(msg)
        
@is_cc_mapper.when_type(CCMapper)
def _is_cc_mapper(obj):
    return True

@dump.when_type(CCMapper)
def _dump_ccm(obj, tab=0, verbosity=None):
    print(obj.dump(tab))

@clone.when_type(CCMapper)
def _clone_ccm(obj):
    return obj.clone()

@hash_.when_type(CCMapper)
def _hash_ccm(obj):
    return crc32(str(obj.serialize()).lower())
