# llia.gui.abstract_control
# 2016.04.25
#
# Defines abstract GUI control

from __future__ import print_function
import abc, numpy

from llia.generic import is_synth_control
from llia.util.lmath import clip, db_to_amp, amp_to_db, logn
from llia.curves import identity

from llia.curves import linear_coefficients as linco
from llia.curves import linear_function as linfn

class AbstractControl(object):

    """
    AbstractControl defines an abstract GUI control element.  A control
    consist of one or more widgets. The exact widget type(s) is dependent on
    the GUI system in use.

    A control may assume any number of pre-defined values which directly
    correspond to a Synth parameter. 

    Each control value has a distinct 'aspect', where an aspect is the
    visual appearance of the control.  This terminology is borrowed from
    railroad signaling. 
    """
    
    def __init__(self, param, editor, primary_widget, **widgets):
        """
        Construct new AbstractControl 
        param - string, the synth parameter
        editor - 
        primary_widget - The control's main widget
        widgets - optional, secondary widgets.
        """
        self.param = param
        self.editor = editor
        self.synth = editor.synth
        self._widgets = widgets
        self._widgets["primary"] = primary_widget
        self.aspect_to_value_transform = identity
        self.value_to_aspect_transform = identity
        self._current_aspect = None
        self._current_value = None
        self.range_ = [-1e6,1e6]   # [min max]
        
    def widget(self, key=None):
        """
        Returns named widget.
        By default returns the primary widget.
        """
        if not key:
            return self._widgets["primary"]
        else:
            return self._widgets[key]

    def widget_keys(self):
        """
        Returns list of string keys for constituent widgets.
        At a minimum this list will contain "primary".
        """
        return self._widgets.keys()

    def has_widget(self, key):
        """
        Predicate, True if key names a constituent widget.
        """
        return self._widgets.has_key(key)
        
    @abc.abstractmethod
    def update_aspect(self):
        """
        Change appearance to match current value.
        """
        pass

    @abc.abstractmethod
    def callback(self, *args):
        """
        Callback function to the GUI library.
        callback is executed whenever the control is manipulated or changed.
        """
        pass
    
    def aspect(self, new_aspect=None):
        """
        Returns, and optionally change, the current aspect.
        If the aspect is altered, the control's values is changed to match.
        """
        if new_aspect is not None:
            self._current_aspect = new_aspect
            self._current_value = self.aspect_to_value_transform(new_aspect)
            self.update_aspect()
        return self._current_aspect

    def value(self, new_value=None):
        """
        Returns, and optionally change, the current value.
        If the value is altered, the aspect is changed to match.
        """
        if new_value is not None:
            mn,mx = self.range_
            new_value = float(min(max(new_value,mn),mx))
            self._current_aspect = self.value_to_aspect_transform(new_value)
            self._current_value = new_value
            self.update_aspect()
        return self._current_value
        
@is_synth_control.when_type(AbstractControl)
def _is_synth_control(obj):
    return True
    

#  ********************************************************************** 
#                         Standardized Control Curves
#  **********************************************************************


#  ---------------------------------------------------------------------- 
#                              Normalized values
#
# The default "normalized" parameter has float range [0.0, 1.0] and an
# int aspect range of [0,99]
#

NORM_ASPECT_DOMAIN = (0, 199)
NORM_CODOMAIN = (0.0, 1.0)

_norm_to_aspect = linfn((0.0, 1.0),(0, 199))
_aspect_to_norm = linfn((0,199),(0.0,1.0))

def norm_to_aspect(n):
    """
    Converts normalized value to control aspect.
    Used with slider like controls to convert a "normalized" value between 
    0.0 and 1.0 inclusive to slider position (int 0..199).
    """
    return int(clip(_norm_to_aspect(n), 0, 199))

def aspect_to_norm(a):
    """
    Converts aspect to normalized value.
    Used with slider like controls to convert slider position (as an int
    between 0 and 199) to a normalized float between 0.0 and 1.0 inclusive. 
    """
    return float(clip(_aspect_to_norm(a), 0.0, 1.0))

