# llia.lliascript.bufferhelper
# 2016.05.16
# Extends Parser with buffer related commands.
# For the moment Buffer support has been disabled.

from __future__ import print_function

from llia.lliascript.ls_constants import *
from llia.llerrors import NoSuchBufferError, LliaError


class BufferHelper(object):

    def __init__(self, parser, local_namespace):
        self.parser = parser
        self.proxy = parser.proxy
        self.current_buffer = ""
        self._init_namespace(local_namespace)

    def _init_namespace(self, ns):
        ns["buffer"] = self.add_buffer
        ns["wavetab"] = self.create_wave_table
        ns["with_buffer"] = self.with_buffer
        ns["list_buffers"] = self.list_buffers
        # ns["sinetab"] = self.create_sine_table
        # ns["sawtab"] = self.create_wave_table
        # ns["pulsetab"] = self.create_pulse_table
        # ns["rm_buffer"] = self.remove_buffer

    def status(self, msg):
        self.parser.status(msg)

    def warning(self, msg):
        self.parser.warning(msg)

    def update_prompt(self):
        pass
    
    def buffer_exists(self, name=None):
        name = name or self.current_buffer
        rs = self.proxy.buffer_exists(name)
        return rs

    def what_is(self, name):
        return self.parser.what_is(name)
    
    def with_buffer(self, name=None):
        name = name or self.current_buffer
        if self.buffer_exists(name):
            self.current_buffer = name
            msg = "Using buffer: %s" % name
            self.status(msg)
            self.update_prompt()
            return self.proxy.get_buffer(name)
        else:
            raise NoSuchBufferError(name)
        
    def add_buffer(self, name, frames=1024, channels=1):
        if self.buffer_exists(name):
            self.status("Using existing buffer '%s'" % name)
            return self.with_buffer(name)
        lstype = self.what_is(name)
        if lstype:
            msg = "Can not change %s '%s' to buffer"
            self.warning(msg % (lstype, name))
            return False
        flag = self.parser.register_entity(name, 
                                           "buffer",
                                           {"frames" : frames,
                                            "channels" : channels,
                                            "filename": ""})
        if flag:
            bobj = self.proxy.add_buffer(name, frames, channels)
            self.with_buffer(name)
            return bobj
        else:
            return False

    def create_wave_table(self, name, harmonics=512, decay=0.55, skip=-1,
                          cutoff=-1, mode="", depth=0.5, frames=1024):
        if self.buffer_exists(name):
            self.status("Using existing buffer '%s'" % name)
            return self.with_buffer(name)
        lstype = self.what_is(name)
        if lstype:
            msg = "Can not change %s '%s' to buffer"
            self.warning(msg % (lstype, name))
        bobj = self.proxy.create_wavetable(name, harmonics, decay, skip, mode,
                                           cutoff, depth, frames)
        self.parser.register_entity(name,
                                     "buffer",
                                     {"is-wavetable" : True,
                                      "harmonics" : harmonics,
                                      "decay" : decay,
                                      "skip" : skip,
                                      "mode" : mode,
                                      "cutoff" : cutoff,
                                      "depth" : depth,
                                      "frames" : frames,
                                      "filename" : ""})
        return self.with_buffer(name)
   
    
    # def create_sine_table(self, name, frames=1024):
    #     return self.create_wave_table(name, 1, frames=frames)

    # def create_pulse_table(self, name, harmonics=512, skip=2, frames=1024):
    #     if skip <= 1:
    #         decay = 0
    #         skip = harmonics+1
    #     else:
    #         decay = 1
    #     return self.create_wave_table(name, harmonics, decay, skip, frames=frames)
    
    # def remove_buffer(self, name):
    #     if self.what_is(name) == "buffer":
    #         self.proxy.remove_buffer(name)
    #         self.parser.forget(name)
    #         self.status("Removed buffer: '%s'" % name)
    #         return True
    #     else:
    #         raise NoSuchBufferError(name)

    def remove_buffer(self, name):
        if name in PROTECTED_BUFFERS:
            msg = "Can not remove protected buffer: '%s'" % name
            raise LliaError(msg)
        if self.what_is(name) == 'buffer':
            self.proxy.remove_buffer(name)
            self.parser.forget(name)
            self.status("Buffer '%s' removed" % name)
            return True
        else:
            raise NoSuchBuffersError(name)
            
    def list_buffers(self):
        lst = self.proxy.buffer_names()
        print(lst)
        return lst
    
