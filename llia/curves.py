# llia.curves
# 2016.03.19

from math import tanh

def identity(x, *ignore):
    """Returns it's argument, identity(x) --> x."""
    return x

def bipolar_to_unipolar(x):
    """
    Maps "normalized" value on bipolar domain (-1.0, 1.0) to 
    unipolar range_ (0.0, 1.0).
    """
    a = b = 0.5
    return x*a+b

def unipolar_to_bipolar(x):
    """
    Maps "normalized" value unipolar domain (0.0, 1.0) to 
    bipolar range_ (-1.0, 1.0).
    """
    a, b = 2, -1
    return x*a+b

def clip(x, mn, mx):
    """
    Limit value between minimum and maximum values:

    ARGS:
       x  - number, the value to limit.
       mn - number, the minimum value.
       mx - number, the maximum value, mn <= mx
    
    RETURNS:
       number, for x < mn --> mn
               for x > mx --> mx
               otherwise  --> x
    """
    return min(max(x, mn), mx)

def clipper(mn, mx):
    """
    Return function to clip value between minimum and maximum.
    
    ARGS:
       mn - number, the minimum value.
       mx - number, the maximum value, mn <= mx.

    RETURNS:
      Function f(x) such that 
               f(x<=mn) --> mn
               f(mx<=x) --> mx
               f(mn < x < mx) --> x
    """
    mn, mx = min(mn,mx), max(mn,mx)
    def f(x):
        y = min(max(mn, x), mx)
        return y
    return f


def linear_coefficients(domain, range_):
    """
    Determine linear coefficients for domain and range_.

    ARGS:
        domain   - tuple, (x0, x1), x0 != x1
        range_ - tuple, (y0, y1)

    RETURNS:
        tuple (a,b) where a is the slope and b the intercept 
        of a linear function between domain and range_.

    Raises: 
        ZeroDivisionError if x0 == x1.
    """
    x0, x1 = domain
    y0, y1 = range_
    dx = float(x1 - x0)
    dy = float(y1 - y0)
    a = dy/dx
    b = y0-a*x0
    return (a,b)

def linear_function(domain, range_):
    """
    Returns linear function between domain and range_.

    ARGS:
        domain   - tuple, (x0, x1), x0 != x1
        range_ - tuple, (y0, y1)

    RETURNS:
        function f(x) such that f(x0) = y0 and f(x1) = y1.

    Raises:
       ZeroDivisionError if x0 == x1.
    """
    a,b = linear_coefficients(domain, range_)
    def f(x):
        return a*x+b
    return f

def normal_exp_curve(x, n=1):
    """
    Maps "normalized" domain (0.0, 1.0) to range_ (0.0, 1.0) with 
    exponential curve.

    ARGS:
        x - float, 0.0 <= x <= 1.0.
        n - float, sets curve steepness and concavity. 
            The sign of n determines concavity: 
                n < 0  --> concave 
                0 < n  --> convex 
            The magnitude of n sets curve degree. degree = 2**|n|
                |n| == 0 --> degree 1, linear
                |n| == 1 --> degree 2, quadratic
                |n| == 2 --> degree 4, quartic
                etc...
    RETURNS:
       float on range_ (0.0, 1.0).  The output value will be outside of
       this range for x < 0 or 1 < x.
    """
    degree = 2**n
    return x**degree



# tanh_comp function
# Amplitude compensation for s-curve
#
def _s_comp(n):
    a,b =  -0.2757, 1.5888
    return max(min(a*n+b, 1.313), 1.037)

def normal_s_curve(x, n=1):
    """
    Maps "normalized" domain (0.0, 1.0) to range_ (0.0, 1.0) using 
    hyperbolic tangent for an "s" shaped curve.

    ARGS:
       x - float, 0.0 <= x <= 1.0
       n - float, curve steepness. The value n sets the sharpness of the 
           curve with higher values producing steeper transitions.  n is
           scaled to produce a useful range for n > 0. Negative n values
           are allowed for compatibility with the function normal_exp_curve,
           but the absolute value is used. -n and +n have the same effect.
           For |n| <= 1, the curve is nearly linear. 
     
    RETURNS:
       float on range_ (0.0, 1.0).  The output value will be outside of
       this range for x < 0 or 1 < x.
    """
    a,b = 2, -1
    x = (a*x+b)
    n = max(abs(n+1), 1)
    y = min(max(0.5*_s_comp(n)*tanh(n*x)+0.5, 0), 1)
    return y

def normal_step_curve(x, n=4):
    """
    Maps "normalized" domain (0.0, 1.0) to range_ (0.0, 1.0) using 
    discreet steps.

    ARGS:
       x - float, 0.0 <= x <= 1.0
       n - int, |n| >= 2, number of steps. 
           Negative values of causes output values to be "stretched" to 
           (0.0, 1.0).
               example n=4,  fn(0.00 <= x < 0.25) --> 0.00
                             fn(0.25 <= x < 0.50) --> 0.25
                             fn(0.50 <= x < 0.75) --> 0.50
                             fn(0.75 <= x < 1.00) --> 0.75
               example n=-4  fn(0.00 <= x < 0.25) --> 0.00
                             fn(0.25 <= x < 0.50) --> 0.33
                             fn(0.50 <= x < 0.75) --> 0.67  
                             fn(0.75 <= x < 1.00) --> 1.00
    RETURNS:
       float on range_ (0.0, 1.0). 
    """
    stretch = n < 0
    n = max(abs(n), 2)
    y = int(x*n)
    y /= float(n)
    if stretch:
        y *= n/(n-1.0)
    return y

def default_modifier_value(ctype):
    return {"linear" : 1.0,
            "exp" : 1.0,
            "s" : 1.0,
            "step" : 4}.get(ctype, 1.0)

def curve(ctype, domain=None, range_=None, n=None, limits=None):
    ctype = str(ctype).lower()
    domain = domain or (0, 127)
    range_ = range_ or (0.0, 1.0)
    n = n or default_modifier_value(ctype)
    limits = limits or range_
    crv = None
    try:
        crv = {"linear" : identity,
               "exp" : normal_exp_curve,
               "s" : normal_s_curve,
               "step" : normal_step_curve}[ctype]
    except KeyError:
        msg = "Invalid curve type '%s'" % ctype
        raise KeyError(msg)
    xscale = linear_function(domain, (0.0, 1.0))
    yscale = linear_function((0.0, 1.0), range_)
    clipfn = clipper(limits[0], limits[1])
    def fn(x):
        return clipfn(yscale(crv(xscale(x), n)))
    return fn
               
