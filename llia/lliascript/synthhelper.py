# llia.lliascript.synthhelper
# 2016.05.15
# Extends Parser with synth related commands
#

from __future__ import print_function

from llia.lliascript.ls_constants import *
from llia.llerrors import LliascriptError, NoSuchSynthError, NoSuchBufferError


class SynthHelper(object):

   
    def __init__(self,parser,local_namespace):
        self.parser = parser
        self.proxy = parser.proxy
        self.config = self.proxy.config
        self.current_sid = ""
        self._init_namespace(local_namespace)

    def _init_namespace(self, ns):
        ns["assign_abus"] = self.assign_abus
        ns["assign_cbus"] = self.assign_cbus
        ns["assign_buffer"] = self.assign_buffer
        ns["assign"] = self.assign_buffer_or_bus
        ns["bend"] = self.bend
        ns["efx"] = self.add_efx
        ns["input_channel"] = self.input_channel
        ns["keyrange"] = self.keyrange
        ns["ping_synth"] = self.ping_synth
        ns["synth"] = self.add_synth
        ns["transpose"] = self.transpose
        ns["with_synth"] = self.with_synth
        #ns["dump_synth"] = self.dump_synth
        #ns["mapsrc"] = self.mapsrc
        ns["cc"] = self.map_cc
        #ns["rm_synth"] = self.rm_synth
        
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
          
    def add_synth(self, stype, id_, keymode="Poly1", voice_count=8):
        sid = "%s_%s" % (stype, id_)
        if self.synth_exists(sid):
            self.with_synth(sid)
            return True
        else:
            self.assert_synth_type(stype)
            self.assert_keymode(keymode)
            rs = self.proxy.add_synth(stype, id_, keymode, voice_count)
            self.parser.register_entity(sid, "synth")
            if rs:
                self.current_sid = sid
                self.update_prompt()
            return rs

    def add_efx(self, stype, id_):
        sid = "%s_%s" % (stype, id_)
        if self.synth_exists(sid):
            self.with_synth(sid)
            return True
        else:
            self.assert_efx_type(stype)
            rs = self.proxy.add_efx(stype, id_)
            self.parser.register_entity(sid, "synth")
            if rs:
                self.current_sid = sid
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
    
    # def mapsrc(self, source, param, curve=linear, mod=None,
    #            range_=(0.0, 1.0), limits=None, sid=None):
    #     self._assert_map_curve(curve)
    #     limits = limits or range_
    #     if not mod:
    #         if curve == step:
    #             mod = 8
    #         else:
    #             mod = 1
    #     sy = self.get_synth(sid)
    #     if self.parser.is_controller(source):
    #         sy.add_controller_map(source,param,curve,mod,range_,limits)
    #         return True
    #     elif source in (velocity, aftertouch, keynumber, pitchwheel):
    #         sy.add_source_map(source,param,curve,mod,range_,limits)
    #         return True
    #     else:
    #         msg = "Expected map_ source to be velocity, aftertouch, \n"
    #         msg += "keynumber, pitchwheel or a MIDI controller.\n"
    #         msg += "Encountered: %s"
    #         msg = msg % source
    #         raise LliascriptError(msg)

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

    def remove_synth(self, sid):
        if sid == self.current_sid:
            msg = "Can not free surrent synth: '%s'" % self.current_sid
            raise LliascriptError(msg)
        self.get_synth(sid)
        stype, id_ = self.parse_sid(sid)
        self.proxy.free_synth(stype, id_)
        self.status("Rmoved synth: '%s'" % sid)
        return True
        
    def dump_synth(self, sid=None):
        sy = self.get_synth(sid)
        sy.x_dump()
        print(sy._bank.current_program.dump(1))
        stype, id_ = self.parse_sid(sid)
        self.proxy.free_synth(stype, id_)
