# llia.gui.tk.graph.lliagraph

from __future__ import print_function
from Tkinter import Canvas, Frame
import random

import llia.gui.tk.graph.graph_config as gconfig
import llia.gui.tk.tk_factory as factory
from llia.gui.tk.graph.token import SynthToken
import llia.constants as con
from graph_config import pallet




pallet = gconfig.pallet


class LliaGraph(Frame):
                
    def __init__(self, master, app):
        Frame.__init__(self, master)
        self.config(background=factory.bg())
        canvas = Canvas(self,
                        width=gconfig.GRAPH_WIDTH,
                        height=gconfig.GRAPH_HEIGHT,
                        background=pallet["graph-background"])
        self.canvas = canvas
        canvas.pack(anchor='nw', expand=True, fill='both')
        self.canvas = canvas
        self.app = app
        self.proxy = app.proxy
        b_sync = factory.button(canvas, "Sync", command=self.sync)
        x0,y0= 15, 15
        b_sync.place(x=x0,y=y0)
        self._tokens = {}  # maps sid -> SynthToken
        #self._drag_info = {"x" : 0, "y" : 0, "item" : None}
    
    def status(self, msg):
        self.app.main_window().status(msg)

    def collect_garbage(self):
        pass
        # self.tokens of deletaed synths/buses
        
    def sync(self):
        self.collect_garbage()
        for sy in self.proxy.get_all_synths():
            sid = sy.sid
            if not(self._tokens.has_key(sid)):
                token = SynthToken(self.canvas, self.app, sy)
                self._tokens[sid] = token

        for sid,tkn in self._tokens.items():
            print("DEBUG sid %s   token %s" % (sid, tkn))
            self.canvas.tag_bind(tkn["image"], "<Enter>",
                                 lambda x: self._highlight_token(tkn))
            self.canvas.tag_bind(tkn["image"], "<Leave>",
                                 lambda x: self._unhighlight_token(tkn))

    def _highlight_token(self, token):
        c = pallet["token-activeoutline"]
        self.canvas.itemconfig(token["pad"], outline=c)
        self._show_synth_info(token)

    def _unhighlight_token(self, token):
        c = pallet["token-outline"]
        self.canvas.itemconfig(token["pad"], outline=c)
        self._clear_synth_info(token)
        
    def _clear_synth_info(self, *_):
        pass
        self.canvas.delete("info-text")

    def _show_synth_info(self, token):
        self._clear_synth_info()
        sid = token.synth.sid
        sy = self.app.proxy.get_synth(sid)
        specs = sy.specs
        line = 0

        def header(text):
            x = gconfig.x_info
            y = gconfig.y_info+line*gconfig.y_info_delta
            tags = ("info-text", "info-header")
            self.canvas.create_text(x,y,text=text,anchor='w',tags=tags)

        def data(text):
            x = gconfig.x_info + gconfig.x_info_data_indent
            y = gconfig.y_info+line*gconfig.y_info_delta
            tags = ("info-text", "info-data")
            self.canvas.create_text(x,y,text=text,anchor='w',tags=tags)
            
        line=0
        if specs["is-controller"]:
            text = "Controller: %s"
        elif specs["is-efx"]:
            text = "Effect: %s"
        else:
            text = "Synth: %s"
        text = text % sid
        header(text)

        plst = sy.available_audio_input_parameters()
        if plst:
            line+=1
            header("Audio Input Buses:")
            for param in plst:
                line+=1
                bname = sy.get_audio_input_bus(param)
                data("%-12s <-- %s" % (param, bname))  

        plst = sy.available_audio_output_parameters()
        if plst:
            line+=1
            header("Audio Output Buses:")
            for param in plst:
                line+=1
                bname = sy.get_audio_output_bus(param)
                data("%-12s --> %s" % (param, bname))  
        
        self.canvas.itemconfig("info-header",
                               fill = pallet["info-header"],
                               font = gconfig.info_font)
        self.canvas.itemconfig("info-data",
                               fill = pallet["info-data"],
                               font = gconfig.info_font)
        
