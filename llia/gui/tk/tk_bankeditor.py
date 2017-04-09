# llia.gui.tk.tk_bankeditor
# 2016.06.05

from __future__ import print_function
import os.path

from Tkinter import (Toplevel, Frame, StringVar)
import tkFileDialog

import llia.gui.tk.tk_factory as factory
import llia.gui.tk.tk_layout as layout
from llia.gui.tk.tk_init_warning import init_warning

HELP_TOPIC = "bank-editor"

class TkBankEditor(Frame):

    def __init__(self, master, parent_editor, synth):
        Frame.__init__(self, master)
        self.config(background=factory.bg())
        self.parent_editor = parent_editor
        self.synth = synth
        self.app = synth.app
        self.listbox = None
        self._var_lock_current = StringVar()
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
        self.sync_no_propegate()

        
    def _init_north_toolbar(self):
        frame = factory.frame(self)
        toolbar = factory.label_frame(frame, "Bank")
        specs = self.synth.specs
        format_ = specs["format"]
        sid = self.synth.sid
        logo_filename = os.path.join("resources", format_, "logo_small.png")
        lab_logo = factory.image_label(frame, logo_filename, format_)
        lab_sid = factory.label(frame, "ID = %s" % sid)
        b_open = factory.button(toolbar, "Open", ttip="Read bank file", 
                                command=self._open_bank)
        b_save = factory.button(toolbar, "Save", ttip="Save bank file", 
                                command=self._save_bank)
        b_init = factory.button(toolbar, "Init", ttip="Initialize bank", 
                                command=self._init_bank)
        b_rem = factory.button(toolbar, "Rem", ttip="Edit bank remarks", 
                               command=self._edit_remarks)
        b_help = factory.help_button(toolbar, command= self._help)
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
        b_pcopy = factory.button(frame, "Copy", 
                                 ttip="Copy current performance to clipboard",
                                 command = self._copy_performance)
        b_ppaste = factory.button(frame, "Paste", 
                                  ttip="Paste clipboard to current performance",
                                  command = self._paste_performance)
        b_pfill = factory.button(frame, "Fill", 
                                 ttip="Copy performance to multiple bank slots",
                                 command = self._fill_performance)
        b_pcopy.grid(row=0, column=0, sticky="ew")
        b_ppaste.grid(row=0, column=1, sticky="ew")
        b_pfill.grid(row=0, column=2, sticky="ew")
        return frame
        
    def _init_south_toolbar(self):
        frame = factory.label_frame(self, "Program")
        b_store = factory.button(frame, "Store", command=self._store_program,
                                 ttip = "Store current program")
        b_random = factory.button(frame, "RND", command=self._random_program,
                                  ttip = "Generate random program (if defined)")
        b_init = factory.button(frame, "Init", command=self._init_program,
                                ttip = "Initialize program")
        b_copy = factory.button(frame, "Copy", command=self._copy_program,
                                ttip="Copy current prgoram to clipbaord")
        b_paste = factory.button(frame, "Paste", command=self._paste_program,
                                 ttip="Paste clipboard to current program")
        cb_lock = factory.checkbutton(frame,"Lock",self._var_lock_current,
                                     command = self.lock_current_program)
        b_store.grid(row=0, column=0, sticky="ew")
        b_random.grid(row=0, column=1, sticky="ew")
        b_init.grid(row=0, column=2, sticky="ew")
        b_copy.grid(row=1, column=0, sticky="ew")
        b_paste.grid(row=1, column=1, sticky="ew")
        cb_lock.grid(row=1, column=2, sticky="ew")
        return frame

    def lock_current_program(self):
        flag = int(self._var_lock_current.get()) == 1
        bnk = self.synth.bank()
        bnk.lock_current_program = flag
        msg = "Current Program "
        if flag:
            msg += "locked"
        else:
            msg += "unlocked"
        self.status(msg)
        
        
    def status(self, msg):
        self.parent_editor.status(msg)

    def warning(self, msg):
        self.parent_editor.warning(msg)
    
    def sync_no_propegate(self):
        bnk = self.synth.bank()
        count = len(bnk)
        self.listbox.delete(0, count)
        for slot in range(count):
            prg = bnk[slot]
            name = prg.name
            self.listbox.insert("end", "[%03d] %s" % (slot, name))
        slot = bnk.current_slot
        program = bnk[None]
        self.listbox.selection_set(slot)
        self.listbox.see(slot)
        txt = "%03d %-8s" % (slot, program.name[:8])
        self.big_label.config(text = txt)
        if bnk.lock_current_program:
            self._var_lock_current.set(1)
        else:
            self._var_lock_current.set(0)

    def sync(self):
        self.sync_no_propegate()
        self.parent_editor.sync("bank")
        
    def _select_slot(self, _):
        slot = self.listbox.curselection()[0]
        self.synth.use_program(slot)
        self.sync() # ISSUE: Remove after testing

    def _decrement_selection(self, _):
        slot = self.listbox.curselection()[0]
        slot = max(slot-1, 0)
        self.synth.use_program(slot)
        self.sync() # ISSUE: Remove after testing

    def _increment_selection(self, _):
        count = len(self.synth.bank())
        slot = self.listbox.curselection()[0]
        slot = min(slot+1, count-1)
        self.synth.use_program(slot)
        self.sync() # ISSUE: Remove after testing

    def _open_bank(self):
        bnk = self.synth.bank()
        specs = self.synth.specs
        ext = ".%s" % specs["format"].lower()
        ftypes = (("%s bank" % specs["format"], "*%s" % ext),
                  ("All files", "*"))
        ifile = bnk.filename
        title ="Open %s Bank" % specs["format"]
        flag = init_warning("Read Bank File (can not be undone) ?", self.app)
        if flag:
            rs = tkFileDialog.askopenfilename(parent=self,
                                              defaultextension = ext,
                                              filetypes = ftypes,
                                              initialfile = ifile,
                                              title = title)
            if rs:
                try:
                    self.parent_editor.busy(True,"Loading program bank")
                    bnk.load(rs, self.parent_editor)
                    self.sync()
                    self.parent_editor.busy(False)
                    self.status("Loaded bankfile '%s'" % rs)
                except (ValueError, TypeError, IOError) as err:
                    msg = "Error while reading bank file '%s'" % rs
                    self.warning(msg)
                    print(err.message)
        else:
            msg = "Read bank canceled"
            self.status(msg)
        
    def _save_bank(self):
        bnk = self.synth.bank()
        specs = self.synth.specs
        ext = ".%s" % specs["format"].lower()
        ftypes = (("%s bank" % specs["format"], "*%s" % ext),
                  ("All files", "*"))
        ifile = bnk.filename
        title = "Save %s Bank" % specs["format"]
        rs = tkFileDialog.asksaveasfilename(parent=self,
                                                defaultextension = ext,
                                                filetypes = ftypes,
                                                initialfile = ifile,
                                                title = title)
        if rs:
            try:
                bnk.save(rs)
                self.status("Bank saved to '%s'" % rs)
            except IOError as err:
                self.warning("Error while saving '%s'" % rs)
                print(err.message)
        else:
            self.status("Bank save canceld")

    def _init_bank(self):
        msg = "Initialize Bank ?"
        flag = init_warning(msg, self.app)
        if flag:
            self.synth.bank().initialize()
            self.sync()
            self.status("Bank initialized")
        else:
            self.status("Bank initialize canceled")
        
    def _edit_remarks(self):
        bnk = self.synth.bank()
        name = bnk.name
        filename = bnk.filename
        remarks = bnk.remarks
        dialog = Toplevel(self)
        frame = factory.frame(dialog, True)
        frame.pack(expand=True, fill="both")
        lab_title = factory.center_label(frame, "Bank Info")
        lab_name = factory.label(frame, "Bank name :  '%s'" % name)
        lab_filename = factory.label(frame, "Filename :  '%s'" % filename)
        frame_text = factory.label_frame(frame, "Remarks")
        lab_title.grid(row=0, column=0, columnspan=3,pady=12)
        lab_name.grid(row=1, column=0, sticky="w", padx=4)
        lab_filename.grid(row=2, column=0, sticky="w", padx=4)
        frame_text.grid(row=3, column=0, columnspan=3, padx=4, pady=8)
        text_widget = factory.text_widget(frame_text, "Bank remarks")
        text_widget.insert('end', remarks)
        text_widget.config(width=80, height=20)
        vsb = factory.scrollbar(frame_text, orientation="vertical")
        hsb = factory.scrollbar(frame_text, orientation="horizontal")
        text_widget.grid(row=0, column=0, rowspan=8, columnspan=8, ipadx=4, ipady=4)
        vsb.grid(row=0, column=8, rowspan=8, columnspan=1, sticky="ns")
        hsb.grid(row=8, column=0, rowspan=1, columnspan=8, sticky="ew")
        vsb.config(command=text_widget.yview)
        hsb.config(command=text_widget.xview)
        text_widget.config(yscrollcommand=vsb.set)
        text_widget.config(xscrollcommand=hsb.set)

        frame_toolbar = factory.frame(frame, True)
        frame_toolbar.grid(row=4, column=0, padx=4, pady=8)

        def clear():
            text_widget.delete(1.0, 'end')

        def accept():
            rem = text_widget.get(1.0, 'end')
            bnk.remarks = rem
            self.status("Bank remarks updated")
            dialog.destroy()

        def cancel():
            self.status("Change bank remarks canceld")
            dialog.destroy()
            
        b_clear = factory.clear_button(frame_toolbar, command=clear, ttip="Clear remarks")
        b_accept = factory.accept_button(frame_toolbar, command=accept)
        b_cancel = factory.cancel_button(frame_toolbar, command=cancel)
        b_clear.grid(row=0, column=0, padx=4, pady=8)
        b_accept.grid(row=0, column=1)
        b_cancel.grid(row=0, column=2)
        dialog.grab_set()
        dialog.mainloop()
    
    def _help(self):
        self.app.main_window().display_help(HELP_TOPIC)

    def _copy_performance(self):
        bnk = self.synth.bank()
        bnk.copy_performance()
        self.status("Performance copied to clipboard")

    def _paste_performance(self):
        try:
            bnk = self.synth.bank()
            bnk.paste_performance()
            self.sync()
            self.status("Clipboard pasted to performance")
        except KeyError:
            msg = "Performance clipboard empty"
            self.warning(msg)

    def _fill_performance(self):
        bnk = self.synth.bank()
        dialog = Toplevel(self)
        frame = factory.frame(dialog, True)
        frame.pack(expand=True, fill="both")
        lab_title = factory.label(frame, "Fill Performance", modal=True)
        lab_start = factory.label(frame, "Starting slot", modal=True)
        lab_end = factory.label(frame, "Ending slot", modal=True)
        var_start = StringVar()
        var_end = StringVar()
        spin_start = factory.int_spinbox(frame, var_start, 0, len(bnk))
        spin_end = factory.int_spinbox(frame, var_end, 0, len(bnk))
        var_start.set(bnk.current_slot)
        var_end.set(bnk.current_slot+1)
        lab_title.grid(row=0, column=0, columnspan=3, padx=4, pady=8)
        lab_start.grid(row=1, column=0, sticky="w", padx=4)
        spin_start.grid(row=1, column=1, columnspan=2, padx=4)
        lab_end.grid(row=2, column=0, sticky="w", padx=4)
        spin_end.grid(row=2, column=1, columnspan=2, padx=4)

        def accept():
            try:
                a,b = int(var_start.get()), int(var_end.get())
                bnk.fill_performance(a,b)
                msg = "Performance filled slots [%3d, %3d]" % (a,b)
                self.status(msg)
                dialog.destroy()
            except ValueError:
                msg = "Invalid slot number"
                self.warning(msg)
            except KeyError as err:
                self.warning(err.message)
                

        def cancel():
            msg = "Performance fill canceld"
            self.status(msg)
            dialog.destroy()
            
        b_accept = factory.accept_button(frame, command=accept)
        b_cancel = factory.cancel_button(frame, command=cancel)
        b_accept.grid(row=3, column=1, padx=4, pady=8,sticky="ew")
        b_cancel.grid(row=3, column=2, padx=4, pady=8,sticky="ew")
        dialog.grab_set()
        dialog.mainloop()

    def _store_program(self):
        bnk = self.synth.bank()
        program = bnk[None]
        slot = bnk.current_slot
        var_name = StringVar()
        var_start = StringVar()
        var_name.set(program.name)
        var_start.set(slot)
        dialog = Toplevel()
        frame = factory.frame(dialog, True)
        frame.pack(expand=True, fill="both")
        lab_title = factory.label(frame, "Store Program", modal=True)
        lab_name = factory.label(frame, "Name", modal=True)
        lab_start = factory.label(frame, "Slot", modal=True)
        entry_name = factory.entry(frame, var_name, "Program name")
        spin_start = factory.int_spinbox(frame, var_start, 0, len(bnk), "Startng slot")
        frame_remarks = factory.label_frame(frame, "Remarks", True)
        text_remarks = factory.text_widget(frame_remarks, "Remarks text", modal=True)
        text_remarks.insert("end", program.remarks)
        vsb = factory.scrollbar(frame_remarks, orientation="vertical")
        hsb = factory.scrollbar(frame_remarks, orientation="horizontal")
        text_remarks.config(width=40, height=10)
        text_remarks.grid(row=0, column=0, rowspan=4, columnspan=4)
        vsb.grid(row=0, column=4, rowspan=4, sticky="ns")
        hsb.grid(row=4, column=0, columnspan=4, sticky="ew")
        vsb.config(command=text_remarks.yview)
        hsb.config(command=text_remarks.xview)
        text_remarks.config(yscrollcommand=vsb.set)
        text_remarks.config(xscrollcommand=hsb.set)
        lab_title.grid(row=0, column=0, columnspan=3, pady=8, padx=4)
        lab_name.grid(row=1, column=0, padx=4)
        entry_name.grid(row=1, column=1, columnspan=2)
        frame_remarks.grid(row=2, column=0, rowspan=4, columnspan=4, padx=4, pady=4)
        lab_start.grid(row=6, column=0, padx=4, sticky="w")
        spin_start.grid(row=6, column=1, columnspan=2, pady=4)
        b_accept = factory.accept_button(frame)
        b_cancel = factory.cancel_button(frame)
        b_accept.grid(row=8, column=1, pady=8, sticky="ew")
        b_cancel.grid(row=8, column=2, pady=8, sticky="ew")
        
        def accept():
            try:
                a = int(var_start.get())
                name = var_name.get()
                remarks = text_remarks.get(1.0, "end")
                program.name = name
                program.remarks = remarks
                bnk[a] = program
                msg = "Stored program '%s' to slots [%3d]" % (name, a)
                self.status(msg)
                dialog.destroy()
                self.sync()
            except ValueError:
                msg = "Invalid slot number"
                self.warning(msg)

        def cancel():
            msg = "Store program canceld"
            self.status(msg)
            dialog.destroy()

        b_accept.config(command=accept)
        b_cancel.config(command=cancel)
        dialog.grab_set()
        dialog.mainloop()
        
    def _random_program(self):
        p = self.synth.random_program()
        if p:
            bnk = self.synth.bank()
            end = len(bnk)-1
            bnk[end] = p
            self.synth.use_program(end)
            self.sync()
            msg = "Random Program"
            self.status(msg)
        else:
            msg = "Random program function not defined"
            self.warning(msg)

    def _init_program(self):
        flag = init_warning("Initialize Program ?", self.app)
        if flag:
            bnk = self.synth.bank()
            prog = bnk.create_program()
            bnk.current_program = prog
            msg = "Program intialized"
            self.status(msg)
            self.sync()
        else:
            msg = "Program initialize canceld"
            self.status(msg)
            
    def _copy_program(self):
        bnk = self.synth.bank()
        bnk.copy_to_clipboard()
        msg = "Current program copied to clipboard"
        self.status(msg)

    def _paste_program(self):
        bnk = self.synth.bank()
        try:
            bnk.paste_clipboard()
            msg = "Clipbaord pasted to current program"
            self.status(msg)
            self.sync()
        except KeyError:
            msg = "Clipboard does not contain %s program"
            msg = msg % self.synth.specs["format"]
            self.warning(msg)
