# llia.gui.tk.graph.bustoken

from llia.gui.tk.graph.token import Token, get_logo_image
from llia.gui.tk.graph.gconfig import gconfig
from llia.gui.tk.graph.port import (AudioSource,AudioSink,
                                    ControlSource,ControlSink)

class BusToken(Token):

    def __init__(self,graph,bus):
        super(BusToken,self).__init__(graph,bus)

    def client_id(self):
        return self.client.name

    def is_protected(self):
        return self.client.is_protected()

    def highlight(self, *_):
        canvas = self.canvas
        highlight = gconfig["highlight-color"]
        canvas.itemconfigure(self['pad'], outline=highlight)
        canvas.itemconfigure(self['text'], fill=highlight)

    def dehighlight(self, *_):
        canvas = self.canvas
        outline = self['outline']
        canvas.itemconfigure(self['pad'], outline=outline)
        canvas.itemconfigure(self['text'], fill=outline)
            
    def _init_event_bindings(self):
        canvas = self.canvas
        itm = self['pad']
        canvas.tag_bind(itm, '<Enter>', self.highlight)
        canvas.tag_bind(itm, '<Leave>', self.dehighlight)
        itm = self['text']
        canvas.tag_bind(itm, '<Enter>', self.highlight)
        canvas.tag_bind(itm, '<Leave>', self.dehighlight)
        
    
class AudiobusToken(BusToken):

    def __init__(self,graph,bus):
        super(AudiobusToken,self).__init__(graph,bus)

    def is_audio_bus(self):
        return True

    def is_protected(self):
        return self.client.is_protected()
    
    def render(self):
        x0,y0 = self.graph.suggest_initial_coords(self)
        x1,y1 = x0+gconfig["audio-bus-width"], y0+gconfig["audio-bus-height"]
        chamfer = gconfig["audio-bus-chamfer"]
        xc = (x0+x1)/2
        yc = (y0+y1)/2
        canvas = self.canvas
        fill = gconfig["audio-bus-fill"]
        outline = gconfig.audio_bus_color()
        self['outline'] = outline
        self['pad'] = None
        self['text'] = None
        self['in-port'] = None
        self['out-port'] = None
        if self.client.is_hardware_input():
            tags = ('audio-input-bus','audio-bus',self.client_id())
            x2 = x1-chamfer
            pad = canvas.create_polygon([x0,y0,x2,y0,x1,yc,x2,y1,x0,y1,x0,y0],
                                        tags=tags,
                                        fill = fill,
                                        outline = outline)
            txt = canvas.create_text(xc,yc,
                                     tags=tags,
                                     text = self.client_id(),
                                     fill = outline,
                                     font = gconfig["bus-name-font"])
            port_source = AudioSource(self.graph,self,(x1+4,yc))
            port_sink = None
        elif self.client.is_hardware_output():
            tags = ('audio-output-bus','audio-bus',self.client_id())
            x2 = x0 + chamfer
            pad = canvas.create_polygon([x0,y0,x1,y0,x1,y1,x0,y1,x2,yc,x0,y0],
                                        tags=tags,
                                        fill = fill,
                                        outline = outline)
            txt = canvas.create_text(xc+4,yc,
                                     tags=tags,
                                     text = self.client_id(),
                                     fill = outline,
                                     font = gconfig["bus-name-font"])
            port_sink = AudioSink(self.graph,self,(x0,yc))
            port_source = None
        else:
            tags = ('audio-bus', self.client_id())
            x2,x3 = x0+chamfer, x1-chamfer
            pad = canvas.create_polygon([x0,y0,x3,y0,x1,yc,x3,y1,
                                         x0,y1,x2,yc,x0,y0],
                                        tags = tags,
                                        fill = fill,
                                        outline = outline)
            txt = canvas.create_text(xc,yc,
                                     tags = tags,
                                     text = self.client_id(),
                                     fill = outline,
                                     font = gconfig["bus-name-font"])
            port_sink = AudioSink(self.graph,self,(x0,yc))
            port_source = AudioSource(self.graph,self,(x1+4,yc))
        self['pad'] = pad
        self['text'] = txt
        self['in-port'] = port_sink
        self['out-port'] = port_source
        self._init_event_bindings()
        

class ControlbusToken(BusToken):

    def __init__(self,graph,bus):
        super(ControlbusToken,self).__init__(graph,bus)

    def is_control_bus(self):
        return True

    def render(self):
        canvas = self.canvas
        x0,y0 = self.graph.suggest_initial_coords(self)
        x1 = x0+gconfig['control-bus-width']
        y1 = y0+gconfig['control-bus-height']
        xc,yc = (x0+x1)/2,(y0+y1)/2
        if not(self.is_protected()):
            tags = ('control-bus', self.client_id())
            outline = gconfig.control_bus_color()
            self['outline'] = outline
            pad = canvas.create_oval(x0,y0,x1,y1,
                                     tags=tags,
                                     fill=gconfig['control-bus-fill'],
                                     outline=outline)
            txt = canvas.create_text(xc,yc,
                                     tags = tags,
                                     text = self.client_id(),
                                     font = gconfig['bus-name-font'],
                                     fill=outline)
            port_sink = ControlSink(self.graph,self,(xc,y1))
            port_source = ControlSource(self.graph,self,(xc,y0))
            self['pad'] = pad
            self['text'] = txt
            self['in-port'] = port_sink
            self['out-port'] = port_source
            self._init_event_bindings()
        else:
            pad = None
            txt = None
            port_sink = None
            port_source = None

        
