# llia.gui.tk.graph.token
#

from __future__ import print_function
import abc
from Tkinter import Button
from PIL import Image, ImageTk
from random import randint

import llia.gui.tk.graph.graph_config as gconfig


pallet = gconfig.pallet

_image_cachet = {}

def get_logo_image(sy):
    filename = sy.specs["small-logo"]
    try:
        return _image_cachet[filename]
    except KeyError:
        try:
            img = Image.open(filename)
            photo = ImageTk.PhotoImage(img)
            _image_cachet[filename] = photo
            return photo
        except IOError as err:
            msg = "Can not open logo image '%s'"
            msg = msg % filename
            raise IOError(msg)

class SynthToken(dict):

    def __init__(self, canvas, app, synth):
        self.canvas = canvas
        self.app = app
        self.synth = synth
        x0,y0 = randint(30, 500), randint(30, 500)
        w,h = gconfig.TOKEN_WIDTH, gconfig.TOKEN_HEIGHT
        x1,y1 = x0+w,y0+h
        self["pad"] = canvas.create_rectangle(x0,y0,x1,y1,
                                              tags = (synth.sid, "pad"),
                                              fill = pallet["token-pad-fill"],
                                              outline = pallet["token-outline"],
                                              activeoutline = pallet["token-activeoutline"])
        ipad = gconfig.TOKEN_IMAGE_PAD
        xi, yi = x0+ipad, y0+ipad
        self["image"] = canvas.create_image(xi, yi,
                                            image=get_logo_image(synth),
                                            anchor = "nw",
                                            tags = (synth.sid, "image"))
        
                                                      

        
        
