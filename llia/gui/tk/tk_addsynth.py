# llia.gui.tk.tk_addsynth
# 2016.06.11

from __future__ import print_function

from Tkinter import (BOTH, W, EW, E, Toplevel, StringVar)
from ttk import (Frame,)
import llia.constants as con
import llia.gui.tk.tk_factory as factory


class TkAddSynthDialog(Toplevel):


    id_dict = {}

    def __init__(self, master, app):
        Toplevel.__init__(self, master)
        self.wm_title = "Add Synth"
        self.app = app
        self.proxy = app.proxy
        main = Frame(self)
        main.pack(expand=True, fill=BOTH)
        self.var_synth_type = StringVar()
        self.var_synth_id = StringVar()
        self.var_keymode = StringVar()
        self.var_voice_count = StringVar()
        self.var_outbus_param = StringVar()
        self.combo_outbus_name = None
        self.var_outbus_offset = StringVar()
        self.var_outbus_offset.set("0")
        self.lab_warning = factory.warning_label(main)
        frame_synth = self._init_synth_selection_frame(main)
        frame_keymode = self._init_keymode_selection_frame(main)
        frame_bus = self._init_outbus_frame(main)
        frame_tools = self._init_toolbar(main)
        w = factory.dialog_title_label(main, "Add Synth")
        w.grid(row=0, column=0, columnspan=2, pady=8)
        frame_synth.grid(row=1, column = 0, columnspan=2, sticky=EW, padx=4, pady=4)
        frame_keymode.grid(row=2, column=0, columnspan=2, sticky=EW, padx=4, pady=4)
        frame_bus.grid(row=3, column=0, columnspan=2, sticky=EW, padx=4, pady=4)
        frame_tools.grid(row=4, column=0, columnspan=2, sticky=EW, padx=4, pady=4)
        self.lab_warning.grid(row=5, column=0, columnspan=2, sticky=W, padx=4, pady=4)
        self.grab_set()
        self.mainloop()
        
    def _init_synth_selection_frame(self, master):
        frame = factory.label_frame(master, "Synths")
        row = 1
        for s in sorted(con.SYNTH_TYPES):
            if row == 1: self.var_synth_type.set(s)
            rb = factory.radio(frame, s, self.var_synth_type, s)
            rb.grid(row=row, column=0, sticky=W, padx=4)
            row += 1
            rb.config(command=self._autoset_id)
        w = factory.label(frame, "Synth ID")
        w.grid(row=row, column=0, sticky = W, padx=4, pady=4)
        sb = factory.int_spinbox(frame, self.var_synth_id, from_=1, to=100)
        sb.grid(row=row, column = 1, padx=4, pady=8, sticky=E)
        return frame

    def _init_keymode_selection_frame(self, master):
        frame = factory.label_frame(master, "Key Mode")
        row = 1
        for km in sorted(con.KEY_MODES):
            rb = factory.radio(frame, km, self.var_keymode, value=km)
            rb.grid(row=row, column = 0, sticky=W, padx=4)
            row += 1
        self.var_keymode.set("Poly1")
        w = factory.label(frame, "Voice Count")
        w.grid(row=row, column = 0, padx=4)
        sb = factory.int_spinbox(frame, self.var_voice_count, from_=1, to=64)
        sb.grid(row=row, column = 1, padx=4, pady=8)
        self.var_voice_count.set(8)
        return frame

    def _init_outbus_frame(self, master):
        frame = factory.label_frame(master, "Output Bus")
        w = factory.label(frame, "Bus")
        cb_buses = factory.combobox(frame, self.proxy.audio_bus_keys())
        w.grid(row=0, column=0, sticky=W, padx=4)
        cb_buses.grid(row=0, column=1, padx=4, pady=4, sticky=E)
        w = factory.label(frame, "Param")
        entry = factory.entry(frame, self.var_outbus_param)
        self.var_outbus_param.set("outbus")
        w.grid(row=1, column=0, sticky=W, padx=4, pady=4)
        entry.grid(row=1, column=1, padx=4, pady=4, sticky=EW)
        w = factory.label(frame, "Offset")
        sp = factory.int_spinbox(frame, self.var_outbus_offset, from_=0, to=128)
        w.grid(row=2, column=0, sticky=W, padx=4, pady=4)
        sp.grid(row=2, column=1, padx=4, pady=4, sticky=E)
        self.combo_outbus_name = cb_buses
        cb_buses.set("out_0")
        return frame

    def _init_toolbar(self, master):
        frame = Frame(master)
        b_help = factory.help_button(frame, command=self.display_help)
        b_ok = factory.accept_button(frame, command=self.accept)
        b_cancel = factory.cancel_button(frame, command=self.cancel)
        b_help.grid(row=0, column=0, sticky=W)
        b_ok.grid(row=0, column=1, sticky=E)
        b_cancel.grid(row=0, column=2, sticky=E)
        return frame
    
    def _autoset_id(self):
        st = self.var_synth_type.get()
        n = self.id_dict[st]
        self.var_synth_id.set(n)

    def warning(self, msg=""):
        if msg:
            msg = "WARNING: %s" % msg
            self.lab_warning.config(text=msg)
        else:
            self.lab_warning.config(text = "")
        
    def display_help(self):
        self.app.main_window().display_help("add_synth_dialog")

    def cancel(self):
        self.app.main_window().status("Add Synth Canceld")
        self.destroy()

    def accept(self):
        shelper = self.app.ls_parser.synthhelper
        st = self.var_synth_type.get()
        id_ = int(self.var_synth_id.get())
        km = self.var_keymode.get()
        vcount = int(self.var_voice_count.get())
        outbus = self.combo_outbus_name.get()
        param = self.var_outbus_param.get()
        offset = int(self.var_outbus_offset.get())
        rs = shelper.add_synth(st, id_, km, vcount, [outbus, param, offset])
        if rs:
            self.id_dict[st] = self.id_dict[st]+1
            sid = "%s_%s" % (st, id_)
            self.app.main_window().status("Added synth %s" % sid)
            self.destroy()
        else:
            self.warning("Synth could not be added")
        
for s in con.SYNTH_TYPES:
    TkAddSynthDialog.id_dict[s] = 1
    
