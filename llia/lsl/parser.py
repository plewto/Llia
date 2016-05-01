# llia.lsl.parser
# 2016.04.27

from __future__ import print_function
import sys

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
        self._exit_repl = False
        self._dispatch_table = {}
        self._init_dispatch_table()
        self.prompt = "Lila> "

    def _init_dispatch_table(self):
        self._dispatch_table["test"] = self.test
        self._dispatch_table[REMARK_TOKEN] = self.remark
        self._dispatch_table["?"] = self.help_
        self._dispatch_table["help"] = self.help_
        self._dispatch_table["abus"] = self.add_audio_buss
        self._dispatch_table["boot"] = self.boot_server
        self._dispatch_table["buffer"] = self.add_buffer    
        self._dispatch_table["cbus"] = self.add_control_bus
        self._dispatch_table["dump"] = self.dump
        self._dispatch_table["efx"] = self.add_efx
        self._dispatch_table["exit"] = self.exit_
        self._dispatch_table["load"] = self.load
        self._dispatch_table["panic"] = self.panic
        self._dispatch_table["ping"] = self.ping
        self._dispatch_table["py"] = self.exec_python
        self._dispatch_table["q"] = self.query
        self._dispatch_table["save"] = self.save
        self._dispatch_table["synth"] = self.add_synth

    def add_to_history(self, tokens):
        pass
        # print("HISTORY ", tokens)

    def remark(self, tokens):
        pass

    @staticmethod
    def _strip_remarks(tokens):
        acc = []
        if len(tokens) == 0 or tokens == ['']:
            return acc
        else:
            for t in tokens:
                if t[0] == REMARK_TOKEN:
                    break
                else:
                    acc.append(t)
            return acc
            
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
        # Required arg
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

    def test(self, tokens):
        id_ = tokens[1]
        rs = self.proxy.q_control_bus_info(id_)
        print(rs)
            
    def help_(self, tokens):
        topic = LSLParser.parse_line_positional(tokens,
                                                ["str"],
                                                [["str", "help"]])
        topic = topic[1]
        print("FPO help topic: ", topic)

    # cmd name [numchans]
    #
    def add_audio_buss(self, tokens):
        values = LSLParser.parse_line_positional(tokens,
                                                 ["str", "str"],
                                                 [["int", 1]])
        alias, numchans = values[1:]
        rs = self.proxy.add_audio_bus(alias, numchans)
        self.echo(rs)

    # cmd [server-name]
    #
    def boot_server(self, tokens):
        values = LSLParser.parse_line_positional(tokens,
                                                 ["str"],
                                                 [["str", "default"]])
        rs = self.proxy.boot_server(values[1])
        self.echo(rs)
        
        
    def add_buffer(self, tokens): # ISSUE: Fix Me
        print("FPO add_buffer")

    # cmd name [numchans]
    #
    def add_control_bus(self, tokens):
        values = LSLParser.parse_line_positional(tokens,
                                                 ["str", "str"],
                                                 [["int", 1]])
        alias, numchans = values[1:]
        rs = self.proxy.add_control_bus(alias, numchans)
        self.echo(rs)

    # cmd [target]
    # If target specified dump, specifically that entity.
    # If no target specified dump global application data
    #
    def dump(self, tokens):     # ISSUE: Fix Ms
        target = LSLParser.parse_line_positional(tokens,
                                                 ["str"],
                                                 [["str", "global"]])[1]
        if target == "global":
            rs = self.proxy.dump()
            self.echo(rs)
        else:
            print("No dump function defined for target: '%s'" % target)
            self.echo(False)

    # cmd name id [:inbus name][:inbus-count 1][:outbus name][:outbus-count 1]
    #
    def add_efx(self, tokens):
        values = LSLParser.parse_line_keywords(tokens,
                                               ["str", "str", "int"],
                                               [":inbus", ":inbus-offset",
                                                ":outbus", ":outbus-offset"],
                                               {":inbus" : ["strint", 1000],
                                                ":inbus-offset" : ["int", 0],
                                                ":outbus" : ["strint", 0],
                                                ":outbus-offset" : ["int", 0]})
        cmd, synth, id_, ibus, ibus_offset, obus, obus_offset = values
        try:
            if not self.proxy.audio_bus_exists(ibus):
                msg = "Input bus does not exists: '%s'" % ibus
                raise NoSuchBusError(msg)
            if not self.proxy.audio_bus_exists(obus):
                msg = "Output bus does not exists: '%s'" % obus
                raise NoSuchBussError(msg)
            rs = self.proxy.add_efx(synth, id_, (ibus, ibus_offset), (obus, obus_offset))
            self.echo(rs)
        except NoSuchBusError as err:
            print(err.message)
            self.echo(False)
        

        
    def exit_(self, tokens):
        self._exit_repl = True
        self.app.exit()
        
    def load(self, tokens):
        print("FPO load")
        
    def panic(self, tokens):
        print("FPO panic")
        
    def ping(self, tokens):
        print("FPO ping")
        
    def exec_python(self, tokens):
        print("FPO exec_python")
        
    def query(self, tokens):
        print("FPO query")
        
    def save(self, tokens):
        print("FPO save")
        
    def add_synth(self, tokens):
        print("FPO add_synth")
        
