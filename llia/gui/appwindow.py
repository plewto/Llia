# llia.gui.appwindow
# 2016.04.23
#

from __future__ import print_function
import abc

from llia.gui.widget import DUMMY_WIDGET

class AbstractApplicationWindow(object):

    def __init__(self, app, root):
        self.app = app
        self.root = root

    @abc.abstractmethod
    def status(self, msg, timeout=-1):
        oscid = self.app.global_osc_id()
        print("Status oscID %s : %s" % (oscid, msg))

    @abc.abstractmethod
    def warning(self, msg):
        oscid = self.app.global_osc_id()
        print("WARNING oscID %s : %s" % (oscid, msg))

    @abc.abstractmethod
    def as_widget(self):
        return None

    @abc.abstractmethod
    def start_main_loop(self):
        return None
        
class DummyApplicationWindow(AbstractApplicationWindow):

    def __init__(self, app, *_):
        super(DummyApplicationWindow, self).__init__(app, None)

    def as_widget(self):
        return DUMMY_WIDGET

    def start_main_loop(self):
        self.app.status("Satring main loop")
        while True:
            pass
        
        
        
