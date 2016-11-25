# llia.util.frange


# Like range except accepts floats.
# - only produces ascending series
#
# r - rounding argument
def frange(start, end, increment=1, r=4):
    star, end = min(start,end), max(start,end)
    acc = []
    x = start
    while x <= end:
        acc.append(round(x, r))
        x += increment
    return acc
    
