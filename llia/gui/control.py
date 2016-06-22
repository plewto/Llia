# llia.gui.widget.py
# 2016.04.25


import abc
from llia.curves import identity

# Each widget has an "aspect" and a "value".  The value represents an
# actual synth parameter value.  The aspect represents the appearance of the
# widget.  A typical example is a slider used for envelope attack
# time with 100 discrete positions between 0 and 99.  Together these 100
# positions are the possible slider aspects.   The slider aspects will map
# to some other range for the actual attack times.  


class AbstractWidget(object):

    def __init__(self, param, client_widget=None):
        super(AbstractWidget, self).__init__()
        self.param = param
        self._client_widget = client_widget
        # Function to map aspect to param value
        self.aspect_to_param_transform = identity
        # Inverse function to map param value to aspect.
        self.param_to_aspect_transform = identity
        self._value = None
        self._aspect = None

    def as_widget(self):
        return self._client_widget or self

    @abc.abstractmethod
    def _set_aspect(self, new_aspect):
        self._aspect = new_aspect
        # Subclasses should override to update client_widget
   
    def aspect(self, new_aspect=None):
        if new_aspect is not None:
            self._set_aspect(new_aspect)
            val = self.aspect_to_param_transform(new_aspect)
            self._value = val
        return self._aspect

    def value(self, new_value=None):
        if new_value is not None:
            self._value = new_value
            asp = self.param_to_aspect_transform(new_value)
            self._set_aspect(asp)
        return self._value


# DUMMY_WIDGET = AbstractWidget(None)


