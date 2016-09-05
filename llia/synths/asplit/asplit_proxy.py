# llia.synths.asplit.asplit_proxy

from __future__ import print_function

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.asplit.asplit_data import program_bank, pp

specs = SynthSpecs("ASplit")

class ASplitProxy(SynthProxy):

    def __init__(self, app, id_):
        super(ASplitProxy, self).__init__(app, specs, id_, program_bank)
        self.app = app
        
    def create_subeditors(self):
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            from llia.synths.asplit.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            

asplit_pallet = Pallet(default_pallet)
asplit_pallet["SLIDER-TROUGH"] = "#432703"
asplit_pallet["SLIDER-OUTLINE"] = "#42033E"

specs["constructor"] = ASplitProxy
specs["description"] = "Split audio signal to 4 separate buses"
specs["keymodes"] = ("EFX", )
specs["audio-output-buses"] = (("outbusA", 1),("outbusB", 1),
                               ("outbusC", 1),("outbusD", 1))
specs["audio-input-buses"] = (("inbus", 1),)
specs["control-input-buses"] = tuple()
specs["control-output-buses"] = tuple()
specs["pretty-printer"] = pp
specs["program-generator"] = None
specs["is-efx"] = True
specs["help"] = "ASplit"
specs["pallet"] = asplit_pallet