#  ---------------------------------------------------------------------- 
#                          Bipolar Normalized values
#
# Polarized normal values have real range of [-1.0, +1.0] and an
# aspect range of [0,99]
#

POLAR_ASPECT_DOMAIN = (0, 199)
POLAR_CODOMAIN = (-1.0, 1.0)

_polar_to_aspect = linfn((-1.0, 1.0),(0,199))
_aspect_to_polar = linfn((0,199),(-1.0, 1.0))

def polar_to_aspect(n):
    """
    Converts signed normalized value to controller aspect.
    Used with slider like controls with signed normalized values.
    Converts signed normal value, a float between -1.0 and +1.0 inclusive,
    to slider position, an int between 0 and 199.
    """
    return int(clip(_polar_to_aspect(n), 0, 199))

def aspect_to_polar(n):
    """
    Converts controller aspect to signed normalized value.
    Used with slider like controls with signed normalized values.
    Converts slider position, an int between 0 and 199, to signed 
    normalized value, a float between -1.;0 and +1.0.
    """
    return float(clip(_aspect_to_polar(n), -1.0, 1.0))


# Two sets of amplitude related functions are defied: mix and volume.
# Both have aspect domains of (0,199).
#
# The mix functions are intended for the relative mix between synth
# elements, such as oscillator levels.   
#
# The volume functions are for over all instrument/effect amplitude, and
# provide up to +6 db of gain.
#
#  ---------------------------------------------------------------------- 
#                                   Mix
#
# Mix is expressed as a liner aspect between 0 and 199 with a discontinuous
# mapping to amplitude.   Maximum gain is 0.  
#
# aspect(199)   ->   0 db
# aspect(100)   ->  -9 db
# aspect(  1)   -> -48db
# aspect(  0)   -> -infinitiy

def mix_aspect_to_amp(va):
    """
    Converts slider position, an int between 0 and 199, to gain factor.
    Used with slider like gain controls.
    The response is divided into several distinct regions.

           199  -  0db
    100 to 198  -  -9db to 0db
      1 to  99  - -48db to -9db
      0         - -infinity
    """
    if va == 0:
        return 0
    elif va <= 99:
        a,b = 0.398,-48.4
    else:
        a,b = 0.091,-18.11
    return db_to_amp(min(a*va+b, 0))

def amp_to_mix_aspect(amp):
    """
    Converts gain ratio to slider position.
    Used with slider like gain controls.
    The response is non-linear, see mix_aspect_to_amp
    """
    amp = abs(amp)
    if amp == 0:
        return 0
    else:
        db = amp_to_db(amp)
        if db < -9:
            a,b = 2.51,121.6
        else:
            a,b = 11,199.0
        pos = a*db+b
        return int(min(pos, 199))
    
        
#  ---------------------------------------------------------------------- 
#                                   Volume
#
# Volume is similar to mix but allows positive gain and has control "dead"
# spots.
#
# aspect(191...199)  ->  +6db
# aspect(181...189)  ->  +3db
# aspect(179...180)  ->   0db
# aspect(81)         -> -12db
# aspect(1)          -> -48db
# aspect(0)          -> -infinity

def volume_aspect_to_amp(va):
    """
    Convwerts controller aspect to gain factor. 
    Used with slider like volume controls.
    The response has several distinct regions:

           199 -  +6db
    181 to 198 -  +3db
    179 to 180 -   0db
     81 to 178 -  -12db to 0db
      1 to 80  -  -48db to -12db
      0        -  -infinity db
    """
    if 191 <= va:
        db = 6
    elif 181 <= va:
        db = 3
    elif 171 <= va:
        db = 0
    elif 81 <= va:
        db = int(0.135 * va -23)
    elif 1 <= va:
        db = int(0.462 * va -48.462)
    else:
        return 0.0
    amp = float(db_to_amp(db))
    return amp

def amp_to_volume_aspect(amp):
    """
    Converts gain factor to controller aspect.
    Used with slider like volume controls.
    See volume_aspect_to_amp
    """
    amp = abs(amp)
    if amp == 0:
        return 0
    else:
        db = int(amp_to_db(amp))
        if db >= 6:
            aspect = 199
        elif db >= 3:
            aspect = 185
        elif db >= 0:
            aspect = 175
        elif -12 <= db:
            aspect = 7.42*db + 170
        elif -48 <= db:
            aspect = 2.2*db + 106.4
        else:
            aspect = 0
        return int(aspect)

