# llia.synth_proxy
# 2016.04.23

from __future__ import print_function

import llia.constants as con
import llia.curves as curves
from llia.llerrors import LliaPingError
from llia.generic import is_instrument, clone, dump
from llia.osc_transmitter import OSCTransmitter

#  ---------------------------------------------------------------------- 
#                               SynthSpecs class

class SynthSpecs(dict):

    global_synth_type_registry = {}
    # synth_counter = {}

    @staticmethod
    def available_synth_types():
        k = SynthSpecs.global_synth_type_registry.keys()
        k.sort()
        return k

    @staticmethod
    def is_known_synth_type(stype):
        return SynthSpecs.global_synth_type_registry.has_key(stype)
    
    # @staticmethod
    # def create_id(ss):
    #     format_ = ss["format"]
    #     count = SynthSpecs.synth_counter.get(format_, 1)
    #     SynthSpecs.synth_counter[format_] = count+1
    #     return count

    @staticmethod
    def create_synth_proxy(app, stype, id_):
        try:
            specs = SynthSpecs.global_synth_type_registry[stype]
            # id_ = id_ or SynthSpecs.create_id(stype)
            cfn = specs["constructor"]
            syproxy = cfn(app, id_)
            return syproxy
        except KeyError:
            return None
    
    def __init__(self, format_):
        super(SynthSpecs, self).__init__()
        super(SynthSpecs, self).__setitem__("format", format_)
        super(SynthSpecs, self).__setitem__("constructor", None)
        super(SynthSpecs, self).__setitem__("description", None)
        super(SynthSpecs, self).__setitem__("program-generator", None)
        super(SynthSpecs, self).__setitem__("pretty-printer", None)
        super(SynthSpecs, self).__setitem__("help", None)
        super(SynthSpecs, self).__setitem__("notes", None)
        SynthSpecs.global_synth_type_registry[format_] = self
        
    def __setitem__(self, key, item):
        if self.has_key(key):
            super(SynthSpecs, self).__setitem__(key, item)
        else:
            msg = "Illegal SynthSpecs key: '%s'" % key
            raise KeyError(msg)

    def create_proxy_synth(self, app):
        cfn = self["constructor"]
        id_ = SynthSpecs.create_id(self)
        return cfn(app, id_)

#  ---------------------------------------------------------------------- 
#                              SynthProxy class
    
BEND_SCALE, BEND_BIAS = curves.linear_coefficients(con.PITCHWHEEL_DOMAIN,
                                                   con.BIPOLAR_RANGE)
        
