# llia.keytab.keytable
# 2016.03.17
#

from __future__ import print_function

from llia.generic import is_keytable, clone

EQTEMP = 0
JUST = 1
MIXED = 2

class KeyTable(object):

    """
    KeyTable defines mapping between MIDI key-number and frequency.
    """

    def __init__(self, stype, name, refkey=(69, 440.0), npo=None):
        """
        Constructs new KeyTable object.
        
        ARGS:
         stype  - int, indicates the general type of scale.
                  Possible values are EQTEMP, JUST or MIXED.
                  stype is not currently used by Llia.
         name   - String, table name
         refkey - Tuple, defines the reference key (keynumber, frequency).
                  Defaults to A440 (69, 440.0)
         npo    - int, Notes Per Octave. 
        """
        self.scale_type = stype
        self.name = str(name)
        self.notes_per_octave = npo
        self.refkey = refkey
        self._table = [440.0] * len(self)

    def __len__(self):
        return 128

    def __setitem__(self, keynumber, frequency):
        self._table[keynumber] = frequency

    def __getitem__(self, keynumber):
        return self._table[keynumber]

    def __str__(self):
        acc = "KeyTable '%s'  scale-type %s  ref %s  npo %s"
        acc = acc % (self.name, self.scale_type, self.refkey,
                     self.notes_per_octave)
        return acc

    def clone(self):
        other = KeyTable(self.scale_type, self.name,
                         self.refkey, self.notes_per_octave)
        for k,f in enumerate(self._table):
            other[k] = f
        return other

    def __eq__(self, other):
        if self is other:
            return True
        else:
            if is_keytable(other) and len(other) == len(self):
                flag, keynum, limit = True, 0, len(self)
                while flag and keynum < limit:
                    flag = self[keynum] == other[keynum]
                    keynum += 1
                return flag
            else:
                return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def serialize(self):
        """
        Convert self to serialized form.

        RETURNS:
          String
        """
        n = len(self)
        acc = ["llia.KeyTable",
               {"format" : 0,
                "length" : n,
                "scale-type" : self.scale_type,
                "name" : self.name,
                "notes-per-octave" : self.notes_per_octave,
                "refkey" : self.refkey},
               self._table[:]]
        return acc

    @staticmethod
    def deserialize(obj):
        """
        Use serialized data to construct new KeyTable.
        
        ARGS:
          obj - String

        RETURNS:
          KeyTable

        Raises TypeError if obj is not a String or is a String with wrong 
        format.
        """
        clss = obj[0]
        if clss == "llia.KeyTable":
            header, data = obj[1], obj[2]
            ktab = KeyTable(header["scale-type"], header["name"],
                            header["refkey"], header["notes-per-octave"])
            ktab._table = data
            return ktab
        else:
            msg = "Can not deserilize %s as Llia KeyTable"
            msg = msg % obj
            raise TypeError(msg)

    def dump(self, tab=0):
        pad = ' '*tab*4
        acc = "%s%s\n" % (pad, self)
        npo = self.notes_per_octave or 12
        for pc in range(npo):
            acc += "%s[%3d] " % (pad, pc)
            keynum = pc
            while keynum < len(self):
                freq = round(self[keynum], 4)
                acc += "%5.4f " % freq
                keynum += npo
            acc += '\n'
        return acc
        
        

@is_keytable.when_type(KeyTable)
def _is_keytab(obj):
    return True

@clone.when_type(KeyTable)
def _clone_keytab(obj):
    return obj.clone()
