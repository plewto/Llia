# llia.synths.pitchshifter.pitchshifter_proxy

from __future__ import print_function

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.pitchshifter.pitchshifter_data import program_bank,pp
#from llia.synths.pitchshifter.pitchshifter_random import random_program

specs = SynthSpecs("PitchShifter")

class PitchShifterProxy(SynthProxy):

    def __init__(self, app):
        super(PitchShifterProxy, self).__init__(app, specs,program_bank)
        self.app = app
        
    def create_subeditors(self):
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            from llia.synths.pitchshifter.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)


pitchshifter_pallet = Pallet(default_pallet)
pitchshifter_pallet["SLIDER-TROUGH"] = "#400137"
pitchshifter_pallet["SLIDER-OUTLINE"] = "#10400A"

specs["constructor"] = PitchShifterProxy
specs["is-efx"] = True
specs["description"] = "Pitch shift effect with feedback"
specs["keymodes"] = ("EFX", )
specs["pretty-printer"] = pp
# specs["program-generator"] = random_program
specs["help"] = "pitchshifter"
specs["pallet"] = pitchshifter_pallet


specs["audio-output-buses"] = [["outbus1", "out_0"],
                               ["outbus2", "out_1"]]
specs["audio-input-buses"] = [["inbus", "in_0"]]

