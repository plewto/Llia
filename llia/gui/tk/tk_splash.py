# llia.gui.tk.tk_splash
# 2016.05.20

from __future__ import print_function
from Tkinter import Toplevel, Label
import ttk


class TkSplashWindow(object):

    def __init__(self, app):
        self.app = app
        self.config = app.config
        self.top = Toplevel()
        self.top.title("Llia Setup")

        w = Label(self.top, text="Wht Up Dog?")
        w.pack()
        self.top.mainloop()


