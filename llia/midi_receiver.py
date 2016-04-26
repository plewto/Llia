# llia.midi_receiver
# 2016.04.23
# Defines MIDI input port by wrapping mido BaseInput.
#

from __future__ import print_function
import sys
import mido
from threading import Thread
import time

import llia.constants as constants


class __MIDIReceiver(object):

    def __init__(self, port_name, trace=False):
        """
        Construct new MIDIReceiver object.
        DO NOT instinate directly, use get_receiver function instead.

        ARGS:
          port_name - String.
                      For a list of available ports execute the mido-ports
                      script on the command line. 
        """
        self._dispatch_table = {"note_on" : {},
                                "note_off" : {},
                                "program_change" : {},
                                "aftertouch" : {},
                                "control_change" : {},
                                "pitchwheel" : {},
                                "polytouch" : {},
                                "sysex" : {},
                                "quarter_frame" : {},
                                "songpos" : {},
                                "song_select" : {},
                                "tune_request" : {},
                                "clock" : {},
                                "start" : {},
                                "continue" : {},
                                "stop" : {},
                                "reset" : {},
                                "active_sensing" : {}}
        self._port_name = port_name
        self._port = mido.open_input(self._port_name)
        self._thread = None
        self._active = False
        if trace:
            self.register_handler("note_on", "trace_on", trace_note_on)
            self.register_handler("note_off","trace_off", trace_note_off)
            self.register_handler("polytouch", "trace_polytouch", trace_polytouch)
            self.register_handler("control_change", "trace_cc", trace_control_change)
            self.register_handler("program_change", "trace_program", trace_program_change)
            self.register_handler("pitchwheel", "trace_pitchwheel", trace_pitchwheel)
            self.register_handler("aftertouch", "trace_aftertouch", trace_aftertouch)
        
    def __run(self):
        while self._active:
            for msg in self._port:
                self.dispatch(msg)

    def port_name(self):
        """Returns String, the MIDI port name."""
        return self._port_name
                
    def start(self):
        """Enable MIDI data reception"""
        self._active = True
        self._thread = Thread(target=self.__run)
        self._thread.setDaemon(True)
        self._thread.start()

    def stop(self):
        """Disable MIDI data reception"""
        self._active = False

    def is_active(self):
        """Returns True if MIDI data reception is enabled"""
        return self._active
            
    def event_types(self):
        """
        Returns a list of possible message types.  See register_handler.
        """
        return self._dispatch_table.keys()

    def register_handler(self, mtype, name, fn):
        """
        Register a function to be called in response to specific MIDI 
        messages.  Each MIDI message type may call any number of registered
        functions.   
        
        ARGS:
          mtype - String, the message type.  The events_types method returns
                  a list of valid message types.
          name  - String, an ID to associate with this specific function
                  and message type.   name may be anything but by convention
                  the primary callback function has the ID "prime".
          fn    - The callback function.  fn should take a single argument
                  which is a mido MIDI message.  No  guarantee is made as to 
                  the order messages registered to the same message type are
                  executed. 
        RAISES:
           KeyError if mtype is invalid.
        """
        self._dispatch_table[mtype][name] = fn

    def remove_handler(self, mtype, name="ALL"):
        """
        Removes handler function for specific MIDI message type.
        
        ARGS:
          mtype - String, the message type.  The event_types method returns
                  a list of valid message types.
          name -  optional String, the function's ID.  If ID is "ALL" then
                  all functions registered to mtype are removed.
        Non defined mtype and function ID's are ignored.
        """
        if name == "ALL":
            self._dispatch_table[mtype] = {}
        else:
            try:
                del self._dispatch_table[mtype][name]
            except KeyError:
                pass
                
    def handler_names(self, mtype):
        """
        Return list of hander ID's for specific message type.
        
        ARGS:
          mtype - String, the message type.  See event_types method.
        
        RETURNS:
          list
        
        RAISES:
          KeyError if mtype is invalid.
        """
        return self._dispatch_table[mtype].keys()

    def __dispatch(self, msg):
        for hfn in self._dispatch_table[msg.type].values():
            hfn(msg)

    def dispatch(self, msg):
        """
        Call registered handlers for MIDI message.

        ARGS:
          msg - A mido Message.
        """
        if self._active:
            self.__dispatch(msg)

