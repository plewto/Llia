# llia.synth_proxy
#
# Defines two classes:
#   SynthSpecs - holds global information about all synths of a given type
#   SynthProxy - a client side representation of an active synth.

from __future__ import print_function
import abc
from os.path import join

import llia.constants as con
import llia.curves as curves
from llia.llerrors import LliaPingError, NoSuchBusOrParameterError
from llia.generic import is_instrument, clone, dump
from llia.osc_transmitter import OSCTransmitter
from llia.locked_dictionary import LockedDictionary
from llia.mutation import DUMMY_MUTATION

#  ---------------------------------------------------------------------- 
#                               SynthSpecs class

SPECS_TEMPLATE = {"format" : None,
                  "constructor" : None,
                  "description" : None,
                  "program-generator" : None,
                  "mutation" : DUMMY_MUTATION,
                  "pretty-printer" : None,
                  "help" : None,
                  "notes" : None,
                  "is-efx" : False,
                  "is-controller" : False,
                  "keymodes" : [],
                  "audio-output-buses" : [],  
                  "audio-input-buses" : [],
                  "control-output-buses" : [],
                  "control-input-buses" : [],
                  "buffers" : [],
                  "pallet" : None,
                  "logo" : None,
                  "small-logo" : None}


class SynthSpecs(LockedDictionary):

    '''
    SynthSpecs is a dictionary like object which defines the features and 
    structure of a class of synths.   All synths of the same type share
    a common SynthSpecs.
    '''
    
    global_synth_type_registry = {}

    @staticmethod
    def available_synth_types():
        '''
        Returns a sorted list of available synth types.
        '''
        k = SynthSpecs.global_synth_type_registry.keys()
        k.sort()
        return k

    @staticmethod
    def is_known_synth_type(stype):
        '''
        Predicate returns True is argument is a known synth type.
        '''
        return SynthSpecs.global_synth_type_registry.has_key(stype)
    
    @staticmethod
    def create_synth_proxy(app, stype):
        '''
        Creates an instance of SynthProxy.

        ARGS:
         
            app   - an instance of LliaApp
            stype - String, the synth type.
                    is_know_synth_type(stype) must be True
        RETURNS: SynthProxy

        Raises KeyError if stype is unknown.
        '''
        try:
            specs = SynthSpecs.global_synth_type_registry[stype]
            cfn = specs["constructor"]
            syproxy = cfn(app)
            return syproxy
        except KeyError:
            return None
    
    def __init__(self, stype):
        '''
        Construct new instance of SynthSpecs.  
        This constructor should only be called once for any given stype.

        SynthSpecs is a dictionary like object with a pre-defined set of 
        keys.  All keys are strings:
        
            format            - String, same as stype
            constructor       - Function to create SynthProxy fn(app)
                                app - instance of LliaApp
            description       - String, short (one-line) description of Synth
            program-generator - Optional function to generate random patches.
                                fn(slot, *args)
                                   slot - int program number (0..127)
                                   args - optional arguments, 
                                          currently not used.                   
            pretty-printer    - Optional function to "pretty-print" program.
                                fn(program, slot=127)
                                     program - an instance of Program
                                     returns: String
                                     The resulting string should be valid 
                                     Python code which may be used to recreate
                                     the program. 
            help              - String, help-topic
            notes             - String, optional remarks about this synth.
            is-efx            - Boolean.  Synths come in three flavors:
                                 'synth', 'efx' and 'controller'.
  
                                  A regular 'synth' is a playable instrument.
                                  
                                  An 'efx' is an effects synth used to process
                                  audio signals.

                                  A 'controller' is a synth object which 
                                  generates control signals.  

                                  is-efx should be True for efx and controller
                                  synths.
            keymodes          - A list of supported key-modes.
            buffers           - A list of synth parameters used for indicating
                                SuperCollider buffers.
            pallet            - An instance of Pallet.
            audio-output-buses   - A nested list of synth parameters for audio
                                   output.  The list format has the form:
                                   [[param1, default],[param2,default],...]
            audio-input-buses    - A nested list of audio input parameters,
                                   with same format as audio-output-buses
            control-output-buses - A nested list of control bus output 
                                   parameters.
            control-input-buses  - A nested list of control bus input
                                   parameters.

        ARGS:
           stype - String, the synth type.
                   Once constructed the SynthSpecs is added to a global 
                   registry of known synth types.

        RETURNS: SynthSpecs.
        '''
        super(SynthSpecs, self).__init__(SPECS_TEMPLATE)
        SynthSpecs.global_synth_type_registry[stype] = self
        self["format"] = stype
        resource_path = join("resources", stype)
        self["logo"] = join(resource_path, "logo.png")
        self["small-logo"] = join(resource_path, "logo_small.png")
        
        
    def __setitem__(self, key, item):
        '''
        Set spec value.
        Raises KeyError if key was not established at object 
        construction time.
        '''
        if self.has_key(key):
            super(SynthSpecs, self).__setitem__(key, item)
        else:
            msg = "Illegal SynthSpecs key: '%s'" % key
            raise KeyError(msg)

    def create_proxy_synth(self, app):
        '''
        Creates instance of SynthProxy.
        The synth serial id is generated automatically.

        ARGS:
           app - an instance of LliaApp

        RETURNS: SynthProxy
        '''
        cfn = self["constructor"]
        id_ = SynthSpecs.create_id(self)
        return cfn(app, id_)

    
