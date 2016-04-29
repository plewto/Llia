# llia.lsl.parser
# 2016.04.27

from __future__ import print_function
import sys

from llia.lsl.lsl_constants import *

class LSLParser(object):

    def __init__(self, app):
        super(LSLParser, self).__init__()
        self.app = app
        self.proxy = app.proxy
        self._exit = False

    def repl(self):
        print(BANNER)
        print(VERSION)
        print()
        pyver = sys.version_info[0]
        if pyver <= 2:
            infn = raw_input
        else:
            infn = input
        while not self._exit:
            usrin = infn("Llia> ")
            self.parse_line(usrin)

    def log(self, tokens):
        print(tokens)  # ISSUE: FPO   FIX ME

    def error(self, msg):
        print("# ERROR: %s" % msg)
        self.log(msg)
        
    @staticmethod
    def tokenize(line):
        tokens = line.split(" ")
        return tokens
    
    def parse_line(self, line):
        tokens = self.tokenize(line)
        cmd, args = tokens[0], tokens[1:]
        cmd = cmd.upper()
        self.log(tokens)
        if cmd == REMARK:
            return
        elif cmd == "TEST":
            print(self.proxy.q_bus_and_buffer_info())
        elif cmd == "?":        # Help
            pass
        elif cmd == "ABUS":    # Add audio bus
            self.add_audio_bus(args)
        elif cmd == "CBUS":    # Add control bus
            self.add_control_bus(args)
        elif cmd == "EFX":     # Add effects
            self.add_efx_synth(args)
        elif cmd == "SYNTH":   # Add synth
            self.add_synth(args)
        elif cmd == "BOOT":     # Boot server
            self.boot(args)
        elif cmd == "DUMP":
            pass
        elif cmd == "EXIT":
            self.exit()
        elif cmd == "LOAD":     # Load and execute script file
            pass
        elif cmd == "PY":       # Load python code
            pass
        elif cmd == "Q":        # Query
            pass
        elif cmd == "SAVE":     # Save current state as script
            pass
        elif cmd == "SELECT":   # Select synth
            pass
        else:
            err = "%s Huh? '%s'" % (REMARK, cmd)
            print(err)

    def default_token(self, tokens, index, default):
        try:
            rs = tokens[index]
        except IndexError:
            rs = default
        return rs
            
    def expect(self, tokens, index, test, msg):
        value = tokens[index]
        flag = test(value)
        if not flag:
            self.error(msg)
        return flag

    def expect_n_tokens(self, tokens, n):
        if len(tokens) < n:
            msg = "Expected argument missing"
            self.error(msg)
            return False
        else:
            return True

    def expect_one_of(self, valid_options, token):
        if token in valid_options:
            return True
        else:
            msg = "Expected one of %s, encountered '%s'"
            msg = msg % (valid_options, token)
            self.error(msg)
            return False
    
    def exit(self):
        self._exit = True
        self.app.exit()
        
    def boot(self, tokens):
        server = self.default_token(tokens, 0, "default")
        if self.expect_one_of(("default", "internal", "local"), server):
            rs = self.proxy.boot_server(server)
            print("# %s" % rs)
        return rs
            
    def add_audio_bus(self, tokens):
        # abus name [count]
        if self.expect_n_tokens(tokens, 1):
            name = tokens[0]
            nchans = self.default_token(tokens, 1, 1)
            try:
                nchans = int(nchans)
            except ValueError:
                msg = "Expected int channel count, encountered: %s" % nchans
                self.error(msg)
                return False
            rs = self.proxy.add_audio_bus(name, nchans)
            if not rs:
                self.error("Can not add audio bus '%s'" % name)
            else:
                print("# Added audio bus '%s' with %d channel(s)" % (name, nchans))
            return rs
        else:
            return False

    def add_control_bus(self, tokens):
        # abus name [count]
        if self.expect_n_tokens(tokens, 1):
            name = tokens[0]
            nchans = self.default_token(tokens, 1, 1)
            try:
                nchans = int(nchans)
            except ValueError:
                msg = "Expected int channel count, encountered: %s" % nchans
                self.error(msg)
                return False
            rs = self.proxy.add_control_bus(name, nchans)
            if not rs:
                self.error("Can not add control bus '%s'" % name)
            else:
                print("# Added control bus '%s' with %d channel(s)" % (name, nchans))
            return rs
        else:
            return False

    def add_synth(self, tokens):
        # synth stype id [keymode outbus inbus voive_count]
        if self.expect_n_tokens(tokens, 2):
            stype = tokens[0]
            try:
                id_ = int(tokens[1])
            except ValueError:
                msg = "Expected int OSC synth ID, encountered: %s" % id_
                self.error(msg)
                return False
            keymode = self.default_token(tokens, 2, "Poly1")
            outbus = self.default_token(tokens, 3, 0)
            inbus = self.default_token(tokens, 4, 1000)
            vcount = self.default_token(tokens, 5, 8)
            try:
                vcount = int(vcount)
            except ValueError:
                msg = "Expected int voice count, encountered: %s" % vcount
                self.error(msg)
                return False
            rs = self.proxy.add_synth(stype, id_, keymode, outbus, inbus, vcount)
            if not rs:
                self.error("Could not add synth %s.%s" % (stype, id_))
            return rs
        else:
            return False

    def add_efx_synth(self, tokens):
        # efx stype id inbus [outbus]
        if self.expect_n_tokens(tokens, 3):
            stype = tokens[0]
            try:
                id_ = int(tokens[1])
            except ValueError:
                msg = "Expected int OSC EFX ID, encountered: %s" % id_
                self.error(msg)
                return False
            inbus = tokens[2]
            outbus = self.default_token(tokens, 3, 0)
            rs = self.proxy.add_efx(stype, id_, inbus, outbus)
            if not rs:
                self.error("Could not add efx synth %s.%s" % (stype, id_))
            return rs
        else:
            return False    
