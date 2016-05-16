# llia.lliascript.parser
# 2016.05.14

from __future__ import print_function
import sys, os.path

from llia.lliascript.ls_constants import *
from llia.llerrors import LliaPingError, LliascriptParseError, LliascriptError
from llia.lliascript.ls_command import LsCommand
from llia.lliascript.synthhelper import SynthHelper
from llia.lliascript.bufferhelper import BufferHelper


class LsEntity(object):

    def __init__(self, lsid, lstype):
        self.lsid = lsid
        self.lstype = lstype


class Parser(object):

    def __init__(self, app):
        self.app = app
        self.proxy = app.proxy
        self.config = app.config
        self._exit_repl = False
        self._prompt = "Llia> "
        self._entities = {}
        # ISSUE: Number of hardcoded input and output buses is hard coded.
        #
        for i in range(8):
            for n in ("out_", "in_"):
                name = "%s%d" % (n, i)
                e = LsEntity(name, "abus")
                self._entities[name] = e
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
            ns["HELP"] = self.help_
            ns["abus"] = self.abus
            ns["cbus"] = self.cbus
            ns["channel_name"] = self.channel_name
            ns["controller_name"] =self.controller_name
            ns["clear_history"] = self.clear_history
            ns["dump"] = self.dump
            ns["history"] = self.print_history
            ns["ls"] = self._lsCommand.ls
            ns["panic"] = self.panic
            ns["ping"] = self.ping
            ns["load"] = self.load_python
            ns["sync"] = self.sync_all
            ns["use"] = self.use
            ns["what_is"] = self.what_is_interactive
            ns["x"] = self.exit_  
        
    def repl(self):
        print(BANNER)
        print(VERSION)
        print()
        pyver = sys.version_info[0]
        if pyver <= 2:
            infn = raw_input
        else:
            infn = input
        while not self._exit_repl:
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
        msg = "WARNING: %s" % msg
        print(msg)
        self._append_history(msg)

    def status(self, msg):
        print(msg)
        self._append_history(msg)
        
    def help_(self, topic=None):
        print("Help topic = %s, not implemented" % topic)
        return True
    
    def what_is(self, name):
        ent = self._entities.get(name, None)
        if ent:
            return ent.lstype
        else:
            return ""

    def what_is_interactive(self, name):
        lstype = self.what_is(name)
        if not lstype:
            msg = "'%s' has no value" % name
        else:
            msg = "'%s' is a %s" % (name, lstype)
        self.status(msg)
        return lstype
        
    def use(self, name):
        lstype = self.what_is(name)
        if lstype == "buffer":
            self.bufferhelper.use_buffer(name)
        elif lstype == "synth":
            self.synthhelper.use_synth(name)
        elif lstype == "abus":
            msg = "Can not use an abus"
            self.warning(msg)
        elif lstype == "cbus":
            msg = "Can not use a cbus"
            self.warning(msg)
        else:
            msg = "name '%s' ?" % name
            raise LliascriptError(msg)
        
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
            self._entities[name] = ent
            return True
        
    def abus(self, name, channels=1):
        lstype = self.register_entity(name, "abus", {"channels" : channels})
        if lstype:
            rs = self.proxy.add_audio_bus(name, channels)
            if rs:
                print("Adding audio bus: ", name)  # DEBUG
            return rs
        else:
            return lstype == "abus"

    def cbus(self, name, channels=1):
        lstype = self.register_entity(name, "cbus", {"channels" : channels})
        if lstype:
            rs = self.proxy.add_control_bus(name, channels)
            if rs:
                print("Adding control bus: ", name) # DEBUG
            return rs
        else:
            return lstype == "cbus"

    def channel_name(self, n, name=None):
        try:
            name = self.config.channel_name(n, name)
            print(name)
            return name
        except IndexError as err:
            self._append_history(err.message)
            print(err.message)
            return False

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

    def print_history(self):
        print("HISTORY:")
        print(self._history)
        return True

    # ISSUE: FIX ME dump target not implemented
    #
    def dump(self, target=None):
        self.proxy.dump()
        return True

    def panic(self):
        self.proxy.panic()
        print("Panic!")
        return True

    def ping(self, target=None):
        try:
            if target:
                return True
                pass                # ISSUE; FIX ME
            
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
        self._exit_repl = True
        self.app.exit()
