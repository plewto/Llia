# llia.gui.abstract_control
# 2016.04.25
#
# Defines abstract GUI control

from __future__ import print_function
import abc, numpy
    
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
# A very common simple case is a slider used for envelope time.  The slider
# will have a fixed number of discrete steps, for instance between 0 and
# 99, which indicate the slider's aspect.  Each of these positions will map
# to some real value for envelope time.
#
# A control may also be "compound" and encompass more then one widget.  A
# typical example would be a group of radio buttons.  Another compound
# example might be coarse and fine oscillator frequency controls. 
#
class AbstractControl(object):

    def __init__(self, param, editor, **widget):
        self.param = param
        self.editor = editor
        self._widgets = widgets
        self.aspect_to_value_transform = identity
        self.value_to_aspect_transform = identity
        self._current_aspect = None
        self._current_value = None

    def widget(self, key):
        return self._widgets[key]

    def widget_keys(self):
        return self._widgets.keys()

    def has_widget(self, key):
        return self._widgets.has_key(key)
        
    @abc.abstractmethod
    def update_widget_aspect(self):
        pass

    @abc.abstractmethod
    def callback(self, *args):
        pass
    
    def aspect(self, new_aspect=None):
        if new_aspect is not None:
            self._current_aspect = new_aspect
            self._current_value = self.aspect_to_value_transform(new_aspect)
            self.update_widget_aspect()
        return self._current_aspect

    def value(self, new_value=None):
        if new_value is not None:
            self._current_aspect = self.value_to_aspect_transform(new_value)
            self._current_value = new_value
            self.update_widget_aspect()
        return self._current_value
        


#  ********************************************************************** 
#                         Standardized Control Curves
#  **********************************************************************


#  ---------------------------------------------------------------------- 
#                              Normalized values
#
# The default "normalized" parameter has float range [0.0, 1.0] and an
# int aspect range of [0,99]
#

NORM_ASPECT_DOMAIN = (0, 99)
NORM_CODOMAIN = (0.0, 1.0)

_norm_to_aspect = linfn((0.0, 1.0),(0, 99))
_aspect_to_norm = linfn((0,99),(0.0,1.0))

def norm_to_aspect(n):
    return int(clip(_norm_to_aspect(n), 0, 99))

def aspect_to_norm(n):
    return float(clip(_aspect_to_norm), 0.0, 1.0)

#  ---------------------------------------------------------------------- 
#                          BiPolar Normalized values
#
# Polarzied normal values have rwal range of [-1.0, +1.0] and an
# aspect range of [0,99]
#

POLAR_ASPECT_DOMAIN = (0, 99)
POLAR_CODOMAIN = (-1.0, 1.0)

_polar_to_aspect = linfn((-1.0, 1.0),(0,99))
_aspect_to_polar = linfn((0,99),(-1.0, 1.0))

def polar_to_aspect(n):
    return int(clip(_polar_to_aspect(n), 0, 99))

def aspect_to_polar(n):
    return float(clip(_aspect_to_polar(n), -1.0, 1.0))

#  ---------------------------------------------------------------------- 
#                                   Volume
#
# Volume is expressed as a liner value between 0 and 99 with a discontinuous
# mapping to amplitude.
#
# vol(99) -> amp(1.000)   0.00 db
# vol(98) -> amp(0.944)  -0.50 db
# vol(97) -> amp(0.891)  -1.00 db
# vol(96) -> amp(0.841)  -1.50 db
# vol( 1) -> amp(0.004)  -48 db
# vol( 0) -> amp(0.000)   -infinity


VOLUME_ASPECT_DOMAIN = (0, 99)
VOLUME_CODOMAIN = (0.0, 1.0)

def volume_aspect_to_amp(va):
    if va < 1:
        amp = 0.0
    else:
        db = 0.48*va-47.52
        amp = db_to_amp(db)
    return float(clip(amp, 0, 1))

def amp_to_volume_aspect(amp):
    db = amp_to_db(amp)
    if db <= -48:
        aspect = 0
    else:
        aspect = 2.042*db + 99
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
#    a[  0] -->  0.000
#    a[  1] -->  0.004  delta = 0.004 seconds
#
#    a[ 25] -->  0.100
#    a[ 26] -->  0.1375 delta = 0.0375
#
#    a[ 50] -->  1.0375
#    a[ 51] -->  1.1605 delta = 0.1230
#
#    a[ 75] -->   4.1125 gemoetric growth above a[75]
#    a[ 76] -->   4.7294 ratio = 1.15
#    a[ 80] -->   8.2717
#    a[ 90] -->  33.4637 
#    a[ 99] --> 117.721


__ENV_TIMES = []
__time, __delta = 0.0, 0.004
for i in range(0, 25):
    __ENV_TIMES.append(__time)
    __time += __delta
__delta = 0.0375
for i in range(25, 50):
    __ENV_TIMES.append(__time)
    __time += __delta
__delta = 0.123
for i in range(50, 75):
    __ENV_TIMES.append(__time)
    __time += __delta
__ratio = 1.15
for i in range(75, 100):
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
            
        
    


