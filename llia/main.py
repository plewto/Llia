# Llia.main
#

from __future__ import print_function
import os, sys
abs_path = os.path.abspath(__file__)
project_root = os.path.dirname(abs_path)
project_root = os.path.dirname(project_root)
sys.path.insert(1, project_root)

from argparse import ArgumentParser

import llia.constants as constants
from llia.config import LliaConfig
#from llia.api import LliaApp
#import llia.gui.window_factory as wfactory

def banner():
    print(constants.BANNER)
    print("\nversion ",constants.VERSION)
    print()

HM_VERSION="display version and exit."
HM_USAGE = "display detailed usage and exit."
HM_CONFIG = "set config file."
HM_PORTS = "display list of available MIDI ports and exit."
HM_MIDIIN = "set MIDI input port."
HM_MIDIOUT = "set MIDI output port."
HM_BACKEND = "set mido backend, must be either 'mido.backends.rtmidi; or 'mido.backends.portmidi'."
HM_HOST = "set OSC server host address."
HM_PORT = "set OSC server port."
HM_CLIENT = "set ip address where Llia is running."
HM_CLIENT_PORT = "set port number Llia is listing to."
HM_LISTGUI = "list available GUI systems and exit."
HM_GUI = "set GUI."
HM_SKIP_MAINLOOP = "For testing, do not enter application main loop, load modules and exit"

USAGE='''
Llia is an OSC client for SuperCollider.

Command line options:
 
  -h --help      display help message and exit.
  -u --usage     display this message and exit.
  -v --version   display version and exit.
  -p --midi_ports     display available MIDI ports and exit.
  -g --listgui   display GUI options and exit.
  
  -c FILENAME --config FILENAME      ISSUE: portability

          Explicitly set startup configuration file.  If not specified load
          the file contained in the environmental variable LLIA_CONFIG.
          If LLIA_CONFIG is not defined attempt to load a default config
          file from a platform-dependent location.  On Linux the default 
          location is ~/.config/Llia/config.  The default location has
          not yet been established for OSX or Windows.

          In general configuration values have the following order of 
          precedence:

          1) command line 
          2) config file
          3) environmental variable (if defined)
          4) internal default (if defined)


          A suitable configuration file is provided in the Llia resource
          directory.  Copy, or symlink, this file to the default location 
          for your platform.  At a minimum the MIDI input port should 
          be edited. 

  -i PORT --midiin PORT

          Sets MIDI input port.  Use --midi_ports to see a list of available 
          ports.  The MIDI input port is determined first by this command
          line option, then by value in the config file, and lastly by the 
          LLIA_MIDI_IN environmental variable.  There are no internal 
          defaults.

          NOTE: Linux has the annoying habit of changing MIDI port names
                on reboot.

  -o PORT --midiout PORT  
 
          Sets MIDI output port.  Use --midi_ports to see a list of available
          ports.  The MIDI output port is determined first by this command
          line option, then by a value in the config file, next by the 
          LLIA_MIDI_OUT environmental variable.  If none of these values
          are set the MIDI output port defaults to the same value as the
          MIDI input port.

  --backend BACKEND              ISSUE: portability

          Sets MIDI backend used by mido.  The backend is determined first
          by this command line option, then by config file, next by the
          environmental variable LLIA_BACKEND.  Possible values are:

          'rtmidi'  or  'portmidi'

          The default if none of the above are defined is rtmidi.

          IMPLEMENTATION NOTE:
              The mido backend is ultimately set by the environmental 
              variable MIDO_BACKEND.  This variable is updated to 
              reflect values as established above.
         
  --host HOST

          Sets IP address of the OSC server.  The host address is first
          determined by this command line option, next by the configuration
          file, then by the environmental variable LLIA_HOST.  If none of
          these values are set the host address defaults to 127.0.0.1
        
  --port PORT
   
          Sets OSC server port number.  The port number is first determined
          by this command line option, next by the configuration file, 
          then by the environmental variable LLIA_HOST_PORT.  If none of
          these values are set the host port defaults to 57120.
          
  --client CLIENT

          Sets the ip address for OSC responses, IE the address where this 
          Llia client is running.  The address is first determined by this
          command line option, next by the configuration file, then by the
          environmental variable LLIA_CLIENT.  If none of these values 
          are set the default client address is 127.0.0.1

  --client_port PORT

          Sets the port number for OSC clients, IE the port number 
          this instance of Llia is monitoring.  The port number is
          first set by this command line option, next by the config
          file and then by the environmental variable LLIA_CLIENT_PORT
          If none of these values are set the default client port is
          58000.

  --gui GUI

          Selects the GUI system.  Use --listgui for a list of possible
          values.  The GUI system is selected first by this command line
          option, next by the configuration file, and then by the 
          environmental variable LLIA_GUI.  If none of these values are
          defined the TK GUI system is used.

  --skip_main
   
          For testing.  Do not enter application main loop.
          Load modules and exit.

'''

