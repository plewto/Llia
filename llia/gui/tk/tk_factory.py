# llia.gui.tk.factory
# 2016.05.21

from Tkinter import *
import ttk, tkFont
from PIL import Image, ImageTk


from llia.thirdparty.tk_tooltip import ToolTip
import llia.constants as constants
from llia.gui.tk.pallet import Pallet


pallet = Pallet()



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

def big_label(master, text, var=None):
    w = label(master, text, var)
    w.config(font=BIG_FONT)
    return w

# def image_label(master, filename):
#     image = Image.open(filename)
#     photo = ImageTk.PhotoImage(image)
#     print("DEBUG image %s" % image)
#     print("DEBUG photo %s" % photo)
#     w = Label(master)
#     w.configure(image=photo)
#     w.configure(background=pallet["BG"])
#     return w

# def image_label(master, filename):
#     logo = Image.open(filename)
#     logo = ImageTk.PhotoImage(logo)
#     w = Label(master, image=logo)
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
#                                    Text

def entry(master, var, ttip=""):
    t = Entry(master)
    t.configure(textvariable=var)
    t.configure(background=pallet["BG"])
    t.configure(foreground=pallet["FG"])
    tooltip(t, ttip)
    return t
