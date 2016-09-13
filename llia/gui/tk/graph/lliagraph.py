# llia.gui.tk.graph.lliagraph

from __future__ import print_function
from Tkinter import Canvas, Frame


import llia.gui.tk.tk_factory as factory

from llia.gui.tk.graph.graph_config import gconfig
from llia.gui.tk.graph.sytoken import SynthToken, EfxToken, ControllerToken
from llia.gui.tk.graph.bustoken import AudioBusToken, ControlBusToken
from llia.gui.tk.graph.graph_config import gconfig

#import llia.constants as con
#from graph_config import pallet
#pallet = gconfig.pallet



class LliaGraph(Frame):
                
    def __init__(self, master, app):
        Frame.__init__(self, master)
        self.config(background=factory.bg())
        canvas = Canvas(self,
                        width=gconfig["graph-width"],
                        height=gconfig["graph-height"],
                        background=gconfig["graph-fill"])
        self.canvas = canvas
        canvas.pack(anchor='nw', expand=True, fill='both')
        self.canvas = canvas
        self.app = app
        self.proxy = app.proxy
        b_sync = factory.button(canvas, "Sync", command=self.sync)
        x0,y0= 15, 15
        b_sync.place(x=x0,y=y0)
        self._tokens = {}  # maps sid -> SynthToken
        self._first_pass = True
        
    def status(self, msg):
        self.app.main_window().status(msg)

    def warning(self, msg):
        self.app.main_window().warning(msg)

        
    def collect_garbage(self):
        pass
        # self.tokens of deletaed synths/buses

    def sync(self):
        self.collect_garbage()
        # Add any new synths
        for sy in self.proxy.get_all_synths():
            sid = sy.sid
            specs = sy.specs
            if not(self._tokens.has_key(sid)):
                if specs["is-controller"]:
                    sytoken = ControllerToken(self, self.app, sy)
                elif specs["is-efx"]:
                    sytoken = EfxToken(self, self.app, sy)
                else:
                    sytoken = SynthToken(self, self.app, sy)
                self._tokens[sid] = sytoken
                sytoken.render()
        # Add new audio buses
        for abname in self.proxy.audio_bus_names():
            if not(self._tokens.has_key(abname)):
                bobj = self.proxy.get_audio_bus(abname)
                abtoken = AudioBusToken(self, self.app, bobj, self._first_pass)
                self._tokens[bobj.name] = abtoken
                abtoken.render()
        # Add new control buses
        for cbname in self.proxy.control_bus_names():
            if not(self._tokens.has_key(cbname)):
                bobj = self.proxy.get_control_bus(cbname)
                cbtoken = ControlBusToken(self, self.app, bobj)
                self._tokens[bobj.name] = cbtoken
                cbtoken.render()
        self._first_pass = False
        
            
            
