# llia.gui.tk.tk_appwindow
# 2016.05.20
#
# Tk implementation of AbstractApplicationWindow

from __future__ import print_function
from Tkinter import (Frame, Label, Menu, Tk, BOTH, Toplevel)
from ttk import Progressbar
import ttk
import tkMessageBox,tkFileDialog

from PIL import Image, ImageTk
from llia.llerrors import LliaPingError
from llia.gui.appwindow import AbstractApplicationWindow
from llia.gui.tk.tk_splash import TkSplashWindow
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.tk_layout as layout
from  llia.proxy import LliaProxy
import llia.constants as con
from llia.gui.tk.tk_addsynth import TkAddSynthDialog
from llia.synth_proxy import SynthSpecs
from llia.gui.tk.group_window import GroupWindow
from llia.gui.tk.graph.lliagraph import LliaGraph
specs = SynthSpecs.global_synth_type_registry

PROGRESSBAR_COLUMN = 3


class TkApplicationWindow(AbstractApplicationWindow):

    def __init__(self, app):
        self.root = Tk()
        self.root.title("Llia")
        self.root.config(background=factory.bg())
        super(TkApplicationWindow, self).__init__(app, self.root)
        self.root.withdraw()
        if app.config()["enable-splash"]:
            splash = TkSplashWindow(self.root, app)
        self.root.deiconify()
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)
        self.llia_graph = None
        self._main = layout.BorderFrame(self.root)
        self._main.config(background=factory.bg())
        self._main.pack(anchor="nw", expand=True, fill=BOTH)
        self._progressbar = None
        self._init_status_panel()
        self._init_menu()
        self._init_center_frame(self._main.center)
        self.root.minsize(width=665, height=375)
        self.group_windows = []
        self.add_synth_group()
        self._scene_filename = ""
        
    def _init_status_panel(self):
        south = self._main.south
        south.configure(padx=4, pady=4)
        self._lab_status = factory.label(south, "", modal=False)
        b_panic = factory.panic_button(south)
        b_down = factory.button(south, "-")
        b_up = factory.button(south, "+")
        b_panic.grid(row=0, column=0)
        self._progressbar = Progressbar(south,mode="indeterminate")
        self._progressbar.grid(row=0,column=PROGRESSBAR_COLUMN, sticky='w', padx=8)
        self._lab_status.grid(row=0,column=4, sticky='w')
        south.config(background=factory.bg())
        b_down.configure(command=lambda: self.root.lower())
        b_up.configure(command=lambda: self.root.lift())
        self.update_progressbar(100, 0)
        
    def _tab_change_callback(self, event):
        self.llia_graph.sync()
    
    def _init_center_frame(self, master):
        nb = ttk.Notebook(master)
        nb.pack(expand=True, fill="both")
        frame_synths = layout.FlowGrid(nb, 6)
        frame_efx = layout.FlowGrid(nb, 6)
        frame_controllers = layout.FlowGrid(nb, 6)
        self.llia_graph = LliaGraph(nb, self.app)
        nb.add(frame_synths, text = "Synths")
        nb.add(frame_efx, text = "Effects")
        nb.add(frame_controllers, text = "Controllers")
        nb.add(self.llia_graph, text="Graph")
        nb.bind("<Button-1>", self._tab_change_callback)

        def display_info_callback(event):
            sp = event.widget.synth_spec
            msg = "%s:    %s" % (sp["format"],sp["description"])
            self.status(msg)

        def clear_info_callback(*_):
            self.status("")
        
        for st in con.SYNTH_TYPES:
            sp = specs[st]
            ttp = "Add %s Synthesizer (%s)" % (st, sp["description"])
            b = factory.logo_button(frame_synths, st, ttip=ttp)
            b.synth_spec = sp
            b.bind("<Button-1>", self._show_add_synth_dialog)
            b.bind("<Enter>", display_info_callback)
            b.bind("<Leave>", clear_info_callback)
            frame_synths.add(b)
        for st in con.EFFECT_TYPES:
            sp = specs[st]
            ttp = "Add %s Effect (%s)" % (st, sp["description"])
            b = factory.logo_button(frame_efx, st, ttip=ttp)
            b.synth_spec = sp
            b.bind("<Button-1>", self._show_add_efx_dialog)
            b.bind("<Enter>", display_info_callback)
            b.bind("<Leave>", clear_info_callback)
            frame_efx.add(b)
        for st in con.CONTROLLER_SYNTH_TYPES:
            sp = specs[st]
            ttp = "Add %s Effect (%s)" % (st, sp["description"])
            b = factory.logo_button(frame_controllers, st, ttip=ttp)
            b.synth_spec = sp
            b.bind("<Button-1>", self._show_add_controller_dialog)
            b.bind("<Enter>", display_info_callback)
            b.bind("<Leave>", clear_info_callback)
            frame_controllers.add(b)
    
    @staticmethod
    def menu(master):
        m = Menu(master, tearoff=0)
        m.config(background=factory.bg(), foreground=factory.fg())
        return m
    
    def _init_menu(self):
        main_menu = self.menu(self.root)
        self.root.config(menu=main_menu)
        file_menu = self.menu(main_menu)
        osc_menu = self.menu(main_menu)
        midi_menu = self.menu(main_menu)
        bus_menu = self.menu(main_menu)
        #buffer_menu = self.menu(main_menu)
        tune_menu = self.menu(main_menu)
        help_menu = self.menu(main_menu)
        main_menu.add_cascade(label="File", menu=file_menu)
        main_menu.add_cascade(label="OSC", menu=osc_menu)
        main_menu.add_cascade(label="MIDI", menu=midi_menu)
        #main_menu.add_cascade(label="Buses", menu=bus_menu)
        #main_menu.add_cascade(label="Buffers", menu=buffer_menu)
        #main_menu.add_cascade(label="Tune", menu=tune_menu)
        #main_menu.add_cascade(label="Help", menu=help_menu)
        self._init_file_menu(file_menu)
        self._init_osc_menu(osc_menu)
        self._init_midi_menu(midi_menu)
        self._init_bus_menu(bus_menu)
        #self._init_buffer_menu(buffer_menu)
        self._init_tune_menu(tune_menu)
        self._init_help_menu(help_menu)

    def _init_file_menu(self, fmenu):
        fmenu.add_command(label="Save Scene", command = self.save_scene)
        fmenu.add_command(label="Load Scene", command = self.load_scene)
        fmenu.add_separator()
        fmenu.add_command(label="Lliascript (Legacy)", command = self.show_history_editor)
        fmenu.add_separator()
        fmenu.add_command(label="New Synth Group", command = self._add_synth_group)
        fmenu.add_separator()
        fmenu.add_command(label="Restart", command = self._interactive_tabula_rasa)
        fmenu.add_command(label="Quit", command = self.exit_app)

    def _init_osc_menu(self, iomenu):
        iomenu.add_command(label="Ping", command = self.ping_global)
        iomenu.add_command(label="Dump", command = self.app.proxy.dump)
        iomenu.add_command(label="Toggle OSC Trace", command = self.toggle_osc_trace)

    def _init_midi_menu(self, mmenu):
        map_menu = self.menu(mmenu)
        mmenu.add_command(label = "Channel Names", command = self.show_channel_name_dialog)
        mmenu.add_command(label = "Controller Names", command = self.show_controller_name_dialog)
        mmenu.add_cascade(label = "MIDI Maps", menu = map_menu)
        mmenu.add_command(label = "Toggle MIDI Input Trace", command = self.toggle_midi_input_trace)
        mmenu.add_command(label = "Toggle MIDI Output Trace", command = self.toggle_midi_output_trace)
        mmenu.add_command(label = "Toggle Program Pretty Printer", command = self.toggle_program_pretty_printer)
        
    def _init_bus_menu(self, bmenu):
        bmenu.add_command(label="Audio", command=self.show_audiobus_dialog)
        bmenu.add_command(label="Control", command=self.show_controlbus_dialog)
        
    # def _init_buffer_menu(self, bmenu):
    #     bmenu.add_command(label="View Buffers", command=self.show_bufferlist_dialog)

    def _init_tune_menu(self, tmenu):
        tmenu.add_command(label = "FIX ME: Nothing to see here")

    def _init_help_menu(self, hmenu):
        pass
        
    def exit_gui(self):
        try:
            self.root.destroy()
        except:
            pass

    def confirm_exit(self):
        return tkMessageBox.askyesno("Exit Llia", "Exit Llia?")
        
    def exit_app(self):
        self.app.exit_()

    def as_widget(self):
        return self.root
        
    def status(self, msg):
        self._lab_status.config(text=str(msg))

    def warning(self, msg):
        msg = "WARNING: %s" % msg
        self._lab_status.config(text=msg)
        
    def clear_status(self):
        self.status("")
                                              
    def start_gui_loop(self):
        self.root.mainloop()

    def show_about_dialog(self):
        from llia.gui.tk.tk_about_dialog import TkAboutDialog
        dialog = TkAboutDialog(self.root, self.app)
        self.root.wait_window(dialog)

    def display_help(self, topic=None):
        pass
        
    def show_history_editor(self):
        from llia.gui.tk.tk_history import TkHistoryEditor
        dialog = TkHistoryEditor(self.root, self.app)
        self.root.wait_window(dialog)

    def ping_global(self):
        try:
            rs = self.app.proxy.ping()
            if rs:
                self.status("Ping OK")
            else:
                self.warning("Ping Error")
        except LliaPingError as err:
            self.warning(err.message)

    def toggle_osc_trace(self):
        LliaProxy.trace = not LliaProxy.trace
        if LliaProxy.trace:
            self.status("OSC transmission trace enabled")
        else:
            self.status("OSC transmission trace disabled")

    def show_channel_name_dialog(self):
        from llia.gui.tk.tk_channel_name_editor import TkChannelNameEditor
        dialog = TkChannelNameEditor(self.root, self.app)
        self.root.wait_window(dialog)
  
    def show_controller_name_dialog(self):
        from llia.gui.tk.tk_controller_name_editor import TkControllerNameEditor
        dialog = TkControllerNameEditor(self.root, self.app)
        self.root.wait_window(dialog)
    
    def toggle_midi_input_trace(self):
        flag = not self.app.midi_in_trace
        self.app.midi_in_trace = flag
        self.app.midi_receiver.enable_trace(flag)
        if flag:
            self.status("MIDI input trace enabled")
        else:
            self.status("MIDI output trace disabled")

    def toggle_midi_output_trace(self):
        self.status("MIDI output not available") # FIX ME

    def toggle_program_pretty_printer(self):
        self.app.pp_enabled = not self.app.pp_enabled
        if self.app.pp_enabled:
            self.status("Pretty printer enabled")
        else:
            self.status("Pretty printer disabled")
        
    def show_audiobus_dialog(self):
        from llia.gui.tk.tk_audiobus_editor import TkAudiobusEditor
        dialog = TkAudiobusEditor(self.root, self.app)
        self.root.wait_window(dialog)

    def show_controlbus_dialog(self):
        from llia.gui.tk.tk_controlbus_editor import TkControlbusEditor
        dialog = TkControlbusEditor(self.root, self.app)
        self.root.wait_window(dialog)

    # def show_bufferlist_dialog(self):
    #     from llia.gui.tk.tk_buffer_info import TkBufferListDialog
    #     dialog = TkBufferListDialog(self.root, self.app)
    #     self.root.wait_window(dialog)

    def _show_add_synth_dialog(self, event):
        w = event.widget
        st = w.config()["text"][-1]
        dialog = TkAddSynthDialog(self.root, self.app, st, False)
        self.root.wait_window(dialog)
        
    def _show_add_efx_dialog(self, event):
        w = event.widget
        st = w.config()["text"][-1]
        dialog = TkAddSynthDialog(self.root, self.app, st, is_efx=True, is_controller=False)
        self.root.wait_window(dialog)

    def _show_add_controller_dialog(self, event):
        w = event.widget
        st = w.config()["text"][-1]
        dialog = TkAddSynthDialog(self.root, self.app, st, is_efx=False, is_controller=True)
        self.root.wait_window(dialog)
        
    def _add_synth_group(self):
        sh = self.app.ls_parser.synthhelper
        sh.new_group()
        
    def add_synth_group(self, name=None):
        gw = GroupWindow(self.app, self.root, name)
        # gw.transient(self.root)  # If executed keeps main app window behind all other windows.
        self.group_windows.append(gw)
        self.status("Added new Synth Group Window")
        return gw

    def display_synth_editor(self, sid):
        try:
            swin = self[sid]
            grpid = swin.group_index
            grp = self.group_windows[grpid]
            #grp.deiconify()
            grp.show_synth_editor(sid)
        except (KeyError, IndexError):
            msg = "Can not find editor for %s" % sid
            self.warning(msg)

    def update_progressbar(self, count, value):
        self._progressbar.config(mode="determinate", maximum=count)
        self._progressbar.step()
        self.root.update_idletasks()
            
    def busy(self, flag, message=""):
        if message:
            self.status(message)
        self._progressbar.config(mode="indeterminate")
        if flag:
            self._progressbar.grid(row=0, column=PROGRESSBAR_COLUMN, sticky='w', padx=8)
            self._progressbar.start()
        else:
            self._progressbar.stop()
            # self._progressbar.grid_remove()
        self.root.update_idletasks()

    def save_scene(self, *_):
        options = {'defaultextension' : '.llia',
                   'filetypes' : [('Llia Scenes', '*.llia'),
                                  ('all files', '*')],
                   'initialfile' : self._scene_filename,
                   'parent' : self.root,
                   'title' : "Save Llia Scene"}
        filename = tkFileDialog.asksaveasfilename(**options)
        if filename:
            try:
                self.app.ls_parser.save_scene(filename)
                self._scene_filename = filename
                self.status("Scene saved as '%s'" % filename)
            except Exception as ex:
                self.warning(ex.message)
        else:
            self.status("Scene save canceld")    

    def load_scene(self, *_):
        options = {'defaultextension' : '.llia',
                   'filetypes' : [('Llia Scenes', '*.llia'),
                                  ('all files', '*')],
                   'initialfile' : self._scene_filename,
                   'parent' : self.root,
                   'title' : "Load Llia Scene"}
        filename = tkFileDialog.askopenfilename(**options)
        if filename:
            try:
                self.app.ls_parser.load_scene(filename)
                self.status("Scene '%s' loaded" % filename)
                self._scene_filename = filename
            except Exception as ex:
                self.warning(ex.message)
        else:
            self.status("Load scene canceld")
            
    def tabula_rasa(self):
        for grp in self.group_windows:
            grp.tabula_rasa()
        self.group_windows = []

    def _interactive_tabula_rasa(self, *_):
        # ISSUE: Check config and ask user confirmation before existing
        self.app.ls_parser.tabula_rasa()
