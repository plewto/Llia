# llia.proxy
# Client side representation of LliaHelper instance on SuperCollider
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
from llia.bus import AudioBus, ControlBus
import llia.constants as con

class LliaProxy(object):

    trace = False
    
    def __init__(self, config, app):
        '''
        Constructs new Proxy object.
        
        ARGS:
          config - LliaConfig
          app    - LliaApp
        '''
        self.config = config
        self.app = app
        osc_trace = config.osc_transmission_trace_enabled()
        self.osc_transmitter = OSCTransmitter(self.global_osc_id(), 
                                              self.osc_host(), osc_trace)
        caddress, cport  = config["client"], config["client_port"]
        self.osc_receiver = OSCReceiver(self.global_osc_id(), caddress, cport)
        self._synths = {}
        # initialize protected audio buses
        self._audio_buses = {}
        for i in range(con.PROTECTED_AUDIO_OUTPUT_BUS_COUNT):
            bname = "out_%s" % i
            self._audio_buses[bname] = AudioBus(bname)
        for i in range(con.PROTECTED_AUDIO_INPUT_BUS_COUNT):
            bname = "in_%s" % i
            self._audio_buses[bname] = AudioBus(bname)
        # initialize protected control buses
        self._control_buses = {}
        for i in "AB":
            bname = "CBUS_%s" % i
            self._control_buses[bname] = ControlBus(bname)
        
        self._buffers = {}
        self._callback_message = {}
        for rmsg in ("ping-response", 
                     "booting-server", 
                     "client-address-change",
                     "bus-stats", 
                     "bus-info", 
                     "get-bus-list", 
                     "get-buffer-list",
                     "get-buffer-info", 
                     "get-buffer-info", 
                     "bus-added",
                     "buffer-added"):
            self.osc_receiver.add_handler(rmsg, self._expect_response)
        self.restart()
        #self.sync_to_host()

    def _expect_response(self, path, tags, args, source):
        self._callback_message = {"path" : path,
                                  "tags" : tags,
                                  "args" : args,
                                  "source" : source}

    def status(self, msg):
        '''
        Displays message on status line.
        '''
        self.app.status(msg)
        
    def warning(self, msg):
        '''
        Displays warning on status line.
        '''
        self.app.warning(msg)
    
    def global_osc_id(self):
        return self.config.global_osc_id()

    def osc_host(self):
        '''
        Returns tuple (host-ip-address, port-number)
        '''
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
        '''
        Transmit OSC 'free' message to server.
        In response the server app should free all of it's resources.
        '''
        self._send("free")

    def restart(self):
        '''
        Transmit 'restart' message to server.
        In response the server app should revert to its startup condition.
        All non-protected buses and buffers are freed. All synths are
        freed. 
        '''
        self._send("restart")
        rs = self.expect_osc_response("restarted")
        
    def dump(self):
        self._send("dump")
        pad1 = " "*4
        pad2 = pad1 + " "*4
        print("Llia Proxy Dump")
        print("%soscID   : %s" % (pad1, self.global_osc_id()))
        print("%shost    : %s" % (pad1, self.osc_host()))
        print("%sclient  : ('%s', %s)" % (pad1, self.config["client"], 
                                          self.config["client_port"]))
        print("%saudio buses:" % pad1)
        for k in sorted(self._audio_buses.keys()):
            b = str(self._audio_buses[k])
            print("%s%s" % (pad2, b))
        print("%scontrol buses:" % pad1)
        for k in sorted(self._control_buses.keys()):
            b = str(self._control_buses[k])
            print("%s%s" % (pad2, b))
        
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
        '''
        Transmits 'panic' message to server.
        In response the server should silence all notes.
        '''
        self._send("panic")

    def post(self, text):
        '''
        Post (SupperColliders term for print) text to SuperCollider's 
        post window.  Does not include line feed.
        '''
        self._send("post", [text])

    def postln(self, text):
        '''
        Same as post but includes line feed.
        '''
        self._send("postln", [text])
        
    def get_bus_list(self, rate):
        '''
        Request server to send a list of all allocated buses.

        ARGS:
          rate - String, either 'audio' or 'control'

        RETURNS: list
        '''
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
        '''
        Request information from server about a specific bus.
        
        ARGS:
          rate    - String, either 'audio' or 'control'
          busName - String
        
        RETURNS: dictionary with keys: 'name', 'rate', 'index' and 'channels'

        Application may exit if more then one instance of Llia client with 
        the same OSC credentials are running.
        '''
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
        '''
        Requst server to send list of buffers.
        
        RETURNS: list
        '''
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
        '''
        Request server send information about specific buffer.

        ARGS:
          bname - String, the buffer name.

        RETURNS: dictionary with following keys:
                  "name", "index", "frames", "channels"
                   "sample-rate" and "filename"

        The filename property is used if the buffer contents have been 
        loaded from a file.
        '''
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


    def create_wavetable(self, name, maxharm=64, decay=0.5, skip=None,
                         mode="", cutoff=None, depth=0.5, frames=1024):
        '''
        Creates new buffer on the server and fill it with a wave data.

        ARGS:
           name    - String, buffer name
           maxharm - int, maximum harmonic
           decay   - float, sets how partial amplitudes are determined 
                     as a function of harmonic number.
           skip    - int, sets number of harmonics to skip.
                     2 -> odd only (1,3,5,...)
                     3 -> every third (1,2,4,5,7,...)
           mode    - String, simulated filter mode.
                     ISSUE: FIXME determine valid values.
           cutoff  - int, simulated filter cutoff in terms of harmonic 
                     number
           depth   - float, simulated filter 'depth'
           frames  - int number of buffer frames, must be power of 2.

        '''
        if self.buffer_exists(name):
            self.warning("Buffer %s already exists" % name)
            return False
        else:
            skip = skip or maxHarm+1
            if cutoff is None: cutoff = maxHarm/2
            payload = [name, maxharm, decay, skip, mode, cutoff, depth,
                       frames]
            rs = self._send("create-wavetable", payload)
    
    def audio_bus_exists(self, bname):
        '''
        Predicate, returns True if audio bus exists.
        ARGS:
          bname - String

        RETURNS: bool
        '''
        return self._audio_buses.has_key(bname)
    
    def add_audio_bus(self, bname):
        '''
        Add new audio bus.
        If a bus with the same name already exist, do nothing.

        ARGS:
          bname - String

        RETURNS: bool, True if new bus was added.
        '''
        if self.audio_bus_exists(bname):
            return False
        else:
            self._send("add-bus", ["audio", bname, 1])
            abus = AudioBus(bname)
            self._audio_buses[bname] = abus
            return True

    def get_audio_bus(self, bname):
        '''
        Retrieve Bus object

        ARGS:
          bname - String, the bus name

        RETURNS: AudioBus object.

        Raises KeyError if bus does not exits.
        '''
        return self._audio_buses[bname]
        
    def remove_audio_bus(self, bname):
        '''
        Remove audio bus.
        
        NOTE: SynthProxy objects maintain a list of buses connected to them.
        If a bus is removed and some Synth object still thinks it exists
        there may be problems.  

        ARGS:
          bname - String

        Raises LliaError if the bus is protected.  
           The protected buses represent SuperCollider hardware buses and
           have names "out_?" and "in_?"  where ? is a single digit integer.

        Raises NoSuchBusError if matching bus does not exists.
        '''
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

    # def audio_bus_keys(self):
    #     return sorted(self._audio_buses.keys())

    def audio_bus_count(self):
        '''
        Returns int, number of audio buses
        '''
        return len(self._audio_buses)
    
    # # Returns tuple (name, busnum, chancount)
    # def audio_bus_info(self, bname):
    #     try:
    #         bi = self._audio_buses[bname]
    #         return bi
    #     except KeyError:
    #         msg = "Audio bus '%s' does not exists" % bname
    #         self.warning(msg)
    #         return ("", -1, 0)

    def audio_bus_names(self):
        '''
        Returns sorted list of audio bus names
        '''
        return sorted(self._audio_buses.keys())
        
    def list_audio_buses(self):
        '''
        Prints names of all audio buses to terminal.
        This is a convenience diagnostics method.
        '''
        keys = self.audio_bus_names()
        print("Audio buses:")
        for k in keys:
            print("    ", k)
        return keys
    
            
    def control_bus_exists(self, bname):
        '''
        Predicate, test if control bus exists.

        ARGS:
          bname - String

        RETURNS: Bool
        '''
        return self._control_buses.has_key(bname)
        
    def add_control_bus(self, bname):
        '''
        Add new control-bus.
        If a bus with the same name already exists, do nothing.

        ARGS:
          bname - String

        RETURNS: bool, True if bus added.
        '''
        if self.control_bus_exists(bname):
            return False
        else:
            self._send("add-bus", ["control", bname, 1])
            cbus = ControlBus(bname)
            self._control_buses[bname] = cbus
            return True

    def get_control_bus(self, bname):
        '''
        Get named control bus.

        ARGS:
          bname - String

        RETURNS: ControlBus object.

        Raises KeyError if bus does not exists.
        '''
        return self._control_buses[bname]
        
    def remove_control_bus(self, bname):
        '''
        Removed named control bus.

        NOTE 1: The same concerns with removing audio-buses apply to 
                control buses.   Some synth object may still 'think'
                it is connected to a bus which has been removed.

        NOTE 2: There are also protected control buses which should 
                not be removed and this method does not prevent their 
                removal

        Raises KeyError if the bus does not exists,
        '''
        try:
            del self._control_buses[bname]
            self._send("free-bus", ["control", bname])
            return True
        except KeyError:
            raise NoSuchBusError(bname)

    def control_bus_names(self):
        '''
        Returns sorted list of control bus names.
        '''
        return sorted(self._control_buses.keys())
    
    def list_control_buses(self):
        '''
        List control bus names on terminal.
        This is a convenience diagnostics method.
        '''
        keys = sorted(self._control_buses.keys())
        print("Control Buses:")
        for k in keys:
            print("    ", k)
        return keys

    # def control_bus_keys(self):
    #     return sorted(self._control_buses.keys())

    def control_bus_count(self):
        '''
        Returns number of control buses.
        '''
        return len(self._control_buses)
    
    # def control_bus_info(self, bname):
    #     try:
    #         bi = self._control_buses[bname]
    #         return bi
    #     except KeyError:
    #         msg = "Control bus '%s' does not exists" % bname
    #         self.warning(msg)
    #         return ("", -1, 0)

        
    def buffer_exists(self, bname):
        '''
        Predicate test is named buffer exists.
        '''
        return self._buffers.has_key(bname)


    def buffer_info(self, bname):
        '''
        Returns information about named buffer.

        WARNING: buffer implementation may change in the future.
                 The return type for this method should not be
                 relied on. 

        '''
        print("WARNING: LliaProxy.buffer_info is an unsafe method")
        return self._buffers[bname]
    
    def buffer_names(self):
        '''
        Returns list of buffer names.
        '''
        return sorted(self._buffers.keys())

    def list_buffers(self):
        '''
        Prints names of all buffers to terminal.
        This is a convenience diagnostics method.
        '''
        keys = sorted(self._buffers.keys())
        print("Buffers:")
        for k in keys:
            print("    ", k)
        return keys
    
    def buffer_count(self):
        '''
        Returns number of allocated buffers.
        '''
        return len(self._buffers)
    
    def add_buffer(self, bname, frames=1024, channels=1):
        '''
        Add a new buffer.
        If a buffer with the same name already exists, do nothing

        ARGS:
          bname  - String, buffer name
          frames - int, must be power of 2 if buffer is used as a wave-table
          channels - int 

        RETURNS: bool, True if buffer was added.
        '''
        if self.buffer_exists(bname):
            self.warning("Buffer %s already exists" % bname)
            return False
        else:
            self._send("add-buffer", [bname, frames, channels])
            rs = self.expect_osc_response("buffer-added")
            #self.sync_to_host()
            return rs

    def remove_buffer(self, bname):
        '''
        Remove named buffer.

        ARGS: 
          String - buffer name.

        Raises NoSuchBufferError if buffer does not exists. 
        '''
        if self.buffer_exists(bname):
            del self._buffers[bname]
            self._send("free-buffer", [bname])
        else:
            raise NoSuchBufferError(bname)
            
    def synth_exists(self, stype, id_, sid=None):
        '''
        Predicate returns True if synth exists.

        ARGS:
          stype - String
          id_   - int
          sid   - optional String

        The synth may be specified either by its type and id, or by its sid
        If sid is specified stype and id_ are ignored.
        
        RETURNS: bool
        '''
        sid = sid or "%s_%d" % (stype, int(id_))
        return self._synths.has_key(sid)

    def get_synth(self, sid):
        '''
        Get synth object.

        ARGS:
          sid - String

        RETURNS: SynthProxy
        '''
        rs = self._synths[sid]
        return rs

    def get_all_synths(self):
        '''
        Returns list of all SynthProxy objects.
        '''
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
        '''
        Diagnostic method, print names of all (non-efx) synths.
        '''
        acc = []
        print("Synths:")
        for k in sorted(self._synths.keys()):
            sy = self._synths[k]
            if not sy.is_efx:
                acc.append(self._list_synth(sy))
        return acc

    def list_efx(self):
        '''
        Diagnostic method, print names of all efx synths
        '''
        acc = []
        print("EFX Synths:")
        for k in sorted(self._synths.keys()):
            sy = self._synths[k]
            if sy.is_efx:
                acc.append(self._list_synth(sy))
        return acc

    def add_synth(self, stype, id_, keymode="Poly1", voice_count=8):
        '''
        Adds new synth

        ARGS:
          stype - String, the synth type, MUST be one of the values found
                  in constants.SYNTH_TYPES
          id_   - int, synth serial number.  id_ MUST be unique for any 
                  given stype.
          keymode     - String, the keymode, MUST be a value found in 
                        constants.KEY_MODES.  NOTE: Most synths do not 
                        support all possible key modes.
          voice_count - int, number of allocated voices.
                        voice_count is only used if keymode has a finite
                        voice allocation, otherwise it is ignored.
        RETURNS: SynthProxy if the synth was added,
                 None if the synth could not be added.
        '''
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
                return sy

    def add_efx(self, stype, id_):
        '''
        Add effect synth.
        
        ARGS:
          stype - String, the synth type, MUST match a value found in 
                  constants.EFFECT_TYPES

          id_  - int, synth serial number, MUST be unique for any given stype

        RETURNS: SynthProxy if synth was added.
                 None is synth could not be added.
        '''
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
                return sy

    def free_synth(self, stype, id_):
        '''
        Free indicated synth.

        WARNING: This method alone does not completely clean up
                 after a synth has been removed.  Specifically
                 prior to a synth being removed from the application,
                 it must first be removed from any AudioBus or ControlBus
                 sink/source list it may be connected to.

                 Additionally any GUI editor for the synth should be 
                 destroyed before the synth is removed.
        
        free_synth is used for both 'normal' synths ad 'efx' synths.
        

        ARGS:
          stype - String, the synth type
          id_   - int, the synth id.

        Raises KeyError if indicated synth does not exists.
        '''
        sid = "%s_%s" % (stype, id_)
        try:
            del self._synths[sid]
            self._send("free-synth", [sid])
        except KeyError:
            raise NoSuchSynthError(sid)

    def assign_synth_audio_bus(self, stype, id_, param, bus_name, offset=0):
        '''
        Assign server-side audio bus to synth parameter.
        This method only applies to the server application and does not 
        make any modifications to client-side synth and bus objects.

        ARGS:
          stype    - String, the synth type
          id_      - int, the synth serial id.
          param    - String, the synth parameter used to connect to the bus.
          bus_name - String.
          offset   - int, legacy argument, sets the bus number offset,
                     should always be 0.
        '''
        payload = [stype, id_, param, bus_name, offset]
        rs = self._send("assign-synth-audio-bus", payload)


    def assign_synth_control_bus(self, stype, id_, param, bus_name, offset=0):
        '''
        Assign server-side control bus to synth parameter.
        This method only applies to the server application and does not 
        make any modifications to client-side synth and bus objects.

        ARGS:
          stype    - String, the synth type
          id_      - int, the synth serial id.
          param    - String, the synth parameter used to connect to the bus.
          bus_name - String.
          offset   - int, legacy argument, sets the bus number offset,
                     should always be 0.
        '''
        payload = [stype, id_, param, bus_name, offset]
        rs = self._send("assign-synth-control-bus", payload)


    # def assign_synth_buffer(self, stype, id_, param, buffer_name):
    #     print("WARNING: proxy.assign_synth_buffer disabled")
    #     payload = [stype, id_, param, buffer_name]
    #     rs = self._send("assign-synth-buffer", payload)
    #     sid = "%s_%s" % (stype, id_)
    #     sy = self.get_synth(sid)
    #     #sy.buffers[params] = buffer_name

    # def plot_buffer(self, buffer_name):
    #     payload = [buffer_name]
    #     rs = self._send("plot-buffer", payload)
        
    # def sync_to_host(self):
    #     pass
        #self._audio_buses = {}
        #self._control_buses = {}
        #self._buffers = {}
        # abl = self.get_bus_list("audio")
        # for bname in abl:
        #     binfo = self.get_bus_info("audio", bname)
        #     bname = binfo["name"]
        #     index = int(binfo["index"])
        #     chans = int(binfo["channels"])
        #     self._audio_buses[bname] = (bname, index, chans)
        # cbl = self.get_bus_list("control")
        # for bname in cbl:
        #     binfo = self.get_bus_info("control", bname)
        #     bname = binfo["name"]
        #     index = int(binfo["index"])
        #     chans = int(binfo["channels"])
        #     self._control_buses[bname] = (bname, index, chans)
        # bls = self.get_buffer_list()
        # for bname in bls:
        #     binfo = self.get_buffer_info(bname)
        #     if binfo:
        #         self._buffers[bname] = binfo      
                
