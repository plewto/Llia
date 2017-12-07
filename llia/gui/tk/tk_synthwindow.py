# llia.gui.tk.tk_synthwindow

from __future__ import print_function
from Tkinter import Frame, StringVar

from llia.generic import is_list
import llia.gui.tk.tk_factory as factory
import llia.gui.pallet
from llia.gui.tk.tk_bankeditor import TkBankEditor
from llia.gui.tk.tk_busconnection_editor import TkBusConnectionEditor
from llia.gui.tk.tk_sourcemap_dialog import add_map_dialog, delete_map_dialog
from ttk import Progressbar

PROGRESSBAR_COLUMN = 3

class TkSynthWindow(Frame):

    def __init__(self, master, sproxy):
        Frame.__init__(self, master)
        self.config(background=factory.bg())
        self.synth = sproxy
        self.synth.synth_editor = self
        self.app = sproxy.app
        self.sid = sproxy.sid
        self.group_index = -1
        factory.set_pallet(sproxy.specs["pallet"])
        main = factory.paned_window(self)
        main.pack(expand=True, fill="both")
        self.bank_editor = TkBankEditor(main, self, sproxy)
        self.bus_and_buffer_editor = None
        east = factory.frame(main)
        self.notebook = factory.notebook(east)
        self.notebook.pack(anchor="nw", expand=True, fill="both")
        south = factory.frame(east)
        south.pack(after=self.notebook, anchor="w", expand=True, fill="x")
        # b_panic = factory.panic_button(south, command=self.panic)
        # b_clear_status = factory.clear_button(south, command=self.clear_status)
        # self._lab_status = factory.label(south, "<status>")
        # b_panic.grid(row=0, column=0, sticky='w')
        # b_clear_status.grid(row=0, column=1, sticky='w')
        # self._lab_status.grid(row=0, column=2, sticky='w', padx=8)

        self._lab_status = factory.label(south, "<status>")
        b_panic = factory.panic_button(south, command=self.panic)
        b_lower = factory.button(south, "-", command=self.lower_window)
        b_lift = factory.button(south, "+", command=self.lift_window)
        self._lab_status.grid(row=0, column=2, sticky='ew', padx=8)
        b_panic.grid(row=0, column=0)
        self._lab_status.grid(row=0, column=4, sticky='w')
        self._progressbar = Progressbar(south,mode="indeterminate")
        self._progressbar.grid(row=0,column=PROGRESSBAR_COLUMN, sticky='w', padx=8)
        
        
        south.config(background=factory.bg())
        main.add(self.bank_editor)
        main.add(east)
        self.list_channel = None
        self.list_keytab = None
        self.var_transpose = StringVar()
        self.var_keyrange_low = StringVar()
        self.var_keyrange_high = StringVar()
        self.var_bendrange = StringVar()
        self._init_info_tab(self.notebook)
        self._init_busconnection_tab(self.notebook)
        self._init_performance_tab(self.notebook)
        self._init_map1_tab(self.notebook) # MIDI controllers and pitchwheel
        self._init_map2_tab(self.notebook) # velocity, aftertouch, keynumber
        self._child_editors = {}
        self.update_progressbar(100, 0)

    def panic(self):
        self.synth.osc_transmitter.x_all_notes_off()
        self.status("All notes off")
        
    def clear_status(self):
        self._lab_status.config(text="")
        
    def add_child_editor(self, child_name, child):
        # Adds child editor to list of editors without adding a notebook tab.
        self._child_editors[child_name] = child

    def _create_basic_tab(self,text):
        f = factory.frame(self.notebook)
        self.notebook.add(f, text=text)
        return f

    # icon_filename = "resources/%s/logo_32.png" % sy.specs["format"]
    # icon = factory.image(icon_filename)
    # group.notebook.add(swin, text=sy.sid, image=icon, compound="top")
    
    def _create_compund_tab(self,text,image_filename):
        try:
            icon = factory.image(image_filename)
            f = factory.frame(self.notebook)
            self.notebook.add(f,text=text,image=icon,compound="top")
            return f
        except IOError:
            msg = "IOError while loaidng image file '%s'" % image_filename
            print(msg)
            return self._create_basic_tab(text)
    
    def create_tab(self, tab_text, image_filename=""):
        if not image_filename:
            rs = self._create_basic_tab(tab_text)
        else:
            rs = self._create_compund_tab(tab_text,image_filename)
        return rs
       
    def remove_synth(self, *_):
        sid = self.synth.sid
        parser = self.app.ls_parser
        sh = parser.synthhelper
        sh.destroy_editor(sid)
        sh.remove_synth(sid, force=True)
        self.status("Removed synth: %s" % sid)

    def _init_info_tab(self, master):
        img = factory.image("resources/Tabs/info.png")
        frame = factory.frame(master)
        inner_frame = factory.frame(frame)
        master.add(frame, text="Info", image=img,compound="top")
        text_widget = factory.text_widget(inner_frame)
        text_widget.config(width=120, height=40)
        vsb = factory.scrollbar(inner_frame, orientation='vertical')
        vsb.config(command=text_widget.yview)
        text_widget.config(yscrollcommand=vsb.set, wrap='word',)
        text_widget.grid(row=0, column=0,sticky="ewns")
        vsb.grid(row=0, column=1, sticky='ns')
        inner_frame.grid(row=0, column=0, rowspan=8, columnspan=8, sticky="ewns")
        self._info_text_widget = text_widget

    def lift_window(self):
        mw = self.app.main_window()
        grp = mw.group_windows[self.group_index]
        grp.lift()
        self.status("Lift window")

    def lower_window(self):
        mw = self.app.main_window()
        grp = mw.group_windows[self.group_index]
        grp.lower()
        self.status("Lowewr window")
        
    def sync_program_tab(self):
        bnk = self.synth.bank()
        prog = bnk[None]
        slot = bnk.current_slot
        pp = self.synth.specs["pretty-printer"]
        if pp:
            txt = pp(prog, slot)
        else:
            txt = ""
        self._info_text_widget.delete(1.0, "end")
        self._info_text_widget.insert("end", txt)
    
    def _init_busconnection_tab(self, master):
        img = factory.image("resources/Tabs/bus.png")
        bct = TkBusConnectionEditor(master, self, self.synth)
        master.add(bct, text = "Buses", image=img,compound="top")
        self.bus_connection_editor = bct
        
    def _init_performance_tab(self, master):
        img = factory.image("resources/Tabs/midi.png")
        frame = factory.frame(master)
        master.add(frame, text = "Performance", image=img, compound="top")
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
        spin_transpose = factory.int_spinbox(frame, 
                                             self.var_transpose, -36, 36)
        spin_keylow = factory.int_spinbox(frame, 
                                          self.var_keyrange_low, 0, 127)
        spin_keyhigh = factory.int_spinbox(frame, 
                                           self.var_keyrange_high, 0, 127)
        spin_bendrange = factory.int_spinbox(frame, 
                                             self.var_bendrange, 0, 2400)
        factory.padding_label(frame).grid(row=0)
        frame_channel.grid(row=1, column=0, rowspan=4, columnspan=2)
        self.list_channel.pack(side="left", expand=True, fill="both")
        sb_channel.pack(after=self.list_channel, side="right", 
                        expand=True, fill="y")
        frame_keytab.grid(row=1, column=2, rowspan=4, columnspan=2)
        self.list_keytab.pack(side="left", expand=True, fill="both")
        sb_keytab.pack(after=self.list_keytab, side="right", 
                       expand=True, fill="y")
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

    def sync_performance_tab(self):
        self.list_channel.delete(0, "end")
        for c in self.app.config().channel_assignments.formatted_list():
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

    # map1_tab -> MIDI controller, pitch wheel
    def _init_map1_tab(self, master):
        img = factory.image("resources/Tabs/map.png")
        HELP_TOPIC = "parameter-maps"
        frame = factory.frame(master)
        master.add(frame, text="Map1", image=img, compound="top")
        north = factory.label_frame(frame, "MIDI Controller Maps")
        south = factory.label_frame(frame, "Pitch Wheel Maps")
        north.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        south.grid(row=1, column=0, sticky="ew", padx=8, pady=8)

        def help_callback():
            self.app.main_window().display_help(HELP_TOPIC)
       
        list_cc_maps = factory.listbox(north, 
                                       ttip="Active MIDI controller maps")
        list_cc_maps.config(width=80, height=16)
        self.list_cc_maps = list_cc_maps
        sb = factory.scrollbar(north, orientation="vertical")
        sb.config(command=list_cc_maps.yview)
        list_cc_maps.config(yscrollcommand=sb.set)
        b_add_cc = factory.add_button(north, ttip="Add new controller map")
        b_delete_cc = factory.delete_button(north, 
                                            ttip="Delete controller map")
        list_cc_maps.grid(row=0, column=0, rowspan=4, 
                          columnspan=8, sticky="ew")
        sb.grid(row=0, column=8, rowspan=4, sticky="ns")
        b_add_cc.grid(row=4, column=0, sticky="ew")
        b_delete_cc.grid(row=4, column=1, sticky="ew")

        list_pwheel_maps = factory.listbox(south, 
                                           ttip="Active pitch wheel maps")
        list_pwheel_maps.config(width=80, height=8)
        self.list_pwheel_maps = list_pwheel_maps
        sb = factory.scrollbar(south, orientation="vertical")

        sb.config(command=list_pwheel_maps.yview)
        list_pwheel_maps.config(yscrollcommand=sb.set)
        b_add_pw = factory.add_button(south, ttip="Add pitchwheel map")
        b_delete_pw = factory.delete_button(south, 
                                            ttip="Delete pitchwheel map")
        b_help = factory.help_button(south, command=help_callback)
        list_pwheel_maps.grid(row=0, column=0, rowspan=4,
                              columnspan=8, sticky="ew")
        sb.grid(row=0, column=8, rowspan=4, sticky="ns")
        b_add_pw.grid(row=4, column=0, sticky="ew")
        b_delete_pw.grid(row=4, column=1, sticky="ew")
        b_help.grid(row=4, column=7, sticky="ew")

        def add_cc_callback():
            dialog = add_map_dialog(self.synth, "cc", self.app)

        def delete_cc_callback():
            dialog = delete_map_dialog(self, self.synth, "cc", self.app)

        def add_pw_callback():
            dialog = add_map_dialog(self.synth, "PitchWheel", self.app)

        def delete_pw_callback():
            dialog = delete_map_dialog(self, self.synth, "PitchWheel", self.app)

        b_add_cc.config(command=add_cc_callback)
        b_delete_cc.config(command=delete_cc_callback)
        b_add_pw.config(command=add_pw_callback)
        b_delete_pw.config(command=delete_pw_callback)
        
    def sync_map1_tab(self):
        perf = self.synth.bank()[None].performance
        cmaps = perf.controller_maps
        pwmaps = perf.pitchwheel_maps
        self.list_cc_maps.delete(0, "end")
        for ctrl, mapper in cmaps.items():
            s = str(mapper)
            for q in s.split('\n'):
                self.list_cc_maps.insert("end", q)
        self.list_pwheel_maps.delete(0, "end")
        for q in str(pwmaps).split('\n'):
            self.list_pwheel_maps.insert("end", q)

    def _init_map2_tab(self, master):
        img = factory.image("resources/Tabs/map.png")
        HELP_TOPIC = "parameter-maps"
        HEIGHT = 8
        frame = factory.frame(master)
        master.add(frame, text="Map2",image=img,compound="top")
        north = factory.label_frame(frame, "Velocity Maps")
        center = factory.label_frame(frame, "Aftertouch Maps")
        south = factory.label_frame(frame, "Keynumber Maps")
        north.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        center.grid(row=1, column=0, sticky="ew", padx=8)
        south.grid(row=2, column=0, sticky="ew", padx=8, pady=8)

        def help_callback():
            self.app.main_window().display_help(HELP_TOPIC)

        list_vel_maps = factory.listbox(north, ttip="Active velocity maps")
        list_vel_maps.config(width=80, height=HEIGHT)
        self.list_vel_maps = list_vel_maps
        sb = factory.scrollbar(north, orientation="vertical")
        sb.config(command=list_vel_maps.yview)
        list_vel_maps.config(yscrollcommand=sb.set)
        b_add_vel = factory.add_button(north, ttip="Add velocity map")
        b_delete_vel = factory.delete_button(north, 
                                             ttip="Delete velocity map")
        list_vel_maps.grid(row=0, column=0, columnspan=8, sticky="ew")
        sb.grid(row=0, column=8, sticky="ns")
        b_add_vel.grid(row=1, column=0, sticky="ew")
        b_delete_vel.grid(row=1, column=1, sticky="ew")

        list_atouch_maps = factory.listbox(center, 
                                           ttip="Active after touch maps")
        list_atouch_maps.config(width=80, height=HEIGHT)
        self.list_atouch_maps = list_atouch_maps
        sb = factory.scrollbar(center, orientation="vertical")
        sb.config(command=list_atouch_maps.yview)
        list_atouch_maps.config(yscrollcommand=sb.set)
        b_add_atouch = factory.add_button(center, ttip="Add after touch map")
        b_delete_atouch = factory.delete_button(center, 
                                                ttip="Delete after touch map")
        list_atouch_maps.grid(row=0, column=0, columnspan=8, sticky="ew")
        sb.grid(row=0, column=8, sticky="ns")
        b_add_atouch.grid(row=1, column=0, sticky="ew")
        b_delete_atouch.grid(row=1, column=1, sticky="ew")

        list_keynum_maps = factory.listbox(south, 
                                           ttip="Active key number maps")
        list_keynum_maps.config(width=80, height=HEIGHT)
        self.list_keynum_maps = list_keynum_maps
        sb = factory.scrollbar(south, orientation="vertical")
        sb.config(command=list_keynum_maps.yview)
        list_keynum_maps.config(yscrollcommand=sb.set)
        b_add_keynum = factory.add_button(south, ttip="Add key number map")
        b_delete_keynum = factory.delete_button(south, 
                                                ttip="Delete key number map")
	b_help = factory.help_button(south, command=help_callback)
        list_keynum_maps.grid(row=0, column=0, columnspan=8, sticky="ew")
        sb.grid(row=0, column=8, sticky="ns")
        b_add_keynum.grid(row=1, column=0, sticky="ew")
        b_delete_keynum.grid(row=1, column=1, sticky="ew")
        b_help.grid(row=1, column=7, sticky="ew")

        def add_map_callback(event):
            widget = event.widget
            if widget is b_add_vel:
                dialog = add_map_dialog(self.synth, "velocity", self.app)
            elif widget is b_add_atouch:
                dialog = add_map_dialog(self.synth, "aftertouch", self.app)
            elif widget is b_add_keynum:
                dialog = add_map_dialog(self.synth, "keynumber", self.app)
            else:
                msg = "Invald widget - Should never see this"
                raise ValueError(msg)

        def delete_map_callback(event):
            widget = event.widget
            if widget is b_delete_vel:
                dialog = delete_map_dialog(self, self.synth, "velocity", self.app)
            elif widget is b_delete_atouch:
                dialog = delete_map_dialog(self, self.synth, "aftertouch", self.app)
            elif widget is b_delete_keynum:
                dialog = delete_map_dialog(self, self.synth, "keynumber", self.app)
            else:
                msg = "Invald widget - Should never see this"
                raise ValueError(msg)

        b_add_vel.bind("<Button-1>", add_map_callback)
        b_add_atouch.bind("<Button-1>", add_map_callback)
        b_add_keynum.bind("<Button-1>", add_map_callback)
        b_delete_vel.bind("<Button-1>", delete_map_callback)
        b_delete_atouch.bind("<Button-1>", delete_map_callback)
        b_delete_keynum.bind("<Button-1>", delete_map_callback)
        
    def sync_map2_tab(self):
        perf = self.synth.bank()[None].performance
        vmaps = perf.velocity_maps
        atmaps = perf.aftertouch_maps
        knmaps = perf.keynumber_maps
        self.list_vel_maps.delete(0, 'end')
        self.list_atouch_maps.delete(0, 'end')
        self.list_keynum_maps.delete(0, 'end')
        for q in str(vmaps).split('\n'):
            self.list_vel_maps.insert('end', q)
        for q in str(atmaps).split('\n'):
            self.list_atouch_maps.insert('end', q)
        for q in str(knmaps).split('\n'):
            self.list_keynum_maps.insert('end', q)            
        
    def status(self, msg):
        self._lab_status.config(text = msg)

    def warning(self, msg):
        msg = "WARNING: %s" % msg
        self._lab_status.config(text = msg)

    def set_value(self, param, value):
        for ed in self._child_editors.items():
            ed.set_value(param, value)

    def set_aspect(self, param, value):
        for ed in self._child_editors.values():
            ed.set_value(param, value)
    
    def sync(self, *ignore):
        self.sync_program_tab()
        self.bus_connection_editor.sync()
        self.sync_performance_tab()
        self.sync_map1_tab()
        self.sync_map2_tab()
        if "bank" not in ignore:
            self.bank_editor.sync_no_propegate()
        for key, ed in self._child_editors.items():
            if key not in ignore:
                ed.sync(*ignore)
       
    def annotation_keys(self):
        acc = []
        for ed in self._child_editors.values():
            acc += ed.annotation_keys()
        return acc

    def set_annotation(self, key, text):
        for ed in self._child_editors.values():
            ed.annotation(key, text)

    def get_annotation(self, key):
        rs = None
        for ed in self._child_editors.values():
            rs = ed.get_annotation(key)
            if rs != None:
                return rs
        return None

    def update_progressbar(self, count, value):
        self._progressbar.config(mode="determinate", maximum=count)
        self._progressbar.step()
        self.update_idletasks()
    
    def busy(self, flag, message=""):
        if message:
            self.status(message)
        self._progressbar.config(mode="indeterminate")
        if flag:
            self._progressbar.grid(row=0,column=PROGRESSBAR_COLUMN, sticky='w', padx=8)
            self._progressbar.start()
        else:
            self._progressbar.stop()
        self.update_idletasks()

    # def tabula_rasa(self):
    #     for tid in self.notebook.tabs():
    #         self.notebook.forget(tid)
            
