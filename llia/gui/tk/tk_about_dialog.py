# llia.gui.tk.tk_about_diakog
# 2016.05.24

from __future__ import print_function
from Tkinter import Toplevel, Label, BOTH, Frame
import ttk
from PIL import Image, ImageTk


from llia.constants import *
from llia.gui.tk.tk_layout import VFrame
import llia.gui.tk.tk_factory as factory
#import llia.gui.tk.pallet as pallet

class TkAboutDialog(Toplevel):

    def __init__(self, master, app):
        Toplevel.__init__(self, master)
        self.config(background=factory.bg)
        config = app.config
        id_ = config["global-osc-id"]
        host, port = config['host'], config['port']
        client, cport = config['client'], config['client_port']
        midi_receiver = app.midi_receiver.port_name()
        midi_transmitter = "n/a" # FIX ME
        
        main = VFrame(self)
        main.pack(anchor="nw", expand=True, fill=BOTH)
        image = Image.open("resources/logos/llia_logo_medium.png")
        photo = ImageTk.PhotoImage(image)
        lab_logo = Label(main, image=photo)
        #lab_logo.configure(background=factory.pallet["BG"])
        main.add(lab_logo)
        #south = Frame(main, background=factory.pallet["BG"])
        south = factory.frame(main)
        main.add(south)
        acc = "Llia Version %s.%s.%s \n" % VERSION[0:3]
        acc += "(c) 2016 Steven Jones\n\n"
        acc += "OSC ID      : %s\n" % id_
        acc += "OSC Host    : %-12s port : %s\n" % (host, port)
        acc += "OSC client  : %-12s port  : %s\n\n" % (client, cport)
        acc += "MIDI Receiver    : %s\n" % midi_receiver
        acc += "MIDI Transmitter : %s\n" % midi_transmitter
        tx = factory.read_only_text(south, acc)
        tx.pack(pady=32)
        self.grab_set()
        self.mainloop()
        #root.wait_window(self)
        
