# llia.keytab.eqtemp
# 2016.03.17

from __future__ import print_function

from llia.keytab.keytable import (KeyTable, EQTEMP)
from llia.keytab.util import (eqtemp_to_list, eqtemp_scale_ratio, transpose_reference_key)


class EqTempKeyTable(KeyTable):

    """Extends KeyTable for equal-tempered scales."""
    
    def __init__(self, name, npo, refkey=(69, 440.0), transpose=0, octave=2.0):
        """
        Constructs new EqTempKeyTable

        ARGS:
         name   - String. If string is "" or None, name is automatically 
                  generated form note count.
         npo    - int, notes per octave.
         refkey - optional tuple, sets reference keynumber and frequency.
                  Default (69, 440.0)
         transpose - optional int,transpose reference key, default 0
         octave - optional float, sets ratio used for an octave, default 2.0
        """
        refkey = transpose_reference_key(refkey, transpose)
        if not name:
            name = "EQ%d" % npo
        KeyTable.__init__(self, EQTEMP, name, refkey, npo)
        for k,f in enumerate(eqtemp_to_list(npo, octave, refkey)):
            self[k] = f
            

EQ12 = EqTempKeyTable("EQ12", 12, transpose=0)
EQ19 = EqTempKeyTable("EQ19", 19, transpose=0)
EQ24 = EqTempKeyTable("EQ24", 24, transpose=0)
EQ31 = EqTempKeyTable("EQ31", 31, transpose=0)
