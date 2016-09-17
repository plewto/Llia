# llia.gui.tk.graph.token

from __future__ import print_function
import abc
from PIL import Image,ImageTk

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

    def __init__(self,graph,client):
        dict.__init__(self)
        self.graph = graph
        self.canvas = graph.canvas
        self.app = graph.app
        self.proxy = graph.app.proxy
        self.client = client
        self.selected = False

    @abc.abstractmethod
    def client_id(self):
        msg = "%s subclass of Token does not implement client_id()"
        msg = msg % self.__class__
        raise NotImplementedError(msg)

    @abc.abstractmethod
    def is_synth(self):
        # True if self is -any- sort of synth (synth|efx|controller)
        return False
   
    @abc.abstractmethod
    def is_efx(self):
        # True if self is an efx synth,efx includes controler synths.
        return False

    @abc.abstractmethod
    def is_controller(self):
        # True if self is a controller synth
        return False

    @abc.abstractmethod
    def is_audio_bus(self):
        return False

    @abc.abstractmethod
    def is_control_bus(self):
        return False

    def is_bus(self):
        return self.is_audio_bus() or self.is_control_bus()

    @abc.abstractmethod
    def render(self,*_):
        pass

    @abc.abstractmethod
    def highlight(self, *_):
        pass

    @abc.abstractmethod
    def dehighlight(self, *_):
        pass
