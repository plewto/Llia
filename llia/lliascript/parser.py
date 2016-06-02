# llia.lliascript.parser
# 2016.05.14

from __future__ import print_function
import sys, os.path

from llia.lliascript.ls_constants import *
from llia.llerrors import (LliaPingError, LliascriptParseError, LliascriptError,
                           NoSuchBusError)
from llia.lliascript.ls_command import LsCommand
from llia.lliascript.synthhelper import SynthHelper
from llia.lliascript.bufferhelper import BufferHelper
from llia.gui.llhelp import help_topics, print_topic

from llia.lliascript.compose import Composer


class LsEntity(object):

    def __init__(self, lsid, lstype):
        self.lsid = lsid
        self.lstype = lstype
        self.data = {}

class Parser(object):

    def __init__(self, app):
        self.app = app
        self.proxy = app.proxy
        self.config = app.config
        self.exit_repl = False
        self._prompt = "Llia> "
        self.entities = {}
        # ISSUE: Number of hardcoded input and output buses is hard coded.
        #
        for i in range(8):
            for n in ("out_", "in_"):
                name = "%s%d" % (n, i)
                e = LsEntity(name, "abus")
                self.entities[name] = e
        self._history = ""
        self._global_namespace = {}
        self._local_namespace = {}
        self._lsCommand = LsCommand(self)
        self.synthhelper = SynthHelper(self, self._local_namespace)
        self.bufferhelper = BufferHelper(self, self._local_namespace)
        self._init_namespace(self._local_namespace)


    def _init_namespace(self, ns):
            ns["ABUS"] = ABUS
            ns["CBUS"] = CBUS
            ns["BUFFER"] = BUFFER
            ns["SYNTH"] = SYNTH
            ns["EFX"] = EFX
            ns["CHAN"] = CHAN
            ns["CTRL"] = CTRL
            ns["STYPE"] = STYPE
            ns["KEYMODE"] = KEYMODE
            ns["ALL"] = ALL
            ns["velocity"] = velocity
            ns["aftertouch"] = aftertouch
            ns["keynumber"] = keynumber
            ns["pitchwheel"] = pitchwheel
            ns["linear"] = linear
            ns["exp"] = exp
            ns["scurve"] = scurve
            ns["step"] = step
            ns["help"] = self.help_
            ns["abus"] = self.abus
            ns["compose"] = self.compose
            ns["cbus"] = self.cbus
            ns["channel_name"] = self.channel_name
            ns["controller_name"] =self.controller_name
            ns["clear_history"] = self.clear_history
            ns["dump"] = self.dump
            ns["history"] = self.print_history
            ns["ls"] = self._lsCommand.ls
            ns["panic"] = self.panic
            ns["ping"] = self.ping
            ns["pp"] = self.pretty_printer
            ns["load"] = self.load_python
            ns["rm"] = self.rm
            ns["sync"] = self.sync_all
            ns["trace_midi"] = self.trace_midi
            ns["trace_osc"] = self.trace_osc
            ns["what_is"] = self.what_is_interactive
            ns["exit"] = self.exit_
            ns["test"] = self.test
        
    def repl(self):
        print(BANNER)
        print()
        pyver = sys.version_info[0]
        if pyver <= 2:
            infn = raw_input
        else:
            infn = input
        while not self.exit_repl:
            usrin = infn(self._prompt)
            self._append_history(usrin, False)
            try:
                self.batch(usrin)
            except SyntaxError as err:
                msg = "SyntaxError: %s" % err.message
                print(msg)
                self._append_history(msg)
            except NameError as err:
                msg = "NameError: %s" % err.message
                print(msg)
                self._append_history(msg)
            self.proxy.sync_to_host()
                
    def batch(self, pycode):
        try:
            exec pycode in self._global_namespace, self._local_namespace
        except Exception as err:
            msg = "%s " % err.__class__.__name__
            self.warning(msg)
            self.warning(err.message)

    def load_python(self, filename, sync=True):
        fname = os.path.expanduser(filename)
        if os.path.exists(fname):
            with open(fname, 'r') as input:
                pycode = input.read()
                self.batch(pycode)
                if sync: self.proxy.sync_to_host()
            return True
        else:
            msg = "Can not open python file '%s' for input" % fname
            self.warning(msg)
            if sync: self.proxy.sync_to_host()
            return False
        
    def _append_history(self, text, as_remark=True):
        if as_remark: text = "# " + text
        self._history += "%s\n" % text
        
    def warning(self, msg):
        for line in str(msg).split("\n"):
            line = "WARNING: %s" % line
            print(line)
            self._append_history(line)

    def status(self, msg):
        for line in str(msg).split("\n"):
            print(line)
            self._append_history(line)
        
    def help_(self, topic=None):
        if not topic:
            print("Help topics: ", end=" ")
            counter = 13
            for t in help_topics():
                print("%s" % t, end = " ")
                counter += len(t)+1
                if counter > 70:
                    print()
                    counter = 0
            print()
        else:
            print("*" * 70)
            print_topic(str(topic))

    def is_abus(self, name):
        ent = self.entities.get(name, None)
        return ent and ent.lstype == "abus"

    def is_cbus(self, name):
        ent = self.entities.get(name, None)
        return ent and ent.lstype == "cbus"

    def is_buffer(self, name):
        ent = self.entities.get(name, None)
        return ent and ent.lstype == "buffer"

    def is_synth(self, name):
        ent = self.entities.get(name, None)
        return ent and ent.lstype == "synth"

    def is_channel(self, name):
        try:
            name = int(str(name))
            return 1 <= name <= 16
        except ValueError:
            return self.config.channel_assignments.channel_defined(name)

    def is_controller(self, name):
        try:
            ctrl = int(str(name))
            return 0 <= ctrl <= 127
        except ValueError:
            return self.config.controller_assignments.controller_defined(name)

    # Removes name from parser entities only.
    # Does not actually remove underlying object.
    #
    def forget(self, name):
        try:
            del self.entities[name]
        except KeyError:
            pass

    def test(self):
        print("DEBUG parser entities")
        for k in sorted(self.entities.keys()):
            print("   '%s'" % k)
        
        
    def what_is(self, name):
        ent = self.entities.get(name, None)
        if ent:
            return ent.lstype
        else:
            chnflag = self.is_channel(name)
            ccflag = self.is_controller(name)
            if chnflag and ccflag:
                return "channel_or_controller"
            else:
                if chnflag:
                    return "channel"
                if ccflag:
                    return "controller"
                return ""

    def what_is_interactive(self, name):
        lstype = self.what_is(name)
        if not lstype:
            msg = "'%s' is " % type(name)
        else:
            msg = "'%s' is a %s" % (name, lstype)
        self.status(msg)
        return lstype
        
    def register_entity(self, name, lstype, data = {}):
        xtype = self.what_is(name)
        if xtype and xtype != lstype:
            msg = "Can not change %s '%s' to %s"
            msg = msg % (xtype, name, lstype)
            self.warning(msg)
            return False
        else:
            ent = LsEntity(name, lstype)
            ent.data = data
            self.entities[name] = ent
            return True
        
    def abus(self, name, channels=1):
        lstype = self.register_entity(name, "abus", {"channels" : channels})
        if lstype:
            rs = self.proxy.add_audio_bus(name, channels)
            return rs
        else:
            return lstype == "abus"

    def cbus(self, name, channels=1):
        lstype = self.register_entity(name, "cbus", {"channels" : channels})
        if lstype:
            rs = self.proxy.add_control_bus(name, channels)
            return rs
        else:
            return lstype == "cbus"

    def _set_channel_name(self, channel, new_name):
        new_name.replace(' ','_')
        stype = self.what_is(new_name)
        if not stype:
            self.config.channel_name(channel, new_name)
        elif stype == "channel":
            old_chan = self.config.channel_number(new_name)
            if old_chan == channel:
                pass
            else:
                msg = "Channel '%s' already in use" % new_name
                raise ValueError(msg)
        else:
            msg = "Can not resuse %s '%s' as MIDI channel name"
            msg = msg % (stype, new_name)
            raise ValueError(msg)
    
    def channel_name(self, n, new_name=None, silent=False):
        if new_name != None:
            self._set_channel_name(n, new_name)
        cname = self.config.channel_name(n)
        if not silent: print(cname)
        return cname
    
    def controller_name(self, ctrl, name=None):
        try:
            name = self.config.controller_name(ctrl, name)
            print(name)
            return name
        except (IndexError,TypeError) as err:
            self._append_history(err.message)
            print(err.message)
            return False

    def clear_history(self):
        self._history = ""
        return True

    def get_history(self):
        return self._history

    def set_history(self, txt):
        self._history = txt
    
    def print_history(self):
        print("HISTORY:")
        print(self._history)
        return True

    # ISSUE: FIX ME dump target not implemented
    #
    def dump(self, target=None):
        if not target:
            self.proxy.dump()
        else:
            self.synthhelper.dump_synth(target)
            
    def panic(self):
        self.proxy.panic()
        print("Panic!")
        return True

    def ping(self, sid=None):
        try:
            if sid:
                self.synthhelper.ping_synth(sid)
                return True
            else:
                rs = self.proxy.ping()
                return rs
        except LliaPingError as err:
            self._append_history(err.message)
            print(err.message)
            return False
            
    def sync_all(self):
        self.app.sync_all()
        return True
        
    def exit_(self):
        self.exit_repl = True
        self.app.exit_()

    def pretty_printer(self, flag=None):
        if flag is not None:
            if flag:
                flag = True
            else:
                flag = False
            self.config.set_option("MIDI", "enable-program-pp", flag)
        flag = self.config.get_option("MIDI", "enable-program-pp")
        msg = "Pretty printer "
        if flag:
            msg += "enabled."
        else:
            msg += "disabled."
        print(msg)
        return flag

    def trace_midi(self, flag):
        self.app.midi_receiver.enable_trace(flag)
        msg = "MIDI trace "
        if flag:
            msg += "enabled."
        else:
            msg += "disabled."
        print(msg)
        return flag
        
    def trace_osc(self, flag):
        self.proxy.osc_transmitter.trace = flag
        for sy in self.proxy.get_all_synths():
            sy.osc_transmitter.trace = flag
        msg = "Trace OSC "
        if flag:
            msg += "enabled."
        else:
            msg += "disabled."
        print(msg)
        return flag
            
    def remove_bus(self, name):
        lstype = self.what_is(name)
        if lstype == "abus":
            self.proxy.remove_audio_bus(name)
            self.forget(name)
            print("Removed audio bus: '%s'" % name)
        elif lstype == "cbus":
            self.proxy.remove_control_bus(name)
            self.forget(name)
            print("Removed control bus: '%s'" % name)
        else:
            raise NoSuchBusError(name)

    # Universal remove  (bus, buffer, synth, map)
    def rm(self, name, param=ALL, sid=None):
        lstype = self.what_is(name)
        if lstype == "abus" or lstype == "cbus":
            self.remove_bus(name)
        elif lstype == "buffer":
            self.bufferhelper.remove_buffer(name)
        elif lstype == "synth" or lstype == "efx":
            self.synthhelper.remove_synth(name)
        elif "controller" in lstype:
            self.synthhelper.remove_parameter_map(name, param, sid)
        elif name in (velocity,aftertouch,keynumber,pitchwheel):
            self.synthhelper.remove_parameter_map(name, param, sid)
        else:
            msg = "Can not remove '%s' (type '%s')" % (name,lstype)
            raise LliascriptError(msg)

    def compose(self):
        rb = Composer(self)
        code = rb.build()
        self._history = code
