# llia.gui.tk.tumbler

from llia.gui.tk.msb import MsbAspect, MSB, ToggleButton
from llia.generic import is_synth_control

class Tumbler(object):

    
    def __init__(self,canvas,param,editor,
                 sign=False,digits=4,scale=1.0,
                 range_ = None,
                 fill = 'black',
                 foreground = 'white',
                 outline = 'white',
                 active_color = 'yellow',
                 font = ('Times',10)):
        '''
        Tumbler combines several MSB buttons into a single compost control
        for numeric values.
        '''
        self.canvas = canvas
        self.param=param
        self.editor = editor
        self._range = range_ or (0,10**digits-1)
        self._common_aspect = {"fill" : fill,
                               "foreground" : foreground,
                               "outline" : outline,
                               "active-fill" : fill,
                               "active-foreground" : active_color,
                               "active-outline" : active_color,
                               "font" : font}
        self.scale = float(scale)
        self.has_sign = sign
        self._msb_sign = ToggleButton(canvas,"",None,
                                      text=["-","+"],
                                      values=[-1,1])
        self._msb_sign.tag_bind("<Button-1>", self._callback)
        self._msb_sign.tag_bind("<Button-3>", self._callback)

      
        acc = []
        for i in range(digits):
            msb = MSB.digit_msb(canvas,"",None,
                                font = self._common_aspect['font'],
                                fill = self._common_aspect['fill'],
                                foreground = self._common_aspect['foreground'],
                                outline = self._common_aspect['outline'],
                                active_fill = self._common_aspect['fill'],
                                active_foreground = self._common_aspect['active-foreground'],
                                active_outline = self._common_aspect['active-outline'])
            msb.tag_bind("<Button-1>", self._callback)
            msb.tag_bind("<Button-3>", self._callback)
            msb.weight = (10**i)
            acc.append(msb)
        acc.reverse()
        self._digits = acc
        
        

    def widget(self, key=None):
        msg = "Tumbler does not implement widget method"
        raise NotImplementedError(msg)

    def widget_keys(self):
        return []

    def has_widget(self, key):
        return False

    def _get_value(self):
        acc = 0
        for b in self._digits:
            w = b.weight
            digit = b.value()
            acc += digit*w
        acc *= self._msb_sign.value()
        mn,mx = self._range
        acc = min(max(acc,mn),mx)
        return acc*self.scale

    def _set_value(self, v):
        mn,mx = self._range
        v = int(v/self.scale)
        v = min(max(v,mn),mx)
        if v < 0:
            s = -1
        else:
            s = 1
        v = abs(v)
        dcount = len(self._digits)
        for i in range(dcount):
            j = dcount-i-1
            b = self._digits[j]
            lsd = int(v % 10)
            b.value(lsd)
            v /= 10
        self._msb_sign.value(s)
        self._update_synths()

    def _callback(self, *_):
        mn,mx = self._range
        v = min(max(self._get_value(),mn),mx)
        self._set_value(v)
        
    def _update_synths(self, *_):
        if self.editor:
            v = self._get_value()
            synth = self.editor.synth
            synth.x_param_change(self.param,v)
            program = synth.bank()[None]
            program[self.param] = v
            msg = '[%s] -> %s' % (self.param, v)
            self.editor.status(msg)
        
    def update_aspect(self):
        for b in self._digits:
            b.update_aspect()
        self._msb_sign.update_aspect()

    # No range test, no scaling
    def aspect(self, new_aspect=None):
        if new_aspect is not None:
            a = new_aspect
            if a < 0:
                s = -1
                a = abs(a)
            else:
                s = 1
            for b in self._digits:
                lsd = int(a % 10)
                b.value(lsd)
            self._msb_sign.value(s)
        acc = 0
        s = self._msb_sign.value()
        for b in self._digits:
            w = b.weight
            acc += w*b.value()
        return int(acc*s)

    def value(self, new_value=None):
        if new_value is not None:
            self._set_value(new_value)
            self.update_aspect()
        return self._get_value()
    
    def layout(self, offset=(0,0),bwidth=15,height=20):
        x,y= offset
        if self.has_sign:
            self._msb_sign.layout((x,y),width=bwidth,height=height)
            x += bwidth
            self._msb_sign.update_aspect()
        for b in self._digits:
            b.layout((x,y),width=bwidth,height=height)
            x += bwidth
            b.update_aspect()
            
            

@is_synth_control.when_type(Tumbler)
def _is_synth_control(obj):
    return obj
        
