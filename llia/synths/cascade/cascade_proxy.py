# llia.synths.cascade.cascade_proxy

from __future__ import print_function
import llia.constants
from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.cascade.cascade_data import program_bank, pp, random_cascade

specs = SynthSpecs("Cascade")

class CascadeProxy(SynthProxy):

    def __init__(self, app):
        super(CascadeProxy, self).__init__(app,specs,program_bank)
        self.app = app
        
    def create_subeditors(self):
        pass
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            from llia.synths.cascade.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)

            
cascade_pallet = Pallet(default_pallet)
cascade_pallet["SLIDER-TROUGH"] = "#49495c"
cascade_pallet["SLIDER-OUTLINE"] = "#5c4952"




specs["constructor"] = CascadeProxy
specs["description"] = "Pulse Divider Cascade"
specs["keymodes"] = ("EFX", )

specs["pretty-printer"] = pp
specs["program-generator"] = random_cascade
specs["is-efx"] = True
specs["is-controller"] = True
specs["help"] = "CASCADE"
specs["pallet"] = cascade_pallet


specs["control-input-buses"] = [["clkin","null_sink"],
                                ["xgate","null_zero"]]
specs["control-output-buses"] = [["outbus","null_source"],
                                 ["out1","null_source"],
                                 ["out2","null_source"],
                                 ["out3","null_source"],
                                 ["out4","null_source"],
                                 ["out5","null_source"],
                                 ["out6","null_source"],
                                 ["outn","null_source"]]
                                 
print("\t%s" % specs["format"])
llia.constants.CONTROLLER_SYNTH_TYPES.append(specs["format"])
