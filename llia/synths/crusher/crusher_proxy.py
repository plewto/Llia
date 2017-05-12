# llia.synths.crusher.crusher_proxy

from __future__ import print_function
import llia.constants

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.crusher.crusher_data import program_bank,pp


specs = SynthSpecs("Crusher")

class CrusherProxy(SynthProxy):

    def __init__(self, app):
        super(CrusherProxy, self).__init__(app, specs,program_bank)
        self.app = app
        
    def create_subeditors(self):
        gui = self.app.config()["gui"].upper()
        if gui == "TK":
            from llia.synths.crusher.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)

crusher_pallet = Pallet(default_pallet)
crusher_pallet["SLIDER-TROUGH"] = "black"
crusher_pallet["SLIDER-OUTLINE"] = "blue"
specs["constructor"] = CrusherProxy
specs["is-efx"] = True
specs["description"] = "Sample degrade & distortion effect"
specs["keymodes"] = ("EFX", )
specs["pretty-printer"] = pp
# specs["program-generator"] = random_program
specs["help"] = "crusher"
specs["pallet"] = crusher_pallet
specs["audio-output-buses"] = [["outbus", "out_0"]]
specs["audio-input-buses"] = [["inbus","in_0"]]
llia.constants.EFFECT_TYPES.append(specs["format"])
