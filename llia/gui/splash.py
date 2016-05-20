# llia.gui.splash
# 2016.05.19

from __future__ import print_function

import sys
import mido
import llia.constants as con


# Returns ApplicationWindow
#
def create_splash_screen(app, config):
    gui = str(config.gui()).upper()
    if gui == "NONE":
        return _create_text_splash_screen(app, config)
    elif gui == "TK":
        return _create_tk_splash_screen(app, config)
    else:
        print("Using fallback without GUI")
        return _create_text_splash_screen(app, config)

        
def _create_text_splash_screen(app, config):
    from llia.gui.appwindow import DummyApplicationWindow
    pyver = sys.version_info[0]
    if pyver <= 2:
        infn = raw_input
    else:
        infn = input
    # Select MIDI input port
    mrn = config["midi-receiver-name"]
    if not mrn:
        print("\nAvailable MIDI input ports:\n")
        acc = []
        for n,p in enumerate(mido.get_input_names()):
            print("    [%d] %s" % (n, p))
            acc.append(p)
        print()
        selection = None
        limit = len(acc)-1
        while selection is None:
            prompt = "Select MIDI input port [0 - %d] > " % limit
            user = infn(prompt)
            try:
                n = int(user)
                if 0 <= n <= limit:
                    selection = n
            except ValueError:
                pass
        config["midi-receiver-name"] = acc[n]
    print("MIDI Input port: '%s'" % config["midi-receiver-name"])
    # Select MIDI output port
    mtn = config["midi-transmitter-name"]
    if not mtn:
        acc = []
        print("\nAvailable MIDI output ports:\n")
        for n,p in enumerate(mido.get_output_names()):
            print("    [%d] %s" % (n, p))
            acc.append(p)
        print()
        selection = None
        limit = len(acc)-1
        while selection is None:
            prompt = "Select MIDI output port [0 - %d] > " % limit
            user = infn(prompt)
            try:
                n = int(user)
                if 0 <= n <= limit:
                    selection = n
            except ValueError:
                pass
        config["midi-transmitter-name"] = acc[n]
    print("MIDI output port: '%s'" % config["midi-transmitter-name"])
    print("Version %s.%s.%s" % con.VERSION[:3])
    app_window = DummyApplicationWindow(app, config)
    return app_window
                


def _create_tk_splash_screen(config):
    print("DEBUG Crearte TK splash")
            
        
