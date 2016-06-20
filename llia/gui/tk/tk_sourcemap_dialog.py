# llia.gui.tk.tk_sourcemap_dialog
# 2016.06.19

from Tkinter import Toplevel, StringVar, TclError
from llia.generic import is_string
import llia.gui.tk.tk_factory as factory


class TkAddSourceMapDialog(Toplevel):

    HELP_TOPIC = "source-map-dialog"
    default_controller = {}
    default_param = {}

    @staticmethod
    def get_default_controller(synth):
        cmap = TkAddSourceMapDialog.default_controller
        frmt = synth.specs["format"]
        index = cmap.get(frmt, 0)
        return index

    @staticmethod
    def set_default_controller(synth, index):
        frmt = synth.specs["format"]
        TkAddSourceMapDialog.default_controller[frmt] = index
        
    @staticmethod
    def get_default_param(synth):
        cmap = TkAddSourceMapDialog.default_param
        frmt = synth.specs["format"]
        index = cmap.get(frmt, 0)
        return index
        
    @staticmethod
    def set_default_param(synth, index):
        frmt = synth.specs["format"]
        TkAddSourceMapDialog.default_param[frmt] = index
    
    def __init__(self, master, synth, src, app):
        Toplevel.__init__(self, master)
        self.src = src
        self.synth = synth
        self.app = app
        self.var_curve = StringVar()
        self.var_modifier = StringVar()
        self.var_range_low = StringVar()
        self.var_range_high = StringVar()
        self.var_limit_low = StringVar()
        self.var_limit_high = StringVar()
        self.var_curve.set("linear")
        self.var_modifier.set("1.0")
        self.var_range_low.set("0.0")
        self.var_range_high.set("1.0")
        self.var_limit_low.set("0.0")
        self.var_limit_high.set("1.0")
        frame = factory.frame(self, modal=True)
        frame.pack(expand=True, fill="both")
        lab_title = factory.label(frame, "Add MIDI Source Map", modal=True)
        lab_title.grid(row=0, column=0, columnspan=4, padx=4, pady=8)
        if src == "cc":
            lab_src1 = factory.label(frame, "Controller", modal=True)
            self.combo_source = factory.controller_combobox(frame, app)
            lab_src1.grid(row=1, column=0, sticky="w", padx=4)
            self.combo_source.grid(row=1, column=1)
        else:
            lab_src1 = factory.label(frame, "Source", modal=True)
            lab_src2 = factory.label(frame, src, modal=True)
            self.combo_source = factory.combobox(None, [src])  # Hidden
            lab_src1.grid(row=1, column=0, sticky="w", padx=4)
            lab_src2.grid(row=1, column=1, sticky="w")
        lab_params = factory.label(frame, "Params", modal=True)
        bnk = synth.bank()
        params = sorted(bnk.template.keys())
        self.combo_params = factory.combobox(frame, params, 
                                             "Synth parameters")
        frame_curve = factory.label_frame(frame, "Curve", modal=True)
        for i, c in enumerate((("Linear", "linear"), 
                               ("Exponential","exp"), 
                               ("Logistic (S)", "s"), 
                               ("Step","step"))):
            rb = factory.radio(frame_curve, c[0], self.var_curve, c[1], 
                               modal=True)
            rb.config(command=self._auto_modifier_callback)
            rb.grid(row=i, column=0, columnspan=2, sticky="w", padx=4)
        lab_modifier = factory.label(frame_curve, "Modifier", modal=True)
        spin_modifier = factory.float_spinbox(frame_curve, 
                                              self.var_modifier, 
                                              -10, 10, "Curve modifier")
        lab_modifier.grid(row=4, column=0, padx=4, pady=8, sticky="w")
        spin_modifier.grid(row=4, column=1)
        frame_range = factory.label_frame(frame, "Range", modal=True)
        lab_low = factory.label(frame_range, "Low", modal=True)
        lab_high = factory.label(frame_range, "High", modal=True)
        spin_range_low = factory.float_spinbox(frame_range, 
                                               self.var_range_low, -100, 100)
        spin_range_low.config(command=self._auto_limit_callback)
        spin_range_high = factory.float_spinbox(frame_range, 
                                                self.var_range_high, -100, 100)
        spin_range_high.config(command=self._auto_limit_callback)
        lab_low.grid(row=0, column=0, sticky="w", padx=4)
        spin_range_low.grid(row=0, column=1, sticky="ew")
        lab_high.grid(row=1, column=0, sticky="w", padx=4)
        spin_range_high.grid(row=1, column=1, sticky="ew")
        frame_limit = factory.label_frame(frame, "Limit", modal=True)
        lab_low = factory.label(frame_limit, "Low", modal=True)
        lab_high = factory.label(frame_limit, "High", modal=True)
        spin_limit_low = factory.float_spinbox(frame_limit, 
                                               self.var_limit_low, -100, 100)
        spin_limit_high = factory.float_spinbox(frame_limit, 
                                                self.var_limit_high, -100, 100)
        lab_low.grid(row=0, column=0, sticky="w", padx=4)
        spin_limit_low.grid(row=0, column=1, sticky="ew")
        lab_high.grid(row=1, column=0, sticky="w", padx=4)
        spin_limit_high.grid(row=1, column=1, sticky="ew")
        toolbar = factory.frame(frame, modal=True)
        b_help = factory.help_button(toolbar,command=self.help_callback)
        b_restore = factory.clear_button(toolbar, ttip="Restore defaults", 
                                         command=self.restore_callback)
        b_accept = factory.accept_button(toolbar, 
                                         command=self.accept_callback)
        b_cancel = factory.cancel_button(toolbar, 
                                         command=self.cancel_callback)
        b_help.grid(row=0, column=0, sticky="ew")
        b_restore.grid(row=0, column=1, sticky="ew")
        b_accept.grid(row=0, column=2, sticky="ew")
        b_cancel.grid(row=0, column=3, sticky="ew")
        lab_params.grid(row=2, column=0, padx=4, sticky="w")
        self.combo_params.grid(row=2, column=1)
        frame_curve.grid(row=3, column=0, columnspan=2, 
                         padx=4, pady=8, sticky="ew")
        frame_range.grid(row=4, column=0, columnspan=2, 
                         padx=4, pady=4, sticky="ew")
        frame_limit.grid(row=5, column=0, columnspan=2, 
                         padx=4, pady=4, sticky="ew")
        toolbar.grid(row=6, column=0, columnspan=4, 
                     padx=4, pady=8, sticky="ew")
        if src == "cc":
            index = self.get_default_controller(synth)
            if is_string(index):
                index = int(index[1:4])
            self.combo_source.current(index)
        index = self.get_default_param(synth)
        self.combo_params.set(index)
            
    def status(self, msg):
        self.synth.synth_editor.status(msg)

    def warning(self, msg):
        self.synth.synth_editor.warning(msg)
        
    def help_callback(self):
        self.app.main_window().display_help(self.HELP_TOPIC)

    def restore_callback(self):
        self.var_curve.set("Lin")
        self.var_modifier.set("1.0")
        self.var_range_low.set("0.0")
        self.var_range_high.set("1.0")
        self.var_limit_low.set("0.0")
        self.var_limit_high.set("1.0")
        self.combo_source.current(0)
        self.combo_params.current(0)

    def cancel_callback(self):
        msg = "Add Source map canceled"
        self.status(msg)
        self.destroy()

    def accept_callback(self):
        sid = self.synth.sid
        if self.src == "cc":
            src = self.combo_source.get()
            src = int(src[1:4])
            is_cc = True
        else:
            src = self.src
            is_cc = False
        try:
            param = self.combo_params.get()
            curve = self.var_curve.get()
            modifier = float(self.var_modifier.get())
            range_low = float(self.var_range_low.get())
            range_high = float(self.var_range_high.get())
            limit_low = float(self.var_limit_low.get())
            limit_high = float(self.var_limit_high.get())
            shelper = self.app.ls_parser.synthhelper
            shelper.parameter_map(src, param, curve, modifier, 
                                  [range_low, range_high], 
                                  [limit_low, limit_high],
                                  sid)
            if is_cc:
                index = self.combo_source.get()
                self.set_default_controller(self.synth, index)
            index = self.combo_params.get()
            self.set_default_param(self.synth, index)
            msg = "Added source map"
            self.status(msg)
            self.destroy()
            self.synth.synth_editor.sync()
        except ValueError as err:
            self.warning(err.message)
            return

    def _auto_modifier_callback(self):
        curve = self.var_curve.get()
        n = {"linear" : 1,
             "exp" : 1,
             "s" : 1,
             "step" : 4}.get(curve, 1)
        self.var_modifier.set(n)

    def _auto_limit_callback(self, *_):
        try:
            a = float(self.var_range_low.get())
            b = float(self.var_range_high.get())
            a, b = min(a,b), max(a,b)
            self.var_limit_low.set(a)
            self.var_limit_high.set(b)
        except ValueError as err:
            self.warning(err.message)
            

