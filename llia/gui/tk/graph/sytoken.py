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
        self._position = [-1,-1]

    def client_id(self):
        return self.client.sid

    def synth_serial_number(self):
        sid = self.client_id()
        a,b = sid.split("_")
        return int(b)
    
    def is_synth(self):
        return True

    def bbox(self):
        x0,y0,x1,y1 = self.canvas.coords(self['pad'])[:4]
        return x0,y0,x1,y1

    def _create_construction_points(self,x0,y0):
        x0,y0 = float(x0),float(y0)
        self._position = [x0,y0]
        x1 = x0+gconfig['synth-node-width']
        y1 = y0+gconfig['synth-node-height']
        xi = x0+gconfig['synth-node-image-padding']
        yi = y0+gconfig['synth-node-image-padding']
        self._construction_points['pad'] = [x0,y0,x1,y1]
        self._construction_points['image'] = [xi,yi]
        aout,ain,cout,cin = {},{},{},{}
        self._construction_points['aout'] = aout
        self._construction_points['ain'] = ain
        self._construction_points['cout'] = cout
        self._construction_points['cin'] = cin
        spacing = int(gconfig['port-radius'] * 2)
        aoutparams = self.client.available_audio_output_parameters()
        for i,param in enumerate(aoutparams):
             x = gconfig['synth-node-width']
             y = spacing*(i+1)
             rel_position = x,y
             abs_position = x0+rel_position[0], y0+rel_position[1]
             aout[param] = abs_position,rel_position
        ainparams = self.client.available_audio_input_parameters()
        for i,param in enumerate(ainparams):
            x = 0
            y = spacing*(i+1)
            rel_position = x,y
            abs_position = x0+rel_position[0], y0+rel_position[1]
            ain[param] = abs_position,rel_position
        coutparams = self.client.available_control_output_parameters()
        for i,param in enumerate(coutparams):
            x = spacing*(i+1)
            y = 0
            rel_position = x,y
            abs_position = x0+rel_position[0], y0+rel_position[1]
            cout[param] = abs_position,rel_position
        cinparams = self.client.available_control_input_parameters()
        for i,param in enumerate(cinparams):
            x = spacing*(i+1)
            y = gconfig['synth-node-height']
            rel_position = x,y
            abs_position = x0+rel_position[0], y0+rel_position[1]
            cin[param] = abs_position,rel_position

    def render(self):
        x0,y0 = self.graph.suggest_initial_coords(self)
        self._create_construction_points(x0,y0)
        canvas = self.canvas
        xp0,yp0,xp1,yp1 = self._construction_points['pad']
        pad = canvas.create_rectangle(xp0,yp0,xp1,yp1,
                                      tags=('synth','pad',self.client_id()),
                                      fill=gconfig['synth-fill'],
                                      outline=gconfig['synth-outline'])
        xi,yi = self._construction_points['image']
        img = canvas.create_image(xi,yi,
                                  tags=('synth','logo',self.client_id()),
                                  image = get_logo_image(self.client),
                                  anchor='nw')
        aoutparams = self.client.available_audio_output_parameters()
        ainparams = self.client.available_audio_input_parameters()
        coutparams = self.client.available_control_output_parameters()
        cinparams = self.client.available_control_input_parameters()
        for i, param in enumerate(aoutparams):
            abs_pos, rel_pos = self._construction_points['aout'][param]
            port = AudioSource(self.graph,self,abs_pos,param)
            t = (param,port,rel_pos)
            self.audio_output_ports[param] = t
        for i, param in enumerate(ainparams):
            abs_pos, rel_pos = self._construction_points['ain'][param]
            port = AudioSink(self.graph,self,abs_pos,param)
            t = (param,port,rel_pos)
            self.audio_input_ports[param] = t

        for i, param in enumerate(coutparams):
            abs_pos, rel_pos = self._construction_points['cout'][param]
            port = ControlSource(self.graph,self,abs_pos,param)
            t = (param,port,rel_pos)
            self.control_output_ports[param] = t
        for i, param in enumerate(cinparams):
            abs_pos, rel_pos = self._construction_points['cin'][param]
            port = ControlSink(self.graph,self,abs_pos,param)
            t = (param,port,rel_pos)
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

    def move_to(self, x, y):
        radius = gconfig['port-radius']
        self._create_construction_points(x,y)
        ppnts = self._construction_points['pad']
        imgpnts = self._construction_points['image']
        aout = self._construction_points['aout']
        ain = self._construction_points['ain']
        cout = self._construction_points['cout']
        cin = self._construction_points['cin']
        self.canvas.coords(self['pad'],*ppnts)
        self.canvas.coords(self['image'],*imgpnts)
        for aip in self.audio_input_ports.values():
            param,port,junk = aip
            tag=port['pad']
            xc,yc = self._construction_points['ain'][param][0]
            x0,y0 = xc-radius, yc-radius
            x1,y1 = xc+radius, yc+radius
            self.canvas.coords(tag,x0,y0,x1,y1)
        for aop in self.audio_output_ports.values():
            param,port,junk = aop
            tag=port['pad']
            xc,yc = self._construction_points['aout'][param][0]
            x0,y0 = xc-radius, yc-radius
            x1,y1 = xc+radius, yc+radius
            self.canvas.coords(tag,x0,y0,x1,y1)
        for cip in self.control_input_ports.values():
            param,port,junk = cip
            tag=port['pad']
            xc,yc = self._construction_points['cin'][param][0]
            x0,y0 = xc-radius, yc-radius
            x1,y1 = xc+radius, yc+radius
            self.canvas.coords(tag,x0,y0,x1,y1)
        for cop in self.control_output_ports.values():
            param,port,junk = cop
            tag=port['pad']
            xc,yc = self._construction_points['cout'][param][0]
            x0,y0 = xc-radius, yc-radius
            x1,y1 = xc+radius, yc+radius
            self.canvas.coords(tag,x0,y0,x1,y1)

    def position(self):
        return self._position
        
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
