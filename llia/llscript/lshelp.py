# llia.llscript.lshelp
# 2016.05.09

# ********************************************************************
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


# ********************************************************************
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

# ********************************************************************
comments = """All text on a line after # is ignored."""

# ********************************************************************
abus = """
abus name [:channels :nodup]

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

See also cbus, ls, assign
"""

# ********************************************************************
boot = """
boot [server]

Boot SuperCollider server.

optional argument may be one of:
    
     internal  (the default)
     local
     default
"""


# ********************************************************************
cbus = """
cbus name [:channels :nudup]

Create new control bus (actually it doesn't really cause a bus to be
created, all buses are created on SuperCollider startup).  

Each control bus must have a unique name.  An attempt to create a control
bus with an existing name results in a warning message.  Audio and control
buses do not share the same name space, it is therefore possible for both an
audio bus and a control bus to have the same name.

BUG 0000 WARNING: 
    the first control bus created is not recognized by the client until
    after a second bus has been created.

    cbus foo    # foo exists on the server but the client doesn't think so.
    cbus bar    # After bar is created the client is able to see foo.

See also abus, ls, assign
"""

# ********************************************************************
clear_history = """
clear-history

Clears the lliscript history.

See also history
"""

# ********************************************************************
dump = """
dump [*]

Causes informational dump on both the client and the host.  
This may be useful for diagnostics and for checking that both client
and host states are consistent. 

If the optional '*' argument is present, display information about the
current synth.
"""

# ********************************************************************
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

See also synth, ls, with-synth, assign
"""

# ********************************************************************
free = """
free

Free LliaHandler and all of it's resource on the SuperCollider host.
Once freed further communication  between client and host is not possible
"""

# ********************************************************************
history = """
history

Display the lliascript command line history.

See also clear-history
"""

# ********************************************************************
id_self = """
id-self

Inform the host what the client's OSC id, ip address and port numbers are. 

NOTE: inform-host is broken and causes bad things.  It is disabled.

see BUG 0001
"""

# ********************************************************************
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

# ********************************************************************
panic = """
Request host to stop all sound.
"""

# ********************************************************************
ping = """
ping [*]

Request host to display 'ping received' message and send a response.
Ping is used to test the connection between client and host.

If the client does not receiver an appropriate response a warning message
is displayed.  In batch mode the script is terminated.

Ping takes two forms:

    ping      - Test top level host/client connection
    ping *    - Test host/client connection for the current synth     
"""

# ********************************************************************
python = """
python filename

Load and execute external python file.  Two objects are passed in the
global name space for the file: app and rs

app - An instance of LliaTopLevel, the top level application.
rs  - An object to pass results back to Llia.

The python facility is in place but not well developed at this time. 

SECURITY WARNING: Running arbitrary python code can be dangerous, run only
trusted code. """

# ********************************************************************
batch = """
batch filename

Load and execute external lliascript file.
"""

# ********************************************************************
sync = """
sync

Synchronize client state to the host.   If running a GUI update it as well.
sync is automatically called after each interactive lliascript line
executes.   It is not executed for each line of an external lliascript
file.
"""

# ********************************************************************
with_synth = """
with-synth stype id

Select synth as being 'current'.  Some lliascript commands only apply to
the current synth.  Creating synths with either synth or efx automatically
make the new synth the current synth.   The prompt displays the current
synth.

See also synth, efx, ls 
"""

# ********************************************************************
synth = """
synth stype id [:keymode][:voice-count][:outbus][:outbus-offset][:outbus-param]

Creates a new synth instance.

stype - The synthesizer type.
        Use 'ls synth-types' to see list of available synthesizers.
id    - Integer id. The id value MUST be unique for any given stype.  
        Two synths may have the same id if they are of different types.
:keymode       - To see a list of available keymodes type 'ls keymodes'
                 Default 'Poly1'
:voice-count   - int number of voices to allocated. Whether voice-count
                 is used is dependent on the keymode.  For Poly1, Mono1 and 
                 EFX keymodes the voice count is ignored. Default 8.
:outbus        - The outbus audio bus, defaults to 'out_0'
:outbus-offset - An integer offset added to outbus index, default 0.
:outbus-param  - Synth parameter used for output bus, default 'outbus'.

See also efx, ls, with-synth, assign
"""

# ********************************************************************
exit_ = """
exit

Shutdown Llia.
"""

# ********************************************************************
buffer_ = """ 
buffer name [:frames :channels :nodup]

Create a new empty buffer. 

name      - A unique name  
:frames   - Number of frames, default 1024.  If buffer is to be used as a
            wave table frames must be a power of 2. 
:channels - Number of channels, default 1

See also with-buffer, ls, assign
"""

# ********************************************************************
with_buffer = """
with-buffer name

Makes named buffer the 'current' buffer.  Some lliascript commands operate
specifically with the current buffer. 

The current buffer is displayed in the lliascript prompt.
"""

# ********************************************************************
buffer_info = """
buffer_info [name]

Display information about the named buffer.  If no name is specified use the
current buffer.
"""

# ********************************************************************
wavetab = """
wavetab name [:harmonics :decay :skip :mode :cutoff :depth :frames :nodup]

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

# ********************************************************************
sinetab = """
sinetab name [:frames :nodup]

A special case version of wavtab for creating sine tables.

See also wavtab, buffer, with-buffer, ?buffer, sawtab and pulsetab
"""

# ********************************************************************
sawtab = """
sawtab name [:harmonics :frames :nodup]

A special case version of wavtab for creating sawtooth tables.

:harmonics - number of harmonics, default 64

See also wavtab, buffer, with-buffer, ?buffer, sintab and pulsetab
"""

# ********************************************************************
pulsetab = """
pulsetab name [:harmonics :skip :frames :nodup]

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

# ********************************************************************
assign = """
assign entity name to param [:offset]

Assign buffer or bus to current-synth parameter.

entity  - Selects type of object to be assigned, must be one of:
          'abus', 'cbus' or 'buffer'.  
name    - The name of the bus or buffer to be assigned. 
to      - The literal word 'to'
param   - The synth parameter the bus or buffer is assigned to.  
          No checks are made to ensure param is valid.
:offset - An optional offset added to the bus index, default 0.

BUG 0000 WARNING: 
   If only a single control bus has been created the
   the client app does not recognize it.  The following
   valid lliascript code does not work (valid assuming a
   there is a synth type 'Spam' with a parameter 'foo')


          cbus eggs       # client does not recognize eggs exists
          synth Spam 1
          assign cbus eggs to foo


  As a work around a 2nd control bus can be created.


          cbus eggs
          cbus dummy      #  client now recognizes eggs
          synth Spam 1
          assign cbus eggs to foo

See also abus, cbus, buffer
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
    "batch" : batch,
    "sync" : sync,
    "synth" : synth,
    "with-synth" : with_synth,
    "exit" : exit_,
    "buffer" : buffer_,
    "with-buffer" : with_buffer,
    "buffer-info" : buffer_info,
    "wavetab" : wavetab,
    "sinetab" : sinetab,
    "sawtab" : sawtab,
    "pulsetab" : pulsetab,
    "assign" : assign
    }
