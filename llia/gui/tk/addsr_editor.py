# llia.gui.tk.addsr_editor
#
# Defines graphics editor for ADDSR style envelope
#

from __future__ import print_function
from llia.generic import is_synth_control
from llia.locked_dictionary import LockedDictionary
from llia.gui.tk.msb import MSB, ToggleButton

template = {'padx' : 16,
            'pady' : 64,
            'padTop' : 16,
            'fill' : 'black',
            'outline' : 'gray',
            'outline-width' : 1,
            'axis-fill' : 'gray',
            'axis-width' : 1,
            'point-radius' : 8,
            'point-fill' : '',
            'point-outline' : 'red',
            'point-activefill' : 'yellow',
            'point-activeoutline' : 'yellow',
            'segment-fill' : 'green',
            'segment-activefill' : '',
            'sustain-duration' : 10,   # in seconds
            'sustain-dash' : (4,4),
            'text-color' : 'gray',
            'font' : ('Times', 10)}

class EnvEditorSpecs(LockedDictionary):

    def __init__(self):
        super(EnvEditorSpecs, self).__init__(template)
        
            
class ADDSREditor(EnvEditorSpecs):

    clipboard = {'attack' : 0.0,
                 'decay1' : 0.0,
                 'decay2' : 0.0,
                 'release' : 0.0,
                 'breakpoint' : 1.0,
                 'sustain' : 1.0,
                 'gate-mode' : 0}
    
    def __init__(self, canvas, envid, position, size, paramlist, parent_editor,
                 max_segment_time=12):
        '''
        Creates new instance of ADDSREditor
        
        ARGS:
           
           canvas    - a Tk Canvas
           envid     - int, a envelope id.
                       Each envelope editor on the same canvas MUST 
                       have a unique id.
           position  - tuple (x,y) location on canvas to place editor
           size      - tuple (w,h)
           paramlist - list of synth parameters 
                       (attack, decay1, decay2, release, 
                        breakpoint, sustain, gate-mode) 
           parent_editor - TkSubEditor
        '''
        EnvEditorSpecs.__init__(self)
        self.envid = envid
        self.canvas = canvas
        self.parent = parent_editor
        self.synth = parent_editor.synth
        self.bank = self.synth.bank()
        self.zoom = 1
        self.max_segment_time = max_segment_time
        self.paramlist = paramlist
        self.params = {'attack' : paramlist[0],
                       'decay1' : paramlist[1],
                       'decay2' : paramlist[2],
                       'release' : paramlist[3],
                       'breakpoint' : paramlist[4],
                       'sustain' : paramlist[5],
                       'gate-mode' : paramlist[6]}
        x0,y0 = position 
        x1,y1 = x0+size[0],y0+size[1]
        padx,pady,padTop = self['padx'], self['pady'], self['padTop']
        xi0,xi1 = x0+padx,x1-padx # internal x
        deltax = float(xi1-xi0)
        maxtime = self['sustain-duration']+4*max_segment_time
        self.xscale = deltax/maxtime
        self.xorigin = xi0
        yi0,yi1 = y0+padTop,y1-pady # internal y
        deltay = yi1-yi0
        self.yscale = -float(deltay)
        self.yorigin = yi1
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.xi0 = xi0
        self.xi1 = xi1
        self.yi0 = yi0
        self.yi1 = yi1
        # static elements
        canvas.create_rectangle(x0,y0,x1,y1,
                                fill=self['fill'],
                                outline=self['outline'],
                                width=self['outline-width'],
                                tags=('pad', 'static'))
        canvas.create_line(xi0,yi1,xi1,yi1,
                           fill=self['axis-fill'],
                           width=self['axis-width'],
                           tags=('x-axis','axis','static'))
        canvas.create_line(xi0,yi1,xi0,yi0,
                            fill=self['axis-fill'],
                            width=self['axis-width'],
                            tags=('y-axis','axis','static'))
        # dynamic elements
        self.segments = []
        for i,name in enumerate(('attack','decay1','decay2',
                                 'sustain','release')):
            p = canvas.create_line(xi0,yi0,xi1,yi1,
                                   fill=self['segment-fill'],
                                   activefill = self['segment-activefill'],
                                   tags = ("env%s-%s" % (self.envid, name),
                                           "env%s-segment-%s" % (self.envid, i),
                                           "segment"))
            self.segments.append(p)
        canvas.itemconfig('sustain', dash=self['sustain-dash'])
        self.points = []
        for i in range(6):
            p = canvas.create_oval(xi0,yi0,xi1,yi1,
                                   fill=self['point-fill'],
                                   activefill = self['point-activefill'],
                                   outline=self['point-outline'],
                                   activeoutline=self['point-activeoutline'],
                                   tags = ("env%s-point-%s" % (self.envid, i),
                                           'point', 'dynamic'))
            self.points.append(p)
        self.canvas.tag_bind("env%s-point-1" % self.envid, "<B1-Motion>",self.attack_drag)
        self.canvas.tag_bind("env%s-point-2" % self.envid, "<B1-Motion>",self.decay1_drag)
        self.canvas.tag_bind("env%s-point-3" % self.envid, "<B1-Motion>",self.decay2_drag)
        self.canvas.tag_bind("env%s-point-4" % self.envid, "<B1-Motion>",self.sustain_drag)
        self.canvas.tag_bind("env%s-point-5" % self.envid, "<B1-Motion>",self.release_drag)
        self._init_zoom_button()
        self._init_gate_button()
        self._init_init_button()
        self._init_copy_button()
        self._init_paste_button()

    def _msb_aspect(self, text, extras={}):
        d = {
            'text' : text,
            'font' : ('Times', 12),
            'fill' : self['fill'],
            'outline' : self['outline'],
            'active-outline' : self['point-activefill'],
            'foreground' : self['text-color'],
            'active-foreground' : self['point-activefill']}
        for k,v in extras.items(): d[k] = v
        return d
        
    def _init_zoom_button(self):
        msb = MSB(self.canvas, "", None, 3)
        a0 = self._msb_aspect("X1")
        a1 = self._msb_aspect("X10")
        a2 = self._msb_aspect("X100")
        msb.define_aspect(0, 1, a0)
        msb.define_aspect(1, 10, a1)
        msb.define_aspect(2, 100, a2)
        x, y = self.xi0 + 256, self.y1-50
        msb.layout((x,y))
        msb.value(1)
        msb.update_aspect()
        def zoom_callback(*_):
            self.zoom = msb.value()
            self.sync_ui()
        msb.client_callback = zoom_callback
        
    # def _init_gate_button(self):
    #     msb = MSB(self.canvas, self.params['gate-mode'], self.parent, 2)
    #     a0 = self._msb_aspect("GATE")
    #     a1 = self._msb_aspect("TRIG", {"foreground" : "green"})
    #     msb.define_aspect(0, 0, a0)
    #     msb.define_aspect(1, 1, a1)
    #     x, y = self.xi0, self.y1-50
    #     msb.layout((x,y))
    #     msb.update_aspect()
    #     self.msb_gate_mode = msb

    def _init_gate_button(self):
        msb = ToggleButton(self.canvas, self.params['gate-mode'],
                           self.parent,
                           text=["Gate", "Trig"],
                           values=[0,1])
        x, y = self.xi0, self.y1-50
        msb.layout((x,y))
        msb.update_aspect()
        self.msb_gate_mode = msb
    
            
    def _init_init_button(self):
        msb = MSB(self.canvas, '', None, 1)
        a0 = self._msb_aspect("Init")
        msb.define_aspect(0,0,a0)
        x,y = self.xi0+64, self.y1-50
        msb.layout((x,y))
        msb.update_aspect()
        def init_callback(*_):
            self.set_synth_value(self.params['attack'], 0.0)
            self.set_synth_value(self.params['decay1'], 0.0)
            self.set_synth_value(self.params['decay2'], 0.0)
            self.set_synth_value(self.params['release'], 0.0)
            self.set_synth_value(self.params['breakpoint'], 1.0)
            self.set_synth_value(self.params['sustain'], 1.0)
            self.set_synth_value(self.params['gate-mode'], 0)
            self.sync_ui()
            self.status("Reset envelope")
        msb.client_callback = init_callback 

    def _init_copy_button(self):
        msb = MSB(self.canvas, '', None, 1)
        a0 = self._msb_aspect("Copy")
        msb.define_aspect(0,0,a0)
        x,y = self.xi0+128, self.y1-50
        msb.layout((x,y))
        msb.update_aspect()
        def copy_callback(*_):
            program = self.synth.bank()[None]
            for k in self.clipboard.keys():
                p = self.params[k]
                v = program[p]
                self.clipboard[k] = v
            self.status("Envelope copied to clipboard")
        msb.client_callback=copy_callback
        
    def _init_paste_button(self):
        msb = MSB(self.canvas, '', None, 1)
        a0 = self._msb_aspect("Paste")
        msb.define_aspect(0,0,a0)
        x,y = self.xi0+192, self.y1-50
        msb.layout((x,y))
        msb.update_aspect()
        def paste_callback(*_):
            for k in self.clipboard.keys():
                p = self.params[k]
                v = self.clipboard[k]
                self.set_synth_value(p,v)
            self.sync_ui()
            self.status("Envelope pasted from clipboard")
        msb.client_callback = paste_callback

    def add_control(self, param, sctrl):
        if is_synth_control(sctrl):
            self._controls[param] = sctrl
        else:
            msg = "Can not add %s as synth control to TkSubEditor, param = %s"
            msg = msg % (type(sctrl), param)
            raise(TypeError(msg))

    def status(self, msg):
        self.parent.status(msg)

    def warning(self, msg):
        self.parent.warning(msg)

    def set_value(self, param, value):
        if param in self.paramlist:
            self.set_synth_value(param, value)
            self.sync()

    def set_synth_value(self, param, value):
        program = self.bank[None]
        program[param] = value
        self.synth.x_param_change(param, value)
        msg = "[%s] -> %s" % (param, value)
        self.status(msg)
    
    def _drag_helper(self, refpoint, event):
        pref = self.canvas.coords(refpoint)
        xref = pref[0]
        xabs = event.x
        xrel = max(0, xabs-xref)
        time = min(self.max_segment_time, xrel/(self.xscale*self.zoom))

        yref = self.canvas.coords("env%s-point-0" % self.envid)[1]
        yabs = event.y
        yrel =(yabs-yref)/self.yscale
        level = max(0, min(yrel,1))
        return time,level

    def attack_drag(self, event):
        time, level = self._drag_helper("env%s-point-0" % self.envid, event)
        param = self.params['attack']
        self.set_value(param, time)
        self.set_synth_value(param, time)
        self.sync_ui()

    def decay1_drag(self, event):
        time, level = self._drag_helper("env%s-point-1" % self.envid, event)
        self.set_synth_value(self.params['decay1'], time)
        self.set_synth_value(self.params['breakpoint'], level)
        self.sync_ui()

    def decay2_drag(self, event):
        time, level = self._drag_helper("env%s-point-2" % self.envid, event)
        self.set_synth_value(self.params['decay2'], time)
        self.set_synth_value(self.params['sustain'], level)
        self.sync_ui()
        
    def sustain_drag(self, event):
        time, level = self._drag_helper("env%s-point-3" % self.envid, event)
        self.set_synth_value(self.params['sustain'], level)
        self.sync_ui()
        
    def release_drag(self, event):
        time, level = self._drag_helper("env%s-point-4" % self.envid, event)
        self.set_synth_value(self.params['release'], time)
        self.sync_ui()
        
    def sync_ui(self, *_):
        self.canvas.itemconfig('pad',
                               fill=self['fill'],
                               outline=self['outline'],
                               width=self['outline-width'])
        self.canvas.itemconfig('axis',
                               fill=self['axis-fill'],
                               width=self['axis-width'])
        program = self.bank[None]
        attack = program[self.params['attack']]
        decay1 = program[self.params['decay1']]
        decay2 = program[self.params['decay2']]
        release = program[self.params['release']]
        breakpoint = program[self.params['breakpoint']]
        sustain = program[self.params['sustain']]
        t0 = 0
        t1 = t0 + attack
        t2 = t1 + decay1
        t3 = t2 + decay2
        t4 = t3 + self['sustain-duration']
        t5 = t4 + release
        times = (t0,t1,t2,t3,t4,t5)
        a0 = 0.0
        a1 = 1.0
        a2 = breakpoint
        a3 = sustain
        a4 = sustain
        a5 = 0.0
        levels = (a0,a1,a2,a3,a4,a5)
        coords = []
        radius = self['point-radius']/2
        for i in range(6):
            xc = int(self.xorigin + times[i]*self.xscale*self.zoom)
            yc = int(self.yorigin + levels[i]*self.yscale)
            coords.append((xc,yc))
            tag = 'env%s-point-%s' % (self.envid, i)
            self.canvas.coords(tag, xc-radius, yc+radius, xc+radius, yc-radius)
        for i in range(5):
            q0 = coords[i]
            q1 = coords[i+1]
            tag = 'env%s-segment-%s' % (self.envid, i)
            self.canvas.coords(tag,q0[0],q0[1],q1[0],q1[1])
        gate_param = self.params['gate-mode']
        gate_value = program[gate_param]
        self.msb_gate_mode.value(gate_value)
            
    def sync(self, *_):
        # ISSUE: UGLY inconsistent method name
        # Requiers both sync and sync_ui
        self.sync_ui()
    

    
    
        
        
