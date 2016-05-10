# llia.llscript.parser
# 2016.04.27

from __future__ import print_function
import sys, os.path

import llia.constants as con
from llia.llscript.lserrors import LliascriptParseError
from llia.llscript.lsutil import parse_positional_args, parse_keyword_args
from llia.llscript.lshelp import help_topics
from generic import is_int

class LSLParser(object):

    def __init__(self, app):
        super(LSLParser, self).__init__()
        self.app = app
        self.proxy = app.proxy
        self.config = app.config
        self._exit_repl = False
        self.history = ""
        self.dispatch_table = {}
        self._init_dispatch_table()
        self.prompt = "Llia> "
        self._current_line = ""
        self.current_synth = None  # String stype_id
        self.buffer_helper = None

    def _init_dispatch_table(self):
        self.dispatch_table["test"] = self.test # ISSUE: Remove after testing
        self.dispatch_table["#"] = self.remark
        self.dispatch_table["?"] = self.help_
        self.dispatch_table["help"] = self.help_
        self.dispatch_table["abus"] = self.add_audio_bus
        self.dispatch_table["boot"] = self.boot_server
        self.dispatch_table["cbus"] = self.add_control_bus
        self.dispatch_table["clear-history"] = self.clear_history
        self.dispatch_table["dump"] = self.dump
        self.dispatch_table["efx"] = self.add_efx
        self.dispatch_table["exit"] = self.exit_ 
        self.dispatch_table["x"] = self.exit_ # ISSUE: Remove after testing
        self.dispatch_table["free"] = self.free
        self.dispatch_table["history"] = self.print_history
        self.dispatch_table["id-self"] = self.id_self  # BROKEN See BUG 0001
        self.dispatch_table["ls"] = self.list_
        self.dispatch_table["panic"] = self.panic
        self.dispatch_table["ping"] = self.ping
        # self.dispatch_table["post"] = self.post   # ISSUE: Not well implemented
        # self.dispatch_table["postln"] = self.postln
        self.dispatch_table["python"] = self.exec_python
        self.dispatch_table["run"] = self.run_script
        self.dispatch_table["sync"] = self.sync_all
        self.dispatch_table["synth"] = self.add_synth
        self.dispatch_table["with-synth"] = self.with_synth

    def update_prompt(self):
        cs = str(self.current_synth)
        cb = str(self.buffer_helper.current_buffer)
        self.prompt = "Lila(synth: %s, buffer: %s)> " % (cs, cb)
        
    def test(self,tokens):
        return False
        
    def status(self, msg):
        self.app.status(msg)
        self.history += "# %s\n" % msg

    def warning(self, msg):
        self.app.warning(msg)
        self.history += "# WARNING: %s\n" % msg
        
    def add_to_history(self, tokens):
        self.history += self._current_line + "\n"

    def remark(self, tokens):
        pass

    @staticmethod
    def _strip_remarks(tokens):
        acc = []
        try:
            if len(tokens) == 0 or tokens == ['']:
                return acc
            else:
                for t in tokens:
                    if t[0] == "#":
                        break
                    else:
                        acc.append(t)
        except IndexError:
            pass
        return acc

    def exec_script(self, script):
        line_counter = 0
        for line in script.split("\n"):
            usrin = line
            self._current_line = usrin
            tokens = self._strip_remarks(usrin.split(" "))
            if tokens:
                dispatch_token = tokens[0].lower()
                try:
                    dfn = self.dispatch_table[dispatch_token]
                    dfn(tokens)
                    self.add_to_history(usrin)
                except KeyError:
                    print("ERROR: Line %d : %s ?" % (line_counter, dispatch_token))
                    return False
                except LliascriptParseError as err:
                    msg = "ERROR: Line %d\n" + err.message
                    print(msg)
                    return False
            line_counter += 1
        return True
                    
    def exec_scriptfile(self, filename):
        filename = os.path.expanduser(filename)
        if os.path.exists(filename):
            with open(filename, 'r') as input:
                code = input.read()
                return self.exec_script(code)
        else:
            msg = "ERROR: Can not open script file '%s'" % filename
            print(msg)
            return False
            
    def repl(self):
        print(con.BANNER)
        print(con.VERSION)
        print()
        pyver = sys.version_info[0]
        if pyver <= 2:
            infn = raw_input
        else:
            infn = input
        while not self._exit_repl:
            usrin = infn(self.prompt).strip()
            self._current_line = usrin
            tokens = self._strip_remarks(usrin.split(" "))
            if tokens:
                dispatch_token = tokens[0].lower()
                try:
                    dfn = self.dispatch_table[dispatch_token]
                    rs = dfn(tokens)
                    self.add_to_history(usrin)
                    self.echo(rs)
                except KeyError:
                    print("%s ?" % dispatch_token)
                except LliascriptParseError as err:
                    print(err.message)
            self.sync_all([])

 
    def echo(self, flag):
        if flag:
            print("OK")
        else:
            print("ERROR")
            self.history += "# ERROR\n"
            
    def help_(self, tokens):
        topic = parse_positional_args(tokens,
                                                ["str"],
                                                [["str", "help"]])
        topic = topic[1].lower()
        if topic == "help" or topic == "?":
            print("Help topics:")
            for t in sorted(help_topics.keys()):
                print("   %s" % t)
            return True
        else:
            try:
                help_text = help_topics[topic]
                print("%s topic: %s" % ("*"*50, topic))
                print(help_text)
                print()
                return True
            except KeyError:
                msg = "Unknown help topic: '%s'" % topic
                self.warning(msg)
                msg = "Enter help without a topic to see avaliable topics."
                self.warning(msg)
                return False


    def sync_all(self, tokens):
        self.app.sync_all()
        return True
    
    def exit_(self, tokens):
        self._exit_repl = True
        self.app.exit()
        
    def ping(self, tokens):
        rs = self.proxy.ping();
        return rs

    def free(self, tokens):
        self.proxy.free()
        return True

    # dump 
    # 
    def dump(self, tokens):
        self.proxy.dump()
        return True
        
    # boot [server=internal]
    # Possible servers: internal, local, default
    #
    def boot_server(self, tokens):
        target = parse_positional_args(tokens,
                                                 ["str"],
                                                 [["str","internal"]])
        target = str(target[1])
        self.app.status("Booting %s server..." % target)
        return self.proxy.boot_server(target)

    # BROKEN: see BUG 0001
    def id_self(self, tokens):
        ip, port = self.config["client"], self.config["client_port"]
        payload = (self.app.global_osc_id(), ip, port)
        print(payload)
        return self.proxy.id_self()

    # ls abus|cbus|buffer|synth|efx
    def list_ (self, tokens):
        target = parse_positional_args(tokens,
                                                 ["str", "str"])[1]
        target = target.upper()
        if target == "ABUS":
            self.proxy.list_audio_buses()
            return True
        elif target == "CBUS":
            self.proxy.list_control_buses()
            return True
        elif target == "COMMANDS":
            for cmd in sorted(self.dispatch_table.keys()):
                print("   %s" % cmd)
            print()
            return True
        elif target == "BUFFERS":
            self.proxy.list_buffers()
            return True
        elif target == "SYNTHS":
            self.proxy.list_synths()
            return True
        elif target == "EFX":
            self.proxy.list_efx()
            return True
        elif target in ("SYNTH-TYPES", "EFX-TYPES", "KEYMODES"):
            print("Valid synth types:")
            for s in sorted(con.SYNTH_TYPES):
                print("   %s" % s)
            print("Valid EFX Synth types:")
            for s in sorted(con.EFFECT_TYPES):
                print("   %s" % s)
                print("Valid keymodes:")
            for s in sorted(con.KEY_MODES):
                print("   %s" % s)
            return True
        else:
            ls_targets = ("abus", "cbus", "buffers", "synths", "efx", "command",
                          "syhth-types", "efx-types", "keymodes")
            
            #msg = "Expected one of 'abus', 'cbus', 'buffers', 'synths', 'efx', or 'command', "
            #msg = msg + "not %s" % target
            #self.warning(msg)
            self.warning("Expected one of the following ls targets, not '%s'" % target)
            for t in sorted(ls_targets):
                print("   %s" % t)
            return False

    
    # abus name [channels]
    #
    def add_audio_bus(self, tokens):
        args = parse_positional_args(tokens,
                                                 ["str", "str"],
                                                 [["int", 1]])
        cmd, bname, chans = args
        rs = self.proxy.add_audio_bus(bname, chans)
        return rs

    # cbus name [channels]
    #
    def add_control_bus(self, tokens):
        args = parse_positional_args(tokens,
                                                 ["str", "str"],
                                                 [["int", 1]])
        cmd, bname, chans = args
        rs = self.proxy.add_control_bus(bname, chans)
        return rs

    # python filename
    # Execute python file
    #
    # Two objects are passed to the global name space for the file
    # app -> a reference to self.app
    # rs  -> An object used to return values
    #        use rs.value = x to return a value from the script
    #
    def exec_python(self, tokens):
        args = parse_positional_args(tokens,["str", "str"])
        filename = args[1]
        filename = os.path.expanduser(filename)
        if os.path.exists(filename):
            class RS:
                def __init__(self):
                    self.value = None
            rs = RS()
            global_ns = {"app" : self.app, "rs" : rs}
            execfile(filename, global_ns)
            print("rs -> ", rs.value)
            return rs.value
        else:
            msg = "Python file '%s' does not exist" % filename
            self.warning(msg)
            return False

    def panic(self, tokens):
        self.proxy.panic()
        return True
        
    def post(self, tokens):
        cl = self._current_line[4:].strip()
        print(cl, end="")
        self.proxy.post(cl)
        return True

    def postln(self, tokens):
        cl = self._current_line[6:].strip()
        print(cl)
        self.proxy.postln(cl)

    def run_script(self, tokens):
        filename = parse_positional_args(tokens, ["str", "str"])[1]
        rs = self.exec_scriptfile(filename)
        return rs


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
            msg = "Synth %s already exists" % sid
            self.warning(msg)
            return False
        if not self.proxy.audio_bus_exists(obusName):
            msg = "Audio bus '%s' does not exists" % obusName
            self.warning(msg)
            return False
        rs = self.proxy.add_synth(stype, id_, keymode, voice_count)
        if rs:
            self.proxy.assign_synth_audio_bus(stype, id_, obusParam, obusName, obusOffset)
            self.current_synth = sid
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
            self.current_synth = sid
            self.update_prompt()
        return rs
    
    # with stype id_
    # Select synth for editing.
    #
    def with_synth(self, tokens):
        args = parse_positional_args(tokens,
                                               ["str", "str", "int"])
        cmd, stype, id_ = args
        sid = "%s_%d" % (stype, id_)
        if self.proxy.synth_exists(stype, id_):
            msg = "Using synth '%s'" % sid
            self.status(msg)
            self.update_prompt()
            return True
        else:
            msg = "Synth '%s' does not exists" % sid
            self.warning(msg)
            return False
        
    def print_history(self, tokens):
        print("History")
        print(self.history)
        return True

    def clear_history(self, tokens):
        self.history = ""
        return True