def trace_note_on(msg):
    """Diagnostic handler for note_on events"""
    chan0, mtype = msg.channel, msg.type
    keynum, velocity = msg.note, msg.velocity
    velnorm = velocity/127.0
    frmt = "%-15s chan0 [%3d] keynum %3d velocity %3d (%5.3f)"
    if velocity == 0:
        mtype = "note_off*"
    print(frmt % (mtype, chan0, keynum, velocity, velnorm))
    sys.stdout.flush()

def trace_note_off(msg):
    """Diagnostic handler for note_off events"""
    chan0, mtype = msg.channel, msg.type
    keynum, velocity = msg.note, msg.velocity
    velnorm = velocity/127.0
    frmt = "%-15s chan0 [%3d] keynum %3d velocity %3d (%5.3f)"
    print(frmt % (mtype, chan0, keynum, velocity, velnorm))
    sys.stdout.flush()

def trace_polytouch(msg):
    """
    Diagnostic handler for polytouch events.
    NOTE: Llia does not implement polyphonic after touch.
    trace_polytouch has not been tested.
    """
    chan0, mtype = msg.channel, msg.type
    keynum, value = msg.note, msg.value
    valnorm = value/127.0
    frmt = "%-15s chan0 [%3d] keynum %3d value %3d (%5.3f)"
    print(frmt % (mtype, chan0, keynum, value, valnorm))
    sys.stdout.flush()
    
def trace_control_change(msg):
    """Diagnostic handler for MIDI controller events."""
    chan0, mtype = msg.channel, msg.type
    ctrl, value = msg.control, msg.value
    valnorm = value/127.0
    frmt = "%-15s chan0 [%3d] controller %3d value %3d (%5.3f)"
    print(frmt % (mtype, chan0, ctrl, value, valnorm))
    sys.stdout.flush()

def trace_program_change(msg):
    """Diagnostic handler for MIDI program change events"""
    chan0, mtype, prognum = msg.channel, msg.type, msg.program
    frmt = "%-15s chan0 [%3d] program number %3d"
    print(frmt % (mtype, chan0, prognum))
    sys.stdout.flush()

def trace_aftertouch(msg):
    """Diagnostic handler for MIDI aftertouch events"""
    chan0, mtype, value = msg.channel, msg.type, msg.value
    valnorm = value/127.0
    frmt = "%-15s chan0 [%3d] value %3d (%5.3f)"
    print(frmt % (mtype, chan0, value, valnorm))
    sys.stdout.flush()

def trace_pitchwheel(msg):
    """Diagnostic handler for MIDI pitch-bend events"""
    chan0, mtype, pitch = msg.channel, msg.type, msg.pitch
    norm = pitch/float(constants.PITCHWHEEL_DOMAIN[1])
    frmt = "%-15s chan0 [%3d] pitch %+5d (%+6.3f)"
    print(frmt % (mtype, chan0, pitch, norm))
    sys.stdout.flush()

def trace_active_sensing(msg):
    """Diagnostic handler for MIDI active sensing events"""
    print("active_sensing")
    sys.stdout.flush()


__midi_receivers = {}

def get_midi_receiver(port_name, trace=False):
    """
    Retreives MIDIReceiver object.

    ARGS:
     port_name - String

    RETURNS:
      __MIDIReceiver object. 
      If a receiver with the same port_name is already in use, return the
      existing receiver.   Otherwise, create a new receiver object and 
      return.
    """
    try:
        return __midi_receivers[port_name]
    except KeyError:
        mp = __MIDIReceiver(port_name, trace)
        mp.start()
        __midi_receivers[port_name] = mp
        return mp

