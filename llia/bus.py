# llia.bus.py
# Defines abstract bus objects

from __future__ import print_function
import abc

from llia.generic import is_bus_source, is_bus_sink

class BusSource(object):

    '''
    Represents a bus source signal as synth_id and synth parameter.
    '''
    
    def __init__(self, sid, param):
        self.sid = sid
        self.param = param
        
    def __eq__(self, other):
        '''
        An object is considered eq to self if:
        1) other is self
        2) other is an instance of BusSource and at least one of the 
           following conditions is true:
           a) other.param == self.param
           b) other.param is '' or None
        '''
        if self is other:
            return True
        else:
            if not is_bus_source(other):
                return False
        if other.sid == self.sid:
            if not other.param:
                return True
            else:
                return other.param == self.param
        else:
            return False
            
    def __neq__(self, other):
        return not self.__eq__(other)

    def as_tuple(self):
        '''
        Returns tuple (id, param)
        '''
        return tuple([self.sid, self.param])
    
    def __str__(self):
        s = 'BusSource("%s","%s")'
        return s % (self.sid, self.param)

@is_bus_source.when_type(BusSource)
def _is_bus_source(obj):
    return True
    

class BusSink(object):

    '''
    Represents a bus signal sink as synth_id and synth parameter.
    '''
    
    def __init__(self, sid, param):
        self.sid = sid
        self.param = param
        
    def __eq__(self, other):
        '''
        An object is considered eq to self if:
        1) other is self
        2) other is an instance of BusSink and at least one of the 
           following conditions is true:
           a) other.param == self.param
           b) other.param is '' or None
        '''
        if self is other:
            return True
        else:
            if not is_bus_sink(other):
                return False
        if other.sid == self.sid:
            if not other.param:
                return True
            else:
                return other.param == self.param
        else:
            return False
            
    def __neq__(self, other):
        return not self.__eq__(other)

    def as_tuple(self):
        return tuple([self.sid, self.param])
    
    def __str__(self):
        s = 'BusSink("%s","%s")'
        return s % (self.sid, self.param)

@is_bus_sink.when_type(BusSink)
def _is_sink(obj):
    return True

                   
