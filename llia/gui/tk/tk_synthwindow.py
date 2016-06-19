# llia.gui.tk.tk_synthwindow
# 2016.06.11


from __future__ import print_function
from Tkinter import Toplevel, BOTH, StringVar
# from llia.gui.tk.tk_tabbed_window import TabbedWindow

import llia.gui.tk.tk_factory as factory
import llia.gui.pallet
from llia.gui.tk.tk_bankeditor import TkBankEditor

class TkSynthWindow(Toplevel):

    def __init__(self, sproxy):
        Toplevel.__init__(self, None)
        self.config(background=factory.bg())
        self.synth = sproxy
        self.app = sproxy.app
        self.sid = sproxy.sid
        factory.set_pallet(sproxy.specs["pallet"])
        main = factory.paned_window(self)
        main.pack(expand=True, fill=BOTH)
        banked = TkBankEditor(main, sproxy)
        notebook = factory.notebook(main)
        main.add(banked)
        main.add(notebook)

        self.list_channel = None
        self.list_keytab = None
        self.var_transpose = StringVar()
        self.var_keyrange_low = StringVar()
        self.var_keyrange_high = StringVar()
        self.var_bendrange = StringVar()
        
        self._init_performance_tab(notebook)
        self.sync()

    def _init_performance_tab(self, master):
        frame = factory.frame(master)
        master.add(frame, text = "Performance")
        frame_channel = factory.label_frame(frame, "MIDI Channel")
        frame_keytab = factory.label_frame(frame, "Key Table")
        lab_transpose = factory.label(frame, "Transpose")
        lab_keyrange = factory.label(frame, "Key Range")
        lab_bend = factory.label(frame, "Bend Range")
        self.list_channel = factory.listbox(frame_channel)
        sb_channel = factory.scrollbar(frame_channel)
        sb_channel.config(command=self.list_channel.yview)
        self.list_channel.config(yscrollcommand=sb_channel.set)
        self.list_keytab = factory.listbox(frame_keytab)
        sb_keytab = factory.scrollbar(frame_keytab)
        sb_keytab.config(command=self.list_keytab.yview)
        self.list_keytab.config(yscrollcommand=sb_keytab.set)
        spin_transpose = factory.int_spinbox(frame, self.var_transpose, -36, 36)
        spin_keylow = factory.int_spinbox(frame, self.var_keyrange_low, 0, 127)
        spin_keyhigh = factory.int_spinbox(frame, self.var_keyrange_high, 0, 127)
        spin_bendrange = factory.int_spinbox(frame, self.var_bendrange, 0, 2400)
        factory.padding_label(frame).grid(row=0)
        frame_channel.grid(row=1, column=0, rowspan=4, columnspan=2)
        self.list_channel.pack(side="left", expand=True, fill="both")
        sb_channel.pack(after=self.list_channel, side="right", expand=True, fill="y")
        frame_keytab.grid(row=1, column=2, rowspan=4, columnspan=2)
        self.list_keytab.pack(side="left", expand=True, fill="both")
        sb_keytab.pack(after=self.list_keytab, side="right", expand=True, fill="y")
        factory.padding_label(frame).grid(row=6)
        lab_transpose.grid(row=7, column=0, sticky="w", padx=4, pady=4)
        spin_transpose.grid(row=7, column=1, padx=4)
        lab_keyrange.grid(row=8, column=0, sticky="w", padx=4, pady=4)
        spin_keylow.grid(row=8, column=1, padx=4)
        spin_keyhigh.grid(row=8, column=2, padx=4)
        lab_bend.grid(row=9, column=0, sticky="w", padx=4, pady=4)
        spin_bendrange.grid(row=9, column=1, padx=4)

        def channel_callback(_):
            i = self.list_channel.curselection()[0]
            c = i+1
            self.synth.midi_input_channel(c)
            self.status("MIDI Input Channel = %s" % c)

        def keytab_callback(_):
            i = self.list_keytab.curselection()[0]
            kt = self.list_keytab.get(i)
            self.synth.keytable(kt)
            self.status("Using keytable: %s" % kt)

        def transpose_callback(*_):
            try:
                x = int(self.var_transpose.get())
                self.synth.transpose(x)
                self.status("Transpose = %s" % x)
            except ValueError:
                self.warning("Invalid transpose")
                
        def keyrange_callback(*_):
            try:
                a = int(self.var_keyrange_low.get())
                b = int(self.var_keyrange_high.get())
                a, b = min(a,b), max(a,b)
                self.synth.key_range((a,b))
                self.status("Key range = [%3d, %3d]" % (a, b))
            except ValueError:
                self.warning("Invalid keyrange")
                
        def bend_callback(*_):
            try:
                b = int(self.var_bendrange.get())
                self.synth.bend_range(b)
                self.status("Bend range = %s" % b)
            except ValueError:
                self.warning("Invalid Bendrange")
        
        self.list_channel.bind("<<ListboxSelect>>", channel_callback)
        self.list_keytab.bind("<<ListboxSelect>>", keytab_callback)
        spin_transpose.config(command=transpose_callback)
        spin_transpose.bind("<Return>", transpose_callback)
        spin_keylow.config(command=keyrange_callback)
        spin_keylow.bind("<Return>", keyrange_callback)
        spin_keyhigh.config(command=keyrange_callback)
        spin_keyhigh.bind("<Return>", keyrange_callback)
        spin_bendrange.config(command=bend_callback)
        spin_bendrange.bind("<Return>", bend_callback)

    def status(self, msg):
        print("STATUS: ", msg)

    def warning(self, msg):
        print("WARNING: ", msg)

        
    def sync(self, ignore=None):
        self.list_channel.delete(0, "end")
        for c in self.app.config.channel_assignments.formatted_list():
            self.list_channel.insert("end", c)
        mic = self.synth.midi_input_channel()-1
        self.list_channel.selection_set(mic)
        self.list_keytab.delete(0, "end")
        target, index = self.synth.keytable(), 0
        for i, kt in enumerate(sorted(self.app.keytables.keys())):
            self.list_keytab.insert("end", kt)
            if target == kt: index = i
        self.list_keytab.selection_set(index)
        self.var_transpose.set(self.synth.transpose())
        lo, hi = self.synth.key_range()
        self.var_keyrange_low.set(lo)
        self.var_keyrange_high.set(hi)
        self.var_bendrange.set(self.synth.bend_range())
            
