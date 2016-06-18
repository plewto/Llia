# llia.gui.tk.tk_bankeditor
# 2016.06.05

from __future__ import print_function
import os.path

from Tkinter import (BOTH, Frame)

import llia.gui.tk.tk_factory as factory
import llia.gui.tk.tk_layout as layout


class TkBankEditor(Frame):

    def __init__(self, master, synth):
        Frame.__init__(self, master)
        self.config(background=factory.bg())
        self.synth = synth
        self.listbox = None
        north = self._init_north_toolbar()
        center = self._init_list_frame()
        perf_frame = self._init_performance_toolbar()
        south = self._init_south_toolbar()
        north.pack(pady=4, padx=4)
        center.pack(expand=True, fill="both", padx=4, pady=4)
        perf_frame.pack(padx=4, pady=4)
        south.pack(padx=4, pady=4)
        self.big_label = factory.big_label(self, "000 ABCDEFGH")
        self.big_label.pack()
        self.sync()
        
    def _init_north_toolbar(self):
        frame = factory.frame(self)
        toolbar = factory.label_frame(frame, "Bank")
        specs = self.synth.specs
        format_ = specs["format"]
        sid = self.synth.sid
        logo_filename = os.path.join("resources", format_, "logo_small.png")
        lab_logo = factory.image_label(frame, logo_filename, format_)
        lab_sid = factory.label(frame, "ID = %s" % sid)
        b_open = factory.button(toolbar, "Open", ttip="Read bank file")
        b_save = factory.button(toolbar, "Save", ttip="Save bank file")
        b_init = factory.button(toolbar, "Init", ttip="Initialize bank")
        b_rem = factory.button(toolbar, "Rem", ttip="Edit bank remarks")
        b_help = factory.help_button(toolbar)
        b_open.grid(row=0, column=0, sticky="ew")
        b_save.grid(row=0, column=1, sticky="ew")
        b_init.grid(row=0, column=2, sticky="ew")
        b_rem.grid(row=1, column=0, sticky="ew")
        b_help.grid(row=1, column=1, sticky="ew")
        lab_logo.grid(row=0, column=0, sticky='w', pady=4)
        lab_sid.grid(row=0, column=1, columnspan=2)
        toolbar.grid(row=1, column=0, columnspan=2)
        return frame
        
    def _init_list_frame(self):
        frame = factory.frame(self)
        lbx = factory.listbox(frame)
        sbar = factory.scrollbar(frame, orientation="vertical")
        lbx.pack(side="left", expand=True, fill="both")
        sbar.pack(after=lbx, side="right", expand=True, fill="y")
        lbx.config(yscrollcommand=sbar.set)
        lbx.bind("<<ListboxSelect>>", self._select_slot)
        lbx.bind("<Up>", self._decrement_selection)
        lbx.bind("<Down>", self._increment_selection)
        sbar.config(command = lbx.yview)
        self.listbox = lbx
        return frame
    
    def _init_performance_toolbar(self):
        frame = factory.label_frame(self, "Performance")
        b_pcopy = factory.button(frame, "Copy", ttip="Copy current performance to clipboard")
        b_ppaste = factory.button(frame, "Paste", ttip="Paste clipboard to current performance")
        b_pfill = factory.button(frame, "Fill", ttip="Copy current performance to multiple bank slots")
        b_pcopy.grid(row=0, column=0, sticky="ew")
        b_ppaste.grid(row=0, column=1, sticky="ew")
        b_pfill.grid(row=0, column=2, sticky="ew")
        return frame
        
    def _init_south_toolbar(self):
        frame = factory.label_frame(self, "Program")
        b_store = factory.button(frame, "Store")
        b_random = factory.button(frame, "RND")
        b_init = factory.button(frame, "Init")
        b_copy = factory.button(frame, "Copy", ttip="Copy current prgoram to clipbaord")
        b_paste = factory.button(frame, "Paste", ttip="Paste clipboard to current program")
        b_store.grid(row=0, column=0, sticky="ew")
        b_random.grid(row=0, column=1, sticky="ew")
        b_init.grid(row=0, column=2, sticky="ew")
        b_copy.grid(row=1, column=0, sticky="ew")
        b_paste.grid(row=1, column=1, sticky="ew")
        return frame
        
    def sync(self):
        bnk = self.synth.bank()
        count = len(bnk)
        self.listbox.delete(0, count)
        for slot in range(count):
            prg = bnk[slot]
            name = prg.name
            self.listbox.insert("end", "[%03d] %s" % (slot, name))
        slot = bnk.current_slot
        program = bnk[slot]
        self.listbox.selection_set(slot)
        self.listbox.see(slot)
        txt = "%03d %-8s" % (slot, program.name[:8])
        self.big_label.config(text = txt)
        
    def _select_slot(self, _):
        slot = self.listbox.curselection()[0]
        self.synth.use_program(slot)
        #self.sync()

    def _decrement_selection(self, _):
        slot = self.listbox.curselection()[0]
        slot = max(slot-1, 0)
        self.synth.use_program(slot)
        #self.sync()

    def _increment_selection(self, _):
        count = len(self.synth.bank())
        slot = self.listbox.curselection()[0]
        slot = min(slot+1, count-1)
        self.synth.use_program(slot)
        #self.sync()
