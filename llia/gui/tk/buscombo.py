# llia.gui.tk.buscombo

from Tkinter import StringVar
from ttk import Combobox



class AudioBusCombobox(Combobox):

    """
    Provides Tk Combobox for audio bus selection.
    """
    
    def __init__(self, master, proxy):
        self.proxy = proxy
        self.var_selection = StringVar()
        self.param = None
        Combobox.__init__(self, master, textvariable=self.var_selection, width=30)
        self.sync()

    def sync(self):
        values = self.proxy.audio_bus_names()
        self.config(values=values)
        self.var_selection.set(values[0])

        
class ControlBusCombobox(Combobox):

    """
    Provides Tk Combobox for control bus selection.
    """
    
    def __init__(self, master, proxy):
        self.proxy = proxy
        self.var_selection = StringVar()
        self.param = None
        Combobox.__init__(self, master, textvariable=self.var_selection, width=30)
        self.sync()

    def sync(self):
        values = self.proxy.control_bus_names()
        self.config(values=values)
        self.var_selection.set(values[0])
