# llia.llscript.lshelp
# 2016.05.09

overview = """ 

lliascript is a simple scripting language used to automate Llia. 
lliasript commands are entered interactively or executed from an external
file.  For more complex operations external Python files may be executed.  

Commands entered interactively are stored to a history which may be saved 
for later execution.

For help enter the line:

    ? topic    or    help topic

For a list of topics enter ? (or help) with out a topic

   ?   or    help


To see a tutorial enter:
    
    ? examples
"""


examples = """
lliascript syntax is extremely simple and never spans more then one line.
Each line is broken into a sequence of tokens delineated by spaces with 
the general form is:

    cmd [arguments...]

where cmd is a command and arguments are zero or more space delineated
values.  

Commands may take required arguments, optional positional arguments or
keyword arguments.  Commands never take both optional position arguments
and keyword arguments; it will be one or the other.

    cmd required-arguments... [optional-arguments...]

     or

    cmd required-arguments... [:keyword value ...]


Comments:

    All text after # on a line is ignored.

"""

comments = """All text on a line after # is ignored."""

abus = """
abus name [channels]

Creates a new audio bus (actually it doesn't really cause a bus to be
created, all buses are created on SuperCollider startup).  

Each audio bus must have a unique name.  If an attempt is made to create a
bus with an existing name a warning message is displayed.  Control buses
and audio buses do not share the same name space and it is possible for
both a control bus and an audio bus to have the same name. 

The optional channels argument sets the number of channels for this bus and
defaults to 1.   

The first several audio buses corresponding to system hardware buses are
automatically created.  The names of these buses have the form: 

    'out_0', 'out_1', ..., 'out_n'

    and 

    'in_0', 'in_1', ..., 'in_n'

See also cbus, ls.
"""

boot = """
boot [server]

Boot SuperCollider server.

optional argument may be one of:
    
     internal  (the default)
     local
     default
"""


cbus = """
cbus name [channels]

Create new control bus (actually it doesn't really cause a bus to be
created, all buses are created on SuperCollider startup).  

Each control bus must have a unique name.  An attempt to create a control
bus with an existing name results in a warning message.  Audio and control
buses do not share the same name space, it is therefore possible for both an
audio bus and a control bus to have the same name.

See also abus, ls
"""

clear_history = """
clear-history

Clears the lliscript history.

See also history
"""

dump = """
dump 

Causes informational dump on both the client and the host.  
This may be useful for diagnostics and for checking that both the client
and host states are consistent. 
"""

efx = """
efx synth-type id inbus [:inbus-offset][:inbus-param][:outbus][:outbus-offset][:outbus-param]

Creates an instance of an effects synth.

An effects synth is used for processing the output of 'normal' synths or
other effects synths and automatically uses the special EFX keymode.
Effects synths MUST be created after any synths which are to serve as
inputs to them. 
 
synth-type - A valid efx synth type  (For available options type: ls efx-types)
id         - An integer index which identifies this specific synth.  For any
             specific synthType id must be unique.  
inbus     -  The name of the primary input audio bus.
:inbus-offset  - int offset from inbus, default 0
:inbus-param   - Synth param for primary input bus, default 'inbus'
:outbus        - Name of primary output bus, default 'out_0'
:outbus-offset - Integer offset from outbus, default 0.
:outbus-param  - Synth param for primary output bus, default 'outbus'

See also synth, ls, with, with-synth
"""

free = """
free

Free LliaHandler and all of it's resource on the SuperCollider host.
Once freed further communication  between client and host is not possible
"""

history = """
history

Display the lliascript command line history.

See also clear-history
"""

id_self = """
id-self

Inform the host what the client's OSC id, ip address and port numbers are. 

NOTE: inform-host is broken and causes bad things.  It is disabled.

see BUG 0001
"""

ls = """
ls target

ls displays a list of various Llia values.  Target should be one of the
following: 

abus        - List assigned audio buses
cbus        - List assigned control buses
buffers     - List assigned buffers
syntns      - List active synths
efx         - List active efx synths
commands    - List all lliscript commands
synth-types - Display valid synth-types, efx-types and keymodes
efx-types   - Same as synth-types
keymodes    - Same as synth-types
"""

panic = """
Request host to stop all sound.
"""

ping = """
Request host to display message that it has received a ping message and
also to return a response message.  ping is used for diagnostics to test
the OSC connection between client and host.
"""

