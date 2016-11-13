# llia.synths.corvus.rndgen.basic
#


from llia.synths.corvus.rndgen.envgen import env,pitch_env
import llia.synths.corvus.rndgen.rutil as ru
from llia.synths.corvus.corvus_data import corvus
from llia.synths.corvus.corvus_constants import *




    


def basic_generator(slot=127,pconfig={}):
    program = corvus(slot,"Basic Random")
    def merge(d):
        for param,value in d.items():
            program[param] = value
    for op in (1,2,3,4):
        merge(env(op, pconfig))
        merge(ru.op_params(op, pconfig))
        merge(ru.fm_params(op, pconfig))
    merge(ru.lfos(pconfig))
    merge(pitch_env())
    return program
    
               
        

