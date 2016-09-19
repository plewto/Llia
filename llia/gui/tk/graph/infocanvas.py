# llia.gui.tk.graph.infocanvas

from Tkinter import Canvas

from llia.gui.tk.graph.gconfig import gconfig
import llia.gui.tk.tk_factory as factory

class InfoCanvas(Canvas):


    def __init__(self, graph):
        Canvas.__init__(self, graph)
        self.config(width=gconfig["info-area-width"],
                    height=gconfig["graph-height"],
                    background=gconfig["info-fill"])
        self._current_info_text = ''
        lab_legend = factory.image_label(self, "resources/graph/legend.png")
        lab_legend.place(x=0,y=200)
        
    def clear_info(self):
        self.delete("info")
        self._current_info_text = ''

    def display_info(self, text):
        self.clear_info()
        txt = self.create_text(10,10,
                               text=text,
                               anchor='nw',
                               tags='info',
                               fill=gconfig['info-text-color'],
                               font=gconfig['info-font'])
        self._current_info_text = text

    def append_info(self, text):
        s = "%s\n%s" % (self._current_info_text, text)
        self.display_info(s)
        

    def clear_warning(self):
        self.delete("warning")
        
    def display_warning(self, text):
        self.clear_warning()
        xw = 10
        yw = 100
        txt = self.create_text(xw,yw,
                               text=text,
                               anchor='nw',
                               tags='warning',
                               fill=gconfig['info-warning-color'],
                               font=gconfig['info-warning-font'])
        
