# llia.synths.saw3.s3_proxy
# 2016.06.05

from __future__ import print_function

from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.saw3.s3_data import program_bank
from llia.synths.saw3.s3_pp import pp_saw3
from llia.synths.saw3.s3_gen import s3gen

specs = SynthSpecs("Saw3")

class Saw3Proxy(SynthProxy):

    def __init__(self, app, id_):
        super(Saw3Proxy, self).__init__(app, specs, id_, program_bank)
        gui = app.config["gui"]

specs["constructor"] = Saw3Proxy
specs["description"] = "A 3 Oscillator Subtractive Synth"
specs["audio-output-buses"] = (("outbus", 1),)
specs["pretty-printer"] = pp_saw3  
specs["program-generator"] = s3gen
specs["help"] = "saw3"


