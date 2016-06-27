# llia.synths.dirtyburger.dirty_proxy
# 2016.04.26

from __future__ import print_function

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.dirtyburger.dirty_data import program_bank
from llia.synths.dirtyburger.dirty_pp import pp_dirty

specs = SynthSpecs("DirtyBurger")

class DirtyProxy(SynthProxy):

    def __init__(self, app, id_):
        super(DirtyProxy, self).__init__(app, specs, id_, program_bank)
        self.app = app
        
    def create_subeditors(self):
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            from llia.synths.dirtyburger.tk.dirty_ed import create_tk_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_tk_editor(parent_editor)
            

dirty_pallet = Pallet(default_pallet)
dirty_pallet["SLIDER-TROUGH"] = "#2C3742"

specs["constructor"] = DirtyProxy
specs["description"] = "An unclean delay"
specs["audio-output-buses"] = (("outbus", 2),)
specs["audio-input-buses"] = (("inbus", 1),)
specs["pretty-printer"] = pp_dirty
specs["is-efx"] = True
specs["help"] = "dirtyburger"
specs["pallet"] = dirty_pallet
