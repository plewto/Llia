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


    """
    TkSubEditor provides a primary canvas for constructions synth editors.
    Depending on complexity an editor may be spread across several sub-editors.
    Typically TkSubEditor is sub-classed for specific editor behavior.
    """
    
    # parent - either TkSubEditor or TkSynthWindow
    # 
    def __init__(self, tk_master, parent, name):
        """
        Construct new TkSubEditor
        tk_master - Tk container.  
                    Older existing editors may use a Tk Frame as the master.
                    Newer editors should use a Canvas widget.             
        parent - The parent editor, either an instance of TkSynthWindow 
                 or another  TkSubEditor.
        name - This editors name.  The name should be unique amongst all  
               sub-editors in a given master TkSynthWindow.    
        """
        Frame.__init__(self, tk_master)
        self.parent = parent
        self.synth = parent.synth
        self.bank = self.synth.bank()
        self.config(background=factory.bg())
        self._child_editors = {}
        self._controls = {}
        self._annotations = {}
        # WARNING: For some 'old-stye' editors, tk_master may be a Frame
        # WARNING: and not a Canvas!
        self.canvas = tk_master
        self.parent = parent

    # Returns set of annotation keys.
    # Does not include any child editors.
    def annotation_keys(self):
        """
        Returns a list of available annotation keys.
        See annotation method.
        """
        return self._annotations.keys()

    # Define new annotation key.
    def _define_annotation(self, key):
        self._annotations[key] = ""

    # Set annotation text.
    # Ignore if key has not previously been defined by _define_annotation.
    # Does not actually update any GUI graphics,
    # Returns True if key is defined, False otherwise.
    def _set_annotation(self, key, text):
        if self._annotations.has_key(key):
            self._annotations[key] =str(text)
            return True
        else:
            return False

    # Returns annotation for key.
    # Returns None if key has not previously been defined by _define_annotation.
    def get_annotation(self, key):
        """
        Returns text for selected annotation.

        """
        return self._annotations.get(key, None)

    # Subclasses should implement.
    # If text, update annotation.
    # Returns annotation text associated with key.
    # If key has not been defined by _define_annotation, return None
    @abc.abstractmethod
    def annotation(self, key, text=None):
        """
        Returns or optionally changes annotation text.
        An annotation allows predesignated labels to be set at run time.
        A typical use case is s mixer effect where annotations allow changing
        fader labels.  The method annotation_keys returns a list of available 
        annotation labels.

        key - name of annotation label.
        text - optional, if non-None, update label text.

        Returns annotation text.  If key is not a defined label, return None.
        """
        return None
    
    
    def add_control(self, param, sctrl):
        """
        Adds a synth control to self.
        param - string, synth parameter
        sctrl - The control, should be a sub class of AbstractControl
        """
        if is_synth_control(sctrl):
            self._controls[param] = sctrl
        else:
            msg = "Can not add %s as synth control to TkSubEditor, param = %s"
            msg = msg % (type(sctrl), param)
            raise(TypeError(msg))

    def get_control(self, param):
        """
        Returns control(s) associated with synth parameter.
        """
        acc = []
        try:
            acc.append(self._controls[param])
        except KeyError:
            pass
        for child in self._child_editors:
            acc.append(child.get_control[param])
        return acc

    def has_control(self, param):
        """
        Predicate, True if self has a control for parameter param.
        """
        f = self._controls.has_key(param)
        if f:
            return True
        else:
            for child in self._child_editors:
                f = child.has_control(param)
                if f: return True
        return False
    
    def add_child_editor(self, name, child):
        """
        Adds an instance of TkSubEditor as a child to this editor
        name - the sub editors name. All sub editors must have a unique name
        child - TkSubEditor
        """
        self._child_editors[name] = child

    def status(self, msg):
        """
        Displays text on status line.
        """
        self.parent.status(msg)

    def warning(self, msg):
        """
        Displays warning on status line.
        """
        self.parent.warning(msg)

    def set_value(self, param, value):
        """
        Set value for selected control(s)
        param - string, synth parameter
        value - new value for param

        Note: This method only updates the editor control to match the new 
              value. It does not alter the current synth program.
        """
        try:
            c = self._controls[param]
            c.value(value)
        except KeyError:
            pass
        for ed in self._child_editors.items():
            ed[1].set_value(param, value)
    
    def sync(self, *ignore):
        """
        Update all controls to match current program.
        """
        for key, ed in self._child_editors.items():
            if key not in ignore:
                ed.sync(*ignore)
        prog = self.bank[None]
        for param, sctrl in self._controls.items():
            sctrl.value(prog[param])

    def norm_slider(self,param,x,y,height=150):
        '''
        Adds "normalized" slider (a linear slider with range (0,1)) 
        to canvas.

        ARGS:
          param  - String, synth parameter
          x      - int, x-coordinate
          y      - int, y-coordinate
          height - int

        RETURNS: Tk Scale Widget
        '''
        s = cf.normalized_slider(self.canvas,param,self.parent)
        self.add_control(param,s)
        s.widget().place(x=x,y=y,height=height)
        return s

    def linear_slider(self,param,range_,x,y,height=150):
        '''
        Adds linear slider to canvas.

        ARGS:
          param  - String, synth parameter
          range_ - Tuple (a,b) slider value range, a != b
          x      - int, x-coordinate
          y      - int, y-coordinate
          height - int

        Returns: Tk Scale Widget
        '''
        s = cf.linear_slider(self.canvas,param,self.parent,range_=range_)
        self.add_control(param,s)
        s.widget().place(x=x,y=y,height=height)
        return s
    
    def exp_slider(self,param,mx,x,y,degree=2,height=150,checkbutton=None):
        s = ExpSlider(self.canvas,param,self.parent,
                      range_=mx,degree=degree)
        '''
        Adds slider with exponential response to canvas.
        
        ARGS:
          param  - String, synth parameter
          mx     - float, maximum slider value, mx > 0.
          x      - int, x coordinate
          y      - int, y coordinate
          degree - int, exponential degree, default 2
          height - int, slider height, default 150     
          checkbutton - Tuple, specifies location of optional checkbutton.
                        The checkbutton is used to invert the sign of the 
                        slider value.  If used it should be a tuple
                        (x-offset,y-offset), typical values for default
                        slider height is (-15,150)
       
        RETURNS: ExpSlider
        '''
        self.add_control(param,s)
        s.layout((x,y),height=height,checkbutton_offset=checkbutton)
        return s

    def third_octave_slider(self,param,x,y,height=150):
        s = cf.third_octave_slider(self.canvas,param,self.parent)
        s.widget().place(x=x,y=y,height=height)
        self.add_control(param,s)
        return s

    
    def volume_slider(self,param,x,y,height=150):
        '''
        Adds volume slider to canvas.  A volume slider is calibrated in 
        db and has several distinct ranges.

        ARGS:
          param  - String, synth parameter
          x      - int, x-coordinate
          y      - int, y-coordinate
          height - int
        
        RETURNS: Tk Scale widget
        '''
        s = cf.volume_slider(self.canvas,param,self.parent)
        self.add_control(param,s)
        s.widget().place(x=x,y=y,height=height)

    def tumbler(self,param,digits,scale,x,y,range_=None):
        '''
        Adds digital tumbler to canvas.
        
        ARGS:
          param  - String, synth parameter
          digits - int, number of digits
          scale  - float, numeric scale factor.
          x      - int, x coordinate
          y      - int, y coordinate
          
        RETURNS: Tumbler
        '''
        range_ = range_ or (0, 10**digits)
        t = Tumbler(self.canvas,param,self.parent,
                    digits = digits,
                    scale = scale,
                    range_ = range_)
        self.add_control(param,t)
        t.layout((x,y))
        return t

    def msb_aspect(self,msb,index,value,
                   text=None,
                   fill=None,
                   foreground=None,
                   outline=None,
                   update = False):
        '''
        Defines an aspect for an MSB (Multi State Button)
        
        ARGS:
          msb        - An instance of MSB
          index      - int, the aspect index.  index must be between 0
                       and the maximum aspect count for the msb.
          value      - The aspects value
          text       - Optional, defaults to string representation of value
          fill       - Optional, background color
          foreground - Optional, foreground color
          outline    - Optional, outline color
          update     - Boolean, if True the update_aspect method is called 
                       on the msb.  update_aspect must be called at least
                       once for the msb to be visible.  On the other hand
                       needlessly calling it for each defined aspect is
                       wasteful.
        
        The optional color arguments default to the BG and FG colors
        of the synth's pallet.  outline defaults to foreground.

        RETURNS: dictionary
        '''
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
    
    def msb(self,param,count,x,y,width=60,height=27):
        '''
        Adds Multi State Button to the canvas.   In order for the button to 
        be useful, two or more aspects must be defined.  The update_aspect()
        method should be called at least once after all the aspects have been
        defined, otherwise the button will not be visible.

        ARGS:
          param - String, synth parameter
          count - int, number of aspects.  count > 1.
          x     - int, x coordinate
          y     - int, y coordinate
        
        RETURNS: MSB
        '''
        b = MSB(self.canvas,param,self.parent,count)
        self.add_control(param,b)
        b.layout((x,y),width=width,height=height)
        return b

    def toggle(self,param,x,y,
               off = (0, "Off"),
               on = (1, "On")):
        '''
        Adds two-position MSB to canvas.
        There is no need to call update_aspect for the toggle button.

        ARGS:
          param - String, synth parameter
          x     - int, x coordinate
          y     - int, y coordinate
          off   - Optional tuple defines the "off" aspect (value,text)
          on    - Optional tuple defines the "On" aspect (value,text)
        
        RETURNS: MSB
        '''
        pallet = self.synth.specs["pallet"]
        fg,bg = pallet["FG"],pallet["BG"]
        b = self.msb(param,2,x,y)
        self.msb_aspect(b,0,off[0],text=off[1],update=False,fill=bg,foreground=fg)
        self.msb_aspect(b,1,on[0],text=on[1],update=True,fill=fg,foreground=bg,outline=fg)
        return b
