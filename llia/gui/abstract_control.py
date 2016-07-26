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


# Defines an abstract GUI control element.
# A control consist of one or more widgets. The exact widget type is
# determined by the GUI library in use.
#
# Each control has a "value" and an associated "aspect".  A control's value
# directly corresponds to a SC synth parameter.  A control's aspect
# indicates it's appearance.
#
# A common simple case is an envelope time slider.  The slider
# will have a fixed number of discrete steps, for instance between 0 and
# 99, which indicate the slider's aspect.  Each of these positions will map
# to some real value for envelope time.
#
# A control may also be "compound" and encompass more then one widget.  A
# typical example would be a group of radio buttons.
#
class AbstractControl(object):

    def __init__(self, param, editor, primary_widget, **widgets):
        self.param = param
        self.editor = editor
        self.synth = editor.synth
        self._widgets = widgets
        self._widgets["primary"] = primary_widget
        self.aspect_to_value_transform = identity
        self.value_to_aspect_transform = identity
        self._current_aspect = None
        self._current_value = None

    def widget(self, key=None):
        if not key:
            return self._widgets["primary"]
        else:
            return self._widgets[key]

    def widget_keys(self):
        return self._widgets.keys()

    def has_widget(self, key):
        return self._widgets.has_key(key)
        
    @abc.abstractmethod
    def update_aspect(self):
        pass

    @abc.abstractmethod
    def callback(self, *args):
        pass
    
    def aspect(self, new_aspect=None):
        if new_aspect is not None:
            self._current_aspect = new_aspect
            self._current_value = self.aspect_to_value_transform(new_aspect)
            self.update_aspect()
        return self._current_aspect

    def value(self, new_value=None):
        if new_value is not None:
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
    return int(clip(_norm_to_aspect(n), 0, 199))

def aspect_to_norm(a):
    return float(clip(_aspect_to_norm(a), 0.0, 1.0))

#  ---------------------------------------------------------------------- 
#                          BiPolar Normalized values
#
# Polarzied normal values have rwal range of [-1.0, +1.0] and an
# aspect range of [0,99]
#

POLAR_ASPECT_DOMAIN = (0, 199)
POLAR_CODOMAIN = (-1.0, 1.0)

_polar_to_aspect = linfn((-1.0, 1.0),(0,199))
_aspect_to_polar = linfn((0,199),(-1.0, 1.0))

def polar_to_aspect(n):
    return int(clip(_polar_to_aspect(n), 0, 99))

def aspect_to_polar(n):
    return float(clip(_aspect_to_polar(n), -1.0, 1.0))


# Two sets of amplitude related functions are defied: mix and volume.
# Both have aspect domains of (0,199).
#
# The mix functions are intended for the relative mix between synth
# elements, such as oscillator levels.   
#
# The volume functions are for over all instrument/effect amplitude, and
# provide up to +6db of gain.
#
#  ---------------------------------------------------------------------- 
#                                   Mix
#
# Mix is expressed as a liner aspect between 0 and 199 with a discontinuous
# mapping to amplitude.   Maximum gain is 0.  
#
# aspect(199)   ->   0db
# aspect(100)   ->  -9db
# aspect(  1)   -> -48db
# aspect(  0)   -> -infinitiy

def mix_aspect_to_amp(va):
    if va == 0:
        return 0
    elif va <= 99:
        a,b = 0.398,-48.4
    else:
        a,b = 0.091,-18.11
    return db_to_amp(min(a*va+b, 0))

def amp_to_mix_aspect(amp):
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
# Volume is similer to mix but allows positive gain and has control "dead"
# spots.
#
# aspect(191...199)  ->  +6db
# aspect(181...189)  ->  +3db
# aspect(179...180)  ->   0db
# aspect(81)         -> -12db
# aspect(1)          -> -48db
# aspect(0)          -> -infinity

def volume_aspect_to_amp(va):
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
# Times are divided into 4 regions with lowe aspects having higher
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
    a = clip(a, 0, len(__ENV_TIMES)-1)
    return __ENV_TIMES[a]

def envtime_to_aspect(t):
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
    f = float(clip(__ASPECT_TO_SIMPLE_LFO(a), 0.1, 7.0))
    return f

def simple_lfo_to_aspect(f):
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
    
