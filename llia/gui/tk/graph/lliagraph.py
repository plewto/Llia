# llia.gui.tk.graph.lliagraph

from Tkinter import Canvas, Frame

from random import randint

from llia.util.lmath import distance
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
        self.synth_tokens = {}  # map [sid] -> SynthToken
        self.audio_bus_tokens = {}    # map [bus-name] -> BusToken
        self.control_bus_tokens = {}
        self.current_token_and_port = None # (token,port) dragdrop source
        self.current_allied_ports = []
        self._drag_data = {'x': 0,
                           'y': 0,
                           'anchor-x' : 0,
                           'anchor-y' : 0,
                           'port1' : None,
                           #'port2' : None,
                           'rubberband' : None}
        canvas.bind("<B1-Motion>", self.bus_drag)
        canvas.bind("<ButtonPress-1>", self.bus_drag_pickup)
        canvas.bind("<ButtonRelease-1>", self.bus_drop)


    def clear_drag_and_drop(self):
        self.current_token_and_port = None
        self._drag_data['port1'] = None
        rb = self._drag_data['rubberband']
        if rb: self.canvas.delete(rb)
        self._drag_data['rubberband'] = None
        self.status("")
            
        
    # bus drag, drop and connect functions

    def bus_drag_pickup(self, event):
        if self.current_token_and_port:
            x,y = event.x, event.y
            rubber = self.canvas.create_line(x,y,x,y,
                                             fill = gconfig['rubberband-fill'],
                                             dash = gconfig['rubberband-dash'],
                                             tags = "rubberband")
            self._drag_data['port1'] = self.current_token_and_port
            self._drag_data['x'] = x
            self._drag_data['y'] = y
            self._drag_data['anchor-x'] = x
            self._drag_data['anchor-y'] = y
            self._drag_data['rubberband'] = rubber
            self.status(self.current_token_and_port)

    def bus_drag(self, event):
        rubber = self._drag_data['rubberband']
        if rubber:
            x0,y0 = self._drag_data['anchor-x'], self._drag_data['anchor-y']
            x1,y1 = event.x, event.y
            self.canvas.delete("rubberband")
            rubber = self.canvas.create_line(x0,y0,x1,y1,
                                             fill = gconfig["rubberband-fill"],
                                             dash = gconfig["rubberband-dash"],
                                             tags = "rubberband")
            self._drag_data['x'] = x1
            self._drag_data['y'] = y1
            self._drag_data['rubberband'] = rubber
            for tkn,prt in self.current_allied_ports:
                try:
                    self.canvas.itemconfig(prt['pad'],
                                           fill = gconfig['allied-port-highlight'])
                except TypeError:
                    pass

    def bus_drop(self, event):
        self.canvas.delete("rubberband")
        for tkn,prt in self.current_allied_ports:
            try:
                c = prt['fill']
                self.canvas.itemconfig(prt['pad'], fill=c)
            except TypeError:
                pass
        prt1 = self._drag_data['port1']
        if prt1:
            if prt1[0].is_synth():
                self._locate_drop_destination_bus(event,prt1)
            else:
                self._locate_drop_destination_synth(event,prt1)

    def _locate_drop_destination_bus(self, event, prt1):
        # Used when drag operation begins with synth port
        x,y = event.x, event.y
        target = None
        min_distance = 1e6
        for tkn,prt in self.current_allied_ports:
            try:
                pos = self.canvas.coords(prt['pad'])
                xc,yc = (pos[0]+pos[2])/2, (pos[1]+pos[3])/2
                d = distance(x,y,xc,yc)
                if d < min_distance:
                    min_distance = d
                    target = tkn,prt
            except TypeError:
                pass
        if min_distance < gconfig["drop-threshold"]:
            tkn1, port1 = self.current_token_and_port
            sid, param = tkn1.client_id(), port1.param
            busname = target[0].client_id()
            shelper = self.app.ls_parser.synthhelper
            if port1.is_audio():
                if port1.is_source():
                    shelper.assign_audio_output_bus(param,busname,sid)
                else:
                    shelper.assign_audio_input_bus(param,busname,sid)
            else:
                print("DEBUG CONTORL port")
                if port1.is_source():
                    pass
                else:
                    pass
        else:
            msg = "No Drag n Drop target located"
            self.warning(msg)
        self.clear_drag_and_drop()
        self.sync()
        

    def _locate_drop_destination_synth(self, event, prt1):
        # Used when drag operation begins from bus
        x,y = event.x, event.y
        target = None
        min_distance = 1e6
        for tkn,prt in self.current_allied_ports:
            try:
                pos = self.canvas.coords(prt['pad'])
                xc,yc = (pos[0]+pos[2])/2, (pos[1]+pos[3])/2
                d = distance(x,y,xc,yc)
                if d < min_distance:
                    min_distance = d
                    target = tkn,prt
            except TypeError:
                pass
        if min_distance < gconfig["drop-threshold"]:
            tkn1,port1 = self.current_token_and_port
            busname = tkn1.client_id()
            shelper = self.app.ls_parser.synthhelper
            sid,param = target[0].client_id(), target[1].param
            if port1.is_audio():
                if port1.is_source():
                    shelper.assign_audio_input_bus(param,busname,sid)
                else:
                    shelper.assign_audio_output_bus(param,busname,sid)
            else:
                print("DEBUG A control bus then")
        self.clear_drag_and_drop()
        self.sync()
                
            
        
        
    def status(self, msg):
        self.app.main_window().status(msg)

    def warning(self, msg):
        self.app.main_window().warning(msg)

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

    def collect_garbage(self):
        for sid,tkn in self.synth_tokens.items():
            if not(self.proxy.synth_exists(None, None, sid)):
                self.synth_tokens.pop(sid)
                self.canvas.delete(sid)
        for bname,tkn in self.audio_bus_tokens.items():
            if not(self.proxy.bus_exists(bname)):
                self.audio_bus_tokens.pop(bname)
                self._canvas.delete(bname)
        for bname,tkn in self.control_bus_tokens.items():
            if not(self.proxy.bus_exists(bname)):
                self.control_bus_tokens.pop(bname)
                self._canvas.delete(bname)

    def sync(self, *_):
        self.collect_garbage()
        # Add new synths
        for sy in self.proxy.get_all_synths():
            sid = sy.sid
            specs = sy.specs
            if not(self.synth_tokens.has_key(sid)):
                if specs["is-controller"]:
                    tkn = ControllerToken(self,sy)
                elif specs["is-efx"]:
                    tkn = EfxToken(self,sy)
                else:
                    tkn = SynthToken(self,sy)
                self.synth_tokens[sid] = tkn
                tkn.render()
        # Add new audio buses
        for bname in self.proxy.audio_bus_names():
            if not(self.audio_bus_tokens.has_key(bname)):
                bobj = self.proxy.get_audio_bus(bname)
                btoken = AudiobusToken(self,bobj)
                self.audio_bus_tokens[bname] = btoken
                btoken.render()
        # Add new control buses
        for bname in self.proxy.control_bus_names():
            if not(self.control_bus_tokens.has_key(bname)):
                bobj = self.proxy.get_control_bus(bname)
                btoken = ControlbusToken(self,bobj)
                self.control_bus_tokens[bname] = btoken
                btoken.render()

        canvas = self.canvas
        canvas.delete('path')
        y_input_offset = gconfig["audio-bus-height"]/2
        for bname, tkn in self.audio_bus_tokens.items():
            busobj = tkn.client
            x0,y0 = canvas.coords(tkn['pad'])[:2]
            xin, yin = x0,y0+y_input_offset
            for bsrc in busobj.sources():
                sid,param = bsrc.sid,bsrc.param
                sytoken = self.synth_tokens[sid]
                port_offset = sytoken.audio_output_ports[param][2]
                xtk,ytk = canvas.coords(sytoken['pad'])[:2]
                xout,yout = xtk+port_offset[0],ytk+port_offset[1]
                canvas.create_line(xin,yin,xout,yout,
                                   fill=tkn['color'],
                                   tags = (bname, sid, "path", "audio-path"))
            xout, yout = x0+gconfig["audio-bus-width"],y0+y_input_offset
            for bsink in busobj.sinks():
                sid,param = bsink.sid,bsink.param
                sytoken = self.synth_tokens[sid]
                port_offset = sytoken.audio_input_ports[param][2]
                xtk,ytk = canvas.coords(sytoken['pad'])[:2]
                xin,yin = xtk+port_offset[0],ytk+port_offset[1]
                canvas.create_line(xin,yin,xout,yout,
                                   fill=tkn['color'],
                                   tags = (bname,sid,"path","audio-path"))
                
        height = gconfig["control-bus-height"]
        width = gconfig["control-bus-width"]
        for bname,tkn in self.control_bus_tokens.items():
            if not(tkn.is_protected()):
                busobj = tkn.client
                x0,y0 = canvas.coords(tkn['pad'])[:2]
                xin = x0+width/2
                yin = y0+height
                dash = gconfig["control-path-dash"]
                lwidth = gconfig["control-path-width"]
                for bsrc in busobj.sources():
                    sid,param = bsrc.sid,bsrc.param
                    sytoken = self.synth_tokens[sid]
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
                    sytoken = self.synth_tokens[sid]
                    port_offset = sytoken.control_input_ports[param][2]
                    xtk,ytk = canvas.coords(sytoken['pad'])[:2]
                    xin,yin = xtk+port_offset[0],ytk+port_offset[1]
                    canvas.create_line(xin,yin,xout,yout,
                                       fill=tkn['color'],
                                       dash=dash,
                                       width=lwidth,
                                       tags = (bname,sid,"path","control-path"))
        canvas.lower("path")

    
