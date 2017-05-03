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
    def assert_control_synth_type(stype):
        if stype not in CONTROLLER_SYNTH_TYPES:
            msg = "Invalid Controler synthtype: '%s'" % stype
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

    def assign_audio_output_bus(self, param, busname, sid=None):
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
        sy = self.get_synth(sid)
        rs = sy.keytable(newtab)
        if not silent:
            msg = "Synth %s keytable: '%s'" % (sid,rs)
            self.status(msg)
        return rs
    
    def midi_input_channel(self, chan=None, sid=None,silent=False):
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
        curve,mod,range_,limits,sy = self._assert_map_args(curve,mod,range_,limits,sid)
        source = self.config.controller_assignments.get_controller_number(ctrl)
        sy.add_controller_map(source,param,curve,mod,range_,limits)
        return True

    def map_velocity(self, param, curve=linear, mod=None, 
                     range_=None, limits=None, sid=None):
        curve,mod,range_,limits,sy = self._assert_map_args(curve,mod,range_,limits,sid)
        sy.add_source_map("velocity", param, curve, mod, range_, limits)
        return True

    def map_aftertouch(self, param, curve=linear, mod=None, 
                       range_=None, limits=None, sid=None):
        curve,mod,range_,limits,sy = self._assert_map_args(curve,mod,range_,limits,sid)
        sy.add_source_map("aftertouch", param, curve, mod, range_, limits)
        return True

    def map_pitchwheel(self, param, curve=linear, mod=None, 
                       range_=None, limits=None, sid=None):
        curve,mod,range_,limits,sy = self._assert_map_args(curve,mod,range_,limits,sid)
        sy.add_source_map("pitchwheel", param, curve, mod, range_, limits)
        return True

    def map_keynumber(self, param, curve=linear, mod=None, 
                      range_=None, limits=None, sid=None):
        curve,mod,range_,limits,sy = self._assert_map_args(curve,mod,range_,limits,sid)
        sy.add_source_map("keynumber", param, curve, mod, range_, limits)
        return True

    def parameter_map(self, source, param, curve=linear, mod=None, 
                      range_=None, limits=None, sid=None):
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
        sy = self.get_synth(sid)
        sy.x_dump()
        print(sy._bank.current_program.dump(1))
        stype, id_ = self.parse_sid(sid)
        self.proxy.free_synth(stype, id_)

    def _use_program(self, slot, sid):
        sy = self.get_synth(sid)
        sy.use_program(slot)

    def use_program(self, slot, sid=None, *more):
        self._use_program(slot, sid)
        for m in more:
            self._use_program(slot, m)
        
    def get_bank(self, sid=None, silent=False):
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
        bnk = self.get_bank(sid, silent=True)
        bnk.initialize()
        return bnk
        
    def save_bank(self, filename, sid=None):
        bnk = self.get_bank(sid, silent=True)
        filename = os.path.expanduser(filename)
        bnk.save(filename)
        return filename
        
    def load_bank(self, filename, sid=None):
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
        sy = self.get_synth(sid)
        p = sy.random_program()
        if p and use:
            sy.bank()[127] = p
            sy.use_program(127)

    def copy_program(self, slot=None, sid=None):
        sy = self.get_synth(sid)
        bnk = sy.bank()
        bnk.copy_to_clipboard(slot)

    def paste_program(self, slot=None, sid=None):
        sy = self.get_synth(sid)
        bnk = sy.bank()
        bnk.paste_clipboard(slot)
            
    def store_program(self, slot=None, name=None, sid=None):
        sy = self.get_synth(sid)
        bnk = sy.bank()
        prg = bnk.current_program
        if name: prg.name = name
        slot = slot or bnk.current_slot
        bnk[slot] = prg
        
    def copy_performance(self, slot=None, sid=None):
        sy = self.get_synth(sid)
        bnk = sy.bank()
        bnk.copy_performance(slot)

    def paste_performance(self, sid=None):
        sy = self.get_synth(sid)
        bnk = sy.bank()
        bnk.paste_performance()

    def fill_performance(self, start, end, sid=None):
        sy = self.get_synth(sid)
        bnk = sy.bank()
        bnk.fill_performance(start, end)
            
    def q_buses(self, sid=None, silent=False):
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
        specs = self.get_synth(sid).specs
        buffers = specs["buffers"]
        if not silent:
            print("# Buffers:")
            for b in buffers:
                print("#    ", b)
        return buffers

    def new_group(self, grp_name=""):
        mw = self.parser.app.main_window()
        grp = mw.add_synth_group(grp_name)
        try:
            grpname = grp.name
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
        mw = self.parser.app.main_window()
        if str(index).upper() == 'ALL':
            for grp in mw.group_windows:
                grp.deiconify()
        else:
            grp = mw.group_windows[index]
            grp.deiconify()
        
    def q_params(self, sid=None, silent=False):
        sy = self.get_synth(sid)
        bnk = sy.bank()
        params = bnk.template.keys()
        if not silent:
            for p in sorted(params):
                print("# %s" % p)
        return params

    def param(self, pname, new_value=None, slot=None, sid=None, silent=False):
        sy = self.get_synth(sid)
        bnk = sy.bank()
        program = bnk[slot]
        if new_value != None:
            program[pname] = new_value
        value = program[pname]
        if not silent:
            print("# [%s] -> %s" % (pname, value))
        return value

    def annotation_keys(self, sid=None):
        sy = self.get_synth(sid)
        ed = sy.synth_editor
        return ed.annotation_keys()

    # Ignore if key is not a defined annotation.
    def set_annotation(self, key, text, sid=None):
        sy = self.get_synth(sid)
        ed = sy.synth_editor
        ed.set_annotation(key, text)

    def get_annotation(self, key, sid=None):
        sy = self.get_synth(sid)
        ed = sy.synth_editor
        return ed.get_annotation(key)

    def bank_locked(self, sid=None):
        sy = self.get_synth(sid)
        return sy.bank().current_program_locked()

    def lock_bank(self, flag, sid=None):
        sy = self.get_synth(sid)
        sy.bank().lock_current_program(flag)
        return flag
