# llia.synths.locus.locus_proxy

from __future__ import print_function
import llia.constants
from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.locus.locus_data import program_bank
from llia.synths.locus.locus_pp import locus_pp
from llia.synths.locus.locus_random import locus_random

specs = SynthSpecs("Locus")

class LocusProxy(SynthProxy):

    def __init__(self, app):
        super(LocusProxy,self).__init__(app,specs,program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            from llia.synths.locus.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            return parent_editor

pallet = Pallet(default_pallet)
#pallet["BACKGROUND"] =  
pallet["SLIDER-OUTLINE"] = "#777f86"
pallet["SLIDER-TROUGH"] = "#2d242d"
specs["constructor"] = LocusProxy
specs["description"] = "Vector synth"
specs["help"] = "Locus"
specs["pretty-printer"] = locus_pp
specs["program-generator"] = locus_random
specs["pallet"] = pallet
specs["is-efx"] = False
specs["is-controller"] = False
specs["keymodes"] = ("PolyN","PolyRotate","Poly1","Mono1","MonoExclusive")
specs["audio-output-buses"] = [["outbus","out_0"],["xoutbus", "out_2"],["youtbus","out_2"]]
specs["audio-input-buses"] = []
specs["control-output-buses"] = []
specs["control-input-buses"] = [["xbus","null_sink"],["ybus","null_sink"]]
print("\t%s" % specs["format"])
llia.constants.SYNTH_TYPES.append(specs["format"])
