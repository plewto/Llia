# llia.osc_transmitter
# 2016.02.21
# Wraps Pyosc object for OSC transmissions

from __future__ import print_function
import llia.thirdparty.OSC as pyosc
#import llia.config as config

class OSCTransmitter(object):

    def __init__(self, oscID, host_and_port, trace=False):
        """
        Construct new OSCTransmitter object.

        ARGS:
          oscID   - String, oscID used for OSC message address.
          host - tuple (address, port).
        """
        object.__init__(self)
        self._oscID = oscID
        self._host = None # tuple (ip-addr, port)
        self._client = None
        self._is_dead = False
        self.trace = trace
        self.host(host_and_port)
        
    def oscID(self):
        """
        Retrieve and optionally change OSC address id.
        """
        return self._oscID
        
    def message_path(self, *args):
        """
        Construct OSC message address from oscID and optional arguments.
        For arguments 'a', 'b', 'c' the resulting address is '/oscID/a/b/c'
        where oscID is result of self.oscID()
        """
        acc = self._oscID
        for a in args:
            acc += "/%s" & a
        return acc

    def _create_client(self):
        if self._client:
            self._client.close()
        self._client = pyosc.OSCClient()
        self._client.connect(self._host)
    
    def host(self, new_host=None):
        """
        Retrieve and optionally change server host address and port.

        ARGS:
          new_host - optional, tuple (address, port).  If new_host is specified
                     the current client (if any) is closed prior to opening a 
                     new client.
        RETURNS:
          tuple (address, port)
        """
        if new_host:
            self._host = new_host
            self._create_client()
        return self._host

    def create_message(self, msg, payload):
        """
        Creates a new OSC message.
        
        ARGS:
          msg     - String, the msg name.  The ultimate OSC address is 
                    derived form self.oscID() and msg.
          payload - List of message parameters
        
        RETURNS:
          pyosc.OSCMessage
        """
        path = "/Llia/%s/%s" % (self._oscID, msg)
        omsg = pyosc.OSCMessage(path)
        for a in payload:
            omsg.append(a)
        return omsg

    def send(self, msg, payload=[]):
        """
        Transmits OSC message to server.
        msg and payload arguments are identical to create_message
        """
        if self._is_dead:
            msg = "Connection Closed oscID = %s, host = %s"
            msg = msg % (self._oscID, self._host)
            raise IOError(msg)
        omsg = self.create_message(msg, payload)
        if self.trace:
            tmsg = "OSCTransmitter.send %s" % omsg
            print(tmsg)
        self._client.send(omsg)

    def send_raw(self, path, payload=[]):
        omsg = pyosc.OSCMessage(path)
        for a in payload:
            omsg.append(a)
        if self.trace:
            tmsg = "OSCTransmitter.send_raw %s" % omsg
            print(tmsg)
        self._client.send(omsg)

        
    def x_ping(self):
        """
        Transmit a 'ping' to the OSC server.   The server should respond in 
        an obvious way to indicate it has received the message.
        """
        self.send("ping")

    def x_reset(self):
        """
        Request OSC server to reset synth parameters to default values.
        """
        self.send("reset")

    def x_free(self):
        """
        Request OSC server to free resources.  Once free is called it is
        unlikely the server will respond to further OSC messages.
        """
        self.send("free")

    def x_dump(self):
        """
        Request OSC server to produce a diagnostic dump of its current state.
        """
        self.send("dump")

    def x_note_on(self, keynumber, frequency=440, velocity=0.5):
        """
        Request OSC server to turn a note on.

        ARGS:
          keynumber - MIDI keynumber
          frequency - float, note frequency in Hertz.
          velocity  - float, normalized velocity in range (0.0, 1.0)

        Velocity values of 0 should be treated as a note_off.
        """
        self.send("note-on", [keynumber, frequency, velocity])

    def x_note_off(self, keynumber):
        """
        Request OSC server to turn a note off.  Llia does not support
        release velocity.
        
        ARGS:
          keynumber - MIDI key number.
        """
        self.send("note-off", [keynumber])

    def x_all_notes_off(self):
        """Request that OSC server to turn all notes off"""
        self.send("all-notes-off")

    def x_synth_param(self, param, value):
        """
        Request OSC server to update synth parameter.
        
        ARGS:
          param - String, parameter name
          value - The new value (most likely a float)        
        """
        self.send("synth-param", [param, value])
        
    def x_synth_program(self, program):
        """
        Request OSC server to update all synth parameters of program.

        ARGS:
          program - An instance of llia.Program or any dictionary like 
                    object.  A parameter update is sent for each 
                    parameter/value pair in the dictionary.
        """
        for k,v in program.items():
            self.x_synth_param(k,v)
