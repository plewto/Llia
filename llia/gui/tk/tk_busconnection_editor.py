# llia.gui.tk.tk_busconnection_editor

from __future__ import print_function
from Tkinter import Frame

import llia.gui.tk.tk_factory as factory
import llia.constants as con


class TkBusConnectionEditor(Frame):

    def __init__(self, master, editor, synth):
        Frame.__init__(self, master)
        self.editor = editor
        self.synthhelper = editor.app.ls_parser.synthhelper
        self.synth = synth
        self.config(background=factory.bg())
        self.pack(anchor="nw", expand=True, fill="both")
        frame_audio_input = factory.label_frame(self, 
                                                "Audio Input Buses")
        frame_audio_output  = factory.label_frame(self, 
                                                  "Audio Output Buses")
        frame_control_input = factory.label_frame(self, 
                                                  "Control Input Buses")
        frame_control_output = factory.label_frame(self, 
                                                   "Control Output Buses")
        frame_audio_input.grid(row=0, column=0, rowspan=4, columnspan=4, 
                               padx=16, pady=16, sticky='nesw')
        frame_audio_output.grid(row=4, column=0, rowspan=4, columnspan=4, 
                                padx=16, pady=16, sticky='nesw')
        frame_control_input.grid(row=0, column=4, rowspan=4, columnspan=4, 
                                 padx=16, pady=16, sticky='nesw')
        frame_control_output.grid(row=4, column=4, rowspan=4, columnspan=4, 
                                  padx=16, pady=16, sticky='nesw')
        specs = synth.specs

        frame_south = factory.frame(self)
        frame_south.grid(row=9, column=0, rowspan=1, columnspan=8, sticky='ew',
                        padx=16, pady=16)
        b_sync = factory.button(frame_south, "Sync", command=self.sync)
        b_sync.grid(row=0, column=0)
        
        # audio inputs
        self._combo_audio_in = {}
        row = 0
        for i in range(con.MAX_BUS_COUNT):
            try:
                b = specs["audio-input-buses"][i]
                param = b[0]
                lab_name = factory.label(frame_audio_input, "%d - %s" % (i+1, param))
                combo = factory.audio_bus_combobox(frame_audio_input, self.editor.app)
                combo.param = param
                combo.bind("<<ComboboxSelected>>", self.audio_in_callback)
                combo.set(b[1])
                lab_name.grid(row=row, column=0, sticky='ew', padx=4, pady=4)
                combo.grid(row=row, column=1, sticky='ew', padx=4, pady=4)
                self._combo_audio_in[param] = combo
            except IndexError:
                lab_dummy = factory.label(frame_audio_input, "%d - n/a" % (i+1,))
                lab_dummy.grid(row=row, column=0)
            row += 1
            
                                         
        # audio output
        self._combo_audio_out = {}
        row = 0
        for i in range(con.MAX_BUS_COUNT):
            try:
                b = specs["audio-output-buses"][i]
                param = b[0]
                lab_name = factory.label(frame_audio_output, "%d - %s" % (i+1, param))
                combo = factory.audio_bus_combobox(frame_audio_output, self.editor.app)
                combo.param = param
                combo.bind("<<ComboboxSelected>>", self.audio_out_callback)
                combo.set(b[1])
                lab_name.grid(row=row, column=0, sticky='ew', padx=4, pady=4)
                combo.grid(row=row, column=1, sticky='ew', padx=4, pady=4)
                self._combo_audio_out[param] = combo
            except IndexError:
                lab_dummy = factory.label(frame_audio_output, "%d - n/a" % (i+1,))
                lab_dummy.grid(row=row, column=0)
            row += 1

        # control inputs
        self._combo_control_in = {}
        row = 0
        for i in range(con.MAX_BUS_COUNT):
            try:
                b = specs["control-input-buses"][i]
                param = b[0]
                lab_name = factory.label(frame_control_input, "%d - %s" % (i+1, param))
                combo = factory.control_bus_combobox(frame_control_input, self.editor.app)
                combo.param = param
                combo.bind("<<ComboboxSelected>>", self.control_in_callback)
                combo.set(b[1])
                lab_name.grid(row=row, column=0, sticky='ew', padx=4, pady=4)
                combo.grid(row=row, column=1, sticky='ew', padx=4, pady=4)
                self._combo_control_in[param] = combo
            except IndexError:
                lab_dummy = factory.label(frame_control_input, "%d - n/a" % (i+1,))
                lab_dummy.grid(row=row, column=0)
            row += 1
            
                                         
        # control output
        self._combo_control_out = {}
        row = 0
        for i in range(con.MAX_BUS_COUNT):
            try:
                b = specs["control-output-buses"][i]
                param = b[0]
                lab_name = factory.label(frame_control_output, "%d - %s" % (i+1, param))
                combo = factory.control_bus_combobox(frame_control_output, self.editor.app)
                combo.param = param
                combo.bind("<<ComboboxSelected>>", self.control_out_callback)
                combo.set(b[1])
                lab_name.grid(row=row, column=0, sticky='ew', padx=4, pady=4)
                combo.grid(row=row, column=1, sticky='ew', padx=4, pady=4)
                self._combo_control_out[param] = combo
            except IndexError:
                lab_dummy = factory.label(frame_control_output, "%d - n/a" % (i+1,))
                lab_dummy.grid(row=row, column=0)
            row += 14
        self.sync()
            
    @staticmethod
    def _callback_helper(event):
        cb = event.widget
        param = cb.param
        bus = cb.get()
        return (param, bus)
        

    def audio_in_callback(self, event):
        param, busname = self._callback_helper(event)
        self.synthhelper.assign_audio_input_bus(param, busname, self.synth.sid)
        
    def audio_out_callback(self, event):
        param, busname = self._callback_helper(event)
        self.synthhelper.assign_audio_output_bus(param, busname, self.synth.sid)
        
    def control_in_callback(self, event):
        param, busname = self._callback_helper(event)
        self.synthhelper.assign_control_input_bus(param, busname, self.synth.sid)

    def control_out_callback(self, event):
        param, busname = self._callback_helper(event)
        self.synthhelper.assign_control_output_bus(param, busname, self.synth.sid)
        
    def sync(self, *_):
        for cb in self._combo_audio_in.values():
            cb.sync()
            busname = self.synth.get_audio_input_bus(cb.param)
            cb.var_selection.set(busname)
        for cb in self._combo_audio_out.values():
            cb.sync()
            busname = self.synth.get_audio_output_bus(cb.param)
            cb.var_selection.set(busname)
        for cb in self._combo_control_in.values():
            cb.sync()
            busname = self.synth.get_control_input_bus(cb.param)
            cb.var_selection.set(busname)
        for cb in self._combo_control_out.values():
            cb.sync()
            busname = self.synth.get_control_output_bus(cb.param)
            cb.var_selection.set(busname)            
                                 
        
        
            
            
