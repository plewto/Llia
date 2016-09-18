# llia.gui.tk.graph.lliagraph

from Tkinter import Canvas, Frame

from random import randint

import llia.gui.tk.tk_factory as factory
from llia.gui.tk.graph.gconfig import gconfig
from llia.gui.tk.graph.sytoken import SynthToken, EfxToken, ControllerToken
from llia.gui.tk.graph.bustoken import AudiobusToken, ControlbusToken
from llia.gui.tk.graph.infocanvas import InfoCanvas

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
        info_canvas = InfoCanvas(self)
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

        self._synth_tokens = {}  # map [sid] -> SynthToken
        self._audio_bus_tokens = {}    # map [bus-name] ->BusToken
        self._control_bus_tokens = {}
        
    def status(self, msg):
        self.app.main_window().status(msg)

    def warning(self, msg):
        self.app.mani_window().warning(msg)

    def clear_info(self):
        self.info_canvas.clear_info()

    def display_info(self, text):
        self.info_canvas.display_info(text)
        
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
  
    # def collect_garbage(self):
    #     for sid,tkn in self._synth_tokens.items():
    #         if not(self.proxy.synth_exists(None, None, sid)):
    #             self._synth_tokens.pop(sid)
    #             self.canvas.delete(sid)
    #     for bname,tkn in self._bus_tokens.items():
    #         if not(self.proxy.bus_exists(bname)):
    #             self._bus_tokens.pop(bname)
    #             self.canvas.delete(bname)

    def collect_garbage(self):
        for sid,tkn in self._synth_tokens.items():
            if not(self.proxy.synth_exists(None, None, sid)):
                self._synth_tokens.pop(sid)
                self.canvas.delete(sid)
        for bname,tkn in self._audio_bus_tokens.items():
            if not(self.proxy.bus_exists(bname)):
                self._audio_bus_tokens.pop(bname)
                self._canvas.delete(bname)
        for bname,tkn in self._control_bus_tokens.items():
            if not(self.proxy.bus_exists(bname)):
                self._control_bus_tokens.pop(bname)
                self._canvas.delete(bname)

    def sync(self, *_):
        self.collect_garbage()
        # Add new synths
        for sy in self.proxy.get_all_synths():
            sid = sy.sid
            specs = sy.specs
            if not(self._synth_tokens.has_key(sid)):
                if specs["is-controller"]:
                    tkn = ControllerToken(self,sy)
                elif specs["is-efx"]:
                    tkn = EfxToken(self,sy)
                else:
                    tkn = SynthToken(self,sy)
                self._synth_tokens[sid] = tkn
                tkn.render()
        # Add new audio buses
        for bname in self.proxy.audio_bus_names():
            if not(self._audio_bus_tokens.has_key(bname)):
                bobj = self.proxy.get_audio_bus(bname)
                btoken = AudiobusToken(self,bobj)
                self._audio_bus_tokens[bname] = btoken
                btoken.render()
        # Add new control buses
        for bname in self.proxy.control_bus_names():
            if not(self._control_bus_tokens.has_key(bname)):
                bobj = self.proxy.get_control_bus(bname)
                btoken = ControlbusToken(self,bobj)
                self._control_bus_tokens[bname] = btoken
                btoken.render()

        canvas = self.canvas
        canvas.delete('path')
        y_input_offset = gconfig["audio-bus-height"]/2
        for bname, tkn in self._audio_bus_tokens.items():
            busobj = tkn.client
            x0,y0 = canvas.coords(tkn['pad'])[:2]
            xin, yin = x0,y0+y_input_offset
            for bsrc in busobj.sources():
                sid,param = bsrc.sid,bsrc.param
                sytoken = self._synth_tokens[sid]
                port_offset = sytoken.audio_output_ports[param][2]
                xtk,ytk = canvas.coords(sytoken['pad'])[:2]
                xout,yout = xtk+port_offset[0],ytk+port_offset[1]
                canvas.create_line(xin,yin,xout,yout,
                                   fill=tkn['color'],
                                   tags = (bname, sid, "path", "audio-path"))
            xout, yout = x0+gconfig["audio-bus-width"],y0+y_input_offset
            for bsink in busobj.sinks():
                sid,param = bsink.sid,bsink.param
                sytoken = self._synth_tokens[sid]
                port_offset = sytoken.audio_input_ports[param][2]
                xtk,ytk = canvas.coords(sytoken['pad'])[:2]
                xin,yin = xtk+port_offset[0],ytk+port_offset[1]
                canvas.create_line(xin,yin,xout,yout,
                                   fill=tkn['color'],
                                   tags = (bname,sid,"path","audio-path"))
                
        height = gconfig["control-bus-height"]
        width = gconfig["control-bus-width"]
        for bname,tkn in self._control_bus_tokens.items():
            if not(tkn.is_protected()):
                busobj = tkn.client
                x0,y0 = canvas.coords(tkn['pad'])[:2]
                xin = x0+width/2
                yin = y0+height
                dash = gconfig["control-path-dash"]
                lwidth = gconfig["control-path-width"]
                for bsrc in busobj.sources():
                    sid,param = bsrc.sid,bsrc.param
                    sytoken = self._synth_tokens[sid]
                    port_offset = sytoken.control_output_ports[param][2]
                    xtk,ytk = canvas.coords(sytoken['pad'])[:2]
                    xout,yout = xtk+port_offset[0], ytk+port_offset[1]
                    canvas.create_line(xin,yin,xout,yout,
                                       fill=tkn['color'],
                                       dash=dash,
                                       width = lwidth,
                                       tags = (bname,sid,"path","control-path"))
                xout, yout = x0+height/2,y0
                for bsink in busobj.sinks():
                    sid,param = bsink.sid,bsink.param
                    sytoken = self._synth_tokens[sid]
                    port_offset = sytoken.control_input_ports[param][2]
                    xtk,ytk = canvas.coords(sytoken['pad'])[:2]
                    xin,yin = xtk+port_offset[0],ytk+port_offset[1]
                    canvas.create_line(xin,yin,xout,yout,
                                       fill=tkn['color'],
                                       dash=dash,
                                       width=lwidth,
                                       tags = (bname,sid,"path","control-path"))
        canvas.lower("path")
