# llia.gui.tk.graph.sytoken
#
#  class Hierarchy:
#
#  Token 
#    |
#    +---- SynthToken
#              |
#              +--- EfxToken
#              +--- ControllerToken


# ISSUE:
#   1) On mouse release (Drop) update all buses
#   2) There is a bug, ig the moving icon collides with the info text
#      the program crashes.  One solutino is to use an actual Widget
#      instead of directly rendering info to canvas.
#      Another possibility is to use a seperate canvas for info       



from __future__ import print_function
from random import randint


from llia.gui.tk.graph.graph_config import gconfig
from llia.gui.tk.graph.token import Token, get_logo_image


class SynthToken(Token):

    def __init__(self, graph, app, synth):
        super(SynthToken, self).__init__(graph, app, synth)
        self["width"] = gconfig["synth-token-width"]
        self["height"] = gconfig["synth-token-height"]
        self["pad"] = -1
        self["image"] = -1
        self._drag_data = [0,0]

    def client_id(self):
        return self.client.sid

    def is_synth(self):
        return True
    
    def render(self):
        if not(self.keep_hidden()):
            x0, y0 = randint(30, 500), randint(30, 300)
            x1, y1 = x0+self["width"], y0+self["height"]
            canvas = self.canvas
            synth = self.client
            sid = self.client_id()
            fill = gconfig["synth-fill"]
            outline = gconfig["synth-outline"]
            activeoutline = gconfig["synth-activeoutline"]
            pad = canvas.create_rectangle(x0, y0, x1, y1,
                                          tags = ("pad", "synth", sid),
                                          fill = fill,
                                          outline = outline,
                                          activeoutline = activeoutline)
            x0 = x0 + gconfig["token-image-padding"]
            y0 = y0 + gconfig["token-image-padding"]
            image = canvas.create_image(x0,y0, image = get_logo_image(synth),
                                        anchor='nw',
                                        tags = ("image", "pad", sid))
            self["pad"] = pad
            self["image"] = image
            canvas.tag_bind(image, "<Enter>", self.highlight)
            canvas.tag_bind(image, "<Leave>", self.unhighlight)

            canvas.tag_bind(image, "<B1-Motion>", self.drag)
            canvas.tag_bind(image, "<ButtonPress-1>", self.press)
            canvas.tag_bind(image, "<ButtonRelease-1>", self.drop)
            canvas.tag_bind(image, "<Double-Button-1>", self.display_editor)


    def debug_callback(self, event):
        print("DEBUG CALLBACK")
            
    def show_editor(self, *_):
        sid = self.client_id()
        print("SyToken.show_editor  sid = %s" % sid)
        mw = self.app.main_window()
        mw.raise_synth_editor(sid)
            
    def render_info(self, *_):
        self.clear_info()
        if gconfig["info-enabled"]:
            line = 0
            if self.is_controller():
                header = "Controller: %s"
            elif self.is_efx():
                header = "Effect: %s"
            else:
                header = "Synth: %s"
            self._info_header(line, header % self.client_id())
            # DEBUG FPO
            self._info_data(line+1, "FPO DATA")

    def highlight(self, *_):
        c = gconfig["synth-activeoutline"]
        self.canvas.itemconfig(self["pad"], outline=c)
        self.render_info()
        
    def unhighlight(self, *_):
        c = gconfig["synth-outline"]
        self.canvas.itemconfig(self["pad"], outline=c)
        self.clear_info()

    def press(self, event):
        x, y = event.x, event.y
        self._drag_data[0] = x
        self._drag_data[1] = y

    def drop(self, event):
        self._drag_data[0] = 0
        self._drag_data[1] = 0
        
    def drag(self, event):
        delta_x = event.x - self._drag_data[0]
        delta_y = event.y - self._drag_data[1]
        self.canvas.move(self.client_id(), delta_x, delta_y)
        self._drag_data[0] = event.x
        self._drag_data[1] = event.y


        
    def display_editor(self, *_):
        mw = self.app.main_window()
        sid = self.client_id()
        mw.display_synth_editor(sid)

        
class EfxToken(SynthToken):

    def __init__(self, graph, app, efxsynth):
        super(EfxToken, self).__init__(graph, app, efxsynth)

    def is_efx(self):
        return True

        
class ControllerToken(SynthToken):

    def __init__(self, graph, app, ctrlsynth):
        super(ControllerToken, self).__init__(graph,app, ctrlsynth)

    def is_controller(self):
        return True
