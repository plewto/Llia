# llia.synths.tremolo.tremolo_proxy

from __future__ import print_function

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.tremolo.trm_data import program_bank, pp, random_tremolo


specs = SynthSpecs("Tremolo");

class TremoloProxy(SynthProxy):

    def __init__(self, app):
        super(TremoloProxy, self).__init__(app, specs, program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            from llia.synths.tremolo.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)


tremolo_pallet = Pallet(default_pallet)
tremolo_pallet["SLIDER-OUTLINE"] = "#a5a08a"

specs["is-efx"] = True
specs["constructor"] = TremoloProxy
specs["description"] = "Simple amplitude modulation effect (mono)"
specs["keymodes"] = ("EFX",)
specs["program-generator"] = random_tremolo
specs["pretty-printer"] = pp
specs["pallet"] = tremolo_pallet
specs["help"] = "tremolo"

specs["audio-output-buses"] = [["outbus", "out_0"]]
specs["audio-input-buses"] = [["inbus", "in_0"]]
specs["control-input-buses"] = [["xbus","CBUS_B"]]
specs["control-output-buses"] = [["lfoOutbus", "CBUS_A"]]


    
