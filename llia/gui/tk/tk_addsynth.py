from __future__ import print_function

from Tkinter import (BOTH, W, EW, E, X, LEFT, Toplevel, StringVar)
#from ttk import (Frame,)
import llia.constants as con
import llia.gui.tk.tk_factory as factory
from llia.synth_proxy import SynthSpecs
from llia.gui.tk.tk_synthwindow import TkSynthWindow


HELP_TOPIC = "add_synth_dialog"

def select_synth_id(app, stype):
    n = 1
    while True:
        if not app.proxy.synth_exists(stype, n):
            return n
        else:
            n = n+1

        
class TkAddSynthDialog(Toplevel):

    def __init__(self, master, app, synth_type, is_efx=False, is_controller=False):
        Toplevel.__init__(self, master)
        main = factory.frame(self)
        main.pack(anchor=W, expand=True, fill=BOTH)
        self.app = app
        self.stype = synth_type
        self.is_efx = is_efx
        self.is_controller = is_controller
        self.id_ = select_synth_id(self.app, synth_type)
        self.sid = "%s_%d" % (synth_type, self.id_)
        specs = SynthSpecs.global_synth_type_registry[synth_type]
        self._busname_map = {}   # Maps synth parameters to bus name Comboboxes
        self._busoffset_map = {} # Maps synth parameters to bus offset var
        self._buffername_map = {}
        title = "Add %s " % synth_type
        if is_efx:
            title += "Effect"
        elif is_controller:
            title += "Controller Synth"
        else:
            title += "Synth"
        title += "      sid = %s" % self.sid
        w = factory.dialog_title_label(main, title)
        w.grid(row = 0, column = 0, sticky="w", padx=4, pady=8)

        def spinbox(master, param):
            var = StringVar()
            var.set("0")
            sp  = factory.int_spinbox(master, var, 0, 128, "Bus offset")
            self._busoffset_map[param] = var
            return sp
        
        # Audio Output Buses
        frame_audio_out = factory.label_frame(main, "Audio Output Buses")
        row = 0
        for b in specs["audio-output-buses"]:
            bname = b[0]
            lab_name = factory.label(frame_audio_out, bname)
            combo = factory.audio_bus_combobox(frame_audio_out, self.app)
            combo.set("out_0")
            lab_name.grid(row=row, column=0, sticky="w", padx=4, pady=4)
            self._busname_map[bname] = combo
            spin = spinbox(frame_audio_out, bname)
            combo.grid(row=row, column=1, sticky="w", padx=4, pady=4)
            spin.grid(row=row, column=2, sticky="e", padx=4, pady=4)
            row += 1
        factory.padding_label(frame_audio_out).grid(row=row, column=0)
        frame_audio_out.grid(row=5, column=0, padx=4, pady=4)
        
        # Audio Input Buses
        if specs["audio-input-buses"]:
            frame_audio_in = factory.label_frame(main, "Audio Input Buses")
            row = 0
            for b in specs["audio-input-buses"]:
                bname = b[0]
                lab_name = factory.label(frame_audio_in, bname)
                combo = factory.audio_bus_combobox(frame_audio_in, self.app)
                combo.set("in_0")
                lab_name.grid(row=row, column=0, sticky="w", padx=4, pady=4)
                self._busname_map[bname] = combo
                spin = spinbox(frame_audio_in, bname)
                combo.grid(row=row, column=1, sticky="w", padx=4, pady=4)
                spin.grid(row=row, column=2, sticky="w", padx=4, pady=4)
                row += 1
            factory.padding_label(frame_audio_in).grid(row=row, column=0)
            frame_audio_in.grid(row=1, column=0, padx=4, pady=4)

        # Control Output Buses
        if specs["control-output-buses"]:
            frame_control_out = factory.label_frame(main, "Control Output Buses")
            row = 0
            for b in specs["control-output-buses"]:
                bname = b[0]
                lab_name = factory.label(frame_control_out, bname)
                combo = factory.control_bus_combobox(frame_control_out, self.app)
                combo.set("CBUS_A")
                lab_name.grid(row=row, column=0, sticky="w", padx=4, pady=4)
                self._busname_map[bname] = combo
                spin = spinbox(frame_control_out, bname)
                combo.grid(row=row, column=1, sticky="w", padx=4, pady=4)
                spin.grid(row=row, column=2, sticky="w", padx=4, pady=4)
                row += 1
            factory.padding_label(frame_control_out).grid(row=row, column=0)
            frame_control_out.grid(row=5, column=3, padx=4, pady=4)
        
        # # Control Input Buses
        if specs["control-input-buses"]:
            frame_control_in = factory.label_frame(main, "Control Input Buses")
            row = 0
            for b in specs["control-input-buses"]:
                bname = b[0]
                lab_name = factory.label(frame_control_in, bname)
                combo = factory.control_bus_combobox(frame_control_in, self.app)
                combo.set("CBUS_A")
                lab_name.grid(row=row, column=0, sticky="w", padx=4, pady=4)
                self._busname_map[bname] = combo
                spin = spinbox(frame_control_in, bname)
                combo.grid(row=row, column=1, sticky="w", padx=4, pady=4)
                spin.grid(row=row, column=2, sticky="w", padx=4, pady=4)
                row += 1
            factory.padding_label(frame_control_in).grid(row=row, column=0)
            frame_control_in.grid(row=1, column=3, padx=4, pady=4)

        # # Buffers
        if specs["buffers"]:
            frame_buffers = factory.label_frame(main, "Buffers")
            row = 0
            for bname in specs["buffers"]:
                lab_name = factory.label(frame_buffers, bname)
                combo = factory.buffer_combobox(frame_buffers, self.app)
                lab_name.grid(row=row, column=0, sticky="w", padx=4, pady=4)
                combo.grid(row=row, column=1, sticky="w", padx=4, pady=4)
                self._buffername_map[bname] = combo
                row += 1
            factory.padding_label(frame_buffers).grid(row=row, column=0)
            frame_buffers.grid(row=9, column=3, padx=4, pady=4)

        # # Keymode
        self.var_keymode = StringVar()
        self.var_voice_count = StringVar()
        self.var_voice_count.set(8)
        frame_keymode = factory.label_frame(main, "Key mode")
        col = 0
        for km in specs["keymodes"]:
            rb = factory.radio(frame_keymode, km, self.var_keymode, km)
            rb.grid(row=0, column=col, sticky="w", padx=4, pady=4)
            # if self.is_efx:
            #     rb.config(state="disabled")
            col += 1
        self.var_keymode.set(specs["keymodes"][0])  # Set default keymode
       
        lab_vc = factory.label(frame_keymode, "Voice count")
        spin_vc = factory.int_spinbox(frame_keymode, self.var_voice_count, from_=1, to=128)
        # voice count spin_vc is place hoder for future.
        lab_vc.grid(row=1, column=0, padx=4)
        spin_vc.grid(row=1, column=1, columnspan=3, padx=4, pady=4)
        frame_keymode.grid(row=9, column=0, padx=4, pady=4)
        factory.padding_label(frame_keymode).grid(row=2, column=0)
        # South Toolbar
        toolbar = factory.frame(main)
        b_help = factory.help_button(toolbar, command=self.display_help)
        b_accept = factory.accept_button(toolbar, command=self.accept)
        b_cancel = factory.cancel_button(toolbar, command=self.cancel)
        b_help.grid(row=0, column=0, sticky="w")
        factory.padding_label(toolbar).grid(row=0, column=1)
        b_accept.grid(row=0, column=2, sticky="e")
        b_cancel.grid(row=0, column=3, sticky="e")
        toolbar.grid(row=10, column=0, columnspan=5, sticky="ew", padx=4, pady=8)
        #self.grab_set() # ISSUE: Throws TclError: grab failed: window not viewable?
        self.mainloop()

    def display_help(self):
        self.app.main_window().display_help(HELP_TOPIC)

    def cancel(self):
        self.destroy()
        self.app.main_window().status("Add Synth Canceld")

    def accept(self):
        shelper = self.app.ls_parser.synthhelper
        if self.is_efx:
            sy = shelper.add_efx(self.stype, self.id_, outbus=None)
        elif self.is_controller:
            sy = shelper.add_control_synth(self.stype, self.id_)
        else:
            km = self.var_keymode.get()
            vc = int(self.var_voice_count.get())
            sy = shelper.add_synth(self.stype, self.id_, km, vc, outbus=None)
        for p in self._busname_map.keys():
            busname = self._busname_map[p].get()
            offset = int(self._busoffset_map[p].get())
            shelper.assign_buffer_or_bus(p, busname, offset)
        for p,bname in self._buffername_map.items():
            shelper.assign_buffer(p, bname)
        factory.set_pallet(sy.specs["pallet"])
        mw = self.app.main_window()
        group = mw.group_windows[-1]
        swin = TkSynthWindow(group.notebook, sy)
        group.notebook.add(swin, text=self.sid)
        mw[self.sid] = swin
        sy.create_subeditors()
        self.app.main_window().status("Added %s" % self.sid)
        self.destroy()
        

