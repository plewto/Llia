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
        self._drag_data = [0,0]
        self._construction_points = {}

    # Token drag and drop
    def pickup_token(self, event):
        x,y = event.x, event.y
        self._drag_data = [x,y]

    def drop_token(self, event):
        self.graph.sync()
        self._drag_data = [0,0]

    def drag_token(self, event):
        x,y = event.x, event.y
        dx = x-self._drag_data[0]
        dy = y-self._drag_data[1]
        self._drag_data[0] = x
        self._drag_data[1] = y
        self.canvas.move(self.client_id(), dx,dy)
        self._create_construction_points(x,y)
        self.canvas.delete("path")  # Hide paths while moving token
        # This s ugly:
        # There are two types of drag-n-drop operations
        # The one here is to move synth/buses around the screen
        # The other is to connect ports to each other
        # The call to graph.clear_drag_and_drop is to prevent
        # the canvas event bindings from interpreting this action
        # as the wrong type of drag and drop
        self.graph.clear_drag_and_drop()
        
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
        # True if self is an efx synth,efx includes controller synths.
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

    @abc.abstractmethod
    def move_to(self, x, y):
        pass
    
    @abc.abstractmethod
    def info_text(self):
        return self.client_id()

    def __str__(self):
        cname = self.__class__.__name__
        s = "%s('%s')" % (cname, self.client_id())
        return s

    def __repr__(self):
        return self.__str__()
