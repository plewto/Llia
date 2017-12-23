# llia.lliascript.synthhelper
# 2016.05.15
# Extends Parser with synth related commands
#

from __future__ import print_function
import os.path

from llia.generic import is_list, clone
from llia.llerrors import LliascriptError, NoSuchSynthError, NoSuchBufferError
from llia.lliascript.ls_constants import *
from llia.synth_proxy import SynthProxy

class SynthHelper(object):

    _synth_and_group_serial_number = 0
    
    def __init__(self,parser,local_namespace):
        self.parser = parser
        self.proxy = parser.proxy
        self.config = self.proxy.config
        self.current_sid = ""
        self._init_namespace(local_namespace)
        self._assignment_serial_number = 0

    def _init_namespace(self, ns):
        ns["assign_audio_output"] = self.assign_audio_output_bus
        ns["assign_audio_input"] = self.assign_audio_input_bus
        ns["assign_control_output"] = self.assign_control_output_bus
        ns["assign_control_input"] = self.assign_control_input_bus
        ns["bend"] = self.bend
        ns["efx"] = self.add_efx
        ns["midi_input_channel"] = self.midi_input_channel
        ns["keytable"] = self.keytable
        ns["keyrange"] = self.keyrange
        ns["synth"] = self.add_synth
        ns["control_synth"] = self.add_control_synth
        ns["group"] = self.new_group
        ns["show_group"] = self.show_group
        ns["create_editor"] = self.create_editor
        ns["destroy_editor"] = self.destroy_editor
        ns["transpose"] = self.transpose
        ns["use"] = self.use_synth
        ns["pmap"] = self.parameter_map
        ns["program"] = self.use_program
        ns["bank"] = self.get_bank
        ns["synth_proxy"] = self.get_synth
        ns["save_bank"] = self.save_bank
        ns["init_bank"] = self.init_bank
        ns["load_bank"] = self.load_bank
        ns["random"] = self.random_program
        ns["copy"] = self.copy_program
        ns["paste"] = self.paste_program
        ns["store"] = self.store_program
        ns["copy_performance"] = self.copy_performance
        ns["paste_performance"] = self.paste_performance
        ns["fill_performance"] = self.fill_performance
        ns["qbuses"] = self.q_buses
        ns["qbuffers"] = self.q_buffers
        ns["qparams"] = self.q_params
        ns["param"] = self.param
        ns["annotation_keys"] = self.annotation_keys
        ns["set_annotation"] = self.set_annotation
        ns["get_annotation"] = self.get_annotation
        ns["bank_locked"] = self.bank_locked
        ns["lock_bank"] = self.lock_bank
        ns["extended_mode"] = self.extended_mode
        ns["extended_enabled"] = self.extended_enabled
        
    def warning(self, msg):
        self.parser.warning(msg)

    def status(self, msg):
        self.parser.status(msg)
        
    def update_prompt(self):
        pass

    def what_is(self, name):
        return self.parser.what_is(name)
        
    def synth_exists(self, sid=None):
        """
        Predicate returns true if synth exists.
        Defaults to current synth.
        """
        sid = sid or self.current_synth
        return self.proxy.synth_exists(None, None, sid)

    def get_synth(self, sid=None):
        """
        Returns SynthProxy for synth sid.
        sid defaults to current synth.
        """
        if not sid or sid == "*":
            sid = self.current_sid
        else:
            sid = sid or self.current_sid
        try:
            sy = self.proxy.get_synth(sid)
            return sy
        except KeyError:
          raise NoSuchSynthError(sid)

    def use_synth(self, sid):
        """
        Make synth sid the 'current' synth.
        Many lliscript functions default to the current synth.
        """
        self.get_synth(sid)
        self.current_sid = sid
        msg = "Using synth: %s" % sid
        self.status(msg)
        return True
        
    @staticmethod
    def assert_synth_type(stype):
        if stype not in SYNTH_TYPES:
            msg = "Invalid synth type: '%s'" % stype
            raise LliascriptError(msg)

    @staticmethod
    def assert_efx_type(stype):
        if stype not in EFFECT_TYPES:
            msg = "Invalid EFX synth type: '%s'" % stype
            raise LliascriptError(msg)

    @staticmethod
    def assert_control_synth_type(stype):
        if stype not in CONTROLLER_SYNTH_TYPES:
            msg = "Invalid Controller synthtype: '%s'" % stype
            raise LliascriptError(msg)
        
    @staticmethod
    def assert_keymode(kmode):
        if kmode not in KEY_MODES:
            msg = "Invalid keymode: '%s'" % kmode
            raise LliascriptError(msg)

    # Split synth_Id string in form "stype_n" into components (stype, n)
    # 
    def parse_sid(self, sid=None):
        """
        Split sid into component parts (T,N).
        An sid, for "synth id', is a unique identification string assigned to 
        each synth.  The id format is stype_n, where stype is the synthesizer
        type, and n is a unique serial number.  No two synths have the same 
        sid.  The n portion of the sid is also unique, no two synths have the 
        same serial number.   Newer synths have higher serial numbers.

        parse_sid  returns a tuple (T,N) where T and N are strings for the 
        synth type and serial number.

        The current sid is used by default.
        """
        sid = sid or self.current_sid
        pos = sid.rfind('_')
        if pos > -1:
            head, tail  = sid[:pos], sid[pos+1]
        else:
            head, tail = sid, ""
        return (head, tail)

    def assign_audio_output_bus(self, param, busname, sid=None):
        """
        Assign an audio output bus to a synth parameters
        param - The synth parameter used for output bus assignments.
        busname - the buses name
        sid - the synth id, defaults to current synth.

        Returns bool True if assignment could be made.
        """
        sid = sid or self.current_sid
        sy = self.get_synth(sid)
        lstype = self.what_is(busname)
        if lstype == 'abus' and self.proxy.audio_bus_exists(busname):
            stype, id_ = self.parse_sid(sid)
            self.proxy.assign_synth_audio_bus(stype, id_, param, busname)
            sy.assign_audio_output_bus(param, busname)
            ename = "assign-audio-bus-%d" % self._assignment_serial_number
            etype = "audio-bus-assignment"
            data = {"param" : param,
                    "assignment-type" : "output-bus",
                    "bus-name" : busname,
                    "offset" : 0,
                    "sid" : sid}
            self.parser.register_entity(ename, etype, data)
            self._assignment_serial_number += 1
            return True
        else:
            msg = "Can not assign audio output bus: " 
            msg += "sid=%s, param=%s, busname=%s"
            msg = msg % (sid, param, busname)
            self.warning(msg)
            return False

    def assign_audio_input_bus(self, param, busname, sid=None):
        """
        Assign an audio input bus to a synth parameters
        param - The synth parameter used for input bus assignments.
        busname - the buses name
        sid - the synth id, defaults to current synth.

        Returns bool True if assignment could be made.
        """
        sid = sid or self.current_sid
        sy = self.get_synth(sid)
        lstype = self.what_is(busname)
        if lstype == 'abus' and self.proxy.audio_bus_exists(busname):
            stype, id_ = self.parse_sid(sid)
            self.proxy.assign_synth_audio_bus(stype, id_, param, busname)
            sy.assign_audio_input_bus(param, busname)
            ename = "assign-audio-bus-%d" % self._assignment_serial_number
            etype = "audio-bus-assignment"
            data = {"param" : param,
                    "bus-name" : busname,
                    "assignment-type" : "input-bus",
                    "offset" : 0,
                    "sid" : sid}
            self.parser.register_entity(ename, etype, data)
            self._assignment_serial_number += 1
            return True
        else:
            msg = "Can not assign audio input bus:  "
            msg += "sid=%s, param=%s, busname=%s"
            msg = msg % (sid, param, busname)
            self.warning(msg)
            return False

    def assign_control_output_bus(self, param, busname, sid=None):
        """
        Assign an control output bus to a synth parameters
        param - The synth parameter used for output bus assignments.
        busname - the buses name
        sid - the synth id, defaults to current synth.

        Returns bool True if assignment could be made.
        """
        sid = sid or self.current_sid
        sy = self.get_synth(sid)
        lstype = self.what_is(busname)
        if lstype == 'cbus' and self.proxy.control_bus_exists(busname):
            stype, id_ = self.parse_sid(sid)
            self.proxy.assign_synth_control_bus(stype, id_, param, busname)
            sy.assign_control_output_bus(param, busname)
            ename = "assign-control-bus-%d" % self._assignment_serial_number
            etype = "control-bus-assignment"
            data = {"param" : param,
                    "bus-name" : busname,
                    "offset" : 0,
                    "sid" :sid}
            self.parser.register_entity(ename,etype,data)
            self._assignment_serial_number += 1
            return True
        else:
            msg = "Can not assign control output bus: "
            msg += "sid=%s, param=%s, busname=%s"
            msg = msg % (sid,param,busname)
            self.warning(msg)
            return False

    def assign_control_input_bus(self, param, busname, sid=None):
        """
        Assign an control input bus to a synth parameters
        param - The synth parameter used for input bus assignments.
        busname - the buses name
        sid - the synth id, defaults to current synth.

        Returns bool True if assignment could be made.
        """
        sid = sid or self.current_sid
        sy = self.get_synth(sid)
        lstype = self.what_is(busname)
        if lstype == 'cbus' and self.proxy.control_bus_exists(busname):
            stype, id_ = self.parse_sid(sid)
            self.proxy.assign_synth_control_bus(stype, id_, param, busname)
            sy.assign_control_input_bus(param, busname)
            ename = "assign-control-bus-%d" % self._assignment_serial_number
            etype = "control-bus-assignment"
            data = {"param" : param,
                    "bus-name" : busname,
                    "offset" : 0,
                    "sid" :sid}
            self.parser.register_entity(ename,etype,data)
            self._assignment_serial_number += 1
            return True
        else:
            msg = "Can not assign control input bus: "
            msg += "sid=%s, param=%s, busname=%s"
            msg = msg % (sid,param,busname)
            self.warning(msg)
            return False
        
    def assign_buffer(self, param, name=None, sid=None):
        """
        Assign a buffer to synth
        Buffers are temporarily disabled.
        """
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

    def add_synth(self, stype, keymode="PolyN", voice_count=8):
        """
        Add a new synth
        stype   - String, the synth type
        keymode - String, the key mode, see llia.constants.KEY_MODES, 
                  defaults to PolyN
        voice_count - int, number of voices to allocate, 
                  voice_count is ignored by some key modes.
                   
        The new synth becomes the current synth 
        Returns SynthProxy.
        """
        self.assert_synth_type(stype)
        self.assert_keymode(keymode)
        sy = self.proxy.add_synth(stype, keymode, voice_count)
        if sy:
            data =  {
                "serial-number" : self._synth_and_group_serial_number,
                "is-group" : False,
                "stype" : stype,
                "id" : sy.id_,
                "keymode" : keymode,
                "voice-count" : voice_count,
                "is-control-synth" : False,
                "is-efx" : False,
                "is-controller" : False}
            self.parser.register_entity(sy.sid,"synth",data)
            self._synth_and_group_serial_number+=1
            self.current_sid = sy.sid
            self.update_prompt()
            sy.keymode = keymode
            sy.voice_count = voice_count
        return sy

    def add_efx(self, stype):
        """
        Adds new effects synth.
        stype - String, the effect type.

        The new effect becomes the current synth.
        Returns SynthProxy.
        """
        self.assert_efx_type(stype)
        sy = self.proxy.add_efx(stype)
        if sy:
            data =  {
                "serial-number" : self._synth_and_group_serial_number,
                "is-group" : False,
                "stype" : stype,
                "id" : sy.id_,
                "is-control-synth" : False,
                "is-efx" : True}
            self.parser.register_entity(sy.sid,"synth",data)
            self._synth_and_group_serial_number+=1
            self.current_sid = sy.sid
            self.update_prompt()
        return sy
    
    def add_control_synth(self, stype):
        """
        Adds new controller synth.
        stype - String, the synth type.
        The new synth becomes the current synth.
        Returns SynthProxy.
        """
        self.assert_control_synth_type(stype)
        sy = self.proxy.add_efx(stype)
        if sy:
            data =   {
                "serial-number" : self._synth_and_group_serial_number,
                "is-group" : False,
                "is-efx" : False,
                "is-control-synth" : True,
                "stype" : stype}
            self.parser.register_entity(sy.sid, "synth",data)
            self._synth_and_group_serial_number+=1
            self.current_sid = sy.sid
            self.update_prompt()
            return sy

    # Creates editor for current synth.
    # Ignore if synth already has an editor or
    # GUI is not enabled.
    def create_editor(self):
        """
        Creates editor for current synth.
        Editors are not automatically created when the synth is.
        Does nothing if the synth already has an editor or if GUI 
        is not enabled.
        """
        gui = self.parser.config.gui().upper()
        if gui == "NONE":
            return
        if gui == "TK":
            sy = self.get_synth()
            if sy.synth_editor:
                # print("Synth %s already has an editor" % sy.sid)
                return
            else:
                from llia.gui.tk.tk_synthwindow import TkSynthWindow
                import llia.gui.tk.tk_factory as factory
                mw = self.parser.app.main_window()
                icon_filename = "resources/%s/logo_32.png" % sy.specs["format"]
                icon = factory.image(icon_filename)
                group_index = len(mw.group_windows)-1
                notebook = mw.group_windows[-1].notebook
                swin = TkSynthWindow(notebook, sy)
                swin.group_index = group_index
                sy.synth_editor = swin
                mw[sy.sid] = swin
                sy.create_subeditors()
                notebook.add(swin, text=sy.sid, image=icon, compound="top")
                sy.use_program(0)
                sy.synth_editor.sync()

    # Destroy editor for indicated synth
    # NOTES:
    #  For tk at least the synth *MUST* still be defined!!!
    #    First: destroy editor
    #    Next: remove synth
    #  
    def destroy_editor(self, sid='*'):
        """
        Destroy indicated editor.
        synth defaults to current synth.

        NOTE:
          The synth must still be defined to destroy ity's editor.
               1) Destroy editor
               2) remove synth.
        """
        gui = self.parser.config.gui().upper()
        if gui == "NONE":
            return
        if gui == "TK":
            from Tkinter import TclError
            sy = self.get_synth(sid)
            swin = sy.synth_editor
            grp_index = swin.group_index
            mw = self.parser.app.main_window()
            grp = mw.group_windows[grp_index]
            notebook = grp.notebook
            try:
                notebook.forget(swin)
            except TclError:
                pass

    def keytable(self,newtab=None,sid=None,silent=False):
        """
        Returns/changes/displays synth keytable.
        
        newtab - optional string, if specified change synths keytable.
        sid - string synth id, defaults to current synth
        silent - bool, if True do not display keytable name (useful in batch mode)

        Returns String, key table name
        """
        sy = self.get_synth(sid)
        rs = sy.keytable(newtab)
        if not silent:
            msg = "Synth %s keytable: '%s'" % (sid,rs)
            self.status(msg)
        return rs
    
    def midi_input_channel(self, chan=None, sid=None,silent=False):
        """
        Returns/changes/displays synth MIDI input channel.

        chan - optional int or String.  If specified change synths MIDI 
               channel.   The channel may either be an integer between 
               1 and 16 inclusive, or a channel name alias (see config)
        sid - String synth id, defaults to current synth.
        silent - bool, if True do not display channel name.
        
        Returns int
        """
        sy = self.get_synth(sid)
        chan_number = None
        if not chan:
            chan_number = sy.midi_input_channel()
        else:
            chan_number = self.config.channel_assignments.get_channel(chan)
            chan_number = sy.midi_input_channel(chan_number)
        if not silent:
            msg = "Synth %s MIDI input channel:  %s   '%s'" % (sid, chan_number, chan)
            self.status(msg)
        return chan_number

    def keyrange(self, lower=None, upper=None, sid=None, silent=False):
        """
        Returns/changes/displays synth key range.

        lower - optional int, lower key number.
        upper - optional int, upper key number
        sid - optional String synth id, defaults to current synth
        silent - bool, if True do not display range.

        If either lower or upper are specified the synths key range 
        is updated.

        Returns tuple (low, high)
        """
        sy = self.get_synth(sid)
        if lower or lower == 0:
            range_ = (lower, upper or 127)
            sy.key_range(range_)
        kr = sy.key_range()
        if not silent:
            msg = "Synth %s keyrange: %s" % (sid, kr)
            self.status(msg)
        return kr
    
    def bend(self, range_=None, param=None, sid=None, silent=False):
        """
        Returns/changes/displays synth bend range.

        range_ - optional int, bend range in cents.
        param - optional, synth parameter used for pitch-bend
                defaults to 'detune'
        sid -String synth id, defaults to current synth
        silent - bool, if True do not print bend range

        Returns tuple (c, p)  where
                c - range in cents
                p - synth parameter
        """
        sy = self.get_synth(sid)
        a = sy.bend_range(range_)
        b = sy.bend_parameter(param)
        if not silent:
            msg = "%s bend range: %d cents,  parameter: '%s'"
            msg = msg % (sid, a,b)
            self.status(msg)
        return (a, b)

    def transpose(self, n=None, sid=None, silent=False):
        """
        Returns/changes/displays synth transpose value.

        n - optional int, transposition in half-steps
        sid - String synth id, defaults to current synth 
        silent - optional bool, if True do not display transpose

        Returns int
        """
        sy = self.get_synth(sid)
        x = sy.transpose(n)
        if not silent:
            msg = "%s transpose: %s" % (sid, x)
            self.status(msg)
        return x

    def ping_synth(self, sid=None):
        """
        Diagnostic function which sends an OSC 'ping' to a server side synth.
        If the synth is alive it should post a response in the SuperCollider 
        post window.  Defaults to current synth.
        """
        sy = self.get_synth(sid)
        sy.x_ping()
        return True

    @staticmethod
    def _assert_map_curve(curve):
        if curve in curves:
            return True
        else:
            msg = "Expected one of the following for map_ curve argument:\n"
            msg += "linear, exp, scurve or step.  Encountered: %s"
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

    def map_cc(self, ctrl, param, curve=linear, mod=None, 
               range_=None, limits=None,sid=None):
        """
        See parameter_map 
        """
        curve,mod,range_,limits,sy = self._assert_map_args(curve,mod,range_,limits,sid)
        source = self.config.controller_assignments.get_controller_number(ctrl)
        sy.add_controller_map(source,param,curve,mod,range_,limits)
        return True

    def map_velocity(self, param, curve=linear, mod=None, 
                     range_=None, limits=None, sid=None):
        """
        See parameter_map
        """
        curve,mod,range_,limits,sy = self._assert_map_args(curve,mod,range_,limits,sid)
        sy.add_source_map("velocity", param, curve, mod, range_, limits)
        return True

    def map_aftertouch(self, param, curve=linear, mod=None, 
                       range_=None, limits=None, sid=None):
        """
        See parameter_map
        """
        curve,mod,range_,limits,sy = self._assert_map_args(curve,mod,range_,limits,sid)
        sy.add_source_map("aftertouch", param, curve, mod, range_, limits)
        return True

    def map_pitchwheel(self, param, curve=linear, mod=None, 
                       range_=None, limits=None, sid=None):
        """
        See parameter_map
        """
        curve,mod,range_,limits,sy = self._assert_map_args(curve,mod,range_,limits,sid)
        sy.add_source_map("pitchwheel", param, curve, mod, range_, limits)
        return True

    def map_keynumber(self, param, curve=linear, mod=None, 
                      range_=None, limits=None, sid=None):
        """
        See parameter_map
        """
        curve,mod,range_,limits,sy = self._assert_map_args(curve,mod,range_,limits,sid)
        sy.add_source_map("keynumber", param, curve, mod, range_, limits)
        return True

    def parameter_map(self, source, param, curve=linear, mod=None, 
                      range_=None, limits=None, sid=None):
        """
        Define mapping of MIDI value to synth parameter.

        source - String, the source signal, may be:
                 velocity
                 aftertouch
                 pitchwheel
                 keynumber
                 controller alias (see config)
                 controller number, an int between 0 and 127 inclusive.
        parm   - String,the synth parameter.
        curve  - String, the transfer function.
                 See llia.constants.CURVES, default "Linear"
        mod    - int, curve coefficient alters curve characteristics.
                 linear - has no effect.
                 exp - sets degree and concavity.  Higher absolute values 
                       are steeper, sign changes concavity between 
                       concave and convex.
        range_ - Tuple (A,B) range of parameter values. If B<A curve is 
                 inverted.
        limits - Tuple (min,max) sets hard limits on possible parameter values.
        sid    - The synth id, defaults to current synth.
        """
        lstype = self.what_is(source)
        if "controller" in lstype:
            self.map_cc(source, param, curve, mod, range_, limits, sid)
        else:
            source = str(source).lower()
            if source == velocity:
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
        """
        Removes a MIDI parameter map.
        
        source - the source signal, 
                 see parameter_map for possible value.
        param - String, the synth parameter
                If param is ALL then all maps from source are removed.
                Defaults to ALL.
        sid - synth id,defaults to current synth.
        """
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
        
    def remove_synth(self, sid, force=False):
        """
        Removes the indicated synth
        It is not possible to remove the current synth
        unless Force is True.
        """
        if sid == self.current_sid and not force:
            msg = "Can not free current synth: '%s'" % self.current_sid
            raise LliascriptError(msg)
        sy = self.get_synth(sid)
        sy.disconnect_from_buses()
        stype, id_ = self.parse_sid(sid)
        self.proxy.free_synth(stype, id_)
        self.parser.forget(sid)
        self.status("Removed synth: '%s'" % sid)
        if sid == self.current_sid:
            msg = "Lliascript current_sid '%s' has been removed" % sid
            self.warning(msg)
        return True
        
    def dump_synth(self, sid=None):
        """
        Diagnostic displays information about synth.
        
        sid - The synth id, defaults to current synth.
        """
        sy = self.get_synth(sid)
        sy.x_dump()
        print(sy._bank.current_program.dump(1))
        stype, id_ = self.parse_sid(sid)
        self.proxy.free_synth(stype, id_)

    def _use_program(self, slot, sid):
        sy = self.get_synth(sid)
        sy.use_program(slot)


    # ISSUE: Whats the point of the *more argument?
    def use_program(self, slot, sid=None, *more):
        """
        Update synth to use program from indicated bank slot.

        slot - int, bank slot number
        sid - synth id, defaults to current synth
        """
        self._use_program(slot, sid)
        for m in more:
            self._use_program(slot, m)
        
    def get_bank(self, sid=None, silent=False):
        """
        get/display program bank

        sid - Synth id, defaults to current synth.
        silent - bool, if True do not display bank contents

        Returns ProgramBank
        """
        sy = self.get_synth(sid)
        bnk = sy.bank()
        if not silent:
            print("%s bank:" % sy.sid)
            columns = 4
            rows = 128/columns
            for r in range(rows):
                acc = ""
                for c in range(columns):
                    slot = r + c * rows
                    program = bnk[slot]
                    name = program.name[:12]
                    acc += '[%3d] %-12s ' % (slot, name)
                print(acc)
        return bnk

    def init_bank(self, sid=None):
        """
        Initialize synth bank
        
        sid - the synth id, default to current bank.
        """
        bnk = self.get_bank(sid, silent=True)
        bnk.initialize()
        return bnk
        
    def save_bank(self, filename, sid=None):
        """
        Save bank file from synth.
        
        filename - the bank file name.
        sid - synth id, defaults to current synth.
        """
        bnk = self.get_bank(sid, silent=True)
        filename = os.path.expanduser(filename)
        bnk.save(filename)
        return filename
        
    def load_bank(self, filename, sid=None):
        """
        Loads bank file into synth.

        filename - The file name
        sid - The synth id, defaults to current synth

        If successful return True.
        If bank file could not be read, display warning and return False.
        """
        try:
            bnk = self.get_bank(sid, silent=True)
            filename = os.path.expanduser(filename)
            bnk.load(filename)
            return True
        except IOError:
            msg = "Can not open bank file: '%s'" % filename
            self.warning(msg)
            return False

    def random_program(self, use=True, sid=None):
        """
        Generate random program 

        use - bool, if True immediately load the program into the synth
        sid - The synth id, default current synth.

        The generated program is stored to bank slot 127.
        """
        sy = self.get_synth(sid)
        p = sy.random_program()
        if p and use:
            sy.bank()[127] = p
            sy.use_program(127)

    def copy_program(self, slot=None, sid=None):
        """
        Copy program to clipboard.
        
        slot - optional bank slot number.
               Defaults to current program
        sid - the synth id,defaults to current synth.
        """
        sy = self.get_synth(sid)
        bnk = sy.bank()
        bnk.copy_to_clipboard(slot)

    def paste_program(self, slot=None, sid=None):
        """
        Paste clipboard contents to synth bank.
        The clipboard is smart enough to only paste compatible programs.
        
        slot - The bank slot number, defaults to current program number.
        sid - The synth id,defaults to current synth.
        """
        sy = self.get_synth(sid)
        bnk = sy.bank()
        bnk.paste_clipboard(slot)
            
    def store_program(self, slot=None, name=None, sid=None):
        """
        Store the current program into program bank.
        slot - bank slot number,defaults to current program number.
        name - Then program name, defaults to current program name.
        sid - synth id, defaults to current synth.
        """
        sy = self.get_synth(sid)
        bnk = sy.bank()
        prg = bnk.current_program
        if name: prg.name = name
        slot = slot or bnk.current_slot
        bnk[slot] = prg
        
    def copy_performance(self, slot=None, sid=None):
        """
        Copy performance (MIDI parameters) to clipboard.
        
        slot - bank slot number, defaults to current program
        sid - synth id, defaults to current synth
        """
        sy = self.get_synth(sid)
        bnk = sy.bank()
        bnk.copy_performance(slot)

    def paste_performance(self, sid=None):
        """
        Paste performance clipboard to synth.
        sid - synth id, defaults to current synth
        """
        sy = self.get_synth(sid)
        bnk = sy.bank()
        bnk.paste_performance()

    def fill_performance(self, start, end, sid=None):
        """
        Copy the current Performance (MIDI parameters) to a range
        of bank slots.

        start - int starting slot number, 
        end - int, final slot number, 0<= start < end < 128
        sid - synth id, defaults to current synth.
        """
        sy = self.get_synth(sid)
        bnk = sy.bank()
        bnk.fill_performance(start, end)
            
    def q_buses(self, sid=None, silent=False):
        """
        Returns/print dictionary of bus assignments
        
        sid - synth id,default current synth
        silent - bool, if True do not display assignments.

        Returns dictionary
        """
        specs = self.get_synth(sid).specs
        aibus = specs["audio-input-buses"]
        aobus = specs["audio-output-buses"]
        cibus = specs["control-input-buses"]
        cobus = specs["control-output-buses"]
        if not silent:
            if aibus:
                print("# Audio input buses:")
                for b in aibus:
                    print("#    ",  b)
            if aobus:
                print("# Audio output buses:")
                for b in aobus:
                    print("#    ",  b)
            if cibus:
                print("# Control input buses:")
                for b in cibus:
                    print("#   ", b)
            if cobus:
                print("# Control output buses:")
                for b in cobus:
                    print("#  ", b)
        rs = {"audio-inputs" : aibus,
              "audio-outputs" : aobus,
              "control-inputs" : cibus,
              "control-outputs" : cobus}
        return rs

    def q_buffers(self, sid=None, silent=False):
        """
        Display list of buffer assignments.
        Buffer support are temporarily disabled.
        """
        specs = self.get_synth(sid).specs
        buffers = specs["buffers"]
        if not silent:
            print("# Buffers:")
            for b in buffers:
                print("#    ", b)
        return buffers

    def new_group(self, grp_name=""):
        """
        Create a new synth group.

        grp_name - the group name
        """
        mw = self.parser.app.main_window()
        grpwin = mw.add_synth_group(grp_name)
        try:
            grpname = grpwin.name
        except AttributeError:
            grpname = ""
        data = {"name" : grpname,
                "is-efx" : False,
                "is-group" : True,
                "serial-number" : self._synth_and_group_serial_number}
        self.parser.register_entity(grpname, "group", data)
        self._synth_and_group_serial_number+=1

    # deiconify group window(s)
    # index may be either int, the windows index 
    # or 'ALL'
    #
    def show_group(self, index=-1):
        """
        Deiconify group window
        
        index - The group window index.
                The special value ALL deiconify all group windows. 
        """
        mw = self.parser.app.main_window()
        if str(index).upper() == 'ALL':
            for grp in mw.group_windows:
                grp.deiconify()
        else:
            grp = mw.group_windows[index]
            grp.deiconify()
        
    def q_params(self, sid=None, silent=False):
        """
        Returns/displays a list of all synth parameters
        
        sid - synth id, default current synth
        silent - bool, if True do not display list
        
        Returns list
        """
        sy = self.get_synth(sid)
        bnk = sy.bank()
        params = bnk.template.keys()
        if not silent:
            for p in sorted(params):
                print("# %s" % p)
        return params

    def param(self, pname, new_value=None, slot=None, sid=None, silent=False):
        """
        display/change/return synth parameter value.
        pname - string parameter
        new_value - optional, if specified update current value of parameter.
        slot - optional bank slot number, if not specified use current program
        sid - synth id, default current synth
        silent - bool, if True do not display value
        """
        sy = self.get_synth(sid)
        bnk = sy.bank()
        program = bnk[slot]
        if new_value != None:
            program[pname] = new_value
        value = program[pname]
        if not silent:
            print("# [%s] -> %s" % (pname, value))
        return value

    def annotation_keys(self, sid=None, silent=False):
        """
        Returns a list of possible annotation keys.
        An annotation is an editor label which may be set at run time.
        sid - synth id, default current synth 
        """
        sy = self.get_synth(sid)
        ed = sy.synth_editor
        keys = ed.annotation.keys()
        if not silent:
            print("Annotation keys: ", keys)
        return keys

    # Ignore if key is not a defined annotation.
    # Ignore if annotation not enabled.
    def set_annotation(self, key, text, sid=None):
        """
        Set text of annotation label.
        If either key is not defined or annotation is not enabled, 
        do nothing.

        key - label selection key. See annotation_keys
        text - String, new label text
        sid - Synth id, default current synth
        """
        sy = self.get_synth(sid)
        ed = sy.synth_editor
        try:
            ed.set_annotation(key, text)
        except AttributeError:
            print("Editor annotation not enabled.")

    # Return annotation text.
    # Return empty string "" if annotation is not enabled.
    def get_annotation(self, key, sid=None):
        """
        Returns text from annotation label

        key - label selection key, see annotation_keys
        sid - Synth id, default current synth
        """
        sy = self.get_synth(sid)
        ed = sy.synth_editor
        try:
            return ed.get_annotation(key)
        except AttributeError:
            return ""

    def bank_locked(self, sid=None):
        """
        Returns True if bank is locked.
        sid - synth id
        """
        sy = self.get_synth(sid)
        return sy.bank().current_program_locked()

    def lock_bank(self, flag, sid=None):
        """
        Set lock status of bank.
        
        flag - bool 
        sid - synth id.
        """
        sy = self.get_synth(sid)
        sy.bank().lock_current_program(flag)
        return flag
    
    def extended_mode(self, enable, count, sid=None, nosync=False):
        """
        Change status of extended_program mode.

        enable - Bool.
        count  - int, voice count
        sid    - synth id.
        nosunc - bool, if True do not update editor graphics.
        """
        sy = self.get_synth(sid)
        km = sy.keymode
        sync = not nosync
        if km in SUPPORTS_EXTENDED_PROGRAMS:
            count = max(0, min(count,sy.voice_count))
            sy.extended_mode = enable
            sy.extended_count = count
            if sync:
                sy.synth_editor.sync()

    def extended_enabled(self,sid=None):
        """
        Returns status of extended program mode.
        Result is either False or an int, the voice count.
        """
        sy =self.get_synth(sid)
        return sy.extended_mode and sy.extended_count

    

            
            
