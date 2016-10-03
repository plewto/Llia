# llia.gui.tk.graph.bustoken

from llia.gui.tk.graph.token import Token, get_logo_image
from llia.gui.tk.graph.gconfig import gconfig
from llia.gui.tk.graph.port import (AudioSource,AudioSink,
                                    ControlSource,ControlSink,
                                    is_port)

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
        self.graph.display_info(self.info_text())

    def dehighlight(self, *_):
        canvas = self.canvas
        outline = self['outline']
        canvas.itemconfigure(self['pad'], outline=outline)
        canvas.itemconfigure(self['text'], fill=outline)
        self.graph.clear_info()
 
    def _init_event_bindings(self):
        canvas = self.canvas
        for citem in (self['pad'],self['text']):
            canvas.tag_bind(citem, '<Enter>', self.highlight)
            canvas.tag_bind(citem, '<Leave>', self.dehighlight)
            canvas.tag_bind(citem, '<B1-Motion>', self.drag_token)
            canvas.tag_bind(citem, '<ButtonPress-1>', self.pickup_token)
            canvas.tag_bind(citem, '<ButtonRelease-1>', self.drop_token)
            canvas.tag_bind(citem, '<Double-Button-3>', self.remove_bus)
    
    def info_text(self):
        bus = self.client
        acc = bus.dump(depth=0, silent=True)
        return acc

    def remove_bus(self, event):
        busname = self.client_id()
        if not(self.is_protected()):
            parser = self.app.ls_parser
            parser.rm(busname)
            self.graph.sync()
            self.graph.status("Removed bus '%s'" % busname)
        else:
            self.graph.warning("Can not remove protected bus '%s'" % busname)

    def move_to(self, x, y):
        self._create_construction_points(x,y)
        ppnts = self._construction_points['pad']
        txpnts = self._construction_points['text']
        srcpnts = self._construction_points['source']
        snkpnts = self._construction_points['sink']
        pairs = ((self['pad'],self._construction_points['pad']),
                 (self['text'],self._construction_points['text']),
                 (self['in-port'],self._construction_points['sink']),
                 (self['out-port'],self._construction_points['source']))
        radius = gconfig['port-radius']
        for tag,cpnts in pairs:
            if tag:
                if is_port(tag):
                    xc,yc = cpnts
                    x0,y0 = xc-radius, yc-radius
                    x1,y1 = xc+radius, yc+radius
                    self.canvas.coords(tag['pad'], x0,y0,x1,y1)
                else:
                    self.canvas.coords(tag,*cpnts)

            
class AudiobusToken(BusToken):

    def __init__(self,graph,bus):
        super(AudiobusToken,self).__init__(graph,bus)

    def is_audio_bus(self):
        return True

    def is_protected(self):
        return self.client.is_protected()

    def _create_construction_points(self,x0,y0):
        x0,y0 = float(x0),float(y0)
        x1,y1 = x0+gconfig["audio-bus-width"], y0+gconfig["audio-bus-height"]
        chamfer = gconfig["audio-bus-chamfer"]
        xc = (x0+x1)/2
        yc = (y0+y1)/2
        if self.client.is_hardware_input():
            x2 = x1-chamfer
            pad_points = [x0,y0,x2,y0,x1,yc,x2,y1,x0,y1,x0,y0]
        elif self.client.is_hardware_output():
            x2 = x0 + chamfer
            pad_points = [x0,y0,x1,y0,x1,y1,x0,y1,x2,yc,x0,y0]
        else:
            x2,x3 = x0+chamfer, x1-chamfer
            pad_points = [x0,y0,x3,y0,x1,yc,x3,y1,x0,y1,x2,yc,x0,y0]
        self._construction_points["pad"] = pad_points
        self._construction_points['text'] = [xc,yc]
        self._construction_points['sink'] = [x0,yc]
        self._construction_points['source'] = [x1+4,yc]
  
    def render(self):
        x0,y0 = self.graph.suggest_initial_coords(self)
        canvas = self.canvas
        fill = gconfig["audio-bus-fill"]
        outline = gconfig.audio_bus_color()
        self['outline'] = outline
      
        font = gconfig['bus-name-font']
        self._create_construction_points(x0,y0)
        if self.client.is_hardware_input():
            tags = ('audio-input-bus','audio-bus',self.client_id())
            source = AudioSource(self.graph,self,self._construction_points['source'])
            sink = None
        elif self.client.is_hardware_output():
            tags = ('audio-output-bus','audio-bus',self.client_id())
            source = None
            sink = AudioSink(self.graph,self,self._construction_points['sink'])
        else:
            tags = ('audio-bus', self.client_id())
            source = AudioSource(self.graph,self,self._construction_points['source'])
            sink = AudioSink(self.graph,self,self._construction_points['sink'])
        pad = canvas.create_polygon(self._construction_points['pad'],
                                    tags = tags,
                                    fill = fill,
                                    outline = outline)
        text = canvas.create_text(self._construction_points['text'],
                                  tags = tags,
                                  text = self.client_id(),
                                  fill = outline,
                                  font = font)
        self['pad'] = pad
        self['text'] = text
        self['in-port'] = sink
        self['out-port'] = source
        self['color'] = outline
        self._init_event_bindings()
            
class ControlbusToken(BusToken):

    def __init__(self,graph,bus):
        super(ControlbusToken,self).__init__(graph,bus)

    def is_control_bus(self):
        return True

    def _create_construction_points(self,x0,y0):
        x0,y0 = float(x0),float(y0)
        x1 = x0+gconfig['control-bus-width']
        y1 = y0+gconfig['control-bus-height']
        xc,yc = (x0+x1)/2,(y0+y1)/2
        self._construction_points['pad'] = [x0,y0,x1,y1]
        self._construction_points['text'] = [xc,yc]
        self._construction_points['sink'] = [xc,y1]
        self._construction_points['source'] = [xc,y0]
 
    def render(self):
        x0,y0 = self.graph.suggest_initial_coords(self)
        self._create_construction_points(x0,y0)
        canvas = self.canvas
        if not(self.is_protected()):
            tags = ('control-bus', self.client_id())
            outline = gconfig.control_bus_color()
            self['outline'] = outline
            x0,y0,x1,y1 = self._construction_points['pad']
            pad = canvas.create_oval(x0,y0,x1,y1,
                                     tags=tags,
                                     fill=gconfig['control-bus-fill'],
                                     outline=outline)
            xc,yc = self._construction_points['text']
            txt = canvas.create_text(xc,yc,
                                     tags = tags,
                                     text = self.client_id(),
                                     font = gconfig['bus-name-font'],
                                     fill=outline)
            xk, yk = self._construction_points['sink']
            port_sink = ControlSink(self.graph,self,(xk,yk))
            xr, yr = self._construction_points['source']
            port_source = ControlSource(self.graph,self,(xr,yr))
            self['pad'] = pad
            self['text'] = txt
            self['in-port'] = port_sink
            self['out-port'] = port_source
            self['color'] = outline
            self._init_event_bindings()
        else:
            self['pad'] = None
            self['text'] = None
            self["in-port"] = None
            self["out-port"] = None
            
        
    
