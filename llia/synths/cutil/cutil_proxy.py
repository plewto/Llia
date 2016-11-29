# llia.synths.cutil.cutil_proxy

from __future__ import print_function
import llia.constants

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.cutil.cutil_data import program_bank,pp

specs = SynthSpecs("CUtil")

class CUtilProxy(SynthProxy):

    def __init__(self, app):
        super(CUtilProxy, self).__init__(app, specs, program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            from llia.synths.cutil.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            return parent_editor
            
cutil_pallet = Pallet(default_pallet)

specs["constructor"] = CUtilProxy
specs["is-efx"] = False
specs["is-controller"] = True
specs["description"] = "Control signal processor"
specs["keymodes"] = ('Poly1', 'PolyRotate', 'Mono1')
specs["pretty-printer"] = pp   
specs["help"] = "CUtil"
specs["pallet"] = cutil_pallet
specs["audio-output-buses"] = []
specs["audio-input-buses"] = []
specs["control-output-buses"] = [["outbus","null_source"]]
specs["control-input-buses"] = [["inbus","null_sink"]]
print("\t%s" % specs["format"])
llia.constants.CONTROLLER_SYNTH_TYPES.append(specs["format"])
