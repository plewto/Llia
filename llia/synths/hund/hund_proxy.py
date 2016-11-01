# llia.synths.hund.hund_proxy

from __future__ import print_function

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.hund.hund_data import program_bank,pp
#from llia.synths.hund.hund_random import hund_random

specs = SynthSpecs("Hund")

class HundProxy(SynthProxy):

    def __init__(self, app):
        super(HundProxy, self).__init__(app, specs, program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            from llia.synths.hund.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            return parent_editor
            
hund_pallet = Pallet(default_pallet)
hund_pallet["SLIDER-TROUGH"] = "#262323"
hund_pallet["SLIDER-OUTLINE"] = "#401E3F"

specs["constructor"] = HundProxy
specs["is-efx"] = True
specs["is-controller"] = False
specs["description"] = "Filter and Envelope Follower effect"
specs["keymodes"] = ('Efx',)
specs["pretty-printer"] = pp   
#specs["program-generator"] = hund_random
specs["help"] = "Hund"
specs["pallet"] = hund_pallet
specs["audio-output-buses"] = [["outbus", "out_0"]]
specs["audio-input-buses"] = [["inbus","in_0"]]
specs["control-output-buses"] = [["envout", "null_source"]]
specs["control-input-buses"] = [["xbus", "null_sink"]]
