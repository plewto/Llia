# llia.gui.tk.nudgetool

from __future__ import print_function
import abc
from llia.gui.abstract_control import AbstractControl

class NudgeTool(object):

    WIDTH = 8
    HEIGHT = 8
    
    def __init__(self, canvas, client, editor, value):
        super(NudgeTool, self).__init__()
        self.canvas = canvas 
        self.client = self.client = client 
        self.editor = editor 
        self.value = value 
        self.width = NudgeTool.WIDTH
        self.height = NudgeTool.HEIGHT
        self.fill = 'black'
        self.outline = 'blue'
        self.active_outline = 'yellow'
        self.rollover_text = ''
        self._canvas_items = []

    def _bind_callbacks(self):
        for ci in self._canvas_items:
            self.canvas.tag_bind(ci,'<Enter>',self._enter_callback)
            self.canvas.tag_bind(ci,'<Leave>',self._leave_callback)
            self.canvas.tag_bind(ci,'<Button-1>',self._nudge)
            self.canvas.tag_bind(ci,'<Button-3>',self._inv_nudge)
        
    @abc.abstractmethod
    def _nudge(self, event):
        # implementing method should call after value update
        self._update_synth(self.client.value())

    @abc.abstractmethod
    def _inv_nudge(self, event):
        # implementing method should call after value update
        self._update_synth(self.client.value())

    def _enter_callback(self, *_):
        for ci in self._canvas_items:
            self.canvas.itemconfig(ci, outline=self.active_outline)
        self.editor.status(self.rollover_text)

    def _leave_callback(self, *_):
        for ci in self._canvas_items:
            self.canvas.itemconfig(ci, outline=self.outline)
        self.editor.status('')

    @abc.abstractmethod
    def render(self, x=0, y=0):
        pass

    def _update_synth(self, value):
        param = self.client.param
        synth = self.client.synth
        prog = synth.bank()[None]
        synth.x_param_change(param,value)
        prog[param] = value
        msg = '[%s] -> %s' % (param, value)
        self.editor.status(msg)

class BasicNudgeTool(NudgeTool):

    def __init__(self,canvas,client,editor,diff):
        super(BasicNudgeTool, self).__init__(canvas,client,editor,diff)
        ro = "Left/Right click -> Increment/Decrement %s by %s"
        self.rollover_text = ro % (client.param,diff)

    def _nudge(self, event):
        v0 = self.client.value()
        self.client.value(v0+self.value)
        super(BasicNudgeTool, self)._nudge(event)

    def _inv_nudge(self, event):
        v0 = self.client.value()
        self.client.value(v0-self.value)
        super(BasicNudgeTool, self)._nudge(event)

    def render(self,x=0,y=0):
        x0,y0 = x,y
        x1,y1 = x+self.width,y+self.height
        xc,yc = (x0+x1)/2,(y0+y1)/2
        chevron = self.canvas.create_polygon([x1,y1,xc,y0,x0,y1],
                                             fill = self.outline,
                                             outline = self.outline)
        self._canvas_items = [chevron]
        self._bind_callbacks()

        
class ScaleNudgeTool(NudgeTool):

    def __init__(self,canvas,client,editor,ratio,rollover=''):
        super(ScaleNudgeTool, self).__init__(canvas,client,editor,ratio)
        ro = "Left/Right click -> Scale/Divide %s by %s"
        self.rollover_text = rollover or ro % (client.param,ratio)

    def _nudge(self, event):
        v0 = self.client.value()
        self.client.value(v0*self.value)
        super(ScaleNudgeTool,self)._nudge(event)

    def _inv_nudge(self, event):
        v0 = self.client.value()
        self.client.value(v0/self.value)
        super(ScaleNudgeTool,self)._inv_nudge(event)

    def render(self,x=0,y=0):
        x0,y0 = x,y
        x1,y1 = x0+self.width,y0+self.height
        inner = 3
        x2,y2 = x0+inner,y0+inner
        x3,y3 = x1-inner,y1-inner
        c1 = self.canvas.create_oval([x0,y0,x1,y1],
                                     fill=self.fill,
                                     outline=self.outline)
        c2 = self.canvas.create_oval([x2,y2,x3,y3],
                                     fill=self.fill,
                                     outline=self.outline)
        self._canvas_items = [c1,c2]
        self._bind_callbacks()

        
class ConstantNudgeTool(NudgeTool):

    def __init__(self,canvas,client,editor,value):
        super(ConstantNudgeTool, self).__init__(canvas,client,editor,value)
        ro = "Set %s to %s" % (client.param,value)
        self.rollover_text = ro

    def _nudge(self,event):
        self.client.value(self.value)
        super(ConstantNudgeTool, self)._nudge(event)

    def _inv_nudge(self,event):
        self._nudge(event)

    def render(self,x=0,y=0):
        x0,y0 = x,y
        x1,y1 = x0+self.width,y0+self.height
        r = self.canvas.create_rectangle([x0,y0,x1,y1],
                                         fill = self.fill,
                                         outline = self.outline)
        self._canvas_items = [r]
        self._bind_callbacks()
