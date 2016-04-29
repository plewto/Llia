# llia.toplevel
# 2016.04.23
#

from __future__ import (print_function)
import abc, sys, threading

from llia.proxy import LliaProxy
from llia.midi_receiver import get_midi_receiver
from llia.keytab.registry import KeyTableRegistry
from llia.gui.appwindow import DummyApplicationWindow
from llia.lsl.parser import LSLParser
import llia.constants as con


class LliaTopLevel(object):

    def __init__(self, config, skip_mainloop=False):
        super(LliaTopLevel, self).__init__()
        self.config = config
        self.proxy = LliaProxy(config, self)
        logfile_name = config.log_file()
        self.logfile = None
        if logfile_name:
            try:
                self.logfile = open(logfile_name, 'w')
                print("Llia logfile: '%s'" % logfile_name)
            except IOError:
                msg = "Can not open log file '%s'" % logfile_name
                self.warning(msg)
        if not self.logfile:
            print("No log file specified")
        print(logfile_name)
        self._main_window = DummyApplicationWindow(self, None)
        midi_in_trace = config.trace_midi_reception_enabled()
        midi_in_port = config["midi-receiver-name"]
        self.midi_receiver = get_midi_receiver(midi_in_port,midi_in_trace)
        self.keytables = KeyTableRegistry()
        self._repl_thread = None
        self.lsl_parser = LSLParser(self)
        if not skip_mainloop:
            self.start_main_loop()
        
    def global_osc_id(self):
        return self.config.global_osc_id()

    def log_event(self, msg):
        if self.logfile:
            self.logfile.write(msg+'\n')
    
    @abc.abstractmethod
    def exit(self, xcode=0):
        if xcode != 0:
            self.status("Llia exits with code %s" % xcode)
        else:
            self.status("Exit...")
        if self.logfile:
            self.logfile.close()
        self._main_window.exit_gui()
        sys.exit(xcode)

    def status(self, msg, timeout=-1):
        lgmsg = "Status oscID %s : %s" % (self.global_osc_id(), msg)
        self.log_event(lgmsg)
        self._main_window.status(msg, timeout)
    
    def warning(self, msg):
        lgmsg = "WARNING /Llia/%s : %s" % (self.global_osc_id(), msg)
        self.log_event(lgmsg)
        self._main_window.warning(msg)
    
    def error(self, errnum, msg, exception=None):
        acc = "ERROR: errnum = %s\n" % errnum
        acc += "ERROR: global OSC ID is '%s'\n" % self.global_osc_id()
        for line in msg.split("\n"):
            acc += "ERROR: %s\n" % line
        if exception:
            acc += "%s %s" % (type(exception), exception.message)
        self.log_event(acc)
        print(acc)
        self.exit(errnum)

    # def repl(self):
    #     print(con.BANNER)
    #     print(con.VERSION)
    #     print()
    #     pyver = sys.version_info[0]
    #     if pyver <= 2:
    #         infn = raw_input
    #     else:
    #         infn = input
    #     while True:
    #         usrin = infn("Llia> ")
    #         print(usrin)



        
    # def start_main_loop(self):
    #     # self._main_window.start_gui_loop()
    #     self.gui_thread = threading.Thread(target = self._main_window.start_gui_loop)
    #     self.gui_thread.setDaemon(True)
    #     self.gui_thread.start()
    #     self.repl()


    def start_main_loop(self):
        self._repl_thread = threading.Thread(target = self.lsl_parser.repl)
        self._repl_thread.start()
        self._main_window.start_gui_loop()
        
