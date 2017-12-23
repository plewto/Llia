# llia.gui.tk.msb
# MSB --> Multi State Button
#
# Defines a multi-state synth control button for use with TkSubEditor
#

from llia.generic import is_synth_control


#  ---------------------------------------------------------------------- 
#                               MsbAspect class
#

class MsbAspect(dict):

    '''
    MsbAspect is a helper class for MSB.  It is essentially a dictionary with
    with a restricted set of keys and defines a single aspect of MSB.
    An attempt is made to resolve unset keys with defaults.
    '''
    
    ALLOWED_KEYS = ('value',
                    'fill','disabled-fill','active-fill',
                    'foreground','disabled-foreground','active-foreground',
                    'outline','disabled-outline','active-outline',
                    'text', 'image')

    KEY_SUBSTITUTIONS = {
        'value' : None,
        'fill' : None,
        'disabled-fill' : 'fill',
        'active-fill' : 'fill',
        'foreground' : None,
        'disabled-foreground' : 'foreground',
        'active-foreground' : 'foreground',
        'outline' : 'foreground',
        'disabled-outline' : 'outline',
        'active-outline' : 'outline',
        'text' : 'text',
        'image' : None
    }
    
    def __init__(self, common):
        '''
        Creates new instance of MsbAspect.
        
        ARGS:
           common - A dictionary holding the common aspect parameters of 
                    a MSB object.   All instances of MsbAspect used with 
                    the same instance of MSB share a common dictionary.
        '''
        super(MsbAspect, self).__init__()
        self.common = common
        self['value'] = -1
        self['fill'] = 'black'
        self['foreground'] = 'white'
        self['text'] = ''

    def __getitem__(self, key):
        try:
            return self.common[key]
        except KeyError:
            rs = None
            working_key = key
            while not rs:
                try:
                    rs = super(MsbAspect, self).__getitem__(working_key)
                    return rs
                except KeyError:
                    working_key = self.KEY_SUBSTITUTIONS[working_key]
                    if not working_key:
                        raise KeyError(key)

    def __setitem__(self, key, value):
        if key in MsbAspect.ALLOWED_KEYS:
            super(MsbAspect, self).__setitem__(key,value)
                    

#  ---------------------------------------------------------------------- 
#                                  MSB class

def null_callback(*_):
    pass


