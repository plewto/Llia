# llia.proxy
# 2016.04.20
#

from __future__ import print_function
from time import sleep
import sys

from llia.llerrors import (LliaPingError, LliaError, NoSuchSynthError,
                           NoSuchBusError, NoSuchBufferError)
from llia.osc_transmitter import OSCTransmitter
from llia.osc_receiver import OSCReceiver
from llia.synth_proxy import SynthSpecs
from llia.generic import is_int

class LliaProxy(object):

    trace = False
    
    def __init__(self, config, app):
        self.config = config
        self.app = app
        osc_trace = config.osc_transmission_trace_enabled()
        self.osc_transmitter = OSCTransmitter(self.global_osc_id(), self.osc_host(), osc_trace)
        caddress, cport  = config["client"], config["client_port"]
        self.osc_receiver = OSCReceiver(self.global_osc_id(), caddress, cport)
        self._synths = {}
        self._audio_buses = {}
        self._control_buses = {}
        self._buffers = {}
        self._callback_message = {}
        for rmsg in ("ping-response", "booting-server", "client-address-change",
                     "bus-stats", "bus-info", "get-bus-list", "get-buffer-list",
                     "get-buffer-info", "get-buffer-info", "bus-added",
                     "buffer-added"):
            self.osc_receiver.add_handler(rmsg, self._expect_response)
        self.sync_to_host()
        
    # def init(self):
    #     self._synths = {}
    #     self._audio_buses = {}
    #     self._control_buses = {}
    #     self._bufers = {}
    #     self.establish_default_buses()
    #     self.status("LliaProxy initialized")

    def _expect_response(self, path, tags, args, source):
        self._callback_message = {"path" : path,
                                  "tags" : tags,
                                  "args" : args,
                                  "source" : source}

    def status(self, msg):
        self.app.status(msg)
        
    def warning(self, msg):
        self.app.warning(msg)
    
    def global_osc_id(self):
        return self.config.global_osc_id()

    def osc_host(self):
        return self.config["host"], self.config["port"]

    # Returns dictionary from current callback
    # The callback dictionary may only be read once.
    # Once read the dictionary contents are cleared.
    #
    def _get_callback_message(self):
        rs = self._callback_message.copy()
        self._callback_message = {}
        return rs

    # Check callback dictionary for expected response message
    # Return True if expected message has been received.
    # Return False otherwise
    #
    def expect_osc_response(self, msg):
        rs = False
        try:
            sleep(0.05)
            self.osc_receiver.handle_request()
            cbm = self._get_callback_message()
            # print("DEBUG Proxy._expect cbm -> %s", cbm)
            msg = "/Llia/%s/%s" % (self.global_osc_id(), msg)
            rs = msg == cbm["path"]
        except KeyError:
            wmsg = "Did not receive expected response: '%s'" % msg
            self.warning(wmsg)
        finally:
            return rs

    # Transmit OSS message
    # msg     - ~/oscID/msg
    # payload - optional data
    #
    def _send(self, msg, payload=[]):
        if LliaProxy.trace:
            print("LliaProxy._send '%s' %s" % (msg, payload))
        self.osc_transmitter.send(msg, payload)

    # Request host to return value(s)
    # msg - /oscID/msg
    # returns -> list
    def _query_host(self, msg, payload=[], delim=" "):
        self._send(msg, payload)
        self.osc_receiver.handle_request()
        cbm = self._get_callback_message()
        args = cbm.get("args", [""])
        # args = args[0].split(delim)
        return args

    # Requst ping-response from host
    # transmit Llia/oscID/ping
    # response -> ping-response
    # returns bool
    def ping(self):
        self._send("ping")
        rs = self.expect_osc_response("ping-response")
        if not rs:
            msg = "Did not receive expected ping response from '/Llia/%s'"
            msg = msg % self.global_osc_id()
            raise LliaPingError(msg)
        return rs
    
    def free(self):
        self._send("free")
    
    def dump(self):
        self._send("dump")
        pad1 = " "*4
        pad2 = pad1 + " "*4
        print("Llia Proxy Dump")
        print("%soscID   : %s" % (pad1, self.global_osc_id()))
        print("%shost    : %s" % (pad1, self.osc_host()))
        print("%sclient  : ('%s', %s)" % (pad1, self.config["client"], self.config["client_port"]))
        print("%saudio buses:" % pad1)
        abl = self._audio_buses.keys()
        acc = []
        for b in abl:
            binfo = self._audio_buses[b]
            acc.append(binfo)
        acc = sorted(acc, key=lambda n: n[1])
        for binfo in acc:
            print("%sindex: %3d, name: '%-12s', channels: %s" % (pad2, binfo[1], binfo[0], binfo[2]))
        print("%scontrol buses:" % pad1)
        abl = self._control_buses.keys()
        acc = []
        for b in abl:
            binfo = self._control_buses[b]
            acc.append(binfo)
        acc = sorted(acc, key=lambda n: n[1])
        for binfo in acc:
            print("%sindex: %3d, name: '%-12s', channels: %s" % (pad2, binfo[1], binfo[0], binfo[2]))
        print("%sbuffers:" % pad1)
        frmt = "%sindex: %3d, name: '%-12s', frames: %4d, channels: %2d, "
        frmt = frmt + "sr: %d,  filename: '%s'"
        for b in sorted(self._buffers.keys()):
            binfo = self._buffers[b]
            index = binfo["index"]
            bname = binfo["name"]
            frames = binfo["frames"]
            chans = binfo["channels"]
            sr = binfo["sample-rate"]
            filename = binfo["filename"]
            print(frmt % (pad2, index, bname, frames, chans, sr, filename))
        print("%sSynths:" % pad1)
        for s in sorted(self._synths.keys()):
            print("%s%s" % (pad2, s))
        
    def boot_server(self, s="default"):
        self._send("boot-server", [s])
        sleep(2)
        return self.expect_osc_response("booting-server")

    # BROKEN see BUG 0001
    def id_self(self):
        ip, port = self.config["client"], self.config["client_port"]
        payload = [self.global_osc_id(), ip, port]
        print("BUG 0001 id_self disabled")
        # self._send("set-client", payload)
        # self.expect_osc_response("ping-response")
        return False

    def panic(self):
        self._send("panic")

    def post(self, text):
        self._send("post", [text])

    def postln(self, text):
        self._send("postln", [text])
        
    def get_bus_list(self, rate):
        payload = [rate]
        raw = self._query_host("get-bus-list", payload)[0].strip().split(" ")
        acc = []
        if len(raw) > 4:
            for r in raw[2:-1]:
                if r[-1] == ",":
                    acc.append(r[:-1])
                else:
                    acc.append(r)
        return acc
    
    def get_bus_info(self, rate, busName):
        payload = [rate, busName]
        raw = self._query_host("get-bus-info", payload)[0].strip().split(" ")
        rs = {"name" : "DOES-NOT-EXISTS",
              "rate" : -1,
              "index" : -1,
              "channels" : -1}
        if raw[0] != 'DOES-NOT-EXISTS':
            try:
                rs = {"name" : raw[0],
                      "rate" : raw[1],
                      "index": int(raw[2]),
                      "channels": int(raw[3])}
            except ValueError:
                msg = "\n***************************************************\n"
                msg += "*** ValueError in LliaProxy.get_bus_info        ***\n"
                msg += "*** We have seen this before.  Check that there ***\n"
                msg += "*** are not two copies of Llia with identical   ***\n"
                msg += "*** global OSC ids running on the host.         ***\n"
                msg += "***************************************************\n"
                print(msg)
                sys.exit(1)
        return rs

    def get_buffer_list(self):
        raw = self._query_host("get-buffer-list")[0].strip().split(" ")
        raw = raw[1:-1]
        acc = []
        for r in raw:
            if r and r[-1] == ",":
                acc.append(r[:-1])
            else:
                acc.append(r)
        if acc == ['']: acc = []        
        return acc

    def get_buffer_info(self, bname):
        raw = self._query_host("get-buffer-info", [bname])[0]
        raw = raw.split(" ")
        if raw[1] == "DOES-NOT-EXISTS":
            return None
        raw_filename = raw[5:]
        if raw_filename == ['nil']:
            fname = None
        else:
            # Attempt to reconstruct pathological filenames with embedded
            # spaces.  If the filename contains more then 1 consecutive
            # spaces, it will not be reconstructed properly.
            # 
            fname = ""
            for p in raw_filename:
                fname = fname + p + " "
            fname = fname.strip()
        bname, index, frames, channels, sr = raw[:5]
        def asInt(key, value, default):
            try:
                v = int(value)
                return v
            except ValueError:
                msg = "WARNING: LliaProxy.get_buffer_info %s = %s" % (key, value)
                print(msg)
                return default
        bname = str(bname)
        rs = {"name" : bname,
              "index" : asInt("index", index, 0),
              "frames" : asInt("frames", frames, 1024),
              "channels" : asInt("channels", channels, 1),
              "sample-rate" : asInt("sample-rate", sr, 44100),
              "filename" : fname}
        return rs


    def create_wavetable(self, name, maxharm=64, decay=0.5, skip=None, mode="",
                          cutoff=None, depth=0.5, frames=1024):
        if self.buffer_exists(name):
            self.warning("Buffer %s already exists" % name)
            return False
        else:
            skip = skip or maxHarm+1
            if cutoff is None: cutoff = maxHarm/2
            payload = [name, maxharm, decay, skip, mode, cutoff, depth, frames]
            rs = self._send("create-wavetable", payload)
    
    def audio_bus_exists(self, bname):
        return self._audio_buses.has_key(bname)
    
    def add_audio_bus(self, bname, channels=1):
        rate = "audio"
        if self.audio_bus_exists(bname):
            #self.warning("Audio bus %s already exists" % bname)
            return False
        else:
            self._send("add-bus", [rate, bname, channels])
            rs = self.expect_osc_response("bus-added")
            self.sync_to_host()
            return rs

    def remove_audio_bus(self, bname):
        if bname[:4] == "out_" or bname[:3] == "in_":
            msg = "Can not remove protected audio bus: '%s'." % bname
            raise LliaError(msg)
        else:
            try:
                del self._audio_buses[bname]
                self._send("free-bus", ["audio", bname])
                return True
            except KeyError:
                raise NoSuchBusError(bname)
        
    def control_bus_exists(self, bname):
        return self._control_buses.has_key(bname)
        
    def add_control_bus(self, bname, channels=1):
        rate = "control"
        if self.control_bus_exists(bname):
            #self.warning("Control bus %s already exists"  % bname)
            return False
        else:
            self._send("add-bus", [rate, bname, channels])
            rs = self.expect_osc_response("bus-added")
            self.sync_to_host()
            return rs

    def remove_control_bus(self, bname):
        try:
            del self._control_buses[bname]
            self._send("free-bus", ["control", bname])
            return True
        except KeyError:
            raise NoSuchBusError(bname)
        
    def buffer_exists(self, bname):
        return self._buffers.has_key(bname)

    def buffer_info(self, bname):
        return self._buffers[bname]

    def buffer_keys(self):
        return sorted(self._buffers.keys())

    def buffer_count(self):
        return len(self._buffers)
    
    def add_buffer(self, bname, frames=1024, channels=1):
        if self.buffer_exists(bname):
            self.warning("Buffer %s already exists" % bname)
            return False
        else:
            self._send("add-buffer", [bname, frames, channels])
            rs = self.expect_osc_response("buffer-added")
            self.sync_to_host()
            return rs

    def remove_buffer(self, bname):
        if self.buffer_exists(bname):
            del self._buffers[bname]
            self._send("free-buffer", [bname])
        else:
            raise NoSuchBufferError(bname)

    def audio_bus_keys(self):
        return sorted(self._audio_buses.keys())

    def audio_bus_count(self):
        return len(self._audio_buses)
    
    # Returns tuple (name, busnum, chancount)
    def audio_bus_info(self, bname):
        try:
            bi = self._audio_buses[bname]
            return bi
        except KeyError:
            msg = "Audio bus '%s' does not exists" % bname
            self.warning(msg)
            return ("", -1, 0)
    
    def list_audio_buses(self):
        keys = self.audio_bus_keys()
        print("Audio buses:")
        for k in keys:
            print("    ", k)
        return keys
            
    def list_control_buses(self):
        keys = sorted(self._control_buses.keys())
        print("Control Buses:")
        for k in keys:
            print("    ", k)
        return keys

    def control_bus_keys(self):
        return sorted(self._control_buses.keys())

    def control_bus_count(self):
        return len(self._control_buses)
    
    def control_bus_info(self, bname):
        try:
            bi = self._control_buses[bname]
            return bi
        except KeyError:
            msg = "Control bus '%s' does not exists" % bname
            self.warning(msg)
            return ("", -1, 0)
            
    def list_buffers(self):
        keys = sorted(self._buffers.keys())
        print("Buffers:")
        for k in keys:
            print("    ", k)
        return keys
            
    def synth_exists(self, stype, id_, sid=None):
        sid = sid or "%s_%d" % (stype, int(id_))
        return self._synths.has_key(sid)

    def get_synth(self, sid):
        rs = self._synths[sid]
        # print("Proxy.get_synth  sid %s   '%s'   rs -> %s" % (type(sid), sid, rs))
        return rs

    def get_all_synths(self):
        return self._synths.values()
    
    @staticmethod
    def _list_synth(sy):
        specs = sy.specs
        stype = specs["format"]
        id_ = sy.id_
        sid = "%s_%s" % (stype, id_)
        print("    %s" % sid)
        return sid
    
    def list_synths(self):
        acc = []
        print("Synths:")
        for k in sorted(self._synths.keys()):
            sy = self._synths[k]
            if not sy.is_efx:
                acc.append(self._list_synth(sy))
        return acc

    def list_efx(self):
        acc = []
        print("EFX Synths:")
        for k in sorted(self._synths.keys()):
            sy = self._synths[k]
            if sy.is_efx:
                acc.append(self._list_synth(sy))
        return acc

    def add_synth(self, stype, id_, keymode="Poly1", voice_count=8):
       sid = "%s_%d" % (stype, int(id_))
       if self.synth_exists(stype, id_):
           msg = "Synth %s already exists" % sid
           self.warning(msg)
           return False
       else:
           sy = SynthSpecs.create_synth_proxy(self.app, stype, id_)
           if not sy:
               msg = "Synth %s could not be created" % sid
               self.warning(msg)
               return False
           else:
               print("Creating synth: %s" % sid)
               self._synths[sid] = sy
               self._send("add-synth", [stype, id_, keymode, voice_count])
               return True

    def add_efx(self, stype, id_):
        sid = "%s_%d" % (stype, id_)
        if self.synth_exists(stype, id_):
            msg = "EFX Synth %s already exists" % sid
            self.warning(msg)
            return False
        else:
            sy = SynthSpecs.create_synth_proxy(self.app, stype, id_)
            if not sy:
                msg ="EFX Synth %s could not be created" % sid
                self.warning(msg)
                return False
            else:
                sy.is_efx = True
                self._synths[sid] = sy
                self._send("add-efx", [stype, id_])
                return True

    def free_synth(self, stype, id_):
        sid = "%s_%s" % (stype, id_)
        try:
            del self._synths[sid]
            self._send("free-synth", [sid])
        except KeyError:
            raise NoSuchSynthError(sid)
            
    def assign_synth_audio_bus(self, stype, id_, param, bus_name, offset):
        payload = [stype, id_, param, bus_name, offset]
        rs = self._send("assign-synth-audio-bus", payload)

    def assign_synth_control_bus(self, stype, id_, param, bus_name, offset):
        payload = [stype, id_, param, bus_name, offset]
        rs = self._send("assign-synth-control-bus", payload)

    def assign_synth_buffer(self, stype, id_, param, buffer_name):
        payload = [stype, id_, param, buffer_name]
        rs = self._send("assign-synth-buffer", payload)

    def plot_buffer(self, buffer_name):
        payload = [buffer_name]
        rs = self._send("plot-buffer", payload)
        
    def sync_to_host(self):
        self._audio_buses = {}
        self._control_buses = {}
        self._buffers = {}
        abl = self.get_bus_list("audio")
        for bname in abl:
            binfo = self.get_bus_info("audio", bname)
            bname = binfo["name"]
            index = int(binfo["index"])
            chans = int(binfo["channels"])
            self._audio_buses[bname] = (bname, index, chans)
        cbl = self.get_bus_list("control")
        for bname in cbl:
            binfo = self.get_bus_info("control", bname)
            bname = binfo["name"]
            index = int(binfo["index"])
            chans = int(binfo["channels"])
            self._control_buses[bname] = (bname, index, chans)
        bls = self.get_buffer_list()
        for bname in bls:
            binfo = self.get_buffer_info(bname)
            if binfo:
                self._buffers[bname] = binfo        
