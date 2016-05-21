# llia.config
# 2016.03.20
#

from __future__ import print_function
import sys, os, os.path
from ConfigParser import RawConfigParser,NoOptionError,NoSectionError

import llia.constants as constants
from llia.alias import CCAssignments, ChannelAssignments

# MSG_NO_MIDI_PORT = """
# ERROR:
# No MIDI input port specified.
# A MIDI input port must be specified in at least one of the following
# locations (in order of precedence)
#
#     1) --midiin command line option.
#     2) via the configuration file.
#     3) the LLIA_MIDI_IN environmental variable.
#
# Use --midi_ports command line flag to see a list of available ports.
# """

MSG_NO_CONFIG_FILE = """
ERROR:
Could not locate startup configuration file '%s'
Try either creating it or specify an alternative
location with command line option --config or
environmental variable LLIA_CONFIG.

A suitable default configuration file may be found
in the Llia resource folder.
"""

def _non_support_message(os):
    msg = '''Default config file for %s is not supported at this time.
Use either --config command line argument are LLIA_CONFIG environment
variable.'''
    print()
    print(msg % os)
    print()
    sys.exit(1)

class LliaConfig(dict):

    @staticmethod
    def create_instance(args):
        filename = args.config
        if not filename:
            try:
                filename = os.environ["LLIA_CONFIG"]
            except KeyError:
                platform = (sys.platform).lower()
                print("Trying default platform configuration: %s" % platform)
                if platform.startswith("linux"):
                    filename = "~/.config/Llia/config"
                elif platform.startswith("darwin"): # ISSUE: OSX Portability
                    _non_support_message("OSX")
                elif platform.startswith("win32"): # ISSUE: Windows Portability
                    _non_support_message("Windows")
                else:
                    _non_support_message(sys.platform)
        filename = os.path.expanduser(filename)
        if not os.path.exists(filename):
            msg = MSG_NO_CONFIG_FILE % filename
            print("%s\n" % msg)
            sys.exit(0)
        print("Using configuration file '%s'" % filename)
        return LliaConfig(filename, args)
    
    def __init__(self, filename, args):
        dict.__init__(self)
        self.filename = filename
        self._parser = RawConfigParser()
        self._parser.read(filename)
        self._select_backend(args)
        self._select_midi_input_port(args)
        self._select_midi_output_port(args)
        self._select_default_host_and_client(args)
        self._select_gui(args)
        # self._midi_receiver = None
        # self._midi_transmitter = None
        self.controller_assignments = CCAssignments(self._parser)
        self.channel_assignments = ChannelAssignments(self._parser)
        
    def _select_backend(self, args):
        try:
            env = os.environ["LLIA_BACKEND"]
        except KeyError:
            env = None
        options = ("mido.backends.rtmidi", "mido.backends.portmidi")
        sources = (args.backend, self._parser.get("MIDI", "backend"), env)
        backend = None
        for s in sources:
            if s:
                backend = s
                break
        if backend not in options:
            print("\nERROR:")
            print("Invalid mido backend: '%s'" % backend)
            print("Valid options are:")
            for o in options:
                print("\t%s" % o)
            print()
            sys.exit(1)
        else:
            self["backend"] = backend
            os.environ["MIDO_BACKEND"] = backend
            print("Backend: %s" % backend)
                  
    # def _select_midi_input_port(self, args):
    #     try:
    #         env = os.environ["LLIA_MIDI_IN"]
    #     except KeyError:
    #         env = None
    #     sources = (args.midiin, self._parser.get("MIDI", "input-port"), env)
    #     port_name = None
    #     for s in sources:
    #         if s:
    #             port_name = s
    #             break
    #     if not port_name:
    #         print(MSG_NO_MIDI_PORT)
    #         # sys.exit(1)
    #     self["midi-receiver-name"] = port_name
    #     print("MIDI input port: '%s'" % port_name)


    def _select_midi_input_port(self, args):
        try:
            env = os.environ["LLIA_MIDI_IN"]
        except KeyError:
            env = None
        sources = (args.midiin, self._parser.get("MIDI", "input-port"), env)
        port_name = None
        for s in sources:
            if s:
                port_name = s
                break
        # if not port_name:
        #     print(MSG_NO_MIDI_PORT)
        #     # sys.exit(1)
        if port_name:
            self["midi-receiver-name"] = port_name
        else:
            self["midi-receiver-name"] = None
                
    def _select_midi_output_port(self, args):
        try:
            env = os.environ["LLIA_MIDI_OUT"]
        except KeyError:
            env = None
        #sources = (args.midiout, self._parser.get("MIDI","output-port"),
        #           env, self["midi-receiver-name"])

        sources = (args.midiout, self._parser.get("MIDI","output-port"),env)
        port_name = None
        for s in sources:
            if s:
                port_name = s
                break
        # if not port_name:
        #     raise RuntimeError("No MIDI output port")
        # self["midi-transmitter-name"] = port_name
        # print("MIDI output port: '%s'" % port_name)
        if port_name:
            self["midi-transmitter-name"] = port_name
            # print("MIDI output port: '%s'" % port_name)
        else:
            self["midi-transmitter-name"] = None
                  
        
    def _select_gui(self, args):
        options = []
        for g in constants.GUI_OPTIONS:
            options.append(g[0].upper())
            
        try:
            env = os.environ["LLIA_GUI"]
        except KeyError:
            env = None
        sources = (args.gui, self._parser.get("GUI", "gui"), env, "tk")
        gui = None
        for s in sources:
            if s:
                gui = s.upper()
                break
        if gui in options:
            self["gui"] = s
            print("GUI: %s" % gui)
        else:
            print("\nWARNING:")
            print("Invalid gui '%s'" % gui)
            print("Valid options are:")
            for g in constants.GUI_OPTIONS:
                print("\t%-12s %s" % g)
            print("Not using GUI")
            self["gui"] = None

    def _select_default_host_and_client(self, args):
        host = None
        try:
            env = os.environ["LLIA_HOST"]
        except KeyError:
            env = None
        sources = (args.host,
                   self._parser.get("OSC", "host-address"),
                   env, "127.0.0.1")
        for s in sources:
            if s:
                host = s
                break
        port = None
        try:
            env = os.environ["LLIA_HOST_PORT"]
        except KeyError:
            env = None
        sources = (args.port,
                   self._parser.get("OSC", "host-port"),
                   env, 57120)
        for s in sources:
            if s:
                port = int(s)
                break
        client = None
        try:
            env = os.environ["LLIA_CLIENT"]
        except KeyError:
            env = None
        sources = (args.client,
                   self._parser.get("OSC", "client-address"),
                   env, "127.0.0.1")
        for s in sources:
            if s:
                client = s
                break
        client_port = None
        try:
            env = os.environ["LLIA_CLIENT_PORT"]
        except KeyError:
            env = None
        sources = (args.client_port,
                   self._parser.get("OSC", "client-port"),
                   env, 58000)
        for s in sources:
            if s:
                client_port = int(s)
                break
        self["host"] = host
        self["port"] = port
        self["client"] = client
        self["client_port"] = client_port
        print("OSC host '%s'  port %s" % (host, port))
        print("OSC client '%s'  port %s" % (client, client_port))

    def write_config_file(self, filename):
        with open(filename, 'w') as output:
            self._parser.write(output)
        self.filename = filename
    
    def sections(self):
        return self._parser.sections()

    def options(self, section):
        return self._parser.options(section)

    def get_option(self, section, option):
        return self._parser.get(section, option)

    def set_option(self, section, option, value):
        self._parser.set(section, option, value)
        
    def channel_name(self, channel, new_name=None):
        if new_name is not None:
            name = str(new_name)
            section = "MIDI-CHANNELS"
            key = "C%02d" % channel
            self.channel_assignments[channel] = name
        return self.channel_assignments[channel]

    def reset_channel_names(self):
        for c in range(1, 17):
            self.channel_name(c, "")

    def formatted_channel_names(self):
        return self.channel_assignments.formatted_list()
    
    def controller_name(self, ctrl, new_name=None):
        if new_name is not None:
            name = str(new_name)
            section = "MIDI-CONTROLLERS"
            key = "CTRL%03d" % ctrl
            self.controller_assignments[ctrl] = name
        return self.controller_assignments[ctrl]

    def reset_controller_names(self):
        for c in range(128):
            self.controller_name(c, "")

    def formatted_controller_names(self):
        return self.controller_assignments.formatted_list()
    

    def __get_value(self, section, key, default):
        try:
            return self._parser.get(section, key)
        except (NoOptionError, NoSectionError):
            return default

    def host_and_port(self):
        ip = self.__get_value("OSC","host-address","127.0.0.1")
        port = self.__get_value("OSC","host-port", 57120)
        return (ip, port)
        
    def global_osc_id(self):
        return self.__get_value("OSC", "global-id", "Llia")

    def osc_transmission_trace_enabled(self):
        flg = str(self.__get_value("OSC", "trace-osc-transmission", False)).upper()
        return flg == "TRUE"
    
    def gui(self):
        return self.__get_value("GUI", "gui", "NONE").upper()
    
    def enable_tooltips(self):
        flg = str(self.__get_value("GUI", "enable-tooltips", True)).upper()
        return flg != "FALSE"
    
    def warn_on_overwrite(self):
        flg = str(self.__get_value("GUI", "warn-on-overwrite", True)).upper()
        return flg != "FALSE"

    def warn_on_initialize(self):
        flg = str(self.__get_value("GUI", "warn-on-initialize", True)).upper()
        return flg != "FALSE"

    def warn_on_exit(self):
        flg = str(self.__get_value("GUI", "warn-on-exit", True)).upper()
        return flg != "FALSE"
    
    def active_updates_enabled(self):
        flg = str(self.__get_value("GUI", "enable-active-update", False)).upper()
        return flg == "TRUE"
        
    def enable_controller_edit(self):
        msg = "**DEPRECIATED** config.enable_controller_edit\n"
        msg += "  Use midi_edit_enabled instead."
        print(msg)
        flg = str(self.__get_value("GUI", "enable-controller-edit", False)).upper()
        return flg == "TRUE"

    def midi_edit_enabled(self):
        flg = str(self.__get_value("GUI", "enable-midi-edit", False)).upper()
        return flg == "TRUE"

    def trace_midi_reception_enabled(self):
        flg = str(self.__get_value("MIDI", "trace-midi-reception", False)).upper()
        return flg == "TRUE"
    
    def program_pp_enabled(self):
        flg = str(self.__get_value("MIDI", "enable-program-pp", True)).upper()
        return flg == "TRUE"
    
    def autogen_program_slot(self):
        msg = "**DEPRECIATED** config.autogen_program_slot"
        print(msg)
        try:
            rs = self._parser.get("MIDI", "autogen-program-slot")
            return int(rs)
        except (NoOptionError, NoSectionError, TypeError):
            return None

    def store_autogen_results(self):
        msg = "**DEPRECIATED** config.store_autogen_results"
        print(msg)
        try:
            rs = self._parser.get("MIDI", "autogen-store-slot")
            return int(rs)
        except (NoOptionError, NoSectionError, TypeError):
            return None

    def keyswitch_enabled(self):
        flg = str(self._parser.get("MIDI", "enable-keyswitch")).upper()
        return flg == "TRUE"

    def keyswitch_channel(self):
        mc = 10
        try:
            mc = int(self._parser.get("MIDI", "keyswitch-channel"))
            mc = min(16, max(mc, 1))
        except ValueError:
            pass
        return mc

    def keyswitch_transpose(self):
        x = 0
        try:
            x = int(self._parser.get("MIDI", "keyswitch-transpose"))
        except ValueError:
            pass
        return x
