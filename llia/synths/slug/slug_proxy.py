# llia.synths.slug.slug_proxy

from __future__ import print_function
import llia.constants
from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.slug.slug_data import program_bank
from llia.synths.slug.slug_pp import slug_pp
from llia.synths.slug.slug_random import slug_random

specs = SynthSpecs("Slug")

class SlugProxy(SynthProxy):

    def __init__(self, app):
        super(SlugProxy,self).__init__(app,specs,program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config()["gui"].upper()
        if gui == "TK":
            from llia.synths.slug.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            return parent_editor

pallet = Pallet(default_pallet)
#pallet["BACKGROUND"] =  
#pallet["SLIDER-OUTLINE"] = 
#pallet["SLIDER-TROUGH"] = 
specs["constructor"] = SlugProxy
specs["description"] = "Hybrid synth"
specs["help"] = "Slug"
specs["pretty-printer"] = slug_pp
specs["program-generator"] = slug_random
specs["pallet"] = pallet
specs["is-efx"] = False
specs["is-controller"] = False
specs["keymodes"] = ("PolyN","PolyRotate","Poly1","Mono1","MonoExclusive")
specs["audio-output-buses"] = [["outbus","out_0"]]
specs["audio-input-buses"] = []
specs["control-output-buses"] = [["xbus","null_sink"]]
specs["control-input-buses"] = []
llia.constants.SYNTH_TYPES.append(specs["format"])
