# llia.gui.tk.tk_synthwindow
# 2016.06.11


from __future__ import print_function
from Tk import Toplevel, BOTH, Frame, Label
import tkk


from llia.gui.appwindow import AbstractApplicationWindow




class TkSynthWindow(AbstractApplicationWindow):

    def __init__(self, sproxy):
        app = sproxy.app
        super(TkSynthWindow, self).__init__(app, app.main_window().root)
        self.synth = sproxy
        self.sid = sproxy.sid
        self.toplevel = self.app.main_window().as_widget()

        main = Frame(self.toplevel)
        main.pack(expand=True, fill=BOTH)

        # DEBUG FPO
        wfpo = Label(main, text= "FPO sid = %s" % self.sid)
        wfpo.pack()
        # END FPO DEBUG
        
    def as_widget():
        return self.toplevel

    
        
