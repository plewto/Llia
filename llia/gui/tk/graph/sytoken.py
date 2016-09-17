# llia.gui.tk.graph.sytoken

from llia.gui.tk.graph.token import Token, get_logo_image
from llia.gui.tk.graph.gconfig import gconfig
from llia.gui.tk.graph.port import (AudioSource,AudioSink,
                                    ControlSource,ControlSink)

class SynthToken(Token):

    def __init__(self,graph,synth):
        super(SynthToken,self).__init__(graph,synth)
        self["width"] = 0
        self["height"] = 0
        self["pad"] = None
        self["image"] = None
        self._audio_input_ports = {}    # map synth param to tuple
        self._audio_output_ports = {}   # (param, Port, (x, y)).
        self._control_input_ports = {}  # Where x and y are relative to
        self._control_output_ports = {} # x0,y0.
                                        

    def client_id(self):
        return self.client.sid

    def is_synth(self):
        return True

    def bbox(self):
        x0,y0,x1,y1 = self.canvas.coords(self['pad'])[:4]
        return x0,y0,x1,y1
                                    
    def render(self):
        x0,y0 = self.graph.suggest_initial_coords(self)
        x1 = x0+gconfig['synth-node-width'],
        y1 = y0+gconfig['synth-node-height']
        canvas = self.canvas
        pad = canvas.create_rectangle(x0,y0,x1,y1,
                                      tags=('synth','pad',self.client_id()),
                                      fill=gconfig['synth-fill'],
                                      outline=gconfig['synth-outline'],)
        xi = x0+gconfig['synth-node-image-padding']
        yi = y0+gconfig['synth-node-image-padding']
        img = canvas.create_image(xi,yi,
                                  tags=('synth','logo',self.client_id()),
                                  image = get_logo_image(self.client),
                                  anchor='nw')
        spacing = int(gconfig['port-radius'] * 2)
        aoutparams = self.client.available_audio_output_parameters()
        for i,param in enumerate(aoutparams):
            x = gconfig['synth-node-width']
            y = spacing*(i+1)
            rel_position = x,y
            abs_position = x0+rel_position[0], y0+rel_position[1]
            port = AudioSource(self.graph, self, abs_position, param)
            t = (param, port, rel_position)
            self._audio_output_ports[param] = t
        ainparams = self.client.available_audio_input_parameters()
        for i,param in enumerate(ainparams):
            x = 0
            y = spacing*(i+1)
            rel_position = x,y
            abs_position = x0+rel_position[0], y0+rel_position[1]
            port = AudioSink(self.graph, self, abs_position, param)
            t = (param, port, rel_position)
            self._audio_input_ports[param] = t
        coutparams = self.client.available_control_output_parameters()
        for i,param in enumerate(coutparams):
            x = spacing*(i+1)
            y = 0
            rel_position = x,y
            abs_position = x0+rel_position[0], y0+rel_position[1]
            port = ControlSource(self.graph, self, abs_position, param)
            t = (param, port, rel_position)
            self._control_output_ports[param] = t
        cinparams = self.client.available_control_input_parameters()
        for i,param in enumerate(cinparams):
            x = spacing*(i+1)
            y = gconfig['synth-node-height']
            rel_position = x,y
            abs_position = x0+rel_position[0], y0+rel_position[1]
            port = ControlSink(self.graph, self, abs_position, param)
            t = (param, port, rel_position)
            self._control_input_ports[param] = t
        self['pad'] = pad
        self['image'] = img
        canvas.tag_bind(self['image'], '<Enter>', self.highlight)
        canvas.tag_bind(self['image'], '<Leave>', self.dehighlight)
        
            
    def highlight(self, *_):
        canvas = self.canvas
        highlight = gconfig['highlight-color'] 
        canvas.itemconfig(self['pad'],
                          fill = highlight,
                          outline = highlight)

    def dehighlight(self, *_):
        canvas = self.canvas
        fill = gconfig['synth-fill']
        outline = gconfig['synth-outline']
        canvas.itemconfig(self['pad'],
                          fill = fill,
                          outline = outline)
            
        
class EfxToken(SynthToken):

    def __init__(self,graph,synth):
        super(EfxToken,self).__init__(graph,synth)

    def is_efx(self):
        return True
        
        
class ControllerToken(SynthToken):

    def __init__(self,graph,synth):
        super(ControllerToken,self).__init__(graph,synth)

    def is_efx(self):
        return True
        
    def is_controller(self):
        return True
