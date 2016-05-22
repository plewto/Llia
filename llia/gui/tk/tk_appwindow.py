# llia.gui.tk.tk_appwindow
# 2016.05.20

from __future__ import print_function
from Tkinter import (Frame, Label, Menu, Tk, BOTH)
import ttk

from llia.gui.appwindow import AbstractApplicationWindow
from llia.gui.tk.tk_splash import TkSplashWindow
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.tk_layout as layout



class TkApplicationWindow(AbstractApplicationWindow):

    def __init__(self, app):
        self.root = Tk()
        self.root.title("Llia")
        self.root.configure(background=factory.pallet["BG"])
        super(TkApplicationWindow, self).__init__(app, self.root)
        self.root.withdraw()
        splash = TkSplashWindow(self.root, app)
        self.root.deiconify()
        
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)
        self._main = layout.BorderFrame(self.root)
        self._main.pack(anchor="nw", expand=True, fill=BOTH)
        self._init_status_panel()
        self._init_menu()
        self.status("Why ask?")

       
    def _init_status_panel(self):
        south = self._main.south
        south.configure(padx=4, pady=4)
        self._lab_status = factory.label(south, "")
        b_panic = factory.button(south, "PANIC")
        ttip = "Clear status line"
        b_clear_status = factory.clear_button(south,self.clear_status,ttip)
        b_panic.grid(row=0, column=0, sticky="w")
        b_clear_status.grid(row=0, column=1, sticky="w")
        self._lab_status.grid(row=0,column=2, sticky="w", ipadx=8) 
        
    def _init_menu(self):
        menu = Menu(self.root)
        menu.configure(background=factory.pallet["BG"])
        menu.configure(foreground=factory.pallet["FG"])
        self.root.config(menu=menu)
        file_menu = Menu(menu)
        io_menu = Menu(menu)
        bus_menu = Menu(menu)
        buffer_menu = Menu(menu)
        synth_menu = Menu(menu)
        tune_menu = Menu(menu)
        midimap_menu = Menu(menu)
        help_menu = Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)
        menu.add_cascade(label="IO", menu=io_menu)
        menu.add_cascade(label="Bus", menu=bus_menu)
        menu.add_cascade(label="Buffer", menu=buffer_menu)
        menu.add_cascade(label="Synth", menu=synth_menu)
        menu.add_cascade(label="Tune", menu=tune_menu)
        menu.add_cascade(label="Map", menu=midimap_menu)
        menu.add_cascade(label="Help", menu=help_menu)

    def exit_gui(self):
        try:
            self.root.destroy()
        except:
            pass

    def exit_app(self):
        # ISSUE: Check config and ask user confirmation before existing
        self.app.exit_()

    def as_widget(self):
        return self.root
        
    def status(self, msg):
        self._lab_status.config(text=str(msg))

    def warning(self, msg):
        msg = "WARNING: %s" % msg
        self._lab_status.config(text=msg)
        
    def clear_status(self):
        self.status("")
                                              
    def start_gui_loop(self):
        self.root.mainloop()
