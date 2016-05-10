# llia.llscript.parser
# 2016.04.27

from __future__ import print_function
import sys, os.path

import llia.constants as con
from llia.llerrors import LliaPingError, LliascriptParseError
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
        self.buffer_helper = None
        self.synth_helper = None

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
        self.dispatch_table["exit"] = self.exit_ 
        self.dispatch_table["x"] = self.exit_ # ISSUE: Remove after testing
        self.dispatch_table["free"] = self.free
        self.dispatch_table["history"] = self.print_history
        self.dispatch_table["id-self"] = self.id_self  # BROKEN See BUG 0001
        self.dispatch_table["ls"] = self.list_
        self.dispatch_table["panic"] = self.panic
        self.dispatch_table["ping"] = self.ping
        self.dispatch_table["python"] = self.exec_python
        self.dispatch_table["run"] = self.run_script
        self.dispatch_table["sync"] = self.sync_all

    def update_prompt(self):
        cs = str(self.synth_helper.current_synth)
        cb = str(self.buffer_helper.current_buffer)
        self.prompt = "Lila(synth: %s, buffer: %s)> " % (cs, cb)
        
    def test(self,tokens):
        msg = "A self infliced wound"
        raise ValueError(msg)
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
        try:
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
        except LliaPingError as err:
            self.warning(err.message)
            return False
                    
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
            try:
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
            except LliaPingError as err:
                self.warning(err.message)
 
    def echo(self, flag):
        if flag:
            print("OK")
        else:
            print("ERROR")
            self.history += "# ERROR\n"
            
    def help_(self, tokens):
        topic = parse_positional_args(tokens,["str"],[["str", "help"]])
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

    # ping [*]
    #   without arguments ping global app
    #   with * argument ping current synth
    def ping(self, tokens):
        args = parse_positional_args(tokens, ["str"],[["str", ""]])
        cmd, target = args
        if target == "*":
            rs = self.synth_helper.ping_synth()
        else:
            rs = self.proxy.ping();
        return rs

    def free(self, tokens):
        self.proxy.free()
        return True

    # dump [*] 
    # 
    def dump(self, tokens):
        args = parse_positional_args(tokens, ["str"],[["str", ""]])
        cmd, target = args
        if target == "*":
            rs = self.synth_helper.dump_synth()
        else:
            self.proxy.dump()
            rs = True
        return rs
        
    # boot [server=internal]
    # Possible servers: internal, local, default
    #
    def boot_server(self, tokens):
        target = parse_positional_args(tokens,["str"],[["str","internal"]])
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
        
    def print_history(self, tokens):
        print("History")
        print(self.history)
        return True

    def clear_history(self, tokens):
        self.history = ""
        return True
