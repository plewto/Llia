# llia.gui.tk.tk_splash
# 2016.05.20
#
# Defines initial splash screen allowing user to set OSC and MIDI
# parameters before main application starts.
# The ssplash screen may be bypassed by configuratin or command
# line flags.
#

from __future__ import print_function

import mido
from Tkinter import (BOTH, Button, Entry, Frame, Label,
                     Radiobutton, StringVar, Toplevel)
#import ttk  # Do not use ttk
from PIL import Image, ImageTk
from llia.gui.tk.tk_layout import VFrame
from llia.gui.tk.pallet import pallet

bg = pallet["bg"]
fg = pallet["fg"]
bbg = pallet["button-bg"]
warning_fg = pallet["warning-fg"]

def label(master, text):
    w = Label(master, text=text)
    w.config(background=bg, foreground=fg)
    return w

def button(master, text, command):
    b = Button(master, text = text, command=command)
    b.config(background=bbg, foreground=fg)
    b.config(highlightbackground=bg)
    return b
    
def radio(master, text, var, value):
    rb = Radiobutton(master, text=text, variable=var, value=value)
    rb.config(background=bg, foreground=fg)
    rb.config(activeforeground="yellow")
    rb.config(activebackground=bg)
    rb.config(selectcolor=bg)
    rb.config(highlightbackground=bg)
    return rb

def entry(master, var):
    e = Entry(master)
    e.config(textvariable=var)
    e.config(background=bg, foreground=fg)
    return e

def padding(master):
    w = Frame(master,background=bg)
    return w

class TkSplashWindow(Toplevel):

    def __init__(self, root, app):
        Toplevel.__init__(self, root)
        self.config(background=bg)
        self.title("Llia Setup")
        self.maxsize(660, 685)
        self.app = app
        self.config = app.config
        main = VFrame(self)
        main.pack(anchor="nw", expand=True, fill=BOTH)
        image = Image.open("resources/logos/llia_logo_medium.png")
        photo = ImageTk.PhotoImage(image)
        lab_logo = Label(main, image=photo)
        main.add(lab_logo)
        south = Frame(main, background=bg)
        main.add(south)
        self._build_south_panel(south)
        self.bind("<F1>", self.display_help)
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
        e_id = entry(south, self.var_id)
        e_host = entry(south, self.var_host)
        e_port = entry(south, self.var_port)
        e_client = entry(south, self.var_client)
        e_client_port = entry(south, self.var_client_port)
        padding(south).grid(row=0, column=0, ipadx=8, ipady=8)
        e_id.grid(row=1, column=1, columnspan=2)
        e_host.grid(row=2, column=1, columnspan=2)
        e_port.grid(row=2, column=5, columnspan=2)
        e_client.grid(row=3, column=1, columnspan=2)
        e_client_port.grid(row=3, column=5, columnspan=2)
        port_count = max(len(self._midi_input_ports),
                         len(self._midi_output_ports))
        lab_id = label(south, "OSC ID")
        lab_host = label(south, "Host")
        lab_host_port = label(south, "Port")
        lab_client = label(south, "Client")
        lab_client_port = label(south, "Port")
        lab_midi_input = label(south, "MIDI Input")
        lab_midi_output = label(south, "MIDI Output")
        padding(south).grid(row=4, column=3, ipadx=8, ipady=8)
        lab_id.grid(row=1, column=0, columnspan=1, ipadx=8, ipady=8)
        lab_host.grid(row=2, column=0, columnspan=1)
        lab_host_port.grid(row=3, column=4, columnspan=1, ipadx=4)
        lab_client.grid(row=3, column=0, columnspan=1)
        lab_client_port.grid(row=3, column=4, columnspan=1)
        lab_midi_input.grid(row=5, column=1, columnspan=2, ipady=8)
        lab_midi_output.grid(row=5, column=5, columnspan=2, ipady=8)
        for n,p in enumerate(self._midi_input_ports):
            rb = radio(south, str(p), self.var_input, str(p))
            rb.grid(row=n+6, column=1, sticky="W")
        for n,p in enumerate(self._midi_output_ports):
            rb = radio(south, str(p), self.var_output, str(p))
            rb.grid(row=n+6, column=5, sticky="W")
        padding(south).grid(row=0, column=7, ipadx=36)
        b_restore = button(south, "Restore", restore_defaults)
        b_continue = button(south, "Continue", self.accept)
        b_help = button(south, "?", self.display_help)
        row = port_count + 6
        b_restore.grid(row=row, column=1, sticky="EW", pady=16)
        b_continue.grid(row=row, column=5, sticky="EW", pady=16)
        b_help.grid(row=row, column=7, padx=8, sticky="W")
        self.lab_warning = label(south, "")
        self.lab_warning.config(foreground=warning_fg)
        self.lab_warning.grid(row=6, column=7, sticky="EW",
                              columnspan=2, rowspan=4)
        
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

    def display_help(self, *_):
        from llia.gui.tk.tk_help import display_help
        display_help("splash")
