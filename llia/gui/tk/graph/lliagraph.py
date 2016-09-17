

from Tkinter import Canvas, Frame

from random import randint

import llia.gui.tk.tk_factory as factory
from llia.gui.tk.graph.gconfig import gconfig
from llia.gui.tk.graph.sytoken import SynthToken, EfxToken, ControllerToken
from llia.gui.tk.graph.bustoken import AudiobusToken, ControlbusToken

class LliaGraph(Frame):

    def __init__(self, master, app):
        Frame.__init__(self, master)
        self.app = app
        self.proxy = app.proxy
        self.config(background=factory.bg())
        canvas = Canvas(self,
                        width=gconfig["graph-width"],
                        height=gconfig["graph-height"],
                        background=gconfig["graph-fill"])
        self.canvas = canvas
        info_canvas = Canvas(self,
                             width=gconfig["info-area-width"],
                             height=gconfig["graph-height"],
                             background=gconfig["info-fill"])
        self.info_canvas = info_canvas
        toolbar = factory.frame(self)
        info_canvas.grid(row=0,column=0,rowspan=1,columnspan=1, sticky='wns')
        canvas.grid(row=0,column=1,rowspan=1,columnspan=1, sticky='nsew')
        toolbar.grid(row=1,column=0, rowspan=1,columnspan=2, sticky='ew')
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        # toolbar buttons
        def tbutton(col, text, command=None, ttip=''):
            b = factory.button(toolbar, text, command=command)
            b.grid(row=0, column=col, sticky='ew')
            return b
        tbutton(0, 'sync', self.sync)

        self._tokens = {}  # map [id] -> Token
        
    def status(self, msg):
        self.app.main_window().status(msg)

    def warning(self, msg):
        self.app.mani_window().warning(msg)

    @staticmethod
    def _initial_audiobus_coords(token):
        bid = token.client_id()
        x,y = randint(90, 400), randint(150, 400)
        y_space = 60
        if bid.startswith("in_"):
            try:
                bnum = int(bid[3])
                x = 30
                y = (bnum+1)*y_space
            except (ValueError,IndexError):
                pass
        elif bid.startswith("out_"):
            try:
                bnum = int(bid[4])
                x = 600
                y = (bnum+1)*y_space
            except (ValueError,IndexError):
                pass
        return x,y

    @staticmethod
    def _initial_controlbus_coords(token):
        x,y = randint(90,400),randint(350, 550)
        return x,y

    @staticmethod
    def _initial_synth_coords(token):
        x,y = randint(90,500),randint(30,500)
        if token.is_controller():
            y = randint(400, 600)
        elif token.is_efx():
            y = randint(200, 400)
        else:
            y = randint(30, 200)
        return x,y
    
    def suggest_initial_coords(self, token):
        if token.is_audio_bus():
            x,y = self._initial_audiobus_coords(token)
        elif token.is_control_bus():
            x,y = self._initial_controlbus_coords(token)
        else:
            x,y = self._initial_synth_coords(token)
        return x,y
    
    def collect_garbage(self):
        for key,tkn in self._tokens.items():
            if tkn.is_synth():
                sid = key
                if not(self.proxy.synth_exists(None, None, sid)):
                    self._tokens.pop(sid)
                    self.canvas.delete(sid)
            else:
                busid = key
                if not(self.proxy.bus_exists(busid)):
                    self._tokens.pop(busid)
                    self.canvas.delete(busid)
        
    def sync(self, *_):
        self.collect_garbage()
        # Add new synths
        for sy in self.proxy.get_all_synths():
            sid = sy.sid
            specs = sy.specs
            if not(self._tokens.has_key(sid)):
                if specs["is-controller"]:
                    tkn = ControllerToken(self,sy)
                elif specs["is-efx"]:
                    tkn = EfxToken(self,sy)
                else:
                    tkn = SynthToken(self,sy)
                self._tokens[sid] = tkn
                tkn.render()
        # Add new audio buses
        for bname in self.proxy.audio_bus_names():
            if not(self._tokens.has_key(bname)):
                bobj = self.proxy.get_audio_bus(bname)
                btoken = AudiobusToken(self,bobj)
                self._tokens[bname] = btoken
                btoken.render()
        # Add new control buses
        for bname in self.proxy.control_bus_names():
            if not(self._tokens.has_key(bname)):
                bobj = self.proxy.get_control_bus(bname)
                btoken = ControlbusToken(self,bobj)
                self._tokens[bname] = btoken
                btoken.render()
                    
                
    
