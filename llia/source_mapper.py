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
import llia.util.trace as trace

_DOMAIN_MAP = {"pitchwheel" : constants.PITCHWHEEL_DOMAIN,
               "velocity" : constants.MIDI_7BIT_DOMAIN,
               "aftertouch" : constants.MIDI_7BIT_DOMAIN,
               "keynumber" : constants.MIDI_7BIT_DOMAIN}
for i in range(128):
    k = "cc-%03d" % i
    _DOMAIN_MAP[k] = constants.MIDI_7BIT_DOMAIN
    k = "cc-%d" % i
    _DOMAIN_MAP[k] = constants.MIDI_7BIT_DOMAIN               

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
        self.source = source
        self.domain = domain or _DOMAIN_MAP[source]
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

    # Old style serilization (pre v0.1.3)
    # def serialize(self):
    #     acc = ["llia.SourceMapper",
    #            {"source" : self.source,
    #             "domain" : self.domain,
    #             "map-count" : len(self._maps)}]
    #     for m in self._maps.values():
    #         acc.append(m.serialize())
    #     return acc

    # Old style serilization (pre v0.1.3)
    # @staticmethod
    # def deserialize(obj):
    #     cls = obj[0]
    #     if cls == "llia.SourceMapper":
    #         header = obj[1]
    #         src = header["source"]
    #         dom = header["domain"]
    #         count = header["map-count"]
    #         mapper = SourceMapper(src, dom)
    #         for i in range(count):
    #             pm = obj[i+2][1]
    #             param = pm["parameter"]
    #             crv = pm["curve"]
    #             mod = pm["modifier"]
    #             cod = pm["range_"]
    #             lim = pm["limits"]
    #             mapper.add_parameter(param, crv, mod, cod, lim)
    #         return mapper
    #     else:
    #         msg = "Can not read %s as SourceMapper" % type(obj)
    #         raise RuntimeError(msg)

    # New style serilization (introduced v0.1.3)
    def serialize(self):
        acc = ["llia.SourceMapper",[self.source,self.domain,len(self._maps)]]
        for m in self._maps.values():
            acc.append(m.serialize())
        return acc

    # New style deserilization (introduced v0.1.3)
    @staticmethod
    def deserialize(obj):
        cls = obj[0]
        if cls == "llia.SourceMapper":
            header = obj[1]
            src,dom,count = header
            mapper = SourceMapper(src, dom)
            for i in range(count):
                pm = obj[i+2][1]
                junk,param,crv,mod,junk2,cod,lim = pm
                mapper.add_parameter(param, crv, mod, cod, lim)
            return mapper
        else:
            msg = "Can not read %s as SourceMapper" % type(obj)
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

@hash_.when_type(SourceMapper)
def _hash_sm(obj):
    return crc32(str(obj.serialize()).lower())
