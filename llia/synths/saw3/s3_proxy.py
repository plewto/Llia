# llia.synths.saw3.s3_proxy
# 2016.06.05

from __future__ import print_function

from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.saw3.s3_data import program_bank
from llia.synths.saw3.s3_pp import pp_saw3
# from llia.synths.orgn.orgn_gen import gen_orgn_program

specs = SynthSpecs("Saw3")

class Saw3Proxy(SynthProxy):

    def __init__(self, app, id_):
        super(Saw3Proxy, self).__init__(app, specs, id_, program_bank)
        gui = app.config["gui"]

specs["constructor"] = Saw3Proxy
specs["description"] = "A 3 Oscillator Subtractive Synth"
specs["pretty-printer"] = pp_saw3  
# specs["program-generator"] = gen_orgn_program
# specs["help"] = "orgn"


