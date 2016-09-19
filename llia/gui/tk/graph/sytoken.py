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
        self.audio_input_ports = {}    # map synth param to tuple
        self.audio_output_ports = {}   # (param, Port, (x, y)).
        self.control_input_ports = {}  # Where x and y are relative to
        self.control_output_ports = {} # x0,y0.

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
            self.audio_output_ports[param] = t
        ainparams = self.client.available_audio_input_parameters()
        for i,param in enumerate(ainparams):
            x = 0
            y = spacing*(i+1)
            rel_position = x,y
            abs_position = x0+rel_position[0], y0+rel_position[1]
            port = AudioSink(self.graph, self, abs_position, param)
            t = (param, port, rel_position)
            self.audio_input_ports[param] = t
        coutparams = self.client.available_control_output_parameters()
        for i,param in enumerate(coutparams):
            x = spacing*(i+1)
            y = 0
            rel_position = x,y
            abs_position = x0+rel_position[0], y0+rel_position[1]
            port = ControlSource(self.graph, self, abs_position, param)
            t = (param, port, rel_position)
            self.control_output_ports[param] = t
        cinparams = self.client.available_control_input_parameters()
        for i,param in enumerate(cinparams):
            x = spacing*(i+1)
            y = gconfig['synth-node-height']
            rel_position = x,y
            abs_position = x0+rel_position[0], y0+rel_position[1]
            port = ControlSink(self.graph, self, abs_position, param)
            t = (param, port, rel_position)
            self.control_input_ports[param] = t
        self['pad'] = pad
        self['image'] = img
        canvas.tag_bind(self['image'], '<Enter>', self.highlight)
        canvas.tag_bind(self['image'], '<Leave>', self.dehighlight)
        canvas.tag_bind(self['image'], '<B1-Motion>', self.drag_token)
        canvas.tag_bind(self['image'], '<ButtonPress-1>', self.pickup_token)
        canvas.tag_bind(self['image'], '<ButtonRelease-1>', self.drop_token)
        canvas.tag_bind(self['image'], '<Double-Button-1>', self.show_editor)
        canvas.tag_bind(self['image'], '<Double-Button-3>', self.delete_synth)

    def show_editor(self, event):
        sy = self.client
        sid = sy.sid
        sed = sy.synth_editor
        grpid = sed.group_index
        grp = self.app.main_window().group_windows[grpid]
        grp.show_synth_editor(sid)

    def delete_synth(self, event):
        sy = self.client
        sid = sy.sid
        parser = self.app.ls_parser
        shelper = parser.synthhelper
        shelper.destroy_editor(sid)
        parser.rm(sid, force=True)
        self.graph.sync()
        self.graph.status("Synth '%s' removed" % sid)
        
        
        
    
    def highlight(self, *_):
        canvas = self.canvas
        highlight = gconfig['highlight-color'] 
        canvas.itemconfig(self['pad'],
                          fill = highlight,
                          outline = highlight)
        self.graph.display_info(self.info_text())

    def dehighlight(self, *_):
        canvas = self.canvas
        fill = gconfig['synth-fill']
        outline = gconfig['synth-outline']
        canvas.itemconfig(self['pad'],
                          fill = fill,
                          outline = outline)

    def info_text(self,head="Synth"):
        sy = self.client
        specs = sy.specs
        acc = "%s %s\n" % (head, self.client_id())
        pad = ' '*4
        aip = sy.available_audio_input_parameters()
        if aip:
            acc += "Audio inputs:\n"
            for p in aip:
                bname = sy.get_audio_input_bus(p)
                acc += '%s%-12s <-- %s\n' % (pad,p,bname)
        aop = sy.available_audio_output_parameters()
        if aop:
            acc += "Audio outputs:\n"
            for p in aop:
                bname = sy.get_audio_output_bus(p)
                acc += '%s%-12s --> %s\n' % (pad,p,bname)
        cip = sy.available_control_input_parameters()
        if cip:
            acc += "Control inputs:\n"
            for p in cip:
                bname = sy.get_control_input_bus(p)
                acc += '%s%-12s <-- %s\n' % (pad,p,bname)
        cop = sy.available_control_output_parameters()
        if cop:
            acc += "Control outputs:\n"
            for p in cop:
                bname = sy.get_control_output_bus(p)
                acc += '%s%-12s --> %s\n' % (pad,p,bname)
        return acc

                  
class EfxToken(SynthToken):

    def __init__(self,graph,synth):
        super(EfxToken,self).__init__(graph,synth)

    def is_efx(self):
        return True
        
    def info_text(self):
        return super(EfxToken, self).info_text("Effect")

    
class ControllerToken(SynthToken):

    def __init__(self,graph,synth):
        super(ControllerToken,self).__init__(graph,synth)

    def is_efx(self):
        return True
        
    def is_controller(self):
        return True

    def info_text(self):
        return super(ControllerToken, self).info_text("Controller")
