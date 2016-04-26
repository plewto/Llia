# llia.keytab.just
# 2016.03.18
#
# Just scale sources:
# http://xenharmonic.wikispaces.com/Gallery+of+12-tone+Just+Intonation+Scales
# http://www.chrysalis-foundation.org/Al-Farabi-s_Uds.htm
#

from fractions import Fraction 

from llia.keytab.keytable import KeyTable, JUST
from llia.keytab.util import just_to_list, transpose_reference_key

def reduce_ratios(lst, acc):
    """
    Converts nested list of rational values to list of floats.

    ARGS:
      lst - A nested list of rational values of the form 

            ((n0, d0),(n1, d1),(n2, d2) ...) 

            Where each ni and di are numerator and denominator respectively 
            which defines the ratio of step i relative to i=0.

      acc - list, used for recursive call, should be an empty list []

    RETURNS:
      list of floats.
    """
    if lst:
        n, d = lst[0]
        r = Fraction(n,d)
        f = float(r)
        acc.append(f)
        return reduce_ratios(lst[1:], acc)
    else:
        return acc

class JustKeyTable(KeyTable):

    """Extends KeyTable for scales with just intonation."""
    
    def __init__(self, name, template, refkey=(69, 440.0), npo=12, transpose=-9):
        """
        Constructs new JustKeyTable.

        ARGS:
          name     - String.
          template - Nested list of scale degree ratios. The list should 
                     have the form ((n0, d0),(n1,d1),(n2,d2)...) where each
                     ni and di define a fraction ni/di.
          refkey   - optional tuple, sets reference key frequency,
                     (keynumber, frequency), default (69, 440) for A440.
          npo      - optional int, notes per octave.  npo is informational 
                     only.  The actual number of notes per octave is 
                     determined by the template list.
          transpose- optional int, sets reference key transposition in
                     half-steps.  The transposition is applied using 
                     equal-tempered ratios.  For example using the default
                     refkey (69, 440.0) a transposition of -9 sets the 
                     reference key to middle C (60) with a frequency ~261.6
                     This value for C will be in agreement with an 
                     equal-tempered scale tuned to A440.  Depending on how it
                     is defined by the template, the transposed value of the 
                     A on key 69 may no longer be at 440.

                     The default transpositons of -9 and refkey (69, 440)
                     produce just scales in the key of C.
        """
        refkey = transpose_reference_key(refkey, transpose)
        KeyTable.__init__(self, JUST, name, refkey, npo)
        template = reduce_ratios(template, [])
        for k,f in enumerate(just_to_list(template, refkey)):
            self[k] = f


# A few default just scales.
#
_JUST_C1       = ((1,1),(16,15),(9,8),(6,5),(5,4),(4,3),(36,25),(3,2),(8,5),(5,3),(9,5),(15,8))
_S44_39_12     = ((1,1),(14,13),(44,39),(13,11),(14,11),(4,3),(56,39),(3,2),(11,7),(22,13),(39,22),(21,11))
_BLUE_JI       = ((1,1),(15,14),(9,8),(6,5),(5,4),(4,3),(7,5),(3,2),(8,5),(5,3),(9,5),(15,8))
_PRE_ARCHYTAS  = ((1,1),(16,15),(9,8),(6,5),(5,4),(4,3),(64,45),(3,2),(8,5),(5,3),(16,9),(15,8))
_BICYCLE       = ((1,1),(13,12),( 9, 8),( 7, 6),( 5, 4),(4,3),(11,8),( 3,2),(13,8),( 5, 3),( 7,4),(11,6))
_BREEDBALL3    = ((1,1),(49,48),(21,20),(15,14),(48,40),(5,4),( 7,5),(10,7),( 3,2),(49,32),(12,7),( 7,4))
_AL_FARABI     = ((1,1),(256,243),(9,8),(32,27),(81,64),(4,3),(1024,729),(3,2),(128,81),(27,16),(7,4),(16,9))
_CANTON        = ((1,1),(14,13),(9,8),(13,11),(14,11),(4,3),(39,28),(3,2),(11,7),(22,13),(16,9),(13,7))
_CARLOS_HARM   = ((1,1),(17,16),(9,8),(19,16),(5,4),(21,16),(11,8),(3,2),(13,8),(27,16),(7,4),(15,8))
_CENTAUR       = ((1,1),(21,20),(9,8),(7,6),(5,4),(4,3),(7,5),(3,2),(14,9),(5,3),(7,4),(15,8))
_COLLAPSAR     = ((1,1),(15,14),(49,44),(7,6),(5,4),(15,11),(7,5),(3,2),(35,22),(5,3),(7,4),(21,11))
_MAJOR_CLUS    = ((1,1),(135,128),(10,9),(9,8),(5,4),(4,3),(45,32),(3,2),(5,3),(27,16),(16,9),(15,8))
_MINOR_CLUS    = ((1,1),(16,15),(9,8),(6,5),(4,3),(27,20),(46,45),(3,2),(8,5),(27,16),(16,9),(9,5))
_THIRTEENDENE  = ((1,1),(13,12),(9,8),(6,5),(9,7),(27,20),(13,9),(3,2),(8,5),(27,16),(9,5),(27,14))
_UNIMAJOR     = ((1,1),(22,21),(9,8),(32,27),(14,11),(4,3),(63,44),(3,2),(11,7),(27,16),(16,9),(21,11))

JUST_C1 = JustKeyTable("just_c1", _JUST_C1)
S44_39_12 = JustKeyTable("44_39_12", _S44_39_12)
BLUE_JI = JustKeyTable("blue_ji", _BLUE_JI)
PRE_ARCHYTAS = JustKeyTable("pre_archytas", _PRE_ARCHYTAS)
BICYCLE = JustKeyTable("bicycle", _BICYCLE)
BREEDBALL3 = JustKeyTable("breedball3", _BREEDBALL3)
AL_FARABI = JustKeyTable("al_farabi", _AL_FARABI)
CANTON = JustKeyTable("canton", _CANTON)
CARLOS_HARM = JustKeyTable("carlos_harm", _CARLOS_HARM)
CENTAUR = JustKeyTable("centaur", _CENTAUR)
COLLAPSAR = JustKeyTable("collapsar", _COLLAPSAR)
MAJOR_CLUS = JustKeyTable("major_clus", _MAJOR_CLUS)
MINOR_CLUS = JustKeyTable("minor_clus", _MINOR_CLUS)
THIRTEENDENE = JustKeyTable("thirteendene", _THIRTEENDENE)
UNIMAJOR = JustKeyTable("unimajor", _UNIMAJOR)
