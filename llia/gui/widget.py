# llia.gui.widget.py
# 2016.04.25


import abc


class AbstractWidget(object):

    def __init__(self):
        super(AbstractWidget, self).__init__()

    
DUMMY_WIDGET = AbstractWidget()
