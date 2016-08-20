# llia.synths.ghostbus.ghost_proxy

from __future__ import print_function

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.ghostbus.ghost_data import program_bank, pp, random_ghostbus

specs = SynthSpecs("Ghostbus")

class GhostbusProxy(SynthProxy):

    def __init__(self, app, id_):
        super(GhostbusProxy, self).__init__(app, specs, id_, program_bank)
        self.app = app
        
    def create_subeditors(self):
        pass
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            from llia.synths.ghostbus.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            

ghostbus_pallet = Pallet(default_pallet)

specs["constructor"] = GhostbusProxy
specs["description"] = "Simple sine LFO"
specs["keymodes"] = ("EFX", )
specs["audio-output-buses"] = []
specs["audio-input-buses"] = []
specs["control-input-buses"] = ("inbus",)
specs["control-output-buses"] = ("outbus",)
specs["pretty-printer"] = pp
specs["program-generator"] = random_ghostbus
specs["is-efx"] = True
specs["help"] = "GHOSTBUS"
specs["pallet"] = ghostbus_pallet
