# llia.gui.tk.layout
# 2016.05.21
#
# Emulation of useful layouts from other GUI systems.
#

from Tkinter import *
import ttk

from llia.generic import is_string
import llia.gui.tk.tk_factory as factory


#  ---------------------------------------------------------------------- 
#                                 FormLayout
#
# Stolen from QT QFormLayout.
# The form layout consist of 2 columns
#
#     label-0   widget-0
#     label-1   widget-1
#     label-2   widget-2
#       ...       ...
#     label-n   widget-n


class FormLayout(Frame):

    def __init__(self, master, title=None):
        Frame.__init__(self, master)
        self._row_count = 0
        self.rows = []
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        if title:
            self.lab_title = factory.center_label(self, str(title))
            self.lab_title.grid(row=0, column=0, columnspan=2, pady=4)
            self._row_count += 1
        else:
            self.lab_title = None

    def add(self, label, payload):
        row = self._row_count
        if is_string(label):
            txt = label
            label = factory.label(self, txt)
        label.grid(row=row, column=0, sticky="w",padx=4)
        payload.grid(row=row, column=1, sticky="ew")
        rs = (label, payload)
        self.rows.append(rs)
        self._row_count += 1
        return rs

    def separator(self):
        return self.add("", factory.label(self, ""))

#  ---------------------------------------------------------------------- 
#                                   VFrame
# Frame with vertical layout
#

class VFrame(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self._row_count = 0
        self.rows = []
        self.grid_columnconfigure(0, weight=1)

    def add(self, payload, pady=0, span=1, weight=0, sticky="ew"):
        if is_string(payload):
            payload = factory.center_label(self, payload)
        payload.grid(row=self._row_count, column=0, pady=pady, sticky=sticky)
        self.grid_rowconfigure(self._row_count, weight=weight)
        self.rows.append(payload)
        self._row_count += span

    def spearator(self):
        self.add("")


#  ---------------------------------------------------------------------- 
#                                   HFrame
# Frame with horizontal layout
#

class HFrame(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self._column_count = 0
        self.columns = []
        self.grid_rowconfigure(0, weight=1)

    def add(self, payload, span=1, padx=0, sticky="ew"):
        if is_string(payload):
            payload = factory.center_label(self, payload)
        payload.grid(row=0, column=self._column_count, columnspan=span, padx=padx, sticky=sticky)
        self.columns.append(payload)
        self.grid_columnconfigure(self._column_count, weight=span)
        self._column_count += span

    def separator(self):
        self.add("")


#  ---------------------------------------------------------------------- 
#                                 BorderFrame
#
# Borrowd from Swing BorderLayout
# BorderFrame has 5 regions: North, South, East, West and Center.
#

class BorderFrame(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        north = Frame(self)
        south = Frame(self)
        east = Frame(self)
        west = Frame(self)
        center = Frame(self)
        span=1
        north.grid(row=0, column=0, rowspan=1, columnspan=span+2, sticky="ew")
        south.grid(row=span+1, column=0, rowspan=1, columnspan=span+2, sticky="ew")
        west.grid(row=1, column=0, rowspan=span, columnspan=1)
        east.grid(row=1, column=span+1, rowspan=span, columnspan=1)
        center.grid(row=1, column=1, rowspan=span, columnspan=span, sticky="nesw")
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(span+1, weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1, uniform=True)
        self.grid_rowconfigure(span+1, weight=0)
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        self.center = center

#  ---------------------------------------------------------------------- 
#                                    Test
#
# ISSUE: Test functions may not work ~ they were developed using a previous
#        version of factory.
#
def form_test():
    root = Tk()
    a = FormLayout(root, "Why ask why?")
    a.pack(anchor="nw", expand=True, fill="both")
    a.add("Button", factory.button(a, "A"))
    a.add("Spinner box dog", factory.spinner(a, (0, 10)))
    svar = StringVar()
    svar.set("An Entry")
    a.add("Entry", factory.text_entry(a, svar))
    a.separator()
    a.add("Button 2", factory.button(a, "B2"))
    root.mainloop()

def vframe_test():
    root = Tk()
    a = VFrame(root)
    a.pack(anchor="nw", expand=True, fill="both")
    a.add("VFrame Test", pady=4)
    a.add(factory.button(a, "A Button"))
    a.add(factory.text_entry(a, StringVar()))
    root.mainloop()

def hframe_test():
    root = Tk()
    a = HFrame(root)
    a.pack(anchor="nw", expand=True, fill="both")
    a.add("VFrame Test", padx=4)
    a.add(factory.button(a, "A Button"))
    a.add(factory.text_entry(a, StringVar()))
    root.mainloop()

def border_test():
    root = Tk()
    bframe = BorderFrame(root)
    bframe.pack(anchor="nw", expand=True, fill="both")
    for i in range(4):
        bn = factory.button(bframe.north, "N%d" % i)
        bn.grid(row=0, column=i)
        bs = factory.button(bframe.south, "S%d" % i)
        bs.grid(row=0, column=i)
        be = factory.button(bframe.east, "E%d" % i)
        be.grid(row=i, column=0)
        bw = factory.button(bframe.west, "W%d" % i)
        bw.grid(row=i, column=0)
    for r in range(4):
        for c in range(4):
            b = factory.button(bframe.center, "%d.%d" % (r,c))
            b.grid(row=r, column=c)
            bframe.center.grid_columnconfigure(c, weight=1)
        bframe.center.grid_rowconfigure(r, weight=1)
    bframe.center.config(bg="BLUE")
    root.mainloop()    
