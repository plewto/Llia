# llia.synths.tremolo.tremolo_proxy

from __future__ import print_function

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.tremolo.trm_data import program_bank, pp, random_tremolo


specs = SynthSpecs("Tremolo");

class TremoloProxy(SynthProxy):

    def __init__(self, app, id_):
        super(TremoloProxy, self).__init__(app, specs, id_, program_bank)
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
specs["audio-output-buses"] = (("outbus", 1),)
specs["audio-input-buses"] = (("inbus", 1),)
specs["control-input-buses"] = ("xbus",)
specs["control-output-buses"] = ("lfoOutbus",)
specs["program-generator"] = random_tremolo
specs["pretty-printer"] = pp
specs["pallet"] = tremolo_pallet
specs["help"] = "tremolo"
