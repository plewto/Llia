# llia.parameter_map
# 2016.03.19
#
# Defines classes for mapping source signals, such as velocity,
# MIDI controller, aftertouch etc to synth parameters.
# See llia.source_mapper

from __future__ import print_function
from zlib import crc32

from llia.generic import is_parameter_map, clone, hash_ 
import llia.curves as curves
import llia.constants as constants

# sources:  pitchwheel
#           controller  "cc-xxx"
#           aftertouch
#           velocity
#           keynumber

class ParameterMap(object):

    """
    ParameterMap maps a source signal to a single synth parameter.
    """
    def __init__(self, source, parameter,
                 curve=None, curve_modifier=None,
                 domain=None, range_=None, limits=None):
        """
        Constructs new instance of ParameterMap.
        
        ARGS:
          source    - String, the source signal should be one of the following
                      "pitchwheel", "aftertouch", "velocity", "keynumber" or
                      "cc-xxx".  Where cc-xxx is MIDI controller number xxx.
          parameter - String, the synth parameter.
          curve     - Optional String, mapping curve selection, should be 
                      one of "linear", "exp", "s" or "step", default "linear"
          curve_modifier - Optional float, see llia.curves.
          domain    - Optional tuple (a,b), the expected source signal values.
                      For most sources the domain is (0,127), for pitchwheel
                      the domain is (-8192, 8191).
          range_  - Optional tuple (q,r), the mapped parameter range. 
                      map(source=a) --> q,  map(source=b) -->r.  For r < q, 
                      the curve slope is inverted. Default (0.0, 1.0).
          limits    - Optional tuple set hard limits on parameter value. 
                      Limits may be used to modify the shape of the mapping 
                      curve. Defaults to value of range_.
        """
        self.source = str(source).lower()
        self.parameter = parameter
        self.curve_type = curve or "linear"
        self.curve_modifier = curve_modifier or \
                              curves.default_modifier_value(self.curve_type)
        if domain:
            self.domain = domain
        else:
            if source == "pitchwheel":
                self.domain = constants.PITCHWHEEL_DOMAIN
            else:
                self.domain = constants.MIDI_7BIT_DOMAIN
        if range_:
            self.range_ = range_
        else:
            if source == "pitchwheel":
                self.range_ = constants.BIPOLAR_RANGE
            else:
                self.range_ = constants.NORMAL_RANGE
        self.limits = limits or self.range_
        self.curve_fn = curves.curve(self.curve_type, self.domain,
                                        self.range_, self.curve_modifier,
                                        self.limits)

    def change_domain(self, new_domain):
        """
        Change the domain of the source signal.
        ARGS:
          new_domain - tuple (a,b)
        """
        self.domain = new_domain
        self.curve_fn = curves.curve(self.curve_type, self.domain,
                                        self.range_, self.curve_modifier,
                                        self.limits)

    def __cmp__(self, other):
        """
        Compare two ParameterMap.
        A combination of the map source and parameter are used for comparison.
        """
        a = self.source + self.parameter
        b = other.source + other.parameter
        if a < b:
            return -1
        elif a == b:
            return 0
        else:
            return 1
        
    def source_is_midi_cc(self):
        """Returns True if source is a MIDI controller"""
        return self.source[:3] == "cc-"

    def get_source_midi_cc_number(self):
        """
        Extract controller number if source is a MIDI controller.
        If source is not a MIDI controller returns None.
        RETURNS:
          int or None
        """
        try:
            if self.source_is_midi_cc():
                ctrl = int(self.source[3:])
                return ctrl
            else:
                return None
        except ValueError:
            return None

    def map_value(self, x):
        """
        Map source signal to parameter.

        ARGS:
          x - int, the source signal.
         
        RETURNS:
          float
        """
        y = self.curve_fn(x)
        return y

    def serialize(self):
        acc = ["llia.ParameterMap",
               {"source" : self.source,
                "parameter" : self.parameter,
                "curve" : self.curve_type,
                "modifier" : self.curve_modifier,
                "domain" : self.domain,
                "range_" : self.range_,
                "limits" : self.limits}]
        return acc
    
    def __eq__(self, other):
        return is_parameter_map(other) and hash_(self) == hash_(other)
                     
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def clone(self):
        other = ParameterMap(self.source, self.parameter)
        other.curve_type = self.curve_type
        other.domain = self.domain
        other.range_ = self.range_
        other.limits = self.limits
        other.curve_fn = self.curve_fn
        return other
    
    def copy_parameter_map(self, other):
        self.source = other.source
        self.parameter = other.parameter
        self.curve_type = other.curve_type
        self.curve_modifier = other.curve_modifier
        self.domain = other.domain
        self.range_ = other.range_
        self.limits = other.limits
        self.curve_fn = other.curve_fn
        return None
    
    def __str_common(self):
        acc = "--> %-12s %-6s mod %+5.2f %s clip to %s"
        acc = acc % (self.parameter, self.curve_type, float(self.curve_modifier),
                     self.range_, self.limits)
        return acc
 
    def __str__(self):
        src = "%s " % self.source
        return src + self.__str_common()

    def format_repr(self, ccassignments):
        if self.source_is_cc():
            ctrl = self.get_source_midi_cc_number()
            name = ccassignments[ctrl]
            src = "[cc %3d] %s " % (ctrl, name)
        else:
            src = "%s " % self.source
        return src + self.__str_common()
    
    @staticmethod
    def deserialize(obj):
        cls = obj[0]
        if cls == "llia.ParameterMap":
            data = obj[1]
            src = data["source"]
            param = data["parameter"]
            curve = data["curve"]
            mod = data["modifier"]
            dom = data["domain"]
            codom = data["range_"]
            lim = data["limits"]
            return ParameterMap(src, param, curve, mod, dom, codom, lim)
        else:
            msg = "Can not read %s as Llia ParameterMap" % type(obj)
            raise RunTimeError(msg)


@is_parameter_map.when_type(ParameterMap)
def _is_parameter_map(obj):
    return True

@clone.when_type(ParameterMap)
def _clone_pm(obj):
    return obj.clone()

def test():
    p1 = ParameterMap("Velocity", "detune")
    p2 = ParameterMap("Velocity", "detune")
    p3 = ParameterMap("Velocity", "vibrato")
    print(p1)
    print(p2)
    print(p3)
    print(p1 == p1, p1 == p2, p1 == p3)
    
