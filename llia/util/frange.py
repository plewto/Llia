# llia.util.frange


# Like range except accepts floats.
# - only produces ascending series
#
# r - rounding argument
def frange(start, end, increment=1, r=4):
    """
    frange is an extension of range which accepts floats.

    start - starting value
    end - ending value
    increment - optional step size, default 1
    r - optional, rounding decimal point, default 4

    Returns list.

    WARNING: frange may only ascending sequences. 
    WARNING: If increment is negative, frange never terminates.
    ISSUE: Fix This!
    """
    star, end = min(start,end), max(start,end)
    acc = []
    x = start
    while x <= end:
        acc.append(round(x, r))
        x += increment
    return acc
    
