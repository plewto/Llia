# llia.gui.tk.graph.infocanvas

from Tkinter import Canvas

from llia.gui.tk.graph.gconfig import gconfig

class InfoCanvas(Canvas):


    def __init__(self, graph):
        Canvas.__init__(self, graph)
        self.config(width=gconfig["info-area-width"],
                    height=gconfig["graph-height"],
                    background=gconfig["info-fill"])
        self._current_info_text = ''

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
        
                                  
            
