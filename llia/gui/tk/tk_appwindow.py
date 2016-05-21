# llia.gui.tk.tk_appwindow
# 2016.05.20

from __future__ import print_function
import Tkinter as tk
import ttk

from llia.gui.appwindow import AbstractApplicationWindow


class TkApplicationWindow(AbstractApplicationWindow):

    def __init__(self, root, app):
        self.root = root
        super(TkApplicationWindow, self).__init__(app, root)
        w = tk.Label(self.root, text = "Hello World")
        w.pack()

    def start_gui_loop(self):
        self.root.mainloop()
    
    def exit_gui(self):
        self.root.quit()
