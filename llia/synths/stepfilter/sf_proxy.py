# llia.synths.stepfilter.sf_proxy
# 2016.06.11

from __future__ import print_function

from llia.generic import clone
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.stepfilter.sf_data import program_bank
from llia.synths.stepfilter.sf_pp import pp_stepfilter
from llia.synths.stepfilter.sf_gen import gen_stepfilter_program

specs = SynthSpecs("StepFilter")

class StepFilterProxy(SynthProxy):

    def __init__(self, app, id_):
        super(StepFilterProxy, self).__init__(app, specs, id_, program_bank)
        self._editors = None

    def create_subeditors(self):
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            from llia.synths.stepfilter.tk.sf_editor import create_stepfilter_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_stepfilter_editor(parent_editor)

        
        
specs["constructor"] = StepFilterProxy
specs["description"] = "Filter effect with complex control signal."
specs["keymodes"] = ("EFX",)
specs["audio-output-buses"] = (("outbus", 2),)
specs["audio-input-buses"] = (("inbus", 1),)
specs["program-generator"] = gen_stepfilter_program
specs["is-efx"] = True
specs["pretty-printer"] = pp_stepfilter
specs["help"] = "stepfilter"