class BusProxy(object):
    '''
    An abstract super class for audio or control buses.
    Each bus has a name, a list of sources and a list of sinks.
    '''
    def __init__(self, name, app, sync=False):
        super(BusProxy, self).__init__()
        self.app = app
        self.name = name
        self._sources = []
        self._sinks = []
        if sync: self.sync_editor()

    @abc.abstractmethod
    def is_protected(self):
        '''
        Predicate which is True for protected buses.
        Protected buses may not be removed.  
        '''
        return False

    @abc.abstractmethod
    def rate(self):
        '''
        Returns sample rate, either "Audio" or "Control"
        '''
        return None

    # Update editor of bus connection change
    def sync_editor(self):
        pass
        # ISSUE: place holder method, not implemented
    
    def is_audio_bus(self):
        return self.rate() == "Audio"

    def is_control_bus(self):
        return self.rate() == "Control"

    def source_count(self):
        '''
        Returns number of source signals sending data to this bus.
        '''
        return len(self._sources)

    def sources(self):
        '''
        Returns list of BusSource objects
        '''
        return self._sources
        
    def has_source(self, sid, param=''):
        '''
        Predicate test if receives data from specific synth

        ARGS:
          sid   - String, synth identification.
          param - optional String, a synth parameter. If param is not 
                  specified then -any- input from sid is considered True

        RETURNS: Bool
        '''
        bs = BusSource(sid, param)
        for q in self._sources:
            if q == bs: return True
        return False
        
    def add_source(self, sid, param, sync=True):
        '''
        Add new source signal.  If an identical source already exists 
        do nothing.

        ARGS:
           sid   - String, synth id
           param - String, synth param used for output
           sync  - boolean, if True re synchronize the GUI editor.
                   ISSUE: sync argument is not used and should be removed.
        '''
        if not self.has_source(sid, param):
            bs = BusSource(sid, param)
            self._sources.append(bs)
            if sync: self.sync_editor()
            
    def remove_source(self,sid, param='', sync=True):
        '''
        Remove source signal, it is not an error if the bus does not have the 
        indicated source.

        ARGS:
           sid   - String, synth id
           param - String, synth param used for output
           sync  - boolean, if True re synchronize the GUI editor.
                   ISSUE: sync argument is not used and should be removed.
        '''
        bs = BusSource(sid, param)
        def fn(a):
            return not(a == bs)
        self._sources = filter(fn, self._sources)
        if sync: self.sync_editor()

    def sink_count(self):
        '''
        Returns count of outputs this bus transmits to.
        '''
        return len(self._sinks)

    def sinks(self):
        '''
        Returns list of BusSink objects.
        '''
        return self._sinks
        
    def has_sink(self, sid, param=''):
        '''
        Predicate test for specific sink.

        ARGS:
           sid   - String, synth id
           param - optional String, synth parameter.  If param is not
                   specified then -any- connection to sid is considered 
                   true.

        RETURNS: Bool
        '''
        bs = BusSink(sid, param)
        for q in self._sinks:
            if q == bs: return True
        return False
        
    def add_sink(self, sid, param, sync=True):
        '''
        Add new output connection.  It is not an error if the specified
        sink already exits.

        ARGS:
          sid   - String, synth id.
          param - String, synth parameter used for input.
          sync  - optional Bool, 
                  ISSUE: sync flag is not used and should be removed.
        '''
        if not self.has_sink(sid, param):
            bs = BusSink(sid, param)
            self._sinks.append(bs)
            if sync: self.sync_editor()

    def remove_sink(self,sid, param='', sync=True):
        '''
        Remove output connection.  It is not an error if the specified
        connection does not exists.

        ARGS:
           sid   - String, synth id.
           param - String, synth parameter used for input.
           sync  - optional Bool, 
                   ISSUE: sync flag is not used and should be removed.
        '''
        bs = BusSink(sid, param)
        def fn(a):
            return not(a == bs)
        self._sinks = filter(fn, self._sinks)
        if sync: self.sync_editor()
            
    def dump(self, depth=0, silent=False):
        '''
        Produce diagnostic dump of bus state.

        ARGS:
          depth  - optional int, sets indentation amount.
          silent - optional flag, if True does not produce screen
                   output as side effect.

        RETURNS: String
        '''
        pad1 = ' '*4*depth
        pad2 = pad1 + ' '*4
        pad3 = pad2 + ' '*4
        r = self.rate()
        acc = "%s%sBus\n" % (pad1, r)
        acc += "%ssources:\n" % pad2
        for s in self._sources:
            t = s.as_tuple()
            acc += '%s%s\n' % (pad3, t)
        acc += "%ssinks:\n" % pad2
        for s in self._sinks:
            t = s.as_tuple()
            acc += '%s%s\n' % (pad3, t)
        if not silent:
            print(acc)
        return acc

    def __str__(self):
        frmt = '%sBus("%s") # '
        acc = frmt % (self.rate(), self.name)
        frmt = '%d sources, %d sinks'
        acc += frmt % (len(self._sources),len(self._sinks))
        return acc
        
class AudioBus(BusProxy):

    def __init__(self, name, app, sync=False):
        super(AudioBus, self).__init__(name, app, sync)

    @staticmethod
    def rate():
        return "Audio"

    def is_hardware_output(self):
        return self.name.startswith("out_")

    def is_hardware_input(self):
        return self.name.startswith("in_")

    def is_protected(self):
        return self.is_hardware_output() or self.is_hardware_input()
    
    
class ControlBus(BusProxy):

    def __init__(self, name, app, sync=False):
        super(ControlBus, self).__init__(name, app, sync)

    @staticmethod
    def rate():
        return "Control"

    def is_protected(self):
        return self.name.startswith("null_")
