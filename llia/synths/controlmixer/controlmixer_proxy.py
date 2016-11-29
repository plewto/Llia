# llia.synths.controlmixer.ghost_proxy

from __future__ import print_function

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.controlmixer.controlmixer_data import program_bank, pp

specs = SynthSpecs("ControlMixer")

class ControlmixerProxy(SynthProxy):

    def __init__(self, app):
        super(ControlmixerProxy, self).__init__(app, specs, program_bank)
        self.app = app
        
    def create_subeditors(self):
        pass
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            from llia.synths.controlmixer.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            

controlmixer_pallet = Pallet(default_pallet)
controlmixer_pallet["SLIDER-TROUGH"] = "#432703"
controlmixer_pallet["SLIDER-OUTLINE"] = "#42033E"

specs["constructor"] = ControlmixerProxy
specs["description"] = "Combines up to 4 control signals"
specs["keymodes"] = ("EFX", )
specs["pretty-printer"] = pp
#specs["program-generator"] = 
specs["is-efx"] = True
specs["is-controller"] = True
specs["help"] = "Controlmixer"
specs["pallet"] = controlmixer_pallet
specs["control-input-buses"] = [["inbusA","null_sink"],
                                ["inbusB","null_sink"],
                                ["inbusC","null_sink"],
                                ["inbusD","null_sink"]]
specs["control-output-buses"] = [["outbus","null_source"]]
