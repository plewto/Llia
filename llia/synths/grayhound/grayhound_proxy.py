# llia.synths.grayhound.grayhound_proxy

from __future__ import print_function

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.grayhound.grayhound_data import program_bank,pp
#from llia.synths.grayhound.grayhound_random import grayhound_random

specs = SynthSpecs("Grayhound")

class GrayhoundProxy(SynthProxy):

    def __init__(self, app):
        super(GrayhoundProxy, self).__init__(app, specs, program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            from llia.synths.grayhound.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            return parent_editor
            
grayhound_pallet = Pallet(default_pallet)
grayhound_pallet["SLIDER-TROUGH"] = "#262323"
grayhound_pallet["SLIDER-OUTLINE"] = "#401E3F"

specs["constructor"] = GrayhoundProxy
specs["is-efx"] = True
specs["is-controller"] = False
specs["description"] = "Filter and Envelope Follower effect"
specs["keymodes"] = ('Efx',)
specs["pretty-printer"] = pp   
#specs["program-generator"] = grayhound_random
specs["help"] = "Grayhound"
specs["pallet"] = grayhound_pallet
specs["audio-output-buses"] = [["outbus", "out_0"]]
specs["audio-input-buses"] = [["inbus","in_0"]]
specs["control-output-buses"] = [["envout", "null_source"]]
specs["control-input-buses"] = [["xbus", "null_sink"]]
