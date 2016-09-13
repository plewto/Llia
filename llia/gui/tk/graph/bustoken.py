# llia.gui.tk.graph.bustoken
#
# class Hierarchy:
#
#  Token
#    |
#    +--- BusToken
#            |
#            +--- AudioBusToken
#            +--- ControlBusToken

from __future__ import print_function

from llia.gui.tk.graph.graph_config import gconfig
from llia.gui.tk.graph.token import Token
from random import randint
from llia.gui.tk.graph.graph_config import gconfig

class BusToken(Token):

    def __init__(self, graph, app, busobj):
        super(BusToken, self).__init__(graph, app, busobj)
        self["width"] = gconfig["bus-token-width"]
        self["height"] = gconfig["bus-token-height"]

    def client_id(self):
        return self.client.name

    def is_protected(self):
        return self.client.is_protected()
   
    def render_info(self, *_):
        if self.is_audio_bus():
            header = "Audio bus: %s"
        else:
            header = "Control bus: %s"
        self._info_header(0, header % self.client_id())
        self._info_data(1, "FPO")

    def highlight(self, *_):
        c = gconfig["bus-activeoutline"]
        self.canvas.itemconfig(self['pad'], outline=c)
        self.render_info()

    def unhighlight(self, *_):
        c = self["color"]
        self.canvas.itemconfig(self['pad'], outline=c)
        self.clear_info()

        
class AudioBusToken(BusToken):

    def __init__(self, graph, app, abusobj, first_pass=False):
        super(AudioBusToken, self).__init__(graph, app, abusobj)
        self._first_pass = first_pass  # if True allign bus on edge

    def is_audio_bus(self):
        return True

    def is_hardware_output(self):
        return self.client.is_hardware_output()

    def is_hardware_input(self):
        return self.client.is_hardware_input()
    
    # def keep_hiden(self):
    #     cid = self.client_id()
    #     c = self.client.source_count() + self.client.sink_count()
    #     io = cid.startswith("in_") or cid.startswith("out_")
    #     return not(io) or c == 0

    def keep_hiden(self):
        return False    
    
    def render(self):
        if not(self.keep_hiden()):
            cid = self.client_id()
            if self._first_pass:
                if cid.startswith("in_"):
                    n = int(cid[3])
                    x0 = 15
                    y0 = (n+1)*48+15
                elif cid.startswith("out_"):
                    n = int(cid[4])
                    x0 = 600
                    y0 = (n+1)*48+15
            else:
                x0, y0 = randint(30, 500), randint(30, 300)
            x1, y1 = x0+self['width'], y0+self['height']
            xc, yc = (x0+x1)/2, (y0+y1)/2

            fill = "black"
            self["color"] = 'blue' # ISSUE generate series of colors
            outline = self["color"]
            activeoutline = gconfig["bus-activeoutline"]
            text_fill = 'white'
            canvas = self.canvas
            pad = canvas.create_rectangle(x0,y0,x1,y1,
                                          tags = ("pad", "audio-bus", cid),
                                          fill = fill,
                                          outline = outline,
                                          activeoutline = activeoutline)
            txt = canvas.create_text(xc,yc,
                                     text = cid,
                                     tags = ("text", "audio-bus", cid),
                                     fill = text_fill,
                                     font = gconfig["bus-name-font"])
            radius = 4 # io "port" radius
            xin0, xin1 = x0-radius, x0+radius
            xout0, xout1 = x1-radius, x1+radius
            yin0, yin1 = yc-radius, yc+radius
            has_input = not(cid.startswith("in_"))
            has_output = not(cid.startswith("out_"))
            if has_input:
                cin = canvas.create_oval(xin0, yin0, xin1, yin1,
                                         tags = ("input-port", "audio-bus", cid),
                                         fill = 'green') # ISSUE
                self["input-port"] = cin
            if has_output:
                cin = canvas.create_oval(xout0, yin0, xout1, yin1,
                                         tags = ("output-port", "audio-bus", cid),
                                         fill = 'green') # ISSUE
                self["output-port"] = cin
            self["pad"] = pad
            self["text"] = txt
            canvas.tag_bind(cid,"<Enter>", self.highlight)
            canvas.tag_bind(cid,"<Leave>", self.unhighlight)
            canvas.tag_bind(cid, "<B1-Motion>", self.drag)
            canvas.tag_bind(cid, "<ButtonPress-1>", self.pickup)
            canvas.tag_bind(cid, "<ButtonRelease-1>", self.drop)
            
            
class ControlBusToken(BusToken):

    def __init__(self, graph, app, cbusobj):
        super(ControlBusToken, self).__init__(graph, app, cbusobj)

    def is_control_bus(self):
        return True

    # def keep_hidden(self):
    #     c = self.client.source_count() + self.client.sink_count()
    #     return self.is_protected() or c == 0
    def keep_hidden(self):
        return self.is_protected()

    def render(self):
        if not(self.keep_hidden()):
            cid = self.client_id()
            x0, y0 = randint(30,500), randint(30,500)
            x1, y1 = x0+self['width'], y0+self['height']
            xc, yc = (x0+x1)/2, (y0+y1)/2
            fill = 'black'
            self["color"] = "green"  # isse generate serwies of colors
            outline = self["color"]
            activeoutline = gconfig["bus-activeoutline"]
            text_fill = 'white'
            canvas = self.canvas
            pad = canvas.create_oval(x0,y0,x1,y1,
                                     tags = ("pad", "control-bus", cid),
                                     fill = fill,
                                     outline = outline,
                                     activeoutline = activeoutline)
            txt = canvas.create_text(xc,yc,
                                     text = cid,
                                     tags = ("text", "control-bus", cid),
                                     fill = text_fill,
                                     font = gconfig["bus-name-font"])
            radius = 4
            xin0, xin1 = x0-radius, x0+radius
            xout0, xout1 = x1-radius, x1+radius
            yin0, yin1 = yc-radius, yc+radius
            has_input = not(cid.startswith("in_"))
            has_output = not(cid.startswith("out_"))
            cin = canvas.create_oval(xin0, yin0, xin1, yin1,
                                     tags = ("input-port", "control-bus", cid),
                                     fill = 'green') # ISSUE


            cout = canvas.create_oval(xout0, yin0, xout1, yin1,
                                      tags = ("output-port", "control-bus", cid),
                                      fill = 'green') # ISSUE
            self["pad"] = pad
            self["text"] = txt
            self["output-port"] = cout
            self["input-port"] = cin
            canvas.tag_bind(cid,"<Enter>", self.highlight)
            canvas.tag_bind(cid,"<Leave>", self.unhighlight)
            canvas.tag_bind(cid, "<B1-Motion>", self.drag)
            canvas.tag_bind(cid, "<ButtonPress-1>", self.pickup)
            canvas.tag_bind(cid, "<ButtonRelease-1>", self.drop)

