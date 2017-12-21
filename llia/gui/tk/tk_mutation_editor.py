# llia.gui.tk.tk_mutation_editor
#

from Tkinter import StringVar
import ttk

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory



class TkMutationStrip(object):

    def __init__(self, canvas, paramobj):
        super(TkMutationStrip,self).__init__()
        self.paramobj = paramobj
        self.frame = factory.frame(canvas)
        lab_param = factory.label(self.frame, "%-16s" % paramobj.param)
        lab_param.config(width=17)
        lab_prob = factory.label(self.frame, "P")
        lab_range = factory.label(self.frame, "R")
        self.var_prob = StringVar()
        self.var_prob.set(10)   # as int percent 0..100
        self.var_range = StringVar()
        self.var_range.set(1)   # as int percent 0..100
        
        spin_prob = factory.int_spinbox(self.frame,
                                          self.var_prob,0.0,100,
                                          self.set_probability)
        spin_prob.config(width=6)
        spin_range = factory.int_spinbox(self.frame,
                                           self.var_range,0.0,100,
                                           self.set_range)
        spin_range.config(width=6)
        
        lab_param.grid(row=1,column=0, sticky="w", padx=4)
        lab_prob.grid(row=1,column=1, sticky="w", padx=4)
        spin_prob.grid(row=1,column=2, sticky="w", padx=4)
        lab_range.grid(row=1,column=3, sticky="w", padx=4)
        spin_range.grid(row=1,column=4, sticky="w", padx=4)
        

    def set_probability(self):
        i = int(self.var_prob.get())
        self.paramobj.probability = i/100.0
        
    def set_range(self):
        i = int(self.var_range.get())
        self.paramobj.max_ratio = i/100.0
        


class TkMutationEditor(TkSubEditor):

    NAME = "Mutation"
    TAB_FILE = "resources/Tabs/rnd.png"
    RESERVED_ROWS = 5
    RESERVED_COLUMNS = 5
    MAX_STRIPS_PER_COLUMN = 24
    
    def __init__(self, editor):
        frame = editor.create_tab(self.NAME,self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame,1000,700)
        canvas.pack()
        self.canvas = canvas
        self.editor = editor
        TkSubEditor.__init__(self,canvas,editor,self.NAME)
        self.mutation_object = self.synth.specs["mutation"]
        self._strips = {}
        for k,v in self.mutation_object.items():
            strip = TkMutationStrip(canvas,v)
            self._strips[k] = strip
        self._var_fill_start = StringVar()
        self._var_fill_start.set(127)
        self._var_fill_end = StringVar()
        self._var_fill_end.set(128)
        self._var_progressive_fill = StringVar()
        self._var_progressive_fill.set(0)
        
        self._layout_common_widgets()

    def auto_allign(self):
        row, col = self.RESERVED_ROWS, self.RESERVED_COLUMNS
        max_row = row + self.MAX_STRIPS_PER_COLUMN
        for s in self._strips.values():
            s.frame.grid(row=row,column=col,pady=1)
            row += 1
            if row > max_row:
                row = 5
                col += 1

    def keys(self):
        return self._strips.keys()

    def layout(self, param, row, col):
        if row < self.RESERVED_ROWS or col < self.RESERVED_COLUMNS:
            msg = "TkMutationEditor.layout, can not use reserved row or column."
            raise ValueError(msg)
        s = self._strips[param]
        s.frame.grid(row=row, column=col, pady=1)
        
    def _layout_common_widgets(self):
        canvas = self.canvas
        bMutate = factory.button(canvas,"Mutate",command=self.mutate)
        bMutate.grid(row=5, column=1, padx=8, pady=16,columnspan=2)

        
        lab_start = factory.label(canvas,"Start")
        lab_end = factory.label(canvas,"End")
        sbStart = factory.int_spinbox(canvas,self._var_fill_start,from_=0, to=128)
        sbEnd = factory.int_spinbox(canvas,self._var_fill_end,from_=0,to=128)
        sbStart.config(width=4)
        sbEnd.config(width=4)
        lab_start.grid(row=11,column=1,pady=1)
        lab_end.grid(row=11,column=2,pady=1)
        sbStart.grid(row=12,column=1,pady=1)
        sbEnd.grid(row=12,column=2,pady=1)
        
        bFill = factory.button(canvas,"Fill",command=self.fill)
        cbProgressive = factory.checkbutton(canvas,"+",self._var_progressive_fill)
        bFill.grid(row=10  ,column=1,pady=1,padx=4)
        cbProgressive.grid(row=10 ,column=2)
        
    def _mutation_object(self):
        try:
            return self.synth.specs["mutation"]
        except KeyError:
            msg = "Mutation function not defined."
            self.status(msg)
            return None

    def mutate(self):
        print("------------------------------------") # DEBUG
        muobj = self._mutation_object()
        prog1 = self.synth.bank()[None]
        prog2 = muobj.mutate(prog1.clone())
        if True:                # Diagnostic print
            d = prog2.diff(prog1)
            for k,v2 in d.items():
                v1 = prog1[k]
                print("%s:  %s -> %s" % (k,v1,v2))
        slot = int(self._var_fill_start.get())
        self.synth.bank()[slot] = prog2
        self.synth.use_program(slot)
        
            
        
        
        
        
    def fill(self):
        print("Fill")

    