parser = ArgumentParser(description="Llia ~ An OSC client for SuperCollider.")
parser.add_argument("-v", "--version", action="store_true", help=HM_VERSION)
parser.add_argument("-u", "--usage", action="store_true", help=HM_USAGE)
parser.add_argument("-c", "--config", help=HM_CONFIG)
parser.add_argument("-p", "--midi_ports", action="store_true", help=HM_PORTS)
parser.add_argument("-i", "--midiin", help=HM_MIDIIN)
parser.add_argument("-o", "--midiout", help=HM_MIDIOUT)
parser.add_argument("--backend", help=HM_BACKEND)
parser.add_argument("--host", help=HM_HOST)
parser.add_argument("--port", help=HM_PORT)
parser.add_argument("--client", help=HM_CLIENT)
parser.add_argument("--client_port", help=HM_CLIENT_PORT)
parser.add_argument("-g", "--listgui", action="store_true", help=HM_LISTGUI)
parser.add_argument("--gui", help=HM_GUI)
parser.add_argument("--skip_mainloop", action="store_true", help = HM_SKIP_MAINLOOP)


args = parser.parse_args()
if args.version:
    print("Llia version %s.%s.%s" % constants.VERSION)
    sys.exit(0)

if args.usage:
    print(USAGE)
    sys.exit(0)

if args.midi_ports:
    import mido
    print("\nAvailable MIDI input ports:")
    for p in mido.get_input_names():
        print("\t%s" % p)
    print("\nAvailable MIDI output ports:")
    for p in mido.get_output_names():
        print("\t%s" % p)
    print()
    sys.exit(0)

if args.listgui:
    print("\nAvailabe GUI options:")
    for g in constants.GUI_OPTIONS:
        print("\t%-12s%s" % g)
    print()
    sys.exit(0)
    
# banner()    
# llia = LliaApp(LliaConfig.create_instance(args), skip_mainloop=args.skip_mainloop)
# appwin = wfactory.create_main_window(llia)
# llia.add_audio_bus("Alpha")
# echo1 = llia.add_instrument("Echo1", "Echo1", "EFX", 0, "Alpha")
# orgn1 = llia.add_instrument("ORGN", "Pig1", outbus=0)
# #orgn2 = llia.add_instrument("ORGN", "Pig2")
# #saw3 = llia.add_instrument("Saw3")
# appwin.status("Llia...")
# appwin.start_main_loop()



config = LliaConfig.create_instance(args)
from llia.toplevel import LliaTopLevel
import llia.synths.orgn.orgn_proxy
import llia.synths.echo1.echo1_proxy
app = LliaTopLevel(config, True)


# from random import randint
# from time import sleep
# id_ = 1 #randint(0, 10000)
# app.proxy.add_audio_bus("Alpha", 2)
# app.proxy.add_efx("Echo1", id_, inbus="Alpha", outbus=0)
# app.proxy.add_synth("ORGN", id_, outbus=0)

app.start_main_loop()






