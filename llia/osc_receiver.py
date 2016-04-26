# llia.osc_receiver
# 2016.04.23

from __future__ import print_function
import llia.thirdparty.OSC as pyosc

class OSCReceiver(object):

    def __init__(self, oscID, address, port):
        object.__init__(self)
        self._oscID = oscID
        self._server = pyosc.OSCServer((address, port))

    def path(self, tail):
        rs = "/Llia/%s/%s" % (self._oscID, tail)
        return rs

    # fn lambda form  fn(path, tags, args, source)
    #
    def add_handler(self, msg, fn):
        p = self.path(msg)
        self._server.addMsgHandler(p, fn)

    def handle_request(self):
        self._server.handle_request()
        
