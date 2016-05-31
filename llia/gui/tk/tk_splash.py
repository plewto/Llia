# llia.gui.tk.tk_splash
# 2016.05.20

from __future__ import print_function
import mido
from Tkinter import Toplevel, Label, BOTH, Frame, StringVar
import ttk
from PIL import Image, ImageTk
from llia.gui.tk.tk_layout import VFrame
import llia.gui.tk.tk_factory as factory
#import llia.gui.tk.pallet as pallet

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
        #lab_logo.configure(background=factory.pallet["BG"])
        main.add(lab_logo)
        #south = Frame(main, background=factory.pallet["BG"])
        south = Frame(main)
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
        
        self.var_id = StringVar()
        self.var_host = StringVar()
        self.var_port = StringVar()
        self.var_client = StringVar()
        self.var_client_port = StringVar()
        self.var_input = StringVar()
        self.var_output = StringVar()

        def restore_defaults():
            self.var_id.set(init_id)
            self.var_host.set(init_host)
            self.var_port.set(init_port)
            self.var_client.set(init_client)
            self.var_client_port.set(init_client_port)
            self.var_input.set(init_input)
            self.var_output.set(init_output)
        restore_defaults()
        e_id = factory.entry(south, self.var_id)
        e_host = factory.entry(south, self.var_host)
        e_port = factory.entry(south, self.var_port)
        e_client = factory.entry(south, self.var_client)
        e_client_port = factory.entry(south, self.var_client_port)
        padding = Frame(south)
        padding.grid(row=0, column=0, ipadx=8, ipady=8)
        #padding.configure(background=factory.pallet["BG"])
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
        #padding.configure(background=factory.pallet["BG"])
        lab_id.grid(row=1, column=0, columnspan=1, ipadx=8, ipady=8)
        lab_host.grid(row=2, column=0, columnspan=1)
        lab_host_port.grid(row=3, column=4, columnspan=1, ipadx=4)
        lab_client.grid(row=3, column=0, columnspan=1)
        lab_client_port.grid(row=3, column=4, columnspan=1)
        lab_midi_input.grid(row=5, column=1, columnspan=2, ipady=8)
        lab_midi_output.grid(row=5, column=5, columnspan=2, ipady=8)
        for n,p in enumerate(self._midi_input_ports):
            rb = factory.radio(south, str(p), self.var_input, str(p))
            rb.grid(row=n+6, column=1, sticky="W")
        for n,p in enumerate(self._midi_output_ports):
            rb = factory.radio(south, str(p), self.var_output, str(p))
            rb.grid(row=n+6, column=5, sticky="W")
        padding = Frame(south)
        padding.grid(row=0, column=7, ipadx=36)
        #padding.configure(background=factory.pallet["BG"])
        b_restore = factory.button(south, "Restore",
                                   command=restore_defaults,
                                   ttip="Restore default values")
        b_continue = factory.button(south, "Accept",
                                    command = self.accept,
                                    ttip="Accept values and move on")
        row = port_count + 6
        b_restore.grid(row=row, column=1, sticky="EW", pady=16)
        b_continue.grid(row=row, column=5, sticky="EW", pady=16)
        
        self.lab_warning = factory.warning_label(south)
        self.lab_warning.grid(row=6, column=7, sticky="EW",columnspan=2, rowspan=4)
        
    def warning(self, msg):
        self.lab_warning.configure(text=msg)

    @staticmethod
    def validate_port_number(prt):
        try:
            n = int(prt)
            return 0 <= n <= 65535
        except (ValueError, TypeError):
            return False

    @staticmethod
    def validate_address(addr):
        # Place holder function
        # We are not validating anything at this time
        return True
        
    def validate(self):
        prt = self.var_port.get()
        if not self.validate_port_number(prt):
            msg = "Invalid port: %s" % prt
            return msg
        prt = self.var_client_port.get()
        if not self.validate_port_number(prt):
            msg = "Invalid port: %s" % prt
            return msg
        addr = self.var_host.get()
        if not self.validate_address(addr):
            msg = "Invalid address: '%s'" % addr
            return msg
        addr = self.var_client.get()
        if not self.validate_address(addr):
            msg = "Invalid address: '%s'" % addr
            return msg
        return ""
        
    def accept(self):
        errmsg = self.validate()
        if not errmsg:
            self.config.global_osc_id(self.var_id.get())
            self.config["host"] = self.var_host.get()
            self.config["port"] = int(self.var_port.get())
            self.config["client"] = self.var_client.get()
            self.config["client_port"] = int(self.var_client_port.get())
            self.config["midi-receiver-name"] = self.var_input.get()
            self.config["midi-transmitter-name"] = self.var_output.get()
            self.destroy()
        else:
            self.warning(errmsg)
        
