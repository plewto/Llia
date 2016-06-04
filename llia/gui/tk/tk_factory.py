# llia.gui.tk.factory
# 2016.05.21

from __future__ import print_function

from Tkinter import *
from ttk import *
from tkFont import Font
from PIL import Image, ImageTk


from llia.thirdparty.tk_tooltip import ToolTip
import llia.constants as constants


# from llia.gui.tk.pallet import Pallet
# pallet = Pallet()
# BIG_FONT = Font(family="Courier", size=30)
# WARNING_FONT = Font(family="Courier", size=12)

__widget_class_prefix = ""

def set_class_prefix(p):
    __widget_class_prefix = p

def __widget_class_name(base):
    if __widget_class_prefix:
        return "%s.%s" % (__widget_class_prefix, base)
    else:
        return base

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
    cls = __widget_class_name("TLabel")
    w = Label(master, text=text, class_=cls)
    w.config(justify=LEFT)
    if var:
        w.config(textvariable=var)
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
    # w.config(foreground=pallet["WARNING-FG"])
    return w

def padding_label(master, n=4):
    w = Label(master, text = ' '*4)
    return w

# def big_label(master, text, var=None):
#     w = label(master, text, var)
#     w.config(font=BIG_FONT)
#     return w




# def image_label(master, filename):
#     img = Image.open(filename)
#     photo = ImageTk.PhotoImage(img)
#     w = Label(master, image=photo)
#     w.configure(background="red")
#     return w

#  ---------------------------------------------------------------------- 
#                                   Buttons

def button(master, text, command=None, ttip=""):
    cls = __widget_class_name("TButton")
    b = Button(master, text=text, class_ = cls)
    if command:
        b.config(command=command)
    tooltip(b, ttip)
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
    cls = __widget_class_name("TRadiobutton")
    rb = Radiobutton(master, text=text, variable=var, value=value, class_=cls)
    tooltip(rb, ttip)
    return rb


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
    return lbx



#  ---------------------------------------------------------------------- 
#                                  Scrollbar

def scrollbar(master, xclient=None, yclient=None, orientation=VERTICAL):
    if orientation == VERTICAL:
        cls = __widget_class_name("Vertical.TScrollbar")
    else:
        cls = __widget_class_name("Horizontal.TScrollbar")
    sb = Scrollbar(master, class_ = cls)
    sb.config(orient=orientation)
    if xclient:
        xclient.config(xscrollcommand=sb.set)
        sb.config(command = xclient.xview)
    if yclient:
        yclient.config(yscrollcommand=sb.set)
        sb.config(command = yclient.yview)
    return sb


#  ---------------------------------------------------------------------- 
#                                   Spinbox
#
# NOTE: Spinbox is not a ttk widget

def int_spinbox(master, textvar, from_, to, ttip=""):
    sb = Spinbox(master, from_=int(from_), to=int(to), textvariable=textvar)
    tooltip(sb, ttip)
    return sb


#  ---------------------------------------------------------------------- 
#                                    Text
#
# NOTE: Text is not a ttk widget

def entry(master, var, ttip=""):
    cls = __widget_class_name("TEntry")
    t = Entry(master)
    t.configure(textvariable=var)
    # t.configure(background=pallet["BG"])
    # t.configure(foreground=pallet["FG"])
    tooltip(t, ttip)
    return t

def text_widget(master, ttip=""):
    t = Text(master)
    # t.config(background=pallet["BG"])
    # t.config(foreground=pallet["FG"])
    tooltip(t, ttip)
    return t

def read_only_text(master, text):
    t = Text(master)
    t.insert(END, text)
    # t.config(background=pallet["BG"])
    # t.config(foreground=pallet["FG"])
    return t
