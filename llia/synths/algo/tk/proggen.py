# llia.synths.algo.tk.proggen
#
# Define configuratin panl form Algo random patch generator.
# Configurations to the patch generator are gloabl.  If there are
# two or more instances of Algo, all of their condfig panels alter
# the same global
#

import Tkinter, ttk
from llia.synths.algo.algo_constants import *
import llia.synths.algo.algogen.algo_random as rndgen
from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory

_NAME = "Random"


_TAB_FILE = "resources/Tabs/rnd.png"

_BLURB = \
"""
Random Program Generator Options


Engine:
   Selects which generator to use.
   Basic generator -
   Chorus generator - 
      High probability that at least one carrier 
      will have a fixed frequency.

Envelope Type:
   General envelope shape.

Envelope Time:
   General time scale for envelope segments.

Env Changeup:
   Increase likelihood that alternate envelopes, with different
   basic shape and/or time scale, will be selected for some of the
   operators.

Harmonic:
   Probability that only harmonic frequencies will be selected.

Modulation:
   Probability that "deep" modulation indexes will be used.

Feedback:
   Probability that operator feedback will be used."""


class TkProgramGenConfigPanel(TkSubEditor):
    
    def __init__(self,editor):
        frame = editor.create_tab(_NAME, _TAB_FILE)
        frame.config(background=factory.bg())
        self.editor = editor
        TkSubEditor.__init__(self,frame,editor,_NAME)
        editor.add_child_editor(_NAME,self)
        self._layout_engion_selection(frame)
        self._layout_env_type(frame)
        self._layout_env_time(frame)
        self._layout_slider_panel(frame)
        lab_help = factory.label(frame,_BLURB)
        lab_help.grid(row=2,column=0,rowspan=3,columnspan=4)

        
        
    def _layout_engion_selection(self, master):
        var = Tkinter.StringVar()
        frame = factory.frame(master)
        frame.grid(row=1,column=1,sticky='n',padx=8)
        rb_gen_random = factory.radio(frame,"Random",
                                      var,"Random",
                                      command = lambda : rndgen.set_engion("random"))
        rb_gen_basic = factory.radio(frame,"Basic",
                                     var,"Basic",
                                     command = lambda : rndgen.set_engion("basic"))
        rb_gen_chorus = factory.radio(frame,"Chorus",
                                     var,"Chorus",
                                     command = lambda : rndgen.set_engion("chorus"))
        lab = factory.label(frame,"Engion")
        lab.grid(row=0,column=0,sticky='w')
        rb_gen_random.grid(row=1,column=0,sticky='w')
        rb_gen_basic.grid(row=2,column=0,sticky='w')
        rb_gen_chorus.grid(row=3,column=0,sticky='w')

        
        

        
    def _layout_env_type(self, master):
        var = Tkinter.StringVar()
        frame = factory.frame(master)
        frame.grid(row=1,column=2,sticky='n',padx=8)
        def select(n):
            rndgen.gen_config["env-type-hint"] = n
        rb_random = factory.radio(frame,"Random",var,5,
                                  command = lambda : select(None))
        rb_gate = factory.radio(frame,"Gate",var,GATE,
                                command = lambda : select(GATE))
        rb_perc = factory.radio(frame,"Percussive",var,PERCUSSIVE,
                                command = lambda : select(PERCUSSIVE))
        rb_asr = factory.radio(frame,"ASR",var,ASR,
                               command = lambda : select(ASR))
        rb_adsr = factory.radio(frame,"ADSR",var,ADSR,
                                command = lambda : select(ADSR))
       
        lab = factory.label(frame,"Envelope Type")
        lab.grid(row=0,column=0,sticky='w')
        rb_random.grid(row=1,column=0,sticky='w')
        rb_gate.grid(row=2,column=0,sticky='w')
        rb_perc.grid(row=3,column=0,sticky='w')
        rb_asr.grid(row=4,column=0,sticky='w')
        rb_adsr.grid(row=5,column=0,sticky='w')
        
    def _layout_env_time(self, master):
        var = Tkinter.StringVar()
        frame = factory.frame(master)
        frame.grid(row=1,column=3,sticky='n',padx=8)
        def select(n):
            rndgen.gen_config["env-time-hint"] = n
        rb_random = factory.radio(frame,"Random",var,7,
                                  command=lambda : select(None))
        rb_ufast = factory.radio(frame,"Ultra Fast",var,ULTRA_FAST,
                                 command=lambda : select(ULTRA_FAST))
        rb_fast = factory.radio(frame,"Fast",var,FAST,
                                command=lambda : select(FAST))
        rb_med =  factory.radio(frame,"Medium",var,MEDIUM,
                                command=lambda : select(MEDIUM))
        rb_slow = factory.radio(frame,"Slow",var,SLOW,
                                command=lambda : select(SLOW))
        rb_glac = factory.radio(frame,"Glacial",var,GLACIAL,
                                command=lambda : select(GLACIAL))
        lab = factory.label(frame,"Envelope Times")
        lab.grid(row=0,column=0,sticky='w')
        rb_random.grid(row=1,column=0,sticky='w')
        rb_ufast.grid(row=2,column=0,sticky='w')
        rb_fast.grid(row=3,column=0,sticky='w')
        rb_med.grid(row=4,column=0,sticky='w')
        rb_slow.grid(row=5,column=0,sticky='w')
        rb_glac.grid(row=6,column=0,sticky='w')
        self._var_env_changeup = Tkinter.StringVar()
        s = factory.scale(frame,from_=100,to=0,
                          var = self._var_env_changeup,
                          command=self._env_changeup_callback)
        lab = factory.label(frame,"Env Changeup")
        lab.grid(row=0,column=1,sticky='ew',padx=16)
        s.grid(row=1,column=1,rowspan=6,sticky='ns')

    def _env_changeup_callback(self, *_):
        v = float(self._var_env_changeup.get())
        p = v/100.0
        rndgen.gen_config["p-env-changeup"] = p
        self.status("p env changeup = %s" % p)
                          
    def _layout_slider_panel(self,master):
        frame = factory.frame(master)
        frame.grid(row=1,column=4,sticky='n',padx=8)
        self._var_harmonic = Tkinter.StringVar()
        self._var_deepmod = Tkinter.StringVar()
        self._var_feedback = Tkinter.StringVar()
        lab = factory.label(frame,"Harmonic")
        lab.grid(row=0,column=0,sticky='ew',padx=16)
        lab = factory.label(frame,"Modulation")
        lab.grid(row=0,column=1,sticky='ew',padx=16)
        lab = factory.label(frame,"Feedback")
        lab.grid(row=0,column=2,sticky='ew',padx=16)
        sh = factory.scale(frame,from_=100,to=0,
                           var = self._var_harmonic,
                           command = self._harmonic_callback)
        sm = factory.scale(frame,from_=100,to=0,
                           var = self._var_deepmod,
                           command = self._deepmod_callback)
        sf = factory.scale(frame,from_=100,to=0,
                           var = self._var_feedback,
                           command = self._feedback_callback)
        sh.grid(row=1,column=0,rowspan=6,sticky='ns')
        sm.grid(row=2,column=1,rowspan=6,sticky='ns')
        sf.grid(row=3,column=2,rowspan=6,sticky='ns')

    def _harmonic_callback(self,*_):
        v = float(self._var_harmonic.get())
        p = v/100.0
        rndgen.gen_config['p-harmonic'] = p
        self.status("p-harmonic = %s" % p)

    def _deepmod_callback(self,*_):
        v = float(self._var_deepmod.get())
        p = v/100.0
        rndgen.gen_config['p-deep-modulation'] = p
        self.status("p-deep-modulation = %s" % p)

    def _feedback_callback(self,*_):
        v = float(self._var_feedback.get())
        p = v/100.0
        rndgen.gen_config['p-feedback'] = p
        self.status("p-feedback = %s" % p)

