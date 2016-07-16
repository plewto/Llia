from __future__ import print_function
import os.path

from Tkinter import Frame
import tkFileDialog

import llia.gui.tk.tk_factory as factory
import llia.gui.tk.tk_layout as layout
# from llia.gui.tk.tk_init_warning import init_warning



class TkBusAndBufferEditor(Frame):


    def __init__(self, master, parent_editor, synth):
        Frame.__init__(self, master)
        self.parent_editor = parent_editor
        self.synth = synth
        self.config(background=factory.bg())
        self.pack(anchor="nw", expand=True, fill="both")
        main = layout.VFrame(self)
        main.pack(anchor="nw", expand=True, fill="both")
        frame_abus = factory.label_frame(main, "Audio Busses")
        frame_cbus = factory.label_frame(main, "Control Busses")
        frame_buf = factory.label_frame(main, "Buffers")
        main.add(frame_abus, padx=8, pady=8)
        main.add(frame_cbus, padx=8, pady=8)
        main.add(frame_buf, padx=8, pady=8)
        self.lab_abus = factory.label(frame_abus, "")
        self.lab_abus.pack()
        self.lab_cbus = factory.label(frame_cbus, "")
        self.lab_cbus.pack()
        self.lab_buffers = factory.label(frame_buf, "")
        self.lab_buffers.pack()

    def sync(self, *_):
        acc = ''
        for param in sorted(self.synth.audio_buses.keys()):
            bname = self.synth.audio_buses[param]
            acc += "param %-12s : bus %s\n" % (param, bname)
        self.lab_abus.config(text = acc)
        acc = ''
        for param in sorted(self.synth.control_buses.keys()):
            bname = self.synth.control_buses[param]
            acc += "param %-12s : bus %s\n" % (param, bname)
        self.lab_cbus.config(text = acc)
        acc = ''
        for param in sorted(self.synth.buffers.keys()):
            bname = self.synth.buffers[param]
            acc += "param %-12s : buffer %s\n" % (param, bname)
        self.lab_buffers.config(text = acc)
