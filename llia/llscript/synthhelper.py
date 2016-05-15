# llia.llscript.synthhelper
# 2016.05.10
#

from __future__ import print_function

import llia.constants as con
from llia.llerrors import LliascriptParseError
from llia.llscript.lsutil import (parse_positional_args, parse_keyword_args)

class SynthHelper(object):

    def __init__(self, parser):
        self.parser = parser
        self.dispatch_table = parser.dispatch_table
        self.proxy = parser.proxy
        self.config = self.proxy.config
        self._init_dispatch_table()
        self.current_sid = ""

    def _init_dispatch_table(self):
        self.dispatch_table["assign"] = self.assign_buffer_or_bus
        self.dispatch_table["bend"] = self.bend
        self.dispatch_table["channel"] = self.set_midi_input_channel
        self.dispatch_table["efx"] = self.add_efx
        self.dispatch_table["keyrange"] = self.keyrange
        self.dispatch_table["keytable"] = self.keytable
        self.dispatch_table["ping-synth"] = self.ping_synth
        self.dispatch_table["synth"] = self.add_synth
        self.dispatch_table["transpose"] = self.transpose
        self.dispatch_table["with-synth"] = self.with_synth
        
    def status(self, msg):
        self.parser.status(msg)

    def warning(self, msg):
        self.parser.warning(msg)
        
    def update_prompt(self):
        self.parser.update_prompt()

    def assert_current_synth(self):
        if not self.current_sid:
            msg = "No current synth selected."
            self.warning(msg)
            return False
        else:
            return True

    def get_current_synth(self):
        if self.assert_current_synth():
            return self.proxy.get_synth(self.current_sid)
        else:
            return None
        
        
    # Split synth_Id string in form "stype_n" into components (stype, n)
    # 
    def parse_sid(self, sid=None):
        sid = sid or self.current_sid
        pos = sid.rfind('_')
        if pos > -1:
            haed, tail = sid[:pos], sid[pos+1:]
        else:
            head, tail = sid, ""
        return (head, tail)

    def get_synth(self, sid=None):
        sid = sid or self.current_sid
        rs = self.proxy.get_synth(sid or self.current_sid)
        return rs
    
    def synth_exists(self, sid):
        return self.proxy.synth_exists(nil, nil, sid)
    
    def audio_bus_exists(self, bname):
        return self.proxy.audio_bus_exists(bname)

    def control_bus_exists(self, bname):
        return self.proxy.control_bus_exists(bname)
        
    def buffer_exists(self, bname):
        return self.proxy.buffer_exists(bname)

    
    # synth stype id_ [:keymode km][:voice-count vc]
    #                 [:outbus busName][:outbus-offset n][:outbus-param param]
    def add_synth(self, tokens):
        args = parse_keyword_args(tokens,
                                  ["str", "str", "int"],
                                  [":keymode", ":voice-count",
                                   ":outbus", ":outbus-offset",
                                   ":outbus-param"],
                                  {":keymode" : ["str", "Poly1"],
                                   ":voice-count" : ["int", 8],
                                   ":outbus" : ["str", "out_0"],
                                   ":outbus-offset" : ["int", 0],
                                   ":outbus-param" : ["str", "outbus"]})
        cmd, stype, id_, keymode, voice_count, obusName, obusOffset, obusParam = args
        sid = "%s_%d" % (stype, id_)
        if stype not in con.SYNTH_TYPES:
            msg = "Unknown synth type: '%s'" % stype
            self.warning(msg)
            return False
        if keymode not in con.KEY_MODES:
            msg = "Invalid keymode: '%s'" % keymode
            self.warning(msg)
            return False
        if self.proxy.synth_exists(stype, id_):
            # msg = "Synth %s already exists" % sid
            # self.warning(msg)
            self.with_synth(["", stype, id_])
            return True
        if not self.proxy.audio_bus_exists(obusName):
            msg = "Audio bus '%s' does not exists" % obusName
            self.warning(msg)
            return False
        rs = self.proxy.add_synth(stype, id_, keymode, voice_count)
        if rs:
            self.proxy.assign_synth_audio_bus(stype, id_, obusParam, obusName, obusOffset)
            self.current_sid = sid
            self.update_prompt()
        return rs
    
    # efx stype id_ inbus [:outbus name][:outbus-offset n][:outbus-param p]
    #                     [:inbus-offset n][:inbus-param p]
    def add_efx(self, tokens):
        req_args = ["str", "str", "int", "str"]
        key_arg_order =  [":outbus", ":outbus-offset",":outbus-param", 
                          ":inbus-offset",":inbus-param"]
        key_args = {":outbus" : ["str", "out_0"],
                    ":outbus-offset" : ["int", 0],
                    ":outbus-param" : ["str", "outbus"],
                    ":inbus-offset" : ["int", 0],
                    ":inbus-param" : ["str", "inbus"]}
        args = parse_keyword_args(tokens,
                                             req_args,
                                             key_arg_order,
                                             key_args)
        cmd, stype, id_, ibs, obs, oboff, obprm, iboff, ibprm = args
        sid = "%s_%d" % (stype, id_)
        if stype not in con.EFFECT_TYPES:
            msg = "Unknown EFX synth type: '%s'" % stype
            self.warning(msg)
            return False
        if self.proxy.synth_exists(stype, id_):
            msg = "Synth %s already exists" % sid
            self.warning(msg)
            return False
        for bs in (obs, ibs):
            if not self.proxy.audio_bus_exists(bs):
                msg = "Audio bus '%s' does not exists" % bs
                self.warning(msg)
                return False
        rs = self.proxy.add_efx(stype, id_)
        if rs:
            self.proxy.assign_synth_audio_bus(stype, id_, obprm, obs, oboff)
            self.proxy.assign_synth_audio_bus(stype, id_, ibprm, ibs, iboff)
            self.current_sid = sid
            self.update_prompt()
        return rs

    # with stype id_
    # Select synth for editing.
    #
    def with_synth(self, tokens):
        args = parse_positional_args(tokens,["str", "str", "int"])
        cmd, stype, id_ = args
        sid = "%s_%d" % (stype, id_)
        if self.proxy.synth_exists(stype, id_):
            self.current_sid = sid
            msg = "Using synth '%s'" % sid
            self.status(msg)
            self.update_prompt()
            return True
        else:
            msg = "Synth '%s' does not exists" % sid
            self.warning(msg)
            return False

    def ping_synth(self, *_):
        if self.assert_current_synth():
            sp = self.get_synth()
            if sp:
                sp.x_ping()
                return True
            else:
                return False
        else:
            return False
        
    def dump_synth(self, *_):
        rs = self.ping_synth()
        if rs:
            sp = self.get_synth()
            sp.x_dump()
            sp.dump()
        return rs

    # assign <what> <name> to <param> [:offset]
    # <what> is 'abus', 'cbus' or 'buffer
    # <name> is name of buffer or bus
    # 'to' is literal
    # <param> is current synth parameter
    #  
    def assign_buffer_or_bus(self, tokens):
        if self.assert_current_synth():
            sp = self.get_synth()
            stype, id_ = sp.synth_format, sp.id_
            req = ["str", "str", "str", "str", "str"]
            pos = [":offset"]
            kw = {":offset" : ["int", 0]}
            args = parse_keyword_args(tokens, req, pos, kw)
            cmd, entity, name, to, param, offset = args
            entity = entity.lower()
            if to.upper() != "TO":
                msg = "Expected literal word 'to', encountered '%s'" % to
                self.warning(msg)
                return False
            if entity == "abus":
                if self.proxy.audio_bus_exists(name):
                    self.proxy.assign_synth_audio_bus(stype, id_, param, name, offset)
                    return True
                else:
                    msg = "Audio bus '%s' does not exists." % name
                    self.warning(msg)
                    return False
            elif entity == "cbus":
                if self.proxy.control_bus_exists(name):
                    self.proxy.assign_synth_control_bus(stype, id_, param, name, offset)
                    return True
                else:
                    msg = "Control bus '%s' does not exists." % name
                    self.warning(msg)
                    return False
            elif entity == "buffer":
                if self.parser.buffer_helper.buffer_exists(name):
                    self.proxy.assign_synth_buffer(stype, id_, param, name)
                    return True
                else:
                    msg = "Buffer '%s' does not exists." % name
                    self.warning(msg)
                    return False
            else:
                self.warning("Invalid first argument.")
                self.warning("Expected either 'abus', 'cbus' or 'buffer'.")
                self.warning("Encountered '%s'" % entity)
                return False
        else:
            return False

    # cmd [channel]
    # Set and display MIDI input chanel of current synth
    # channel either int, channel alias, or nil
    #
    def set_midi_input_channel(self, tokens):
        sy = self.get_current_synth()
        if sy:
            args = parse_positional_args(tokens, ["str"],[["str",""]])
            cmd, alias = args
            if alias:
                chan, cca = 0, self.config.channel_assignments
                try:
                    chan = int(alias)
                except ValueError:
                    if cca.channel_defined(alias):
                        chan = cca.get_channel(alias)
                if chan <= 0 or chan > 16:
                    msg = "Invalid MIDI channel: '%s', using default." % alias
                    self.warning(msg)
                    chan = 1
                sy.midi_input_channel(chan)
            chan = sy.midi_input_channel() 
            msg = "%s MIDI input channel: %s [%d]"
            msg = msg % (self.current_sid, alias, chan)
            self.status(msg)
            return True
        else:
            return False

    # cmd [n]
    # change and display current synth transpose
    def transpose(self, tokens):
        sy = self.get_current_synth()
        if sy:
            args = parse_positional_args(tokens, ["str"],[["str", ""]])
            cmd, xpose = args
            if xpose:
                try:
                    xpose = int(xpose)
                except ValueError:
                    msg = "Invalid transpose amount: '%s'" % xpose
                    self.warning(msg)
                    return False
                sy.transpose(xpose)
            xpose = sy.transpose()
            msg = "%s transpose: %s" % (self.current_sid, xpose)
            self.status(msg)
            return True
        else:
            return False

    # cmd [low high]
    # change and display current synth keyrange
    def keyrange(self, tokens):
        sy = self.get_current_synth()
        if sy:
            args = parse_positional_args(tokens,
                                         ["str"],
                                         [["str",""],["str",""]])
            cmd, low, high = args
            if low != "":
                try:
                    low, high = int(low), int(high)
                    low, high = min(low, high), max(low, high)
                    low, high = max(low, 0), min(high, 127)
                    sy.key_range((low, high))
                except ValueError:
                    msg = "Invalid keyrange: low = '%s' high = '%s'"
                    msg = msg % (low, high)
                    self.warning(msg)
                    return False
            range_ = sy.key_range()
            msg = "%s keyrange %s" % (self.current_sid, range_)
            self.status(msg)
            return True
        else:
            return False

    # cmd [range param]
    #
    def bend(self, tokens):
        sy = self.get_current_synth()
        if sy:
            args = parse_positional_args(tokens,
                                        ["str"],
                                        [["str",""],["str","detune"]])
            cmd, range_, param = args
            if range_ != "":
                try:
                    range_ = abs(int(range_))
                    sy.bend_range(range_)
                    sy.bend_parameter(param)
                except ValueError:
                    msg = "Invalid bend range: '%s'" % range_
                    self.warning(msg)
                    return False
            range_ = sy.bend_range()
            param = sy.bend_parameter()
            msg = "%s bend range: %d, parameter: '%s'"
            msg = msg % (self.current_sid, range_, param)
            self.status(msg)
            return True
        else:
            return False        

    # cmd [name]
    #
    def keytable(self, tokens):
        sy = self.get_current_synth()
        if sy:
            args = parse_positional_args(tokens,["str"],[["str",""]])
            cmd, tabname = args
            if tabname:
                sy.keytable(tabname)
            msg = "%s keytable: '%s'" % (self.current_sid, sy.keytable())
            self.status(msg)
            return True
        else:
            return False
