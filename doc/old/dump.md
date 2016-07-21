### lliascript dump command

dump(target=None)

Causes both client and server to display diagnostic data about their
respective states.  This is particularly useful if it is suspected the
client and host are no longer in sync.

**ARGS

-    target - Optional String.  There are in general two types of dumps.
     The default is to display global values such as bus, buffer and
     synths.   If a target it relates to a specific synth and must be in
     "synth_id" form (see synth_id help).  The special target "*" may be
     used for the current synth.