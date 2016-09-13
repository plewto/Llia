# llia.gui.tk.graph.token
#
#  class Hierarchy:
#
#  Token(dict) 
#    |
#    +---- SynthToken
#    |         |
#    |         +--- EfxToken
#    |         +--- ControllerToken
#    |
#    +---- BusToken
#             |
#             +--- AudioBusToken
#             +--- ControlBusToken

from __future__ import print_function
import abc
from PIL import Image, ImageTk

from llia.gui.tk.graph.graph_config import gconfig


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


class Token(dict):

    def __init__(self, graph, app, client):
        dict.__init__(self)
        self.graph = graph
        self.canvas = graph.canvas
        self.app = app
        self.proxy = app.proxy
        self.client = client
        self._drag_data = [0,0]

    # Drag and drop
    def pickup(self, event):
        # initialize mouse drag
        x, y = event.x, event.y
        self._drag_data[0] = x
        self._drag_data[1] = y

    def drop(self, event):
        # fianlized mouse drag
        self._drag_data[0] = 0
        self._drag_data[1] = 0
        # ISSUE: sync buses here !!!!

    def drag(self, event):
        delta_x = event.x - self._drag_data[0]
        delta_y = event.y - self._drag_data[1]
        self.canvas.move(self.client_id(), delta_x, delta_y)
        self._drag_data[0] = event.x
        self._drag_data[1] = event.y
        
    def is_synth(self):
        # True for synth/efx/controller
        # False for bus
        return False

    def is_efx(self):
        # True only if an efx synth
        return False

    def is_controller(self):
        # True only if is a controller synth
        return False

    def is_audio_bus(self):
        return False

    def is_control_bus(self):
        return False

    def is_protected(self):
        return False
    
    def is_bus(self):
        return self.is_audio_bus() or self.is_controller_bus()

    def keep_hidden(self):
        return False
    
    @abc.abstractmethod
    def client_id(self):
        msg = "%s subclass of Token does not implement client_id()"
        msg = msg % self.__class__
        raise NotImplementedError(msg)

    @abc.abstractmethod
    def render(self):
        msg = "WARNING: %s subclass of Token does not implement render()"
        msg = msg % self.__class__
        #raise NotImplementedError(msg)
        print(msg)
        
    @abc.abstractmethod
    def render_info(self, *_):
        msg = "warning: %s subclass of Token does not implement render_info()"
        msg = msg % self.__class__
        print(msg)

    def clear_info(self, *_):
        self.canvas.delete("info-text")
        
    def _info_header(self, line, text):
        tags = ("info-text", "info-header")
        x = gconfig["info-x"]
        y = gconfig["info-y"] + line * gconfig["info-y-delta"]
        tx = self.canvas.create_text(x,y, text=text, tags=tags,
                                     anchor='w')
        self.canvas.itemconfig(tx,
                               fill = gconfig["info-header-fill"],
                               font = gconfig["info-font"])
        return tx

    def _info_data(self, line, text):
        tags = ("info-text", "info-data")
        x = gconfig["info-x"] + gconfig["info-x-indent"]
        y = gconfig["info-y"] + line * gconfig["info-y-delta"]
        tx = self.canvas.create_text(x,y,text=text,tags=tags,
                                     anchor='w')
        self.canvas.itemconfig(tx,
                               fill = gconfig["info-data-fill"],
                               font = gconfig["info-font"])
        return tx

        
    @abc.abstractmethod
    def highlight(self, *_):
        pass

    @abc.abstractmethod
    def unhighlight(self, *_):
        pass
        
    def status(self, msg):
        self.app.main_window().status(msg)

    def warning(self, msg):
        self.app.main_window().warning(msg)

   
                                     
        
    

    
        
        
