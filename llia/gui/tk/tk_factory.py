# llia.gui.tk.factory
# 2016.05.21

from __future__ import print_function

from Tkinter import *
import ttk
from tkFont import Font
from PIL import Image, ImageTk


from llia.thirdparty.tk_tooltip import ToolTip
import llia.constants as constants
from llia.gui.tk.pallet import Pallet


pallet = Pallet()

# BIG_FONT = Font(family="Courier", size=30)
# WARNING_FONT = Font(family="Courier", size=12)

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
    w.configure(background=pallet["BG"])
    w.configure(foreground=pallet["FG"])
    if var:
        w.config(textvariable=var)
    return w

def center_label(master, text):
    w = label(master, text)
    w.config(justify=CENTER)
    return w

# def big_label(master, text, var=None):
#     w = label(master, text, var)
#     w.config(font=BIG_FONT)
#     return w

def warning_label(master, text="", var=None):
    w = label(master, text, var)
    w.config(foreground=pallet["WARNING-FG"])
    return w


# def image_label(master, filename):
#     img = Image.open(filename)
#     photo = ImageTk.PhotoImage(img)
#     w = Label(master, image=photo)
#     w.configure(background="red")
#     return w

#  ---------------------------------------------------------------------- 
#                                   Buttons

def button(master, text, command=None, ttip=""):
    b = Button(master, text=text)
    if command:
        b.config(command=command)
    b.configure(background=pallet["BUTTON-BG"])
    b.configure(foreground=pallet["FG"])
    tooltip(b, ttip)
    return b

def clear_button(master, command=None, ttip=""):
    b = button(master, 'X', command, ttip)
    return b


def help_button(master):
    b = button(master, "?")
    return b


def radio(master, text, var, value, ttip=""):
    rb = Radiobutton(master, text=text, variable=var, value=value)
    rb.configure(background=pallet["BG"])
    rb.configure(foreground=pallet["FG"])
    rb.configure(highlightbackground=pallet["BG"])
    rb.configure(selectcolor=pallet["RADIO-SELECT"])
    tooltip(rb, ttip)
    return rb


#  ---------------------------------------------------------------------- 
#                                   Listbox

def listbox(master, command=None, ttip=""):
    lbx = Listbox(master)
    lbx.config(background=pallet["BG"])
    lbx.config(foreground=pallet["FG"])
    if command:
        lbx.bind("<<ListboxSelect>>", command)
    tooltip(lbx, ttip)
    return lbx



#  ---------------------------------------------------------------------- 
#                                  Scrollbar

def scrollbar(master, xclient=None, yclient=None, orientation=VERTICAL):
    sb = Scrollbar(master)
    sb.config(orient=orientation)
    if xclient:
        xclient.config(xscrollcommand=sb.set)
        sb.config(command = xclient.xview)
    if yclient:
        yclient.config(yscrollcommand=sb.set)
        sb.config(command = yclient.yview)
    #print("DEBUG scrollbar config keys -> ", sb.config().keys())
    sb.config(background=pallet["BG"])
    sb.config(highlightbackground="red")
    return sb

#  ---------------------------------------------------------------------- 
#                                    Text

def entry(master, var, ttip=""):
    t = Entry(master)
    t.configure(textvariable=var)
    t.configure(background=pallet["BG"])
    t.configure(foreground=pallet["FG"])
    tooltip(t, ttip)
    return t

def text_widget(master, ttip=""):
    t = Text(master)
    #t.config(textvariable=var)
    t.config(background=pallet["BG"])
    t.config(foreground=pallet["FG"])
    tooltip(t, ttip)
    return t
