# llia.llscript.bufferhelper
# 2016.05.09
#
# ISSUE: TODO SuperCollider Wavetable class may be useful here.
#

from __future__ import print_function

from llia.llerrors import LliascriptParseError
from llia.llscript.lsutil import parse_positional_args, parse_keyword_args

class BufferHelper(object):

    def __init__(self, parser):
        self.parser = parser
        self.dispatch_table = parser.dispatch_table
        self.proxy = parser.proxy
        self._init_dispatch_table()
        self.current_buffer = ""

    def _init_dispatch_table(self):
        self.dispatch_table["buffer"] = self.add_buffer
        self.dispatch_table["with-buffer"] = self.with_buffer
        self.dispatch_table["?buffer"] = self.buffer_info
        self.dispatch_table["wavetab"] = self.create_wavetable
        # convenience short cuts for wavetab
        self.dispatch_table["sinetab"] = self.create_sinetable    
        self.dispatch_table["sawtab"] = self.create_sawtable
        self.dispatch_table["pulsetab"] = self.create_pulsetable

    def status(self, msg):
        self.parser.status(msg)

    def warning(self, msg):
        self.parser.warning(msg)
        
    def update_prompt(self):
        self.parser.update_prompt()

    def buffer_exists(self, bname):
        blist = self.proxy.get_buffer_list()
        return bname in blist

    # assert that buffer exists
    def assert_buffer(self, bname):
        flag = self.buffer_exists(bname)
        if not flag:
            msg = "Buffer '%s' does not exists" % bname
            self.warning(msg)
        return flag

    def assert_buffer_does_not_exists(self, bname):
        flag = self.buffer_exists(bname)
        if flag:
            msg = "Buffer '%s' already exists" % bname
            self.warning(msg)
        return not flag
    
    def assert_current_buffer(self):
        if not self.current_buffer:
            msg = "No current buffer selected, (use with-buffer)"
            self.warning(msg)
            return False
        else:
            return True
        
    # buffer name [:frames :channels]
    def add_buffer(self, tokens):
        req = ["str", "str"]
        pos = [":frames", ":channels"]
        dflt = {":frames" : ["int", 1024],
                ":channels" : ["int", 1]}
        args = parse_keyword_args(tokens, req, pos, dflt)
        cmd, bname, frames, channels = args
        rs = self.proxy.add_buffer(bname, frames, channels)
        self.with_buffer(["", bname])
        return rs
    
    # with-buffer name
    def with_buffer(self, tokens):
        args = parse_positional_args(tokens, ["str", "str"])
        bname = args[1]
        if self.assert_buffer(bname):
            self.current_buffer = bname
            self.update_prompt()
            return True
        else:
            return False
        
    def buffer_info(self, tokens):
        args = parse_positional_args(tokens, ["str"],[["str", ""]])
        bname = args[1]
        if not bname:
            bname = self.current_buffer
        if self.assert_buffer(bname):
            binfo = self.proxy.get_buffer_info(bname)
            print("Buffer  : '%s'" % bname)
            print("    index    : %d" % binfo["index"])
            print("    frames   : %d" % binfo["frames"])
            print("    channels : %d" % binfo["channels"])
            print("    srate    : %d" % binfo["sample-rate"])
            print("    filename : '%s'" % binfo["filename"])
            return True
        else:
            return False

    # cmd name [:harmonics][:decay][:skip][:mode][:cutoff][:depth][:frames]
    #
    def create_wavetable(self, tokens):
        req = ["str","str"]
        pos = [":harmonics", ":decay", ":skip",
               ":mode", ":cutoff", ":depth", ":frames"]
        kw = {":harmonics" : ["int", 64],
              ":decay" : ["float", 0.5],
              ":skip" : ["int", -1],
              ":mode" : ["str", ""],
              ":cutoff" : ["int", -1],
              ":depth" : ["float", 0.5],
              ":frames" : ["int", 1024]}
        args = parse_keyword_args(tokens, req, pos, kw)
        cmd, name, harm, decay, skip, mode, cutoff, depth, frames = args
        if skip == -1: skip = harm+1
        if cutoff == -1: cutoff = harm/2
        self.proxy.create_wavetable(name, harm, decay, skip, mode, cutoff, depth, frames)
        self.with_buffer(["", name])
        return True

    # cmd name [:frames]
    #
    def create_sinetable(self, tokens):
        req = ["str","str"]
        pos = [":frames"]
        kw = {":frames" : ["int", 1024]}
        args = parse_keyword_args(tokens, req, pos, kw)
        cmd, name, frames = args
        tokens = ["", name,
                  ":harmonics",1,
                  ":decay", 1,
                  ":skip", 2,
                  ":mode", "",
                  ":frames", frames]
        rs = self.create_wavetable(tokens)
        return rs

    # cmd name [:harmonis][:frames]
    #
    def create_sawtable(self, tokens):
        req = ["str", "str"]
        pos = [":harmonics", ":frames"]
        kw = {":harmonics" : ["int", 64],
              ":frames" : ["int", 1024]}
        args = parse_keyword_args(tokens, req, pos, kw)
        cmd, name, harm, frames = args
        tokens = ["", name,
                  ":harmonics", harm,
                  ":decay", 1,
                  ":skip", harm+1,
                  ":mode", "",
                  ":frames", frames]
        rs = self.create_wavetable(tokens)
        return rs

    # cmd name [:harmonics][:skip][:frames]
    #
    def create_pulsetable(self, tokens):
        req = ["str", "str"]
        pos = [":harmonics", ":skip", ":frames"]
        kw = {":harmonics" : ["int", 64],
              ":skip" : ["int", 2],
              ":frames" : ["int", 1024]}
        args = parse_keyword_args(tokens, req, pos, kw)
        cmd, name, harm, skip, frames = args
        if skip <= 1:
            tokens = ["", name, ":harmonics", harm, ":decay", 0,
                      ":skip", harm+1, ":mode", "", ":frames", frames]
        else:
            tokens = ["", name, ":harmonics", harm, ":decay", 0,
                      ":skip", skip, ":mode", "", ":frames", frames]
        rs = self.create_wavetable(tokens)
        return rs
