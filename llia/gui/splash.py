# llia.gui.splash
# 2016.05.19

from __future__ import print_function

import sys
import mido
import llia.constants as con
import llia.gui.llhelp as lliahelp



pyver = sys.version_info[0]
if pyver <= 2:
    infn = raw_input
else:
    infn = input

    
class TextSplashScreen(object):

    def __init__(self, app):
        self.app = app
        self.config = app.config
        self.main_menu()
        
    def main_menu(self):
        more = True
        while more:
            id_ = self.config["global-osc-id"]
            host = self.config["host"]
            port = self.config["port"]
            client = self.config["client"]
            client_port = self.config["client_port"]
            mrn = self.config["midi-receiver-name"]
            mtn = self.config["midi-transmitter-name"]
            print()
            print("*"*40, end=" ")
            print("Llia Setup\n")
            print("    [0] - Set OSC ID : '%s'" % id_)
            print("    [1] - Set host   : '%s'  port : %s" % (host, port)) 
            print("    [2] - Set client : '%s'  port : %s" % (client, client_port))
            print("    [3] - Set MIDI input port  : '%s'" % mrn)
            print("    [4] - Set MIDI output port : '%s'" % mtn)
            print()
            print("    [?]    - Help")
            print("    [X]    - Continue to Lliascript prompt")
            print("    [Exit] - Exit Llia")
            print("")
            user = infn("Enter Selection > ")
            user = user.upper()
            if user == "0":
                self.select_id()
            elif user == "1":
                self.select_host()
            elif user == "2":
                self.select_client()
            elif user == "3":
                self.select_midi_input_port()
            elif user == "4":
                self.select_midi_output_port()
            elif user == "?":
                self.help_()
            elif user == "X":
                more = False
            elif user == "EXIT":
                print("Bye")
                sys.exit(0)
            else:
                print("ERROR: '%s' ?" % user)

    def select_id(self):
        print("\n\nSelect OSC ID")
        print("Press [Enter] to select default")
        id_ = self.config["global-osc-id"]
        usr = infn("Enter OSC id (%s) > " % id_)
        if usr:
            self.config["global-osc-id"] = usr
                
    def select_host(self):
        while True:
            print("\n\nSelect OSC host address and port")
            print("Press [Enter] to select default")
            h, p = self.config["host"], self.config["port"]
            hst = infn("Enter new host address (%s) > " % h)
            prt = infn("Enter new host port (%s) > " % p)
            if not hst: hst = h
            if not prt: prt = p
            try:
                self.config["port"] = int(prt)
                self.config["host"] = hst
                break
            except ValueError:
                print("ERROR")

    def select_client(self):
        while True:
            print("\n\nSelect OSC client address and port")
            print("Press [Enter] to select default")
            h, p = self.config["client"], self.config["client_port"]
            hst = infn("Enter new client address (%s) > " % h)
            prt = infn("Enter new client port (%s) > " % p)
            if not hst: hst = h
            if not prt: prt = p
            try:
                self.config["client_port"] = int(prt)
                self.config["client"] = hst
                break
            except ValueError:
                print("ERROR")
   

    def select_midi_input_port(self):
        acc = []
        for p in mido.get_input_names():
            acc.append(p)
        while True:
            print()
            mrn = self.config["midi-receiver-name"]
            for n, p in enumerate(acc):
                print("    [%d] %s" % (n+1, p))
            print("\nPress [Enter] to select default")
            usr = infn("Select MIDI input port (%s) > " % mrn)
            if not usr: break
            try:
                n = int(usr)
                if 0 < n <= len(acc):
                    mrn = acc[n-1]
                    self.config["midi-receiver-name"] = mrn
                    break
                else:
                    raise ValueError()
            except ValueError:
                print("ERROR")

    def select_midi_output_port(self):
        acc = []
        for p in mido.get_output_names():
            acc.append(p)
        while True:
            print()
            mrn = self.config["midi-transmitter-name"]
            for n, p in enumerate(acc):
                print("    [%d] %s" % (n+1, p))
            print()
            print("\nPress [Enter] to select default")
            usr = infn("Select MIDI output port (%s) > " % mrn)
            if not usr: break
            try:
                n = int(usr)
                if 0 < n <= len(acc):
                    mrn = acc[n-1]
                    self.config["midi-transmitter-name"] = mrn
                    break
                else:
                    raise ValueError()
            except ValueError:
                print("ERROR")                

    def help_(self):
        text = lliahelp.read_help_file("splash")
        print(text)
        
