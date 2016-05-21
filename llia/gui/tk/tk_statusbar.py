# llia.gui.tk.statusbar
# 2016.05.21

from Tkinter import Frame
import ttk

from llia.gui.tk.tk_layout import BorderFrame
import llia.gui.tk.tk_factory as factory

class StatusBar(BorderFrame):

    def __init__(self, master):
        BorderFrame.__init__(self, master)
        b_clear = factory.clear_button(self.west, self.clear, "Clear status line")
        self.label = factory.label(self.center, text = "")
        b_clear.pack()
        self.label.pack(anchor="w", expand=True, fill="x")

    @staticmethod
    def _pad_text(text):
        mx = 40
        n = len(text)
        diff = mx - n
        if diff > 0:
            pad = ' '*diff
            text = text + pad
        return text
        
    def clear(self):
        self.label.config(text = self._pad_text(""))
        self.label.update_idletasks()

    def set(self, msg):
        self.label.config(text = self._pad_text(msg))
        self.label.update_idletasks()

    def set_format(self, frmt, *args):
        self.set(frmt % args)

    def warning(self, msg):
        msg = "WARNING: %s" % msg
        self.label.config(text = self._pad_text(msg))
        self.label.update_ideltask()

    def error(self, msg):
        msg = "ERROR: %s" % msg
        self.label.config(text = self._pad_text(msg))
        self.label.update_ideltask()
