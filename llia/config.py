# llia.config
# 2016.03.20
#

from __future__ import print_function
import sys, os, os.path
from ConfigParser import RawConfigParser,NoOptionError,NoSectionError

import llia.constants as constants
from llia.alias import CCAssignments, ChannelAssignments

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
        '''
        Creates LliaConfig object.  create_instance should be used instead 
        of directly creating LliaConfig by it's constructor. 
        create_instance attempts to read a platform dependent configuration
        file.
        
           Linux    ~/.config/Llia/config
           OSX      ~/.config/Llia/config (Tentitive)
           Windows  ? not yet determined
        
        ARGS:
          args - Namespace, passed from command line arguments.

        RETURNS: LliaConfig
        '''
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
                    filename = "~/.config/Llia/config"
                elif platform.startswith("win32"): # ISSUE: Windows Portability
                    _non_support_message("Windows")
                else:
                    _non_support_message(sys.platform)
        filename = os.path.expanduser(filename)
        if not os.path.exists(filename):
            msg = MSG_NO_CONFIG_FILE % filename
            print("%s\n" % msg)
            sys.exit(0)
        return LliaConfig(filename, args)
    
    def __init__(self, filename, args):
        '''
        Construct new LliaConfig object.
        Do not call directly, use LliaConfig.create_instance instead.
        ARGS:
           filename - String, config file filename
           args     - Namespace, command line arguments.
        '''
        dict.__init__(self)
        self.filename = filename
        self._parser = RawConfigParser()
        self._parser.read(filename)
        self._select_backend(args)
        self._select_midi_input_port(args)
        self._select_midi_output_port(args)
        self._select_default_host_and_client(args)
        self._select_gui(args)
        self._select_startup_options(args)
        self.controller_assignments = CCAssignments(self._parser)
        self.channel_assignments = ChannelAssignments(self._parser)
        
    def _select_backend(self, args):
        '''
        Internal method selects mido MIDI backend.
        args - Namespace
        RETURNS: String, either 'mido.backends.rtmidi' or 
                'midi.backends.portmidi'
        '''
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
        if port_name:
            self["midi-receiver-name"] = port_name
        else:
            self["midi-receiver-name"] = None
                
    def _select_midi_output_port(self, args):
        try:
            env = os.environ["LLIA_MIDI_OUT"]
        except KeyError:
            env = None
        sources = (args.midiout, self._parser.get("MIDI","output-port"),env)
        port_name = None
        for s in sources:
            if s:
                port_name = s
                break
        if port_name:
            self["midi-transmitter-name"] = port_name
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
        global_id = self.__get_value("OSC", "global-id", "Llia")
        for s in sources:
            if s:
                client_port = int(s)
                break
        self["host"] = host
        self["port"] = port
        self["client"] = client
        self["client_port"] = client_port
        self["global-osc-id"] = global_id
        print("OSC host '%s'  port %s" % (host, port))
        print("OSC client '%s'  port %s" % (client, client_port))

    def _select_startup_options(self, args):
        # Splash screen enable
        flag1 = str(self._parser.get("GUI","no-splash")).upper()
        flag1 = flag1 != "TRUE" # true on disable
        flag2 = self["midi-receiver-name"] # false -> enable
        enable = flag1 or not flag2
        self["enable-splash"] = enable
        # Skip REPL
        flag1 = str(self._parser.get("GENERAL", "no-repl")).upper()
        self["enable-repl"] = flag1 != "TRUE"

    def write_config_file(self, filename):
        '''
        Write self to a configuration file.

        ARGS:
          filename
        '''
        with open(filename, 'w') as output:
            self._parser.write(output)
        self.filename = filename
    
    def sections(self):
        '''
        Returns list of top level configuration sections.
        '''
        return self._parser.sections()

    def options(self, section):
        '''
        Returns list of options under top level section.

        ARGS:
          section - string
        '''
        return self._parser.options(section)

    def get_option(self, section, option):
        '''
        Returns current config value.
        
        ARGS:
           section - String 
           option  - String
        
        RETURNS: String

        ISSUE: What error is raised if option/section is not defined?
        '''
        return self._parser.get(section, option)

    def set_option(self, section, option, value):
        '''
        Set configuration value
        
        ARGS:
          section - String
          option  - String
          value   - String

        ISSUE: What error is raised if option/section dis not defined?
        '''
        self._parser.set(section, option, value)
        
    def channel_name(self, channel, new_name=None):
        '''
        Return/change MIDI channel name.

        ARGS:
          channel  - int, MIDI channel, [1,2,3,...,16]
          new_name - optional String, if specified change channel's name

        RETURNS: String

        Raises IndexError on invalid channel number.
        '''
        if new_name is not None:
            name = str(new_name)
            section = "MIDI-CHANNELS"
            key = "C%02d" % channel
            self.channel_assignments[channel] = name
        return self.channel_assignments[channel]

    def channel_number(self, name):
        '''
        Get channel number for named MIDI channel

        ARGS:
          name - Sting

        RETURNS: int, MIDI channel [1,2,3,...,16]
                 If name is not a defined channel return 1.
        '''
        return self.channel_assignments.get_channel(name)
    
    def reset_channel_names(self):
        '''
        Remove all MIDI channel name assignments.
        '''
        for c in range(1, 17):
            self.channel_name(c, "")

    def formatted_channel_names(self):
        '''
        Returns a list of formatted MIDI channel names.
        '''
        return self.channel_assignments.formatted_list()
    
    def controller_name(self, ctrl, new_name=None):
        '''
        Get/change MIDI controller name.

        ARGS:
          ctrl     - int MIDI controller number, [0,1,2,...127]
          new_name - optional String, if specified change controller name.

        RETURNS: String

        Raises: IndexError 
        '''
        if new_name is not None:
            name = str(new_name)
            section = "MIDI-CONTROLLERS"
            key = "CTRL%03d" % ctrl
            self.controller_assignments[ctrl] = name
        return self.controller_assignments[ctrl]

    def reset_controller_names(self):
        '''
        Clear all MIDI controller names.
        '''
        for c in range(128):
            self.controller_name(c, "")

    def formatted_controller_names(self):
        '''
        Returns list of formatted controller names.
        '''
        return self.controller_assignments.formatted_list()

    def __get_value(self, section, key, default):
        try:
            return self._parser.get(section, key)
        except (NoOptionError, NoSectionError):
            return default

    def host_and_port(self):
        '''
        Returns tuple (host,port) the ip address and port number
        for SuperCollider server.
        '''
        ip = self.__get_value("OSC","host-address","127.0.0.1")
        port = self.__get_value("OSC","host-port", 57120)
        return (ip, port)
        
    def global_osc_id(self, new_id=None):
        '''
        Get/change global OSC id.
        The OSC id -MUST- be the same for both the client and server apps.
        For most situations the default value 'Llia' may be used.
        If more then one instance of Llia is running then each client/server
        pair must have their own unique OSC id.

        ARGS:
          new_id - optional String.

        RETURNS: String.
        '''
        if new_id:
            self["global-osc-id"] = str(new_id)
        return self["global-osc-id"]

    def osc_transmission_trace_enabled(self):
        '''
        Returns True if OSC transmission trace is enabled.
        '''
        flg = str(self.__get_value("OSC", "trace-osc-transmission", False)).upper()
        return flg == "TRUE"
    
    def gui(self):
        '''
        Returns name of GUI system.
        Currently two systems are supported:
           'NONE' - run 'headless' without GUI support
           'TK'   - use Tk 
        '''
        return self.__get_value("GUI", "gui", "NONE").upper()
    
    # def enable_tooltips(self):
    #     flg = str(self.__get_value("GUI", "enable-tooltips", True)).upper()
    #     return flg != "FALSE"
    
    def warn_on_overwrite(self):
        '''
        Returns flag indicating if a warning dialog should appear if a file 
        is about to be overwritten.  

        Tk automatically produces such a dialog and will ignore this value.
        '''
        flg = str(self.__get_value("GUI", "warn-on-overwrite", True)).upper()
        return flg != "FALSE"

    def warn_on_initialize(self):
        '''
        Returns flag indicating if a warning dialog should appear prior to 
        initializing some big data structure, such as a bank.
        '''
        flg = str(self.__get_value("GUI", "warn-on-initialize", True)).upper()
        return flg != "FALSE"

    def warn_on_exit(self):
        '''
        Returns flag indication if a warning dialog should appear prior to 
        exiting the application.
        '''
        flg = str(self.__get_value("GUI", "warn-on-exit", True)).upper()
        return flg != "FALSE"
    
    def active_updates_enabled(self):
        '''
        Returns flag indicating if active updates are enabled.
        Active updates allow GUI controls to change appearance in response to 
        to specific MIDI events. 
        '''
        flg = str(self.__get_value("GUI", "enable-active-update", False)).upper()
        rs = flg == "TRUE"
        return rs
        
    def enable_controller_edit(self):
        '''
        DO NOT USE: this method is depreciated, use midi_edit_enabled instead.
        '''
        msg = "**DEPRECIATED** config.enable_controller_edit\n"
        msg += "  Use midi_edit_enabled instead."
        print(msg)
        flg = str(self.__get_value("GUI", "enable-controller-edit", False)).upper()
        return flg == "TRUE"

    def midi_edit_enabled(self):
        '''
        Returns flag indicating if mapped MIDI events should alter current 
        program values.  If enabled changes incoming MIDI events which are 
        mapped to some parameter will both update active synths and make 
        matching modifications to the current program.  If the program is
        subsequently saved to the ProgramBank these changes will be preserved.


        This is a double edged sword.  Modifying the program via MIDI 
        controller events makes some sense, doing so by velocity is
        dubious. 
        '''
        flg = str(self.__get_value("GUI", "enable-midi-edit", False)).upper()
        return flg == "TRUE"

    def trace_midi_reception_enabled(self):
        '''
        Returns flag indicating if incoming MIDI events should display
        diagnostic data.
        '''
        flg = str(self.__get_value("MIDI", "trace-midi-reception", False)).upper()
        return flg == "TRUE"
    
    def program_pp_enabled(self):
        '''
        Returns flag indicating if 'pretty printing' should be enabled.
        Pretty printing produces output in response to MIDI program changes.
        The result should be valid Python code which could be used to 
        recreate the current program. 
        '''
        flg = str(self.__get_value("MIDI", "enable-program-pp", True)).upper()
        return flg == "TRUE"
    
    def autogen_program_slot(self):
        '''
        DEPRECIATED, DO NOT USE.
        '''
        msg = "**DEPRECIATED** config.autogen_program_slot"
        print(msg)
        try:
            rs = self._parser.get("MIDI", "autogen-program-slot")
            return int(rs)
        except (NoOptionError, NoSectionError, TypeError):
            return None

    def store_autogen_results(self):
        '''
        DEPRECIATED, DO NOT USE.
        '''
        msg = "**DEPRECIATED** config.store_autogen_results"
        print(msg)
        try:
            rs = self._parser.get("MIDI", "autogen-store-slot")
            return int(rs)
        except (NoOptionError, NoSectionError, TypeError):
            return None

    # def keyswitch_enabled(self):
    #     '''
    #     Returns flag indicating if MIDI 'keyswitch' mode is enabled.
    #     Keyswitching allows MIDI key events to be interpreted as program 
    #     changes.  

    #     ISSUE: The current keyswitch implementation is rudimentary.
    #     '''
    #     flg = str(self._parser.get("MIDI", "enable-keyswitch")).upper()
    #     return flg == "TRUE"

    # def keyswitch_channel(self):
    #     '''
    #     Returns MIDI channel used for key switching. [1,2,3,...16]
        
    #     '''
    #     mc = 10
    #     try:
    #         mc = int(self._parser.get("MIDI", "keyswitch-channel"))
    #         mc = min(16, max(mc, 1))
    #     except ValueError:
    #         pass
    #     return mc

    # def keyswitch_transpose(self):
    #     '''
    #     Returns a transposition amount added to incoming key switch events
    #     to produce to the resulting program number.

    #     ISSUE: The keyswitch implementation is rudimentary and this 
    #            method should be viewed with suspicion for the future.
    #     '''
    #     x = 0
    #     try:
    #         x = int(self._parser.get("MIDI", "keyswitch-transpose"))
    #     except ValueError:
    #         pass
    #     return x
  
    def startup_script(self):
        '''
        Returns filename of python script to executed on startup.
        '''
        ss = self.get_option("GENERAL", "startup-script")
        return ss

    def startup_scene(self):
        '''
        Returns filename for scene object to load on startup."
        '''
        ss = self.get_option("GENERAL", "startup-scene")
        return ss
