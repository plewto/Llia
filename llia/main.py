# Llia.main
#

from __future__ import print_function
import os, sys, imp, warnings
abs_path = os.path.abspath(__file__)
project_root = os.path.dirname(abs_path)
project_root = os.path.dirname(project_root)
sys.path.insert(1, project_root)


from argparse import ArgumentParser

import llia.constants as constants
from llia.config import LliaConfig
from llia.llia_app import LliaApp


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
HM_NO_SPLASH = "Do not display initial splash menu"
HM_NO_REPL = "Do not enter REPL"

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
          for your platform.  


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

   --nosplash

         Skip initial splash screen.  If a MIDI input port has not been
         specified this flag is ignored.  nosplash is primarily used
         for testing.

   --norepl

        Do not enter REPL.  This option is primarily used for testing and 
        is positively useless if no GUI has been selected.

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
parser.add_argument("--nosplash", action="store_false", help = HM_NO_SPLASH)
parser.add_argument("--norepl", action="store_false", help = HM_NO_REPL)

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
    print("\nAvailable GUI options:")
    for g in constants.GUI_OPTIONS:
        print("\t%-12s%s" % g)
    print()
    sys.exit(0)

config = LliaConfig.create_instance(args)

def _import(modname):
    path = modname.replace(".","/")+".py"
    warnings.filterwarnings("ignore")
    imp.load_source(modname,path)
    warnings.filterwarnings("default")

def _import_synth(stype, modname):
    print("Importing synth: %s" % stype)
    _import(modname)
    constants.SYNTH_TYPES.append(stype)

def _import_effect(stype, modname):
    print("Importing effect: %s" % stype)
    _import(modname)
    constants.EFFECT_TYPES.append(stype)

def _import_controller(stype, modname):
    print("Importing controller: %s" % stype)
    _import(modname)
    constants.CONTROLLER_SYNTH_TYPES.append(stype)     

_import_synth("M","llia.synths.m.m_proxy")        
_import_synth("SS1","llia.synths.ss1.ss1_proxy")    
_import_synth("Io","llia.synths.io.io_proxy")    
_import_synth("Corvus","llia.synths.corvus.corvus_proxy")
_import_synth("Algo","llia.synths.algo.algo_proxy")
_import_synth("Orgn", "llia.synths.orgn.orgn_proxy")
_import_synth("Saw3", "llia.synths.saw3.s3_proxy")
_import_synth("Klstr", "llia.synths.klstr.klstr_proxy")
_import_synth("RDrum", "llia.synths.rdrum.rdrum_proxy")
_import_synth("MASA", "llia.synths.masa.masa_proxy")
_import_synth("FM2", "llia.synths.fm2.fm2_proxy")

_import_effect("Formant","llia.synths.formant.formant_proxy")
_import_effect("CarnalDelay", "llia.synths.carnal.crnl_proxy")
_import_effect("XOver", "llia.synths.xover.xover_proxy")
_import_effect("Flngr", "llia.synths.flngr.flngr_proxy")
_import_effect("Tremolo", "llia.synths.tremolo.trm_proxy")
_import_effect("Mixer", "llia.synths.mixer.mixer_proxy")
_import_effect("Panner", "llia.synths.panner.panner_proxy")
_import_effect("ASplit", "llia.synths.asplit.asplit_proxy")
_import_effect("Rumklang", "llia.synths.rumklang.rumklang_proxy")
_import_effect("Chronos", "llia.synths.chronos.chronos_proxy")
_import_effect("PitchShifter", "llia.synths.pitchshifter.pitchshifter_proxy")
_import_effect("RingModulator", "llia.synths.ringmodulator.rm_proxy")
_import_effect("Crusher", "llia.synths.crusher.crusher_proxy")
_import_effect("Hund", "llia.synths.hund.hund_proxy")
_import_effect("QMod","llia.synths.qmod.qmod_proxy")

_import_controller("LFO1", "llia.synths.lfo1.lfo1_proxy")
_import_controller("LFO2", "llia.synths.lfo2.lfo2_proxy")
_import_controller("LFO3", "llia.synths.lfo3.lfo3_proxy")
_import_controller("Cascade", "llia.synths.cascade.cascade_proxy")
_import_controller("SnH", "llia.synths.snh.snh_proxy")
_import_controller("Ghostbus", "llia.synths.ghostbus.ghost_proxy")
_import_controller("ControlMixer", "llia.synths.controlmixer.controlmixer_proxy")
_import_controller("CUtil", "llia.synths.cutil/cutil_proxy")
_import_controller("Envgen", "llia.synths.envgen.envgen_proxy")

app = LliaApp(config, args.skip_mainloop)
