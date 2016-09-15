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

    def find_sink_tokens(self):
        acc = []
        for bs in self.client.sinks():
            tk = self.graph.find_token(bs.sid)
            if tk: acc.append(tk)
        return acc

    def find_source_tokens(self):
        acc = []
        for bs in self.client.sources():
            tk = self.graph.find_token(bs.sid)
            if tk: acc.append(tk)
        return acc

        
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

    def keep_hiden(self):
        return False    
    
    def render(self):
        x0, y0 = randint(30,500), randint(30,500)
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
            self["color"] = gconfig.audio_bus_color()
            outline = self["color"]
            activeoutline = gconfig["bus-activeoutline"]
            text_fill = 'white'
            canvas = self.canvas
            text_x_shift = 0
            self._x_wedge = 20
            xin, xout = x0+self._x_wedge, x1+self._x_wedge
            if self.is_hardware_output():
                pad = canvas.create_polygon([x0,y0,x1,y0,x1,y1,x0,y1,
                                             xin,yc,x0,y0],
                                            tags = ("pad", "audio-bus", cid),
                                            fill = fill,
                                            outline = outline)
                text_x_shift = 10
            elif self.is_hardware_input():
                pad = canvas.create_polygon([x0,y0,x1,y0,xout,yc,x1,y1,
                                             x0,y1,x0,y0],
                                            tags = ("pad", "audio-bus", cid),
                                            fill = fill,
                                            outline = outline)
                text_x_shift = -10
            else:
                pad = canvas.create_polygon([x0,y0,x1,y0,xout,yc,x1,y1,x0,y1,
                                             xin,yc,x0,y0],
                                            tags = ("pad", "audio-bus", cid),
                                            fill = fill,
                                            outline = outline)
            txt = canvas.create_text(xc+text_x_shift,yc,
                                     text = cid,
                                     tags = ("text", "audio-bus", cid),
                                     fill = text_fill,
                                     font = gconfig["bus-name-font"])
            radius = 4 # io "port" radius
            xin0, xin1 = x0-radius, x0+radius
            xout0, xout1 = x1+self._x_wedge-radius, x1+self._x_wedge+radius
            yin0, yin1 = yc-radius, yc+radius
            has_input = not(cid.startswith("in_"))
            has_output = not(cid.startswith("out_"))
            if has_input:
                cin = canvas.create_oval(xin0, yin0, xin1, yin1,
                                         tags = ("input-port", "audio-bus", cid),
                                         fill = gconfig["io-audio-sink"])
                self["input-port"] = cin
            if has_output:
                cout = canvas.create_oval(xout0, yin0, xout1, yin1,
                                         tags = ("output-port", "audio-bus", cid),
                                         fill = gconfig["io-audio-source"]) 
                self["output-port"] = cout
            self["pad"] = pad
            self["text"] = txt
            canvas.tag_bind(cid,"<Enter>", self.highlight)
            canvas.tag_bind(cid,"<Leave>", self.unhighlight)
            canvas.tag_bind(cid, "<B1-Motion>", self.drag)
            canvas.tag_bind(cid, "<ButtonPress-1>", self.pickup)
            canvas.tag_bind(cid, "<ButtonRelease-1>", self.drop)

    def audio_input_coords(self):
        x0,y0 = self.canvas.coords(self["pad"])[:2]
        x1,y1 = x0+self['width'], y0+self['height']
        yc = (y0+y1)/2
        return x0,yc

    def audio_output_coords(self):
        x0,y0 = self.canvas.coords(self["pad"])[:2]
        x1,y1 = x0+self['width'], y0+self['height']
        yc = (y0+y1)/2
        return x1+self._x_wedge,yc

    def render_paths(self):
        x0,y0 = self.audio_input_coords()
        color = self["color"]
        dash = gconfig["audio-dash-pattern"]
        for tk in self.find_source_tokens():
            x1,y1 = tk.audio_output_coords()
            ln = self.canvas.create_line(x0,y0,x1,y1,
                                         fill = color,
                                         dash = dash,
                                         tags = ("path","audio",
                                                 self.client_id(),
                                                 tk.client_id()))
        x0,y0 = self.audio_output_coords()
        for tk in self.find_sink_tokens():
            x1,y1 = tk.audio_input_coords()
            ln = self.canvas.create_line(x0,y0,x1,y1,
                                         fill = color,
                                         dash = dash,
                                         tags = ("path","audio",
                                                 self.client_id(),
                                                 tk.client_id()))
            
            
    
            
class ControlBusToken(BusToken):

    def __init__(self, graph, app, cbusobj):
        super(ControlBusToken, self).__init__(graph, app, cbusobj)

    def is_control_bus(self):
        return True

    def keep_hidden(self):
        return self.is_protected()

    def render(self):
        if not(self.keep_hidden()):
            cid = self.client_id()
            x0, y0 = randint(30,500), randint(30,500)
            x1, y1 = x0+self['width'], y0+self['height']
            xc, yc = (x0+x1)/2, (y0+y1)/2
            fill = 'black'
            self["color"] = gconfig.control_bus_color()
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
                                     fill = gconfig['io-control-sink'])
            cout = canvas.create_oval(xout0, yin0, xout1, yin1,
                                      tags = ("output-port", "control-bus", cid),
                                      fill = gconfig['io-control-source'])
            self["pad"] = pad
            self["text"] = txt
            self["output-port"] = cout
            self["input-port"] = cin
            canvas.tag_bind(cid,"<Enter>", self.highlight)
            canvas.tag_bind(cid,"<Leave>", self.unhighlight)
            canvas.tag_bind(cid, "<B1-Motion>", self.drag)
            canvas.tag_bind(cid, "<ButtonPress-1>", self.pickup)
            canvas.tag_bind(cid, "<ButtonRelease-1>", self.drop)

    def control_input_coords(self):
        x0,y0,x1,y1 = self.canvas.coords(self["pad"])
        yc = (y0+y1)/2
        return x0,yc

    def control_output_coords(self):
        x0,y0,x1,y1 = self.canvas.coords(self["pad"])
        yc = (y0+y1)/2
        return x1,yc
            
    def render_paths(self):
        try:
            x0,y0 = self.control_input_coords()
            color = self["color"]
            dash = gconfig["control-dash-pattern"]
            for tk in self.find_source_tokens():
                x1,y1 = tk.control_output_coords()
                ln = self.canvas.create_line(x0,y0,x1,y1,
                                             fill = color,
                                             dash = dash,
                                             tags = ("path","control",
                                                     self.client_id(),
                                                     tk.client_id()))
            x0,y0 = self.control_output_coords()
            for tk in self.find_sink_tokens():
                x1,y1 = tk.control_input_coords()
                ln = self.canvas.create_line(x0,y0,x1,y1,
                                             fill = color,
                                             dash = dash,
                                             tags = ("path","control",
                                                     self.client_id(),
                                                     tk.client_id()))
        except KeyError:   # ignore hidden buses
            pass
            
