# llia.lliascript.synthhelper
# 2016.05.15
# Extends Parser with synth related commands
#

from __future__ import print_function

from llia.generic import is_list
from llia.llerrors import LliascriptError, NoSuchSynthError, NoSuchBufferError
from llia.lliascript.ls_constants import *



class SynthHelper(object):

   
    def __init__(self,parser,local_namespace):
        self._synth_serial_number = 0
        self.parser = parser
        self.proxy = parser.proxy
        self.config = self.proxy.config
        self.current_sid = ""
        self._init_namespace(local_namespace)
        self._assignment_serial_number = 0

    def _init_namespace(self, ns):
        ns["assign"] = self.assign_buffer_or_bus
        ns["bend"] = self.bend
        ns["efx"] = self.add_efx
        ns["input_channel"] = self.input_channel
        ns["keyrange"] = self.keyrange
        ns["synth"] = self.add_synth
        ns["transpose"] = self.transpose
        ns["with_synth"] = self.with_synth
        ns["pmap"] = self.parameter_map
        
    def warning(self, msg):
        self.parser.warning(msg)

    def status(self, msg):
        self.parser.status(msg)
        
    def update_prompt(self):
        pass

    def what_is(self, name):
        return self.parser.what_is(name)
        
    def synth_exists(self, sid=None):
        sid = sid or self.current_synth
        return self.proxy.synth_exists(None, None, sid)

    def get_synth(self, sid=None):
        if sid == "*":
            sid = self.current_sid
        else:
            sid = sid or self.current_sid
        try:
            sy = self.proxy.get_synth(sid)
            return sy
        except KeyError:
          raise NoSuchSynthError(sid)

    def with_synth(self, sid):
        self.get_synth(sid)
        self.current_sid = sid
        msg = "Using synth: %s" % sid
        self.status(msg)
        return True
        
    @staticmethod
    def assert_synth_type(stype):
        if stype not in SYNTH_TYPES:
            msg = "Invalid synthtype: '%s'" % stype
            raise LliascriptError(msg)

    @staticmethod
    def assert_efx_type(stype):
        if stype not in EFFECT_TYPES:
            msg = "Invalid EFX synthtype: '%s'" % stype
            raise LliascriptError(msg)
        
    @staticmethod
    def assert_keymode(kmode):
        if kmode not in KEY_MODES:
            msg = "Invalid keymode: '%s'" % kmode
            raise LliascriptError(msg)

    # Split synth_Id string in form "stype_n" into components (stype, n)
    # 
    def parse_sid(self, sid=None):
        sid = sid or self.current_sid
        pos = sid.rfind('_')
        if pos > -1:
            head, tail  = sid[:pos], sid[pos+1]
        else:
            head, tail = sid, ""
        return (head, tail)
        
    def assign_abus(self, param, busname, offset=0, sid=None):
        sid = sid or self.current_sid
        self.get_synth(sid)
        lstype = self.what_is(busname)
        if lstype == '':
              msg = "Audio bus '%s' does not exists." % busname
              self.warning(msg)
              return False
        if lstype == "abus":
            stype, id_ = self.parse_sid(sid)
            if self.proxy.audio_bus_exists(busname):
                self.proxy.assign_synth_audio_bus(stype, id_, param, busname, offset)
                ename = "assign-audio-bus-%d" % self._assignment_serial_number
                etype = "audio-bus-assignment"
                data = {"param" : param,
                        "bus-name" : busname,
                        "offset" : offset,
                        "sid" : sid}
                self.parser.register_entity(ename, etype, data)
                self._assignment_serial_number += 1
                return True
            else:
                msg = "Can not assign audio bus: '%s'." % busname
                self.warning(msg)
                return False
        else:
            msg = "Can not assign %s '%s' as audio bus." % (lstype, busname)
            self.warning(msg)
            return False

    def assign_cbus(self, param, busname, offset=0, sid=None):
        sid = sid or self.current_sid
        self.get_synth(sid)
        lstype = self.what_is(busname)
        if lstype == '':
              msg = "Control bus '%s' does not exists." % busname
              self.warning(msg)
              return False
        if lstype == "cbus":
            stype, id_ = self.parse_sid(sid)
            if self.proxy.control_bus_exists(busname):
                self.proxy.assign_synth_control_bus(stype, id_, param, busname, offset)
                ename = "assign-control-bus-%d" % self._assignment_serial_number
                etype = "control-bus-assignment"
                data = {"param" : param,
                        "bus-name" : busname,
                        "offset" : offset,
                        "sid" : sid}
                self.parser.register_entity(ename, etype, data)
                self._assignment_serial_number += 1
                return True
            else:
                msg = "Can not assign control bus: '%s'.  (See BUG 0000)" % busname
                self.warning(msg)
                return False
        else:
            msg = "Can not assign %s '%s' as control bus." % (lstype, busname)
            self.warning(msg)
            return False

    def assign_buffer(self, param, name=None, sid=None):
        sid = sid or self.current_sid
        self.get_synth(sid)
        name = name or self.parser.bufferhelper.current_buffer
        lstype = self.what_is(name)
        if lstype == '':
            msg = "Buffer '%s' does not exist." % name
            raise NoSuchBufferError(msg)
        elif lstype != "buffer":
            msg = "Can not use %s '%s' as buffer." % (lstype, name)
            raise NoSuchBufferError(msg)
        else:
          stype, id_ = self.parse_sid(sid)
          self.proxy.assign_synth_buffer(stype, id_, param, name)
          ename = "buffer-assignment-%d" % self._assignment_serial_number
          etype = "buffer-assignment"
          data = {"param" : param,
                  "buffer-name" : name,
                  "sid" : sid}
          self.parser.register_entity(ename, etype, data)
          self._assignment_serial_number += 1
          

    def assign_buffer_or_bus(self, param, name="", offset=0, sid=None):
        if not name:
            return self.assign_buffer(param, name, sid)
        lstype = self.what_is(name)
        if lstype == "abus":
            self.assign_abus(param, name, offset, sid)
        elif lstype == "cbus":
            self.assign_cbus(param, name, offset, sid)
        elif lstype == "buffer":
            self.assign_buffer(param, name, sid)
        else:
            msg = "Can not assign %s %s to %s %s"
            msg = msg % (lstype, name, sid, param)
            raise LliascriptError(msg)


    # Fill in default values for synth outbus argument
    # obarg may be:  None
    #             :  A single String bus name
    #             :  list or tuple
    # The result is a list [bus-name, synth-parameter, bus-offset]
    #
    @staticmethod
    def fill_outbus_args(obarg):
        if not obarg: obarg = ["out_0"]
        if not is_list(obarg): obarg = [obarg]
        obarg = list(obarg)
        if len(obarg) == 0:
            return ["out_0", "outbus", 0]
        if len(obarg) == 1:
            return obarg + ["outbus", 0]
        if len(obarg) == 2:
            return obarg + [0]
        else:
            return obarg

    # outbus as list [bus-name, param, offset]
    def add_synth(self, stype, id_, keymode="Poly1", voice_count=8, outbus=["out_0", "outbus", 0]):
        
        sid = "%s_%s" % (stype, id_)
        if self.synth_exists(sid):
            self.with_synth(sid)
            return True
        else:
            self.assert_synth_type(stype)
            self.assert_keymode(keymode)
            rs = self.proxy.add_synth(stype, id_, keymode, voice_count)
            self.parser.register_entity(sid, "synth",
                                        {"serial-number" : self._synth_serial_number,
                                         "stype" : stype,
                                         "id" : id_,
                                         "keymode" : keymode,
                                         "voice-count" : voice_count,
                                         "outbus" : outbus,
                                         "is-efx" : False})
            self._synth_serial_number += 1
            if rs:
                self.current_sid = sid
                bname,param,offset = self.fill_outbus_args(outbus)
                self.assign_abus(param, bname, offset)
                self.update_prompt()
            return rs

    def add_efx(self, stype, id_, outbus=["out_0", "outbus", 0]):
        sid = "%s_%s" % (stype, id_)
        if self.synth_exists(sid):
            self.with_synth(sid)
            return True
        else:
            self.assert_efx_type(stype)
            rs = self.proxy.add_efx(stype, id_)
            self.parser.register_entity(sid, "synth",
                                        {"serial-number" : self._synth_serial_number,
                                         "stype" : stype,
                                         "id" : id_,
                                         "outbus" : outbus,
                                         "is-efx" : True})
            self._synth_serial_number += 1
            if rs:
                self.current_sid = sid
                bname,param,offset = self.fill_outbus_args(outbus)
                self.assign_abus(param, bname, offset)
                self.update_prompt()
            return rs
                
    def input_channel(self, chan=None, sid=None):
        sy = self.get_synth(sid)
        chan_number = None
        if not chan:
            chan_number = sy.midi_input_channel()
        else:
            chan_number = self.config.channel_assignments.get_channel(chan)
            chan_number = sy.midi_input_channel(chan_number)
        msg = "Synth %s MIDI input channel:  %s   '%s'" % (sid, chan_number, chan)
        self.status(msg)
        return chan_number

    def keyrange(self, lower=None, upper=None, sid=None):
        sy = self.get_synth(sid)
        if lower or lower == 0:
            range_ = (lower, upper or 127)
            sy.key_range(range_)
        kr = sy.key_range()
        msg = "Synth %s keyrange: %s" % (sid, kr)
        self.status(msg)
        return kr
    
    def bend(self, range_=None, param=None, sid=None):
        sy = self.get_synth(sid)
        a = sy.bend_range(range_)
        b = sy.bend_parameter(param)
        msg = "%s bend range: %d cents,  parameter: '%s'"
        msg = msg % (sid, a,b)
        self.status(msg)
        return (a, b)

    def transpose(self, n=None, sid=None):
        sy = self.get_synth(sid)
        x = sy.transpose(n)
        msg = "%s transpose: %s" % (sid, x)
        self.status(msg)
        return x

    def ping_synth(self, sid=None):
        if sid == "*": sid = None
        sy = self.get_synth(sid)
        sy.x_ping()
        return True

    @staticmethod
    def _assert_map_curve(curve):
        if curve in curves:
            return True
        else:
            msg = "Expected one of the following for map_ curve argument:\n"
            msg += "linear, exp, scurve or step.  Encounterd: %s"
            msg = msg % curve
            raise LliascriptError(msg)

    def _assert_map_args(self, curve, mod, range_, limits, sid):
        self._assert_map_curve(curve)
        range_ = range_ or (0.0, 1.0)
        limits = limits or range_
        if not mod:
            if mod == step:
                mod = 8
            else:
                mod = 1
        sy = self.get_synth(sid)
        return (curve, mod, range_, limits, sy)

    def map_cc(self, ctrl, param, curve=linear, mod=None, range_=None, limits=None,sid=None):
        curve,mod,range_,limits,sy = self._assert_map_args(curve,mod,range_,limits,sid)
        source = self.config.controller_assignments.get_controller_number(ctrl)
        sy.add_controller_map(source,param,curve,mod,range_,limits)
        return True

    def map_velocity(self, param, curve=linear, mod=None, range_=None, limits=None, sid=None):
        curve,mod,range_,limits,sy = self._assert_map_args(curve,mod,range_,limits,sid)
        sy.add_source_map("velocity", param, curve, mod, range_, limits)
        return True

    def map_aftertouch(self, param, curve=linear, mod=None, range_=None, limits=None, sid=None):
        curve,mod,range_,limits,sy = self._assert_map_args(curve,mod,range_,limits,sid)
        sy.add_source_map("aftertouch", param, curve, mod, range_, limits)
        return True

    def map_pitchwheel(self, param, curve=linear, mod=None, range_=None, limits=None, sid=None):
        curve,mod,range_,limits,sy = self._assert_map_args(curve,mod,range_,limits,sid)
        sy.add_source_map("pitchwheel", param, curve, mod, range_, limits)
        return True

    def map_keynumber(self, param, curve=linear, mod=None, range_=None, limits=None, sid=None):
        curve,mod,range_,limits,sy = self._assert_map_args(curve,mod,range_,limits,sid)
        sy.add_source_map("keynumber", param, curve, mod, range_, limits)
        return True

    def parameter_map(self, source, param, curve=linear, mod=None, range_=None, limits=None, sid=None):
        lstype = self.what_is(source)
        if "controller" in lstype:
            self.map_cc(source, param, curve, mod, range_, limits, sid)
        elif source == velocity:
            self.map_velocity(param, curve, mod, range_, limits, sid)
        elif source == aftertouch:
            self.map_aftertouch(param, curve, mod, range_, limits, sid)
        elif source == pitchwheel:
            self.map_pitchwheel(param, curve, mod, range_, limits, sid)
        elif source == keynumber:
            self.map_keynumber(param, curve, mod, range_, limits, sid)
        else:
            msg = "Do not understand parameter map source: '%s'" % source
            raise LliascriptError(msg)

    def remove_parameter_map(self, source, param=ALL, sid=None):
        if sid == "*" : sid = None
        sy = self.get_synth(sid)
        lstype = self.what_is(source)
        if "controller" in lstype:
            cca = self.config.controller_assignments
            ctrl = cca.get_controller_number(source)
            sy.remove_controller_map(ctrl, param)
        elif source in (velocity, aftertouch, keynumber, pitchwheel):
            sy.remove_source_map(source, param)
        else:
            msg = "Do not understand remove parameter map source: '%s'" % source
            raise LliascriptError(msg)
        
    def remove_synth(self, sid):
        if sid == self.current_sid:
            msg = "Can not free current synth: '%s'" % self.current_sid
            raise LliascriptError(msg)
        self.get_synth(sid)
        stype, id_ = self.parse_sid(sid)
        self.proxy.free_synth(stype, id_)
        self.parser.forget(sid)
        self.status("Removed synth: '%s'" % sid)
        return True
        
    def dump_synth(self, sid=None):
        if sid == "*": sid = None # Force current sid
        sy = self.get_synth(sid)
        sy.x_dump()
        print(sy._bank.current_program.dump(1))
        stype, id_ = self.parse_sid(sid)
        self.proxy.free_synth(stype, id_)
