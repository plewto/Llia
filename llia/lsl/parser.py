# llia.lsl.parser
# 2016.04.27

from __future__ import print_function
import sys, os.path

from llia.lsl.lsl_constants import *
from llia.lsl.lsl_errors import *
from generic import is_int

# class LliaParseError(Exception):

#     def __init__(self, msg=""):
#         super(LliaParseError, self).__init__(msg)

class LSLParser(object):

    def __init__(self, app):
        super(LSLParser, self).__init__()
        self.app = app
        self.proxy = app.proxy
        self.config = app.config
        self._exit_repl = False
        self._dispatch_table = {}
        self._init_dispatch_table()
        self.prompt = "Lila> "
        self._current_line = ""
        self._current_synth = None  # String stype_id

    def _init_dispatch_table(self):
        self._dispatch_table["test"] = self.test
        self._dispatch_table[REMARK_TOKEN] = self.remark
        self._dispatch_table["?"] = self.help_
        self._dispatch_table["help"] = self.help_
        self._dispatch_table["abus"] = self.add_audio_bus
        self._dispatch_table["boot"] = self.boot_server
        self._dispatch_table["buffer"] = self.add_buffer    
        self._dispatch_table["cbus"] = self.add_control_bus
        self._dispatch_table["dump"] = self.dump
        self._dispatch_table["efx"] = self.add_efx
        self._dispatch_table["x"] = self.exit_ # FPO Change to 'exit' after testing
        self._dispatch_table["free"] = self.free
        self._dispatch_table["id-self"] = self.id_self
        # self._dispatch_table["load"] = self.load
        self._dispatch_table["ls"] = self.list_
        self._dispatch_table["panic"] = self.panic
        self._dispatch_table["ping"] = self.ping
        self._dispatch_table["post"] = self.post
        self._dispatch_table["postln"] = self.postln
        self._dispatch_table["python"] = self.exec_python
        self._dispatch_table["run"] = self.run_script
        # self._dispatch_table["save"] = self.save
        self._dispatch_table["sync"] = self.sync_all
        self._dispatch_table["synth"] = self.add_synth
        self._dispatch_table["with"] = self.with_synth

    def status(self, msg):
        self.app.status(msg)

    def warning(self, msg):
        self.app.warning(msg)
        
    def add_to_history(self, tokens):
        pass
        # print("HISTORY ", tokens)

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
                    if t[0] == REMARK_TOKEN:
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
                    dfn = self._dispatch_table[dispatch_token]
                    dfn(tokens)
                    self.add_to_history(usrin)
                except KeyError:
                    print("ERROR: Line %d : %s ?" % (line_counter, dispatch_token))
                    return False
                except LliaParseError as err:
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
        print(BANNER)
        print(VERSION)
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
                    dfn = self._dispatch_table[dispatch_token]
                    dfn(tokens)
                    self.add_to_history(usrin)
                except KeyError:
                    print("%s ?" % dispatch_token)
                except LliaParseError as err:
                    print(err.message)

    @staticmethod
    def expect(ttype, token):
        if ttype == "str":
            return token
        elif ttype == "strint":
            try:
                value = int(token)
            except ValueError:
                value= token
            return value
        elif ttype == "int":
            try:
                value = int(token)
                return value
            except ValueError:
                msg = "Expected int, encountered %s" % token
                raise LliaParseError(msg)
        else:
            return token
        
    @staticmethod
    def parse_line_required(tokens, required_args):
        acc = []
        min_count = len(required_args)
        if len(tokens) < min_count:
            msg = "Expected at least %d tokens, found %d"
            msg = msg % (min_count, len(tokens))
            raise LliaParseError(msg)
        # Required args
        for i,exptype in enumerate(required_args):
            token = tokens[i]
            value = LSLParser.expect(exptype, token)
            acc.append(value)
        return acc
    
    @staticmethod
    def parse_line_positional(tokens, required_args, opt_args=[]):
        acc = LSLParser.parse_line_required(tokens, required_args)
        index = len(required_args)
        for j,arg in enumerate(opt_args):
            try:
                token = tokens[index]
            except IndexError:
                token = arg[1]
            exptype = arg[0]
            value = LSLParser.expect(exptype, token)
            acc.append(value)
            index += 1
        return acc

    @staticmethod
    def parse_line_keywords(tokens, required_args, order=[], keyword_args={}):
        acc = LSLParser.parse_line_required(tokens, required_args)
        bcc = {}
        index = len(required_args)
        while index < len(tokens):
            try:
                kw = tokens[index].lower()
                token = tokens[index+1]
                try:
                    spec = keyword_args[kw]
                except KeyError:
                    msg = "Unexpected keyword %s" % kw
                    raise LliaParseError(msg)
                value = LSLParser.expect(spec[0], token)
                bcc[kw] = value
            except IndexError:
                msg = "Expected matching keyword/value pairs"
                raise LliaParseError(msg)
            index += 2
        for kw in order:
            kw = kw.lower()
            dflt = keyword_args[kw][1]
            value = bcc.get(kw, dflt)
            acc.append(value)
        return acc

    @staticmethod
    def echo(flag):
        if flag:
            print("OK")
        else:
            print("ERROR")

 
            
    def help_(self, tokens):
        topic = LSLParser.parse_line_positional(tokens,
                                                ["str"],
                                                [["str", "help"]])
        topic = topic[1]
        print("FPO help topic: ", topic)
        return True

    def sync_all(self, tokens):
        self.app.sync_all()
    
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
        target = LSLParser.parse_line_positional(tokens,
                                                 ["str"],
                                                 [["str","internal"]])
        target = str(target[1])
        self.app.status("Booting %s server..." % target)
        return self.proxy.boot_server(target)
        
    def id_self(self, tokens):
        return self.proxy.id_self()

    # ls abus|cbus|buffer|synth|efx
    def list_ (self, tokens):
        target = LSLParser.parse_line_positional(tokens,
                                                 ["str", "str"])[1]
        head = target[0].upper()
        if head == "A":
            self.proxy.list_audio_buses()
            return True
        elif head == "C":
            self.proxy.list_control_buses()
            return True
        elif head == "B":
            self.proxy.list_buffers()
            return True
        elif head == "S":
            self.proxy.list_synths()
            return True
        elif head == "E":
            self.proxy.list_efx()
            return True
        else:
            msg = "Expected one of 'abus', 'cbus', 'buffer', 'synth' or 'efx', "
            msg = msg + "not %s" % target
            self.warning(msg)
            return False

    
    # abus name [channels]
    #
    def add_audio_bus(self, tokens):
        values = LSLParser.parse_line_positional(tokens,
                                                 ["str", "str"],
                                                 [["int", 1]])
        cmd, bname, chans = values
        self.proxy.add_audio_bus(bname, chans)

    # cbus name [channels]
    #
    def add_control_bus(self, tokens):
        values = LSLParser.parse_line_positional(tokens,
                                                 ["str", "str"],
                                                 [["int", 1]])
        cmd, bname, chans = values
        self.proxy.add_control_bus(bname, chans)

    # buffer name [:frames :channels]
    def add_buffer(self, tokens):
        values = LSLParser.parse_line_keywords(tokens,
                                              ["str","str"],
                                              [":frames", ":channels"],
                                              {":frames" : ["int", 1024],
                                               ":channels" : ["int", 1]})
        cmd, bname, frames, channels = values
        self.proxy.add_buffer(bname, frames, channels)

    # python filename
    # Execute python file
    #
    # Two objects are passed to the global name space for the file
    # app -> a reference to self.app
    # rs  -> An object used to return values
    #        use rs.value = x to return a value from the script
    #
    def exec_python(self, tokens):
        values = LSLParser.parse_line_positional(tokens,
                                                 ["str", "str"])
        filename = values[1]
        filename = os.path.expanduser(filename)
        if os.path.exists(filename):
            class RS:
                def __init__(self):
                    self.value = None
            rs = RS()
            global_ns = {"app" : self.app, "rs" : rs}
            execfile(filename, global_ns)
            print("rs -> ", rs.value)
            return rs
        else:
            msg = "Python file '%s' does not exist" % filename
            self.warning(msg)
            return False

    def panic(self, tokens):
        self.proxy.panic()
        
    def post(self, tokens):
        cl = self._current_line[4:].strip()
        print(cl, end="")
        self.proxy.post(cl)

    def postln(self, tokens):
        cl = self._current_line[6:].strip()
        print(cl)
        self.proxy.postln(cl)

    def run_script(self, tokens):
        filename = LSLParser.parse_line_positional(tokens,
                                                  ["str", "str"])[1]
        self.exec_scriptfile(filename)


    # synth stype id_ [:keymode km][:voice-count vc]
    #                 [:outbus busName][:outbus-offset n][:outbus-param param]
    def add_synth(self, tokens):
        args = LSLParser.parse_line_keywords(tokens,
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
        if stype not in SYNTH_TYPES:
            msg = "Unknown synth type: '%s'" % stype
            self.warning(msg)
            return False
        if keymode not in KEY_MODES:
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
        self.proxy.assign_synth_audio_bus(stype, id_, obusParam, obusName, obusOffset)
        self._current_synth = sid
        self.prompt = "Llia(%s)> " % sid
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
        args = LSLParser.parse_line_keywords(tokens,
                                             req_args,
                                             key_arg_order,
                                             key_args)
        cmd, stype, id_, ibs, obs, oboff, obprm, iboff, ibprm = args
        sid = "%s_%d" % (stype, id_)
        if stype not in EFFECT_TYPES:
            msg = "Unknown EFX synth type: '%s'" % stype
            self.warning(msg)
            return False
        if self.proxy.synth_exists(stype, id_):
            msg = "Synth %s already exists" % sid
            self.warning(msg)
            return False
        for bs in (obs, ibs):
            if not self.proxy.audio_bus_exists(bs):
                msg = "Audio bus '%s' does not exists"
                self.warnng(msg)
                return False
        rs = self.proxy.add_efx(stype, id_)
        self.proxy.assign_synth_audio_bus(stype, id_, obprm, obs, oboff)
        self.proxy.assign_synth_audio_bus(stype, id_, ibprm, ibs, iboff)
        self._current_synth = sid
        self.prompt = "Llia(%s)> " % sid
        return rs
    
    # with stype id_
    # Select synth for editing.
    #
    def with_synth(self, tokens):
        args = LSLParser.parse_line_positional(tokens,
                                               ["str", "str", "int"])
        cmd, stype, id_ = args
        sid = "%s_%d" % (stype, id_)
        if self.proxy.synth_exists(stype, id_):
            msg = "Using synth '%s'" % sid
            self.status(msg)
            self.prompt = "Llia(%s)> " % sid
        else:
            msg = "Synth '%s' does not exists" % sid
            self.warning(msg)
        
        
        
    def test(self,tokens):
        pass
