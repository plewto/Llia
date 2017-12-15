# llia.llia_app
# Top level Llia Client application
#

from __future__ import (print_function)
import abc, sys, threading

from llia.proxy import LliaProxy
from llia.midi_receiver import get_midi_receiver
from llia.keytab.registry import KeyTableRegistry
from llia.gui.appwindow import create_application_window
from llia.lliascript.lliascript import lliascript_parser
# from llia.synth_group import SynthGroup
import llia.constants as con

class LliaApp(object):

    def __init__(self, config, scene_file=None, skip_mainloop=False):
        '''
        Constructs top-level client application.
        
        ARGS:
          config - an instance of LliaConfig
          skip_mainloop - flag, if True do not enter main application loop.
                          intended for testing.
        '''
        super(LliaApp, self).__init__()
        self._config = config
        self.pp_enabled = config.program_pp_enabled()
        self.proxy = LliaProxy(config, self)
        self._main_window = create_application_window(self)
        self.midi_in_trace = config.trace_midi_reception_enabled()
        midi_in_port = config["midi-receiver-name"]
        try:
            self.midi_receiver = get_midi_receiver(midi_in_port,
                                                   self.midi_in_trace)
        except IOError:
            msg = "Unknown MIDI port: '%s'\n" % midi_in_port
            msg += "Use -p command line option to see list of available ports\n"
            msg += "and then change input-port value in configuration file\n"
            msg += "accordingly.\n\n"

            msg += "Alternately set no-splash to False in configuration file to\n"
            msg += "select MIDI port on startup.\n\n"
            msg += "If on Linux, MIDI port names change with every reboot."
            print("*"*60)
            for line in msg.split('\n'):
                print("** %s" % line)
            print("*"*60)
            sys.exit(-1)
        self.keytables = KeyTableRegistry()
        self._repl_thread = None
        self.ls_parser = lliascript_parser(self)
        ss = config.startup_script()
        if ss:
            print("Loading startup script '%s'" % ss)
            self.ls_parser.load_python(ss)
        ss = scene_file or config.startup_scene()
        if ss:
            print("Loading startup scene '%s'" % ss)
            self.ls_parser.load_scene(ss)
        if not skip_mainloop:
            self.start_main_loop()

    # def current_synth_group(self, index=-1):
    #     return self._groups[index]

    # def add_synth_group(self, name=""):
    #     self._groups.append(SynthGroup(name))
    #     return self.current_synth_group()
            
    def config(self):
        return self._config
            
    def global_osc_id(self):
        '''
        Returns String, the global OSC id.   
        The OSC id MUST match between the client and server applications.
        '''
        return self._config.global_osc_id()
    
    def exit_(self, xcode=0):
        '''
        Exit client application.

        ARGS:
          xcode - int exit code, non-zero indicates an error.
        '''
        if self._config.warn_on_exit():
            flag = self._main_window.confirm_exit()
        else:
            flag = True
        if flag:
            print("Llia exit code: %s" % xcode)
            self.proxy.restart()
            self._main_window.exit_gui()
            self.ls_parser.exit_repl = True
            sys.exit(xcode)
        else:
            print("Exit aborted.")
            
    def main_window(self):
        '''
        Returns the application's main window. 
        The exact object type is dependent on the GUI system in use.
        In the case where no GUI has been enabled, the return object is 
        a dummy 'window' 
        '''
        return self._main_window
        
    def status(self, msg):
        '''
        Displays message to application status line.
        '''
        self._main_window.status(msg)
            
    def warning(self, msg):
        '''
        Displays warning to application status line.
        '''
        self._main_window.warning(msg)
    
    def error(self, errnum, msg, exception=None):
        '''
        Print error message and terminate application.
        '''
        acc = "ERROR: errnum = %s\n" % errnum
        acc += "ERROR: global OSC ID is '%s'\n" % self.global_osc_id()
        for line in msg.split("\n"):
            acc += "ERROR: %s\n" % line
        if exception:
            acc += "%s %s" % (type(exception), exception.message)
        print(acc)
        self.exit(errnum)

    def start_main_loop(self):
        if self._config["enable-repl"]:
            self._repl_thread = threading.Thread(target = self.ls_parser.repl)
            self._repl_thread.start()
        else:
            print("REPL disabled")
        self._main_window.start_gui_loop()

    # # ISSUE: FIX ME  update all GUI windows.
    # def sync_all(self):
    #     self.proxy.sync_to_host()
    #     # print("LliaApp.sync_all is not completely implemented")

    def tabula_rasa(self):
        "clean up - reinitialize all data."
        self.proxy.tabula_rasa()
        self._main_window.tabula_rasa()
