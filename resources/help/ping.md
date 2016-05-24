### lliascript ping command

ping(target=None)

Test connection between client and host.  The ping command request the
host displays a message in the post window and to also return a message
to the client indicating the ping was received.  If no return message is
received its reasonable to assume the OSC connection between client and host
is broken.

**ARGS

-    target - optional synth_id (see synth_id help).  If a synth is
     specified check connection only for that specific synth.  The special
     syntax "*" may bes used for the current synth.

