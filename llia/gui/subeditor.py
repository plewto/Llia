# llia.gui.subeditor
# 2016.04.25
# DEPRECIATED

from __future__ import print_function
import abc

from llia.generic import is_subeditor


class SubEditor(object):

    def __init__(self, parent, synth_proxy):
        print("DEPRCIATION warning: llia.gui.subeditor.SubEditor is depreciated")
        super(SubEditor, self).__init__()
        self.parent = parent
        self.synth_proxy = synth_proxy
        self.app = synth_proxy.app
        self._sub_editors = []

    def add_subeditor(self, sed):
        if is_subeditor(sed):
            self._sub_editors.append(sed)
        else:
            msg = "Expected SubEditor, encountered %s" % type(sed)
            raise TypeError(msg)
        
    @abc.abstractmethod
    def as_widget(self):
        pass

    @abc.abstractmethod
    def hide(self):
        pass

    @abc.abstractmethod
    def show(self):
        pass
    
    def status(self, msg):
        self.parent.status(msg)

    def warning(self, msg):
        self.parent.warning(msg)

    def set_aspec(self, param, value):
        for sed in self.sub_editors:
            sed.set_aspect(param, value)

    def sync_ui(self):
        for sed in self._sub_editors:
            sed.sync_ui()

            
@is_subeditor.when_type(SubEditor)
def _is_subed(sed):
    return True
