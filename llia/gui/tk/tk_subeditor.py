# llia.gui.tk.tk_subeditor
# 22-June-2016

from __future__ import print_function
from Tkinter import Frame
import abc

from llia.generic import is_synth_control
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.expslider import ExpSlider
from llia.gui.tk.msb import MSB, ToggleButton
from llia.gui.tk.tumbler import Tumbler

class TkSubEditor(Frame):

    # parent - either TkSubEditor or TkSynthWindow
    # 
    def __init__(self, tk_master, parent, name):
        Frame.__init__(self, tk_master)
        self.parent = parent
        self.synth = parent.synth
        self.bank = self.synth.bank()
        self.config(background=factory.bg())
        self._child_editors = {}
        self._controls = {}
        # WARNING: For some 'old-stye' editors, tk_master may be a Frame
        # WARNING: and not a Canvas!
        self.canvas = tk_master
        self.parent = parent

    def add_control(self, param, sctrl):
        if is_synth_control(sctrl):
            self._controls[param] = sctrl
        else:
            msg = "Can not add %s as synth control to TkSubEditor, param = %s"
            msg = msg % (type(sctrl), param)
            raise(TypeError(msg))

    def get_control(self, param):
        acc = []
        try:
            acc.append(self._controls[param])
        except KeyError:
            pass
        for child in self._child_editors:
            acc.append(child.get_control[param])
        return acc

    def has_control(self, param):
        f = self._controls.has_key(param)
        if f:
            return True
        else:
            for child in self._child_editors:
                f = child.has_control(param)
                if f: return True
        return False
    
    def add_child_editor(self, name, child):
        self._child_editors[name] = child

    def status(self, msg):
        self.parent.status(msg)

    def warning(self, msg):
        self.parent.warning(msg)

    def set_value(self, param, value):
        try:
            c = self._controls[param]
            c.value(value)
        except KeyError:
            pass
        for ed in self._child_editors.items():
            ed[1].set_value(param, value)
    
    def sync(self, *ignore):
        for key, ed in self._child_editors.items():
            if key not in ignore:
                ed.sync(*ignore)
        prog = self.bank[None]
        for param, sctrl in self._controls.items():
            sctrl.value(prog[param])

    def norm_slider(self,param,x,y,height=150):
        s = cf.normalized_slider(self.canvas,param,self.parent)
        self.add_control(param,s)
        s.widget().place(x=x,y=y,height=height)
        return s

    def linear_slider(self,param,range_,x,y,height=150):
        s = cf.linear_slider(self.canvas,param,self.parent)
        self.add_control(param,s)
        s.widget().place(x=x,y=y,height=height)
        return s
    
    def exp_slider(self,param,mx,x,y,degree=2,height=150,checkbutton=None):
        s = ExpSlider(self.canvas,param,self.parent,
                      range_=mx,degree=degree)
        self.add_control(param,s)
        s.layout((x,y),height=height,checkbutton_offset=checkbutton)
        return s

    def volume_slider(self,param,x,y,height=150):
        s = cf.volume_slider(self.canvas,param,self.parent)
        self.add_control(param,s)
        s.widget().place(x=x,y=y,height=height)

    def tumbler(self,param,digits,scale,x,y):
        t = Tumbler(self.canvas,param,self.parent,
                    digits = digits,
                    scale = scale)
        self.add_control(param,t)
        t.layout((x,y))
        return t

    def msb_aspect(self,msb,index,value,
                  text=None,
                  fill=None,
                  foreground=None,
                  outline=None,
                   update = False):
        pallet = self.synth.specs["pallet"]
        fill = fill or pallet["BG"]
        foreground = foreground or pallet["FG"]
        outline = outline or foreground
        text = text or str(value)
        d = {"fill" : fill,
             "foreground" : foreground,
             "outline" : outline,
             "text" : text,
             "value" : value}
        msb.define_aspect(index,value,d)
        if update: msb.update_aspect()
        return d

    def msb(self,param,count,x,y):
        b = MSB(self.canvas,param,self.parent,count)
        self.add_control(param,b)
        b.layout((x,y))
        return b

    def toggle(self,param,x,y,
               off = (0, "Off"),
               on = (1, "On"),
               update=False):
        b = self.msb(param,2,x,y)
        self.msb_aspect(b,0,off[0],text=off[1],update=False)
        self.msb_aspect(b,1,on[0],text=on[1],update=False)
        return b
        
        
        
