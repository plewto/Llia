# llia.gui.tk.tk_about_diakog
# 2016.05.24

from __future__ import print_function
from Tkinter import Toplevel, Label, BOTH, Frame
import ttk
from PIL import Image, ImageTk


from llia.constants import *
from llia.gui.tk.tk_layout import VFrame
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.pallet as pallet

class TkAboutDialog(Toplevel):

    def __init__(self, root, app):
        Toplevel.__init__(self, root)
        self.app = app
        main = VFrame(self)
        main.pack(anchor="nw", expand=True, fill=BOTH)
        image = Image.open("resources/logos/llia_logo_medium.png")
        photo = ImageTk.PhotoImage(image)
        lab_logo = Label(main, image=photo)
        lab_logo.configure(background=factory.pallet["BG"])
        main.add(lab_logo)
        south = Frame(main, background=factory.pallet["BG"])
        main.add(south)
        lab_version = factory.label(south, "LLia Version %s" % (VERSION,))
        lab_copyright = factory.label(south, "(c) 2016 Steven Jones")
        lab_version.pack()
        lab_copyright.pack()
        self.grab_set()
        self.mainloop()
        #root.wait_window(self)
