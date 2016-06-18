# llia.gui.tk.factory
# 2016.05.21

from __future__ import print_function

import os.path
from Tkinter import *
from ttk import Combobox
import tkFont 
from PIL import Image, ImageTk

from llia.thirdparty.tk_tooltip import ToolTip
import llia.constants as constants
import llia.gui.pallet 




_current_pallet = None

def set_pallet(p):
    global _current_pallet
    if p:
        _current_pallet = p

set_pallet(llia.gui.pallet.pallet)
    
def pallet(key):
    return _current_pallet[key]

def bg():
    return pallet("bg")

def fg():
    return pallet("fg")


_logo_cachet = []


#  ---------------------------------------------------------------------- 
#                                   ToolTip

# Global flag, tooltips enabled/disabled across all instances of Llia
#
enable_tooltips = True

def tooltip(widget, text):
    if enable_tooltips and text:
        tt = ToolTip(widget, msg=text, delay=1.0, follow=True)
        

#  ---------------------------------------------------------------------- 
#                                   Labels

def label(master, text, var=None):
    w = Label(master, text=text)
    w.config(justify=LEFT)
    if var:
        w.config(textvariable=var)
    w.config(background=bg(), foreground=fg())
    return w

def center_label(master, text):
    w = label(master, text)
    w.config(justify=CENTER)
    return w

def dialog_title_label(master, text):
    w = label(master, text)
    return w

def warning_label(master, text=" ", var=None):
    w = label(master, text, var)
    w.config(foreground=pallet("warning-fg"))
    return w

def padding_label(master, n=4):
    w = Label(master, text = ' '*4)
    w.config(background=bg())
    return w

def image_label(master, fname, alt=None):
    alt = alt or fname
    w = label(master, "")
    try:
        img = Image.open(fname)
        photo = ImageTk.PhotoImage(img)
        _logo_cachet.append(photo)
        w.config(image=photo)
    except IOError as err:
        w.config(text=alt)
    w.config(background=bg(), foreground=fg())
    return w

def big_label(master, text):
    f = tkFont.Font(family="Courier", size=18)
    w = Label(master, text=text)
    w.config(font=f)
    w.config(background=bg(), foreground=fg())
    return w

#  ---------------------------------------------------------------------- 
#                                   Buttons

def button(master, text, command=None, ttip=""):
    b = Button(master, text=text)
    if command:
        b.config(command=command)
    tooltip(b, ttip)
    b.config(background=pallet("button-bg"), foreground=fg())
    b.config(activebackground=pallet("ACTIVE-BG"))
    b.config(activeforeground=pallet("ACTIVE-FG"))
    b.config(highlightbackground=bg())
    return b

def clear_button(master, text = "X", command=None, ttip=""):
    b = button(master, text, command, ttip)
    return b

def help_button(master, text="?", command=None):
    b = button(master, text, command=command)
    return b

def accept_button(master, text="OK", command=None, ttip=""):
    b = button(master, text, command, ttip)
    return b

def cancel_button(master, text="Cancel", command=None, ttip=""):
    b = button(master, "Cancel", command, ttip)
    return b

def remove_button(master, text='[-]', command=None, ttip=""):
    b = button(master, text, command, ttip)
    return b

def add_button(master, text = '[+]', command=None, ttip=""):
    b = button(master, text, command, ttip)
    return b

def refresh_button(master, text="()", command=None, ttip="Refresh"):
    b = button(master, text, command, ttip)
    return b

def radio(master, text, var, value, ttip=""):
    rb = Radiobutton(master, text=text, variable=var, value=value)
    tooltip(rb, ttip)
    rb.config(background=bg(), foreground=fg())
    rb.config(highlightbackground=bg())
    rb.config(selectcolor=pallet("radio-select"))
    rb.config(activebackground=pallet("active-bg"))
    rb.config(activeforeground=pallet("active-fg"))
    
    return rb

