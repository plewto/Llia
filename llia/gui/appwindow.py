# llia.gui.appwindow
# 2016.04.23
#

from __future__ import print_function
import abc, sys

from llia.gui.splash import TextSplashScreen

class AbstractGroupWindow(object):

    """
    Defines group window interface.
    A group window contains a tabbed pane (Notebook in Tk) for each active 
    synth in the group.
    """

    def __init__(self, app, root=None, name=""):
        """
        Construct new AbstractGroupWindow

        app - The application, an instance if lliaApp
        root - optional, the GUI root object.
        name - optional
        """
        self.app = app
        self.root=root
        self.name = str(name)
        
    @abc.abstractmethod
    def on_closing(self, *args):
        """
        Function called in response to user clicking the close button.
        """
        pass

    @abc.abstractmethod
    def show_synth_editor(self, sid):
        """
        Make indicated synth editor visible.
        ISSUE: What happens if self does not contain indicated synth?
        """
        pass

    @abc.abstractmethod
    def lift(self):
        """
        Iconify this window
        """
        pass

    @abc.abstractmethod
    def deiconify(self):
        pass
    
    @abc.abstractmethod
    def lower(self):
        pass

    @abc.abstractmethod
    def tabula_rasa(self):
        pass

    @abc.abstractmethod
    def sync(self):
        pass
    

    

class AbstractApplicationWindow(object):


    """
    AbstractApplicationWindow defines the GUI interface for the primary application window.
    """
    
    def __init__(self, app, root):
        """
        Constructs application window.
        app - an instance of LliaApp
        root - The GUI systems root object


        This constructor should not be called directly
        """
        self.app = app
        self.root = root
        self.config = app.config()
        self._synth_editors = {}  # Active synth editors. synth SID used as key
        
    def __setitem__(self, sid, sed):
        self._synth_editors[sid] = sed

    def __getitem__(self, sid):
        return self._synth_editors[sid]

    def keys(self):
        """
        Returns list of active synth editor keys.
        """
        return self._synth_editors.keys()

    @abc.abstractmethod
    def status(self, msg):
        """
        Displays message on status line.
        """
        oscid = self.app.global_osc_id()
        print("STATUS  : /Llia/%s : %s" % (oscid, msg))

    @abc.abstractmethod
    def warning(self, msg):
        """
        Displays warning on status line.
        """
        oscid = self.app.global_osc_id()
        print("WARNING : /Llia/%s : %s" % (oscid, msg))

    @abc.abstractmethod
    def start_gui_loop(self):
        return None
    
    @abc.abstractmethod
    def exit_gui(self):
        return None

    @abc.abstractmethod
    def update_progressbar(self, count, value):
        """
        Update progress bar.
        count - int, expected number of steps
        value - int, current value. 0 <= value <= count
        """
        self.status("Progress %s/%s" % (value, count))
    
    @abc.abstractmethod
    def busy(self, flag, message=""):
        """
        If flag indicate application is busy.
        otherwise turn busy aspect off.
        """ 
        return None

    @abc.abstractmethod
    def tabula_rasa(self):
        pass

    @abc.abstractmethod
    def add_synth_group(self, name=""):
        """
        Adds a new SynthGroup window named name.
        """
        return None

    @abc.abstractmethod
    def display_synth_editor(self, sid):
        """
        Display editor for indicated synth.
        """
        pass

    @abc.abstractmethod
    def confirm_exit(self):
        """
        Ask users permission prior to exiting application.
        Exit confirmation may be turned off as a configuration option.
        The default behavior is to not ask for confirmation.
        """
        return True
    
class DummyApplicationWindow(AbstractApplicationWindow):

    """
    DummyApplicationWindow is a concrete implementation of AbstractApplicationWindow.
    A dummy window is used when running Llia without a GUI.
    """
    
    def __init__(self, app, *_):
        """
        Constructs a Dummy application window.
        Do not call directly, use create_application_window.
        """
        super(DummyApplicationWindow, self).__init__(app, None)
        self.group_windows=[AbstractGroupWindow(app)]

    def busy(self, flag, message=""):
        if flag:
            self.status("BUSY %s ..." % message)
        else:
            self.status("NOT BUSY")

    def add_synth_group(self, name=""):
        """
        Adding GroupWindow is ignored by DummyApplicationWindow.
        """
        pass
        
        
def create_application_window(app):
    """
    Creates the main application window.
    The exact type is depended on the GUI systems selected in the configuration file.
    Currently (2017.12.13) there are two case-insensitive options:
         NONE - Creates a DummyApplicationWindow
         TK   - Creates Tk TopLevelWindow

    app - An instance of LLiaApp
    """
    config = app.config()
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
    
    
