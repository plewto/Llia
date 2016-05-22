# llia.gui.tk.tk_splash
# 2016.05.20

from __future__ import print_function
import mido
from Tkinter import Toplevel, Label, BOTH, Frame, StringVar
import ttk
from PIL import Image, ImageTk
from llia.gui.tk.tk_layout import VFrame
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.pallet as pallet

class TkSplashWindow(Toplevel):

    def __init__(self, root, app):
        Toplevel.__init__(self, root)
        self.title("Llia Setup")
        self.app = app
        self.config = app.config
        main = VFrame(self)
        main.pack(anchor="nw", expand=True, fill=BOTH)
        image = Image.open("resources/logos/llia_logo_medium.png")
        photo = ImageTk.PhotoImage(image)
        lab_logo = Label(main, image=photo)
        lab_logo.configure(background=factory.pallet["BG"])
        main.add(lab_logo)
        south = Frame(main, background=factory.pallet["BG"])
        main.add(south)
        self._build_south_panel(south)
        
        root.wait_window(self)

    def _build_south_panel(self, south):
        self._midi_input_ports = mido.get_input_names()
        self._midi_output_ports = mido.get_output_names()
        port_rows = max(len(self._midi_input_ports),
                        len(self._midi_output_ports))
        init_id = self.config.global_osc_id()
        init_host = self.config["host"]
        init_port = self.config["port"]
        init_client = self.config["client"]
        init_client_port = self.config["client_port"]
        init_input = self.config["midi-receiver-name"]
        init_output = self.config["midi-transmitter-name"]
        
        var_id = StringVar()
        var_host = StringVar()
        var_port = StringVar()
        var_client = StringVar()
        var_client_port = StringVar()
        var_input = StringVar()
        var_output = StringVar()

        def restore_defaults():
            var_id.set(init_id)
            var_host.set(init_host)
            var_port.set(init_port)
            var_client.set(init_client)
            var_client_port.set(init_client_port)
            var_input.set(init_input)
            var_output.set(init_output)
        restore_defaults()
        e_id = factory.entry(south, var_id)
        e_host = factory.entry(south, var_host)
        e_port = factory.entry(south, var_port)
        e_client = factory.entry(south, var_client)
        e_client_port = factory.entry(south, var_client_port)
        padding = Frame(south)
        padding.grid(row=0, column=0, ipadx=8, ipady=8)
        padding.configure(background=factory.pallet["BG"])
        e_id.grid(row=1, column=1, columnspan=2)
        e_host.grid(row=2, column=1, columnspan=2)
        e_port.grid(row=2, column=5, columnspan=2)
        e_client.grid(row=3, column=1, columnspan=2)
        e_client_port.grid(row=3, column=5, columnspan=2)
        port_count = max(len(self._midi_input_ports),
                         len(self._midi_output_ports))
        lab_id = factory.label(south, "OSC ID")
        lab_host = factory.label(south, "Host")
        lab_host_port = factory.label(south, "Port")
        lab_client = factory.label(south, "Client")
        lab_client_port = factory.label(south, "Port")
        lab_midi_input = factory.label(south, "MIDI Input")
        lab_midi_output = factory.label(south, "MIDI Output")
        padding = Frame(south)
        padding.grid(row=4, column=3, ipadx=8, ipady=8)
        padding.configure(background=factory.pallet["BG"])
        lab_id.grid(row=1, column=0, columnspan=1, ipadx=8, ipady=8)
        lab_host.grid(row=2, column=0, columnspan=1)
        lab_host_port.grid(row=3, column=4, columnspan=1, ipadx=4)
        lab_client.grid(row=3, column=0, columnspan=1)
        lab_client_port.grid(row=3, column=4, columnspan=1)
        lab_midi_input.grid(row=5, column=1, columnspan=2, ipady=8)
        lab_midi_output.grid(row=5, column=5, columnspan=2, ipady=8)
        for n,p in enumerate(self._midi_input_ports):
            rb = factory.radio(south, str(p), var_input, str(p))
            rb.grid(row=n+6, column=1, sticky="W")
        for n,p in enumerate(self._midi_output_ports):
            rb = factory.radio(south, str(p), var_output, str(p))
            rb.grid(row=n+6, column=5, sticky="W")
        padding = Frame(south)
        padding.grid(row=0, column=7, ipadx=36)
        padding.configure(background=factory.pallet["BG"])
        b_help = factory.help_button(south)
        b_about = factory.button(south, "About")
        b_restore = factory.button(south, "Restore")
        b_continue = factory.button(south, "Continue")
        b_help.grid(row=1, column=8, sticky="EW", pady=2)
        b_restore.grid(row=2, column=8, sticky="EW", pady=2)
        b_continue.grid(row=3, column=8, sticky="EW", pady=2)
        b_about.grid(row=4, column=8, sticky="EW", pady=2)

        

    def done(self):
        self.destroy()
        
