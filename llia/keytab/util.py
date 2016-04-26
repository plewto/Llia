# llia.keytab.util
# 2016.03.18

def just_to_list(template, refkey=(69, 440.0)):
    """
    Convert scale template to list of key frequencies.
    
    ARGS:
      template - list, one octave of scale degree ratios.
      refkey   - optional tuple (keynumber, freq), default (69, 440.0).

    RETURNS:
      list - a list of 128 key frequencies.
    """
    length = 128
    acc = [None]*length
    keynum, rfreq = refkey
    acc[keynum] = rfreq
    # octaves above ref key
    octave = 1
    while keynum < length:
        for r in template:
            kfreq = rfreq * r * octave
            if keynum < length:
                acc[keynum] = kfreq
                keynum += 1
            else:
                break
        octave *= 2
    # octaves below ref key
    keynum = refkey[0]
    npo = len(template)
    for kc in range(npo):
        src = keynum+kc
        dst = src - npo
        freq = acc[src]/2.0
        while dst >= 0:
            acc[dst] = freq
            dst -= npo
            freq /= 2
    return acc

def eqtemp_scale_ratio(npo=12, octave=2):
    """
    Calculate step ratio for equal-tempered scale.

    ARGS:
      npo    - int, notes per octave, default 12.
      octave - float, ratio for an octave, default 2.0
    
    RETURNS:
      float.
    """
    ex = 1.0/npo
    return octave**ex

TWELVETH_ROOT_TWO = eqtemp_scale_ratio()

def eqtemp_to_list(npo, octave=2.0, refkey=(69, 440.0)):
    """
    Create list of key frequencies for equal-tempered scale.
    
    ARGS:
      npo    - int, notes per octave
      octave - float, octave ratio, default 2
      refkey - tuple, reference key number and frequency
               default (69, 440.0)
    RETURN:
      list of 128 frequencies.
    """
    length = 128
    acc = [None] * length
    rkey, freq = refkey
    r = eqtemp_scale_ratio(npo, octave)
    acc[rkey] = freq
    for i in range(rkey+1, length):
        freq *= r
        acc[i] = round(freq, 4)
    freq = acc[rkey]
    qr = 1/r
    for i in range(rkey-1, -1, -1):
        freq *= qr
        acc[i] = round(freq, 4)
    return acc


def transpose_reference_key(refkey=(69, 440.0), transpose=-9):
    """
    Transpose key table reference key.
    The most common usage is to transpose A440 at key 69 to middle C on key 60.
    
    ARGS:
      refkey    - Tuple (keynumber, frequency), default (69, 440.0) 
      transpose - int, transposition in key steps, default -9.

    RETURNS:
      tuple (keynumber, frequency)
    """
    akey, afreq = refkey
    scale = TWELVETH_ROOT_TWO**transpose
    ckey, cfreq = akey+transpose, afreq*scale
    return (ckey, cfreq)