#  ---------------------------------------------------------------------- 
#                              SynthProxy class
    
BEND_SCALE, BEND_BIAS = curves.linear_coefficients(con.PITCHWHEEL_DOMAIN,
                                                   con.BIPOLAR_RANGE)
        
class SynthProxy(object):

    IS_SYNTH_PROXY = True
    
    '''
    SynthProxy is a client side representation of an active synth(s).
    '''

    _synth_serial_number = 0

    @staticmethod
    def current_synth_serial_number():
        '''
        Each synth is assigned a unique int identification when it is 
        created.  This method returns the new value to be used without 
        incrementing the internal counter.
        
        RETURNS: int
        '''
        return SynthProxy._synth_serial_number

    @staticmethod
    def assign_synth_serial_number():
        ''''
        Returns a unique synth identification number.
        This method will never return the same number twice.
        If you wish to inspect the current serial number without 
        altering it, use current_synth_serial_number

        RETURNS: int
        '''
        sn = SynthProxy._synth_serial_number
        SynthProxy._synth_serial_number += 1
        return sn
    
    def __init__(self, app, specs, bank):
        '''
        Constructs new SynthProxy

        Do not call this constructor directly! 
        Use SynthSpecs.create_synth_proxy to create a new SynthProxy.

        ARGS:
           
          app   - an instance of LliaApp.
          specs - an instance of SynthSpecs.
          bank  - an instance of ProgramBank.

        RETURNS: SynthProxy.
        '''
        super(SynthProxy, self).__init__()
        self.is_efx = False
        self.is_controller = False
        self.id_ = SynthProxy.assign_synth_serial_number()
        self.app = app
        self.specs = specs
        self.synth_format = specs["format"]      # format is synonyms with
                                                 # "synth type"
        self.sid = "%s_%d" % (self.synth_format, # sid is a combination of
                              self.id_)          # synth-type and id_
        self.synth_editor = None                 # under Tk, an instance of
                                                 # TkSynthWindow
        global_oscid = app.proxy.global_osc_id()
        self.oscID = "%s/%s/%s" % (global_oscid,self.synth_format, self.id_)
        self._bank = bank.clone()
        self.keymode = ""            # Read only
        self.voice_count = 0         # Read only
        self._midi_chan0 = 0         # MIDI channel is "zero-indexed" (0..15)
        self._key_table_name = "EQ12"
        # _audio_output_buses
        # _audio_input_buses
        # _control_output_buses
        # _control_input_buses
        # Each dictionary maps synth parameter(s) to the names of the buses
        # connected to that parameter.  The actual Bus objects are maintained
        # by app.proxy (an instance of LliaProxy)
        self._audio_output_buses = {}
        for bs in specs["audio-output-buses"]:
            param, busname = bs
            self._audio_output_buses[param] = busname
            self.assign_audio_output_bus(param, busname)
        self._audio_input_buses = {}
        for bs in specs["audio-input-buses"]:
            self._audio_input_buses[bs[0]] = bs[1]
        self._control_output_buses = {}
        for bs in specs["control-output-buses"]:
            self._control_output_buses[bs[0]] = bs[1]
        self._control_input_buses = {}
        for bs in specs["control-input-buses"]:
            self._control_input_buses[bs[0]] = bs[1]
        self._buffers = {}
        host_and_port = app.config().host_and_port()
        host_and_port = host_and_port[0], int(host_and_port[1])
        trace_osc = app.config().osc_transmission_trace_enabled()
        self.osc_transmitter = OSCTransmitter(self.oscID, 
                                              host_and_port,
                                              trace_osc)
        def register_midi_handler(event, hfn, fid=""):
            fid = "%s%s.%s" % (fid, self.oscID, event)
            app.midi_receiver.register_handler(event, fid, hfn)
        register_midi_handler("note_on", self._note_on_handler)
        register_midi_handler("note_off", self._note_off_handler)
        register_midi_handler("aftertouch", self._aftertouch_handler)
        register_midi_handler("pitchwheel", self._pitchwheel_handler)
        register_midi_handler("control_change", self._cc_handler)
        register_midi_handler("program_change", self._program_change_handler)
        register_midi_handler("clock", self._dummy_handler)
        register_midi_handler("start", self._dummy_handler)
        register_midi_handler("stop", self._dummy_handler)
        register_midi_handler("continue", self._dummy_handler)
        register_midi_handler("reset", self._dummy_handler)

    def status(self, msg):
        '''
        Display status message on main app window.
        '''
        self.app.main_window().status(msg)

    @abc.abstractmethod
    def create_subeditors(self):
        '''
        An abstract method used to build GUI editor for self.
        Subclasses must implement if they are to create editors.

        The exact editor is dependent on the GUI system in use.
        If no GUI system is being used this method should do 
        nothing.
        '''
        pass

    def available_audio_output_parameters(self):
        '''
        Returns sorted list of available audio output bus parameters.
        '''
        def fn(a): return a[0]
        blist = sorted(self._audio_output_buses.keys())
        blist = filter(fn, blist)
        return blist

    def assign_audio_output_bus(self, param, bname, sync=False):
        '''
        Assigns audio output bus to a synth parameter.
        NOTE: This method only modifies the internal state of self.
              It does not transmit any OSC messages to actually establish
              the bus/parameter connection.  
              (use LliaProxy.assign_synth_audio_bus)
        
        ARGS:
          param - String, the synth parameter
          bname - String, the bus name.
          sync  - optional bool, if True notify synth editor of change
        '''
        try:
            proxy = self.app.proxy
            current_bus_name = self._audio_output_buses[param]
            current_bus = proxy.get_audio_bus(current_bus_name)
            new_bus = proxy.get_audio_bus(bname)
            current_bus.remove_source(self.sid, param, sync=False)
            new_bus.add_source(self.sid, param, sync=sync)
            self._audio_output_buses[param] = bname
        except KeyError:
            msg = "Can not assign audio output bus.  "
            msg += "sid=%s, param=%s, bus_name=%s"
            msg = msg % (self.sid, param, bname)
            raise NoSuchBusOrParameterError(msg)

    def available_audio_input_parameters(self):
        '''
        Returns sorted list of available audio output bus parameters.
        '''
        def fn(a): return a[0]
        blist = sorted(self._audio_input_buses.keys())
        blist = filter(fn, blist)
        return blist
        
    def assign_audio_input_bus(self, param, bname, sync=False):
        '''
        Assigns audio input bus to a synth parameter.
        NOTE: This method only modifies the internal state of self.
              It does not transmit any OSC messages to actually establish
              the bus/parameter connection.  
              (use LliaProxy.assign_synth_audio_bus)
        
        ARGS:
          param - String, the synth parameter
          bname - String, the bus name.
          sync  - optional bool, if True notify synth editor of change
        '''
        try:
            proxy = self.app.proxy
            current_bus_name = self._audio_input_buses[param]
            current_bus = proxy.get_audio_bus(current_bus_name)
            new_bus = proxy.get_audio_bus(bname)
            current_bus.remove_sink(self.sid, param, sync=False)
            new_bus.add_sink(self.sid, param, sync=sync)
            self._audio_input_buses[param] = bname
        except KeyError:
            msg = "Can not assign audio input bus.  "
            msg += "sid=%s, param=%s, bus_name=%s"
            msg = msg % (self.sid, param, bname)
            raise NoSuchBusOrParameterError(msg)   

    # Returns bus name assigned to audio input parameter
    # raises KeyError
    def get_audio_input_bus(self, param):
        '''
        Return name of bus assigned to audio input parameter.

        ARGS:
          param - String

        RETURNS: String
        '''
        return self._audio_input_buses[param]

    def get_audio_output_bus(self, param):
        '''
        Return name of bus assigned to audio output parameter.
        
        ARGS:
           param - String
        
        RETURNS: String
        '''
        return self._audio_output_buses[param]

    def get_control_input_bus(self, param):
        '''
        Return name of bus assigned to control input parameter.
        
        ARGS:
          param - String

        RETURNS: String
        '''
        return self._control_input_buses[param]

    def get_control_output_bus(self, param):
        '''
        Return name of bus assigned to control output parameter.

        ARGS:
          param - String

        RETURNS: String
        '''
        return self._control_output_buses[param]

    def available_control_input_parameters(self):
        '''
        Returns sorted list of available control input bus parameters.
        '''
        def fn(a): return a[0]
        blist = sorted(self._control_input_buses.keys())
        blist = filter(fn, blist)
        return blist

    def available_control_output_parameters(self):
        '''
        Returns sorted list of available control output bus parameters.
        '''
        def fn(a): return a[0]
        blist = sorted(self._control_output_buses.keys())
        blist = filter(fn, blist)
        return blist
    
    def assign_control_output_bus(self, param, bname, sync=False):
        '''
        Assigns control output bus to a synth parameter.
        NOTE: This method only modifies the internal state of self.
              It does not transmit any OSC messages to actually establish
              the bus/parameter connection.  
              (use LliaProxy.assign_synth_control_bus)
        
        ARGS:
          param - String, the synth parameter
          bname - String, the bus name.
          sync  - optional bool, if True notify synth editor of change

        Raises llerrors.NoSuchBusOrParameterError
        '''
        try:
            proxy = self.app.proxy
            current_bus_name = self._control_output_buses[param]
            current_bus = proxy.get_control_bus(current_bus_name)
            new_bus = proxy.get_control_bus(bname)
            current_bus.remove_source(self.sid, param, sync=False)
            new_bus.add_source(self.sid, param, sync=sync)
            self._control_output_buses[param] = bname
        except KeyError:
            msg = "Can not assign control output bus.  "
            msg += "sid=%s, param=%s, bus_name=%s"
            msg = msg % (self.sid, param, bname)
            raise NoSuchBusOrParameterError(msg)

    def assign_control_input_bus(self, param, bname, sync=False):
        '''
        Assigns control input bus to a synth parameter.
        NOTE: This method only modifies the internal state of self.
              It does not transmit any OSC messages to actually establish
              the bus/parameter connection.  
              (use LliaProxy.assign_synth_control_bus)
        
        ARGS:
          param - String, the synth parameter
          bname - String, the bus name.
          sync  - optional bool, if True notify synth editor of change

        Raises llerrors.NoSuchBusOrParameterError
        '''
        try:
            proxy = self.app.proxy
            current_bus_name = self._control_input_buses[param]
            current_bus = proxy.get_control_bus(current_bus_name)
            new_bus = proxy.get_control_bus(bname)
            current_bus.remove_sink(self.sid, param, sync=False)
            new_bus.add_sink(self.sid, param, sync=sync)
            self._control_input_buses[param] = bname
        except KeyError:
            msg = "Can not assign control input bus.  "
            msg += "sid=%s, param=%s, bus_name=%s"
            msg = msg % (self.sid, param, bname)
            raise NoSuchBusOrParameterError(msg)
        
    def disconnect_from_buses(self, sync=False):
        '''
        Notifies all buses connected to self that they are to disconnect
        from self.

        This method is called in preparation of removing self.  Once
        executed the synth should no longer be used.
        '''
        proxy = self.app.proxy
        sid = self.sid
        for bn in self._audio_output_buses.values():
            try:
                bus = proxy.get_audio_bus(bn)
                bus.remove_source(sid, None, sync=False)
                self._audio_output_buses[bn] = None
            except KeyError:
                pass
        for bn in self._audio_input_buses.values():
            try:
                bus = proxy.get_audio_bus(bn)
                bus.remove_sink(sid, None, sync=False)
                self._audio_input_buses[bn] = None
            except KeyError:
                pass
        for bn in self._control_output_buses.values():
            try:
                bus = proxy.get_control_bus(bn)
                bus.remove_source(sid, None, sync=False)
                self._control_output_buses[bn] = None
            except KeyError:
                pass
        for bn in self._control_input_buses.values():
            try:
                bus = proxy.get_control_bus(bn)
                bus.remove_sink(sid, None, sync=False)
                self._control_input_buses[bn] = None
            except KeyError:
                pass
        return True

    def midi_input_channel(self, new_channel=None):
        '''
        Retrieve/change MIDI channel number.

        ARGS:
          new_channel - optional int.  If specified change input channel
                        Channel numbers are specified indexed from 1 (1..16)
                        but are saved internally indexed from 0 (0..15).
        RETURNS: MIDI channel number (1..16)
        '''
        if new_channel is not None:
            c = int(new_channel)-1
            self._midi_chan0 = min(max(c, 0), 15)
        return self._midi_chan0+1

    def bank(self):
        '''
        RETURNS: ProgramBank
        '''
        return self._bank
    
    def current_program(self):
        '''
        RETURNS: Program, the current program.
        '''
        return self._bank[None]

    def current_performance(self):
        '''
        RETURNS: Performance, the performance portion of the current program.
        '''
        prog = self.current_program()
        return prog.performance

    def transpose(self, n=None):
        '''
        Retrieve/change transposition amount.

        ARGS:
          n - optional int, transposition in MIDI key numbers.
              If specified the transposition amount is changed.

        RETURNS: int
        '''
        prf = self.current_performance()
        if n is not None:
            prf.transpose = n
        return prf.transpose

    def key_range(self, range_=None):
        '''
        Retrieve/change active key-range.  Notes outside the key range 
        are ignored.

        ARGS:
          range_ - optional tuple (low,high) where low and high are MIDI 
                   key-numbers  0 <= low < high <= 127.

        RETURNS: tuple (or list?) 
        '''
        prf = self.current_performance()
        if range_ is not None:
            lower, upper = range_
            lower = max(int(lower), 0)
            upper = max(lower, min(int(upper), 127))
            prf.key_range((lower, upper))
        rs = prf.key_range()
        return rs

    def bend_range(self, range_=None):
        '''
        Retrieve/change bend range
        
        ARGS:
          range_ - optional int (cents).  0 <= range_ <= 2400 (2-octaves)

        RETURNS: bend range in cents.
        '''
        prf = self.current_performance()
        if range_ is not None:
            c = abs(int(range_))
            prf.bend_range = c
        return prf.bend_range

    def bend_parameter(self, new_param=None):
        '''
        Retrieve/change synth parameter used for MIDI pitch bend.
        Normally this parameter is 'detune'

        ARGS:
          new_parameter - optional String

        RETURNS: String
        '''
        prf = self.current_performance()
        if new_param is not None:
            prf.bend_parameter = new_param
        return prf.bend_parameter

    def keytable(self, tabname=None):
        '''
        Retrieve/change the key-table.   key tables map MIDI key numbers
        to frequency and are used for alternate scales.
        (See LliaApp.keytables for list of available tables)

        ARGS:
          tabname - optional String, the key-table name.  If the name is 
                    invalid the default 12-note equal tempered table "EQ12"
                    is used.

        RETURNS: String
        '''
        if tabname:
            self._key_table_name = tabname
        return self._key_table_name

    def use_program(self, slot):
        '''
        Recall indicated program.
        The following events take place:
             1) Recall the program from the program bank.
             2) Transmit OSC parameter changes to the server.
             3) If a GUI editor is present, update it.
             4) If a pretty-printer is defined and enabled, call it.

        ARGS:
          slot - int, MIDI program number, 0 <= slot <= 127
                 (If slot is 127 and a program-generator is active,
                  generate a new random program -- ISSUE: check validity 
                  of this statement)
        '''
        cp = self._bank.use(slot)
        self.x_program(cp)
        if self.synth_editor:
            self.synth_editor.sync()
        if self.app.pp_enabled:
            try:
                pp = self.specs["pretty-printer"]
                print(pp(cp, slot))
            except (TypeError, KeyError):         # ignore
                pass

    def store_program(self, slot=None):
        '''
        Stores current program to program bank.
        
        ARGS:
          slot - optional MIDI program number. If not specified
                 use the 'current' slot.

        '''
        if slot == None:
            slot = self._bank.current_slot
        prog = self.current_program()
        self._bank[slot] = prog
            
    def _get_source_mapper (self, source):
        '''
        Returns indicated SourceMapper object

        ARGS:
          source - String, one of "velocity", "aftertouch", "pitchwheel", or
                   "keynumber"

        RETURNS: SourceMapper
        '''
        perf = self.current_performance()
        try:
            sm ={"velocity" : perf.velocity_maps,
                 "aftertouch" : perf.aftertouch_maps,
                 "pitchwheel" : perf.pitchwheel_maps,
                 "keynumber" : perf.keynumber_maps}[source.lower()]
            return sm
        except KeyError:
            msg = "Invalid parameter map source: '%s'" % source
            raise KeyError(msg)

    def add_source_map(self, source, param, curve=None, modifier=None, 
                       range_=None, limits=None):
        '''
        Adds/changes source mapping.
        See also add_controller_map.

        ARGS:

           source   - String, one of "velocity", "aftertouch", pitchwheel",
                      or "keynumber"
           param    - String, the synth parameter to map source to.
           curve    - String, the mapping transfer function, one of 
                      'linear', 'exp', 's' or 'step'. Default linear
           modifier - optional value used to modify curve shape.
                      Exact usage is dependent on curve.  See llia.curves
           range_   - tuple (a,b).  Range over which to map source to.
                      if b<a, use an inverted curve.
           limits   - tuple (mn,mx) clip mapped value v to mn<=v<=max
        '''
        sm = self._get_source_mapper(source)
        if source.lower() == "keynumber":
            range_ = range_ or self.key_range()
        sm.add_parameter(param,curve,modifier, range_,limits)

    def remove_source_map(self, source, param="ALL"):
        '''
        Remove indicated source map.

        ARGS:
           source - String, one of "velocity", "aftertouch", pitchwheel",
                    or "keynumber"
           param  - String, the synth parameter to unmap.  If param is "ALL"
                    remove all mappings from source.
        '''
        sm = self._get_source_mapper(source)
        sm.remove_parameter(param)

    def add_controller_map(self, ctrl, param, curve=None, modifier=None, 
                           range_=None, limits=None):
        '''
        Adds MIDI cc mapping.

        ARGS:
          ctrl - String or int,  either MIDI controller number or assigned
                 controller name (See app.config().controller_assignments).
          param    - Same usage as with add_source_map.
          curve    - Same usage as with add_source_map.
          modifier - Same usage as with add_source_map.
          range_   - Same usage as with add_source_map.
          limits   - Same usage as with add_source_map.
        '''
        cm = self.current_performance().controller_maps
        cm.add_parameter(ctrl, param, curve, modifier, range_, limits)

    def remove_controller_map(self, ctrl, param="ALL"):
        '''
        Remove MIDI cc map.

        ARGS:
          
          ctrl  - MIDI controller number or assigned controller name.
          param - String, synth parameter.  If param is "All", remove all
                  mappings from ctrl. 
        '''
        cm = self.current_performance().controller_maps
        cm.remove_parameter(ctrl, param)
        
    def x_ping(self):
        '''
        Transmit ping message to server and wait for response.
        If no response is received in a reasonable time raise LliaPingError.
        '''
        self.osc_transmitter.x_ping()
        rs = self.app.proxy.expect_osc_response("ping-response")
        if not rs:
            msg = "Did not receive expected ping response from '/Llia/%s/%s'"
            msg = msg % (self.app.global_osc_id(), self.sid)
            raise LliaPingError(msg)
        return rs

    def x_dump(self):
        '''
        Transmit dump request to server.
        '''
        self.osc_transmitter.x_dump()
    
    def x_param_change(self, param, value):
        '''
        Transmit synth parameter change to server.
        ARGS:
          param - String
          value - number 
        '''
        self.osc_transmitter.x_synth_param(param, value)

    def x_program(self, program):
        '''
        Transmit program change to server.
        
        ARGS:
          program - an instance of Program.
        '''
        for param, val in program.items():
            if param[0] != "_":
                self.x_param_change(param, val)

    # Place holder event hadler.
    def _dummy_handler(self, msg):
        pass
                
    def _note_on_handler(self, mmsg):
        perf = self.current_performance()
        lower, upper = perf.key_range()
        chan = mmsg.channel
        keynumber = mmsg.note
        v127 = mmsg.velocity
        if chan == self._midi_chan0 and lower <= keynumber <= upper:
            keynumber_t = min(max(keynumber+perf.transpose, 0), 127)
            if v127 == 0:
                self.osc_transmitter.x_note_off(keynumber_t)
            else:
                vnorm = v127/127.0
                freq = self.app.keytables[self._key_table_name][keynumber_t]
                perf.velocity_maps.update_synths(v127, self)
                perf.keynumber_maps.update_synths(keynumber, self)
                self.osc_transmitter.x_note_on(keynumber_t, freq, vnorm)

    def _note_off_handler(self, mmsg):
        perf = self.current_performance()
        if mmsg.channel == self._midi_chan0:
            lower, upper = perf.key_range()
            keynumber = mmsg.note
            if lower <= keynumber <= upper:
                kn = min(max(keynumber+perf.transpose, 0), 127)
                self.osc_transmitter.x_note_off(kn)
                
    def _aftertouch_handler(self, mmsg):
        if mmsg.channel == self._midi_chan0:
            perf = self.current_performance()
            perf.aftertouch_maps.update_synths(mmsg.value, self)
    
    def _pitchwheel_handler(self, mmsg):
        if mmsg.channel == self._midi_chan0:
            perf = self.current_performance()
            pos = mmsg.pitch
            norm = pos*BEND_SCALE + BEND_BIAS
            perf.pitchwheel_maps.update_synths(pos, self)
            param = perf.bend_parameter
            s = con.RCENT**perf.bend_range
            self.x_param_change(param, s**norm)

    def _cc_handler(self, mmsg):
        if mmsg.channel == self._midi_chan0:
            perf = self.current_performance()
            ctrl = mmsg.control
            pos = mmsg.value
            perf.controller_maps.update_synths(ctrl, pos, self)

    def _program_change_handler(self, mmsg):
        if mmsg.channel == self._midi_chan0:
            self.use_program(mmsg.program)            
                
    def dump(self):
        pad = " "*4
        program = self._bank[None]
        acc = "SynthProxy: sid = '%s'\n" % self.sid
        acc += "%sMIDI input channel : %2d" % (pad, self.midi_input_channel())
        acc += "%sKeytable           : %s" % (pad, self._key_table_name)
        acc += self._bank.dump(1)
        acc += program.dump(1)
        return acc
    
    def random_program(self, slot=127, *args):
        '''
        Generate random program if a generator is defined.
        Store results to indicated slot of the program bank.

        ARGS:
          slot  - int MIDI program number, 
          *args - optional arguments to pass to random-generator, 
                  currently not used.

        RETURNS: Program or None
        '''
        genfn = self.specs["program-generator"]
        if genfn:
            args = [slot] + list(args)
            prog = genfn(*args)
            return prog
        else:
            msg = "No generator defined for %s" % self.specs["format"]
            self.status(msg)
            return None

    def __str__(self):
        pad = " "*4
        if self.is_controller:
            acc = "Controller"
        elif self.is_efx:
            acc = "Effect"
        else:
            acc = "Synth"
        bnk = self._bank
        prog = self.bank()[None]
        perf = prog.performance
        acc += "  SID %s\n" % self.sid
        acc += "MIDI channel %d\n" % self.midi_input_channel()
        acc += "Key mode  %s   voice count = %s\n" % (self.keymode, self.voice_count)
        acc += "Key table %s\n" % self.keytable()
        acc += 'Program [%s] "%s"\n' % (bnk.current_slot, prog.name)
        acc += "Transpose %d\n" % perf.transpose
        acc += "Key range %s\n" % str(perf.key_range())
        return acc

    @staticmethod
    def tabula_rasa():
        SynthProxy._synth_serial_number = 0
        
        
