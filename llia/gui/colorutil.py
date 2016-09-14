# llia.gui.colorutil
# Utility for creating list of related colors.
#

from __future__ import print_function
from colorsys import *
from random import random

def hue_cycle(h):
    '''
    Wrap out of bounds color hue to valid range (0,1)
    '''
    while h > 1:
        h = h - 1
    while h < 0:
        h = h + 1
    return h


class Color(object):

    def __init__(self, h=0.0, s=0.0, v=0.0):
        '''
        Creates Color object specified by hue, saturation and value.
        All arguments are floats between 0.0 and 1.0.
        '''
        self._hsv = [h,s,v]

    def __len__(self):
        return len(self._hsv)
        
    @staticmethod
    def rgbcolor(r=0.0,g=0.0,b=0.0):
        '''
        Create Color object by RGB values.
        All arguments are floats between 0.0 and 1.0
        '''
        h,s,v = rgb_to_hsv(r,g,b)
        return Color(h,s,v)

    @staticmethod
    def hexcolor(x):
        '''
        Creates Color object by hex string specification.
        The string forms is '#rrggbb'  where rr,gg and bb are
        hex values between 00 and ff.
        '''
        def fail():
            msg = "Invalid color string: '%s'" % x
            raise ValueError(msg)
        if len(x) == 7:
            if x[0] != '#': fail()
            try:
                r,g,b = int(x[1:3],16), int(x[3:5],16), int(x[5:7],16)
                r,g,b = r/255.0, g/255.0, b/255.0
                return Color.rgbcolor(r,g,b)
            except ValueError:
                fail()
        else:
            fail()

    @staticmethod
    def random_color():
        '''
        Returns a new Color object with random values.
        '''
        h, s, v = random(), random(), random()
        return Color(h,s,v)
            
    @staticmethod
    def _map_index(i):
        j = str(i).upper()
        d = {"H" : 0,
             "S" : 1,
             "V" : 2,
             "R" : 3,
             "G" : 4,
             "B" : 5}
        index = d.get(j,i)
        return index

    def __getitem__(self, index):
        '''
        Get color component.  
        index may be either numeric or symbolic.
        index  0 "H"  -> hue
               1 "S"  -> saturation
               2 "V"  -> value
               3 "R"  -> red component
               4 "G"  -> green component
               5 "B"  -> blue component
        Returns float between 0.0 and 1.0.
        '''
        index = Color._map_index(index)
        if index > 2:
            rgb = self.as_rgb()
            return rgb[index-3]
        else:
            return self._hsv[index]

    def __setitem__(self, index, value):
        '''
        Set specific color component.
        Index usage is same as with __getitem__
        value is a float between 0.0 and 1.0
        '''
        index = Color._map_index(index)
        if index > 2:
            rgb = list(self.as_rgb())
            rgb[index-3] = value
            self._set_rgb(rgb)
        else:
            self._hsv[index] = value

    def clone(self):
        '''
        Return new Color object which is clone of self.
        '''
        return Color(self[0],self[1],self[2])
            
    def _set_rgb(self, rgb):
        h,s,v = rgb_to_hsv(rgb[0],rgb[1],rgb[2])
        self._hsv[0] = h
        self._hsv[1] = s
        self._hsv[2] = v
            
    def as_rgb(self, update=None):
        '''
        Return/set RGB values.
        
        update - optional list [R,G,B]

        returns list [R,G.B]
        '''
        if update:
            self._set_rgb(update)
        h,s,v = self[0],self[1],self[2]
        return hsv_to_rgb(h,s,v)

    def _set_hex(self, x):
        other = Color.hexcolor(x)
        for i in range(len(self)):
            self._hsv[i] = other._hsv[i]
    
    def as_hex(self, update=None):
        '''
        Return/set color by hex string
        update - optional string "#rrggbb"
        returns String
        '''
        if update:
            self._set_hex(update)
        acc = '#'
        for v in self.as_rgb():
            v = int(v * 255)
            x = hex(v)[2:]
            if len(x) == 1: x = '0'+x
            acc += x
        return acc.upper()

    def invert(self):
        '''
        Invert self.
        '''
        r,g,b = self.as_rgb()
        self.as_rgb([1.0-r, 1.0-g, 1.0-b])
        return self
        
    def complement(self):
        '''
        Set self to complement.
        '''
        h = self._hsv[0] + 0.5
        h = hue_cycle(h)
        self._hsv[0] = h
        return self

    def darker(self, n=1):
        '''
        darken self, 
        n sets degree of darkening.
        
        c.darker(2)  <-->  c.darker().darker()
        '''
        shift = n*0.1
        v = min(1.0, max(0, self._hsv[2]-shift))
        self._hsv[2] = v
        return self

    def brighter(self, n=1):
        '''
        brighten self.
        n sets degree of brightening
        
        c.brighter(2)  <--> c.brighter().brighter()
        '''
        return self.darker(-n)

    def desaturate(self, n=1):
        '''
        Reduce saturation 
        n - degree of desaturation
        '''
        shift = n*0.1
        s = min(1.0, max(0, self._hsv[1]-shift))
        self._hsv[1] = s
        return self

    def saturate(self, n=1):
        '''
        Increase saturation
        n - degree of saturation
        '''
        return self.desaturate(-n)

    def shift(self, n=0.05):
        '''
        Shift hue of self
        '''
        h = self._hsv[0] + n
        h = hue_cycle(h)
        self._hsv[0] = h
        return self

    def __str__(self):
        acc = "Color HSV["
        frmt = "%5.3f"
        for i,v in enumerate(self._hsv):
            acc += frmt % v
            if i < len(self): acc += ", "
        acc += "] RGB["
        for i,v in enumerate(self.as_rgb()):
            acc += frmt % v
            if i < len(self): acc += ", "
        acc += "] Hex"
        acc += self.as_hex()
        return acc

    @staticmethod
    def gradient(c1, c2, n=8):
        '''
        Generates list by interpolating between two colors.
        c1 and c2 are Color object
        n is number of intermediate colors (including c1 but not c2)
        Returns list.
        '''
        h1,s1,v1 = c1[0],c1[1],c1[2]
        h2,s2,v2 = c2[0],c2[1],c2[2]
        dh,ds,dv = float(h2-h1)/n,float(s2-s1)/n,float(v2-v1)/n
        h,s,v = h1,s1,v1
        acc = []
        for i in range(n):
            c = Color(h,s,v)
            acc.append(c)
            h = hue_cycle(h + dh)
            s = min(max(0,s+ds),1)
            v = min(max(0,v+dv),1)
        return acc

    @staticmethod
    def complements(c1):
        '''
        Returns list of a color and it's complement.
        '''
        c2 = c1.clone().complement()
        return [c1,c2]

    @staticmethod
    def split_complements(c1):
        '''
        Returns lits of three colors, the source color and two 
        colors equal-distant from the complement of the source color.
        '''
        c2 = c1.clone()
        c3 = c1.clone()
        h1 = c1[0]
        h2 = hue_cycle(h1 + 0.433)
        h3 = hue_cycle(h1 + 0.567)
        c2[0] = h2
        c3[0] = h3
        return [c3,c1,c2]

    @staticmethod
    def triads(c1):
        '''
        Returns list of 3 equally spaced colors
        '''
        h1 = c1[0]
        h2 = hue_cycle(h1+0.333)
        h3 = hue_cycle(h1+0.667)
        c2 = c1.clone()
        c3 = c1.clone()
        c2[0] = h2
        c3[0] = h3
        return [c1,c2,c3]

    @staticmethod
    def tetrads(c1):
        '''
        Returns list of 4 equally spaced colors
        '''
        h1 = c1[0]
        h2 = hue_cycle(h1+0.25)
        h3 = hue_cycle(h1+0.50)
        h4 = hue_cycle(h1+0.75)
        c2 = c1.clone()
        c3 = c1.clone()
        c4 = c1.clone()
        c2[0] = h2
        c3[0] = h3
        c4[0] = h4
        return [c1,c2,c3,c4]

    @staticmethod
    def analogous(c1):
        '''
        Return list of a color and 2 analog colors.
        '''
        h1 = c1[0]
        h2 = hue_cycle(h1+0.083)
        h3 = hue_cycle(h1+0.920)
        c2 = c1.clone()
        c3 = c1.clone()
        c2[0] = h2
        c3[0] = h3
        return [c1,c2,c3]

    @staticmethod
    def monochromatic(c1, n=8, darken=True):
        '''
        Return list of monochromatic variations on color.
        '''
        c1 = c1.clone()
        acc = []
        for i in range(8):
            acc.append(c1)
            c1 = c1.clone()
            if darken:
                c1.darker(1)
            else:
                c1.brighter(1)
        return acc
            