class SynthProxy(object):

    def __init__(self, app, specs, id_, bank):
        super(SynthProxy, self).__init__()
        self.is_efx = False
        self.id_ = id_
        self.app = app
        self.specs = specs
        self.synth_format = specs["format"]
        self.sid = "%s_%d" % (self.synth_format, self.id_)
        global_oscid = app.proxy.global_osc_id()
        self.oscID = "%s/%s/%s" % (global_oscid,self.synth_format, id_)
        self._bank = bank.clone()
        self._midi_chan0 = 0
        self._key_table_name = "EQ12"
        host_and_port = app.config.host_and_port()
        host_and_port = host_and_port[0], int(host_and_port[1])
        trace_osc = app.config.osc_transmission_trace_enabled()
        self._osc_transmitter = OSCTransmitter(self.oscID, host_and_port, trace_osc)
        def register_midi_handler(event, hfn, fid=""):
            fid = "%s%s.%s" % (fid, self.oscID, event)
            app.midi_receiver.register_handler(event, fid, hfn)
        register_midi_handler("note_on", self._note_on_handler)
        register_midi_handler("note_off", self._note_off_handler)
        register_midi_handler("aftertouch", self._aftertouch_handler)
        register_midi_handler("pitchwheel", self._pitchwheel_handler)
        register_midi_handler("control_change", self._cc_handler)
        register_midi_handler("program_change", self._program_change_handler)
        if app.config.keyswitch_enabled():
            self._keyswitch_chan0 = app.config.keyswitch_channel()-1
            self._keyswitch_transpose = app.config.keyswitch_transpose()
            register_midi_handler("note_on", self._keyswitch_handler, "keyswitch.")

    # Free instrument
    # Return bool True if all goes well.
    #
    def free(self):   # ISSUE: FIX ME
        return True

    def midi_input_channel(self, new_channel=None):
        if new_channel is not None:
            c = int(new_channel)-1
            self._midi_chan0 = min(max(c, 0), 15)
        return self._midi_chan0

    def current_program(self):
        return self._bank[None]

    def current_performance(self):
        prog = self.current_program()
        return prog.performance

    def transpose(self, n=None):
        prf = self.current_performance()
        if n is not None:
            prf.transpose = n
        return prf

    def key_range(self, range_=None):
        prf = self.current_performance()
        if range_ is not None:
            lower, upper = range_
            lower = max(int(lower), 0)
            upper = max(lower, min(int(upper), 127))
            prf.key_range((lower, upper))
        rs = prf.key_range()
        return rs

    def bend_range(self, range_=None):
        prf = self.current_performance()
        if range_ is not None:
            c = abs(int(range_))
            prf.bend_range = c
        return prf.bend_range

    def bend_parameter(self, new_param=None):
        prf = self.current_performance()
        if new_param is not None:
            prf.bend_parameter = new_param
        return prf.bend_parameter

    def use_program(self, slot):
        cp = self._bank.use(slot)
        self.x_program(cp)
        # ISSUE: Fix me
        ## call sync_ui on gui window
        if self.app.config.program_pp_enabled():
            try:
                pp = self.specs["pretty-printer"]
                print(pp(cp, slot))
            except TypeError:         # ignore
                pass

    def store_program(self, slot=None):
        if slot == None:
            slot = self._bank.current_slot
        prog = self.current_program()
        self._bank[slot] = prog
            
    def _get_source_mapper (self, source):
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

    def add_source_map(self, source, param, curve=None, modifier=None, range_=None, limits=None):
        sm = self._get_source_mapper(source)
        if source.lower() == "keynumber":
            range_ = range_ or self.key_range()
        sm.add_parameter(param,curve,modifier, range_,limits)

    def remove_source_map(self, source, param="ALL"):
        sm = self._get_source_mapper(source)
        sm.remove_parameter(param)

    def add_controller_map(self, ctrl, param,curve=None, modifier=None, range_=None, limits=None):
        cm = self.current_performance().controller_maps
        cm.add_parameter(ctrl, param, curve, modifier, range_, limits)

    def remove_controller_map(self, ctrl, param="ALL"):
        cm = self.current_performance().controller_maps
        cm.remove_parameter(ctrl, param)

        
    def x_ping(self):
        self._osc_transmitter.x_ping()
        rs = self.app.proxy.expect_osc_response("ping-response")
        if not rs:
            #sid = "%s_%d" % (self.synth_format, self.id_)
            msg = "Did not receive expected ping responce from '/Llia/%s/%s'"
            msg = msg % (self.app.global_osc_id(), self.sid)
            raise LliaPingError(msg)
        return rs

    def x_dump(self):
        self._osc_transmitter.x_dump()
    
    def x_param_change(self, param, value):
        self._osc_transmitter.x_synth_param(param, value)

    def x_program(self, program):
        for param, val in program.items():
            if param[0] != "_":
                self.x_param_change(param, val)
    
    def _note_on_handler(self, mmsg):
        perf = self.current_performance()
        lower, upper = perf.key_range()
        chan = mmsg.channel
        keynumber = mmsg.note
        v127 = mmsg.velocity
        if chan == self._midi_chan0 and lower <= keynumber <= upper:
            keynumber_t = min(max(keynumber+perf.transpose, 0), 127)
            if v127 == 0:
                self._osc_transmitter.x_note_off(keynumber_t)
            else:
                vnorm = v127/127.0
                freq = self.app.keytables[self._key_table_name][keynumber_t]
                perf.velocity_maps.update_synths(v127, self)
                perf.keynumber_maps.update_synths(keynumber, self)
                self._osc_transmitter.x_note_on(keynumber_t, freq, vnorm)

    def _note_off_handler(self, mmsg):
        perf = self.current_performance()
        if mmsg.channel == self._midi_chan0:
            lower, upper = perf.key_range()
            keynumber = mmsg.note
            if lower <= keynumber <= upper:
                kn = min(max(keynumber+perf.transpose, 0), 127)
                self._osc_transmitter.x_note_off(kn)
                
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
    
    def _keyswitch_handler(self, mmsg):
        if mmsg.channel == self._keyswitch_chan0:
            v127 = mmsg.velocity
            if v127 != 0:
                slot = mmsg.note+self._keyswitch_transpose
                slot = min(max(slot, 0), 127)
                self.use_program(slot)
                
    def dump(self):
        print("ISSUE: FIX ME SynthProxy.dump")
        
            
