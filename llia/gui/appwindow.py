# llia.gui.appwindow
# 2016.04.23
#

from __future__ import print_function
import abc, sys

from llia.gui.widget import DUMMY_WIDGET
from llia.gui.splash import TextSplashScreen

class AbstractApplicationWindow(object):

    def __init__(self, app, root):
        self.app = app
        self.root = root
        self.config = app.config

    @abc.abstractmethod
    def status(self, msg):
        oscid = self.app.global_osc_id()
        print("STATUS  : /Llia/%s : %s" % (oscid, msg))

    @abc.abstractmethod
    def warning(self, msg):
        oscid = self.app.global_osc_id()
        print("WARNING : /Llia/%s : %s" % (oscid, msg))

    @abc.abstractmethod
    def as_widget(self):
        return None

    @abc.abstractmethod
    def start_gui_loop(self):
        return None
    
    @abc.abstractmethod
    def exit_gui(self):
        return None
        
    
class DummyApplicationWindow(AbstractApplicationWindow):

    def __init__(self, app, *_):
        super(DummyApplicationWindow, self).__init__(app, None)

    def as_widget(self):
        return DUMMY_WIDGET

def create_application_window(app):
    config = app.config
    gui = str(config.gui())
    if gui.upper() == "NONE":
        if str(config["enable-splash"]).upper() != "FALSE":
            TextSplashScreen(app)
        return DummyApplicationWindow(app)
    elif gui.upper() == "TK":
        import llia.gui.tk.tk_appwindow as tkaw
        # import Tkinter as tk
        # import ttk
        # root = tk.Tk()
        appwin = tkaw.TkApplicationWindow(app)
        return appwin
    else:
        msg = "ERROR: Invalid gui: '%s'" % gui
        print(msg)
        sys.exit(1)
    
    
