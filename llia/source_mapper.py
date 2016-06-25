# llia.source_mapper
# 2016.02.21
# Maps single source signal (velocity, aftertouch, etc...) to any number
# of synth parameters.
# See also parameter_map.

from __future__ import print_function
from zlib import crc32

from llia.generic import is_source_mapper, is_cc_mapper, dump, clone, hash_
import llia.constants as constants
from llia.parameter_map import ParameterMap

class SourceMapper(object):

    """
    Maps single source signal to any number of synth parameters.
    """

    def __init__(self, source, domain=None):
        """
        Constructs new SourceMapper object.
        
        ARGS:
          source - String, the source signal. Valid options are "velocity",
                   "aftertouch", "pitchwheel", "keynumber" or "cc-xxx".
                   Where cc-xxx is for MIDI controller xxx.
          domain - Optional tuple (a,b) sets expected value range of source 
                   signal.  Unless specified domain defaults to (0,127) for
                   velocity, aftertouch, keynumber, and MIDI controller. 
                   For pitchwheel domain defaults to (-8192, 8191).
        """
        self.source = str(source).lower()
        # self._transient = self.source in ("keynumber","aftertouch",
        #                                   "velocity","pitchwheel")
        if domain:
            self.domain = domain
        else:
            if source == "pitchwheel":
                self.domain = constants.PITCHWHEEL_DOMAIN
            else:
                self.domain = constants.MIDI_7BIT_DOMAIN
        self._maps = {}

    def __len__(self):
        return len(self._maps)
    
    def __eq__(self, other):
        return hash_(self) == hash_(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def clone(self):
        other = SourceMapper(self.source, self.domain[:])
        for p,m in self._maps.items():
            other._maps[p] = clone(m)
        return other
    
    def reset(self):
        """Remove all mapped parameters"""
        self._maps = {}
        
    def change_domain(self, new_domain):
        """
        Change domain of source signal.  
        Change domain is primarily used for keynumber source so that the 
        full range of values is spread across the current key range.

        ARGS:
          new_domain - tuple (a,b)
        """
        self.domain=new_domain
        for pm in self._maps.values():
            pm.change_domain(new_domain)
      
    def remove_parameter(self, param="ALL"):
        """
        Remove synth parameter.

        ARGS:
          param - Optional string. If specified only the matching parameter 
                  map is removed.  The default of "ALL" removes all parameter
                  maps for this source.
        """
        if str(param).upper() == "ALL":
            self.reset()
        else:
            try:
                del self._maps[param]
            except KeyError:
                pass
            
    def add_parameter(self, param, curve=None, modifier=None,
                      range_=None, limits=None):
        """
        Adds parameter map.
        
        ARGS:
          param    - String
          curve    - Optional String, one of "linear", "exp", "s" or "step".
                     Default "linear"
          modifier - Optional float, curve modification coefficient.
                     See llia.curves.
          range_ - Optional tuple sets range of parameter values.
                     Default (0.0, 1.0)
          limits   - Optional clipping limits, defaults to range_.
        """
        self.remove_parameter(param)
        pm = ParameterMap(self.source, param, curve, modifier, 
                          self.domain, range_, limits)
        self._maps[param] = pm

    def __call__(self, param, curve=None, modifier=None,
                 range_=None, limits=None):
        self.add_parameter(param, curve, modifier, range_, limits)
        
    def __len__(self):
        """Returns number of mapped parameters"""
        return len(self._maps)

    def keys(self):
        """Returns list of mapped parameter names"""
        klst = list(self._maps.keys())
        klst.sort()
        return klst

    def items(self):
        """
        Returns nested list of parameter name and ParameterMap objects.
        ((param1, map1),(param2, map2) ...)
        """
        acc = []
        for k in self.keys():
            pm = self._maps[k]
            acc.append((k,pm))
        return acc

    def __getitem__(self, param):
        """Return ParameterMap for given parameter"""
        return self._maps[param]

    def update_synths(self, x, instrument):
        """
        Update all mapped parameters for new source value.
       
        ARGS:
          x - int, The source value
          instrument - An instance of Instrument
        """
        active_update = instrument.app.config.active_updates_enabled()
        for pm in self._maps.values():
            value = pm.map_value(x)
            param = pm.parameter
            instrument.x_param_change(param, value)
            if active_update: # and not self._transient:
                sed = instrument.synth_editor
                if sed:
                    sed.set_aspect(param, value)
    
    def dump(self, tab=0):
        pad = ' '*4*tab
        pad2 = pad+' '*4
        acc = "%sSourceMapper %s domain %s\n" % \
              (pad, self.source, self.domain)
        for k,pm in self.items():
            acc += "%s%s\n" % (pad2, pm)
        return acc

    def serialize(self):
        acc = ["llia.SourceMapper",
               {"source" : self.source,
                "domain" : self.domain,
                "map-count" : len(self._maps)}]
        for m in self._maps.values():
            acc.append(m.serialize())
        return acc

    def copy_source_mapper(self, other):
        self.source = other.source
        self.domain = other.domain
        self._maps = {}
        for m in other._maps.values():
            p = m.parameter
            self._maps[p] = clone(m)
    
    def __str__(self):
        if len(self) == 0:
            return "# No mapped values for %s" % self.source
        else:
            acc = ""
            for k,pm in self.items():
                acc += "%s\n" % pm
        return acc

    @staticmethod
    def deserialize(obj):
        cls = obj[0]
        if cls == "llia.SourceMapper":
            header = obj[1]
            src = header["source"]
            dom = header["domain"]
            count = header["map-count"]
            mapper = SourceMapper(src, dom)
            for i in range(count):
                pm = obj[i+2][1]
                param = pm["parameter"]
                crv = pm["curve"]
                mod = pm["modifier"]
                cod = pm["range_"]
                lim = pm["limits"]
                mapper.add_parameter(param, crv, mod, cod, lim)
            return mapper
        else:
            msg = "Can not read %s as SourceMapper" % type(obj)
            raise RuntimeError(msg)
            
#  ---------------------------------------------------------------------- 
#                               CCMapper class
    
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
        
    def serialize(self):
        count = len(self._maps)
        acc = ["llia.CCMapper",
               {"domain" : self.domain,
                "count" : count}]
        maps = {}
        for k,v in self._maps.items():
            maps[k] = v.serialize()
        acc.append(maps)
        return acc
        
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
            
        
@is_source_mapper.when_type(SourceMapper)
def _is_source_mapper(obj):
    return True

@dump.when_type(SourceMapper)
def _dump_sm(obj, tab=0, verbosity=None):
    print(obj.dump(tab))

@clone.when_type(SourceMapper)
def _clone_sm(obj):
    return obj.clone()

@is_cc_mapper.when_type(CCMapper)
def _is_cc_mapper(obj):
    return True

@dump.when_type(CCMapper)
def _dump_ccm(obj, tab=0, verbosity=None):
    print(obj.dump(tab))

@clone.when_type(CCMapper)
def _clone_ccm(obj):
    return obj.clone()

@hash_.when_type(SourceMapper)
def _hash_sm(obj):
    return crc32(str(obj.serialize()).lower())

@hash_.when_type(CCMapper)
def _hash_ccm(obj):
    return crc32(str(obj.serialize()).lower())


#  ---------------------------------------------------------------------- 
#                                    Test

def test_source_mapper():
    print("*** SourceMapper test ***")
    sm1 = SourceMapper("velocity")
    sm1.add_parameter("A")
    sm1.add_parameter("B", curve="exp", modifier=2, range_=(100, 200))
    sm1.add_parameter("C")
    dump(sm1)
    print("len  : ", len(sm1))
    print("keys : ", sm1.keys())
    print("sm1['B'] --> ", sm1["B"])

    print("\n*** Serilization, eq and clone ***")
    s = sm1.serialize()
    sm2 = SourceMapper.deserialize(s)
    dump(sm2)
    print("sm1 == sm2", sm1 == sm2, "   sm1 is sm2", sm1 is sm2)
    sm3 = clone(sm1)
    dump(sm3)

    print("\n*** Remove parameters ***")
    sm1.remove_parameter("C")
    dump(sm1)
    sm2.remove_parameter("ALL")
    dump(sm2)

def test_cc_mapper():
    print("*** CCMapper test ***")
    a = CCMapper()
    a.add_parameter(1, "vibrato")
    a.add_parameter(4, "volume")
    a.add_parameter(4, "filter", "exp", range_=(100, 10000))
    a.add_parameter(4, "filterRes")
    dump(a)

    print("\n*** Serialization, clone and eq ***")
    s = a.serialize()
    b = CCMapper.deserialize(s)
    c = clone(a)
    dump(b)
    dump(c)
    print("a == b", a == b, "  a is b", a is b)
    print("a == c", a == c, "  a is c", a is c)

    print("\n*** Remove parameters ***")
    b.remove_parameter(4, "filter")
    dump(b)
    b.remove_parameter(4)
    dump(b)
    c.reset()
    dump(c)


def test_clone():
    a = SourceMapper("velocity")
    a.add_parameter("vibrato")
    b = clone(a)
    dump(a)
    dump(b)
    print(a is b)
    c = CCMapper()
    c.add_parameter(1, "vibrato")
    d = clone(c)
    dump(c)
    dump(d)
    print(c is d)
