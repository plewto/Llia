# llia.synths.stepfilter.sf_proxy
# 2016.06.11

from __future__ import print_function

from llia.generic import clone
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.stepfilter.sf_data import program_bank
from llia.synths.stepfilter.sf_pp import pp_stepfilter

specs = SynthSpecs("StepFilter")

class StepFilterProxy(SynthProxy):

    def __init__(self, app, id_):
        super(StepFilterProxy, self).__init__(app, specs, id_, program_bank)
        gui = app.config["gui"]
    
specs["constructor"] = StepFilterProxy
specs["description"] = "Filter effect with complex control signal."
specs["audio-output-buses"] = (("outbus", 2),)
specs["audio-input-buses"] = (("inbus", 1),)
specs["is-efx"] = True
specs["pretty-printer"] = pp_stepfilter
specs["help"] = "stepfilter"