def logo_button(master, name, fname=None, command=None, ttip=""):
    if not fname:
        fname = os.path.join("/home/sj/dev/Llia/resources", name, "logo.png")
    try:
        img = Image.open(fname)
        photo = ImageTk.PhotoImage(img)
        _logo_cachet.append(photo)
        b = Button(master, text = name, image=photo)
        b.config(compound="top")
        tooltip(b, ttip)
    except IOError:
        b = button(master, name, ttip)
    b.config(command=command)
    b.config(background=bg(), foreground=fg())
    return b
        


#  ---------------------------------------------------------------------- 
#                                   Listbox
#
# NOTE: Listbox is not a ttk widget
#
def listbox(master, command=None, ttip=""):
    lbx = Listbox(master)
    lbx.config(selectmode="SINGLE", exportselection=0)
    if command:
        lbx.bind("<<ListboxSelect>>", command)
    tooltip(lbx, ttip)
    lbx.config(background=bg(), foreground=fg())
    return lbx

#  ---------------------------------------------------------------------- 
#                                  Scrollbar

def scrollbar(master, xclient=None, yclient=None, orientation=VERTICAL):
    # if orientation == VERTICAL:
    #     cls = __widget_class_name("Vertical.TScrollbar")
    # else:
    #     cls = __widget_class_name("Horizontal.TScrollbar")
    # sb = Scrollbar(master, class_ = cls)
    sb = Scrollbar(master)
    sb.config(orient=orientation)
    if xclient:
        xclient.config(xscrollcommand=sb.set)
        sb.config(command = xclient.xview)
    if yclient:
        yclient.config(yscrollcommand=sb.set)
        sb.config(command = yclient.yview)
    sb.config(background=pallet("scrollbar-background"))
    sb.config(troughcolor=pallet("scrollbar-trough"))
    return sb


#  ---------------------------------------------------------------------- 
#                                   Spinbox
#
# NOTE: Spinbox is not a ttk widget

def int_spinbox(master, textvar, from_, to, ttip=""):
    sb = Spinbox(master, from_=int(from_), to=int(to), textvariable=textvar)
    tooltip(sb, ttip)
    sb.config(background=bg(), foreground=fg())
    sb.config(buttonbackground=bg())
    return sb


#  ---------------------------------------------------------------------- 
#                                  Combobox
#

# ISSUE: ttk.Combobox style not effected by pallet
#
def combobox(master, values, ttip=""):
    cb = Combobox(master, values = values)
    tooltip(cb, ttip)
    return cb

def audio_bus_combobox(master, app):
    values = app.proxy.audio_bus_names()
    ttip = "Audio buses"
    return combobox(master, values, ttip)

def control_bus_combobox(master, app):
    values = app.proxy.control_bus_names()
    ttip = "Control buses"
    return combobox(master, values, ttip)

def buffer_combobox(master, app):
    values = app.proxy.buffer_keys()
    ttip = "Buffers"
    return combobox(master, values, ttip)


#  ---------------------------------------------------------------------- 
#                                    Text
#
# NOTE: Text is not a ttk widget

def entry(master, var, ttip=""):
    t = Entry(master)
    t.configure(textvariable=var)
    tooltip(t, ttip)
    t.config(background=bg(), foreground=fg())
    return t

def text_widget(master, ttip=""):
    t = Text(master)
    tooltip(t, ttip)
    t.config(background=bg(), foreground=fg())
    return t

def read_only_text(master, text):
    t = Text(master)
    t.insert(END, text)
    t.config(background=bg(), foreground=fg())
    return t


#  ---------------------------------------------------------------------- 
#                                   Frames

def frame(master):
    f = Frame(master)
    f.config(background = bg())
    f.config(highlightcolor="red")
    f.config(highlightbackground="green")
    return f

def label_frame(master, text):
    f = LabelFrame(master, text=text)
    f.config(background=bg(), fg=fg())
    return f

def notebook(master):
    nb = Notebook(master)
    nb.config(background=bg())
    return nb

def paned_window(master, orient=HORIZONTAL):
    pw = PanedWindow(master, orient=orient)
    pw.config(background=bg())
    return pw


#  ---------------------------------------------------------------------- 
#                                  Toplevel

def toplevel(master=None):
    t = Toplevel(master)
    t.config(background=bg())
    return t
