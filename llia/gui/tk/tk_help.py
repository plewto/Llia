# llia.gui.tk.tk_help
# 2016.05.24

from __future__ import print_function
from Tkinter import (BOTH, END, FLAT, HORIZONTAL, LEFT, PanedWindow, RIGHT, StringVar, Toplevel)

import llia.gui.tk.tk_factory as factory
import llia.gui.tk.tk_layout as layout
from llia.gui.llhelp import help_topics, read_help_file


__help_window = None

def display_help(topic=None):
    global __help_window
    if not __help_window:
        __help_window = __TkHelpDialog(None)
    __help_window.deiconify()
    if topic:
        __help_window.display_topic(topic)


class __TkHelpDialog(Toplevel):

    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.title("Llia Help")
        main = PanedWindow(self, orient=HORIZONTAL)
        main.pack(anchor="nw", expand=True, fill=BOTH)

        # Help topics list in west pane
        west = layout.BorderFrame(main)
        lab_topics = factory.center_label(west.north, "Help Topics")
        lab_topics.pack()
        listbox_topics = factory.listbox(west.center, self._select_topic)
        scrollbar_topics = factory.scrollbar(west.center, yclient=listbox_topics)
        scrollbar_topics.pack(side=RIGHT, fill="y")
        listbox_topics.pack(side=LEFT, fill="y")
        for topic in help_topics():
            listbox_topics.insert(END, topic)
        main.add(west)
        self.listbox_topics = listbox_topics

        # Help Text Area
        east = factory.frame(main)
        #east.config(background=factory.pallet["BG"])
        main.add(east)
        text_widget = factory.text_widget(east)
        self.text_widget = text_widget
        sbar_left = factory.scrollbar(east, yclient=text_widget)
        sbar_left.pack(side=RIGHT, fill="y")
        text_widget.pack(side=LEFT, fill=BOTH)
        text_widget.config(relief=FLAT)
        self.display_topic("abus")
        self.protocol("WM_DELETE_WINDOW", self.iconify)
        
    def clear(self):
        self.text_widget.delete('1.0', END)
        
    def append(self, text):
        self.text_widget.insert(END, text)

    def set_text(self, text):
        self.clear()
        self.append(text)
        
    def display_topic(self, topic):
        txt = read_help_file(topic)
        self.set_text(txt)
        
    def _select_topic(self, _):
        index = self.listbox_topics.curselection()[0]
        topic = self.listbox_topics.get(index)
        self.display_topic(topic)
        
    # def hide(self):
    #     print("HELP WINDOW CCLOSE")
    #     self.withdraw()
        
