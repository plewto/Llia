# llia.keytab.registry
# 2016.03.18

from __future__ import print_function
import json

from llia.generic import is_keytable, dump
from llia.keytab.keytable import KeyTable
import llia.keytab.eqtemp as eqt
import llia.keytab.just as jst


class KeyTableRegistry(dict):

    """KeyTableRegistry provides dictionary of KeyTable objects."""
    
    @staticmethod
    def extension():
        """Returns String, the filename extension."""
        return "ktr"
    
    def __init__(self):
        """Constructs new KeyTableRegistry."""
        dict.__init__(self)
        self.clear()
        self._filename = ""

    def __setitem__(self, key, ktab):
        """
        Add KeyTable to registry.
        Raises TypeError if ktab is not a KeyTable object.
        """
        if is_keytable(ktab):
            key = key or ktab.name
            dict.__setitem__(self, key, ktab)
        else:
            msg = "Can not add %s to KeyTableRegistry"
            msg = msg % type(ktab)
            raise TypeError(msg)

    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            return eqt.EQ12

    def clear(self):
        """Remove all but default key tables."""
        dict.clear(self)
        self[None] = eqt.EQ12
        self[None] = eqt.EQ19
        self[None] = eqt.EQ24
        self[None] = eqt.EQ31
        self[None] = jst.JUST_C1
        self[None] = jst.S44_39_12
        self[None] = jst.BLUE_JI
        self[None] = jst.PRE_ARCHYTAS
        self[None] = jst.BICYCLE
        self[None] = jst.BREEDBALL3
        self[None] = jst.AL_FARABI
        self[None] = jst.CANTON
        self[None] = jst.CARLOS_HARM
        self[None] = jst.CENTAUR
        self[None] = jst.COLLAPSAR
        self[None] = jst.MAJOR_CLUS
        self[None] = jst.MINOR_CLUS
        self[None] = jst.THIRTEENDENE
        self[None] = jst.UNIMAJOR
        
    def reset(self):
        """reset is an alias for clear."""
        self.clear()

    def eqtemp(self, npo, name=None, refkey=(69, 440.0),
               octave=2.0):
        """
        Adds equal-tempered key table to registry.

        ARGS:
          name      - String, table name.  If name is "" or None a default 
                      name based on note-count is used.
          npo       - int, notes per octave.
          refkey    - optional tuple, reference keynumber and frequency used
                      to tune the table.  Default (69, 440.0)
          octave    - optional float, sets ratio used for an octave. Default 2.0

        RETURNS:
          KeyTable
        """
        ktab = eqt.EqTempKeyTable(name, npo, refkey, 0, octave)
        self[ktab.name] = ktab
        return ktab

    def just(self, template, name, refkey=(69, 440.0),
             transpose=-9, npo=12):
        """
        Adds key table with just intonation to registry.

        ARGS:
          template  - Nested list of scale degree ratios
                      ((n0, d0),(n1,d1),(n2, d2)...)
                      where each ni, di define the ratio of step i 
                      as the fraction ni/di.
          name      - String
          refkey    - optional tuple, (keynumber, frequency), 
                      default (69, 440.0)
          transpose - optional int, transposition amount.
                      See JustKeyTable docs.  Default -9
          npo       - optional int, notes per octave.  npo is informational 
                      only, the actual number of notes per octave is 
                      determined by template.  Default 12

        RETURNS:
          KeyTable
        """
        ktab = jst.JustKeyTable(name, template, refkey, npo, transpose)

        self[name] = ktab
        return ktab

    def __str__(self):
        return "KeyTableRegistry"

    def dump(self, tab=0, verbosity=0):
        pad=' '*4*tab
        pad2 = pad+' '*4
        acc = "%s%s\n" % (pad, str(self))
        for k in sorted(list(self.keys())):
            acc += "%s%s\n" % (pad2, k)
        return acc

    def serialize(self):
        """Convert to serialized form."""
        acc = ["llia.KeyTableRegistry"]
        header = {}
        header["count"] = len(self)
        acc.append(header)
        data = {}
        for kname in sorted(list(self.keys())):
            ktab = self[kname]
            data[kname] = ktab.serialize()
        acc.append(data)
        return acc

    def default_filename(self):
        return self._filename
    
    def save(self, filename):
        """Save self to file."""
        with open(filename, 'w') as output:
            s = self.serialize()
            json.dump(s, output, indent=4)
            self._filename = filename

    @staticmethod
    def deserialize(obj):
        """Construct KeyTableRegistry from serialized data."""
        cls = obj[0]
        if cls == "llia.KeyTableRegistry":
            header, data = obj[1], obj[2]
            other = KeyTableRegistry()
            for name, ktab in data.items():
                other[name] = KeyTable.deserialize(ktab)
            return other
        else:
            msg = "Can not deserialize %s as KeyTableRegistry"
            msg = msg % obj
            raise TypeError(msg)

    def load(self, filename):
        """
        Update self from external file.
        All non-default tables are removed and replaced by those
        in the file.
        """
        with open(filename, 'r') as input:
            obj = json.load(input)
            if type(obj) == list:
                other = self.deserialize(obj)
                self.clear()
                self._filename = filename
                for name, ktab in other.items():
                    self[name] = ktab
    
        
@dump.when_type(KeyTableRegistry)
def _dump(ktr):
    print(ktr.dump())

#  ---------------------------------------------------------------------- 
#                                    Test

def test():
    print("KeyTableRegistry test")
    r = KeyTableRegistry()
    dump(r)
    r.eqtemp(56)
    template = ((1, 1),(13, 12),(14,12),(15,12),
                (16,12),(17,12),(18,12),(19,12),
                (20,12),(21,21),(22, 12),(23,12))
    r.just(template, "zzz")
    dump(r)
    # filename = "/home/sj/t/keytab"
    # r.save(filename)
    # r2 = KeyTableRegistry()
    # dump(r2)
    # r2.load(filename)
    # dump(r2)
