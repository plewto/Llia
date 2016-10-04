# llia.gui.tk.graph.lliagraph

from Tkinter import Canvas, Frame

from random import randint

from llia.util.lmath import distance
import llia.gui.tk.tk_factory as factory
from llia.gui.tk.graph.gconfig import gconfig
from llia.gui.tk.graph.sytoken import SynthToken, EfxToken, ControllerToken
from llia.gui.tk.graph.bustoken import AudiobusToken, ControlbusToken
from llia.gui.tk.graph.infocanvas import InfoCanvas

BUS_WARNING = '''
Effects must be connected in the correct order.
Newer synths may not process previous synths.
'''



class LliaGraph(Frame):

    control_bus_counter = 0
    audio_bus_counter = 0
    
    
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
        info_canvas.grid(row=0,column=0,rowspan=1,columnspan=1, sticky='wns')
        canvas.grid(row=0,column=1,rowspan=1,columnspan=1, sticky='nsew')
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        # toolbar buttons
        def tbutton(col, text, command=None):
            bwidth=75
            b = factory.button(self.canvas, text,command=command)
            y0 = 15
            x0 = 15
            x = x0+col*bwidth
            b.place(x=x,y=y0,width=bwidth)
            
        tbutton(0, 'sync', self.sync)
        tbutton(1, '+Audio', self.add_audio_bus)
        tbutton(2, "+Control", self.add_control_bus)
        tbutton(3, "Allign", self.allign_tokens)
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

    def add_audio_bus(self):
        parser = self.app.ls_parser
        while True:
            bname = "A%d" % LliaGraph.audio_bus_counter
            w = parser.what_is(bname)
            if not w:
                parser.abus(bname)
                self.status("Added audio bus '%s'" % bname)
                break
            LliaGraph.audio_bus_counter += 1
        self.sync()

    def add_control_bus(self):
        parser = self.app.ls_parser
        while True:
            bname = "C%d" % LliaGraph.control_bus_counter
            w = parser.what_is(bname)
            if not w:
                parser.cbus(bname)
                self.status("Added contol bus '%s'" % bname)
                break
            LliaGraph.control_bus_counter += 1
        self.sync()

  
    def _allign_audio_synths(self):
        acc, bcc = [], []
        for t in self.synth_tokens.values():
            if t.is_controller():
                bcc.append(t)
            else:
                acc.append(t)
        acc.sort(key=lambda x: x.synth_serial_number())
        bcc.sort(key=lambda x: x.synth_serial_number()) # Used only as function return
        x = x0 = 850
        xdelta = 200
        y = 0
        ydelta = 100
        tokens_per_line = 4
        token_counter = 0
        line_counter = 0
        for i,token in enumerate(acc):
            if token_counter == 0:
                token_counter = tokens_per_line
                line_counter += 1
                xstagger = (line_counter%2)*(xdelta/2)
                x = x0 - xstagger
                y += ydelta
            token.move_to(x,y)
            x -= xdelta
            token_counter -= 1
        return acc,bcc

    def _allign_audio_buses(self, synth_tokens):
        for ab in self.audio_bus_tokens.values():
            ab.move_to(-100, 0)
            ab.off_screen = True
        # Allign synth output buses
        for st in synth_tokens:
            sid = st.client_id()
            bus_counter = 0
            for aport in st.audio_output_ports.values():
                param,port,junk = aport
                for abtoken in self.audio_bus_tokens.values():
                    abus = abtoken.client
                    if abtoken.off_screen and abus.has_source(sid,param):
                        x,y = st.position()
                        y = y + bus_counter*32
                        abtoken.move_to(x+100,y)
                        abtoken.off_screen = False
                        bus_counter += 1
        # Park remaining audio buses
        input_bus_counter = 0
        output_bus_counter = 0
        general_bus_counter = 0
        xin, xgeneral, xout = 30, 120, 210
        y0, ydelta = 300, 40
        for atoken in self.audio_bus_tokens.values():
            if atoken.off_screen:
                cid = atoken.client_id()
                atoken.off_screen = False
                if cid.startswith("in_"):
                    x = xin
                    y = y0 + ydelta * input_bus_counter
                    input_bus_counter += 1
                elif cid.startswith("out_"):
                    x = xout
                    y = y0 + ydelta * output_bus_counter
                    output_bus_counter += 1
                else:
                    x = xgeneral
                    y = y0 + ydelta * general_bus_counter
                    general_bus_counter += 1
                atoken.move_to(x,y)
                        
    def _allign_controller_synths(self, controller_tokens):
        x = x0 = 850
        xdelta = 96
        y = 300
        ydelta = 150
        tokens_per_line = 6
        token_counter = 0
        line_counter = 0
        for i,token in enumerate(controller_tokens):
            if token_counter == 0:
                line_counter += 1
                xstagger = (line_counter%2)*(xdelta/4)
                x = x0+xstagger
                y += ydelta
                token_counter = tokens_per_line
            token.move_to(x,y)
            x -= xdelta
            token_counter -= 1
        
    def _allign_control_buses(self, controller_tokens):
        for cb in self.control_bus_tokens.values():
            cb.move_to(-100,0)
            cb.off_screen = True
        for st in controller_tokens:
            sid = st.client_id()
            bus_counter = 0
            for cport in st.control_output_ports.values():
                param,port,junk = cport
                for cbtoken in self.control_bus_tokens.values():
                    cbus = cbtoken.client
                    if cbtoken.off_screen and cbus.has_source(sid,param):
                        x,y = st.position()
                        x += bus_counter*32
                        cbtoken.move_to(x,y-64)
                        cbtoken.off_screen = False
                        bus_counter += 1
        # Park remaining control buses
        x,y = x0,y0 = 300,300
        ydelta = 40
        for ctoken in self.control_bus_tokens.values():
            if ctoken.off_screen:
                ctoken.off_screen = False
                ctoken.move_to(x,y)
                y += ydelta
                

                
        

    
    def allign_tokens(self):
        self.canvas.delete('path')
        synth_tokens, controller_tokens = self._allign_audio_synths()
        self._allign_audio_buses(synth_tokens)
        self._allign_controller_synths(controller_tokens)
        self._allign_control_buses(controller_tokens)
        self.sync()
        
    def _show_bus_warning(self):
        self.info_canvas.display_warning(BUS_WARNING)

    def _clear_bus_warning(self):
        self.info_canvas.clear_warning()
        
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
            self._show_bus_warning()
            

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
        self._clear_bus_warning()

                
    def _locate_drop_destination_bus(self, event, prt1):
        # For use when drag operation begins with synth port
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
                if port1.is_source():
                    shelper.assign_control_output_bus(param,busname,sid)
                else:
                    shelper.assign_control_input_bus(param,busname,sid)
        else:
            msg = "No Drag n Drop target located"
            self.warning(msg)
        self.clear_drag_and_drop()
        self.sync()
        

    def _locate_drop_destination_synth(self, event, prt1):
        # For use when drag operation begins from bus
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
                if port1.is_source():
                    shelper.assign_control_input_bus(param,busname,sid)
                else:
                    shelper.assign_control_output_bus(param,busname,sid)
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
                self.canvas.delete(bname)
        for bname,tkn in self.control_bus_tokens.items():
            if not(self.proxy.bus_exists(bname)):
                self.control_bus_tokens.pop(bname)
                self.canvas.delete(bname)

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

    