def add_map_dialog(synth, src, app):
    dialog = TkAddSourceMapDialog(None, synth, src, app)



class TkDeleteSourceMapDialog(Toplevel):

    def __init__(self, master, synth, src, app):
        Toplevel.__init__(self, master)
        self.src = src
        self.synth = synth
        self.app = app
        self.var_all = StringVar()
        self.var_all.set(0)
        frame = factory.frame(self, modal=True)
        frame.pack(expand=True, fill="both")
        lab_title = factory.label(frame, "Remove MIDI Source Map", modal=True)
        lab_title.grid(row=0, column=0, columnspan=3, padx=4, pady=8)
        if src == "cc":
            lab_src = factory.label(frame, "Controller", modal=True)
            self.combo_source = factory.controller_combobox(frame, app)
            lab_src.grid(row=1, column=0, padx=4, sticky='w')
            self.combo_source.grid(row=1, column=1, columnspan=2, sticky="ew")
        else:
            lab_src = factory.label(frame, "Source: %s" % src, modal=True)
            self.combo_source = factory.combobox(None, [src])
            lab_src.grid(row=1, column=0, columnspan=3, padx=4, sticky='w')
        lab_param = factory.label(frame, "Param", modal=True)
        self.cb_all = factory.checkbutton(frame, "All", var = self.var_all, modal=True)
        params = sorted(synth.bank().template.keys())
        self.combo_params = factory.combobox(frame, params, 
                                             "Synth Parameters")
        lab_param.grid(row=2, column=0, padx=4, pady=4, sticky='w')
        self.cb_all.grid(row=2, column=1, padx=4)
        self.combo_params.grid(row=2, column=2)

        def disable_param_callback():
            val = int(self.var_all.get())
            if val == 0:
                self.combo_params.config(state="normal")
            else:
                self.combo_params.config(state="disabled")
        
        def accept_callback():
            shelper = self.app.ls_parser.synthhelper
            if self.src == "cc":
                src = self.combo_source.get()[1:4]
            else:
                src = self.src
            src = src.lower()
            if int(self.var_all.get()) == 0:
                param = self.combo_params.get()
            else:
                param = "ALL"
            shelper.remove_parameter_map(src, param, self.synth.sid)
            msg = "Removed MIDI source map"
            self.status(msg)
            self.destroy()
            self.synth.synth_editor.sync()

        def cancel_callback():
            msg = "Delete source map canceld"
            self.status(msg)
            self.destroy()

        toolbar = factory.frame(frame, modal=True)
        b_accept = factory.accept_button(toolbar, command=accept_callback)
        b_cancel = factory.cancel_button(toolbar, command=cancel_callback)
        toolbar.grid(row=3, column=0, columnspan=3, padx=4, pady=8, sticky="ew")
        b_accept.grid(row=0, column=0, sticky="ew")
        b_cancel.grid(row=0, column=1, sticky="ew")
        self.cb_all.config(command=disable_param_callback)
        try:                    # ISSUE BUG 0004
            self.grab_set()
        except TclError as err:
            print("-" * 60)
            print("BUG 0004 trapped. TkDeleteSourceMapDialog.__init__")
            print(err.message)
            print("Unable to open dialog as modal")
            
        self.mainloop()
        
    def status(self, msg):
        self.synth.synth_editor.status(msg)

    def warning(self, msg):
        self.synth.synth_editor.warning(msg)
                                  

def delete_map_dialog(master, synth, src, app):
    dialog = TkDeleteSourceMapDialog(None, synth, src, app)