python = """
python filename

Load and execute external python file.  Two objects are passed in the
global name space for the file: app and rs

app - An instance of LliaTopLevel, the top level application.
rs  - An object to pass results back to Llia.

The python facility is in place but not well developed at this time. 

SECURITY WARNING: Running arbitrary python code can be dangerous, run only
trusted code. """

run = """
run filename

Load and execute external lliascript file.
"""

sync = """
sync

Synchronize client state to the host.   If running a GUI update it as well.
sync is automatically called after each interactive lliascript line
executes.   It is not executed for each line of an external lliascript
file.
"""

with_synth = """
with-synth stype id

Select synth as being 'current'.  Some lliascript commands only apply to
the current synth.  Creating synths with either synth or efx automatically
make the new synth the current synth.   The prompt displays the current
synth.

See also synth, efx, ls 
"""

exit_ = """
exit

Shutdown Llia.
"""

buffer_ = """ 
buffer name [:frames][:channels]

Create a new empty buffer. 

name      - A unique name  
:frames   - Number of frames, default 1024.  If buffer is to be used as a
            wave table frames must be a power of 2. 
:channels - Number of channels, default 1

see also with-buffer
"""

with_buffer = """
with-buffer name

Makes named buffer the 'current' buffer.  Some lliascript commands operate
specifically with the current buffer. 

The current buffer is displayed in the lliascript prompt.
"""

buffer_info = """
buffer_info [name]

Display information about the named buffer.  If no name is specified use the
current buffer.
"""

wavetab = """
wavetab name [:harmonics][:decay][:skip][:mode][:cutoff][:depth][:frames] 

Create and fill new buffer.

name - The buffers name must be unique.  The new buffer becomes the
       current-buffer. 
:harmonics - int, maximum number of harmonics, default 64.
:decay     - int, sets amplitude decay rate for upper harmonics.  Harmonic
             amplitude  is amp = 1.0/(freq**decay)  where freq id harmonic 
             frequency.  Default 1.   
:skip      - int, make every nth harmonic have 0 amplitude. 
             Defaults to 1 greater then harmonic count which disables skip. 
:mode      - Simulated filter mode, may be one of: lowpass, highpass,
             bandpass, bandreject or "" (none).  Default "".
:cutoff    - Cutoff/center frequency of simulated filter in terms of
             harmonic number.  Default harmonics/2.
:depth     - Depth of simulated filter 0 < depth <= 1.  Values closer to 0
             have greater effect.  Default 0.5.
:frames    - Number of buffer frames, default 1024.  Wavetable buffer
             lengths must be a power of 2.
             
See also buffer, with-buffer, ?buffer, sinetab, sawtab and pulsetab
"""

sinetab = """
sinetab name [:frames]

A special case version of wavtab for creating sine tables.

See also wavtab, buffer, with-buffer, ?buffer, sawtab and pulsetab
"""

sawtab = """
sawtab name [:harmonics][:frames]

A special case version of wavtab for creating sawtooth tables.

:harmonics - number of harmonics, default 64

See also wavtab, buffer, with-buffer, ?buffer, sintab and pulsetab
"""

pulsetab = """
pulsetab name [:harmonics][:skip][:frames]

A special case version of wavtab for creating pulse wave tables.
:harmonics - default 64
:skip - harmonics to be skipped.  If skip is 1 then all harmonics have
        amplitude 1.  For greater values of skip every nth harmonic is
        missing. 
        skip = 2 -> 50% square wave (the default)
        skip = 3 -> 33% pulse
        skip = 4 -> 25% pulse
        skip = 5 -> 20% pulse
        skip = 6 -> ~17% pulse

See also wavtab, buffer, with-buffer, ?buffer, sintab and sawtab
"""

help_topics = {
    "overview" : overview,
    "examples" : examples,
    "comments" : comments,
    "abus" : abus,
    "boot" : boot,
    "cbus" : cbus,
    "clear-history" : clear_history,
    "dump" : dump,
    "efx" : efx,
    "free" : free,
    "history" : history,
    "id-self" : id_self,
    "ls" : ls,
    "panic" : panic,
    "ping" : ping,
    "python" : python,
    "run" : run,
    "sync" : sync,
    "with-synth" : with_synth,
    "exit" : exit_,
    "buffer" : buffer_,
    "with-buffer" : with_buffer,
    "buffer-info" : buffer_info,
    "wavetab" : wavetab,
    "sinetab" : sinetab,
    "sawtab" : sawtab,
    "pulsetab" : pulsetab
    
    }
