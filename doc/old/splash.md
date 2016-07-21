### Llia Splash Screen.

The initial Llia screen allows adjustment of key OSC and MIDI parameters
with initial defaults determined by one of several sources.  In order of
highest to lowest priority these sources are: command line options,
configuration file and environmental variables.  Once past the splash screen
these values are fixed throughout the duration of the application and may
not be changed. .



**OSC id** - The OSC id is a unique string which identifies the specific
  invocation of Llia.  Both the client and server applications must have
  matching OSC ids.  The default ID is *“llia”* and as long as only one
  instance of Llia is running there is no reason to change it.

-  The default OSC id is established by configuration file value [OSC]global-id 


**Host address and port** - Sets the IP address and port number of the
  Supercollider host.  The default host address and port are set in the 
  following locations:


-    Command line options --host and --port
-    Configuration file values [OSC]host-address and [OSC]host-port
-    Environmental variables LLIA_HOST and LLIA_HOST_PORT 
   

**Client address and port** - Sets the IP address and port number for the
  client application.  The default client address and port are set in the
  following locations:


-    Command line options  --client and --client_port
-    Configuration file values [OSC]client-address and [OSC]client-port
-    Environmental variables LLIA_CLIENT and  LLIA_CLIENT_PORT


**MIDI input device** - Selects one of the available devices for MIDI input.  
  The default MIDI input device is set in the following locations:

-    Command line options -i  or --midiin
-    Configuration file value [MIDI]input-port
-    Environmental variable LLIA_MIDI_IN

**Special note for Linux:**  Linux has the annoying habit of not being
consistent with MIDI device names between reboots.  This means that values
set in the configuration file or by environmental variables can not be
relied upon after the system reboots.  Use the command line option -p to
see a list of available MIDI devices.


**MIDI output device** - Selects one of the available devices for MIDI
  output.  The initial version of Llia does not make use of MIDI output.
  This parameter is provided for future expansion.  The default MIDI
  output port is set in the following locations:

-    Command line options -o or --midiout
-    Configuration file value [MIDI]output-port
-    Environmental variable LLIA_MIDI_OUT