#  ---------------------------------------------------------------------- 
#                               Envelope Times
#
# Envelope times using table lookup.
# aspect range [0, 99]
# time range [0.0, ~120]
#
# Times are divided into 4 regions with lower aspects having higher
# resolutions.
#

__ENV_TIMES = []
__time, __delta = 0.0, 0.004
for i in range(0, 50):
    __ENV_TIMES.append(__time)
    __time += __delta
__delta = 0.0375
for i in range(25,100):
    __ENV_TIMES.append(__time)
    __time += __delta
__delta = 0.123
for i in range(50,150):
    __ENV_TIMES.append(__time)
    __time += __delta
__ratio = 1.15
for i in range(75, 199):
    __ENV_TIMES.append(__time)
    __time *= __ratio
__ENV_TIMES = numpy.array(__ENV_TIMES)

ENVTIME_ASPECT_DOMAIN = (0, 99)
ENVTIME_CODOMAIN = (0.0, __ENV_TIMES[-1])

def aspect_to_envtime(a):
    """
    Converts controller aspect to envelope segment time.
    The response has several distinct regions:
    """
    a = clip(a, 0, len(__ENV_TIMES)-1)
    return __ENV_TIMES[a]

def envtime_to_aspect(t):
    """
    Converts envelope segment time to controller aspect.
    The response has several distinct regions.
    See aspect_to_envtime
    """
    a = (numpy.abs(__ENV_TIMES-t)).argmin()
    return a
    
    
#  ---------------------------------------------------------------------- 
#                              Simple LFO times
#
# aspect range [0, 199]
# frequency range [0.1, 7.0]  resolution 0.0345 s
#

SIMPLE_LFO_ASPECT_DOMAIN = (0, 199)
SIMPLE_LFO_CODOMAIN = (0.1, 7.0)

__ASPECT_TO_SIMPLE_LFO = linfn(SIMPLE_LFO_ASPECT_DOMAIN, 
                               SIMPLE_LFO_CODOMAIN)
__SIMPLE_LFO_TO_ASPECT = linfn(SIMPLE_LFO_CODOMAIN, 
                               SIMPLE_LFO_ASPECT_DOMAIN)

def aspect_to_simple_lfo(a):
    """
    Converts controller aspect to LFO frequency.
    """
    f = float(clip(__ASPECT_TO_SIMPLE_LFO(a), 0.1, 7.0))
    return f

def simple_lfo_to_aspect(f):
    """
    Converts LFO frequency to controller aspect.
    """
    a = int(clip(__SIMPLE_LFO_TO_ASPECT(f), 0, 199))
    return a
            
        
#  ---------------------------------------------------------------------- 
#                           Fine Frequency Control
# aspect range [0, 1990
# freq scale [1.0,2.0]

FINE_FREQUENCY_DOMAIN = (0,199)
FINE_FREQUENCY_CODOMAIN = (1.0, 2.0)

aspect_to_fine_frequency = linfn(FINE_FREQUENCY_DOMAIN,
                                 FINE_FREQUENCY_CODOMAIN)
fine_frequency_to_aspect = linfn(FINE_FREQUENCY_CODOMAIN,
                                FINE_FREQUENCY_DOMAIN)
                                 
#  ---------------------------------------------------------------------- 
#                             Third Octave Tables

__THIRD_OCTAVE = [20, 25, 32, 40, 50, 63, 80,
                  100, 125, 160, 200, 250, 315, 400, 500, 630, 800,
                  1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000,
                  6300, 8000, 10000, 12500, 16000, 20000]
__THIRD_OCTAVE = numpy.array(__THIRD_OCTAVE)


def aspect_to_third_octave(a):
    a = int(min(max(a, 0), 30))
    f = __THIRD_OCTAVE[a]
    return f

def third_octave_to_aspect(f):
    a = (numpy.abs(__THIRD_OCTAVE-f)).argmin()
    return int(a)
    
