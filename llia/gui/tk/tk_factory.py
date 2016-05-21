# llia.gui.tk.factory
# 2016.05.21

from Tkinter import *
import ttk, tkFont

import llia.constants as constants
from llia.thirdparty.tk_tooltip import ToolTip

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
    return w

def center_label(master, text):
    w = label(master, text)
    w.config(justify=CENTER)
    return w

def big_label(master, text, var=None):
    w = label(master, text, var)
    w.config(font=BIG_FONT)
    return w


#  ---------------------------------------------------------------------- 
#                                   Buttons

def button(master, text, command=None, ttip=""):
    b = Button(master, text=text)
    if command:
        b.config(command=command)
    tooltip(b, ttip)
    return b

def clear_button(master, command=None, ttip=""):
    b = button(master, 'X', command, ttip)
    return b