class MSB(object):

    '''
     MSB (Multi State Button) is a synth editor widget for use with TkSubEditor
    
    each MSB has a fixed number of possible aspects/values.
    Graphically an MSB consist of the following Canvas items (from bottom up):

        1) pad     - filled rectangle, the background
        2) outline - open rectangle
        3) image   - (currently not supported)
        4) text    -

    The appearance of these four components may be set separately for each 
    of the possible button states. 
    
    MSB implements nearly the same interface as 
    llia.gui.abstract_control.
    '''

    def __init__(self, canvas, param, editor, naspects):
        '''
        Construct new instance of MSB

        ARGS:
          canvas - An instance of Tk Canvas.
          param  - String, the synth parameter
          editor - TkApplicationWindow or None.
                   An MSB may be used as a general widget by 
                   setting editor to None.
          naspects - int, number of possible aspects

        The number of possible aspects can not be changed once the button
        has been created.  Initially each aspect is set to a default.  Once the 
        button is created use the define_aspect method to set actual values.
        '''
        self.canvas = canvas
        self.param = param
        self.editor = editor
        self._common = {'outline-width' : 1,
                        'font' : ('Times', 12)}
        self._aspects = []
        for i in range(naspects):
            a = MsbAspect(self._common)
            self._aspects.append(a)
        self._value_map = {}   # maps value to int aspect index 
        self._current_aspect = 0
        self._disabled = False
        self.wrap = True
        self._pad = canvas.create_rectangle(0,0,0,0, fill='', outline='')
        self._outline = canvas.create_rectangle(0,0,0,0, fill='', outline='')
        self._image = canvas.create_image(0,0,image=None)
        self._text = canvas.create_text(0,0,text='', fill='')
        self.canvas.tag_bind(self._pad, '<Enter>', self._enter_callback)
        self.canvas.tag_bind(self._pad, '<Leave>', self._exit_callback)
        self.canvas.tag_bind(self._pad, '<Button-1>', self.next_state)
        self.canvas.tag_bind(self._pad, '<Button-3>', self.previous_state)
        self.canvas.tag_bind(self._outline, '<Button-1>', self.next_state)
        self.canvas.tag_bind(self._outline, '<Button-3>', self.previous_state)
        self.canvas.tag_bind(self._text, '<Button-1>', self.next_state)
        self.canvas.tag_bind(self._text, '<Button-3>', self.previous_state)
        self.client_callback = null_callback

    def enable(self, state):
        self.disable(not state)
        
    def tag_bind(self, binding, callback, add='+'):
        self.canvas.tag_bind(self._pad, binding, callback, add)
        self.canvas.tag_bind(self._outline, binding, callback, add)
        self.canvas.tag_bind(self._text, binding, callback, add)

    def tag_unbind(self, binding):
        self.canvas.tag_unbind(self._pad, binding)
        self.canvas.tag_unbind(self._outline, binding)
        self.canvas.tag_unbind(self._text, binding)
        
    def __len__(self):
        '''Returns number of possible aspects.'''
        return len(self._aspects)
        
    def define_aspect(self, n, value, adict):
        '''
        Define value and appearance of specific aspect.
        
        ARGS:
           n     - The aspect index, 0 <= n < len(self)
           value - float, synth parameter value for this aspect.
           adict - dictionary holding aspect values.

        adict is used internally to update the MsbAspect object for this 
        aspect.  All colors use Tk color specification strings. 
        The possible keys are:

          'font' - Tk font specification, defaults to ('Times', 12)
          'outline-width' - int width in pixels of button outline.
          'fill'       - the background color
          'foreground' - the text color
          'outline'    - the outline color, defaults to foreground
          'disabled-fill'       - defaults to fill
          'disabled-foreground' - defaults to foreground
          'disabled-outline'    - defaults to outline
          'active-fill'         - defaults to fill
          'active-foreground'   - defaults to foreground
          'active-outline'      - defaults to outline
          
       The 'active' colors are used to highlight the button when the mouse
       enters it.
        '''
        a = self._aspects[n]
        self._current_aspect = n
        ck = self._common.keys()
        for k,v in adict.items():
            if k in ck:
                self._common[k] = v
            else:
                a[k] = v
        value = float(value)
        a['value'] = value
        self._aspects[n] = a
        self._value_map[value] = n
        
    def __getitem__(self, key):
        ''' 
        self.__getitem__(key) ==> self[key]
        Returns item using current button aspect.
        ''' 
        a = self._aspects[self._current_aspect]
        return a[key]

    def widget(self, key=None):
        '''
        Included only for compatibility with AbstractControl and 
        Should not be used.  Raises NoImplementedError
        '''
        msg = "MSB does not implement widget method"
        raise NotImplementedError(msg)

    def widget_keys(self):
        '''
        Included only for compatibility with AbstractControl.
        Returns an empty list.
        '''
        return []

    def has_widget(self, key):
        return False
    
    def update_aspect(self):
        '''
        Update the button appearance to match it's current aspect.
        In most cases update_aspect should be called after all aspects are defined,
        to force drawing of self on canvas. 
        '''
        canvas = self.canvas
        canvas.itemconfig(self._outline, fill='', width=self['outline-width'])
        canvas.itemconfig(self._text, text=self['text'], font=self['font'])
        if self.is_disabled():
            canvas.itemconfig(self._pad, fill=self['disabled-fill'])
            canvas.itemconfig(self._outline, outline=self['disabled-outline'])
            canvas.itemconfig(self._text, fill=self['disabled-foreground'])
            canvas.itemconfig(self._text, text=self['text'])
        else:
            canvas.itemconfig(self._pad, fill=self['fill'])
            canvas.itemconfig(self._outline, outline=self['outline'])
            canvas.itemconfig(self._text, fill=self['foreground'])
            canvas.itemconfig(self._text, text=self['text'])
        canvas.update_idletasks()

    def _enter_callback(self, *_):
        # Mouse enter callback
        canvas = self.canvas
        if self.is_disabled():
            canvas.itemconfig(self._pad, fill=self['disabled-fill'])
            canvas.itemconfig(self._outline, outline=self['disabled-outline'])
            canvas.itemconfig(self._text, fill=self['disabled-foreground'])
        else:
            canvas.itemconfig(self._pad, fill=self['active-fill'])
            canvas.itemconfig(self._outline, outline=self['active-outline'])
            canvas.itemconfig(self._text, fill=self['active-foreground'])
            msg = "[%s] -> %s" % (self.param, self.value())
            if self.editor:
                self.editor.status(msg)
            
    def _exit_callback(self, *_):
        # Mouse exit callback
        canvas = self.canvas
        if self.is_disabled():
            canvas.itemconfig(self._pad, fill=self['disabled-fill'])
            canvas.itemconfig(self._outline, outline=self['disabled-outline'])
            canvas.itemconfig(self._text, fill=self['disabled-foreground'])
        else:
            canvas.itemconfig(self._pad, fill=self['fill'])
            canvas.itemconfig(self._outline, outline=self['outline'])
            canvas.itemconfig(self._text, fill=self['foreground'])
            
    def callback(self, *_):
        self.next_state()

    def _update_synths(self):
        if self.editor:
            a = self._aspects[self._current_aspect]
            value = a['value']
            synth = self.editor.synth
            synth.x_param_change(self.param, value)
            program = synth.bank()[None]
            program[self.param] = value
            msg = '[%s] -> %s' % (self.param, value)
            self.editor.status(msg)
        
    def next_state(self, *_):
        '''
        Increment button to next state.  
        If the final state has been reached and self.wrap is True, wrap 
        around to the first state.

        If the button is disabled, do nothing.
        '''
        if not self._disabled:
            n = self._current_aspect + 1
            if n >= len(self):
                if self.wrap:
                    n = 0
                else:
                    n = len(self)-1
            self._current_aspect = n
            self.update_aspect()
            self._update_synths()
            self.client_callback(self)
        

    def previous_state(self, *_):
        '''
        Decrement button to the previous state.
        If the first state is reached and self.wrap is True, wrap around
        to the final state.

        If the button is disabled, do nothing.
        '''
        if not self._disabled:
            n = self._current_aspect - 1
            if n < 0:
                if self.wrap:
                    n = len(self)-1
                else:
                    n = 0
            self._current_aspect = n
            self.update_aspect()
            self._update_synths()
            self.client_callback(self)
        
    def disable(self, flag):
        self._disabled = flag
        self.update_aspect()

    def is_disabled(self):
        return self._disabled
    
    def aspect(self, new_aspect=None):
        '''
        Retrieve/change current button state. 
        
        ARGS:
          new_aspect - optional int.  If specified the button is placed
                       in the indicated state.  

        RETURNS:
          int

        Raises IndexError if new_aspect is an int and 
        new_aspect < 0 or new_aspect >= len(self)
        '''
        if new_aspect is not None:
            n = int(new_aspect)
            if 0 <= n < len(self):
                self._current_aspect = n
                self.update_aspect()
            else:
                msg = "Invalid MSB aspect: %s" % new_aspect
                raise IndexError(msg)
        else:
            self.update_aspect()
        return self._current_aspect


    # Hack to brute force update value (BUG FIX 0015)
    # Should only be called when there is not an exact match between
    # a defined value and new_value, most often this is due to float
    # rounding errors.
    def _update_value_fallback(self, new_value):
        mindiff = 1e6
        locked = None
        for v in self._value_map.keys():
            q = abs(new_value-v)
            if q < mindiff:
                mindiff = q
                locked = v
        if locked != None:
            aspect = self._value_map[locked]
            self._current_aspect = self._value_map[locked]
            self.update_aspect()
        else:
            raise ValueError("Can not set MSB(%s) value to %s" % (self.param, new_value))

    
    def value(self, new_value=None):
        '''
        Retrieve/change current button value.

        ARGS:
           new_value - optional number.  If specified the button's value 
                       is updated and the corresponding aspect is
                       displayed.  
        RETURNS:
            number

        Raises KeyError if no aspect has matching value.
        '''
        if new_value is not None:
            try:
                value = float(new_value)
                self._current_aspect = self._value_map[value]
                self.update_aspect()
            except KeyError:
                # msg = "'%s' MSB does not have value: %s" % (self.param, value)
                # raise KeyError(msg)
                self._update_value_fallback(new_value)
        a = self._aspects[self._current_aspect]
        return a['value']

    def layout(self, 
               offset=(0,0), width=60, height=27,
               outline_offset = (0,0),
               text_offset = (0,0),
               image_offset = (0,0)):
        x0,y0 = offset
        x1,y1 = x0+width, y0+height
        xc,yc = (x0+x1)/2, (y0+y1)/2
        xout,yout = x0+outline_offset[0], y0+outline_offset[1]
        xtxt,ytxt = xc+text_offset[0], yc+text_offset[1]
        ximg,yimg = x0+image_offset[0], y0+image_offset[1]
        c = self.canvas
        c.coords(self._pad, x0,y0,x1,y1)
        c.coords(self._outline, xout,yout,xout+width, yout+height)
        c.coords(self._text, xtxt, ytxt)
        c.coords(self._image, ximg, yimg)

    @staticmethod
    def digit_msb(canvas,param,editor,digits=range(10),scale=1.0,
                  font=('Times',10),
                  outline_width = 1,
                  fill = 'black',
                  foreground = 'white',
                  outline = 'white',
                  active_fill = 'black',
                  active_foreground = 'yellow',
                  active_outline = 'yellow'):
        '''
        Creates MSB with n digital states.
        
        ARGS:
            canvas - An instance fo Tk Canvas
            param  - String, synth paremter
            editor - TkApplicationWindow or None
            digits - List of states
            scale  - Float, scaling factor applied to values in digits
            font   - Tuple, Tk font specification
            outline_width - int, 
            fill          - String, Tk color
            foreground    - String, Tk color
            outline       - String, Tk color
            active_fill   - String, Tk color
            active_foreground - String, Tk color
            active_outline    - String, Tk color

        RETURNS: MSB
        '''
        naspects = len(digits)
        adict = {"font" : font,
                 "outline-width" : outline_width,
                 "fill" : fill,
                 "outline" : outline,
                 "active-fill" : active_fill,
                 "active-foreground" : active_foreground,
                 "active-outline" : active_outline}
        msb = MSB(canvas,param,editor,naspects)
        for i,d in enumerate(digits):
            value = d*scale
            adict['text'] = str(d)
            msb.define_aspect(i,value,adict)
        return msb
        

class ToggleButton(MSB):

    # Special case 2-state button
    
    def __init__(self, canvas, param, editor, text=["Off", "On"], values=[0,1],
                 fill = 'black',foreground='white', outline='white',
                 active_color = 'yellow', font=('Times', 12),
                 selected_fill = 'white', selected_foreground = 'black'):
        super(ToggleButton, self).__init__(canvas, param, editor, 2)
        aspect0 = MsbAspect(self._common)
        aspect0['text'] = text[0]
        aspect0['fill'] = fill
        aspect0['foreground'] = foreground
        aspect0['outline'] = outline
        aspect0['active-outline'] = active_color
        aspect0['active-foreground'] = active_color
        aspect0['font'] = font
        self.define_aspect(0, values[0], aspect0)
        aspect1 = MsbAspect(self._common)
        aspect1['text'] = text[1]
        aspect1['fill'] = selected_fill
        aspect1['foreground'] = selected_foreground
        aspect1['outline'] = outline
        aspect1['active-outline'] = active_color
        aspect1['active-foreground'] = active_color
        aspect1['font'] = font
        self.define_aspect(1, values[1], aspect1)
        
        
@is_synth_control.when_type(MSB)
def _is_synth_control(obj):
    return True
